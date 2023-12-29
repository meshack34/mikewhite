from django.contrib import admin
from django.urls import path , include

from . import views

urlpatterns = [
    # path('',views.Index, name='inde'),
    path('oauth/success', views.oauth_success, name='test_oauth_success'),
    path('stk-push/success', views.stk_push_success, name='test_stk_push_success'),
    # path('loan/',views.loan,name='loan'),
    path('bund/',views.bund,name='bund'),
    path('Airtime_bund/',views.Airtime_bund,name='Airtime_bund'),
    
    # path('score/',views.score,name='score'),
    path('download_csv/',views.download_csv,name='download_csv'),
    path('dialers/', views.dialer_list, name='dialer_list'),
    path('bundwer/', views.bundwer, name='di'),
    path('score/', views.scoe, name='score'),
    path('cbc/', views.cbc, name='cbc'),
]