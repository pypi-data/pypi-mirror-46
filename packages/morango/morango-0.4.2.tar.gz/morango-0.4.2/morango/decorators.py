import time
import functools

from django.db import connection, reset_queries


def debugger_queries(func):
    """Basic function to debug queries."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("func: ", func.__name__)
        reset_queries()

        start = time.time()
        start_queries = len(connection.queries)

        result = func(*args, **kwargs)

        end = time.time()
        end_queries = len(connection.queries)

        rc = 0
        wc = 0
        for query in connection.queries:
            if 'SELECT' in query['sql']:
                rc += 1
            elif 'UPDATE' in query['sql']:
                wc += 1
            elif 'DELETE' in query['sql']:
                wc += 1
            elif 'INSERT' in query['sql']:
                wc += 1

        print("queries:", end_queries - start_queries)
        print("READS: ", rc)
        print("WRITES: ", wc)
        print("took: %.2fs" % (end - start))
        # for c in connection.queries:
        #     print(c['sql'])
        #     print('BREAKKKK')

        with open('queries.txt', 'w') as f:
            for c in connection.queries:
                f.write(str(c['sql']) + '\n')
        return result

    return wrapper
