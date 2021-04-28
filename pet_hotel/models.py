import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import SMALLINT, TIMESTAMP, UUID, VARCHAR

db = SQLAlchemy()


class Owners(db.Model):
    """
    this class represents pet owner in db

    @owner_id - UUID\n
    @owner_name - VARCHAR(50)\n
    @phone - VARCHAR(15)
    """
    __tablename__ = 'Owners'
    owner_id = db.Column(UUID(as_uuid=True),
                         primary_key=True,
                         default=uuid.uuid4)
    owner_name = db.Column(VARCHAR(50), nullable=False)
    phone = db.Column(VARCHAR(15), nullable=False)

    pet = db.relationship('Pets',
                          backref=db.backref('Owners', lazy=True),
                          cascade="all, delete")

    def __repr__(self):
        return '<Owner %r with phone %r>' % (self.owner_name, self.phone)


class Pets(db.Model):
    """
    this class represents pet owner in db
    """
    __tablename__ = 'Pets'
    pet_id = db.Column(UUID(as_uuid=True),
                       primary_key=True,
                       default=uuid.uuid4)
    pet_name = db.Column(VARCHAR(20))
    booking_time = db.Column(TIMESTAMP, nullable=False,
                             default=datetime.utcnow)
    room_num = db.Column(SMALLINT, nullable=False)
    # foreign relation
    owner_id = db.Column(UUID(as_uuid=True),
                         db.ForeignKey('Owners.owner_id'),
                         nullable=False)

    activity = db.relationship('Activities',
                               backref=db.backref('Pets', lazy=True),
                               cascade="all, delete")

    def __repr__(self):
        return '<Pet %r booked at %r in room %r>' % (
                self.pet_name, self.booking_time, self.room_num)


class Activities(db.Model):
    """
    this class represents all activities assigned to pets
    """
    __tablename__ = 'Activities'
    activity_id = db.Column(UUID(as_uuid=True),
                            primary_key=True,
                            default=uuid.uuid4)
    activity_time = db.Column(TIMESTAMP, nullable=False,
                              default=datetime.utcnow)
    activity_type = db.Column(VARCHAR(20), nullable=False)
    # foreign relation
    pet_id = db.Column(UUID(as_uuid=True),
                       db.ForeignKey('Pets.pet_id'),
                       nullable=False)

    def __repr__(self):
        return '<Activity %r registered at %r in room %r>' % (
                self.pet_name, self.booking_time, self.room_num)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        try:
            session.add(instance)
            session.commit()
        except Exception:
            session.rollback()
            instance = session.query(model).filter_by(**kwargs).one()
            return instance
        else:
            return instance
