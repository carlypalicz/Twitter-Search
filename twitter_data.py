#  Author:  Carly Palicz
#  I pledge my honor that I have abided by the Stevens Honor System

# twitter_data.py searches Twitter for tweets matching a search term,
#      up to a maximun number, and sorts them in order of date posted

######  user must supply authentication keys where indicated

# to run from terminal window: 
#python3  twitter_data.py   --search_term  mysearch   --search_max  mymaxresults --search_sort mysort
# where:  mysearch is the term the user wants to search for;  default = music
#   and:  mymaxresults is the maximum number of resulta;  default = 30
#   and:  mysort is the data item the user wants to sort the output by

# other options used in the search:  lang = "en"  (English language tweets)
#  and  result_type = "popular"  (asks for most popular rather than most recent tweets)

# The program uses the TextBlob sentiment property to analyze the tweet for:
#  polarity (range -1 to 1)  and  
#  subjectivity (range 0 to 1 where 0 is objective and 1 is subjective)

# The program creates a .csv output file with a line for each tweet
#    including tweet data items and the sentiment information

from textblob import TextBlob	# needed to analyze text for sentiment
import argparse    				# for parsing the arguments in the command line
import csv						# for creating output .csv file
import tweepy					# Python twitter API package
import unidecode				# for processing text fields in the search results
from operator import itemgetter #added in order to sort results 

### PUT AUTHENTICATOIN KEYS HERE ###
CONSUMER_KEY = "BV2o0tJwnIYVgcXLBlI9hDCzw"
CONSUMER_KEY_SECRET = "865FxSTD8RA5J6cTdxICfzY4T5Z1L7RKWJyjBgsCk0Dqzcs6ED"
ACCESS_TOKEN = "703304163-9q0TeYNworht8GF3AcMi4InArehHOxiqHTVUzwKm"
ACCESS_TOKEN_SECRET = "jtZKQmq43p8gLEvD30XB5lQAifyp9XlZVYy3EqbN4wUT0"

# AUTHENTICATION (OAuth)
authenticate = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(authenticate)

# Get the input arguments - search_term and search_max
parser = argparse.ArgumentParser(description='Twitter Search')
parser.add_argument("--search_term", action='store', dest='search_term', default="music")
parser.add_argument("--search_max", action='store', dest='search_max', default=30)
#added a third argument so the user could select how to sort the results
parser.add_argument("--search_sort", action='store', dest='sort_by', default="created")

args = parser.parse_args()

search_term = args.search_term
search_max = int(args.search_max)
sort_by = args.sort_by

# create a .csv file to hold the results, and write the header line
csvFile = open('twitter_results.csv','w')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["username","userid","created", "text", "retweets", "followers",
    "friends","polarity","subjectivity"])

#added code: made a list of dictionaries for the results so they could be sorted before written
results = []

# do the twitter search
for tweet in tweepy.Cursor(api.search, q = search_term, lang = "en", 
		result_type = "popular").items(search_max):
		
    created = tweet.created_at				# date created
    text = tweet.text						# text of the tweet
    text = unidecode.unidecode(text) 
    retweets = tweet.retweet_count			# number of retweets
    username  = tweet.user.name            	# user name
    userid  = tweet.user.id              	# userid
    followers = tweet.user.followers_count 	# number of user followers
    friends = tweet.user.friends_count      # number of user friends
    
	# use TextBlob to determine polarity and subjectivity of tweet
    text_blob = TextBlob(text)
    polarity = text_blob.polarity
    subjectivity = text_blob.subjectivity

    #adds the dictionary item
    results.append({"username": username, "userid": userid, "created": created, "text": text, "retweets": retweets, "followers": followers,
    "friends": friends, "polarity": polarity, "subjectivity": subjectivity})

#sorts the list of dictionaries by tweet field specified
if sort_by == "created":
    results_sorted = sorted(results, key=itemgetter('created'), reverse=True)

elif sort_by == "retweets":
    results_sorted = sorted(results, key=itemgetter('retweets'), reverse=True)

elif sort_by == "followers":
    results_sorted = sorted(results, key=itemgetter('followers'), reverse=True)

#throws an error if the tweet field specific isnt valid
else:
    print("ERROR: sort_by argument must be 'retweets', 'followers', or 'created'. Note that 'created' is the default value.")
    exit()

for result in results_sorted:
    csvWriter.writerow([result["username"], result["userid"], result["created"], result["text"], result["retweets"], result["followers"], 
    result["friends"], result["polarity"], result["subjectivity"]])

csvFile.close()
