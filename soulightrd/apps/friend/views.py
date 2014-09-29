# import ast

# from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
# from django.template import RequestContext
# from django.contrib.auth.models import User
# from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
# from django.contrib.auth.decorators import login_required

# from soulightrd.apps.main.models import UserProfile, SocialFriendList
# from soulightrd.settings import SITE_DOMAIN
# from soulightrd.apps.app_helper import get_user_login_object
# from soulightrd.apps.member.helper import get_user_common_info

# from soulightrd.apps.friend.provider.facebook_provider import FacebookFriendsProvider
# from allauth.socialaccount.models import SocialAccount

# import json, logging

# logger = logging.getLogger(__name__)

# @login_required
# def invite_friend(request):
# 	user_login = get_user_login_object(request)
# 	is_have_friend_list = False
# 	if user_login.get_profile().is_facebook_account():
# 		try:
# 			social_friend_list = SocialFriendList.objects.get(user_social_auth__user=user_login)
# 			if len(social_friend_list.friends.replace(" ","")) != 0:
# 				is_have_friend_list = True
# 		except:
# 			pass
# 	return render_to_response('apps/friend/page/main_page.html',{
# 			"is_have_friend_list": is_have_friend_list
# 		},context_instance=RequestContext(request))


# @login_required
# def get_facebook_friends(request):
# 	user_login = get_user_login_object(request)
# 	results = {}
# 	if user_login.get_profile().is_facebook_account():
# 		following_ids = user_login.get_profile().following.values_list('id', flat=True)
# 		social_friend_list = SocialFriendList.objects.get(user_social_auth__user=user_login)
# 		friends = social_friend_list.friends
# 		friends_list = friends[1:len(friends)-1].split(",")
# 		facebook_friends = []
# 		existing_friends = []
# 		for friend in friends_list:
# 			try:
# 				friend_id = friend[friend.index("'") + 1:friend.index(":")]
# 				friend_name = friend[friend.index(":") + 1:len(friend)-1]
# 				if friend_id in following_ids:
# 					user = UserProfile.objects.get(facebook_id=friend_id).user
# 					existing_friends.append({
# 						"user_info": get_user_common_info(user),
# 						"is_following": user_login.get_profile().is_following(user.username)
# 					})
# 				else:
# 					facebook_friends.append({
# 						"id": friend_id,
# 						"name": friend_name
# 					})
# 			except Exception as e:
# 				logger.exception(e)
# 				pass
# 		results['facebook_friends'] = facebook_friends
# 		results['existing_friends'] = existing_friends
# 	else:
# 		results['error'] = "Not facebook account"
# 	return HttpResponse(json.dumps(results,indent=2), content_type='application/json')


