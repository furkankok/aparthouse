from django.urls import path, include
from oauth2_provider.decorators import protected_resource
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from functools import wraps
from django.core.paginator import Paginator
from utils import error_response, success_response


def check_model_permission(permission_type):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(instance, request, *args, **kwargs):
            model_name = instance.model._meta.model_name
            perm_code = f'{instance.model._meta.app_label}.{permission_type}_{model_name}'
            if request.user.is_superuser or request.user.has_perm(perm_code):
                return view_func(instance, request, *args, **kwargs)
            else:
                return error_response("Erişim izniniz yok")
        return _wrapped_view
    return decorator


class ModelToURL:
    def __init__(self, model):
        self.model = model

    @method_decorator(protected_resource())
    @method_decorator(require_http_methods(["POST"]))
    @check_model_permission('add')
    def model_add(self, request, *args, **kwargs):
        for field in self.model._meta.fields:
            if field.name not in request.POST and field.name != 'id' and not field.null and not field.blank:
                return error_response(f"{field.name} field is required")
        data = self.model()
        for field in self.model._meta.fields:
            if field.name in request.POST:
                setattr(data, field.name, request.POST[field.name])
        data.save()
        return success_response(data.to_dict())

    @method_decorator(protected_resource())
    @method_decorator(require_http_methods(["POST"]))
    @check_model_permission('change')
    def model_change(self, request, pk):
        data = self.model.objects.filter(pk=pk).last()
        if not data:
            return error_response("Data not found")
        for field in self.model._meta.fields:
            if field.name in request.POST:
                setattr(data, field.name, request.POST[field.name])
        data.save()
        return success_response(data.to_dict())

    
    @method_decorator(protected_resource())
    @method_decorator(require_http_methods(["GET"]))
    @check_model_permission('view')
    def model_view(self, request, pk):
        data = self.model.objects.filter(pk=pk).last()
        if not data:
            return error_response("Data not found")
        return success_response(data.to_dict())

    @method_decorator(protected_resource())
    @method_decorator(require_http_methods(["POST"]))
    @check_model_permission('delete')
    def model_delete(self, request, pk):
        if not request.user.is_superuser:
            return error_response("You are not authorized to delete data")
        data = self.model.objects.filter(pk=pk).last()
        if not data:
            return error_response("Data not found")
        data.delete()
        return success_response("Data deleted")
    
    # @method_decorator(protected_resource())
    @method_decorator(require_http_methods(["GET"]))
    # @check_model_permission('view')
    def model_list(self, request):
        data = self.model.objects.all()
        # pagination
        paginate = Paginator(data, 50)
        page = request.GET.get('page', 1)
        data = paginate.page(page)
        data = [i.to_dict() for i in data]
        return success_response(data, paginate=paginate)

    def get_urls(self):
        return include([
            # path('add', self.model_add),
            # path('change/<int:pk>', self.model_change),
            # path('view/<int:pk>', self.model_view),
            # path('delete/<int:pk>', self.model_delete),
            path('', self.model_list),
        ])