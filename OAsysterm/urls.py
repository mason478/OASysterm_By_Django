from django.urls import path, include
from django.contrib.auth import logout
from . import views

app_name = 'OAsysterm'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>', views.ProcessDetailView.as_view(), name='detail'),
    path('sign-logout/',views.logout_site,name='logout'),
    path('sys/accounts/',views.AccountManageView.as_view(),name='account_manage'),
    path('sys/add/',views.AddAccountsView.as_view(),name='add_account'),
    path('sys/edit/<int:pk>',views.edit_account,name='edit_account'),
    path('sys/delete/<int:pk>',views.delete_account,name='delete_account'),
    path('startprocess/',views.start_process_view,name='start_process'),
    path('myprocess/',views.MyProcessesView.as_view(),name='my_processes'),
    path('myprocess/detail/<int:pk>',views.MyProcessDetailView.as_view(),name='my_process_detail'),
]
