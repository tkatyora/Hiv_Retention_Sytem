from django.urls import path
from . import views

urlpatterns = [
    path('',views.main,name='sign_in'),
    path('dashboard',views.Dashboard , name ='dashboard'),  
    path('signout',views.Signout , name ='logout'),
    path('analysis',views.Analysis , name ='analysis'),
    path('ViewComment',views.viewComments , name ='View_Comment'),
    path('Comments',views.comments , name ='Comments'),
    path('model-evaluation',views.EvaluationMetric , name ='model'),
    path('predictions',views.Predictions , name ='predictions'),

    
    
  
]
