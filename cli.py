import logging
from datetime import datetime, timedelta
import click
from congressionalrecord.cr import YieldingCRManager, LocalJsonCRManager

#FIXME should be able to exclude more than one

@click.command()
@click.option('--start', type=click.DateTime(), default=datetime.strftime(datetime.today(), YieldingCRManager.DATE_FORMAT), help='The day or first day of Record text you want to download. (Format: YYYY-MM-DD)')
@click.option('--end', type=click.DateTime(), help='The last day in a contiguous series of days user wants to download. Note the parser skips days with no activity. (Format: YYYY-MM-DD)')
@click.option('--mode', '-M', type=click.Choice(['json', 'es', 'pg', 'noparse']), help='json: Store json\nes: Push to ElasticSearch.\npg: Generate flatfiles for Postgres.\nnoparse: Just download the files.')
@click.option('--exclude', '-E', type=click.Choice(['E', 'D', 'H', 'S']), multiple=True, help='Optional list of types of record to exclude.')
def get_and_parse_cr(start, end=None, mode=None, exclude=None):
    """Download and parse the text of the Congressional Record."""
    logging.basicConfig(level=logging.DEBUG)
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
        cr_manager = mgr(current, skip_parsing_for=skip_parsing_for)
        cr_manager()
        current += timedelta(days=1)


if __name__ == '__main__':
    get_and_parse_cr()
