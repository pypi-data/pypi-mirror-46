import sqlite3

def max_parameter_substitution():
    conn = sqlite3.connect(':memory:')
    low = 1
    high = 1000  # hard limit for SQLITE_MAX_VARIABLE_NUMBER <http://www.sqlite.org/limits.html>
    conn.execute('CREATE TABLE T1 (id C1)')
    while low < high - 1:
        guess = (low + high) // 2
        try:
            statement = 'select * from T1 where id in (%s)' % ','.join(['?' for _ in range(guess)])
            values = [i for i in range(guess)]
            conn.execute(statement, values)
        except sqlite3.DatabaseError as ex:
            if 'too many SQL variables' in str(ex):
                high = guess
            else:
                raise
        else:
            low = guess
    conn.close()
    return low


# import sqlite3

# def max_columns():
#     conn = sqlite3.connect(':memory:')
#     c = conn.cursor()
#     c.execute('CREATE TABLE T1 (C1)')
#     low = 1
#     high = 1000  # hard limit <http://www.sqlite.org/limits.html>
#     while low < high - 1:
#         guess = (low + high) // 2
#         try:
# gues            db.execute('CREATE TABLE T%d (%s)' % (
#                 guess, ','.join('C%d' % i for i in range(guess))
#             ))
#         except sqlite3.DatabaseError as ex:
#             if 'too many columns' in str(ex):
#                 high = guess
#             else:
#                 raise
#         else:
#             low = guess
#     return low


from django.db import connection
def max_parameter_substitution():
    low = 1
    high = 1001  # hard limit for SQLITE_MAX_VARIABLE_NUMBER <http://www.sqlite.org/limits.html>
    while low < high - 1:
        guess = (low + high) // 2
        statement = "select * from morango_databasemaxcounter where id in (%s)" % ','.join(['%s' for _ in range(guess)])
        values = [i for i in range(guess)]
        try:
            with connection.cursor() as cursor:
                cursor.execute(statement, values)
        except ValueError as ex:
            if 'too many SQL variables' in str(ex):
                high = guess
            else:
                raise
        else:
            low = guess
    return low
