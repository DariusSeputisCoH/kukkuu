from django.contrib import admin

from .models import Child, Relationship


class RelationshipInline(admin.TabularInline):
    model = Relationship
    extra = 0
    fields = ("user", "type", "created_at")
    readonly_fields = ("created_at",)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birthdate", "created_at", "updated_at")
    fields = ("first_name", "last_name", "birthdate")
    inlines = (RelationshipInline,)
