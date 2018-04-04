import sqlite3

class DBHelper:
  def __init__(self, dbname="efb.sqlite"):
    self.dbname = dbname
    self.conn = sqlite3.connect(dbname)

  def setup(self):
    create_item_table = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
    create_item_index = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
    create_owner_index = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
    create_feelings_table = "CREATE TABLE IF NOT EXISTS feelings (created_at datetime, owner text, rating integer, description text)"
    creat_feelings_config = "CREATE TABLE IF NOT EXISTS feelingsConfig (owner text, frequency text, time_pref text)"
    self.conn.execute(create_item_table)
    self.conn.execute(create_item_index)
    self.conn.execute(create_owner_index)
    self.conn.execute(create_feelings_table)
    self.conn.commit()

  def add_item(self, item_text, owner):
    stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
    args = (item_text, owner)
    self.conn.execute(stmt, args)
    self.conn.commit()

  def delete_item(self, item_text, owner):
    stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
    args = (item_text, owner )
    self.conn.execute(stmt, args)
    self.conn.commit()

  def get_items(self, owner):
    stmt = "SELECT description FROM items WHERE owner = (?)"
    args = (owner, )
    return [x[0] for x in self.conn.execute(stmt, args)]

  def add_feeling_report(self, created_at, owner, rating, description=None):
    stmt = "INSERT INTO feelings (created_at, owner, rating, description) VALUES (?, ?, ?, ?)"
    args = (created_at, owner, rating, description)
    self.conn.execute(stmt, args)
    self.conn.commit()

  def get_feeling_report(self, owner):
    stmt = "SELECT rating FROM feelings WHERE owner = (?)"

  def set_feelings_config(self, owner, frequency, time_pref):
    stmt = "INSERT INTO feelingsConfig (owner, frequency, time_pref) VALUES (?, ?)"
    args = (owner, frequency, time_pref)
    self.conn.execute(stmt, args)
    self.conn.commit()
