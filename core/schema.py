from __future__ import annotations
import graphene
from graphene_django import DjangoObjectType
from .models import Achievement

class AchievementType(DjangoObjectType):
    class Meta:
        model = Achievement
        fields = ('id', 'title', 'description')

class Query(graphene.ObjectType):
    my_achievements = graphene.List(AchievementType)

    def resolve_my_achievements(self, info):
        user = info.context.user
        return user.achievements.all()

class Mutation(graphene.ObjectType):
    pass