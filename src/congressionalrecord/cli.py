import os
import json
import logging
from datetime import datetime, timedelta
import click
from congressionalrecord.govinfo.client import GovInfoClient
from congressionalrecord.congress.client import CongressClient
from congressionalrecord.govinfo.cr import CRManager, LocalJsonCRManager
from congressionalrecord.congress.parsers.docs.chambers import SenateRecordParser
from congressionalrecord.utils import DATE_FORMAT

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

    if source == "govinfo":
        client = GovInfoClient(api_key=os.environ.get("GOVINFO_API_KEY"))
        if mode == "json":
            mgr = LocalJsonCRManager
        else:
            mgr = CRManager

        if exclude:
            skip_parsing_for = list(exclude) + mgr.DEFAULT_SKIP_PARSING
        else:
            skip_parsing_for = None

        current = start
        if not end:
            end = start
        while current <= end:
            cr_manager = mgr(datetime.strftime(current, DATE_FORMAT), client, skip_parsing_for=skip_parsing_for)
            cr_manager()
            current += timedelta(days=1)
    elif source == "congress":
        client = CongressClient()
        senate_html = client.get_cr_senate_section(start)
        print(json.dumps(SenateRecordParser().generate_ans(senate_html, start_tag="tbody"), indent=2))


if __name__ == '__main__':
    cli()
