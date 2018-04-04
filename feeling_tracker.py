import datetime
import schedule

from dbhelper import DBHelper

db = DBHelper()

def set_frequency(owner, frequency):
  db.set_feelings_config_frequency(owner, frequency)

def set_time_pref(owner, time_pref):
  db.set_feelings_config_time_pref(owner, time_pref)

def debug(owner):
  print db.get_feelings_config(owner)
