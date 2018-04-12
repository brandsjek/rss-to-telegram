#!/usr/bin/env python3
import telegram
import feedparser
import argparse
import datetime
import time

parser = argparse.ArgumentParser(description="Sends RSS messages to a Telegram chat/channel.")
parser.add_argument('address', help='The address of the RSS feed.')
parser.add_argument('destination_id', help='The ID (or username, dependent on the type of conversation) to be used as a destination')
parser.add_argument('token', help='The Telegram bot API token to be used.')
parser.add_argument('-t', dest='time', help='The amount of seconds between each request to the RSS feed', default=60)
parser.add_argument('-p', dest='preload', help='The amount of seconds in the past that posts must be in order to be sent in the first iteration.', default = 0)
parser.add_argument('-z', dest='sourcetz', help='The timezone used in the RSS feed.', default="Etc/UTC")
parser.add_argument('-l', dest='localtz', help='The timezone to be used for the time in the message.', default='Europe/Amsterdam')
parser.add_argument('-v', dest='verbose', help='Enable verbosity', action='store_true')
parser.add_argument('--message-format', dest='msgformat', help='The final message. Will be passed on to format(). Read telegram.py for more info.', default="*{}*\n_Published at {}_\n[Go to the full article]({})")
parser.add_argument('--parse-mode', dest='parsemode', help='The parse mode to be used by Telegram.', default='markdown')
parser.add_argument('--time-format', dest='timefmt', help='The formatting for the time in the message. Uses strftime(), so https://docs.python.org/2/library/time.html#time.strftime contains more info.', default='%H:%M:%S')

args = parser.parse_args()

iteration_count = 0

seen_posts = [] # This will store a unique identifier for every post. The post will be ignored if it is already in this list.

def v(text, args):
  if args.verbose:
    print(text)

while True:
  v("Starting iteration " + str(iteration_count), args)
  feed = feedparser.parse(args.address) # Obtain the feed
  if iteration_count is 0: # Iteration 0, send posts sent after a certain time in the past or just place all posts that are currently in the feed into seen_posts
    if args.preload is not 0: # Preload is on.
      for post in feed['items']:
        # struct_time doesnt support subtraction, so we convert it to datetime with a bit of a hack
        post_time_delta = datetime.datetime.fromtimestamp(time.mktime(time.gmtime()))-datetime.datetime.fromtimestamp(time.mktime(post['published_parsed']))
        if post_time_delta < datetime.timedelta(seconds=int(args.preload)):
          # We don't really need to check if the post is in seen_posts as this is the first iteration, but we might dump seen_posts to a file in the future.
          if post.id not in seen_posts:
            v('Publishing message with title "' + post.title + '" as part of preload', args)
            telegram.send_message(args.token, args.destination_id, post, args.localtz, args.sourcetz, args.msgformat, args.parsemode, args.timefmt)
            seen_posts.append(post.id)
        else:
          if post.id not in seen_posts: # Prevent duplicates.
            seen_posts.append(post.id) # We still need to append the post so it won't be sent during the next iteration.
    else: # Preload is off, just append all current posts to seen_posts
      for post in feed['items']:
        seen_posts.append(post.id)
  else: # Iteration is not 0, just iterate over all posts, check if they are in seen_posts, and post them
    for post in feed['items']:
      if post.id not in seen_posts:
        v('Publishing post with title ' + post.title, args)
        telegram.send_message(args.token, args.destination_id, post, args.localtz, args.sourcetz, args.msgformat, args.parsemode, args.timefmt)
        seen_posts.append(post.id)
  iteration_count = iteration_count + 1
  v("Sleeping for " + str(args.time) + " seconds", args)
  time.sleep(int(args.time))
