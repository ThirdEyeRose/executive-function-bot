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
