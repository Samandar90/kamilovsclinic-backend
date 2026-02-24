from django.contrib import admin
from django.urls import path
from clinic.views import lead_create

urlpatterns = [
    path("admin/", admin.site.urls),

    # Заявки → Telegram + БД
    path("lead/", lead_create, name="lead_create"),
]
