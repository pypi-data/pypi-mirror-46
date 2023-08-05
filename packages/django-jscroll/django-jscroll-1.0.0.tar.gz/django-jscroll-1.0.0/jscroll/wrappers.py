from django.core.paginator import Paginator, EmptyPage
from django.template.loader import get_template
from django.views.generic import View
from django.core.cache import cache
from django.shortcuts import render
from django.apps import apps
from re import sub

class JScroll:
    def __init__(self, token, template, queryset, request=None, context={}):
        cache.set('%s-jscroll-%s' %  (token, template), queryset)
        cache.set('%s-jscroll-context-%s' %  (token, template), context)

        # To render the first page initially.
        paginator     = Paginator(queryset, 15)
        self.elems    = paginator.page(1)
        self.template = template
        self.token    = token
        self.request  = request
        self.context  = context

    def as_window(self):
        viewport = sub('/|\.', '', self.template)
        tmp      = get_template('jscroll/jscroll-window.html')
        tmpctx   = {'template': self.template,
        'viewport': viewport, 'elems': self.elems, 'token': self.token}

        tmpctx.update(self.context)
        return tmp.render(tmpctx, self.request)

    def as_div(self):
        viewport = sub('/|\.', '', self.template)
        tmp      = get_template('jscroll/jscroll.html')
        tmpctx   = {'template': self.template,
        'viewport': viewport, 'elems': self.elems, 'token': self.token}

        tmpctx.update(self.context)
        return tmp.render(tmpctx, self.request)

class JScrollView(View):
    def get(self, request):
        template  = request.GET.get('jscroll-template')
        page      = request.GET.get('page')
        token     = request.GET.get('token')
        queryset  = cache.get('%s-jscroll-%s' % (token, template))
        context   = cache.get('%s-jscroll-context-%s' % (token, template))

        paginator = Paginator(queryset, 20)
        elems     = paginator.page(page)
        tmpctx    = {'elems': elems}

        tmpctx.update(context)
        return render(request, template, tmpctx)



