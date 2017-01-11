import datetime

from app import db

games = db.Table("games",
    db.Column("game_id", db.Integer, db.ForeignKey("game.id")),
    db.Column("user_id", db.String(255), db.ForeignKey("user.id"))
)

class User(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    fb_token = db.Column(db.String(255))
    games = db.relationship("Game", secondary=games, backref="players")

    def __init__(self, id, name, first_name, last_name, fb_token):
        self.id = id
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.fb_token = fb_token

    def __repr__(self):
        return "<User(id=%s, name=%s)>" % (self.id, self.name)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.String(255))
    rounds = db.relationship("Round", backref="game")

    def __init__(self, creator_id):
        self.creator_id = creator_id

    def __repr__(self):
        return "<Game(id=%s, creator_id=%s)>" % (self.id, self.creator_id)

class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))
    word = db.Column(db.String(255))
    cluer_id = db.Column(db.String(255))
    clues = db.Column(db.String(255))
    guesses = db.Column(db.String(255))
    replayed = db.Column(db.Boolean)
    updated = db.Column(db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)

    def __init__(self, word, cluer_id):
        self.word = word
        self.cluer_id = cluer_id

    def __repr__(self):
        return "<Round(id=%s, word=%s, cluer_id=%s)>" % (self.id, self.word, self.cluer_id)
