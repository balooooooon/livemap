from balon import app, LOG
import facebook
import tweepy

from balon.controller.IBalloonSubject import IBalloonSubject


class SocialController(IBalloonSubject):
    def notify(self, flight_id):
        pass

    def __init__(self):
        pass

    MSG_FACEBOOK = "Nas balon sa prave nachadza vo vyske {}"
    MSG_TWITTER = "Nas balon sa prave nachadza vo vyske {}"

    def getTwitterApi(self):
        auth = tweepy.OAuthHandler(app.config['TWITTER_CONSUMER_KEY'], app.config['TWITTER_CONSUMER_SECRET'])
        auth.set_access_token(app.config['TWITTER_ACCESS_TOKEN'], app.config['TWITTER_ACCESS_TOKEN_SECRET'])
        return tweepy.API(auth)

    def getFacebookApi(self):
        graph = facebook.GraphAPI(app.config['FACEBOOK_ACCESS_TOKEN'])
        return graph

    def postFacebookStatus(self, altitude):
        api = self.getFacebookApi()
        LOG.info("Facebook API loaded")
        status = api.put_wall_post(message = self.MSG_FACEBOOK.format(altitude))
        # TODO exception logging & handling

    def postTwitterStatus(self, altitude):
        api = self.getTwitterApi()
        LOG.info("Twitter API loaded")
        status = api.update_status(status = self.MSG_TWITTER.format(altitude))
        # TODO exception logging & handling

    def postStatuses(self, altitude, timestamp):
        if ((end - start).total_seconds()) > 60:
            self.postFacebookStatus(altitude)
            self.postTwitterStatus(altitude)
