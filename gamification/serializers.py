from rest_framework import serializers

from gamification.models import Badge, UserBadge, Point, Leaderboard


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ["id", "name", "description", "icon", "created_by", "active"]
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": True},
            "icon": {"required": True},
            "created_by": {"required": True},
            "active": {"required": True},
        }


class UserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadge
        fields = ["id", "user", "badge", "awarded_at", "active"]
        read_only_fields = ["awarded_at"]
        extra_kwargs = {
            "user": {"required": True},
            "badge": {"required": True},
            "awarded_at": {"required": True},
            "active": {"required": True},
        }


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ["id", "user", "value", "reason", "type", "created_at"]
        read_only_fields = ["created_at"]
        extra_kwargs = {
            "user": {"required": True},
            "value": {"required": True},
            "reason": {"required": True},
            "type": {"required": True},
            "created_at": {"required": True},
        }


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ["id", "user", "total_points", "last_updated"]
