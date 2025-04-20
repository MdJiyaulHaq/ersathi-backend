from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, Notification


# Define custom UserAdmin
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = BaseUserAdmin.list_filter + (
        "is_staff",
        "is_active",
        "date_joined",
    )
    search_fields = ("email", "username", "first_name", "last_name")
    list_editable = ("is_staff", "is_active")
    list_per_page = 10
    readonly_fields = ["is_active", "date_joined", "last_login"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        """Ensure email is required before saving the model."""
        if not obj.email:
            raise ValueError("Email is required.")
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)


# Define StudentProfileAdmin
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "get_user_email",
        "phone",
        "registration_date",
        "last_active",
    )
    list_filter = ("discipline", "registration_date", "last_active")
    search_fields = (
        "user__email",
        "user__username",
        "user__first_name",
        "user__last_name",
        "phone",
    )
    list_editable = ("phone",)
    list_per_page = 10
    raw_id_fields = ("user",)  # Useful for selecting the user efficiently

    @admin.display(description="User Email")
    def get_user_email(self, obj):
        return obj.user.email


# Define NotificationAdmin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message_snippet", "is_read", "created_at")
    list_filter = ("is_read", "created_at", "user")
    search_fields = ("user__email", "user__username", "message")
    list_editable = ("is_read",)
    list_per_page = 10
    readonly_fields = ("created_at", "read_at")
    raw_id_fields = ("user",)  # Useful for selecting the user

    @admin.display(description="Message Snippet")
    def message_snippet(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message


# Register the User model with the custom UserAdmin

# StudentProfile and Notification are registered using the @admin.register decorator above
