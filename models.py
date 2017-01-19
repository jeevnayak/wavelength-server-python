from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    func,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship

from database import Base

games_users = Table("games_users", Base.metadata,
    Column("game_id", Integer, ForeignKey("games.id")),
    Column("user_id", String(255), ForeignKey("users.id")))

class User(Base):
    __tablename__ = "users"
    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    fb_token = Column(String(255))
    games = relationship("Game", secondary=games_users, backref="players")

    def __init__(self, id, name, first_name, last_name, fb_token):
        self.id = id
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.fb_token = fb_token

    def __repr__(self):
        return "<User(id=%s, name=%s)>" % (self.id, self.name)

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    creator_id = Column(String(255))
    rounds = relationship("Round", backref="game")

    def __init__(self, creator_id):
        self.creator_id = creator_id

    def __repr__(self):
        return "<Game(id=%s, creator_id=%s)>" % (self.id, self.creator_id)

class Round(Base):
    __tablename__ = "rounds"
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    word = Column(String(255))
    cluer_id = Column(String(255))
    clues = Column(String(255))
    guesses = Column(String(255))
    replayed = Column(Boolean)
    updated = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, word, cluer_id):
        self.word = word
        self.cluer_id = cluer_id

    def __repr__(self):
        return "<Round(id=%s, word=%s, cluer_id=%s)>" % (
            self.id, self.word, self.cluer_id)
