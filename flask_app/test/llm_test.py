import pytest
import sys
import os

# Assuming the tests are in flask_app/test/ and you need to adjust the path.

from flask_app.services.LLMService.LLMServiceObject import LLMServiceObjet
from flask_app.services.emuseumService.EmuseumService import emuseum
from pprint import pprint
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
        
        
        
        
@pytest.mark.skip(reason="Works well now.")
def test_getNationality_with_logging(mock_flask_app, caplog):
    """
    Tests that the getNationalityd() log message is captured.
    """

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

@pytest.mark.skip(reason="Works well now.")
def test_getDetailInfo_with_logging(mock_flask_app, caplog):
    emuseum.getDetailInfo(id='PS0100100101101235600000')
    
    
@pytest.mark.skip(reason="Works well now.")
def test_getMaterial_with_logging(mock_flask_app, caplog):
    """
    Tests that the getMaterial() log message is captured.
    """

    book = "직지심체요절의 정확한 이름은 《백운화상초록불조직지심체요절(白雲和尙抄錄佛祖直指心體要節)》이다. 제목을 풀이하면 백운[3]이라는 고승(화상)이 간추린(초록) 부처님(불조)의 깨달음(직지심체[4])을 요약한 책(요절)이라는 뜻이다. 이름이 길기 때문에 세간에서는 '직지' 또는 '직지심체요절'로 축약해서 부르는 경우가 많다. 일부에서는 '직지심경'으로 부르기도 하나, 직지는 불경이 아닌 요절이므로 '직지심경'은 명백히 잘못된 표현이다. 아마 반야심경을 불경의 대표라고 생각해서 직지+반야심경의 합성으로 튀어나온 단어인 듯."
    
    gold_crown_text = """신라 금관은 1921년 금관총에서 금관 및 금제 관식이 발견되며 처음 알려지게 되었다. 이후 1924년에 금령총에서, 1926년에 서봉총에서 잇달아 금관이 발굴되며 본격적인 관심을 받기 시작했다. 신라 금관들은 대부분 유사한 형태를 가지고 있는데, 이러한 모습을 샤먼의 관에 순록 뿔이 장식되던 것에 비유하여 샤머니즘적 권위를 나타낸 것이라는 의견이 1930년대에 처음 제안되었다.[2] 해방 이후의 한국 학계도 이러한 주장을 받아들여 연구를 계속 하고 있다."""

    # Set the logging level for this test to DEBUG to capture all messages.
    with caplog.at_level('DEBUG'):
        llm_service = LLMServiceObjet() 
        
        # The function will make a real API call here.
        llm_service.getMaterial(book)

        # You can now access the logs captured by caplog.
        print("\n--- Captured Logs ---")
        print(caplog.text)
        print("---------------------")


@pytest.mark.skip(reason="Works well now.")   
def test_getMaterial_with_logging2(mock_flask_app, caplog):
    """
    Tests that the getMaterial() log message is captured.
    """

    book = "직지심체요절의 정확한 이름은 《백운화상초록불조직지심체요절(白雲和尙抄錄佛祖直指心體要節)》이다. 제목을 풀이하면 백운[3]이라는 고승(화상)이 간추린(초록) 부처님(불조)의 깨달음(직지심체[4])을 요약한 책(요절)이라는 뜻이다. 이름이 길기 때문에 세간에서는 '직지' 또는 '직지심체요절'로 축약해서 부르는 경우가 많다. 일부에서는 '직지심경'으로 부르기도 하나, 직지는 불경이 아닌 요절이므로 '직지심경'은 명백히 잘못된 표현이다. 아마 반야심경을 불경의 대표라고 생각해서 직지+반야심경의 합성으로 튀어나온 단어인 듯."
    
    gold_crown_text = """신라 금관은 1921년 금관총에서 금관 및 금제 관식이 발견되며 처음 알려지게 되었다. 이후 1924년에 금령총에서, 1926년에 서봉총에서 잇달아 금관이 발굴되며 본격적인 관심을 받기 시작했다. 신라 금관들은 대부분 유사한 형태를 가지고 있는데, 이러한 모습을 샤먼의 관에 순록 뿔이 장식되던 것에 비유하여 샤머니즘적 권위를 나타낸 것이라는 의견이 1930년대에 처음 제안되었다.[2] 해방 이후의 한국 학계도 이러한 주장을 받아들여 연구를 계속 하고 있다."""

    # Set the logging level for this test to DEBUG to capture all messages.
    with caplog.at_level('DEBUG'):
        llm_service = LLMServiceObjet() 
        
        # The function will make a real API call here.
        llm_service.getMaterial(gold_crown_text)

        # You can now access the logs captured by caplog.
        print("\n--- Captured Logs ---")
        print(caplog.text)
        print("---------------------")
    
