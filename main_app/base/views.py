# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView


class BaseView(TemplateView):
    """
    构造视图基类
    """
    redirect_class = HttpResponseRedirect
    form_class = None
    initial = {}

    json_content_type = 'application/json'

    def get_context_data(self, **kwargs):
        return super(BaseView, self).get_context_data(**kwargs)

    def render_to_json_response(self, status='0', msg=u'成功', result={}):
        # 错误提示
        context = {}
        context.update(status=status, msg=msg, result=result)

        return HttpResponse(json.dumps(context), content_type=self.json_content_type)

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        return self.initial.copy()

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        return self.form_class

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_json_response(status='2', msg=dict(form.errors).popitem()[1][0] if form.errors else '')

    def form_valid(self, form):
        return self.render_to_json_response()
