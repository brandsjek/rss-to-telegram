import requests
import json
import pytz
from time import mktime
import datetime

def send_message(token, chat_id, post, timezone_dest, timezone_orig, message_fmt, parse_mode, time_fmt):
  url = "https://api.telegram.org/bot" + token + "/sendMessage"

  dtz = pytz.timezone(timezone_dest)
  otz = pytz.timezone(timezone_orig) # Create timezone objects for the original and destination timezone

  dt = datetime.datetime(*post.published_parsed[:6]) # Convert time_struct to datetime.

  orig_dt = otz.localize(dt)
  dest_dt = orig_dt.astimezone(dtz) # Convert from source to local TZ.

  time = dest_dt.strftime('%H:%M:%S')

  #text = "*{}*\n_Gepubliceerd om {}_\n[Ga naar het volledige artikel]({})"
  text = message_fmt.format(post.title, str(time), post.link)
  data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}

  response = requests.post(url, json=data)
  return response.text
