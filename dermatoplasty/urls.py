from django.urls import path
from dermatoplasty import views

urlpatterns = [


    path('dermato_home/',views.dermato_home),

    path('dermato_register/', views.dermato_register),
    path('dermato_login/', views.dermato_login),


    path('bioreports/', views.dermato_req_result),

    path('getkey_dermato/<str:project_id>/',views.getkey_dermato),
    path('decrypt_data_dermato/<str:project_id>/',views.decrypt_data_dermato),

    path('dermatoscan/', views.dermatoscan),
    path('dermato_calculation/<str:project_id>/', views.dermato_calculation),
    path('dermatofile/', views.dermatofile),
    path('dermato_logout/', views.dermato_logout),


]