import re

from django.core.urlresolvers import ResolverMatch, Resolver404, NoReverseMatch

from . import views


class URLPattern(object):
    def __init__(self, match, view, name):
        self.match = match
        self.view = view
        self.name = name

    def resolve(self, path):
        if path == self.match:
            return ResolverMatch(self.view, (), {}, self.name)


patterns = [
    URLPattern('hello/', views.hello, 'hello'),
    URLPattern('goodbye/', views.goodbye, 'goodbye'),
]


class URLResolver(object):
    patterns = patterns

    def __init__(self, match):
        self.match = match
        self.regex = re.compile(self.match)
        self.name_lookup = {pattern.name: pattern for pattern in self.patterns}

    def resolve(self, path):
        if path.startswith(self.match):
            sub_path = path[len(self.match):]
            for pattern in self.patterns:
                match = pattern.resolve(sub_path)
                if match:
                    return match
        raise Resolver404({'path': path})

    def _reverse_with_prefix(self, view, prefix, *args, **kwargs):
        if view in self.name_lookup:
            return prefix + self.name_lookup[view].match
        raise NoReverseMatch('nothing here')


resolver = URLResolver
