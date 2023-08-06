from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


class Serializer:
    pass


class DjangoSerializer(Serializer):
    @staticmethod
    def get_encoder():
        return DjangoJSONEncoder

    def serialize(self, request, bundle):
        _data = {
            "limit": bundle.get("limit", 0),
            "skip": bundle.get("skip", 0),
            "total_count": bundle.get("total_count", 0),
        }

        if bundle.get("project"):
            _new_items = []

            for item in bundle["items"]:
                _new_item = {}

                for key in bundle["project"]:
                    _new_item[key] = item[key]

                _new_items.append(_new_item)

            bundle["items"] = _new_items

        _items = bundle.get("items", [])

        if len(_items) is 1:
            _data["item"] = _items[0]
        else:
            _data["items"] = _items

        for item in ['filter', 'order', 'project', 'error_code', 'error_message', 'status_code']:
            if bundle.get(item):
                _data[item] = bundle[item]

        return JsonResponse(_data, status=bundle['status_code'], encoder=self.get_encoder())
