from perestroika.exceptions import BadRequest


class DbLayer:
    pass


class DjangoDbLayer(DbLayer):
    @staticmethod
    def get(bundle, method):
        _filter = bundle.get("filter")
        _exclude = bundle.get("exclude")
        _project = bundle.get("project")

        if _filter:
            bundle["queryset"] = bundle["queryset"].filter(_filter)

        if _exclude:
            bundle["queryset"] = bundle["queryset"].exclude(_exclude)

        if _project:
            bundle["queryset"] = bundle["queryset"].only(*_project)

        bundle["items"] = bundle["queryset"].values()
        bundle["total_count"] = bundle["queryset"].count()

    @staticmethod
    def post(bundle, method):
        _objects = bundle.get("items")

        if not _objects:
            raise BadRequest(message="Empty data for resource")

        _objects = [bundle["queryset"].model(**data) for data in _objects]

        bundle["queryset"].model.objects.bulk_create(
            _objects
        )
