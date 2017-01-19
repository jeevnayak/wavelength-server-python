import graphene

from graphene import resolve_only_args
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import (
    Game as GameModel,
    Round as RoundModel,
    User as UserModel
)

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class Game(SQLAlchemyObjectType):
    class Meta:
        model = GameModel

class Round(SQLAlchemyObjectType):
    class Meta:
        model = RoundModel

class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.String())

    @resolve_only_args
    def resolve_user(self, id):
        return UserModel.query.get(id)

schema = graphene.Schema(query=Query, types=[User, Game, Round])
