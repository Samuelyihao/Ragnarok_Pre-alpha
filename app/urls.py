from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index_view),
    path('summarization',views.summary_1),
    # path('wordcloud', views.wc_1),
]