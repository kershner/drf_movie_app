from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from movie_app.apps.person.serializers import PersonSerializer
from movie_app.apps.person.models import Person
from rest_framework import viewsets
from django.views import generic


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class PersonListView(generic.ListView):
    model = Person
    template_name = 'person/person_list.html'
    paginate_by = 80


class PersonDetailView(generic.DetailView):
    model = Person
    template_name = 'person/person_detail.html'
