from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add_note),
    path('list_note', views.list_note),
    path('test_csv', views.test_csv),
    path('make_csv_view', views.make_csv_view)
]