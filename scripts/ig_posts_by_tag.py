#!/home/pi/script-server/env/bin/python3

from context import Instagram # pylint: disable=no-name-in-module
import csv, time, os, sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--hashtag", required=True, type=str, help="Instagram hashtag without '#' symbol")
parser.add_argument("--max", required=True, type=int, default=10000, help="Maximum number of posts to scrape")

args = parser.parse_args()
hashtag = args.hashtag
maxPosts = args.max

csvPath = os.path.join('outputs/', '%s-posts.csv' % hashtag)

proxies = {
	"http": "socks5h://x2923101:g2XbTQ6tHk@proxy-nl.privateinternetaccess.com:1080",
 	"https": "socks5h://x2923101:g2XbTQ6tHk@proxy-nl.privateinternetaccess.com:1080",
}

instagram = Instagram()
instagram.set_proxies(proxies)

print ("\n Scraping in progress... please wait.\n")

medias = instagram.get_medias_by_tag(hashtag, count=maxPosts)

with open(csvPath, 'a', encoding='utf-8') as f:
	writer = csv.writer(f, lineterminator = '\n')
	writer.writerow(['post id', 'post date', 'post link', 'caption', 'likes', 'comments'])

for media in medias:
	with open(csvPath, 'a', encoding='utf-8') as f:
		writer = csv.writer(f, lineterminator = '\n')
		writer.writerow([media.identifier, media.created_time, media.link, media.caption, media.likes_count, media.comments_count])

f.close()

print ('\nDone! Successfully scraped %s posts.' % len(medias))
print ('A link to download the CSV data file should be below.\n')
print ('**FYI**')
print ('The post dates will be in Unix timestamps...')
print ('Use the formula below to convert to regular date format.\n')
print ('    =(B2/86400)+DATE(1970,1,1)')
