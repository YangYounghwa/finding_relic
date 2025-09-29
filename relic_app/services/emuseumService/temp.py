# relic_app/services/emuseumService/EmuseumService.py

from typing import Any, Dict, List
from dotenv import load_dotenv
from flask import current_app
import json # Import json for pretty printing
from pprint import pformat # Import pformat for pretty printing

from relic_app.dto.EmuseumDTO import BriefInfo, BriefList, DataForVector, DetailInfo, ImageItem, ItemDetail, RelatedItem
from relic_app.services.embeddingService.EmbeddingService import embedding_service

load_dotenv()
import os

import xmltodict

from relic_app.util.MuseumCodeTranslator import materialConverter, purposeConverter, nationalityConverter

import requests
import logging
logger = logging.getLogger(__name__)


# (Helper function parse_list_or_dict_of_items remains the same)
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

# (Mappings remain the same)
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
    (Function description remains the same)
    """
    # Safely extract raw data sections with added logging
    try:
        items_data = raw_json_data.get('result', {}).get('list', {}).get('data', {})
        image_items_data = raw_json_data.get('result', {}).get('imageList', {}).get('list', {}).get('data', [])
        related_items_data = raw_json_data.get('result', {}).get('relationList', {}).get('list', {}).get('data', {})
        logger.debug("Successfully extracted main data sections from raw JSON.")
    except AttributeError as e:
        logger.error(f"Failed to extract main data sections due to unexpected structure: {e}")
        logger.error(f"Raw JSON data that caused the error:\n{pformat(raw_json_data)}")
        return DetailInfo(item=ItemDetail(id=""), imageList=None, related=None)


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
        
        def find_first_existing_key(data_dict: dict, keys: List[str]) -> Any:
            for key in keys:
                if key in data_dict:
                    return data_dict.get(key)
            return None

        purpose_name = find_first_existing_key(parsed_item, purpose_priority)
        material_name = find_first_existing_key(parsed_item, material_priority)
        glsv = parsed_item.get('glsv')
        
        item_data_for_model = {dto_field: parsed_item.get(api_key) 
                               for dto_field, api_key in item_mapping.items()}
        
        item_data_for_model['purposeName'] = purpose_name
        item_data_for_model['materialName'] = material_name
        item_data_for_model['glsv'] = glsv
        
        # **Robustness Improvement**: Ensure required fields are present before creating the model
        if 'id' not in item_data_for_model or not item_data_for_model['id']:
             logger.error("'id' is missing from parsed item data. Cannot create ItemDetail.")
             return DetailInfo(item=ItemDetail(id=""), imageList=None, related=None)

        item_detail_instance = ItemDetail(**item_data_for_model)
        logger.debug(f"Successfully created ItemDetail instance for id: {item_detail_instance.id}")


    # 2. Create the list of ImageItem objects using the provided mapping
    if parsed_image_items_list:
        image_list_instances = []
        for image_data in parsed_image_items_list:
            image_item_data_for_model = {dto_field: image_data.get(api_key)
                                         for dto_field, api_key in image_mapping.items()}
            image_list_instances.append(ImageItem(**image_item_data_for_model))
        logger.debug(f"Created {len(image_list_instances)} ImageItem instances.")


    # 3. Create the RelatedItem object using the provided mapping
    if parsed_related_items_list:
        related_data = parsed_related_items_list[0]
        related_item_data_for_model = {dto_field: related_data.get(api_key)
                                       for dto_field, api_key in related_mapping.items()}
        related_item_instance = RelatedItem(**related_item_data_for_model)
        logger.debug("Successfully created RelatedItem instance.")


    # 4. Construct the final DTO
    if item_detail_instance:
        return DetailInfo(
            item=item_detail_instance,
            imageList=image_list_instances,
            related=related_item_instance
        )
    else:
        # Fallback for when no main item data is found
        logger.warning("No main item data was found in the API response. Returning an empty DetailInfo.")
        return DetailInfo(item=ItemDetail(id=""), imageList=None, related=None)


class EmuseumAPIService:
    
    def __init__(self):
        self.emuseumURL = os.getenv('EMUSESUM_URL')
        self.apiKey = os.getenv('EMUSEUM_KEY_DECODED')
        
        pass 
    
    def _item_list_to_dict(self, item_list):
        return {entry['@key']: entry['@value'] for entry in item_list if '@key' in entry and '@value' in entry}

    
    def _makeRequests(self, apiRoute: str, params: Dict, pageNo: int = 1, numOfRows: int = 10) -> tuple[list, int] | None:
        # (This method remains largely the same, but you could add similar logging if needed)
        params["serviceKey"] = self.apiKey
        params["pageNo"] = pageNo
        params["numOfRows"] = numOfRows
        
        try:
            response = requests.get(self.emuseumURL + apiRoute, params, timeout=10)
            response.raise_for_status()
            xml_content = response.content
            json_data = xmltodict.parse(xml_content)
        except (requests.exceptions.RequestException, xmltodict.expat.ExpatError) as e:
            logger.error(f"API request or XML parsing failed: {e}")
            return None

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
        if isinstance(items, list):
            for item_obj in items:
                if 'item' in item_obj:
                    dict_items.append(self._item_list_to_dict(item_obj['item']))
        elif isinstance(items, dict):
            if 'item' in items:
                dict_items.append(self._item_list_to_dict(items['item']))
        logger.info(f"list received. total count : {total_count}")
        return dict_items, total_count
    
    
    def _makeRequests_detail(self, apiRoute: str, params: Dict, pageNo: int = 1, numOfRows: int = 1) -> dict:
        """
        Makes a request to the detail API, with improved error handling and logging.
        """
        params["serviceKey"] = self.apiKey
        params["pageNo"] = pageNo
        params["numOfRows"] = numOfRows
        
        try:
            response = requests.get(self.emuseumURL + apiRoute, params, timeout=15)
            # **Logging Improvement**: Log the raw response text before parsing
            logger.debug(f"Raw XML response for detail request:\n{response.text}")
            response.raise_for_status()
            xml_content = response.content
            # **Robustness Improvement**: Wrap parsing in a try...except block
            json_data = xmltodict.parse(xml_content)
            # **Logging Improvement**: Use pformat for pretty logging of the parsed JSON
            logger.debug(f"Successfully parsed XML to JSON:\n{pformat(json_data)}")
            return json_data
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
        except requests.exceptions.RequestException as req_err:
            logger.error(f"A request error occurred: {req_err}")
        except xmltodict.expat.ExpatError as xml_err:
            logger.error(f"XML parsing failed: {xml_err}")
            logger.error(f"The raw response that failed to parse was:\n{response.text}")
        except Exception as e:
            logger.error(f"An unexpected error occurred in _makeRequests_detail: {e}")
            
        return {} # Return an empty dict on failure


    def getItemsByKeywords(self,name:str=None,author:str=None,
                           id:str=None,museumCode:str=None,
                           nationalityCode:str=None,materialCode:str=None,
                           purposeCode:str=None,sizeRangeCode:str=None,
                           placeLandCode:str=None,designationCode:str=None,
                           indexWord:str=None,pageNo:int=1,numOfRows:int=20)->BriefList:
        # (This method remains the same)
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
        
        request_result = self._makeRequests(apiRoute, params, pageNo=pageNo, numOfRows=numOfRows)
        if request_result is None:
            logger.warning("API call failed or returned no data. Returning empty BriefList.")
            return BriefList(totalCount=0, brief_info_list=[])
        
        raw_items, total_count = request_result
        
        brief_info_list = []
        
        
        for item in raw_items:
            nationality_name = nationalityConverter.code_to_nameKr(item.get('nationalityCode'))
            
            purpose_code = item.get('purposeCode')
            purposeCodeSlice = purpose_code[:10] if purpose_code else None
            purpose_name = purposeConverter.code_to_nameKr(purposeCodeSlice)
            material_name = materialConverter.code_to_nameKr(item.get('materialCode'))
            
            brief_info = BriefInfo(
                nameKr=item.get('nameKr', item.get('name')),
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
    
    
    def getDetailInfo(self,id:str)->DetailInfo:
        """
        Retrieves and parses detailed information for a specific relic ID.
        Now with enhanced logging and error handling.
        """
        logger.info(f"getDetailInfo called with id: {id}") 
        params={'id': id} if id else {}
        if not params:
            logger.error("getDetailInfo called without an ID.")
            return None
            
        apiRoute = "/relic/detail"
        
        json_data = self._makeRequests_detail(apiRoute, params, pageNo=1, numOfRows=1)
        
        # **Robustness Improvement**: Check if json_data is empty (which indicates a failure in the request)
        if not json_data:
            logger.error(f"Failed to get any data from _makeRequests_detail for id: {id}")
            return None
        
        logger.info("Received JSON data, proceeding with DTO creation.")
        
        try:
            detail_info_dto:DetailInfo = create_detail_info_dto_with_mapping(
                json_data,
                item_mapping,
                image_mapping,
                related_mapping,
                purpose_priority,
                material_priority
            )
            
            if not detail_info_dto or not detail_info_dto.item or not detail_info_dto.item.id:
                 logger.warning(f"create_detail_info_dto_with_mapping returned an empty DTO for id: {id}")
                 return None

            logger.info(f"Successfully created DetailInfo DTO for relic id: {detail_info_dto.item.id}")
            
            singleItem:ItemDetail = detail_info_dto.item
            # Check for glsv and save data for vector embedding if applicable
            if(singleItem.glsv == 1):
                logger.debug(f"glsv is 1 for relic {singleItem.id}. Saving data for vectorization.")
                dataForVector:DataForVector = DataForVector(relicId=singleItem.id,
                    desc=singleItem.desc,
                    purposeName=singleItem.purposeName,
                    materialName=singleItem.materialName,
                    nationalityName=singleItem.nationalityName1)
                embedding_service.save_data_for_vector(dataForVector)
                
            return detail_info_dto
            
        except Exception as e:
            # This is a final catch-all for any other unexpected errors during DTO creation.
            logger.critical(f"A critical, unexpected error occurred during DTO creation for id {id}: {e}", exc_info=True)
            return None

emuseum = EmuseumAPIService()