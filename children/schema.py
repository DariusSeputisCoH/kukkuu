import graphene
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django.utils.timezone import localtime, now
from django_ilmoitin.utils import send_notification
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id
from projects.models import Project

from children.notifications import NotificationType
from common.utils import update_object
from kukkuu.exceptions import (
    ApiUsageError,
    DataValidationError,
    MaxNumberOfChildrenPerGuardianError,
    ObjectDoesNotExistError,
)
from users.models import Guardian
from users.schema import GuardianNode, LanguageEnum, validate_guardian_data

from .models import Child, postal_code_validator, Relationship

User = get_user_model()


class ChildNode(DjangoObjectType):
    available_events = relay.ConnectionField("events.schema.EventConnection")
    past_events = relay.ConnectionField("events.schema.EventConnection")

    class Meta:
        model = Child
        interfaces = (relay.Node,)
        filter_fields = ("project_id",)

    @classmethod
    @login_required
    def get_queryset(cls, queryset, info):
        return queryset.user_can_view(info.context.user).order_by("last_name")

    @classmethod
    @login_required
    def get_node(cls, info, id):
        try:
            return cls._meta.model.objects.user_can_view(info.context.user).get(id=id)
        except cls._meta.model.DoesNotExist:
            return None

    def resolve_past_events(self, info, **kwargs):
        return (
            self.project.events.user_can_view(info.context.user)
            .exclude(occurrences__time__gte=timezone.now())
            .distinct()
        )

    def resolve_available_events(self, info, **kwargs):
        return (
            self.project.events.user_can_view(info.context.user)
            .filter(occurrences__time__gte=timezone.now())
            .distinct()
            .exclude(occurrences__in=self.occurrences.all())
        )

    def resolve_occurrences(self, info, **kwargs):
        # Use distinct to avoid duplicated rows when querying nested occurrences
        return self.occurrences.distinct()


class RelationshipTypeEnum(graphene.Enum):
    PARENT = "parent"
    OTHER_GUARDIAN = "other_guardian"
    OTHER_RELATION = "other_relation"
    ADVOCATE = "advocate"


class RelationshipNode(DjangoObjectType):
    class Meta:
        model = Relationship
        interfaces = (relay.Node,)
        fields = ("type", "child", "guardian")

    type = graphene.Field(RelationshipTypeEnum)

    @classmethod
    @login_required
    def get_queryset(cls, queryset, info):
        return queryset.user_can_view(info.context.user).order_by("id")

    @classmethod
    @login_required
    def get_node(cls, info, id):
        try:
            return cls._meta.model.objects.user_can_view(info.context.user).get(id=id)
        except cls._meta.model.DoesNotExist:
            return None


class RelationshipInput(graphene.InputObjectType):
    type = RelationshipTypeEnum()


class GuardianInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    phone_number = graphene.String()
    language = LanguageEnum(required=True)
    email = graphene.String()


class ChildInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    birthdate = graphene.Date(required=True)
    postal_code = graphene.String(required=True)
    relationship = RelationshipInput()


def validate_child_data(child_data):
    if "postal_code" in child_data:
        try:
            postal_code_validator(child_data["postal_code"])
        except ValidationError as e:
            raise DataValidationError(e.message)
    # TODO temporarily hard-coded until further specs are figured out
    if "birthdate" in child_data:
        birth_year = child_data["birthdate"].year
        if (
            child_data["birthdate"] > localtime(now()).date()
            or not Project.objects.filter(year=birth_year).exists()
        ):
            raise DataValidationError("Illegal birthdate.")
    return child_data


class SubmitChildrenAndGuardianMutation(graphene.relay.ClientIDMutation):
    class Input:
        children = graphene.List(
            graphene.NonNull(ChildInput),
            required=True,
            description="At least one child is required.",
        )
        guardian = GuardianInput(required=True)

    children = graphene.List(ChildNode)
    guardian = graphene.Field(GuardianNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user = info.context.user
        if hasattr(user, "guardian"):
            raise ApiUsageError("You have already used this mutation.")

        children_data = kwargs["children"]
        if not children_data:
            raise ApiUsageError("At least one child is required.")

        if len(children_data) > settings.KUKKUU_MAX_NUM_OF_CHILDREN_PER_GUARDIAN:
            raise MaxNumberOfChildrenPerGuardianError("Too many children.")

        guardian_data = kwargs["guardian"]
        validate_guardian_data(guardian_data)
        guardian = Guardian.objects.create(
            user=user,
            first_name=guardian_data["first_name"],
            last_name=guardian_data["last_name"],
            phone_number=guardian_data.get("phone_number", ""),
            language=guardian_data["language"],
            email=guardian_data.get("email", ""),
        )

        children = []
        for child_data in children_data:
            validate_child_data(child_data)
            relationship_data = child_data.pop("relationship", {})
            child_data["project_id"] = Project.objects.get(
                year=child_data["birthdate"].year
            ).pk
            child = Child.objects.create(**child_data)
            Relationship.objects.create(
                type=relationship_data.get("type"), child=child, guardian=guardian
            )

            children.append(child)

        send_notification(
            guardian.email,
            NotificationType.SIGNUP,
            {"children": children, "guardian": guardian},
            guardian.language,
        )

        return SubmitChildrenAndGuardianMutation(children=children, guardian=guardian)


class AddChildMutation(graphene.relay.ClientIDMutation):
    class Input:
        first_name = graphene.String()
        last_name = graphene.String()
        birthdate = graphene.Date(required=True)
        postal_code = graphene.String(required=True)
        relationship = RelationshipInput()

    child = graphene.Field(ChildNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user = info.context.user
        if not hasattr(user, "guardian"):
            raise ApiUsageError(
                'You need to use "SubmitChildrenAndGuardianMutation" first.'
            )
        if (
            user.guardian.children.count()
            >= settings.KUKKUU_MAX_NUM_OF_CHILDREN_PER_GUARDIAN
        ):
            raise MaxNumberOfChildrenPerGuardianError("Too many children.")

        validate_child_data(kwargs)
        kwargs["project_id"] = Project.objects.get(year=kwargs["birthdate"].year).pk
        user = info.context.user
        relationship_data = kwargs.pop("relationship", {})

        child = Child.objects.create(**kwargs)
        Relationship.objects.create(
            type=relationship_data.get("type"), child=child, guardian=user.guardian
        )

        return AddChildMutation(child=child)


class UpdateChildMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        birthdate = graphene.Date()
        postal_code = graphene.String()
        relationship = RelationshipInput()

    child = graphene.Field(ChildNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        validate_child_data(kwargs)
        user = info.context.user
        child_global_id = kwargs.pop("id")

        try:
            child = Child.objects.user_can_update(user).get(
                pk=from_global_id(child_global_id)[1]
            )
        except Child.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)

        try:
            relationship = child.relationships.get(guardian__user=user)
            update_object(relationship, kwargs.pop("relationship", None))
        except Relationship.DoesNotExist:
            pass

        update_object(child, kwargs)

        return UpdateChildMutation(child=child)


class DeleteChildMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user = info.context.user

        try:
            child = Child.objects.user_can_delete(user).get(
                pk=from_global_id(kwargs["id"])[1]
            )
        except Child.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)

        child.delete()

        return DeleteChildMutation()


class Query:
    children = DjangoFilterConnectionField(ChildNode)
    child = relay.Node.Field(ChildNode)


class Mutation:
    submit_children_and_guardian = SubmitChildrenAndGuardianMutation.Field(
        description="This is the first mutation one needs to execute to start using "
        "the service. After that this mutation cannot be used anymore."
    )
    add_child = AddChildMutation.Field(
        description="This mutation cannot be used before one has started using the "
        'service with "SubmitChildrenAndGuardianMutation".'
    )
    update_child = UpdateChildMutation.Field()
    delete_child = DeleteChildMutation.Field()
