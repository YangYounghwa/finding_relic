
import concurrent.futures

from typing import List
from relic_app.dto.EmuseumDTO import BriefList
from relic_app.dto.llmserviceDTO import KorRelation, Material, Nations, Purpose
from relic_app.services.LLMService.LLMServiceObject import llmService
from relic_app.services.emuseumService.EmuseumService import emuseum
from pprint import pprint
from flask import Flask

from relic_app.util.MuseumCodeTranslator import materialConverter, purposeConverter, nationalityConverter

import logging
logger = logging.getLogger(__name__)


class SearchServiceObject:
    
    def __init__(self):
        pass
        
    
    def getItemList(self,text:str)->BriefList:
        
        
        relation:KorRelation = llmService.isKorHisRelated(text)
        logger.debug(f"relation.related:{relation.related}")
        if not relation.related:
            return []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Submit the tasks to the executor
            future_nation = executor.submit(llmService.getNationality, text)
            future_purpose = executor.submit(llmService.getPurpose, text)
            future_material = executor.submit(llmService.getMaterial, text)

            # Retrieve the results. .result() will block until the task is complete.
            nation:Nations = future_nation.result()
            logger.debug(f"nation:{nation.name}")
            purpose:Purpose = future_purpose.result()
            logger.debug(f"purpose:{purpose.name}")
            material:Material = future_material.result()
            logger.debug(f"material:{material.name}")
        
        
        # case 1
        queryList = []
        argDict = {}
        argDict['nation'] = nation.name
        argDict['purpose'] = purpose.name
        argDict['material'] = material.name
        queryList.append(argDict)
        
        logger.debug(f"queryList:{queryList}")
         
        # if(nation.candidate):
        #     argDict2 ={}
        #     argDict2['nation']= nation.candidate
        #     argDict2['purpose'] = purpose.name
        #     argDict2['material'] = material.name
        #     queryList.append(argDict2)
        # if(purpose.candidate):
        #     argDict3 ={}
        #     argDict3['nation']= nation.name
        #     argDict3['purpose'] = purpose.candidate
        #     argDict3['material'] = material.name
        #     queryList.append(argDict3)
        # if(material.candidate):
        #     argDict4 ={}
        #     argDict4['nation']= nation.name
        #     argDict4['purpose'] = purpose.name
        #     argDict4['material'] = material.candidate
        #     queryList.append(argDict4)
        # if(nation.candidate and purpose.candidate):
        #     argDict5 ={}
        #     argDict5['nation']= nation.candidate
        #     argDict5['purpose'] = purpose.candidate
        #     argDict5['material'] = material.name
        #     queryList.append(argDict5)
        # if(nation.candidate and material.candidate):
        #     argDict6 ={}
        #     argDict6['nation']= nation.candidate
        #     argDict6['purpose'] = purpose.name
        #     argDict6['material'] = material.candidate
        #     queryList.append(argDict6)
        # if(purpose.candidate and material.candidate):
        #     argDict7 ={}
        #     argDict7['nation']= nation.name
        #     argDict7['purpose'] = purpose.candidate
        #     argDict7['material'] = material.candidate
        #     queryList.append(argDict7)
        
        # For each return list of N
        # Does it have order? Emusuem might or mightnot have order.
        my_brief_list:BriefList = BriefList(totalCount=0, brief_info_list=[])

        for item in queryList:
            item['nation']
            item['purpose']
            item['material']
            
            nationCode = nationalityConverter.nameKr_to_code(item['nation'])
            purposeCode = purposeConverter.nameKr_to_code(item['purpose'])
            materialCode = materialConverter.nameKr_to_code(item['material'])
            
            logger.debug(f"nationCode:{nationCode}")
            logger.debug(f"purposeCode:{purposeCode}")
            logger.debug(f"materialCode:{materialCode}")
            
            temp_brief_list = emuseum.getItemsByKeywords(nationalityCode=nationCode, purposeCode=purposeCode, materialCode=materialCode)
            logger.debug(f"temp_brief_list.total_count:{temp_brief_list.total_count}")
            
            my_brief_list.add_brief_list(temp_brief_list)
         
        return my_brief_list
     
        
        
        
        
searcher = SearchServiceObject()
