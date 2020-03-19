#!/home/pi/script-server/env/bin/python3

from context import Instagram # pylint: disable=no-name-in-module
import csv, time, os, sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--postcode", required=True, type=str, help="The part of the post URL after instagram.com")

args = parser.parse_args()

# postURL = input("Paste full post URL and press enter:\n")
if ".com" in args.postcode:
	postCode = input("\nThat was a URL... Please enter the post code by itself below.\n")
else: postCode = args.postcode
#postCode = postURL.replace("https://www.instagram.com/p/", "").replace("/", "")
maxComms = 10000

#csvPath = os.path.join(str(os.path.join(os.path.expanduser("~"), "Desktop")), '%s-likes.csv' % postCode)
csvPath = os.path.join('outputs/', '%s-comments.csv' % postCode)

proxies = {
	"http": "socks5h://x2923101:g2XbTQ6tHk@proxy-nl.privateinternetaccess.com:1080",
 	"https": "socks5h://x2923101:g2XbTQ6tHk@proxy-nl.privateinternetaccess.com:1080",
}

instagram = Instagram()
instagram.set_proxies(proxies)

print("\nScraping in progress... do not close this window.\n")

comments = instagram.get_media_comments_by_code(postCode, maxComms)

with open(csvPath, 'a', encoding='utf-8') as f:
	writer = csv.writer(f, lineterminator = '\n')
	writer.writerow(['comment_id', 'comment', 'username', 'is_private', 'is_verified'])

for comment in comments['comments']:
	with open(csvPath, 'a', encoding='utf-8') as f:
		writer = csv.writer(f, lineterminator = '\n')
		writer.writerow([comment.identifier, comment.text, comment.owner.username, comment.owner.is_private, comment.owner.is_verified])

f.close()

print ('\nDone! Successfully scraped %s comments.\n' % len(comments['comments']))
print ('A link to download the CSV data file should be below.\n')
