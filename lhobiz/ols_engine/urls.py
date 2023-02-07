from django.urls import path, include
from ols_engine.views import Register
from django.views.generic import TemplateView
from django.contrib import admin

from . import views
app_name = 'ols_engine'
urlpatterns = [
    # ex: /ols_engine/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /ols_engine/1/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex:/ols_engine/1/runways
    path('<int:pk>/runways/', views.runways, name='runways'),
    # ex: /ols_engine/1/generate
    path('<int:aerodrome_id>/generate/', views.generate, name='generate'),

    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),

    path( 'register/', Register.as_view(), name="register"),
    path('register/success', TemplateView.as_view(template_name="registration/success.html"), name="register-success"),

    path('', include('django.contrib.auth.urls')),


]

