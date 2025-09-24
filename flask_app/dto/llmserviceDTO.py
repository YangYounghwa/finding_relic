







from enum import Enum
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
    baekje = "벡제"
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
    

# Step 2: Define a Pydantic model to hold the parsed result
class Nations(BaseModel):
    name: KoreanNationsEnum = Field(description="Historic era/nation names in Korean history.")

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
    
class Meterial(BaseModel):
    name: MeterialsEnum = Field(description="Material used in the relic.")
    
    
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
    "구석기": "Paleolithic Age. Hunter-gatherer society, characterized by the use of chipped stone tools.",
    "중석기": "Mesolithic Age. A transitional period between the Paleolithic and Neolithic, with smaller, more refined stone tools.",
    "신석기": "Neolithic Age. The beginning of agriculture, pottery, and settled village life.",
    "청동기": "Bronze Age. The era when bronze tools and weapons were first used, leading to the emergence of class societies and fortified settlements.",
    "초기철기": "Early Iron Age. Iron tools and weapons begin to appear, leading to more advanced agricultural techniques and warfare. This era includes nations like Buyeo and Jin.",
    "원삼국": "Proto–Three Kingdoms period. A transitional time with many small tribal states, including Buyeo, Okjeo, and Dongye, before the formal establishment of the Three Kingdoms.",
    "낙랑": "Nangnang Commandery. A Chinese military commandery established in the Korean peninsula after the fall of Gojoseon.",
    "고구려": "Goguryeo. One of the Three Kingdoms, known for its expansive territory and military strength, located in the northern part of the peninsula.",
    "백제": "Baekje. One of the Three Kingdoms, located in the southwestern part of the peninsula, known for its rich culture and maritime trade.",
    "신라": "Silla. One of the Three Kingdoms, located in the southeastern part of the peninsula, which eventually unified the peninsula.",
    "가야": "Gaya. A confederacy of small city-states in the southern peninsula, known for its iron production.",
    "삼국": "Three Kingdoms period. The era of the three rival kingdoms: Goguryeo, Baekje, and Silla.",
    "통일신라": "Unified Silla. The period after Silla conquered Baekje and Goguryeo, unifying most of the Korean peninsula.",
    "발해": "Balhae. A kingdom established in the northern parts of the former Goguryeo territory.",
    "라말여초": "Late Silla to Early Goryeo. A period of transition and political instability marked by the decline of Unified Silla and the rise of Goryeo.",
    "고려": "Goryeo. A dynasty known for its Buddhist culture, celadon pottery, and defense against invasions from the North.",
    "려말선초": "Late Goryeo to Early Joseon. A time of political and social upheaval, leading to the collapse of Goryeo and the founding of the Joseon dynasty.",
    "조선": "Joseon. The last dynastic kingdom, known for its strong Confucian influence, rich culture, and isolationist policies.",
    "대한제국": "Korean Empire. A short-lived empire established by King Gojong of Joseon, marking a period of modernization before Japanese colonization.",
    "일제강점": "Japanese Rule. The period when Korea was under the colonial rule of the Japanese Empire.",
    "광복이후": "Post-Liberation. The period after the end of Japanese colonial rule in 1945, including the division of Korea and the Korean War.",
    "2000년 이후": "After 2000. Refers to the modern era of the 21st century.",
    "시대미상": "Age Unknown. Used when the text doesn't provide enough information to identify a specific historical period."
}