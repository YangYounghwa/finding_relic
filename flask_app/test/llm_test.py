import pytest
import sys
import os

# Assuming the tests are in flask_app/test/ and you need to adjust the path.

from flask_app.services.LLMService.LLMServiceObject import LLMServiceObjet
from flask import Flask



@pytest.fixture
def mock_flask_app():
    """A fixture to mock a Flask app instance with a logger."""
    app = Flask(__name__)
    with app.app_context():
        yield app


@pytest.mark.skip(reason="Works well now.")
def test_isKorHisRelated_with_logging(mock_flask_app, caplog):
    """
    Tests that the isKoreHistoryRelated() log message is captured.
    """
    # Set the environment variables required for the class to initialize.
    # monkeypatch.setenv("OPENAI_MINI_MODEL", "dummy_mini")
    # monkeypatch.setenv("OPENAI_NANO_MODEL", "dummy_nano")
    
    unrelated = "물론 16세기의 로어노크 식민지 이주시도나 17세기의 제임스타운(Jamestown) 개척이 있긴 했지만, 사실상 성공한 식민 이주는 메이플라워호로 이주한 청교도들 이후였다. 본국은 북미 식민지에 총독을 임명하기는 했으나 이 총독들도 본국 출신보다는 북미 식민지 태생의 이민 2세대나 3세대 인물들이었다. 그리고 각 식민지들은 영국과 영국의 국왕에게 충성한다는 조건하에서 자체적으로 의회와 주 정부를 구성하여 광범위한 자치권을 누리고 있었으며 영국도 이러한 방식으로 식민지를 유지하는 것이 편했다."
    related = "고려가 북진을 표방하고 거란을 노골적으로 적대했으며 요나라 역시 중원으로의 팽창을 염두에 둔 탓에 요와 필연적으로 충돌할 수밖에 없었고 그 결과로 벌어진 세 차례의 전쟁에서 승리했다. 요, 송, 금과 사대 관계를 맺어도 주권 국가로서 처신해 고려만의 독자적 천하관에 따라 내부에 번국을 설정하고 외왕내제 체제를 유지했다."
    china_text = "한편 1922년 갓 건국되었고, 당시 서방 국가들에 의해 고립되어 있던 소련은 중국에 영향력을 확대하여 자신의 우방을 늘리려고 했다. 그래서 코민테른의 명령에 따라 공산당이 국민당에 협력하는 방침을 채택했고, 공산당원들은 당적을 가진 채로 국민당에 입당하는 형식으로 국민당과 공산당은 합작하게 되었다. 이것을 1차 국공합작이라고 한다. 국민당은 광둥성을 세력 기반으로 하고 있었지만, 당시 중국 대륙은 여전히 군벌들이 난립하던 상태였다"

    # Set the logging level for this test to DEBUG to capture all messages.
    with caplog.at_level('DEBUG'):
        llm_service = LLMServiceObjet()
        
        # The function will make a real API call here.
        llm_service.isKorHisRelated(china_text)

        # You can now access the logs captured by caplog.
        print("\n--- Captured Logs ---")
        print(caplog.text)
        print("---------------------")

        # Assert that the specific log message exists in the captured text.
        
        
        
        

def test_getNationality_with_logging(mock_flask_app, caplog):
    """
    Tests that the isKoreHistoryRelated() log message is captured.
    """
    # Set the environment variables required for the class to initialize.
    # monkeypatch.setenv("OPENAI_MINI_MODEL", "dummy_mini")
    # monkeypatch.setenv("OPENAI_NANO_MODEL", "dummy_nano")
    

    goryeo_related = "고려가 북진을 표방하고 거란을 노골적으로 적대했으며 요나라 역시 중원으로의 팽창을 염두에 둔 탓에 요와 필연적으로 충돌할 수밖에 없었고 그 결과로 벌어진 세 차례의 전쟁에서 승리했다. 요, 송, 금과 사대 관계를 맺어도 주권 국가로서 처신해 고려만의 독자적 천하관에 따라 내부에 번국을 설정하고 외왕내제 체제를 유지했다."
    
    Goguryeo_text = """初其臣得來, 見王侵叛中國, 數諫, 王不從. 得來嘆曰, "立見此地, 將生蓬蒿." 遂不食而死. 毋丘儉令諸軍, 不壞其墓, 不伐其樹, 得其妻子, 皆放遣之. 括地志云, "不耐城即國內城也. 城累石爲之." 此即丸都山與國內城相接. 梁書以, "司馬懿討公孫淵, 王遣將襲西安平, 毋丘儉來侵." 通鑑以, "得來諫王, 爲王位宮時事." 誤也."""
    Goguryeo_text_in_korean = """처음에 신하 득래(得來)는 왕이 중국을 침략하고 배반하는 것을 보고 여러 차례 간언하였으나 왕이 따르지 않았다. 득래가 탄식하며 말하기를, "이 땅이 (폐허가 되어) 장차 쑥이 자라나는 꼴을 보겠구나."라고 하고 마침내 음식을 먹지 않고 죽었다. 관구검이 모든 군사들에게 명령하여 그의 무덤을 허물지 말고, 주변의 나무를 베지 못하게 하였으며, 그의 처와 자식을 포로로 잡았으나 모두 놓아서 보내주었다. 《괄지지(括地志)》에는 "불내성이 곧 국내성이다. 성을 돌로 쌓아 만들었다."라고 하였다. 이런즉 환도산과 국내성이 서로 가까이 접하였을 것이다. 《양서》에는 "사마의가 공손연을 토벌하자 왕이 장수를 보내 서안평(西安平)을 습격하였는데 관구검이 침략해왔다."라고 하였다. 《자치통감》에는 "득래가 왕에게 시정을 건의한 것은 왕 위궁(位宮) 때의 일이다."라고 하였는데, 이는 잘못이다"""
    # Set the logging level for this test to DEBUG to capture all messages.
    with caplog.at_level('DEBUG'):
        llm_service = LLMServiceObjet() 
        
        # The function will make a real API call here.
        llm_service.getNationality(Goguryeo_text)

        # You can now access the logs captured by caplog.
        print("\n--- Captured Logs ---")
        print(caplog.text)
        print("---------------------")

        # Assert that the specific log message exists in the captured text.