from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from soulightrd.apps.main.models import *

########################################
#                                      #
#      DEFINE CLASS ADMIN AREA         #
#                                      #
########################################
class SocialFriendListAdmin(admin.ModelAdmin):
    list_display = ['user_social_auth',"friends"]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user',"avatar"]


class MessageAdmin(admin.ModelAdmin):
    list_display = ['user_send','user_receive','content','date','status']

class EmailTrackingAdmin(admin.ModelAdmin):
    list_display = ['pk','to_emails',"email_template","text_content","context_data","status","send_time"]


class ConversationAdmin(admin.ModelAdmin):
    list_display = ['user1','user2','latest_message']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_type','unique_id','user','content','create_date','edit_date']


class ReportAdmin(admin.ModelAdmin):
    list_display = ['report_type','unique_id','date']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['notification_type','content','notify_from','date','status']


class PhotoAdmin(admin.ModelAdmin):
    search_fields = ["caption",'photo_type','user_post']
    list_display = ['unique_id',"caption",'photo_type','object_unique_id','user_post','upload_date']
    list_filter = ["caption",'photo_type','unique_id','user_post','upload_date']

########################################
#                                      #
#            REGISTER AREA             #
#                                      #
########################################
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Conversation,ConversationAdmin)
admin.site.register(SocialFriendList,SocialFriendListAdmin)
admin.site.register(EmailTracking,EmailTrackingAdmin)




