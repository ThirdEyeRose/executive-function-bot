import datetime
import schedule

import chat_helper
from dbhelper import DBHelper

db = DBHelper()

def set_frequency(owner, frequency):
  db.set_feelings_config_frequency(owner, frequency)

def set_time_pref(owner, time_pref):
  db.set_feelings_config_time_pref(owner, time_pref)

def debug(owner):
  config = db.get_feelings_config(owner)
  for setting in config[0]:
    print setting

def command_handler(text, chat_id):
  if text == "/feelingtrackerstart":
    chat_helper.send_message("Feeling Tracking Enabled", chat_id)
    options = ["Daily", "A few times a day", "Hourly"]
    keyboard = chat_helper.build_keyboard(options)
    chat_helper.send_message("How often would you like to talk about your feelings?", chat_id, keyboard)
    return "configfeelingtrackingfrequency"
