from __future__ import annotations
import graphene
import mushrooms.schema as mushrooms_schema
import core.schema as core_schema

class Query(mushrooms_schema.Query, core_schema.Query, graphene.ObjectType):
    pass

class Mutation(mushrooms_schema.Mutation, core_schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)