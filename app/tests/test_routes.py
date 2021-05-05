from flask import jsonify

def test_get_all_planets_with_no_records_return_empty_list(client):
    response = client.get("/planets/all-planets")
    response_body = response.get_json()

    assert response.status_code == 200 
    assert response_body == []

def test_get_one_planet_return_its_data(client, two_test_planets):
    response = client.get("/planets/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Test_planet_1", 
        "description": "Description of Test_planet_1",
        "order": 100
    }

def test_get_one_planet_return_error(client):
    response = client.get("/planets/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": f"Planet with id #1 was not found."} 

def test_get_all_planets_return_their_data(client, two_test_planets):
    response = client.get("/planets/all-planets")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2

def test_post_planet(client, add_planet):

    response = client.post("/planets/add-planet", json=add_planet)
    print('1: ', add_planet)
    response_body = response.get_json()
    print('2: ', response)

    assert response.status_code == 201
    assert response_body == "Planet Test_planet_3 has been successfully added."
