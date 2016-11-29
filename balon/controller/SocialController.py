from balon import app, LOG
import facebook
import tweepy



MSG_FACEBOOK = "N� bal�n sa pr�ve nach�dza vo v��ke {}"
MSG_TWITTER = "N� bal�n sa pr�ve nach�dza vo v��ke {}"

def getTwitterApi():
    auth = tweepy.OAuthHandler(app.config['TWITTER_CONSUMER_KEY'], app.config['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(app.config['TWITTER_ACCESS_TOKEN'], app.config['TWITTER_ACCESS_TOKEN_SECRET'])
    return tweepy.API(auth)

def getFacebookApi():
    graph = facebook.GraphAPI(app.config['FACEBOOK_ACCESS_TOKEN'])
    return graph


def postFacebookStatus(altitude):
    api = getFacebookApi()
    LOG.info("Facebook API loaded")
    status = graph.put_wall_post(message=MSG_FACEBOOK.format(altitude))
    #TODO exception logging & handling

def postTwitterStatus(altitude):
    api = getTwitterApi()
    LOG.info("Twitter API loaded")
    status = api.update_status(status=MSG_TWITTER.format(altitude))
    #TODO exception logging & handling

def postStatuses(altitude,timestamp):
    if ((end - start).total_seconds()) > 60 :
        postFacebookStatus(altitude)
        postTwitterStatus(altitude)
