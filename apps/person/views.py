from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from movie_app.apps.person.serializers import PersonSerializer
from movie_app.apps.person.models import Person
from django.core.paginator import Paginator
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_credits_list = self.get_object().get_movie_credits()
        paginator = Paginator(movie_credits_list, 40)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['filmography'] = page_obj.object_list
        context['page_obj'] = page_obj
        context['is_paginated'] = True
        return context
