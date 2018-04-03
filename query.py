import os
import sys
import argparse
import tdclient
import pandas as pd
from tabulate import tabulate

def on_waiting(cursor):
    print(cursor.job_status())

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Description: Query data from a table in a database on Treasure Data')

    parser.add_argument('db_name', help='Name of the database')
    parser.add_argument('table_name', help='Name of the table')

    parser.add_argument('-f', '--format', choices=["tabular", "csv"] , default='tabular',
                        help='Output format: "tabular" or "csv" (default: tabular)')
    parser.add_argument('-e', '--engine', choices=["presto", "hive"] , default='presto',
                        help='Query engine: "presto" or "hive" (default: presto)')

    parser.add_argument('-c', '--col_list', type=str, default='*',
                        help='Comma separated list of columns; no space in between (default: all columns)')
    parser.add_argument('-m', '--min_time', type=int,
                        help='Minimum UNIX timestamp in seconds (default: NULL)')
    parser.add_argument('-M', '--max_time', type=int,
                        help='Maximum UNIX timestamp in seconds (default: NULL)')
    parser.add_argument('-l', '--limit', type=int,
                        help='Limit of records returned (default: all records)')

    # API key
    if 'TD_API_KEY' in os.environ:
        apikey = os.getenv("TD_API_KEY")
    else:
        raise ValueError('Please set the environment variable TD_API_KEY for API key')

    args = parser.parse_args()

    q_db = args.db_name
    q_table = args.table_name

    q_format = args.format
    q_engine = args.engine

    # Selected columns
    q_col = args.col_list.replace('"','').replace("'","") if args.col_list else '*'

    # WHERE-clause for time range
    if args.min_time and args.max_time:
        if args.min_time > args.max_time:
            raise ValueError('MAX_TIME must be greater than MIN_TIME')
        q_where = ' WHERE TD_TIME_RANGE(time, ' + str(args.min_time) + ', ' + str(args.max_time) + ')'
    elif args.min_time:
        q_where = ' WHERE time > ' + str(args.min_time)
    elif args.max_time:
        q_where = ' WHERE time < ' + str(args.max_time)
    else:
        q_where = ''

    # LIMIT for number of records
    if args.limit is None:
        q_limit = ''
    else:
        if args.limit > 0:
            q_limit = ' LIMIT ' + str(args.limit)
        else:
            raise ValueError('LIMIT must be greater than 0')

    q_query = 'SELECT ' + q_col + ' FROM ' + q_table + q_where + q_limit + ';'

    # Display gathered arguments
    print('-'*28)
    print('{0:>14s} {1}'.format('DB Name:', q_db))
    print('{0:>14s} {1}'.format('Table Name:', q_table))
    print('{0:>14s} {1}'.format('Output Format:', q_format))
    print('{0:>14s} {1}'.format('Query Engine:', q_engine))
    print('{0:>14s} {1}'.format('Running Query:', q_query))
    print('-'*28)

    try:
        with tdclient.connect(db=q_db, type=q_engine, wait_callback=on_waiting) as td:

            print('Getting table columns.  Please wait ...')
            col_data = pd.read_sql('DESCRIBE ' + q_table, td)
            if q_engine == 'hive':
                col_name = [i.strip() for i in col_data['col_name'].values]
            else: 
                # Un-tested: Presto query engine not available in test account
                col_name = [i.strip() for i in col_data['Column'].values]

            # Check column names
            if q_col != '*':
                invalid_col = []
                for i in q_col.split(','):
                    if i not in col_name:
                        invalid_col.append(i)
                if len(invalid_col) > 0:
                    raise ValueError('Column not found: ' + ','.join(invalid_col))
            print('All columns are valid.  Continue ...')

            # Check 'time' column
            if args.min_time or args.max_time:
                if 'time' not in col_name:
                    raise ValueError('Column not found: time')

            data = pd.read_sql(q_query, td)
            data = data.loc[:, data.columns != 'v']

            if q_format == 'tabular':
                print(tabulate([list(row) for row in data.values], \
                      headers=list(data.columns), tablefmt='grid'))
            elif q_format == 'csv':
                print(data.to_csv(sep=',',index=False))
            else:
                print(repr(data))
    except pd.io.sql.DatabaseError as err:
        #print('SQL DatabaseError: ', err)
        if 'Failed to Login' in err.args[0]:
            print('Failed to log in database: ' + q_db + '\nVerify whether API key is valid')
        elif 'Resource not found' in err.args[0]:
            print('Database not found: ' + q_db)
        elif 'job error' in err.args[0]:
            print('Job error: Possibly table not found: ' + q_table)
        elif 'Presto queries are not enabled for your account' in err.args[0]:
            print('Presto not enabled: Contact support or use query engine "hive"')
        # Un-tested: The test account has Hive
        elif 'Hive queries are not enabled for your account' in err.args[0]:
            print('Hive not enabled: Contact support or use query engine "presto"')
        else:
            print('Exception: ', err)
        #raise
        sys.exit(1)
    except tdclient.errors.InternalError as err:
        if 'row index out of bound' in err.args[0]:
            print('No returned records. Your query arguments could be too limited.')
        else:
            print('Exception: ', err)
            sys.exit(1)
    except Exception as err:
        print('Exception: ', err)
        sys.exit(1)
