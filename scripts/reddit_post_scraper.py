#!/home/pi/script-server/env/bin/python3

#from context import Instagram # pylint: disable=no-name-in-module
from igramscraper.instagram import Instagram
import csv, time, os, sys, argparse, praw
import pandas as pd
from time import sleep
from os.path import isfile
reddit = praw.Reddit()

parser = argparse.ArgumentParser()
parser.add_argument("--subreddit", required=True, type=str, help="The subreddit to scrape")
parser.add_argument("--limit", required=True, type=int, default=999, help="Maximum number of posts to scrape")
args = parser.parse_args()

subreddit = args.subreddit
limit = args.limit

class SubredditScraper:

    #def __init__(self, sub, sort='new', lim=900, mode='w'):
    def __init__(self, sub, sort='new', lim=900, mode='w'):
        self.sub = sub
        self.sort = sort
        self.lim = lim
        self.mode = mode

#        print(
#            f'SubredditScraper instance created with values '
#            f'sub = {sub}, sort = {sort}, lim = {lim}, mode = {mode}')

    def set_sort(self):
        if self.sort == 'new':
            return self.sort, reddit.subreddit(self.sub).new(limit=self.lim)
        elif self.sort == 'top':
            return self.sort, reddit.subreddit(self.sub).top(limit=self.lim)
        elif self.sort == 'hot':
            return self.sort, reddit.subreddit(self.sub).hot(limit=self.lim)
        else:
            self.sort = 'hot'
            print('Sort method was not recognized, defaulting to hot.')
            return self.sort, reddit.subreddit(self.sub).hot(limit=self.lim)

    def get_posts(self):
        """Get unique posts from a specified subreddit."""

        sub_dict = {
            'created_utc': [], 'is_self_post': [], 'id': [], 'title': [],
            'self_text': [], 'author': [], 'score': [], 'upvotes': [], 'downvotes': [],
            'num_comments': [], 'permalink': []}
        csv = f'outputs/new_{self.sub}_posts.csv'

        # Attempt to specify a sorting method.
        sort, subreddit = self.set_sort()

        # Set csv_loaded to True if csv exists since you can't evaluate the
        # truth value of a DataFrame.
        df, csv_loaded = (pd.read_csv(csv), 1) if isfile(csv) else ('', 0)

#        print(f'csv = {csv}')
#        print(f'After set_sort(), sort = {sort} and sub = {self.sub}')
#        print(f'csv_loaded = {csv_loaded}')

        print(f'Collecting information from r/{self.sub}.\n')
        for post in subreddit:

            # Check if post.id is in df and set to True if df is empty.
            # This way new posts are still added to dictionary when df = ''
            unique_id = post.id not in tuple(df.id) if csv_loaded else True

            # Save any unique, non-stickied posts with descriptions to sub_dict.
            if unique_id:
                sub_dict['is_self_post'].append(post.is_self)
                sub_dict['created_utc'].append(post.created_utc)
                sub_dict['author'].append(post.author)
                sub_dict['self_text'].append(post.selftext)
                sub_dict['title'].append(post.title)
                sub_dict['id'].append(post.id)
                sub_dict['num_comments'].append(post.num_comments)
                sub_dict['score'].append(post.score)
                sub_dict['ups'].append(post.ups)
                sub_dict['downs'].append(post.downs)
                sub_dict['permalink'].append('http://reddit.com' + post.permalink)
            sleep(0.1)

        # pprint(sub_dict)
        new_df = pd.DataFrame(sub_dict)

        # Add new_df to df if df exists then save it to a csv.
        if 'DataFrame' in str(type(df)) and self.mode == 'w':
            pd.concat([df, new_df], axis=0, sort=0).to_csv(csv, index=False)
            print(
                f'{len(new_df)} new posts collected and saved.'
		f'\nA link to download the CSV data file should be below.\n'
		f'\n**FYI**\n'
		f'The post dates will be in Unix timestamps...\n'
		f'Use the formula below to convert to regular date format.\n'
		f'    =(B2/86400)+DATE(1970,1,1)')
        elif self.mode == 'w':
            new_df.to_csv(csv, index=False)
            print(
                f'{len(new_df)} new posts collected and saved.'
                f'\nA link to download the CSV data file should be below.\n'
                f'\n**FYI**\n'
                f'The post dates will be in Unix timestamps...\n'
                f'Use the formula below to convert to regular date format.\n'
                f'    =(B2/86400)+DATE(1970,1,1)')
        else:
            print(
                f'{len(new_df)} posts were collected but they were not '
                f'added to {csv} because mode was set to "{self.mode}"')

if __name__ == '__main__':
    SubredditScraper(subreddit, lim=limit, mode='w', sort='new').get_posts()
