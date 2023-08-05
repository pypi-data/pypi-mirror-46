import sys

from cog_nba.database import create_tables

for arg in sys.argv:
    if arg == 'init':
        create_tables()
