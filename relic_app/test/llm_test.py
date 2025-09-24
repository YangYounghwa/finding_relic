import pytest
import sys
import os

# Assuming the tests are in flask_app/test/ and you need to adjust the path.

from relic_app.services.LLMService.LLMServiceObject import LLMServiceObjet
from relic_app.services.LLMService.LLMServiceObject import llmService
from relic_app.services.emuseumService.EmuseumService import emuseum
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
        llm_service = llmService
        
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
        llm_service = llmService
        
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
        llm_service = llmService
        
        # The function will make a real API call here.
        llm_service.getMaterial(gold_crown_text)

        # You can now access the logs captured by caplog.
        print("\n--- Captured Logs ---")
        print(caplog.text)
        print("---------------------")
        
@pytest.mark.skip(reason="Works well now.")   
def test_getPurpose_with_logging2(mock_flask_app, caplog):
    """
    Tests that the getMaterial() log message is captured.
    """

    crown_text = """금관총 금관은 지금까지 발견된 신라 금관 중 가장 큰 것이다.[30] 이 금관이 발굴된 노서동의 고분은 금관총이라는 이름을 갖게 되었다. 1962년 12월 12일 국보로 지정되었다.
높이는 44 cm, 머리띠 지름은 19 cm이다. 금관은 내관(內冠)과 외관(外冠)으로 구성되어 있는데, 이 금관은 외관으로 신라금관의 전형을 보여주고 있다. 즉, 원형의 머리띠 정면에 3단으로 ‘출(出)’자 모양의 장식 3개를 두고, 뒤쪽 좌우에 2개의 나뭇가지형(樹枝形) 혹은 사슴뿔모양(鹿角形) 금판 장식이 세워져 있다. 머리띠와 ‘출(出)’자 장식 주위에는 점이 찍혀 있고, 많은 비취색 옥과 구슬모양의 장식들이 규칙적으로 금실에 매달려 있다. 양 끝에는 가는 고리에 금으로 된 사슬이 늘어진 두 줄의 장식이 달려 있는데, 일정한 간격으로 나뭇잎 모양의 장식을 달았으며, 줄 끝에는 비취색 옥이 달려 있다. 현재 국립경주박물관에 있다.."""
    


    # Set the logging level for this test to DEBUG to capture all messages.
    with caplog.at_level('DEBUG'):
        llm_service = LLMServiceObjet() 
        
        # The function will make a real API call here.
        llm_service.getPurpose(crown_text)

        # You can now access the logs captured by caplog.
        print("\n--- Captured Logs ---")
        print(caplog.text)
        print("---------------------")
    
@pytest.mark.skip(reason="Works well.") 
def test_three_with_logging(mock_flask_app, caplog):
    
    
    armor_text = """문헌기록상으로는 두정갑옷은 조선 성종때 간행된 『국조오례의서례』 ‘병기도설’(兵器圖說)에 처음 등장한다. ‘병기도설’의 두정갑은 두 종류로 실전용인 철두정갑과 방호재인 찰이 없는 의장용 황동두정갑이 있었다. 먼저 실전용인 철두정갑은 청금포로 옷을 만들고 옷의 안쪽에 쇠로 만든 찰을 촘촘히 대고 겉에 쇠못을 박아 고정한 형태다. 반면 의장용 황동두정갑은 홍단자로 만들며, 갑옷의 안쪽에 연기를 쏘인 사슴가죽을 대고 겉에 황동으로 만든 못을 박아 고정한 형태다. 또한 철두정갑과 달리 소매를 별도로 만들어 끈으로 연결하도록 제작되었으며, 붉은색으로 짠 넓은 조대를 허리에 두른다.

이후 조선 후기에 평화가 오래 지속되자 일부 장수들은 두정갑 대신 장식갑옷을 입는 경우가 있었다. 장식갑옷은 두정갑과 겉모습이 똑같지만 내부에 갑옷미늘이 없다. 갑옷미늘이 없으므로 방호력도 약하고 당연히 실제 갑옷으로서의 효과는 없다..""" 
    with caplog.at_level('DEBUG'):
        from relic_app.services.searchService.SearchService import SearchServiceObject
        search = SearchServiceObject()
        
        print(search.getItemList(armor_text))
        # The function will make a real API call here.
        
        
@pytest.mark.skip(reason="Works well now.") 
def test_EmuseumService(mock_flask_app, caplog):
    print("-----emuseum testing----")
    
    print(emuseum.getItemsByKeywords(name="백자", nationalityCode="PS06001")) 
    print(caplog.text)
    # emuseum.getDetailInfo(id="PS0100100101101235600000")
    # print(caplog.text)

