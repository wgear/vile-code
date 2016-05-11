import json
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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _


class PublicChat(TemplateView):
    template_name = 'stream/public.html'

    def get_context_data(self, **kwargs):
        context = super(PublicChat, self).get_context_data(**kwargs)
        context['club'] = self.public
        context['is_owner'] = context['club'].owner_id == self.request.user.pk
        context['is_member'] = context['club'].members.filter(id=self.request.user.pk).count() > 0
        context['is_founder'] = context['club'].founders.filter(id=self.request.user.pk).count() > 0

        context['is_subscribed'] = context['is_owner'] or context['is_member'] or context['is_founder']
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
       return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.public = Public.objects.get(pk=int(kwargs.get('id', -1)))
        except:
            return redirect(reverse('404'))

        # Welcome message
        message = json.dumps({
            'user': {
                'id': request.user.pk,
                'image': request.user.image,
                'username': request.user.username
            },
            'public': {
                'id': self.public.pk,
                'image': self.public.image,
                'title': self.public.title
            },
            'message': _('%(username)s has connected to chat in %(title)s') % {
                'username': request.user.username,
                'title': self.public.title
            }
        })

        welcome = RedisMessage(json.dumps(message))
        RedisPublisher(facility=self.public.facility, broadcast=True).publish_message(welcome)

        return super(PublicChat, self).get(request, *args, **kwargs)


class UserChat(TemplateView):
    template_name = ''
