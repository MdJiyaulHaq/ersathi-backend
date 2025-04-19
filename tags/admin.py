from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Tag, TaggedItem


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["label", "created_at"]
    search_fields = ["label"]
    date_hierarchy = "created_at"
    filter_horizontal = ["questions", "study_materials"]
    readonly_fields = ["created_at"]

    fieldsets = (
        (None, {"fields": ("label",)}),
        (
            _("Associated Content"),
            {"fields": ("questions", "study_materials"), "classes": ("collapse",)},
        ),
        (_("Timestamps"), {"fields": ("created_at",), "classes": ("collapse",)}),
    )


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ["tag", "content_type", "object_id"]
    list_filter = ["content_type", "tag"]
    search_fields = ["tag__label", "object_id"]
    autocomplete_fields = ["tag"]

    fieldsets = (
        (None, {"fields": ("tag",)}),
        (_("Content"), {"fields": ("content_type", "object_id")}),
    )
