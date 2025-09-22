

from typing import Dict
from dotenv import load_dotenv
load_dotenv()
import os

import xmltodict

import requests





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

        apiRoute = "/relic/list"  # Adjust this route as needed for your API
        return self._makeRequests(apiRoute, params,pageNo=pageNo,numOfRows=numOfRows)
            
                        
                        
                        


emuseum = EmuseumAPIService()
            

