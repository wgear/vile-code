from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher
from public.models import Public
from person.models import Person


class PublicChat(TemplateView):
    template_name = 'stream/stream.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PublicChat, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PublicChat, self).get_context_data(**kwargs)
        context['public'] = Public.objects.filter(pk=int(kwargs.get('id'))).first()
        return context

    def post(self, request, id, *args, **kwargs):
        try:
            public = Public.objects.get(pk=int(id))
        except:
            return HttpResponse(content='Error', status=404)

        publisher = RedisPublisher(facility='public.{}'.format(str(public.pk)), broadcast=True)
        message = RedisMessage(request.POST.get('message', ''))
        publisher.publish_message(message)
        return HttpResponse('OK')


class UserChat(TemplateView):
    template_name = ''
