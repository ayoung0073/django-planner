"""webproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import study_diary.views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
# for restframework
from rest_framework import routers

# url을 자동으로 맵핑해줌
# router = routers.DefaultRouter()
# router.register('dailys/',study_diary.views.diary_rest)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',study_diary.views.index, name='index'),
    path('login/',study_diary.views.login, name='login'),
    path('join/',study_diary.views.join, name='join'),
    path('daily/',study_diary.views.daily, name='daily'),
    path('daily/<str:daily_date>/',study_diary.views.daily_one, name='daily_one'),
    path('monthly/',study_diary.views.monthly, name='monthly'),
    path('monthly/add',study_diary.views.monthly_add, name='monthly_add'),
    path('diary/',study_diary.views.diary, name='diary'),
    path('diary/write/',study_diary.views.diary_write, name='diary_write'),
    path('diary/write/',study_diary.views.diary_one_delete, name='diary_one_delete'),
    path('diary/<int:diary_id>/',study_diary.views.diary_one, name='diary_one'),
    path('<int:diary_id>/update/',study_diary.views.diary_one_update, name='diary_one_update'),
    path('<int:diary_id>/delete/',study_diary.views.diary_one_delete, name='diary_one_delete'),
    path('chart/',study_diary.views.chart, name='chart'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('logout/',study_diary.views.logout, name='logout'),

    path('diarys/',study_diary.views.diary_rest)

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
