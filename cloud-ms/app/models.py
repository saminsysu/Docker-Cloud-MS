from . import db
import datetime

class IdMixin(object):
    """ ID mixin
    """
    id = db.Column(db.Integer, primary_key=True)

class TimestampMixin(object):
    """ Timestamp mixin
    """
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    # updated_at = db.Column(db.DateTime, default=datetime.datetime.now,
    #                        onupdate=datetime.datetime.now)


class Container(db.Model, IdMixin, TimestampMixin):
    __tablename__ = 'containers'
    container_id = db.Column(db.String(64), default='default')
    username = db.Column(db.String(64), default='default')
    container_name = db.Column(db.String(64), default='default')
    ports = db.Column(db.String(128), default='default')
    status = db.Column(db.String(64), default='default')

    def __repr__(self):
        return '<Container %r>' % self.container_name

