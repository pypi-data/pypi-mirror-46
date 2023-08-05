from django.conf.urls import url
from django.http import JsonResponse
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
import functools


def api_view(url_path: str = None, url_name: str = None, auth: bool = False, allowed_methods: list = None):
    """
    自动包装一个定制的视图的url映射
    url_path: api视图的backend的最后一个路径的名称, 默认为视图方法名称(替换下划线为横线)
    url_name: api视图对应的url定义中的name, 默认为资源类名称+视图方法名称
    auth: 指定是否需要用户验证
    allowed_methods: 用来制定自定义视图允许的请求方法列表
    """

    def view_decorator(view_func):
        view_func._is_api = True
        view_func._url_path = url_path
        view_func._url_name = url_name

        default_allowed_methods = ['get', 'options', 'head']
        final_methods = allowed_methods or default_allowed_methods

        @functools.wraps(view_func)
        def view_wrapper(self, request, *args, **kwargs):
            if auth:
                self.is_authenticated(request)
            self.method_check(request, final_methods)
            return view_func(self, request, *args, **kwargs)

        return view_wrapper

    return view_decorator


class BaseModelResource(ModelResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._handel_api_view()

    def _handel_api_view(self):
        self.prepend_url_list = []
        for attr_name in (attr_name for attr_name in dir(self) if attr_name not in dir(BaseModelResource)):
            attr_value = getattr(self, attr_name)
            if not callable(attr_value) or not hasattr(attr_value, '_is_api'):
                continue

            api_url_path = getattr(attr_value, '_url_path', None) or attr_name
            api_url_name = getattr(attr_value, '_url_name', None) or self._meta.resource_name + '_' + attr_name

            self.prepend_url_list.append(
                url(r'^(?P<resource_name>{})/{}{}'.format(self._meta.resource_name, api_url_path, trailing_slash()),
                    self.wrap_view(attr_name), name=api_url_name)
            )

    def prepend_urls(self):
        return self.prepend_url_list or super().prepend_urls()

    def json_return(self, data=None):
        if not data:
            data = {}
        return JsonResponse(data=data)
