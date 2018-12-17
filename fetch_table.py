#!/usr/bin/env python3

import gzip
import hashlib
import os
import pickle
import sys
import time
from datetime import datetime

import django
from django.core.cache import caches

from main.utils import _execute_query


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()

cache = caches['dump']


def hashit(data):

    if type(data) == str:
        data = data.encode()

    if type(data) != bytes:
        raise Exception("Cannot hash %r" % data)

    return hashlib.md5(data).hexdigest()


def execute_query(query, cache_query=True, **kwargs):
    if cache_query:
        key = hashit('%s\n%r' % (query, kwargs))
        values = cache.get(key)
        if not values:
            print('\n\nExecuting: %s\nkwargs:\n%r\n' % (query, kwargs))
            values = _execute_query(query, **kwargs)
            cache.set(key, values)
    else:
        print('\n\nExecuting: %s\nkwargs:\n%r\n' % (query, kwargs))
        values = _execute_query(query, **kwargs)
    columns, rows = values
    return columns, rows


def get_pk_for_table(table):

    query = """
            SELECT
                b.COLUMN_NAME

            FROM
                ALL_CONSTRAINTS a

                JOIN ALL_CONS_COLUMNS b
                    ON
                        a.owner = b.owner AND
                        a.table_name = b.table_name AND
                        a.constraint_name = b.constraint_name

            WHERE
                a.constraint_type = 'P' AND
                a.table_name = :ptable

        """

    cols, rows = execute_query(query, ptable=table)

    return [row[0] for row in rows]


def get_columns_for_table(table):

    query = """
            SELECT
                OWNER,
                TABLE_NAME,
                COLUMN_NAME,
                DATA_TYPE,
                DATA_TYPE_MOD,
                DATA_TYPE_OWNER,
                DATA_LENGTH,
                DATA_PRECISION,
                DATA_SCALE,
                NULLABLE,
                COLUMN_ID,
                DEFAULT_LENGTH,
                DATA_DEFAULT,
                NUM_DISTINCT,
                LOW_VALUE,
                HIGH_VALUE,
                DENSITY,
                NUM_NULLS,
                NUM_BUCKETS,
                LAST_ANALYZED,
                SAMPLE_SIZE,
                CHARACTER_SET_NAME,
                CHAR_COL_DECL_LENGTH,
                GLOBAL_STATS,
                USER_STATS,
                AVG_COL_LEN,
                CHAR_LENGTH,
                CHAR_USED,
                V80_FMT_IMAGE,
                DATA_UPGRADED,
                HISTOGRAM
            FROM
                ALL_TAB_COLUMNS
            WHERE
                TABLE_NAME = :ptable
            ORDER BY COLUMN_ID ASC
        """

    cols, rows = execute_query(query, ptable=table)

    columns = []

    for row in rows:

        (
            field_owner,
            field_table_name,
            field_column_name,
            field_data_type,
            field_data_type_mod,
            field_data_type_owner,
            field_data_length,
            field_data_precision,
            field_data_scale,
            field_nullable,
            field_column_id,
            field_default_length,
            field_data_default,
            field_num_distinct,
            field_low_value,
            field_high_value,
            field_density,
            field_num_nulls,
            field_num_buckets,
            field_last_analyzed,
            field_sample_size,
            field_character_set_name,
            field_char_col_decl_length,
            field_global_stats,
            field_user_stats,
            field_avg_col_len,
            field_char_length,
            field_char_used,
            field_v80_fmt_image,
            field_data_upgraded,
            field_histogram
        ) = row

        columns.append({
                'owner': field_owner,
                'table_name': field_table_name,
                'column_name': field_column_name,
                'data_type': field_data_type,
                'data_type_mod': field_data_type_mod,
                'data_type_owner': field_data_type_owner,
                'data_length': field_data_length,
                'data_precision': field_data_precision,
                'data_scale': field_data_scale,
                'nullable': field_nullable,
                'column_id': field_column_id,
                'default_length': field_default_length,
                'data_default': field_data_default,
                'num_distinct': field_num_distinct,
                'low_value': field_low_value,
                'high_value': field_high_value,
                'density': field_density,
                'num_nulls': field_num_nulls,
                'num_buckets': field_num_buckets,
                'last_analyzed': field_last_analyzed,
                'sample_size': field_sample_size,
                'character_set_name': field_character_set_name,
                'char_col_decl_length': field_char_col_decl_length,
                'global_stats': field_global_stats,
                'user_stats': field_user_stats,
                'avg_col_len': field_avg_col_len,
                'char_length': field_char_length,
                'char_used': field_char_used,
                'v80_fmt_image': field_v80_fmt_image,
                'data_upgraded': field_data_upgraded,
                'histogram': field_histogram,
            })

    return columns


def save(prefix, table_name, data):


    datestr = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    filename = 'dump/%s___%s___%s.pickle.gz' % (prefix, table_name, datestr)

    fp = gzip.open(filename, 'wb')
    pickle.dump(data, fp)
    fp.close()


def fetch_rows(table, columns, next_rowid, num_rows):


    query = """
            SELECT
                {fields}
            FROM (
                    SELECT
                        {fields}
                    FROM
                        {table}
                    {filter_condition}
                    ORDER BY
                        ROWID ASC
                )
            WHERE
                ROWNUM <= :prownummax
        """
    query = query.format(
            fields=', '.join(['ROWID', 'ORA_ROWSCN'] + columns),
            table=table,
            filter_condition="WHERE ROWID > :prowid" if next_rowid else "",
        )
    params = {'prownummax': num_rows}
    if next_rowid:
        params.update({'prowid': next_rowid})

    cols, rows = execute_query(query, cache_query=False, **params)

    next_rowid = rows[-1][0] if rows else None

    return rows, next_rowid


def fetch_table(table, fetch_count=250, delay_seconds_between_rows=0):

    fetched_tables = cache.get('fetched_tables', {})
    fetch_details = fetched_tables.get(table, {})
    if fetch_details.get('finished_at'):
        print('=' * 79)
        print('Table %s has already been fetched' % table)
        print('=' * 79)
        print('Finished fetching at %s with %s rows. Took %3.3f seconds.' % (
                fetch_details['finished_at'].strftime('%Y-%m-%d %H:%M:%S'),
                fetch_details['num_rows_fetched'],
                fetch_details['duration'],
            ))
        return


    ts_start_overall = time.time()

    print('=' * 79)
    print('Fetching: %s' % table)
    print('=' * 79)

    column_infos = get_columns_for_table(table)
    save('columns', table, column_infos)

    columns = [v['column_name'] for v in column_infos]
    if 'PSP_NUM' in columns:
        columns[columns.index('PSP_NUM')] = 'ISM.Crypt.decrypt(PSP_NUM) as PSP_NUM'

    table_name_in_query = column_infos[0]['owner'] + '.' + column_infos[0]['table_name']

    print('Columns %s: %s' % (len(columns), ', '.join(columns)))
    print('=' * 79)

    next_rowid = cache.get('last_rowid___' + table)
    if next_rowid:
        print(">>> CONTINUE rowid at '%s'" % next_rowid)

    while True:

        ts_start = time.time()
        rows, next_rowid = fetch_rows(table_name_in_query, columns, next_rowid, fetch_count)
        print("fetch duration: %3.3fs '%s'" % (time.time() - ts_start, next_rowid))

        # increment num rows
        cache.set('num_rows___' + table, cache.get('num_rows___' + table, 0) + len(rows))

        for row in rows:
            print('Value: %r' % (row[:4],))

        save('chunk', table, rows)

        cache.set('last_rowid___' + table, next_rowid)

        if len(rows) < fetch_count:
            break
        else:
            if delay_seconds_between_rows:
                time.sleep(delay_seconds_between_rows)

    print('=' * 79)

    details = {
        'finished_at': datetime.now(),
        'num_rows_fetched': cache.get('num_rows___' + table),
        'duration': time.time() - ts_start_overall,
    }
    cache.set('fetched_tables', {**cache.get('fetched_tables', {}), **{table: details}})

    print('Finished fetching %s at %s with %s rows. Took %3.3f seconds' % (
            table,
            details['finished_at'].strftime('%Y-%m-%d %H:%M:%S'),
            details['num_rows_fetched'],
            details['duration'],
        ))

    # cleanup
    cache.delete('last_rowid___' + table)
    cache.delete('num_rows___' + table)


if __name__ == "__main__":

    if len(sys.argv) < 4:
        print('\n    Usage:')
        print('        fetch_table.py <table> <fetch_count> <delay_seconds_between_rows>\n')
        sys.exit()

    table = sys.argv[1]
    fetch_count = int(sys.argv[2])
    assert fetch_count > 0, "Fetch count must be greater than 0"
    delay_seconds_between_rows = int(sys.argv[3])

    ts_start = time.time()
    fetch_table(table, fetch_count, delay_seconds_between_rows)

    print('=' * 79)
    print('Overall duration: % 6.3fs' % (time.time() - ts_start))
