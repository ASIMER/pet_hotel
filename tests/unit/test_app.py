def test_app(app):
    resp = app.get('/', headers={'api_token': 'token'})
    assert resp.status_code == 200
