from django.urls import path
from . import views

urlpatterns = [
    #path("", views.index, name="index")
    path("", views.ReqestByPinView.as_view(), name="pinreq"),
    path("submitted",views.submitted, name ="submitted"),
    path("dist",views.ReqestByDistView.as_view(), name ="distreq"),
    #path("dist",views.distslots, name ="distreq"),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts')
]
