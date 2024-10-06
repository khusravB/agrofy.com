from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins, status
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from .models import *
from .serializers import *
import openai
from datetime import datetime
import math
import os
from dotenv import load_dotenv, dotenv_values
import requests
import json
from rest_framework.decorators import api_view


class FieldsViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldsSerializer


class AddSeedView(APIView):
    def post(self, request, seed_id, field_id, *args, **kwargs):
        user_id = request.user.id
        try:
            seed = Seed.objects.get(id=seed_id)
            field = Field.objects.get(id=field_id)
            field.seeds.add(seed)
            field.save()
            load_dotenv()

            client = openai.OpenAI()
            #key = "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"
            openai.api_key = os.getenv("OPENAI_API_KEY")
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": "Write a haiku about recursion in programming."
                    }
                ]
            )

            print(completion.choices[0].message)

            return Response({'status': 'success', 'message': 'Seed added to Your Field'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Field.DoesNotExist:
            return Response({'status': 'error', 'message': 'Your Field not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def AnalyseMyField(request, field_id):


    # Получаем объект Field по id
    field = Field.objects.filter(id=field_id).first()

    # Извлекаем долготу и широту
    longitude = float(field.longtitude)
    latitude = float(field.latitude)

    # Получаем текущую дату и преобразуем в формат A<year><day_of_year>
    current_date = datetime.now()
    start_date = "A2018049"
    end_date = "A2018049"

    # Вычисляем квадратный корень из площади для kmAboveBelow и kmLeftRight
    km_above_below = int(math.sqrt(int(field.area)))
    km_left_right = km_above_below

    # Параметры для запроса
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'startDate': start_date,
        'endDate': end_date,
        'kmAboveBelow': km_above_below,
        'kmLeftRight': km_left_right
    }

    # Отправка запроса (например, с requests)
    response = requests.get("https://modis.ornl.gov/rst/api/v1/MOD13Q1/subset", params=params)
    data = response.json()
    response1 = requests.get("https://modis.ornl.gov/rst/api/v1/MYD09A1/subset", params=params)
    data1 = response1.json()
    print(data, data1)

    load_dotenv()

    client = openai.OpenAI()
    openai.api_key = os.getenv("OPENAI_API_KEY")


    data_str = json.dumps(data)
    data_str1 = json.dumps(data1)
    seeds = field.seeds.all()

    # Преобразуем данные связанных объектов в список для последующего использования
    seeds_data = [{'id': seed.id, 'name': seed.name} for seed in seeds]
    content = "Пожалуйста дай оценку для поля по этим данным. Анализ в любом случае должен быть даже если данных мало. Знай что данные 100% верны. Ответ должен быть на русском и содержать либо 'да' либо 'нет'. Также дай рейтинг от 0 до 100. Также не указывай нигде дату. И не жалуйся на то что данных мало. Если да то дай рекомендации по максимизированию урожая если он хочет посадить:" + str(seeds_data) + "Ниже будет данные поля от MODIS." + data_str + data_str1
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": content},

        ]
    )

    print(completion.choices[0].message)

    return Response({'status': 'success', 'message': completion.choices[0].message}, status=status.HTTP_200_OK)
