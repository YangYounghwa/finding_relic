


import pytest
import sys
import os

# Assuming the tests are in flask_app/test/ and you need to adjust the path.


from pprint import pprint
from flask import Flask
import json



@pytest.fixture
def mock_flask_app():
    """A fixture to mock a Flask app instance with a logger."""
    from relic_app.app import create_app
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture
def client(mock_flask_app):  # <-- CORRECTED LINE
    # This now correctly receives the app object from the 'mock_flask_app' fixture.
    return mock_flask_app.test_client()


# @pytest.mark.skip(reason="Works well now.")
def test_search_text_success(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to /test/searchText with valid JSON
    THEN check that the response is successful and contains the correct data
    """
    # 1. Arrange: Set up the mock and test data
    search_term = """문헌기록상으로는 두정갑옷은 조선 성종때 간행된 『국조오례의서례』 ‘병기도설’(兵器圖說)에 처음 등장한다. ‘병기도설’의 두정갑은 두 종류로 실전용인 철두정갑과 방호재인 찰이 없는 의장용 황동두정갑이 있었다. 먼저 실전용인 철두정갑은 청금포로 옷을 만들고 옷의 안쪽에 쇠로 만든 찰을 촘촘히 대고 겉에 쇠못을 박아 고정한 형태다. 반면 의장용 황동두정갑은 홍단자로 만들며, 갑옷의 안쪽에 연기를 쏘인 사슴가죽을 대고 겉에 황동으로 만든 못을 박아 고정한 형태다. 또한 철두정갑과 달리 소매를 별도로 만들어 끈으로 연결하도록 제작되었으며, 붉은색으로 짠 넓은 조대를 허리에 두른다.

이후 조선 후기에 평화가 오래 지속되자 일부 장수들은 두정갑 대신 장식갑옷을 입는 경우가 있었다. 장식갑옷은 두정갑과 겉모습이 똑같지만 내부에 갑옷미늘이 없다. 갑옷미늘이 없으므로 방호력도 약하고 당연히 실제 갑옷으로서의 효과는 없다..""" 
    post_data = {"data": {"text": search_term}}
    
    # This is the data we expect searcher.getItemList to return
    
    # Use 'patch' to temporarily replace 'searcher.getItemList' during this test.
    # We configure its return value.

    response = client.post('/test/searchText', json=post_data)

    # 3. Assert: Check the results
    assert response.status_code == 200
    
    # Verify that the mocked function was called correctly

    response_data = response.get_json()
    assert response_data['success'] is True
    assert response_data['message'] == "Success"
    print(response_data['data'])
       # Save the response data to a JSON file
    with open('search_text_response.json', 'w', encoding='utf-8') as f:
        json.dump(response_data, f, ensure_ascii=False, indent=4)
    
    print(f"Response data saved to search_text_response.json") 


# @pytest.mark.skip(reason="Works well now.")
def test_detail_info_with_query_params(client):
    """

    """
    item_id = 'PS0100100101101235600000'
        
    response = client.get(f'/test/detailInfo?id={item_id}')

    assert response.status_code == 200

    
    response_data = response.get_json()
    print(response_data)
    assert response_data['success'] is True
    with open('detail_info_response.json', 'w', encoding='utf-8') as f:
        json.dump(response_data, f, ensure_ascii=False, indent=4)
    
    print(f"Response data saved to detail_info_response.json")
    
    

def test_user_add(client):
    """

    """
    response = client.get('/test/userAdd?google_id=1')
    print(response.get_json())
    
     
