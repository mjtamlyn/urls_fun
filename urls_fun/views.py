from django.core.urlresolvers import reverse
from django.http import HttpResponse


def hello(request):
    return HttpResponse('hello world')


def goodbye(request):
    url = reverse('hello')
    return HttpResponse('<a href="%s">Hello again</a>' % url)
