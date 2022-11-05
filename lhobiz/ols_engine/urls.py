from django.urls import path

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
]

