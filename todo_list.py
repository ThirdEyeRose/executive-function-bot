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
    return "addtodo"
  elif text == "/todoremoveitem":
    keyboard = build_keyboard(todoitems)
    chat_helper.send_message("Select an item to mark complete", chat_id, keyboard)
    return "removetodo"

def listener_handler(text, chat_id):
  if listener == "todoremove":
    todo.remove_item_from_list(text, chat_id)
    return todo.get_item_list(chat_id)
  elif listener == "todoadd":
    todo.add_item_to_list(text, chat_id)
    return todo.get_item_list(chat_id)
