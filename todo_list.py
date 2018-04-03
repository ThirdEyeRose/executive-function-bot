import json

def build_keyboard(items):
  keyboard = [[item] for item in items]
  reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
  return json.dumps(reply_markup)
