

# Select only needed info from api and save into the DTO below.



from typing import List
from pydantic import BaseModel
from typing import Generic, TypeVar


class ImageItem(BaseModel):
    imgUri:str | None
    imgThumUriS:str | None
    imgThumUriM:str | None
    imgThumUriL:str | None

class RelatedItem(BaseModel):
    reltId:str
    reltRelicName:str
    reltMuseumFullName:str

class ItemDetail(BaseModel):
    # for all subjectName (museumName, purposeName, materialName)
    # if name not found use Code and translate into Names. with flask_app.util.MuseumCodeTranslator
    
    nameKr:str # name of the object. if 'name' does not exist use name.
    id:str # id of the object. PS0100100101101235600000
    museumName1:str # 국립, 사립 ... 
    museumName2:str # 국립중앙박물관
    # skip museumName3
    
    desc:str # description
    
    # try to use purposeName3
    # if not found use parent
    purposeName:str | None
    
    # Use materialName3.
    # If no matericalCode3, use materialCode2, if not found use materialCode1
    materialName:str | None
    
    imgUri:str | None
    imgThumUriS:str | None
    imgThumUriM:str | None
    imgThumUriL:str | None
    

class DetailInfo(BaseModel):
    item:ItemDetail
    imageList:List[ImageItem] | None 
    related:RelatedItem | None
    
class DetailInfoList(BaseModel):
    detail_info_list:List[DetailInfo]

    
    
class BriefInfo(BaseModel):
    nameKr:str   # Use name if nameKr not found
    id:str
    imgUri:str | None
    imgThumUriS:str | None
    imgThumUriM:str | None
    imgThumUriL:str | None
    museumName1:str
    museumName2:str
    museumName3:str
    
    # Must be converted from Code.
    nationalityName:str | None
    purposeName:str | None
    materialName:str | None


class BriefList(BaseModel):
    totalCount:int
    brief_info_list:List[BriefInfo]
    

T = TypeVar('T')
class APIResponse(BaseModel,Generic[T]):
    message:str | None
    userId:int | None
    searchQueryLeft:int | None  # Placeholder for now
    data:T  # T can be either BriefList or DetailInfoList
    
    
    