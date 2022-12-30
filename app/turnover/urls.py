from django.urls import path
from .views import (
    TurnoverApiView
)

urlpatterns = [
    path('performance', TurnoverApiView.as_view()),
]
