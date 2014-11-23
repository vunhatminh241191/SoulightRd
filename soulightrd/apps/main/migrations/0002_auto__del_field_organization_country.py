# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Organization.country'
        db.delete_column(u'main_organization', 'country')


    def backwards(self, orm):
        # Adding field 'Organization.country'
        db.add_column(u'main_organization', 'country',
                      self.gf('django_countries.fields.CountryField')(default=0, max_length=2),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'cities_light.city': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('region', 'name'), ('region', 'slug'))", 'object_name': 'City'},
            'alternate_names': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']"}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'feature_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_ascii': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'population': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Region']", 'null': 'True', 'blank': 'True'}),
            'search_names': ('cities_light.models.ToSearchTextField', [], {'default': "''", 'max_length': '4000', 'db_index': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name_ascii'"})
        },
        u'cities_light.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'alternate_names': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'code2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'code3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'name_ascii': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name_ascii'"}),
            'tld': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '5', 'blank': 'True'})
        },
        u'cities_light.region': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('country', 'name'), ('country', 'slug'))", 'object_name': 'Region'},
            'alternate_names': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities_light.Country']"}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'geoname_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_ascii': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name_ascii'"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reports': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'comment_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['main.Report']"}),
            'unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.conversation': {
            'Meta': {'object_name': 'Conversation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'latest_message'", 'null': 'True', 'to': u"orm['main.Message']"}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'messages'", 'null': 'True', 'to': u"orm['main.Message']"}),
            'unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user1'", 'to': u"orm['auth.User']"}),
            'user2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user2'", 'to': u"orm['auth.User']"})
        },
        u'main.donation': {
            'Meta': {'object_name': 'Donation'},
            'amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'amount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'donation_project'", 'to': u"orm['main.Project']"}),
            'transaction_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'donation_user'", 'to': u"orm['auth.User']"})
        },
        u'main.emailtracking': {
            'Meta': {'object_name': 'EmailTracking'},
            'context_data': ('django.db.models.fields.TextField', [], {}),
            'email_template': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '50'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '350', 'blank': 'True'}),
            'text_content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'to_emails': ('django.db.models.fields.TextField', [], {})
        },
        u'main.message': {
            'Meta': {'object_name': 'Message'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user_receive': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_receive'", 'to': u"orm['auth.User']"}),
            'user_send': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_send'", 'to': u"orm['auth.User']"})
        },
        u'main.notification': {
            'Meta': {'object_name': 'Notification'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'notify_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notify_from'", 'to': u"orm['auth.User']"}),
            'notify_to': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'notify_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.organization': {
            'Meta': {'object_name': 'Organization'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organization_city'", 'to': u"orm['cities_light.City']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organization_created_by_user'", 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'normal_member': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'organization_normal_member'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'verify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'main.organizationboardmember': {
            'Meta': {'object_name': 'OrganizationBoardMember'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'board_member_organization'", 'to': u"orm['main.Organization']"}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'board_member_projects'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['main.Project']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'board_member_user'", 'to': u"orm['auth.User']"})
        },
        u'main.organizationboardmemberinvitation': {
            'Meta': {'object_name': 'OrganizationBoardMemberInvitation'},
            'board_member_invite': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'board_member_invite'", 'to': u"orm['main.OrganizationBoardMember']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitation_status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'invited_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invited_member'", 'to': u"orm['auth.User']"})
        },
        u'main.organizationjoinrequest': {
            'Meta': {'object_name': 'OrganizationJoinRequest'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organization'", 'to': u"orm['main.Organization']"}),
            'request_status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'user_request': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_request'", 'to': u"orm['main.Volunteer']"})
        },
        u'main.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'object_unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'photo_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user_post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.project': {
            'Meta': {'object_name': 'Project'},
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'project_comments'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['main.Comment']"}),
            'current_funding': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'current_funding_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'current_volunteer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'followers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'project_followers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'funding_goal': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'funding_goal_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_organization'", 'to': u"orm['main.Organization']"}),
            'project_duration': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'project_end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'project_image': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'main_image'", 'to': u"orm['main.Photo']"}),
            'project_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_location'", 'to': u"orm['cities_light.City']"}),
            'project_start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'project_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'volunteer_goal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'main.projectactivity': {
            'Meta': {'object_name': 'ProjectActivity'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_proof': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'project_activity_image_proof'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['main.Photo']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_activity'", 'to': u"orm['main.Project']"}),
            'responsible_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_activity_responsible_member'", 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.report': {
            'Meta': {'object_name': 'Report'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'report_content': ('django.db.models.fields.TextField', [], {}),
            'report_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user_report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_report'", 'blank': 'True', 'to': u"orm['auth.User']"})
        },
        u'main.socialfriendlist': {
            'Meta': {'object_name': 'SocialFriendList'},
            'friends': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_social_auth': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'social_account'", 'unique': 'True', 'to': u"orm['socialaccount.SocialAccount']"})
        },
        u'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'avatar'", 'null': 'True', 'to': u"orm['main.Photo']"}),
            'basic_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cover_picture': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cover_picture'", 'null': 'True', 'to': u"orm['main.Photo']"}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'following_projects': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_following_projects'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['main.Project']"}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_organization_board_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'privacy_status': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'reports': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['main.Report']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'main.volunteer': {
            'Meta': {'object_name': 'Volunteer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_signed_confirmation': ('django.db.models.fields.BooleanField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'volunteer_project'", 'to': u"orm['main.Project']"}),
            'register_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'volunteer_user'", 'to': u"orm['auth.User']"})
        },
        u'socialaccount.socialaccount': {
            'Meta': {'unique_together': "(('provider', 'uid'),)", 'object_name': 'SocialAccount'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'extra_data': ('allauth.socialaccount.fields.JSONField', [], {'default': "'{}'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['main']