import datetime
import schedule

import chat_helper
from dbhelper import DBHelper

db = DBHelper()

def set_frequency(owner, frequency):
  db.set_feelings_config_frequency(owner, frequency)

def set_time_pref(owner, time_pref):
  db.set_feelings_config_time_pref(owner, time_pref)

def prompt_user(owner):
  options = [["1", "2", "3", "4","5"]]
  keyboard = chat_helper.build_keyboard(options)
  chat_helper.send_message("How are you feeling?", owner)

def initialize_schedule(owner):
  config = db.get_feelings_config(owner)
  frequency = {"Daily" : 24, "A few times a day" : 4, "Hourly" : 1 }
  # config[0][0] is frequency
  # config[0][1] is time pref
  schedule.every(frequency[config[0][0]]).hours.do(prompt_user, owner)

def debug(owner):
  initialize_schedule(owner)
  print schedule.jobs

def command_handler(text, chat_id):
  if text == "/feelingtrackerstart":
    chat_helper.send_message("Feeling Tracking Enabled", chat_id)
    options = ["Daily", "A few times a day", "Hourly"]
    keyboard = chat_helper.build_keyboard(options)
    chat_helper.send_message("How often would you like to talk about your feelings?", chat_id, keyboard)
    return "feelingtrackerconfigfrequency"

def listener_handler(listener, text, chat_id):
  if listener == "feelingtrackerconfigfrequency":
    set_frequency(chat_id, text)
    options = ["Morning", "Afternoon", "Evening", "Throughout the day"]
    keyboard = chat_helper.build_keyboard(options)
    chat_helper.send_message("Do you have a preference of when you want to talk about your feelings?", chat_id, keyboard)
    return "feelingtrackerconfigtime"
  elif listener == "feelingtrackerconfigtime":
    set_time_pref(chat_id, text)
    chat_helper.send_message("Thanks for letting me know!", chat_id)
