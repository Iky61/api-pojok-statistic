from django.contrib import admin
from django.urls import path, include
from turnover import urls as turnover_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(turnover_urls))
]
