from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ChapterProgress, QuestionAttempt


@admin.register(ChapterProgress)
class ChapterProgressAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "chapter",
        "completion_percentage",
        "start_date",
        "completion_date",
        "last_accessed",
    )
    list_filter = ("completion_date", "start_date", "chapter__subject")
    search_fields = (
        "student__username",
        "student__email",
        "chapter__title",
        "chapter__subject__name",
    )
    raw_id_fields = ("student", "chapter")
    list_editable = ("completion_percentage",)
    date_hierarchy = "start_date"

    fieldsets = (
        (_("Student Information"), {"fields": ("student", "chapter")}),
        (_("Progress"), {"fields": ("completion_percentage", "completion_date")}),
        (
            _("Timestamps"),
            {"fields": ("start_date", "last_accessed"), "classes": ("collapse",)},
        ),
    )
    readonly_fields = ("start_date", "last_accessed")


@admin.register(QuestionAttempt)
class QuestionAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "question",
        "exam_attempt",
        "is_correct",
        "time_taken",
        "answered_at",
    )
    list_filter = ("is_correct", "exam_attempt", "answered_at")
    search_fields = (
        "student__username",
        "student__email",
        "question__text",
        "exam_attempt__exam__title",
    )
    raw_id_fields = ("student", "question", "exam_attempt", "selected_answer")
    readonly_fields = ("answered_at",)
    date_hierarchy = "answered_at"

    fieldsets = (
        (_("Attempt Information"), {"fields": ("student", "exam_attempt", "question")}),
        (_("Answer"), {"fields": ("selected_answer", "is_correct")}),
        (_("Performance"), {"fields": ("time_taken", "answered_at")}),
    )

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + (
                "student",
                "exam_attempt",
                "question",
                "is_correct",
            )
        return self.readonly_fields
