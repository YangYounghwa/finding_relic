
import concurrent.futures

from itertools import product
from typing import List
from relic_app.dto.EmuseumDTO import BriefList
from relic_app.dto.llmserviceDTO import KorRelation, Material, Nations, Purpose, RelicName
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
        
    def getItemList(self, text: str) -> BriefList:
        """
        Finds items by first analyzing text to extract attributes with an LLM,
        then running all possible search queries against the museum API in parallel.
        """
        
        # 1. Initial check to see if the text is relevant (unchanged)
        relation: KorRelation = llmService.isKorHisRelated(text)
        logger.debug(f"relation.related: {relation.related}")
        if not relation.related:
            return BriefList(totalCount=0, brief_info_list=[])

        # 2. Get all attributes from the text in parallel (unchanged)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_nation = executor.submit(llmService.getNationality, text)
            future_purpose = executor.submit(llmService.getPurpose, text)
            future_material = executor.submit(llmService.getMaterial, text)
            future_name = executor.submit(llmService.getName, text)
            
            nation: Nations = future_nation.result()
            purpose: Purpose = future_purpose.result()
            material: Material = future_material.result()
            relicName: RelicName = future_name.result()

        # 3. Build a list of all search arguments, prioritizing name searches
        search_args_list = []
        
        # --- Add name-based searches FIRST to prioritize them ---
        if relicName.name:
            search_args_list.append({'name': relicName.name})
        if relicName.candidate and relicName.candidate_certainty:
            search_args_list.append({'name': relicName.candidate})

        # --- Use itertools.product for a clean way to get all keyword combinations ---
        nation_opts = [nation.name]
        if nation.candidate:
            nation_opts.append(nation.candidate)
            
        purpose_opts = [purpose.name]
        if purpose.candidate:
            purpose_opts.append(purpose.candidate)
            
        material_opts = [material.name]
        if material.candidate:
            material_opts.append(material.candidate)

        # This creates all possible combinations, e.g., (nation1, purpose1, material2)
        keyword_combinations = product(nation_opts, purpose_opts, material_opts)
        
        for n, p, m in keyword_combinations:
            # Convert names to codes for the API call
            nation_code = nationalityConverter.nameKr_to_code(n)
            purpose_code = purposeConverter.nameKr_to_code(p)
            material_code = materialConverter.nameKr_to_code(m)
            
            # Add the search arguments if at least one code is valid
            if any((nation_code, purpose_code, material_code)):
                search_args_list.append({
                    'nationalityCode': nation_code,
                    'purposeCode': purpose_code,
                    'materialCode': material_code
                })

        # 4. Execute all searches in parallel and collect results in order
        my_brief_list = BriefList(totalCount=0, brief_info_list=[])
        if not search_args_list:
            return my_brief_list

        # Use a thread pool to make all API calls concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Create a future for each search. The order is preserved.
            futures = [executor.submit(emuseum.getItemsByKeywords, **args) for args in search_args_list]
            
            for future in futures:
                try:
                    # .result() waits for the future to complete
                    temp_brief_list = future.result()
                    if temp_brief_list:
                        logger.debug(f"Search found {temp_brief_list.totalCount} items.")
                        my_brief_list.add_brief_list(temp_brief_list)
                except Exception as e:
                    logger.error(f"A search query failed: {e}")

        return my_brief_list
     
        
        
        
        
searcher = SearchServiceObject()
