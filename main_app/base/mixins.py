# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.http import HttpResponse
from django.conf import settings
try:
    import ujson as json
except ImportError:
    import json


class JsonResponse(object):

    json_content_type = 'application/json'

    def render_to_json_sucsses(self, status='0', msg=u'成功',code=200, result={},**kwargs):
        context = {

            "status":status,
            "code": code,
            "msg": msg,
            "result": result
        }

        context.update(**kwargs)

        return HttpResponse(json.dumps(context), content_type=self.json_content_type)

    def render_to_json_error(self,status='1',error_string=u"失败", code=500,result={}, **kwargs):
        data = {
            "status":status,
            "code": code,
            "msg": error_string,
            "result": result
        }
        data.update(kwargs)

        return HttpResponse(json.dumps(data), content_type=self.json_content_type)



class SignatureRequiredMixin(object):


    def signature_required(self, request):
        nonce = request.GET.get("nonce")
        timestamp = request.GET.get("timestamp")
        signature = request.GET.get("signature")

        if self.check_signature(settings.THIRD_PART_TOKEN, signature, timestamp, nonce):
            return True

    def check_signature(self, token, signature, timestamp, nonce):
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        import hashlib

        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return True

    def dispatch(self, request, *args, **kwargs):
        if not self.signature_required(request):
            return JsonResponse({'status': 1, 'msg': u'认证失败'})

        return super(SignatureRequiredMixin, self).dispatch(request, *args, **kwargs)



class LoginRequiredMixin(object):
    """
    是否登录校验
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)




class PermissionRequireMixin(object):
    """
    权限控制
    """

    required_permissions = ()
    superuser_permission = False

    def _has_perm(self):
        user = self.request.user

        if not isinstance(self.required_permissions, (list, tuple)):
            raise ValueError('required_permissions need list or set!')

        if set(self.required_permissions).issubset(set(user.permission_cache)) or user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if request.user.is_authenticated():
            if not hasattr(user, 'permission_cache'):
                user.get_all_permissions()
            if not self._has_perm():
                return HttpResponseForbidden()
        if self.superuser_permission and not user.is_superuser:
            return HttpResponseForbidden()

        return super(PermissionRequireMixin, self).dispatch(request, *args, **kwargs)


class PaginateMixin(object):
    """
    分页处理
    """

    allow_empty = True
    page_size = 20
    paginate_orphans = 0
    paginator_class = Paginator
    page_kwarg = 'page'

    def range_list(self, page):
        num = page.number
        total = page.paginator.num_pages
        page_range = list(page.paginator.page_range)

        if num <= 5:
            return page_range[:6]
        elif num > total - 3:
            return page_range[total-6:total]
        else:
            return page_range[num-3:num+3]

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1

        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404("Page is not 'last', nor can it be converted to an int.")
        try:
            page = paginator.page(page_number)
            page.range_list = self.range_list(page)
            return page
        except InvalidPage as e:
            raise Http404('Invalid page (%(page_number)s): %(message)s' % {
                'page_number': page_number,
                'message': str(e)
            })

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs):
        """
        Return an instance of the paginator for this view.
        """
        return self.paginator_class(
            queryset, per_page, orphans=orphans,
            allow_empty_first_page=allow_empty_first_page, **kwargs)

    def get_paginate_orphans(self):
        """
        Returns the maximum number of orphans extend the last page by when
        paginating.
        """
        return self.paginate_orphans

    def get_allow_empty(self):
        """
        Returns ``True`` if the view should display empty lists, and ``False``
        if a 404 should be raised instead.
        """
        return self.allow_empty
