import time
import json
import requests
import urllib

from CREDENTIALS import *
from dbhelper import DBHelper

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

def build_keyboard(items):
  keyboard = [[item] for item in items]
  reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
  return json.dumps(reply_markup)

def send_message(text, chat_id, reply_markup=None):
  text = urllib.quote_plus(text)
  url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
  if reply_markup:
    url += "&reply_markup={}".format(reply_markup)
  get_url(url)

def handle_updates(updates):
  for update in updates["result"]:
    text = update["message"]["text"]
    chat = update["message"]["chat"]["id"]
    items = db.get_items()
    if text == "/done":
      keyboard = build_keyboard(items)
      send_message("Select an item to mark complete", chat, keyboard)
    elif text in items:
      db.delete_item(text)
      items = db.get_items()
      keyboard = build_keyboard(items)
      send_message("Select an item to mark complete", chat, keyboard)
    else:
      db.add_item(text)
      items = db.get_items()
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
