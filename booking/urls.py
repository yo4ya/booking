from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'booking'

urlpatterns = [
    path('', views.top, name='top'),
    path('calendar/', views.Calendar.as_view(), name='calendar'),
    path('login/', LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('list/', views.list, name='list'),
    path('/calendar/<int:year>/<int:month>/<int:day>/', views.Calendar.as_view(), name='calendar'),
    path('/booking/<int:year>/<int:month>/<int:day>/<int:hour>/', views.Booking.as_view(), name='booking'),
    #path('user_data_input/', views.UserDataInput.as_view(), name='user_data_input'),
    path('user_data_confirm/<int:year>/<int:month>/<int:day>/<int:hour>/', views.UserDataConfirm.as_view(), name='user_data_confirm'),
    #path('user_data_confirm/<int:year>', views.UserDataConfirm.as_view(), name='user_data_confirm'),
    path('user_data_create/<int:year>/<int:month>/<int:day>/<int:hour>/', views.UserDataCreate.as_view(), name='user_data_create'),
]