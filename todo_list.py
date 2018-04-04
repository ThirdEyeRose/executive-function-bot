import chat_helper

from dbhelper import DBHelper

db = DBHelper()

def get_item_list(owner):
  items = db.get_items(owner)
  return "\n".join(items)

def add_item_to_list(item, owner):
  db.add_item(item, owner)

def remove_item_from_list(item, owner):
  db.delete_item(item, owner)

def command_handler(text, chat_id):
  todoitems = db.get_items(chat_id)
  if text == "/todoadditem":
    chat_helper.send_message("What do you need to do?", chat_id)
    return "todoadd"
  elif text == "/todoremoveitem":
    keyboard = chat_helper.build_keyboard(todoitems)
    chat_helper.send_message("Select an item to mark complete", chat_id, keyboard)
    return "todoremove"

def listener_handler(listener, text, chat_id):
  if listener == "todoremove":
    remove_item_from_list(text, chat_id)
    return get_item_list(chat_id)
  elif listener == "todoadd":
    add_item_to_list(text, chat_id)
    return get_item_list(chat_id)
