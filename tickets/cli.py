# -*- coding: utf-8 -*-
import click

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
