# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE

import click
from terminaltables import SingleTable

from ..utils import with_cr
from ..main import odoo


def _select(version, args=False, relations=False):
    select_list = ["""
    SELECT
        CASE
            WHEN imf.required IS TRUE then '[R] '||imf.name ELSE imf.name
        END field_name,
        imf.ttype field_type,
        imd.module module
    """]
    if args:
        args_str = """
        '['
        || CASE WHEN imf.required = 't' THEN 'REQUIRED, ' ELSE '' END
        || CASE WHEN imf.readonly = 't' THEN 'READONLY, ' ELSE '' END
        """
        if version > 8:
            args_str += """
            || CASE WHEN imf.related IS NOT NULL THEN 'RELATED, ' ELSE '' END
            || CASE WHEN imf.store = 't' THEN 'STORED, ' ELSE '' END
            || CASE WHEN imf.copy = 't' THEN 'COPY, ' ELSE '' END
            """
        args_str += """
        || ']' attrs
        """
        select_list.append(args_str)
    if relations:
        relations_str = """
        CASE
        """
        if version > 8:
            relations_str += """
            WHEN imf.related IS NOT NULL
                THEN '->.-> ' || imf.related ||
                    ' (' || COALESCE(imf.relation, '') ||')'
            WHEN imf.ttype ~ 'one2many' AND imf.related IS NOT NULL
                THEN '<- ' || imf.related || ' (' || imf.relation ||')'
            WHEN imf.ttype ~ 'many2many'
                THEN '<- ' || imf.column1 || '.' ||
                    replace(imf.relation_table, '.', '_')|| '.' ||
                    imf.column2 || ' -> (' || imf.relation ||')'
            """
        relations_str += """
            WHEN imf.ttype ~ 'one2many'
                THEN '<- '||replace(imf.relation, '.', '_')||'.'||
                    imf.relation_field  || ' (' || imf.relation ||')'
            WHEN imf.ttype ~ 'many2one'
                THEN '-> '||replace(imf.relation, '.', '_') ||
                    ' (' || imf.relation ||')'
            ELSE ''
        END relational
        """
        select_list.append(relations_str)
    return (",").join(select_list)


def _from():
    from_str = """
    FROM ir_model_fields imf
    JOIN ir_model_data imd
        ON imd.res_id = imf.id
            AND imd.model = 'ir.model.fields'
    """
    return from_str


def _where(model, match=False):
    where_list = ["""
    WHERE imf.model ~* '^%(model)s$'
    """]
    where_params = {
        'model': model,
    }
    if match:
        where_list.append("""
        imf.name ~* '%(fname)s'
        """)
        where_params.update({
            'fname': match,
        })
    where_str = (" AND ").join(where_list)
    return where_str % where_params


def _group_by():
    group_by_str = """
    """
    return group_by_str


def _order_by():
    # TODO Optional sorting
    order_by_str = """
    ORDER BY imf.name
    """
    return order_by_str


def _get_odoo_version(cr):
    version_query = """
    SELECT latest_version FROM ir_module_module WHERE name='base'
    """
    cr.execute(version_query)
    full_version = cr.fetchone()[0]
    version_as_int = int(full_version.split('.')[0])
    return version_as_int


def _get_databases(ctx, args, incomplete):
    def _filter_db(dbname):
        return incomplete in dbname

    try:
        cmd = [
            "psql", "-l", "-A", "-F','", "-R';'", "-t"
        ]
        proc = Popen(cmd, stdout=PIPE)
        proc.wait()
        bases_data = proc.stdout.read().decode()
        databases = [row.split(",")[0].strip("'") for
                     row in bases_data.split(";")]
        return filter(_filter_db, databases)
    except BaseException as e:
        return []


def _get_models(ctx, args, incomplete):
    database = args[-1]

    @with_cr
    def _fetch_models(database, cr=False):
        if not cr:
            return []

        query = """
        SELECT im.model
        FROM ir_model im
        WHERE im.model ~* %(model)s
        ORDER BY im.model
        """
        query_vals = {
            'model': incomplete,
        }
        cr.execute(query, query_vals)
        fetch = cr.fetchall()
        return [row[0] for row in fetch]

    return _fetch_models(database=database)


@odoo.command()
@click.argument('database', autocompletion=_get_databases)
@click.argument('model', autocompletion=_get_models)
@click.option('-a', '--args',
              help="Whether the field is Required, Related, Readonly, " +
              "Stored, Copyable.", is_flag=True)
@click.option('-r', '--relations',
              help="Information of the Foreing Keys to take in account.",
              is_flag=True)
@click.option('-f', '--filter', 'filter_',
              help="Show only fields matching pattern.")
@click.option('-v', '--verbose',
              help="Show all information available.", is_flag=True)
@with_cr
def fields(model, database, args, relations, filter_, verbose, cr=False):
    """
    Human explain of fields available in <model>
    """
    if not cr:
        click.echo("\nError: Could not connect to database %s" % database)
        return
    if verbose:
        args = True
        relations = True

    try:
        odoo_version = _get_odoo_version(cr)
    except BaseException as err:
        click.echo(err)
        msg = "\nError: Could not recognize the database as an Odoo DB"
        click.echo(msg)

    query = """
    %(select)s
    %(from)s
    %(where)s
    %(group_by)s
    """
    query_params = {
        'select': _select(odoo_version, args=args, relations=relations),
        'from': _from(),
        'where': _where(model, match=filter_),
        'group_by': _group_by(),
    }
    cr.execute(query % query_params)

    regs = cr.fetchall()
    header = [('\33[32m' + col.name + '\x1b[0m') for col in cr.description]
    regs.insert(0, header)
    table = SingleTable(regs)
    click.echo(table.table)
