

# Select only needed info from api and save into the DTO below.



from typing import List
from pydantic import BaseModel, Field
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
    
    
    nationalityName1:str | None # 한국
    nationalityName2:str | None # 조선
     
    imgUri:str | None
    imgThumUriS:str | None
    imgThumUriM:str | None
    imgThumUriL:str | None

    glsv : int | None = Field(description="Korea Gov open data license version.") # -- added 20250929    

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

    def add_brief_list(self, new_brief_list: 'BriefList'):
        """
        Appends items from another BriefList, ensuring uniqueness based on BriefInfo.id.
        """
        existing_ids = {info.id for info in self.brief_info_list}
        
        for new_info in new_brief_list.brief_info_list:
            if new_info.id not in existing_ids:
                self.brief_info_list.append(new_info)
                existing_ids.add(new_info.id)
        
        self.totalCount = len(self.brief_info_list)

T = TypeVar('T')
class APIResponse(BaseModel,Generic[T]):
    message:str | None
    success:bool
    userId:int | None
    # searchQueryLeft:int | None  # Placeholder for now
    data:T  # T can be either BriefList or DetailInfoList
    
class DataForVector(BaseModel):
    """_summary_
    Save the data only if 'glsv' == 1  
    This is legal restriction of 공공누리.

    Args:
        BaseModel (_type_): _description_
    """
    relicId : str
    desc : str = Field(description="Will be vectorized and saved to vector DB")
    materialName : str = Field(description="Use materialName depth of 3.")
    purposeName : str = Field(description="Use purposeName depth of 3.")
    nationalityName : str = Field(description="Nation Name")
    
    
    
    
    