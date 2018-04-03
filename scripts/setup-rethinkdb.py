import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError

if __name__ == "__main__":
  conn = r.connect('localhost', 28015)
  try:
    print(r.db_create('bcb').run(conn))
    print(r.db('bcb').table_create('records').run(conn))
    print(r.db('bcb').table_create('topics').run(conn))
    print(r.db('bcb').table_create('participants').run(conn))
  except RqlRuntimeError as err:
    print(err.message)
  finally:
    conn.close()
