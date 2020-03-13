import json
from datetime import datetime
import os
import tweepy as twp
import re
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
#import preprocessor as p

def prolyzer(event, context):
	consumer_key = 'k7bmKlFjUf3eyFcwpqi1D34aZ'
	consumer_secret = 'l4u0IRz5AYt9HXThR5lWTN41dTX5UMrs3VmZnmNPZky1mJmf7M'
	access_token = '1263822842-QDqzja2ZGdE2RWlL12UxEnMCcGsDUxDkxsfdDZc'
	access_token_secret = 'gcRxVFfwpeQr8mGF4BLP9ScK2qJnxWZxnneoq0fQFDznq'

	auth = twp.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = twp.API(auth)
    
	authenticator = IAMAuthenticator('G7Um77PYTSWaI23-QJg-NqJrDrECeUnzn1_nSCbPkS-Q')
	tone_analyzer = ToneAnalyzerV3(
	version='2017-09-21',
	authenticator=authenticator
	)

	tone_analyzer.set_service_url('https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/046af756-8b3b-4b48-be22-627b30bf6321')

	tone_analyzer.set_disable_ssl_verification(False)

	#tweets = api.user_timeline()
	search_words = "#covid-19"
	date_since = "2019-12-20"

	totalTweets = ''
	# Collect tweets
	tweets = twp.Cursor(api.search,q=search_words,lang="en",since=date_since).items(10)
	#p.set_options(p.OPT.URL,p.OPT.MENTION,p.OPT.HASHTAG,p.OPT.RESERVED,p.OPT.NUMBER)
	for tweet in tweets:
		#totalTweets = totalTweets + p.clean(tweet.text)+ '\n'
		totalTweets = totalTweets + ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet.text).split())

	print(totalTweets)
	tone_analysis = tone_analyzer.tone(
	{'text': totalTweets},
	content_type='application/json'
	).get_result()

	response = {
		"statusCode": 200,
		"body": json.dumps({
			"tone_response": tone_analysis
		})
	}

	return response


handler = prolyzer
