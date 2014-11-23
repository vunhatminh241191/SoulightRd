from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, AnonymousUser
from django.utils import simplejson, timezone
from django.core import serializers
from django.contrib.auth.decorators import login_required

from frittie.apps.main.models import Message, Conversation
from frittie.apps.app_helper import get_user_login_object

import json, logging, datetime

logger = logging.getLogger(__name__)

APP_NAME = "message"

class ConversationView(AppBaseView,ListView):
	app_name = APP_NAME
	template_name = "conversation"

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ConversationView, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		user_login = get_user_login_object(self.request)
		return Conversation.objects.filter(Q(user1=user_login) | Q(user2=user_login)).order_by("-latest_message__date")[:20]


class MessageView(AppBaseView,ListView):
	app_name = APP_NAME
	template_name = "message"
	conversation = None
	user_chat = None

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(MessageView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['conversation'] = self.conversation
        context['user_chat'] = self.user_chat
        return context

	def get_queryset(self):
		user_login = get_object_or_404(self.request)
		self.conversation = get_object_or_404(Conversation,unique_id=self.kwargs.get('conversation_unique_id'))
		self.user_chat = conversation.user1
		if conversation.user2.username != user_login.username:
			self.user_chat = conversation.user2
		new_messages = conversation.messages.filter(status="1")
		for message in new_messages:
			message.status = "0"
			message.save()
		messages = conversation.messages.order_by("date")[:100]
		return messages



