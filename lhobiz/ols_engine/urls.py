from django.urls import path

from . import views
app_name = 'ols_engine'
urlpatterns = [
    # ex: /ols_engine/
    path('', views.index, name='index'),
    # ex: /ols_engine/1/
    path('<int:aerodrome_id>/', views.detail, name='detail'),
    # ex:/ols_engine/1/runways
    path('<int:aerodrome_id>/runways/', views.runways, name='runways'),
    # ex: /ols_engine/1/generate
    path('<int:aerodrome_id>/generate/', views.generate, name='generate'),
]

