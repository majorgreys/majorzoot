#!/usr/bin/env python

from pyzotero import zotero
import click
import ConfigParser
import os
import shelve

APP_NAME = 'majorzoot'

def read_config():
    cfg = os.path.join(click.get_app_dir(APP_NAME), 'config.ini')
    parser = ConfigParser.RawConfigParser()
    parser.read([cfg])
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv['%s.%s' % (section, key)] = value
    return rv

def get_items(library):
    config = read_config()
    zot = zotero.Zotero(config['%s.library_id' % library],
                        config['%s.library_type' % library],
                        config['%s.api_key' % library])
    version = zot.last_modified_version()
    store = shelve.open(os.path.join(click.get_app_dir(APP_NAME), '%s.cache' % library))
    if store.has_key(str(version)):
        return store[str(version)]
    else:
        click.echo('Refreshing cache')
        num_items = zot.num_items()
        limit = 100
        all_items = []
        for start in range(1, num_items, limit):
            if start + limit > num_items:
                limit = num_items - start + 1
            items = zot.items(start=start, limit=limit)
            all_items.extend(items)
        store[str(version)] = all_items
        store.close()
        # TODO: clear old version?
        return all_items

@click.group()
def cli():
    pass

@click.command()
@click.option('--library',
              default=read_config().items()[0][0].split('.')[0], # default to first library in config
              help='Name of Zotero library')
def listauthors(library):
    click.echo('Listing authors for %s' % library)
    items = get_items(library)
    click.echo(len(items))
    #click.echo(set([c['creatorType'] for c in creators]))

cli.add_command(listauthors)
