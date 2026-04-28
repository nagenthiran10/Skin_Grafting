from django.urls import path
from bioadhesion import views


urlpatterns = [

    path('bio_home/',views.bio_home),

    path('bio_register/',views.bio_register),
    path('bio_login/',views.bio_login),
    path('bio_logout/',views.bio_logout),


    path('exforeports/',views.bio_req_result),

    path('getkey_bio/<str:project_id>/',views.getkey_bio),
    path('decrypt_data_bio/<str:project_id>/',views.decrypt_data_bio),


    path('bio_scan/',views.bio_scan),
    path('bio_calculation/<str:project_id>/',views.bio_calculation),
    path('bio_file/',views.bio_file)


]