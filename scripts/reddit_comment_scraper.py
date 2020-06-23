#!/home/pi/script-server/env/bin/python3

from igramscraper.instagram import Instagram
import csv, time, os, sys, argparse, praw
import pandas as pd
from time import sleep
from os.path import isfile
reddit = praw.Reddit()

parser = argparse.ArgumentParser()
parser.add_argument("--postid", required=True, type=str, help="The ID of the post to scrape")
args = parser.parse_args()

postid = args.postid

with open('outputs/%s_comments.csv' % postid, 'a', encoding='utf-8') as f:
	writer = csv.writer(f, lineterminator = '\n')
	writer.writerow(['parent_id', 'comment', 'score', 'author', 'created_utc', 'permalink'])
	submission = reddit.submission(id=postid)
	submission.comments.replace_more(limit=0)
	for comment in submission.comments.list():
		writer.writerow([comment.parent_id, comment.body, comment.score, comment.author, comment.created_utc, comment.permalink])
	time.sleep(0.5)

f.close()

print ('\nDone! Successfully scraped %s comments.' % len(submission.comments.list()))
print ('A link to download the CSV data file should be below.\n')
print ('**FYI**')
print ('The dates will be in Unix timestamps...')
print ('Use the formula below to convert to regular date format.\n')
print ('    =(B2/86400)+DATE(1970,1,1)')
