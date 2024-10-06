from django.urls import path, include, re_path
from .views import *
from rest_framework import routers

fields = routers.DefaultRouter()
fields.register(r'my-fields', FieldsViewSet)


urlpatterns = [
    path('', include(fields.urls)),
    path('my-fields/<int:field_id>/<int:seed_id>/add-seed/', AddSeedView.as_view(), name='add-seed'),
    path('my-fields/<int:field_id>/analyse/', AnalyseMyField)
]
