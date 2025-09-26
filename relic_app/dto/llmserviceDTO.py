







from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
class KorRelation(BaseModel):
    related:bool = Field(description="Whether if the text is related to the Korean history")
    unsure:bool = Field(description="If you are not sure about it, mark as true")
            
            
# Step 1: Define the Enum for Korean dynasties
class KoreanNationsEnum(str, Enum):

    oldStoneAge = "구석기"
    middleStoneAge = "중석기"
    neolithicAge = "신석기"
    bronzeAge = "청동기"
    earlyIronAge = "초기철기"
    protoThreeKingdoms = "원삼국"
    nangang = "낙랑"
    goguryeobaekje = "고구려"
    baekje = "백제"
    silla = "신라"
    gaya = "가야"
    threeKingdoms = "삼국"
    unifinedSilla = "통일신라"
    balhae = "발해"
    lateSillatoEarlyGoryeo = "라말여초"
    goryeo = "고려"
    goguryeolateGoryeoEarlyJoseon = "려말선초"
    joseon = "조선"
    daehanjeguk = "대한제국"
    japaneseRuleofKoreaByForce = "일제강점"
    afterIndependence = "광복이후"
    after2000 = "2000년 이후"
    ageUnknown = "시대미상"
    

class Nations(BaseModel):
    name: KoreanNationsEnum = Field(description="Historic era/nation names in Korean history.")
    certainty: bool = Field(description="Is it certain, if so True on first name")
    candidate: Optional[KoreanNationsEnum] = Field(description="A candidate historic era/nation name in Korean history.")
    candidate_certainty: bool = Field(description="The candidate certain as well")

class MeterialsEnum(str,Enum):
    metallic = "금속"
    dirt = "흙"
    porcelain = "도자기"
    stone = "돌"
    glass_jewelry = "유리/보석" 
    grass = "풀"
    wood = "나무"
    bone_horn_clamshell = "뼈/뿔/조개"
    paper = "종이"
    leather_fur = "가죽/털"
    fabric = "섬유"
    seed = "씨앗"
    mineral = "광물"
    fossil = "화석"
    rubber = "고무"
    najeon = "칠기"
    etc = "기타"
    
class Material(BaseModel):
    name: MeterialsEnum = Field(description="Material used in the relic.")
    certainty: bool = Field(description="Is it certain, if so True on first name")
    candidate: Optional[MeterialsEnum] = Field(description="A candidate material used in the relic.")
    candidate_certainty: bool = Field(description="The candidate certain as well")
    
    
    
class PurposeEnum(str,Enum):
    
    etc_purpoe = "기타자료"
    media = "미디어"
    science_tech = "과학기술"
    medical = "보건의료"
    military = "군사"
    art_culture ="문화예술"
    religion = "종교신앙"
    society = "사회생활"
    traditional_science = "전통과학"
    transportation_communication = "교통/통신"
    industry_livelihood = "산업/생업"
    residential = "주생활"
    diet = "식생활"
    clothing = "의생활"

class Purpose(BaseModel):
    name: PurposeEnum = Field(description="Type of the relic.")
    certainty: bool = Field(description="Is it certain, if so True on first name")
    candidate: Optional[PurposeEnum] = Field(description="A candidate type of the relic.")
    candidate_certainty: bool = Field(description="If you are certain about the candidate, mark as true")
    
    
    
    
class RelicName(BaseModel):
    name:str = Field("Name of the Relic")
    certainty: bool = Field(description="Is name of the relic certain, if so True on certanity.")
    candidate: Optional[str] = Field("A candidate name of the relic")
    candidate_certainty: bool = Field(description="If you are certain about the candidate, mark as true ")


class Purpose_descriptions:
    purpose_descriptions = {
        "기타자료": "Other purposes not specified in the listed categories.",
        "미디어": "Materials used for recording, storing, or transmitting information such as manuscripts, inscriptions, prints, or audiovisual media.",
        "과학기술": "Objects related to scientific knowledge, experimentation, inventions, and technological advancements.",
        "보건의료": "Artifacts associated with medicine, healing practices, pharmaceuticals, and public health.",
        "군사": "Items connected to warfare, defense, weapons, armor, and military organization.",
        "문화예술": "Objects used in creative expression such as painting, sculpture, music, theater, and literature.",
        "종교신앙": "Artifacts related to spiritual practices, rituals, sacred objects, temples, and religious beliefs.",
        "사회생활": "Objects reflecting daily social activities, governance, law, education, and community life.",
        "전통과학": "Items linked to indigenous knowledge systems, astronomy, calendrical science, and traditional natural philosophy.",
        "교통/통신": "Artifacts related to movement of people and goods, or transmission of information, such as vehicles, ships, letters, and signaling devices.",
        "산업/생업": "Objects associated with production, agriculture, craftsmanship, labor, and livelihood activities.",
        "주생활": "Items used in housing, domestic architecture, furniture, and household management.",
        "식생활": "Artifacts related to food preparation, cooking, storage, and consumption.",
        "의생활": "Objects related to clothing, fashion, textiles, and accessories for personal use."
    }
    

    
class Material_descriptions:
    material_descriptions = {
    "금속": "Metallic materials like gold, silver, bronze, iron, etc.",
    "흙": "Clay or earth-based materials, often used for pottery or earthenware.",
    "도자기": "Ceramic materials, including porcelain, celadon, and stoneware.",
    "돌": "Stone materials such as granite, marble, jade, or various rocks.",
    "유리/보석": "Glass or gemstone materials, including precious and semi-precious stones.",
    "풀": "Plant-based materials like straw, reeds, or other grasses.",
    "나무": "Wood or timber materials.",
    "뼈/뿔/조개": "Materials derived from animal bones, horns, or seashells.",
    "종이": "Paper-based materials.",
    "가죽/털": "Leather or fur materials.",
    "섬유": "Textile materials like silk, cotton, hemp, etc.",
    "씨앗": "Seeds or plant kernels.",
    "광물": "Mineral substances.",
    "화석": "Fossilized remains.",
    "고무": "Rubber materials.",
    "칠기": "Lacquered ware, often made from wood and coated with lacquer. 나전칠기.",
    "기타": "Other materials not specified in the above categories."
}
    
     
class K_nation_descriptions:
    korean_nations_descriptions = {
  "구석기": "구석기 시대 — 수렵·채집 사회로, 주먹도끼와 같은 뗀석기를 사용하였다.",
  "중석기": "중석기 시대 — 구석기에서 신석기로 넘어가는 과도기. 보다 정교하고 작은 석기가 사용되었다.",
  "신석기": "신석기 시대 — 농경이 시작되고, 토기 제작과 정착 생활이 이루어졌다.",
  "청동기": "청동기 시대 — 청동 도구와 무기의 사용이 시작되며, 계급 사회와 성곽 취락이 등장하였다.",
  "초기철기": "초기 철기 시대 — 철제 도구와 무기가 등장해 농업 기술과 전쟁이 발달하였다. 부여·진국 등의 국가가 포함된다.",
  "원삼국": "원삼국 시대 — 삼국 성립 이전, 부여·옥저·동예 등 여러 소국이 존재하던 과도기.",
  "낙랑": "낙랑군 — 고조선 멸망 후 한나라가 한반도에 설치한 군현 가운데 하나.",
  "고구려": "고구려 — 한반도 북부와 만주를 중심으로 한 삼국 중 하나로, 강력한 군사력과 광대한 영토를 자랑하였다.",
  "백제": "백제 — 한반도 남서부의 삼국 중 하나로, 해상 교역과 선진 문화를 꽃피운 나라.",
  "신라": "신라 — 한반도 남동부의 삼국 중 하나로, 후에 삼국을 통일하였다.",
  "가야": "가야 — 한반도 남부의 소국 연맹으로, 우수한 철기 문화로 유명하다.",
  "삼국": "삼국 시대 — 고구려·백제·신라가 대립하던 시기.",
  "통일신라": "통일 신라 — 신라가 백제와 고구려를 정복하고 한반도 대부분을 통일한 시기.",
  "발해": "발해 — 고구려의 북방 지역을 계승해 세운 왕국으로, 해동성국이라 불렸다.",
  "라말여초": "신라 말기~고려 초 — 통일 신라가 쇠퇴하고 고려가 등장하는 과도기.",
  "고려": "고려 — 불교 문화와 청자 도자기, 북방 민족의 침략 방어로 유명한 왕조.",
  "려말선초": "고려 말기~조선 초 — 고려가 쇠망하고 조선이 건국되는 격동기.",
  "조선": "조선 — 유교를 통치 이념으로 삼은 왕조로, 500여 년간 지속되며 문화와 학문이 발달했다.",
  "대한제국": "대한제국 — 조선의 고종이 선포한 근대 국가로, 개혁과 근대화를 추진했으나 일제에 병합되었다.",
  "일제강점": "일제 강점기 — 일본 제국에 의해 한반도가 식민지 지배를 받던 시기.",
  "광복이후": "광복 이후 — 1945년 해방 이후, 한반도 분단과 한국 전쟁 등을 거친 현대사.",
  "2000년 이후": "2000년 이후 — 21세기 현대 한국 사회를 의미한다.",
  "시대미상": "시대 미상 — 특정한 시대를 알 수 없을 때 사용된다."
}