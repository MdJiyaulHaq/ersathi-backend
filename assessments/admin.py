from django.contrib import admin
from .models import Exam, ExamAttempt, AnswerOption


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        "get_exam_title",
        "exam_type",
        "subject",
        "duration",
        "passing_score",
        "start_date",
        "end_date",
    )
    list_filter = ("exam_type", "subject", "passing_score", "start_date", "end_date")
    search_fields = (
        "title",
        "description",
        "subject__name",
        "subject__code",
        "exam_type",
    )
    list_editable = ("passing_score", "duration")
    list_per_page = 10
    readonly_fields = ()

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("title", "description", "subject", "exam_type"),
                "description": "Enter the fundamental information about the exam",
            },
        ),
        (
            "Exam Settings",
            {
                "fields": ("duration", "passing_score"),
                "description": "Configure exam duration and passing criteria",
                "classes": ("collapse",),
            },
        ),
        (
            "Schedule",
            {
                "fields": ("start_date", "end_date"),
                "description": "Set the examination period",
                "classes": ("collapse",),
            },
        ),
    )

    autocomplete_fields = ["subject"]
    ordering = ("-start_date", "title")

    def get_exam_title(self, obj):
        """Display exam title with type indicator"""
        return f"{obj.title} ({obj.get_exam_type_display()})"

    get_exam_title.short_description = "Exam Title"
    get_exam_title.admin_order_field = "title"


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "exam",
        "score",
        "start_time",
        "end_time",
        "get_duration",
    )
    list_filter = ("exam", "start_time", "score")
    search_fields = ("student__email", "student__username", "exam__title")
    readonly_fields = ("start_time", "end_time")
    list_per_page = 10

    autocomplete_fields = ["student", "exam"]
    ordering = ("-start_time",)

    def get_duration(self, obj):
        """Calculate the duration of the exam attempt"""
        duration = obj.end_time - obj.start_time
        minutes = duration.total_seconds() / 60
        return f"{minutes:.1f} minutes"

    get_duration.short_description = "Duration"


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct", "get_question_type")
    list_filter = ("is_correct", "question__question_type")
    search_fields = ("text", "question__text")
    list_editable = ("is_correct",)
    list_per_page = 10

    autocomplete_fields = ["question"]
    ordering = ("question", "-is_correct")

    def get_question_type(self, obj):
        """Get the question type for display"""
        return obj.question.get_question_type_display()

    get_question_type.short_description = "Question Type"

    def has_module_permission(self, request):
        """Only show this model in admin if user is staff"""
        return request.user.is_staff
