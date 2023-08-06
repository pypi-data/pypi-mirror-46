import click
from . import cryo_save_impl, inspect_impl

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {}

@cli.command()
@click.pass_context
@click.option('--force', '-f', is_flag = True, default = False)
@click.argument('xp_name')
@click.argument('cryo_name')
def cryo_save(ctx, xp_name, cryo_name, force):
    cryo_save_impl(xp_name, cryo_name, force)

@cli.command()
@click.pass_context
@click.argument('filename')
@click.argument('layer')
@click.argument('component')
def inspect(ctx, filename, layer, component):
    """FILENAME is a path to a directory where the statdict and meta files are stored
       LAYER is a path to some layer, for example net.Conv2d

       COMPONENT name of part of the layer, like weights or bias"""
    inspect_impl(filename, layer, component)

    
def main():
    return cli()
