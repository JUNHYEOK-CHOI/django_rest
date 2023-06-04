from django.urls import path, include
from addresses import views
from django.urls import path
from django.contrib import admin
from addresses import views as addresses_views


urlpatterns = [
    path('app_login/', views.app_login),
    path('sign_up/', views.sign_up),
    path('friend_list/', views.show_friend_list),
    path('user_list/', views.user_list),
    path('friend_list_add/', views.friend_add),
    path('history_list_add/', views.history_list),
    path('history_list_add2/', views.history_list2),
    path('history_list_add3/', views.history_list3),
    path('history_list_RT/', views.history_RT),
    path('period_check/', views.period_check),
    path('period_check2/', views.period_check2),
    path('friend_list_delete/', views.friend_delete),
    path('get_profile/', views.get_profile),
    path('', addresses_views.index, name="index"),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]