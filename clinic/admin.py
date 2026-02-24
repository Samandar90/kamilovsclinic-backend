from django.contrib import admin
from .models import Lead
# Если позже захочешь вернуть услуги:
# from .models import Service, ServiceCategory


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """
    Заявки с сайта: просмотр контактов, сообщения
    и откуда пришла форма.
    """
    list_display = (
        "created_at",
        "full_name",
        "phone",
        "service",
        "form_context",
    )
    list_filter = (
        "form_context",
        "service",
        "created_at",
    )
    search_fields = (
        "full_name",
        "phone",
        "email",
        "service",
        "message",
        "page_url",
    )
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("Контакты", {
            "fields": ("full_name", "phone", "email"),
        }),
        ("Содержание заявки", {
            "fields": ("service", "message"),
        }),
        ("Технические поля", {
            "fields": ("form_context", "page_url", "created_at"),
        }),
    )


# ===== Если позже захочешь вернуть управление услугами,
# можно раскомментировать эти блоки =====

# @admin.register(ServiceCategory)
# class ServiceCategoryAdmin(admin.ModelAdmin):
#     list_display = ("title", "slug", "order")
#     prepopulated_fields = {"slug": ("title",)}
#     ordering = ("order", "title")
#
#
# @admin.register(Service)
# class ServiceAdmin(admin.ModelAdmin):
#     list_display = (
#         "title",
#         "category",
#         "price_from",
#         "duration",
#         "is_popular",
#         "is_active",
#     )
#     list_filter = ("category", "is_popular", "is_active")
#     search_fields = ("title", "short_intro", "description", "tags")
#     prepopulated_fields = {"slug": ("title",)}
#     ordering = ("order", "title")
#     readonly_fields = ("created_at", "updated_at")
#
#     fieldsets = (
#         ("Основное", {
#             "fields": ("title", "slug", "category", "short_intro", "description"),
#         }),
#         ("Параметры приёма", {
#             "fields": ("duration", "price_from", "tags"),
#         }),
#         ("Показ на сайте", {
#             "fields": ("is_popular", "is_active", "order"),
#         }),
#         ("Служебное", {
#             "fields": ("created_at", "updated_at"),
#         }),
#     )
