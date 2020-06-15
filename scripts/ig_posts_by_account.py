#!env/bin/python3

from context import Instagram
import argparse, csv, time, os, sys

parser = argparse.ArgumentParser()
parser.add_argument("--uname", required=True, type=str, help="Instagram username to scrape")
parser.add_argument("--max", required=True, type=int, default=10000, help="Maximum number of posts to scrape")

args = parser.parse_args()
account = args.uname
maxPosts = args.max

csvPath = os.path.join('outputs/%s-posts.csv' % account)

#proxies = {
#	"http": "socks5h://x2923101:g2XbTQ6tHk@proxy-nl.privateinternetaccess.com:1080",
#	"https": "socks5h://x2923101:g2XbTQ6tHk@proxy-nl.privateinternetaccess.com:1080",
#}

instagram = Instagram()
#instagram.set_proxies(proxies)

print("\nScraping in progress... please wait...")

medias = instagram.get_medias(account, maxPosts)

with open(csvPath, 'a', encoding='utf-8') as f:
	writer = csv.writer(f, lineterminator = '\n')
	writer.writerow(['post type', 'post date', 'caption', 'likes', 'comments', 'video views', 'post url', 'post id'])

for media in medias:
	with open(csvPath, 'a', encoding='utf-8') as f:
		writer = csv.writer(f, lineterminator = '\n')
		writer.writerow([media.type, media.created_time, media.caption, media.likes_count, media.comments_count, media.video_views, media.link, media.identifier])

f.close()

print ('\nDone! Successfully scraped %s posts.' % len(medias))
print ('A link to download the CSV data file should be below.\n')
print ('**FYI**')
print ('The post dates will be in Unix timestamps...')
print ('Use the formula below to convert to regular date format.\n')
print ('    =(B2/86400)+DATE(1970,1,1)')
