from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from projects.models import Project

from children.models import Relationship
from users.models import Guardian


class RelationshipInline(admin.TabularInline):
    model = Relationship
    extra = 0
    fields = ("child", "type", "created_at")
    readonly_fields = ("created_at",)

    def has_change_permission(self, request, obj=None):
        return False


class GuardianForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["language"] = forms.ChoiceField(choices=settings.LANGUAGES)


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "last_name",
        "phone_number",
        "language",
        "created_at",
        "updated_at",
    )
    search_fields = ("first_name", "last_name", "user__email")
    form = GuardianForm
    inlines = (RelationshipInline,)


class ProjectInline(admin.TabularInline):
    model = Project.users.through
    extra = 0


class UserAdmin(DjangoUserAdmin):
    list_display = DjangoUserAdmin.list_display + ("uuid",)
    fieldsets = DjangoUserAdmin.fieldsets + (("UUID", {"fields": ("uuid",)}),)
    readonly_fields = ("uuid",)
    inlines = (ProjectInline,)


admin.site.register(get_user_model(), UserAdmin)
