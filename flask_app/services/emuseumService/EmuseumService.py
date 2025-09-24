

from typing import Any, Dict, List
from dotenv import load_dotenv
from flask import current_app

from flask_app.dto.EmuseumDTO import DetailInfo, ImageItem, ItemDetail, RelatedItem
load_dotenv()
import os

import xmltodict

import requests



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
    'imgThumUriM': 'imgThumUriM', 'imgThumUriL': 'imgThumUriL'
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
        
        # Build a dictionary for the ItemDetail model using the mapping
        item_data_for_model = {dto_field: parsed_item.get(api_key) 
                               for dto_field, api_key in item_mapping.items()}
        
        # Add the special purpose and material fields
        item_data_for_model['purposeName'] = purpose_name
        item_data_for_model['materialName'] = material_name
        
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

    
    def _makeRequests(self,apiRoute:str,params:Dict,pageNo:int=1,numOfRows:int=10)->dict:
        # makes requets and returns the content. 
        params["serviceKey"]= self.apiKey
        params["pageNo"] = pageNo
        params["numOfRows"] = numOfRows
        
        
        response=requests.get(self.emuseumURL+apiRoute,params)
        xml_content = response.content
        json_data = xmltodict.parse(xml_content)
        
        
        items = json_data.get('result', {}).get('list', {}).get('data', [])
        dict_items = []
        for item_obj in items:
            if 'item' in item_obj:
                dict_items.append(self._item_list_to_dict(item_obj['item']))
        return dict_items
        
    def _makeRequests_detail(self,apiRoute:str,params:Dict,pageNo:int=1,numOfRows:int=1)->dict:
        # makes requets and returns the content. 
        params["serviceKey"]= self.apiKey
        params["pageNo"] = pageNo
        params["numOfRows"] = numOfRows
        
        
        response=requests.get(self.emuseumURL+apiRoute,params)
        xml_content = response.content
        json_data = xmltodict.parse(xml_content)

        
        return json_data
        
        
    
    
    
    
    # I might need a query builder. 
    def getItemsByKeywords(self,name:str=None,author:str=None,
                           id:str=None,museumCode:str=None,
                           nationalityCode:str=None,meterialCode:str=None,
                           purposeCode:str=None,sizeRangeCode:str=None,
                           placeLandCode:str=None,designationCode:str=None,
                           indexWord:str=None,pageNo:int=1,numOfRows:int=20):
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
        if meterialCode:
            params['meterialCode'] = meterialCode
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

        apiRoute = "/relic/list" 
        return self._makeRequests(apiRoute, params,pageNo=pageNo,numOfRows=numOfRows)
            
    def getDetailInfo(self,id:str)->DetailInfo:
        """_summary_

        Args:
            id (str): id of the relic item from 'Emuseum'

        Returns:
            dict: detailed json from the api.
        """
        
        params={}
        if id:
            params['id'] = id
        apiRoute = "/relic/detail" 
        
        json_data = self._makeRequests_detail(apiRoute, params,pageNo=1,numOfRows=10)
        etail_info_dto=None
        try:
            detail_info_dto = create_detail_info_dto_with_mapping(
                json_data,
                item_mapping,
                image_mapping,
                related_mapping,
                purpose_priority,
                material_priority
            )
            current_app.logger.info(f"Successfully created DetailInfo DTO with dynamic key mapping:")
            current_app.logger.info(detail_info_dto.model_dump_json(indent=2))
            return detail_info_dto
            
        except Exception as e:
            current_app.logger.info(f"An error occurred: {e}")
            return None

        
        
          
                        
                        


emuseum = EmuseumAPIService()
            

