#  Copyright 2023 Red Hat, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from aap_eda.api.serializers.fields.yaml import YAMLSerializerField
from aap_eda.core import models


class RulebookSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        queryset=models.Project.objects.all(),
        help_text="ID of the project",
    )
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Organization.objects.all(),
        help_text="ID of the organization",
    )

    class Meta:
        model = models.Rulebook
        fields = [
            "id",
            "name",
            "description",
            "rulesets",
            "project_id",
            "organization_id",
            "created_at",
            "modified_at",
        ]
        read_only_fields = [
            "id",
            "organization_id",
            "created_at",
            "modified_at",
        ]


class RulebookRefSerializer(serializers.ModelSerializer):
    """Serializer for Rulebook reference."""

    class Meta:
        model = models.Rulebook
        fields = ["id", "name", "description", "organization_id"]
        read_only_fields = ["id", "organization_id"]


class AuditRuleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        required=True,
        help_text="ID of the fired rule",
    )

    name = serializers.CharField(
        required=True,
        help_text="Name of the fired rule",
    )

    status = serializers.CharField(
        required=False,
        help_text="Status of the fired rule",
    )

    ruleset_name = serializers.CharField(
        required=False,
        help_text="Name of the related ruleset",
    )

    fired_at = serializers.DateTimeField(
        required=True,
        help_text="The fired timestamp of the rule",
    )

    class Meta:
        model = models.AuditRule
        fields = [
            "id",
            "name",
            "description",
            "status",
            "created_at",
            "fired_at",
            "rule_uuid",
            "ruleset_uuid",
            "ruleset_name",
            "activation_instance_id",
            "job_instance_id",
            "organization_id",
            "definition",
        ]
        read_only_fields = ["id", "organization_id", "created_at"]


class AuditRuleDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        required=True,
        help_text="ID of the fired rule",
    )

    name = serializers.CharField(
        required=True,
        help_text="Name of the fired rule",
    )

    status = serializers.CharField(
        required=False,
        help_text="Status of the fired rule",
    )

    activation_instance = serializers.SerializerMethodField()

    organization = serializers.SerializerMethodField()

    ruleset_name = serializers.CharField(
        required=False,
        help_text="Name of the related ruleset",
    )

    created_at = serializers.DateTimeField(
        required=True,
        help_text="The created timestamp of the action",
    )

    fired_at = serializers.DateTimeField(
        required=True,
        help_text="The fired timestamp of the rule",
    )

    @extend_schema_field(
        {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "nullable": True},
                "name": {"type": "string"},
            },
            "example": {"id": 0, "name": "string"},
        }
    )
    def get_activation_instance(self, rule):
        instance = rule.activation_instance
        if instance:
            return {"id": instance.id, "name": instance.name}
        else:
            return {"id": None, "name": "DELETED"}

    @extend_schema_field(
        {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "nullable": False},
                "name": {"type": "string"},
                "description": {"type": "string"},
            },
            "example": {"id": 0, "name": "string", "description": "string"},
        }
    )
    def get_organization(self, rule):
        organization = rule.organization
        return {
            "id": organization.id,
            "name": organization.name,
            "description": organization.description,
        }


class AuditRuleListSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        required=True,
        help_text="ID of the fired rule",
    )

    name = serializers.CharField(
        required=True,
        help_text="Name of the fired rule",
    )

    status = serializers.CharField(
        required=False,
        help_text="Status of the fired rule",
    )

    activation_instance = serializers.SerializerMethodField()

    organization = serializers.SerializerMethodField()

    fired_at = serializers.DateTimeField(
        required=True,
        help_text="The fired timestamp of the rule",
    )

    @extend_schema_field(
        {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "nullable": True},
                "name": {"type": "string"},
            },
            "example": {"id": 0, "name": "string"},
        }
    )
    def get_activation_instance(self, rule):
        instance = rule.activation_instance
        if instance:
            return {"id": instance.id, "name": instance.name}
        else:
            return {"id": None, "name": "DELETED"}

    @extend_schema_field(
        {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "nullable": False},
                "name": {"type": "string"},
                "description": {"type": "string"},
            },
            "example": {"id": 0, "name": "string", "description": "string"},
        }
    )
    def get_organization(self, rule):
        organization = rule.organization
        return {
            "id": organization.id,
            "name": organization.name,
            "description": organization.description,
        }


class AuditActionSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(
        required=True,
        help_text="UUID of the triggered action",
    )

    name = serializers.CharField(
        required=True,
        help_text="Name of the action",
    )

    status = serializers.CharField(
        required=False,
        help_text="Status of the action",
    )

    url = serializers.URLField(
        required=False,
        help_text="The URL in the action",
    )

    fired_at = serializers.DateTimeField(
        required=True,
        help_text="The fired timestamp of the action",
    )

    status_message = serializers.CharField(
        required=False,
        allow_null=True,
        help_text="Message of the action",
    )

    class Meta:
        model = models.AuditAction
        fields = [
            "id",
            "name",
            "status",
            "url",
            "fired_at",
            "rule_fired_at",
            "audit_rule_id",
            "status_message",
        ]
        read_only_fields = ["id"]


class AuditEventSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(
        required=True,
        help_text="UUID of the triggered event",
    )

    source_name = serializers.CharField(
        required=True,
        help_text="Name of the source",
    )

    source_type = serializers.CharField(
        required=True,
        help_text="Type of the source",
    )

    received_at = serializers.DateTimeField(
        required=True,
        help_text="The received timestamp of the event",
    )

    payload = YAMLSerializerField(
        required=False,
        allow_null=True,
        help_text="The payload in the event",
    )

    class Meta:
        model = models.AuditEvent
        fields = [
            "id",
            "source_name",
            "source_type",
            "payload",
            "audit_actions",
            "received_at",
            "rule_fired_at",
        ]
        read_only_fields = ["id"]
