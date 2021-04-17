from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from movie_app.apps.movie_credit.serializers import MovieCreditSerializer
from movie_app.apps.movie_credit.models import MovieCredit
from rest_framework import viewsets


class MovieCreditViewSet(viewsets.ModelViewSet):
    queryset = MovieCredit.objects.all()
    serializer_class = MovieCreditSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
