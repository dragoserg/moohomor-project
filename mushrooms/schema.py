from __future__ import annotations
import graphene
from graphene_django import DjangoObjectType
from .models import Mushroom, MushroomSpecies, Tag, TimerSession
from django.utils import timezone

class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ('id', 'name',)

class MushroomSpeciesType(DjangoObjectType):
    class Meta:
        model = MushroomSpecies
        fields = ('id', 'name', 'description')

class MushroomType(DjangoObjectType):
    class Meta:
        model = Mushroom
        fields = ('id', 'species', 'tag', 'growth_stage', 'created_at')

class StartTimer(graphene.Mutation):
    class Arguments:
        species_id = graphene.ID(required=True)
        tag_id = graphene.ID(required=False)

    timer_id = graphene.ID()
    start_time = graphene.DateTime()

    @classmethod
    def mutate(cls, root, info, species_id: str, tag_id: str | None = None):
        user = info.context.user
        species = MushroomSpecies.objects.get(id=species_id)
        tag = Tag.objects.get(id=tag_id) if tag_id else None
        session = TimerSession.objects.create(
            user=user,
            species=species,
            tag=tag,
            start_time=timezone.now(),
            end_time=timezone.now(),  # временно равны, обновится при остановке
        )
        return StartTimer(timer_id=session.id, start_time=session.start_time)

class StopTimer(graphene.Mutation):
    class Arguments:
        timer_id = graphene.ID(required=True)

    mushroom = graphene.Field(MushroomType)

    @classmethod
    def mutate(cls, root, info, timer_id: str):
        session = TimerSession.objects.get(id=timer_id)
        session.end_time = timezone.now()
        session.save()
        mushroom = session.user.mushrooms.order_by('-created_at').first()
        return StopTimer(mushroom=mushroom)

class Query(graphene.ObjectType):
    my_mushrooms = graphene.List(MushroomType)

    def resolve_my_mushrooms(self, info):
        user = info.context.user
        return Mushroom.objects.filter(user=user).order_by('-created_at')

class Mutation(graphene.ObjectType):
    start_timer = StartTimer.Field()
    stop_timer = StopTimer.Field()