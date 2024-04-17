from django.urls import path
from . import views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    #path('login/', views.login_view, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name="core/Login.html", authentication_form=AuthenticationForm), name="login"),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name="core/Login.html"), name='logout'),
    path('index/', views.index, name='index'),
    path('schedule/', views.schedule, name='schedule'),
    path('purchaseTicket/', views.purchaseTicket, name='purchaseTicket'),
    path('fares/', views.fares, name='fares'),
    path('vessels/', views.vessels, name='vessels'),
    path('emergency/', views.emergency, name='emergency'),
    path('emergencyctd/', views.emergencyctd, name='emergencyctd'),
    path('addschedule/', views.addschedule, name='addschedule'),
    path('viewtickets/', views.viewtickets, name='viewtickets'),
    path('viewemergency/', views.viewemergency, name='viewemergency'),
    path('loginRedirect/', views.loginRedirect, name='loginRedirect'),
    path('emerFreqRep/', views.emerFreqRep, name='emerFreqRep'),
    path('emerFreqRepCtd/', views.emerFreqRepCtd, name='emerFreqRepCtd'),
    path('revenueReportCtd/', views.revenueReportCtd, name='revenueReportCtd'),
    path('revenueReport/', views.revenueReport, name='revenueReport'),
    path('passengerTraffic/', views.passengerTraffic, name='passengerTraffic'),
    path('passengerTrafficCtd/', views.passengerTrafficCtd, name='passengerTrafficCtd'),
    path('addStaff/', views.addStaff, name='addStaff'),
]

