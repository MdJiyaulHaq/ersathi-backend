# ersathi-backend/assessments/admin.py

from django.contrib import admin

# Make sure AnswerOption is imported if needed elsewhere, but we won't register it separately
from .models import Exam, ExamAttempt, AnswerOption
from django.utils.translation import gettext_lazy as _


# --- Admin Configuration for Exam Model ---
# Keep the ExamAdmin class as previously defined (with exam_type etc.)
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    """Admin interface for Exam model"""

    # (Your existing ExamAdmin code from the previous response goes here)
    list_display = (
        "get_exam_title",
        "subject",
        "duration",
        "passing_score",
        "exam_type",
        "created_by",
        "start_date",
        "end_date",
    )
    list_filter = ("exam_type", "subject", "start_date", "end_date", "passing_score")
    search_fields = (
        "title",
        "description",
        "subject__name",
        "subject__code",
        "exam_type",
    )
    list_editable = ("duration", "passing_score")
    list_per_page = 15
    readonly_fields = ("end_date",)

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": ("title", "exam_type", "subject", "description"),
                "description": _("Enter the fundamental information about the exam."),
            },
        ),
        (
            _("Exam Settings"),
            {
                "fields": ("duration", "passing_score"),
                "description": _(
                    "Configure exam duration (minutes) and passing score (%)."
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Schedule"),
            {
                "fields": ("start_date", "end_date"),
                "description": _("Set the optional examination period."),
                "classes": ("collapse",),
            },
        ),
    )

    autocomplete_fields = ["subject"]
    ordering = ("-start_date", "title")

    @admin.display(description=_("Exam Title & Type"), ordering="title")
    def get_exam_title(self, obj):
        """Display exam title combined with its type for clarity."""
        if hasattr(obj, "get_exam_type_display"):
            return f"{obj.title} ({obj.get_exam_type_display()})"
        return obj.title


# --- Admin Configuration for ExamAttempt Model ---
# Keep the ExamAttemptAdmin class as previously defined
@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    """Admin interface for ExamAttempt model"""

    # (Your existing ExamAttemptAdmin code from the previous response goes here)
    list_display = (
        "student",
        "exam",
        "score",
        "start_time",
        "end_time",
        "get_duration",
        "status",
    )
    list_filter = ("exam", "student", "start_time", "status")
    search_fields = ("student__username", "student__email", "exam__title")
    readonly_fields = (
        "student",
        "exam",
        "start_time",
        "end_time",
        "score",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "start_time"
    list_per_page = 20
    autocomplete_fields = ["student", "exam"]
    ordering = ("-start_time",)

    def has_add_permission(self, request):
        return False

    @admin.display(description=_("Duration"))
    def get_duration(self, obj):
        """Calculate and display the duration of the exam attempt."""
        if obj.end_time and obj.start_time:
            duration = obj.end_time - obj.start_time
            minutes = duration.total_seconds() / 60
            return f"{minutes:.1f} minutes"
        return _("N/A")
