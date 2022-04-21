import logging
import logging.config

import click
import dotenv

LEVEL_CLI = 21  # level above info|20
logging.addLevelName(level=LEVEL_CLI, levelName='CLI')


class MetadataNotFound(Exception):
    """Exception to raise when the metadata file cannot be found in the given
    path"""
    def __init__(self, message: str):
        Exception.__init__(self, message)


@click.group()
@click.option('--metapath', required=False,
              default='metadata.json', show_default=True,
              help='Path to metadata JSON file')
@click.option('--envpath', required=False,
              default='./.env', show_default=True,
              help='Path to dotenv file')
@click.option('--lconfig', required=False,
              default='logger.json', show_default=True,
              help='Logging JSON configuration file')
@click.option('--memory', required=False,
              default=8, show_default=True,
              help='Amount of memory to allocate for PySpark')
@click.pass_context
def cli(ctx, metapath, envpath, lconfig, memory):
    import os

    from {{ cookiecutter.name_pymodule }}.utils import ReadMeta
    from {{ cookiecutter.name_pymodule }}.utils import setup_logger

    # SETUP LOGGER
    setup_logger(lconfig)

    logger = logging.getLogger(__name__)
    ctx.obj['LOGGER'] = logger
    logger.info(f'_____ START CLI EXECUTION')

    # SETUP METADATA
    if os.path.exists(metapath):
        meta = ReadMeta(metapath)
        ctx.obj['METADATA'] = meta
    else:
        raise MetadataNotFound(f'Could not find metadata file in path {metapath}')

    ctx.obj['MEMORY'] = memory

    # SETUP ENVFILE
    if os.path.exists(envpath):
        dotenv.load_dotenv(dotenv.find_dotenv(envpath))
    else:
        logger.warning(f'Dotenv not found in the path {envpath}')


@cli.command()
@click.pass_context
def get_dates(ctx):
    """Example command line interface using click"""

    from {{ cookiecutter.name_pymodule }}.utils import ReadMeta
    from {{ cookiecutter.name_pymodule }}.dataprep import Preprocess, LoadData
    from {{ cookiecutter.name_pymodule }}.models import MyModel

    loader = LoadData()
    X, y = loader.base()

    model = MyModel(param=0)
    model.fit(X=X, y=y)
    preds = model.predict(X=[1, 1, 1])
    print(preds)


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
