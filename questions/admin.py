from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Question, AnswerOption


class AnswerOptionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        valid_forms = [
            form for form in self.forms
            if not form.cleaned_data.get("DELETE", False) and form.cleaned_data.get("text")
        ]
        if len(valid_forms) != 4:
            raise ValidationError("Exactly 4 answer options are required.")

        correct_answers = [form for form in valid_forms if form.cleaned_data.get("is_correct")]
        if len(correct_answers) != 1:
            raise ValidationError("Exactly one answer option must be marked as correct.")


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 4  # Show 4 empty answer option forms by default
    formset = AnswerOptionInlineFormSet


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "subject", "chapter", "marks", "is_active", "created_at"]
    list_filter = ["subject", "marks", "is_active", "created_at"]
    search_fields = ["text", "explanation"]
    inlines = [AnswerOptionInline]
    readonly_fields = ["created_at", "updated_at"]
