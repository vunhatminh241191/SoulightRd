from soulightrd.apps.friend.provider import BaseFriendsProvider

from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp

import facebook

class FacebookFriendsProvider(BaseFriendsProvider):

    def fetch_friends(self, user):
        social_app = SocialApp.objects.get_current('facebook')
        oauth_token = SocialToken.objects.get(account=user, app=social_app).token

        graph = facebook.GraphAPI(oauth_token)

        return graph.get_connections("me", "friends")

    def fetch_friends_data(self, user):
        friends = self.fetch_friends(user)
        friends_data = []
        for friend in friends['data']:
            friends_data.append(str(friend['id']) + ":" + friend['name'])
        return friends_data
