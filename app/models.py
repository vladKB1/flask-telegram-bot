from app import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, index=True)


class User(Base):
    __tablename__ = "users"
    username = db.Column(db.String(64))
    state = db.Column(db.String(64))
    state_data = db.Column(db.String(64))
    #posts = db.relationship("Post", backref="users", lazy=True)


class Channel(Base):
    __tablename__ = "channels"
    channel_id = db.Column(db.String(64))
    name = db.Column(db.String(64))
    admin_user = db.Column(db.Integer)
    #post_messages = db.relationship("Post", backref="channels", lazy=True)


class Post(Base):
    __tablename__ = "posts"
    user_id = db.Column(db.Integer)
    channel_id = db.Column(db.String(64))
    text = db.Column(db.Text)


class UserFavoritesRelation(Base):
    __tablename__ = "user_favorites_relations"
    user_id = db.Column(db.Integer)
    channel_id = db.Column(db.String(64))
