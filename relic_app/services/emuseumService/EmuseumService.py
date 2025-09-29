

from typing import Any, Dict, List
from dotenv import load_dotenv
from flask import current_app

from relic_app.dto.EmuseumDTO import BriefInfo, BriefList, DataForVector, DetailInfo, ImageItem, ItemDetail, RelatedItem
from relic_app.services.embeddingService.EmbeddingService import embedding_service

load_dotenv()
import os

import xmltodict

from relic_app.util.MuseumCodeTranslator import materialConverter, purposeConverter, nationalityConverter

import requests
import logging
logger = logging.getLogger(__name__)



# Helper function.
def parse_list_or_dict_of_items(data):
    """Parses a data structure that can be either a list of dictionaries or a single dictionary."""
    parsed_list = []
    
    if isinstance(data, list):
        for item_dict in data:
            if isinstance(item_dict.get('item'), list):
                parsed_item = {item['@key']: item['@value'] for item in item_dict['item']}
                parsed_list.append(parsed_item)
    
    elif isinstance(data, dict):
        if isinstance(data.get('item'), list):
            parsed_item = {item['@key']: item['@value'] for item in data['item']}
            parsed_list.append(parsed_item)
            
    return parsed_list

item_mapping = {
    'nameKr': 'nameKr', 'id': 'id', 'museumName1': 'museumName1',
    'museumName2': 'museumName2', 'desc': 'desc',
    'imgUri': 'imgUri', 'imgThumUriS': 'imgThumUriS',
    'imgThumUriM': 'imgThumUriM', 'imgThumUriL': 'imgThumUriL',
    'nationalityName1': 'nationalityName1', 'nationalityName2': 'nationalityName2',
}
image_mapping = {
    'imgUri': 'imgUri', 'imgThumUriS': 'imgThumUriS',
    'imgThumUriM': 'imgThumUriM', 'imgThumUriL': 'imgThumUriL'
}
related_mapping = {
    'reltId': 'reltId', 'reltRelicName': 'reltRelicName',
    'reltMuseumFullName': 'reltMuseumFullName'
}
purpose_priority = ['purposeName3', 'purposeName2', 'purposeName1']
material_priority = ['materialName3', 'materialName2', 'materialName1']

def create_detail_info_dto_with_mapping(
    raw_json_data: dict,
    item_mapping: Dict[str, str],
    image_mapping: Dict[str, str],
    related_mapping: Dict[str, str],
    purpose_priority: List[str],
    material_priority: List[str]
) -> DetailInfo:
    """
    Parses raw API JSON data and fits it into Pydantic DTO models using dynamic key mapping.

    Args:
        raw_json_data: A dictionary representing the raw JSON response.
        item_mapping: A dict to map API keys to ItemDetail fields.
        image_mapping: A dict to map API keys to ImageItem fields.
        related_mapping: A dict to map API keys to RelatedItem fields.
        purpose_priority: A list of ordered keys for the purposeName.
        material_priority: A list of ordered keys for the materialName.

    Returns:
        A DetailInfo Pydantic model instance.
    """
    # Safely extract raw data sections
    items_data = raw_json_data.get('result', {}).get('list', {}).get('data', {})
    image_items_data = raw_json_data.get('result', {}).get('imageList', {}).get('list', {}).get('data', [])
    related_items_data = raw_json_data.get('result', {}).get('relationList', {}).get('list', {}).get('data', {})

    # Parse raw data into usable dictionaries
    parsed_items_list = parse_list_or_dict_of_items(items_data)
    parsed_image_items_list = parse_list_or_dict_of_items(image_items_data)
    parsed_related_items_list = parse_list_or_dict_of_items(related_items_data)

    item_detail_instance = None
    image_list_instances = None
    related_item_instance = None

    # 1. Create the ItemDetail object using the provided mapping
    if parsed_items_list:
        parsed_item = parsed_items_list[0]
        
        # Use a function to find the first existing key from a priority list
        def find_first_existing_key(data_dict: dict, keys: List[str]) -> Any:
            for key in keys:
                if key in data_dict:
                    return data_dict.get(key)
            return None

        # Dynamically set purposeName and materialName based on priority
        purpose_name = find_first_existing_key(parsed_item, purpose_priority)
        material_name = find_first_existing_key(parsed_item, material_priority)
        glsv = parsed_item.get('glsv')
        
        # Build a dictionary for the ItemDetail model using the mapping
        item_data_for_model = {dto_field: parsed_item.get(api_key) 
                               for dto_field, api_key in item_mapping.items()}
        
        # Add the special purpose and material fields
        item_data_for_model['purposeName'] = purpose_name
        item_data_for_model['materialName'] = material_name
        item_data_for_model['glsv'] = glsv
        
        item_detail_instance = ItemDetail(**item_data_for_model)

    # 2. Create the list of ImageItem objects using the provided mapping
    if parsed_image_items_list:
        image_list_instances = []
        for image_data in parsed_image_items_list:
            image_item_data_for_model = {dto_field: image_data.get(api_key)
                                         for dto_field, api_key in image_mapping.items()}
            image_list_instances.append(ImageItem(**image_item_data_for_model))

    # 3. Create the RelatedItem object using the provided mapping
    if parsed_related_items_list:
        related_data = parsed_related_items_list[0]
        related_item_data_for_model = {dto_field: related_data.get(api_key)
                                       for dto_field, api_key in related_mapping.items()}
        related_item_instance = RelatedItem(**related_item_data_for_model)

    # 4. Construct the final DTO
    if item_detail_instance:
        return DetailInfo(
            item=item_detail_instance,
            imageList=image_list_instances,
            related=related_item_instance
        )
    else:
        # Fallback for when no main item data is found
        return DetailInfo(item=ItemDetail(id=""), imageList=None, related=None)
    
    
class EmuseumAPIService:
    
    
    
    
    def __init__(self):
        self.emuseumURL = os.getenv('EMUSESUM_URL')
        #self.apiKey = os.getenv('EMUSEUM_KEY_ENCODED')
        self.apiKey = os.getenv('EMUSEUM_KEY_DECODED')
        
        pass 
    
    
    
    def _item_list_to_dict(self, item_list):
        """
        Converts a list of {'@key': ..., '@value': ...} dicts to a single dictionary.
        """
        return {entry['@key']: entry['@value'] for entry in item_list if '@key' in entry and '@value' in entry}

    
    def _makeRequests(self, apiRoute: str, params: Dict, pageNo: int = 1, numOfRows: int = 10) -> tuple[list, int] | None:
        # makes requets and returns the content. 
        params["serviceKey"] = self.apiKey
        params["pageNo"] = pageNo
        params["numOfRows"] = numOfRows
        
        try:
            response = requests.get(self.emuseumURL + apiRoute, params, timeout=10) # Added timeout
            response.raise_for_status()  # Raise an exception for bad status codes
            xml_content = response.content
            json_data = xmltodict.parse(xml_content)
        except (requests.exceptions.RequestException, xmltodict.expat.ExpatError) as e:
            logger.error(f"API request or XML parsing failed: {e}")
            return None # Return None on failure

        # DEBUG LINE
        logger.info(json_data.keys)
        
        # TODO : manage errors when expected key does not exist.
        
        result_data = json_data.get('result', {})
        if not isinstance(result_data, dict):
            logger.warning(f"API response missing 'result' dictionary.")
            return [],0
        list_data = result_data.get('list')
        if not isinstance(list_data, dict):
            logger.warning(f"API response missing 'list' dictionary. Response: {json_data}")
            return [], 0

        items = list_data.get('data', [])
        total_count_str = result_data.get('totalCount', '0')

        total_count = int(total_count_str) if total_count_str.isdigit() else 0
        
        dict_items = []
        # API can return a dict for a single item or a list for multiple items.
        if isinstance(items, list):
            for item_obj in items:
                if 'item' in item_obj:
                    dict_items.append(self._item_list_to_dict(item_obj['item']))
        elif isinstance(items, dict):
            if 'item' in items:
                dict_items.append(self._item_list_to_dict(items['item']))
        logger.info(f"list received. total count : {total_count}")
        return dict_items, total_count
    
    
    
    def _makeRequests_detail(self,apiRoute:str,params:Dict,pageNo:int=1,numOfRows:int=1)->dict:
        # makes requets and returns the content. 
        params["serviceKey"]= self.apiKey
        params["pageNo"] = pageNo
        params["numOfRows"] = numOfRows
        
        
        response=requests.get(self.emuseumURL+apiRoute,params)
        xml_content = response.content
        json_data = xmltodict.parse(xml_content)
        
        #
        

        
        return json_data
        
        
    
    
    
    
    # I might need a query builder. 
    def getItemsByKeywords(self,name:str=None,author:str=None,
                           id:str=None,museumCode:str=None,
                           nationalityCode:str=None,materialCode:str=None,
                           purposeCode:str=None,sizeRangeCode:str=None,
                           placeLandCode:str=None,designationCode:str=None,
                           indexWord:str=None,pageNo:int=1,numOfRows:int=20)->BriefList:
        params={}
        if name:
            params['name'] = name
        if author:
            params['author'] = author
        if id:
            params['id'] = id
        if museumCode:
            params['museumCode'] = museumCode
        if nationalityCode:
            params['nationalityCode'] = nationalityCode
        if materialCode:
            params['materialCode'] = materialCode
        if purposeCode:
            params['purposeCode'] = purposeCode
        if sizeRangeCode:
            params['sizeRangeCode'] = sizeRangeCode
        if placeLandCode:
            params['placeLandCode'] = placeLandCode
        if designationCode:
            params['designationCode'] = designationCode
        if indexWord:
            params['indexWord'] = indexWord
            
        logger.debug(f"params:{params}")

        apiRoute = "/relic/list" 
        
        # Call _makeRequests and handle potential failure
        request_result = self._makeRequests(apiRoute, params, pageNo=pageNo, numOfRows=numOfRows)
        if request_result is None:
            logger.warning("API call failed or returned no data. Returning empty BriefList.")
            return BriefList(totalCount=0, brief_info_list=[])
        
        raw_items, total_count = request_result
        
        brief_info_list = []
        
        
        for item in raw_items:
            # Convert codes to human-readable names using the converters
            nationality_name = nationalityConverter.code_to_nameKr(item.get('nationalityCode'))
            
            # Slice purposeCode into first 10 chars. 
            purpose_code = item.get('purposeCode')
            purposeCodeSlice = purpose_code[:10] if purpose_code else None
            purpose_name = purposeConverter.code_to_nameKr(purposeCodeSlice)
            material_name = materialConverter.code_to_nameKr(item.get('materialCode'))
            
            brief_info = BriefInfo(
                nameKr=item.get('nameKr', item.get('name')), # As per DTO, use 'name' if 'nameKr' not found
                id=item.get('id'),
                imgUri=item.get('imgUri'),
                imgThumUriS=item.get('imgThumUriS'),
                imgThumUriM=item.get('imgThumUriM'),
                imgThumUriL=item.get('imgThumUriL'),
                museumName1=item.get('museumName1'),
                museumName2=item.get('museumName2'),
                museumName3=item.get('museumName3'),
                nationalityName=nationality_name,
                purposeName=purpose_name,
                materialName=material_name,
            )
            brief_info_list.append(brief_info)
            
        return BriefList(totalCount=len(brief_info_list), brief_info_list=brief_info_list)
    
    
    # TODO : Add error handlling when receiving empty data from emuseum 
    def getDetailInfo(self,id:str)->DetailInfo:
        """_summary_

        Args:
            id (str): id of the relic item from 'Emuseum'

        Returns:
            dict: detailed json from the api.
        """
        logger.info(f"getDetailInfo called with id: {id}") 
        params={}
        if id:
            params['id'] = id
        apiRoute = "/relic/detail"
        logger.info(params)
        
        json_data = self._makeRequests_detail(apiRoute, params,pageNo=1,numOfRows=10)
        logger.info("getDetailInfo received json data.")
        logger.info(json_data.keys)
        detail_info_dto=None
        try:
            detail_info_dto:DetailInfo = create_detail_info_dto_with_mapping(
                json_data,
                item_mapping,
                image_mapping,
                related_mapping,
                purpose_priority,
                material_priority
            )
            logger.info(f"Successfully created DetailInfo DTO with dynamic key mapping:")
            # logger.info(detail_info_dto.model_dump_json(indent=2))
            # parse detail_info_dto.item into DataForVector
            
            singleItem:ItemDetail = detail_info_dto.item
            if(singleItem.glsv == 1):
                dataForVector:DataForVector = DataForVector(relicId=singleItem.id,
                    desc=singleItem.desc,
                    purposeName=singleItem.purposeName,
                    materialName=singleItem.materialName,
                    nationalityName=singleItem.nationalityName1)
                embedding_service.save_data_for_vector(dataForVector)
                
            return detail_info_dto
            
        except Exception as e:
            logger.info(f"An error occurred: {e}")
            return None

        
        
          
                        
                        


emuseum = EmuseumAPIService()
            

