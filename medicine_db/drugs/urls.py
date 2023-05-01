from django.urls import path
from drugs import views

urlpatterns = [
    path('drugs_to_csv/', views.drugs_to_csv),
    path('classifier/', views.classifier, name='classifier'),
]
