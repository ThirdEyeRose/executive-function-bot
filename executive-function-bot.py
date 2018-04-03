import time
import json
import requests
import urllib

from CREDENTIALS import *
from dbhelper import DBHelper
import todo_list as todo

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

# Break this up and Abstract pieces of it to To Do class
def handle_updates(updates):
  for update in updates["result"]:
    text = update["message"]["text"]
    chat = update["message"]["chat"]["id"]
    items = db.get_items(chat)
    if text == "/start":
      start_message = """Welcome to the Executive Function Bot. I'm here to
      help you get things done. For now, I operate as a traditional To Do list.
      Tell me things that you want to do and use /done to mark them complete.
      """
      send_message(start_message, chat)
    elif text == "/done":
      keyboard = todo.build_keyboard(items)
      send_message("Select an item to mark complete", chat, keyboard)
    elif text.startswith("/"):
      continue
    elif text in items:
      db.delete_item(text, chat)
      items = db.get_items(chat)
      message = "\n".join(items)
      send_message(message, chat)
    else:
      db.add_item(text, chat)
      items = db.get_items(chat)
      message = "\n".join(items)
      send_message(message, chat)

def main():
  db.setup()
  last_update_id = None
  while True:
    updates = get_updates(last_update_id)
    if len(updates["result"]) > 0:
      last_update_id = get_last_update_id(updates) + 1
      handle_updates(updates)
    time.sleep(0.5)

if __name__ == '__main__':
  main()
send_message(text, chat)
