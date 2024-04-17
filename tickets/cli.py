# -*- coding: utf-8 -*-
import os.path

import click
import yaml

from .loader_dispatcher import LoadDispatcher
from .raw_orders import RawOrderCleaner
from .transfers import TransferCleaner


@click.group()
def cli():
    ...


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
def clean_orders(input_file: str):
    cleaner = RawOrderCleaner()
    df = cleaner.read_raw(input_file)
    cleaner.save(df)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
def clean_transfers(input_file: str):
    cleaner = TransferCleaner()
    df = cleaner.read_raw(input_file)
    cleaner.save(df)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
def load_task(input_file: str):
    with open(input_file, 'r', encoding='utf-8') as f:
        task_defs = yaml.load(f, Loader=yaml.SafeLoader)

    base_dir = os.path.dirname(input_file)

    defs = task_defs.get('imports', list())

    dispatcher = LoadDispatcher()
    dispatcher.load_data(defs, base_dir=base_dir)
