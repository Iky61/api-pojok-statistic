from django.urls import path
from .views import (
    TurnoverApiView
)

urlpatterns = [
    path('turnover', TurnoverApiView.as_view()),
]
