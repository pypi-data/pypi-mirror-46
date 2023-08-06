# -*- coding: utf-8 -*-
import os
import click
import subprocess

from ..main import bash
from .download_dump import _download_dump

@bash.command()
@click.argument('database')
@click.argument('dump', default=False)
@click.option('-v', '--verbose',
              help="Show all information available.", is_flag=True)
@click.option('-r', '--remove_dump',
              help="Remove dump after restore.", is_flag=True)
@click.option('-b', '--bucket',
              help="Bucket for AWS.", default='e2-production')
def restoredb(database, dump, verbose, remove_dump, bucket):
    """
    Restore a DB, droping it if exists, and runs auto-clean.
    """
    display_mode = subprocess.DEVNULL
    if verbose:
        display_mode = 0
    if not dump:
        remove_dump = True
        dump = _download_dump(database, bucket)
    print('--> Droping DB (if exists) ', end = '', flush=True)
    pd = subprocess.Popen(['dropdb', '--if-exists', database], stdout=display_mode, stderr=display_mode)
    pd.wait()
    print ('\33[92m' + 'Success!' + '\x1b[0m')
    print('--> Creating DB ', end = '', flush=True)
    pc = subprocess.Popen(['createdb', database], stdout=display_mode, stderr=display_mode)
    pc.wait()
    print ('\33[92m' + 'Success!' + '\x1b[0m')
    print('--> Restoring DB ', end = '', flush=True)
    pg = subprocess.Popen(['gunzip', '-c', dump], stdout=subprocess.PIPE)
    pp = subprocess.Popen(['psql', '-d', database], stdin=pg.stdout, stdout=display_mode, stderr=display_mode)
    pg.stdout.close()
    output = pp.communicate()[0]
    pp.wait()
    print ('\33[92m' + 'Success!' + '\x1b[0m')
    print('--> Cleaning Data ', end = '', flush=True)
    auto_clean_path = os.path.join(os.path.dirname(__file__), '../templates/auto_clean.sql')
    pa = subprocess.Popen(['psql', '-d', database, '-f', auto_clean_path], stdout=display_mode, stderr=display_mode)
    pa.wait()
    print ('\33[92m' + 'Success!' + '\x1b[0m')
    if remove_dump:
        rm = subprocess.Popen(['rm', dump], stdout=display_mode, stderr=display_mode)
        rm.wait()
    print('Goodbye!')
