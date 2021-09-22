from django.urls import path
from . import views


urlpatterns = [
					path("", views.index, name="index"),
					path("file_result/", views.send_image, name="send_img"),
			]