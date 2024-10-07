from django.urls import path, include, re_path
from .views import *
from rest_framework import routers

fields = routers.DefaultRouter()
fields.register(r'my-fields', FieldsViewSet)


seeds = routers.DefaultRouter()
seeds.register(r'seeds', SeedViewSet)


questions = routers.DefaultRouter()
questions.register(r'questions', QuestionViewSet)


answers = routers.DefaultRouter()
answers.register(r'answers', AnswerViewSet)


urlpatterns = [
    path('', include(fields.urls)),
    path('', include(seeds.urls)),
    path('', include(questions.urls)),
    path('', include(answers.urls)),
    path('my-fields/<int:field_id>/<int:seed_id>/add-seed/', AddSeedView.as_view(), name='add-seed'),
    path('question/<int:question_id>/<int:answer_id>/add-answer/', AddAnswerView.as_view(), name='add-answers'),

    path('question/<int:question_id>/answers/', question_detail_api),
    path('my-fields/<int:field_id>/analyse/', AnalyseMyField)
]
