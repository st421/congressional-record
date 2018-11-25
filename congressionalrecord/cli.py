import logging
from datetime import datetime, timedelta
import click
from congressionalrecord.cr import LocalCRManager, LocalJsonCRManager

#FIXME should be able to exclude more than one

@click.command()
@click.option('--start', type=click.DateTime(), default=datetime.strftime(datetime.today(), LocalCRManager.DATE_FORMAT), help='The day or first day of Record text you want to download. (Format: YYYY-MM-DD)')
@click.option('--end', type=click.DateTime(), default=None, help='The last day in a contiguous series of days user wants to download. Note the parser skips days with no activity. (Format: YYYY-MM-DD)')
@click.option('--mode', type=click.Choice(['json', 'es', 'pg', 'noparse']), default=None, help='json: Store json\nes: Push to ElasticSearch.\npg: Generate flatfiles for Postgres.\nnoparse: Just download the files.')
@click.option('--exclude', type=click.Choice(['E', 'D', 'H', 'S']), default=None, help='Optional list of types of record to exclude.')
def get_and_parse_cr(start, end=None, mode=None, exclude=None):
    """Download and parse the text of the Congressional Record."""
    logging.basicConfig(level=logging.DEBUG)
    if mode == 'json':
        mgr = LocalJsonCRManager
    else:
        mgr = LocalCRManager

    current = start
    if not end:
        end = start
    while current <= end:
        cr_manager = mgr(current, skip_parsing_for=[exclude] + mgr.DEFAULT_SKIP_PARSING)
        cr_manager()
        current += timedelta(days=1)


if __name__ == '__main__':
    get_and_parse_cr()
