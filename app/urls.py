from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from app import views

urlpatterns = [
    path('banks', views.bank_list),
    path('banks_details/<branch_name>', views.banks_actions),
]

urlpatterns = format_suffix_patterns(urlpatterns)