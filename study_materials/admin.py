# ersathi-backend/study_materials/admin.py

from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Question, StudyMaterial
# Import AnswerOption from the assessments app to use in the inline
from assessments.models import AnswerOption

# --- Custom FormSet for Answer Options Inline ---
class AnswerOptionInlineFormSet(forms.BaseInlineFormSet):
    """
    Custom formset to validate that exactly one answer option is marked correct.
    """
    def clean(self):
        super().clean()

        correct_answers_count = 0
        has_at_least_one_form = False

        for form in self.forms:
            # Skip empty forms and forms marked for deletion
            if not form.is_valid() or form.cleaned_data.get('DELETE', False):
                continue

            has_at_least_one_form = True
            if form.cleaned_data.get('is_correct'):
                correct_answers_count += 1

        # Only run validation if there are actual forms being submitted
        # And check the count only after checking all valid forms
        if has_at_least_one_form and correct_answers_count != 1:
            raise ValidationError(
                _("You must mark exactly one answer option as correct.")
            )

# --- Inline Admin for Answer Options ---
class AnswerOptionInline(admin.TabularInline):
    """
    Inline admin configuration for managing AnswerOptions directly within QuestionAdmin.
    Enforces exactly 4 options and uses the custom formset for validation.
    """
    model = AnswerOption
    formset = AnswerOptionInlineFormSet # Use the custom formset
    extra = 0 # Don't show extra blank forms by default
    min_num = 4 # Enforce minimum 4 options
    max_num = 4 # Enforce maximum 4 options
    fields = ('text', 'is_correct') # Fields to display in the inline form


# --- Admin Configuration for Question Model ---
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Question model.
    Includes inline management for AnswerOptions.
    """
    list_display = (
        "__str__", # Use the model's __str__ for display
        "exam",
        "marks",
        "is_active",
        "created_at",
    )
    list_filter = ("exam", "marks", "is_active", "created_at")
    search_fields = ("text", "explanation", "exam__title", "exam__subject__name")
    list_editable = ("is_active",)
    list_per_page = 20

    fieldsets = (
        (None, {
            "fields": ("exam", "text", "marks", "is_active")
        }),
        (_("Explanation (Optional)"), {
            "fields": ("explanation",),
            "classes": ("collapse",), # Make collapsible
        }),
        (_("Metadata"), {
            "fields": ("created_by", "created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
    readonly_fields = ("created_at", "updated_at", "created_by") # Make metadata read-only
    autocomplete_fields = ["exam"]

    # Include the AnswerOption inline interface
    inlines = [AnswerOptionInline]

    # Set created_by automatically on save
    def save_model(self, request, obj, form, change):
        if not obj.pk: # Only set created_by on initial creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# --- Admin Configuration for StudyMaterial Model (remains mostly unchanged) ---
@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "material_type", "subject", "chapter", "created_at")
    search_fields = ("title", "subject__name", "chapter__title")
    list_filter = ("material_type", "subject", "created_at")
    autocomplete_fields = ["subject", "chapter"]
    list_per_page = 20