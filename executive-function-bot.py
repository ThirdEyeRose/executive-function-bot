import time
import json
import schedule

import chat_helper
from dbhelper import DBHelper
import todo_list as todo
import feeling_tracker as ft

db = DBHelper()

def command_handler(text, chat_id):
  if text == "/start":
    start_message = """Welcome to the Executive Function Bot. I'm here to
    help you get things done. For now, I operate as a traditional To Do list.
    Tell me things that you want to do and use /done to mark them complete.
    """
    chat_helper.send_message(start_message, chat_id)
  elif text.startswith("/todo"):
    return todo.command_handler(text, chat_id)
  elif text.startswith("/feelingtracker"):
    return ft.command_handler(text, chat_id)
  elif text == "/debug":
    ft.debug(chat_id)
  else:
    chat_helper.send_message("I'm sorry, I don't know that command. Use /help for a list of commands.", chat_id)

def listener_handler(listener, text, chat_id):
  if listener.startswith("todo"):
    chat_helper.send_message(todo.listener_handler(listener, text, chat_id), chat_id)
  elif listener.startswith("feelingtracker"):
    return ft.listener_handler(listener, text, chat_id)

def handle_updates(updates, listener):
  for update in updates["result"]:
    text = update["message"]["text"]
    chat = update["message"]["chat"]["id"]

    if text.startswith("/"):
      return command_handler(text, chat)
    elif listener is not None:
      return listener_handler(listener, text, chat)
    elif text == "end":
      return None
    else:
      continue

def main():
  db.setup()
  last_update_id = None
  listener = None
  while True:
    updates = chat_helper.get_updates(last_update_id)
    if len(updates["result"]) > 0:
      last_update_id = chat_helper.get_last_update_id(updates) + 1
      listener = handle_updates(updates, listener)
    schedule.run_pending()
    time.sleep(0.5)

if __name__ == '__main__':
  main()
chat_helper.send_message(text, chat)
