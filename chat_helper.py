import json
import requests
import urllib

from CREDENTIALS import *

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
