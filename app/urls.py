from django.urls import path
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz1/', views.quiz1, name='quiz1'),
    path('quiz2/', views.quiz2, name='quiz2'),
    path('quiz3/', views.quiz3, name='quiz3'),
    path('quiz4/', views.quiz4, name='quiz4'),
    path('quiz5/', views.quiz5, name='quiz5'),
    path('quiz6/', views.quiz6, name='quiz6'),
    path('b_ecoli/', views.b_ecoli, name='b_ecoli'),
    # path('b_lplant/', views.b_lplant, name='b_lplant'),
    path('congrats/', views.congrats, name='congrats'),
    path('update_score/', views.update_score, name='update_score'),
    
    
    path('accounts/login/', views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('result/', views.result, name='result'),
]

handler404 = views.custom_404_page




