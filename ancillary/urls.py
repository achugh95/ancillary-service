from django.urls import path
from ancillary.views import SendData


urlpatterns = [
    path("packet/send-data/", SendData.as_view(), name="send-data"),
]
