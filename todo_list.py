import json

from dbhelper import DBHelper

db = DBHelper()

def build_keyboard(items):
  keyboard = [[item] for item in items]
  reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
  return json.dumps(reply_markup)

def get_item_list(owner):
  items = db.get_items(owner)
  return "\n".join(items)

def add_item_to_list(item, owner):
  db.add_item(item, owner)

def remove_item_from_list(item, owner):
  db.delete_item(item, owner)
