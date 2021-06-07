from datetime import datetime

from flask import request
from flask_restful import Resource
from sqlalchemy import func

from .models import Activities, Owners, Pets, db, get_or_create


class MainPage(Resource):
    def get(self):
        return {}, 200


class EmptyRooms(Resource):
    def get(self):
        pets = db.session.query(Pets.room_num, func.count(Pets.room_num)). \
            group_by(Pets.room_num).all()
        filled_rooms = set([pet.room_num for pet in pets])
        empty_rooms = set(range(1, 21))
        empty_rooms -= filled_rooms

        return {'empty rooms': list(empty_rooms)}, 200


class ActivityList(Resource):
    def get(self):
        activities = db.session.query(Pets, Activities).all()
        result = []
        for activity in activities:
            result.append(
                    {
                            "pet_name": activity[0].pet_name,
                            "day": activity[1].activity_time.day,
                            "hour": activity[1].activity_time.hour,
                            "minute": activity[1].activity_time.minute,
                            "type": activity[1].activity_type
                            }
                    )
        print(result)
        return {'Activities': result}, 200


class PetsSettlement(Resource):
    """
    Page for pets settlement
    """

    def post(self):
        response = request.get_json()
        if not response:
            return {'message': "Request empty"}, 200
        elif response['room_num'] not in range(1, 21):
            return {'message': "Wrong room"}, 200
        elif not all(['owner_name' in response, 'owner_phone' in response,
                      'pet_name' in response, 'room_num' in response,
                      ]):
            return {'message': "Wrong request attributes"}, 200

        owner_name = response['owner_name']
        owner_phone = response['owner_phone']
        pet_name = response['pet_name']
        room_num = response['room_num']

        # check if pet already exists
        if Pets.query.filter_by(pet_name=pet_name,
                                room_num=room_num).one_or_none():
            return {'message': 'This pet already exists'}, 201

        owner = get_or_create(session=db.session,
                              model=Owners,
                              owner_name=owner_name, phone=owner_phone)

        pet = Pets(owner_id=owner.owner_id,
                   pet_name=pet_name,
                   room_num=room_num)
        owner.pet.append(pet)
        activity = Activities(activity_time=datetime.now(),
                              activity_type="eat",
                              pet_id=pet.pet_id)
        pet.activity.append(activity)
        db.session.commit()

        return {'message': 'Pet entity has been created'}, 201

    def get(self):
        pets = Pets.query.all()
        result = {}
        for pet in pets:
            result[pet.pet_name] = pet.room_num
        return result, 200


class PetsEviction(Resource):
    """
    Page for pets eviction
    """

    def post(self):
        response = request.get_json()
        if not response:
            return {'message': "Request empty"}, 200
        elif not all(['pet_name' in response, 'room_num' in response,
                      ]):
            return {'message': "Wrong request attributes"}, 200
        elif response['room_num'] not in range(1, 21):
            return {'message': "Wrong room"}, 200

        pet_name = response['pet_name']
        room_num = response['room_num']

        pet = Pets.query.filter_by(pet_name=pet_name,
                                   room_num=room_num).one_or_none()
        if pet:
            livetime = datetime.now() - pet.booking_time
            owner = pet.owner_id

            # check if owner has another pets
            another_pet = Pets.query.filter_by(owner_id=owner).all()
            if not another_pet:
                owner = Owners.query.filter_by(owner_id=owner).one_or_none()
                db.session.delete(owner)

            db.session.delete(pet)
            db.session.commit()

            return {'days': livetime.days}, 200
        else:
            return {'lifetime': "No such pet in hotel"}, 200

    def get(self):
        pets = Pets.query.all()
        result = {}
        for pet in pets:
            result[pet.pet_name] = pet.room_num
        return result, 200
