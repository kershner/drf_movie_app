from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from movie_app.apps.person.serializers import PersonSerializer
from movie_app.apps.person.models import Person
from rest_framework import viewsets


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
