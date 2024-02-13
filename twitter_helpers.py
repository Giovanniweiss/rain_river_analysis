import tweepy

def get_api_tokens(text_file):
    tokens = {}
    with open(text_file, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            tokens[key] = value
    return tokens

def tweet(message):
    tokens = get_api_tokens("API_access_tokens.txt")
    client = tweepy.Client(bearer_token=tokens['bearer_token'],
    consumer_key=tokens['consumer_key'], consumer_secret=tokens['consumer_secret'],
    access_token=tokens['access_token'], access_token_secret=tokens['access_token_secret'])
    
    try:
        client.create_tweet(text = message)
        print(message)
        print("Message successfully published to Twitter.")
        return 0
    except Exception as e:
        print("An error has occurred while trying to publish the tweet: ", e)
        return 1