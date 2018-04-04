import time
import json
import requests
import schedule
import urllib

from CREDENTIALS import *
from dbhelper import DBHelper
import todo_list as todo
import feeling_tracker as ft

db = DBHelper()
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
  response = requests.get(url)
  content = response.content.decode("utf8")
  return content

def get_json_from_url(url):
  content = get_url(url)
  js = json.loads(content)
  return js

def get_updates(offset=None):
  url = URL + "getUpdates?timeout=100"
  if offset:
    url += "&offset={}".format(offset)
  js = get_json_from_url(url)
  return js

def get_last_update_id(updates):
  update_ids = []
  for update in updates["result"]:
    update_ids.append(int(update["update_id"]))
  return max(update_ids)

def send_message(text, chat_id, reply_markup=None):
  text = urllib.quote_plus(text)
  url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
  if reply_markup:
    url += "&reply_markup={}".format(reply_markup)
  get_url(url)

def build_keyboard(items):
  keyboard = [[item] for item in items]
  reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
  return json.dumps(reply_markup)

def handle_updates(updates, listener):
  for update in updates["result"]:
    text = update["message"]["text"]
    chat = update["message"]["chat"]["id"]
    todoitems = db.get_items(chat)
    if text == "/start":
      start_message = """Welcome to the Executive Function Bot. I'm here to
      help you get things done. For now, I operate as a traditional To Do list.
      Tell me things that you want to do and use /done to mark them complete.
      """
      send_message(start_message, chat)
    elif text == "/addtodo":
      send_message("What do you need to do?", chat)
      return "addtodo"
    elif text == "/finishtodo":
      keyboard = build_keyboard(todoitems)
      send_message("Select an item to mark complete", chat, keyboard)
      return "removetodo"
    elif text in todoitems and listener == "removetodo":
      todo.remove_item_from_list(text, chat)
      send_message(todo.get_item_list(chat), chat)
    elif listener == "addtodo":
      todo.add_item_to_list(text, chat)
      send_message(todo.get_item_list(chat), chat)
    elif text == "/starttrackingfeelings":
      send_message("Feeling Tracking Enabled", chat)
      options = ["Daily", "A few times a day", "Hourly"]
      keyboard = build_keyboard(options)
      send_message("How often would you like to talk about your feelings?", chat, keyboard)
      return "configfeelingtrackingfrequency"
    elif listener == "configfeelingtrackingfrequency":
      # Record frequency response in database
      options = ["Morning", "Afternoon", "Evening", "Throughout the day"]
      keyboard = build_keyboard(options)
      send_message("Do you have a preference of when you want to talk about your feelings?", chat, keyboard)
      return "configfeelingtrackingtime"
    elif listener == "configfeelingtrackingtime":
      # Record time preference in database
      send_message("Thanks for letting me know!", chat)
    elif text == "end":
      return None
    elif text.startswith("/"):
      continue
    else:
      continue

def main():
  db.setup()
  last_update_id = None
  listener = None
  while True:
    updates = get_updates(last_update_id)
    if len(updates["result"]) > 0:
      last_update_id = get_last_update_id(updates) + 1
      listener = handle_updates(updates, listener)
    schedule.run_pending()
    time.sleep(0.5)

if __name__ == '__main__':
  main()
send_message(text, chat)
