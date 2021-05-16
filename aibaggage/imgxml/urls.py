from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    #for output image
    path("",views.home,name="home"),
    path("files",views.files,name="files"),
    #for report
    # path("",views.dates,name="csv"),
    # path("report",views.report,name="files"),

]