from flask import *
from praw import *
from os import *
from random import *

""" Meme API by AnshAgarwal using Flask + PRAW """

app = Flask(__name__)
reddit = Reddit(
    client_id=getenv("CLIENT_ID"),
    client_secret=getenv("CLIENT_SECRET"),
    user_agent="python",
    username=getenv("USERNAME"),
    password=getenv("PASSWORD"))

@app.route('/',methods=['GET'])
def home():
	return "<h2> Sup People! </h2> <br> to get a random meme from a random meme subreddit, go to /get and if you want to get memes from a subreddit you wish then go to /get/(subreddit) to get memes from that subreddit :)"

@app.route('/get',methods=['GET'])
def _get():
	
	subreddit = reddit.subreddit(
		choice([
			'dankmemes',
			'me_irl',
			'memes']))

	submissions = subreddit.hot(limit=500)
	
	all_subs = []
	
	for submission in submissions:
		all_subs.append(submission)
	
	final_sub = choice(all_subs)
	
	if final_sub.selftext == "":
		selftext = "this post has no text"
	else:
		selftext = final_sub.selftext

	res = {
		'postTitle': str(final_sub.title),
		'postURL': str(reddit.config.reddit_url+final_sub.permalink),
		'imageURL': str(final_sub.url),
		'postText': str(selftext),
		'isNSFW': bool(final_sub.over_18),
		'isVideo': bool(final_sub.is_video)
	}
	
	return jsonify(res)
		
@app.route('/get/<string:sub>',methods=['GET'])
def _get_sub(sub):
	
	subreddit = reddit.subreddit(sub)
	submissions = subreddit.hot(limit=500)
	
	all_subs = []
	
	for submission in submissions:
		all_subs.append(submission)
	
	final_sub = choice(all_subs)
	
	if final_sub.selftext == "":
		selftext = "this post has no text"
	else:
		selftext = final_sub.selftext

	res = {
		'postTitle': str(final_sub.title),
		'postURL': str(reddit.config.reddit_url+final_sub.permalink),
		'imageURL': str(final_sub.url),
		'postText': str(selftext),
		'isNSFW': bool(final_sub.over_18),
		'isVideo': bool(final_sub.is_video)
	}
	
	return jsonify(res)
		

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=8080,debug=True)