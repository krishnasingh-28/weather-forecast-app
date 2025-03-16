from django.urls import path
from weather import views

urlpatterns = [
    path("predict/", views.predict),
    path("ping/", views.ping_view),
]