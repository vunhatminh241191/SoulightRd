# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SocialFriendList'
        db.create_table(u'main_socialfriendlist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_social_auth', self.gf('django.db.models.fields.related.OneToOneField')(related_name='social_account', unique=True, to=orm['socialaccount.SocialAccount'])),
            ('friends', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'main', ['SocialFriendList'])

        # Adding model 'EmailTracking'
        db.create_table(u'main_emailtracking', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_emails', self.gf('django.db.models.fields.TextField')()),
            ('email_template', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=350, blank=True)),
            ('text_content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('context_data', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=50)),
            ('send_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['EmailTracking'])

        # Adding model 'Photo'
        db.create_table(u'main_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unique_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('upload_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user_post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('photo_type', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('object_unique_id', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'main', ['Photo'])

        # Adding model 'Notification'
        db.create_table(u'main_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unique_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('notification_type', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('notify_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notify_from', to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Notification'])

        # Adding M2M table for field notify_to on 'Notification'
        m2m_table_name = db.shorten_name(u'main_notification_notify_to')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('notification', models.ForeignKey(orm[u'main.notification'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['notification_id', 'user_id'])

        # Adding model 'Message'
        db.create_table(u'main_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unique_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user_send', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_send', to=orm['auth.User'])),
            ('user_receive', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_receive', to=orm['auth.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Message'])

        # Adding model 'Conversation'
        db.create_table(u'main_conversation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unique_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user1', to=orm['auth.User'])),
            ('user2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user2', to=orm['auth.User'])),
            ('latest_message', self.gf('django.db.models.fields.related.ForeignKey')(related_name='latest_message', null=True, to=orm['main.Message'])),
        ))
        db.send_create_signal(u'main', ['Conversation'])

        # Adding M2M table for field messages on 'Conversation'
        m2m_table_name = db.shorten_name(u'main_conversation_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conversation', models.ForeignKey(orm[u'main.conversation'], null=False)),
            ('message', models.ForeignKey(orm[u'main.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['conversation_id', 'message_id'])

        # Adding model 'Comment'
        db.create_table(u'main_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unique_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('comment_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Comment'])

        # Adding M2M table for field reports on 'Comment'
        m2m_table_name = db.shorten_name(u'main_comment_reports')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comment', models.ForeignKey(orm[u'main.comment'], null=False)),
            ('report', models.ForeignKey(orm[u'main.report'], null=False))
        ))
        db.create_unique(m2m_table_name, ['comment_id', 'report_id'])

        # Adding model 'Report'
        db.create_table(u'main_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unique_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('report_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('user_report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_report', blank=True, to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('report_content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'main', ['Report'])

        # Adding model 'OrganizationBoardMember'
        db.create_table(u'main_organizationboardmember', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='board_member_user', to=orm['auth.User'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='board_member_organization', to=orm['main.Organization'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'main', ['OrganizationBoardMember'])

        # Adding model 'Organization'
        db.create_table(u'main_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unique_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'main', ['Organization'])

        # Adding M2M table for field normal_member on 'Organization'
        m2m_table_name = db.shorten_name(u'main_organization_normal_member')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organization', models.ForeignKey(orm[u'main.organization'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['organization_id', 'user_id'])

        # Adding model 'Project'
        db.create_table(u'main_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unique_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('project_image', self.gf('django.db.models.fields.related.ForeignKey')(related_name='main_image', to=orm['main.Photo'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_organization', to=orm['main.Organization'])),
            ('project_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('funding_goal_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('funding_goal', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
            ('current_funding_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('current_funding', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
            ('volunteer_goal', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('current_volunteer', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('project_duration', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('project_start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('project_end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('project_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_location', to=orm['cities_light.City'])),
        ))
        db.send_create_signal(u'main', ['Project'])

        # Adding M2M table for field comments on 'Project'
        m2m_table_name = db.shorten_name(u'main_project_comments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'main.project'], null=False)),
            ('comment', models.ForeignKey(orm[u'main.comment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'comment_id'])

        # Adding M2M table for field followers on 'Project'
        m2m_table_name = db.shorten_name(u'main_project_followers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'main.project'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'user_id'])

        # Adding model 'ProjectActivity'
        db.create_table(u'main_projectactivity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('responsible_member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_activity_responsible_member', to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'main', ['ProjectActivity'])

        # Adding M2M table for field image_proof on 'ProjectActivity'
        m2m_table_name = db.shorten_name(u'main_projectactivity_image_proof')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('projectactivity', models.ForeignKey(orm[u'main.projectactivity'], null=False)),
            ('photo', models.ForeignKey(orm[u'main.photo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['projectactivity_id', 'photo_id'])

        # Adding model 'Payment'
        db.create_table(u'main_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payment_user', to=orm['auth.User'])),
            ('amount_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('amount', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
            ('transaction_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Payment'])

        # Adding model 'UserProfile'
        db.create_table(u'main_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('basic_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='m', max_length=1)),
            ('avatar', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='avatar', null=True, to=orm['main.Photo'])),
            ('cover_picture', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cover_picture', null=True, to=orm['main.Photo'])),
            ('privacy_status', self.gf('django.db.models.fields.CharField')(default='1', max_length=1)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('facebook_id', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('is_organization_board_member', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('phone', self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128, blank=True)),
        ))
        db.send_create_signal(u'main', ['UserProfile'])

        # Adding M2M table for field reports on 'UserProfile'
        m2m_table_name = db.shorten_name(u'main_userprofile_reports')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'main.userprofile'], null=False)),
            ('report', models.ForeignKey(orm[u'main.report'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'report_id'])

        # Adding M2M table for field following_projects on 'UserProfile'
        m2m_table_name = db.shorten_name(u'main_userprofile_following_projects')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'main.userprofile'], null=False)),
            ('project', models.ForeignKey(orm[u'main.project'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'project_id'])


    def backwards(self, orm):
        # Deleting model 'SocialFriendList'
        db.delete_table(u'main_socialfriendlist')

        # Deleting model 'EmailTracking'
        db.delete_table(u'main_emailtracking')

        # Deleting model 'Photo'
        db.delete_table(u'main_photo')

        # Deleting model 'Notification'
        db.delete_table(u'main_notification')

        # Removing M2M table for field notify_to on 'Notification'
        db.delete_table(db.shorten_name(u'main_notification_notify_to'))

        # Deleting model 'Message'
        db.delete_table(u'main_message')

        # Deleting model 'Conversation'
        db.delete_table(u'main_conversation')

        # Removing M2M table for field messages on 'Conversation'
        db.delete_table(db.shorten_name(u'main_conversation_messages'))

        # Deleting model 'Comment'
        db.delete_table(u'main_comment')

        # Removing M2M table for field reports on 'Comment'
        db.delete_table(db.shorten_name(u'main_comment_reports'))

        # Deleting model 'Report'
        db.delete_table(u'main_report')

        # Deleting model 'OrganizationBoardMember'
        db.delete_table(u'main_organizationboardmember')

        # Deleting model 'Organization'
        db.delete_table(u'main_organization')

        # Removing M2M table for field normal_member on 'Organization'
        db.delete_table(db.shorten_name(u'main_organization_normal_member'))

        # Deleting model 'Project'
        db.delete_table(u'main_project')

        # Removing M2M table for field comments on 'Project'
        db.delete_table(db.shorten_name(u'main_project_comments'))

        # Removing M2M table for field followers on 'Project'
        db.delete_table(db.shorten_name(u'main_project_followers'))

        # Deleting model 'ProjectActivity'
        db.delete_table(u'main_projectactivity')

        # Removing M2M table for field image_proof on 'ProjectActivity'
        db.delete_table(db.shorten_name(u'main_projectactivity_image_proof'))

        # Deleting model 'Payment'
        db.delete_table(u'main_payment')

        # Deleting model 'UserProfile'
        db.delete_table(u'main_userprofile')

        # Removing M2M table for field reports on 'UserProfile'
        db.delete_table(db.shorten_name(u'main_userprofile_reports'))

        # Removing M2M table for field following_projects on 'UserProfile'
        db.delete_table(db.shorten_name(u'main_userprofile_following_projects'))


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
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
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'normal_member': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'organization_normal_member'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128'}),
            'unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'main.organizationboardmember': {
            'Meta': {'object_name': 'OrganizationBoardMember'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'board_member_organization'", 'to': u"orm['main.Organization']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'board_member_user'", 'to': u"orm['auth.User']"})
        },
        u'main.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'amount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transaction_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payment_user'", 'to': u"orm['auth.User']"})
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
            'responsible_member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_activity_responsible_member'", 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.report': {
            'Meta': {'object_name': 'Report'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128', 'blank': 'True'}),
            'privacy_status': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            'reports': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['main.Report']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
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