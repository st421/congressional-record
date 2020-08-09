import os
import logging
from datetime import datetime, timedelta
import click
from congressionalrecord.clients.govinfo import GovInfoClient
from congressionalrecord.clients.congress import CongressClient
from congressionalrecord.cr import YieldingCRManager, LocalJsonCRManager
from congressionalrecord.utils import DATE_FORMAT

API_KEY = os.environ.get("GOVINFO_API_KEY")

#FIXME should be able to exclude more than one

@click.command()
@click.option('--start', type=click.DateTime(), default=datetime.strftime(datetime.today(), DATE_FORMAT), help='The day or first day of Record text you want to download. (Format: YYYY-MM-DD)')
@click.option('--end', type=click.DateTime(), help='The last day in a contiguous series of days user wants to download. Note the parser skips days with no activity. (Format: YYYY-MM-DD)')
@click.option('--source', type=click.Choice(['govinfo', 'congress']), default='govinfo', help='Where to get the congressional record from')
@click.option('--mode', '-M', type=click.Choice(['json', 'es', 'pg', 'noparse']), default='json', help='json: Store json\nes: Push to ElasticSearch.\npg: Generate flatfiles for Postgres.\nnoparse: Just download the files.')
@click.option('--exclude', '-E', type=click.Choice(['E', 'D', 'H', 'S']), multiple=True, help='Optional list of types of record to exclude.')
def cli(start, end=None, source=None, mode=None, exclude=None):
    """Download and parse the text of the Congressional Record."""
    logging.basicConfig(level=logging.DEBUG)
    api_client = GovInfoClient(api_key=API_KEY)
    #api_client = CongressClient()

    if mode == 'json':
        mgr = LocalJsonCRManager
    else:
        mgr = YieldingCRManager

    if exclude:
        skip_parsing_for = list(exclude) + mgr.DEFAULT_SKIP_PARSING
    else:
        skip_parsing_for = None

    current = start
    if not end:
        end = start
    while current <= end:
        cr_manager = mgr(datetime.strftime(current, DATE_FORMAT), api_client, skip_parsing_for=skip_parsing_for)
        cr_manager()
        current += timedelta(days=1)


if __name__ == '__main__':
    cli()
