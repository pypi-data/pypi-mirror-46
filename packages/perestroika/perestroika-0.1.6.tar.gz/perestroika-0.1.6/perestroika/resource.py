from typing import Dict, Union, Optional

import attr

from perestroika.methods import Method


@attr.s
class DjangoResource:
    from django.views.decorators.csrf import csrf_exempt

    methods: Optional[Dict[str, Method]] = None
    cache_control: Dict[str, Union[bool, int]] = attr.Factory(dict)

    @csrf_exempt
    def handler(self, request):
        from django.http import HttpResponseNotAllowed
        from django.utils.cache import patch_cache_control

        if self.methods:
            method = self.methods.get(request.method.lower())

            if method:
                response = method.handle(request)

                if self.cache_control:
                    patch_cache_control(response, **self.cache_control)

                return response

        permitted_methods = self.methods.keys() if self.methods else []
        return HttpResponseNotAllowed(permitted_methods=permitted_methods)

    def schema(self, request):
        from django.http import JsonResponse
        _schema = {
            k: v.schema() for k, v in self.methods.items()
        }

        return JsonResponse(_schema)
