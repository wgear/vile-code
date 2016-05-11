from cleave.encrypt import Encrypt
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
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
        context['public'] = self.public
        return context

    def get(self, request, *args, **kwargs):
        try:
            self.public = Public.objects.get(pk=int(kwargs.get('id', -1)))
        except:
            return redirect(reverse('404'))

        welcome = RedisMessage('Hello everybody')
        RedisPublisher(facility=self.public.facility, broadcast=True).publish_message(welcome)

        return super(PublicChat, self).get(request, *args, **kwargs)


class UserChat(TemplateView):
    template_name = ''
