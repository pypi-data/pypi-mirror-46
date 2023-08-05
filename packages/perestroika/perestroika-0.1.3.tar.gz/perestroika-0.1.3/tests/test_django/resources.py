from django.contrib.auth.models import User
from validate_it import schema

from perestroika.methods import Get, Post, Put, Patch, Delete
from perestroika.resource import DjangoResource


class EmptyResource(DjangoResource):
    pass


@schema(strip_unknown=True)
class OutUserValidator:
    username: str


class FullResource(DjangoResource):
    cache_control = dict(max_age=0, no_cache=True, no_store=True, must_revalidate=True)

    get = Get(
        queryset=User.objects.all(),
        output_validator=OutUserValidator
    )

    post = Post(
        queryset=User.objects.all()
    )

    put = Put(
        queryset=User.objects.all()
    )

    patch = Patch(
        queryset=User.objects.all()
    )

    delete = Delete(
        queryset=User.objects.all()
    )


__all__ = [
    "EmptyResource",
    "FullResource",
]
