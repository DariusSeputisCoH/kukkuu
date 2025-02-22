from django.contrib import admin, messages
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import BaseInlineFormSet, ModelMultipleChoiceField
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from subscriptions.models import FreeSpotNotificationSubscription

from .models import Enrolment, Event, EventGroup, Occurrence, TicketSystemPassword


class BaseBooleanListFilter(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        return ("1", _("Yes")), ("0", _("No"))


class IsPublishedFilter(BaseBooleanListFilter):
    title = _("published")
    parameter_name = "is_published"
    lookup_kwarg = "published_at__isnull"

    def queryset(self, request, queryset):
        if self.value() == "0":
            return queryset.filter(**{self.lookup_kwarg: True})
        if self.value() == "1":
            return queryset.filter(**{self.lookup_kwarg: False})


class OccurrenceIsPublishedFilter(IsPublishedFilter):
    lookup_kwarg = "event__published_at__isnull"


class OccurrenceIsUpcomingFilter(BaseBooleanListFilter):
    title = _("upcoming")
    parameter_name = "is_upcoming"

    def queryset(self, request, queryset):
        if self.value() == "0":
            return queryset.in_past()
        if self.value() == "1":
            return queryset.upcoming()


class OccurrencesInline(admin.StackedInline):
    model = Occurrence
    extra = 0


@admin.register(Event)
class EventAdmin(TranslatableAdmin):
    list_display = (
        "id",
        "name",
        "capacity_per_occurrence",
        "participants_per_invite",
        "published_at",
        "project",
        "created_at",
        "updated_at",
        "event_group",
        "ready_for_event_group_publishing",
        "ticket_system",
    )
    list_display_links = ("id", "name")
    fields = (
        "project",
        "name",
        "short_description",
        "description",
        "capacity_per_occurrence",
        "participants_per_invite",
        "duration",
        "image",
        "image_alt_text",
        "published_at",
        "event_group",
        "ready_for_event_group_publishing",
        "ticket_system",
    )
    inlines = [
        OccurrencesInline,
    ]
    actions = ["publish"]
    readonly_fields = ("published_at",)
    list_filter = (
        "project",
        ("event_group", admin.RelatedOnlyFieldListFilter),
        IsPublishedFilter,
    )

    def publish(self, request, queryset):
        success_count = 0
        for obj in queryset:
            try:
                obj.publish()
                success_count += 1
            except ValidationError as e:
                self.message_user(request, e.message, level=messages.ERROR)
        if success_count:
            self.message_user(request, _("%s successfully published.") % success_count)

    publish.short_description = _("Publish selected events")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related(
                "translations",
                "event_group__translations",
                "project__translations",
                "event_group__project",
            )
        )


class EnrolmentsInlineFormSet(BaseInlineFormSet):
    def delete_existing(self, obj, commit=True):
        if commit:
            obj.delete_and_send_notification()


class EnrolmentsInline(admin.TabularInline):
    model = Enrolment
    extra = 0
    fields = (
        "child",
        "attended",
        "created_at",
        "updated_at",
        "reminder_sent_at",
        "feedback_notification_sent_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    formset = EnrolmentsInlineFormSet
    raw_id_fields = ("child",)


class FreeSpotNotificationSubscriptionInline(admin.TabularInline):
    model = FreeSpotNotificationSubscription
    extra = 0
    fields = ("child", "created_at")
    readonly_fields = ("created_at",)
    raw_id_fields = ("child",)


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    list_display = (
        "time",
        "event",
        "venue",
        "get_enrolments",
        "get_free_spot_notification_subscriptions",
        "occurrence_language",
        "ticket_system_url",
        "created_at",
        "updated_at",
    )
    fields = (
        "time",
        "event",
        "venue",
        "occurrence_language",
        "capacity_override",
        "ticket_system_url",
    )
    inlines = [EnrolmentsInline, FreeSpotNotificationSubscriptionInline]
    list_filter = (
        "event__project",
        ("event", admin.RelatedOnlyFieldListFilter),
        ("venue", admin.RelatedOnlyFieldListFilter),
        OccurrenceIsPublishedFilter,
        OccurrenceIsUpcomingFilter,
    )
    ordering = ("-time",)

    def get_enrolments(self, obj):
        return f"{obj.get_enrolment_count()} / {obj.get_capacity()}"

    def get_free_spot_notification_subscriptions(self, obj):
        return obj.free_spot_notification_subscriptions.count()

    get_enrolments.short_description = _("enrolments")
    get_free_spot_notification_subscriptions.short_description = _("subscriptions")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related(
                "event__translations",
                "venue__translations",
                "enrolments",
                "free_spot_notification_subscriptions",
            )
        )


class EventGroupForm(TranslatableModelForm):
    events = ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=FilteredSelectMultiple(verbose_name="events", is_stacked=False),
        required=False,
    )

    class Meta:
        model = EventGroup
        fields = (
            "project",
            "name",
            "short_description",
            "description",
            "image",
            "image_alt_text",
            "published_at",
            "events",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["events"].initial = self.instance.events.all()


@admin.register(EventGroup)
class EventGroupAdmin(TranslatableAdmin):
    list_display = (
        "name",
        "short_description",
        "project",
        "get_event_count",
        "published_at",
        "created_at",
        "updated_at",
    )

    readonly_fields = ("published_at",)
    form = EventGroupForm
    actions = ("publish",)
    list_filter = ("project", IsPublishedFilter)

    def get_event_count(self, obj):
        return obj.events.count()

    get_event_count.short_description = _("event count")

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        obj.save()
        obj.events.set(form.cleaned_data["events"])

    def publish(self, request, queryset):
        success_count = 0
        for obj in queryset:
            try:
                obj.publish()
                success_count += 1
            except ValidationError as e:
                self.message_user(request, e.message, level=messages.ERROR)
        if success_count:
            self.message_user(request, _("%s successfully published.") % success_count)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("translations", "project__translations", "events")
        )


class PasswordAssignedListFilter(BaseBooleanListFilter):
    title = _("assigned")
    parameter_name = "assigned"

    def queryset(self, request, queryset):
        if self.value() == "0":
            return queryset.filter(child=None)
        if self.value() == "1":
            return queryset.exclude(child=None)


@admin.register(TicketSystemPassword)
class TicketSystemChildPasswordAdmin(admin.ModelAdmin):
    fields = (
        "value",
        "event",
        "child",
        "assigned_at",
    )
    list_display = (
        "value",
        "event",
        "child",
        "get_guardian",
        "created_at",
        "assigned_at",
    )
    list_filter = ("event", PasswordAssignedListFilter)
    search_fields = (
        "child__first_name",
        "child__last_name",
        "child__guardians__first_name",
        "child__guardians__last_name",
        "child__guardians__email",
    )

    def get_guardian(self, obj):
        try:
            return obj.child.guardians.all()[0]
        except (AttributeError, IndexError):
            return None

    get_guardian.short_description = _("guardian")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("child")
            .prefetch_related("child__guardians")
        )
