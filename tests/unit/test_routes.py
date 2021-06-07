from json import loads


def test_app(app):
    resp = app.get('/', headers={'api_token': 'token'})
    assert resp.status_code == 200


def test_pet_settlement(app):
    """
    test pets_settlement route with create/delete operations
    """
    data_json = {
            "owner_name": "test 12",
            "owner_phone": "65465137878",
            "pet_name": "test pet name 1876",
            "room_num": 15
            }
    # create pet
    resp = app.post('/pets_settlement',
                    json=data_json,
                    headers={'api_token': 'token'})

    # check is pet created
    resp = app.get('/pets_settlement', headers={'api_token': 'token'})
    assert resp.status_code == 200
    assert data_json['pet_name'] in loads(resp.data)

    # check pet deletion
    resp = app.post('/pets_eviction',
                    json=data_json,
                    headers={'api_token': 'token'})
    assert 'days' in loads(resp.data)

    resp = app.get('/pets_settlement', headers={'api_token': 'token'})
    assert data_json['pet_name'] not in loads(resp.data)


def test_activity_list(app):
    """
    test activity_list route route with create/delete operations
    """
    data_json = {
            "owner_name": "test 12",
            "owner_phone": "65465137878",
            "pet_name": "test pet name1123",
            "room_num": 16
            }
    # create pet
    resp = app.post('/pets_settlement',
                    json=data_json,
                    headers={'api_token': 'token'})

    # check activity exists
    resp = app.get('/activity_list', headers={'api_token': 'token'})
    assert any(["test pet name" in act['pet_name']
                for act in loads(resp.data)['Activities']])

    # pet deletion
    resp = app.post('/pets_eviction',
                    json=data_json,
                    headers={'api_token': 'token'})

    # check empty activity
    resp = app.get('/activity_list', headers={'api_token': 'token'})
    assert not any([data_json['pet_name'] in act['pet_name']
                    for act in loads(resp.data)['Activities']])


def test_wrong_room(app):
    """
    test rooms out of 1-20 range
    """
    # check for 21 room
    data_json = {
            "owner_name": "test 12",
            "owner_phone": "65465137878",
            "pet_name": "test pet name1123",
            "room_num": 21
            }
    resp = app.post('/pets_settlement',
                    json=data_json,
                    headers={'api_token': 'token'})
    assert resp.status_code == 200
    assert {'message': "Wrong room"} == resp.json

    # check for 0 room
    data_json = {
            "owner_name": "test 12",
            "owner_phone": "65465137878",
            "pet_name": "test pet name1123",
            "room_num": 0
            }
    resp = app.post('/pets_settlement',
                    json=data_json,
                    headers={'api_token': 'token'})

    # check pet create
    assert resp.status_code == 200
    assert {'message': "Wrong room"} == resp.json


def test_empty_rooms(app):
    """
    test empty_rooms route
    """
    data_json = {
            "owner_name": "test 112212",
            "owner_phone": "1231",
            "pet_name": "test pet name8765",
            "room_num": 19
            }
    # create pet
    resp = app.post('/pets_settlement',
                    json=data_json,
                    headers={'api_token': 'token'})

    # check empty rooms to not contain 19 room
    resp = app.get('/empty_rooms', headers={'api_token': 'token'})
    assert data_json['room_num'] not in loads(resp.data)['empty rooms']

    # pet delete
    resp = app.post('/pets_eviction',
                    json=data_json,
                    headers={'api_token': 'token'})
