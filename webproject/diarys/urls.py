from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
import study_diary.views

urlpatterns = [
    path('diary/',study_diary.views.diary_rest)
]
