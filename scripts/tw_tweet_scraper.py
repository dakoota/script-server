import tweepy, time, datetime, csv, sys, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--uname", required=True, type=str, help="Twitter username to scrape")

args = parser.parse_args()
acct = args.uname
acct = acct.replace('@','')

auth = tweepy.OAuthHandler('svwoALxCmje0MXh3hx5UnUiaf', 'yTRtMZMvkQzyHfcWJZz1Y7YYFUGzTiX1ZlmVRFCDDhelOX5apE')
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=set([503]))

if (not api):
  print ('Can\'t Authenticate')
  sys.exit(-1)

csvPath = os.path.join('outputs/', '%s-tweets.csv' % acct)

#initialize a list to hold all the tweepy Tweets
alltweets = []

#make initial request for most recent tweets (200 is the maximum allowed count)
new_tweets = api.user_timeline(screen_name=acct,count=200)

#save most recent tweets
alltweets.extend(new_tweets)

#save the id of the oldest tweet less one
oldest = alltweets[-1].id - 1

#keep grabbing tweets until there are no tweets left to grab
while len(new_tweets) > 0:
	#all subsiquent requests use the max_id param to prevent duplicates
	new_tweets = api.user_timeline(screen_name=acct,count=200,max_id=oldest)

	#save most recent tweets
	alltweets.extend(new_tweets)

	#update the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	print ("...%s tweets downloaded so far" % (len(alltweets)))

outtweets = [[tweet.id_str, tweet.created_at, tweet.text, tweet.favorite_count, tweet.retweet_count] for tweet in alltweets]

with open(csvPath, 'a', encoding='utf-8') as f:
	writer = csv.writer(f, lineterminator = '\n')
	writer.writerow(["tweet_id","created_at","text","favorties","retweets"])
	writer.writerows(outtweets)
f.close()

print ('\nAll done!')
print ('A link to download the CSV data file should be below.')
