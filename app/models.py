from app import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.BigInteger, primary_key=True, index=True)


# one-to-one db.relationship("", backref="", lazy=True, uselist=False)


class User(Base):
    __tablename__ = "users"
    username = db.Column(db.String(64))
    state = db.Column(db.String(64))
    state_data = db.Column(db.String(512))
    posts = db.relationship("Post", backref="users", lazy=True)


class Channel(Base):
    __tablename__ = "channels"
    name = db.Column(db.String(64))
    admin_user = db.Column(db.BigInteger, index=True)
    posts = db.relationship("Post", backref="channels", lazy=True)


class Post(Base):
    __tablename__ = "posts"
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    channel_id = db.Column(db.BigInteger, db.ForeignKey("channels.id"))
    text = db.Column(db.Text)


class UserFavoritesRelation(Base):
    __tablename__ = "user_favorites_relations"
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), index=True)
    channel_id = db.Column(db.BigInteger, db.ForeignKey("channels.id"))
