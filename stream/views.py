from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher
from public.models import Public
from person.models import Person


class PublicChat(TemplateView):
    template_name = 'stream/stream.html'

    def get_context_data(self, **kwargs):
        context = super(PublicChat, self).get_context_data(**kwargs)
        context['public'] = Public.objects.filter(pk=int(kwargs.get('id'))).first()
        return context

    def get(self, request, *args, **kwargs):
        welcome = RedisMessage('Hello everybody')  # create a welcome message to be sent to everybody
        RedisPublisher(facility='foobar', broadcast=True).publish_message(welcome)
        return super(PublicChat, self).get(request, *args, **kwargs)


class UserChat(TemplateView):
    template_name = ''
