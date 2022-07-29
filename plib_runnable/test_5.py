"""
Extensions for Pandas
---------------------

This module extends ``pandas.DataFrame`` with methods ``pg_copy_to`` and
``pg_copy_from``.

To enable, simply import this module anywhere in your project,
(most likely -- just once, in its root module)::

    >>> import ohio.ext.pandas

For example, if you have just one module -- in there -- or, in a Python
package::

    ohio/
        __init__.py
        baseio.py
        ...

then in its ``__init__.py``, to ensure that extensions are loaded before
your code, which uses them, is run.

**Note**: These extensions are intended for Pandas, and attempt to
``import pandas``. Pandas must be available (installed) in your
environment.

"""
import functools

import ohio
import pandas



def to_sql_method_pg_copy_to(table, engine, keys, data_iter):
    """Write pandas data to table via stream through PostgreSQL
    ``COPY``.

    This implements a pandas ``to_sql`` "method", utilizing
    ``ohio.CsvTextIO`` for performance stability.

    """
    columns = ', '.join('"{}"'.format(key) for key in keys)
    if table.schema:
        table_name = '{}.{}'.format(table.schema, table.name)
    else:
        table_name = table.name

    sql = 'COPY {table_name} ({columns}) FROM STDIN WITH CSV'.format(
        table_name=table_name,
        columns=columns,
    )

    with ohio.CsvTextIO(data_iter) as csv_buffer:
        with engine.connect() as conn:
            with conn.connection.cursor() as cursor:
                cursor.copy_expert(sql, csv_buffer)


def test_to_sql_method_pg_copy_to():
    """Check the correctness of to_sql_method_pg_copy_to
    """
    assert to_sql_method_pg_copy_to(None, None, [], None) is None