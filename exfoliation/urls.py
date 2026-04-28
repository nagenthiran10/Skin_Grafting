from django.urls import path
from exfoliation import views

urlpatterns = [

    path('exfo_home/', views.exfo_home,name="exfo_home"),


    path('exfo_register/', views.exfo_register),
    path('exfo_login/', views.exfo_login),
    path('exfo_logout/', views.exfo_logout, name="exfo_logout"),


    path('exfo_requirements/', views.exfo_req_result, name="exfo_requirements"),


    path('getkey_exfo/<str:project_id>/',views.getkey_exfo),
    path('decrypt_data_exfo/<str:project_id>/',views.decrypt_data_exfo),


    path('exfo_scan/',views.exfo_scan, name="exfo_scan"),
    path('exfo_calculation/<str:project_id>/',views.exfo_calculation, name="exfo_calculation"),
    path('exfo_file/',views.exfo_file,name="exfo_file")


]