



from langchain.chains import LLMChain
import os
from typing import Dict

from flask import current_app
from langchain_openai import ChatOpenAI
import logging
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser, OutputParserException
from langchain.prompts import PromptTemplate

from flask_app.dto.llmserviceDTO import KorRelation


class LLMServiceObjet:
    
    def __init__(self):
        

        openaiMINI = os.getenv("OPENAI_MINI_MODEL")
        openaiNANO = os.getenv("OPENAI_NANO_MODEL")
        
        # API KEY Loads automatically
        self.llm_mini_cold = ChatOpenAI(model=openaiMINI,temperature=0) 
        self.llm_nanao_cold = ChatOpenAI(model=openaiNANO,temperature=0)
        self.llm_mini_warm = ChatOpenAI(model=openaiMINI,temperature=0.1) 
        self.llm_nanao_warm = ChatOpenAI(model=openaiNANO,temperature=0.1)

     
    def isKorHisRelated(self,text:str)->Dict:
        
        current_app.logger.debug("isKoreHistoryRelated().")
        # Checks the context and findout if it is related to korean history. 
        # If not, it will not be used for query
        result = Dict({"related":True, "error":False})
        

        
        parser = PydanticOutputParser(pydantic_object=KorRelation)
        text_to_extract_relation = "Read the text and check whether if the text is related to the Korena History, if so mark related as True, if not mark it false. If you are not sure on the result mark unsure as True, otherwise false."
        
        
        prompt = PromptTemplate(
            template=text_to_extract_relation,
            input_variables=["query"],
            output_parser={"format_instructions":parser.get_format_instructions()}
        )
        
        llm = self.llm_nano_cold
        chain = prompt | llm | parser
        try:
            prompt = text_to_extract_relation
            relation = chain.invoke({'query':prompt})
            current_app.logger.debug(f"relation.related:{relation.related}")
        except OutputParserException as e:
            current_app.logger.debug(f"Failed to parse LLM response")
            current_app.logger.debug(f"Arguments {e.args[0]}") 
        
        
        return relation
    
