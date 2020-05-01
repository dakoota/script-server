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

csvPath = os.path.join('outputs/', '%s-FollowerData.csv' % acct)
user = api.get_user(screen_name = acct)

print ('\n' + user.screen_name + ' currently has ' + str(user.followers_count) + ' followers.')
if round(user.followers_count / 3000) == 0:
  print ('It will take less than a minute to pull all follower details...')
else:
  print ('It will take about ' + str(round(user.followers_count / 3000)) + ' minutes to pull all follower details...')

keepGoing = input('\nDo you want to continue? (y/n) \n')

if keepGoing == "n":
  print ('\nK thanks bye!')
  time.sleep(5)
elif keepGoing == "y":
    pg_count = 0
    ids = []
    print ('\nGetting follower IDs...')
    for page in tweepy.Cursor(api.followers_ids, screen_name=acct).pages():
        ids.extend(page)
        pg_count += 1
        if len(page) == 5000:
          time.sleep(11)

    def gen_chunks(ids, chunksize=100):
        chunk = []
        for i, id in enumerate(ids):
            if (i % chunksize == 0 and i > 0):
                yield chunk
                del chunk[:]
            chunk.append(id)
        yield chunk

    chunkCount = 1
    print ('IDs collected. Time for the good stuff!')
    with open(csvPath, 'a', encoding='utf-8') as f:
      writer = csv.writer(f, lineterminator = '\n')
      writer.writerow(["id","screen_name","name","verified","protected","location","followers","following","tweets","created_at","bio","url"])
    for chunk in gen_chunks(ids):
        users = api.lookup_users(user_ids=chunk)
        cleanData = [[u.id, u.screen_name, u.name, u.verified, u.protected, u.location, u.followers_count, u.friends_count, u.statuses_count, u.created_at.strftime("%B %d, %Y"), u.description, u.url] for u in users]
        with open(csvPath, 'a', encoding='utf-8') as f:
          writer = csv.writer(f, lineterminator = '\n')
          writer.writerows(cleanData)
        followersDown = chunkCount * 100
        if (100 * (followersDown/user.followers_count)) >= 100:
          sys.stdout.write('\rData downloaded for ' + str(user.followers_count) + ' followers\n')
        else:
          sys.stdout.write('\rDownloading follower data....' + "{0:.0f}".format(100 * float(followersDown)/float(user.followers_count)) + '%')
        sys.stdout.flush()
        chunkCount += 1
    f.close()
    print ('\nAll done!')
    print ('A link to download the CSV data file should be below.')
else:
  print ('\nPlease enter Y for yes or N for no..')
