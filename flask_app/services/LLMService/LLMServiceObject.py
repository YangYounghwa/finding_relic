



from langchain.chains import LLMChain
import os
from typing import Dict

from flask import current_app
from langchain_openai import ChatOpenAI
import logging
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException 
from langchain.prompts import PromptTemplate

from flask_app.dto.llmserviceDTO import KorRelation, KoreanNationsEnum, Material_descriptions, Meterial, Nations, K_nation_descriptions
from langchain_community.callbacks import get_openai_callback
from dotenv import load_dotenv
load_dotenv()

class LLMServiceObjet:
    
    def __init__(self):
        

        openaiMINI = os.getenv("OPENAI_MINI_MODEL")
        openaiNANO = os.getenv("OPENAI_NANO_MODEL")
        
        # API KEY Loads automatically
        self.llm_mini_cold = ChatOpenAI(model=openaiMINI,temperature=0) 
        self.llm_nano_cold = ChatOpenAI(model=openaiNANO,temperature=0)
        self.llm_mini_warm = ChatOpenAI(model=openaiMINI,temperature=0.1) 
        self.llm_nano_warm = ChatOpenAI(model=openaiNANO,temperature=0.1)


    def isKorHisRelated(self,text:str)->Dict:
        
        current_app.logger.debug("isKoreHistoryRelated().")
        # Checks the context and findout if it is related to korean history. 
        # If not, it will not be used for query
        # result = {"related": True, "error": False}
        

        
        parser = PydanticOutputParser(pydantic_object=KorRelation)
        template = """Read the text and check whether if the text is related to the Korean History, if so mark related as True, if not mark it false. If you are not sure on the result mark unsure as True, otherwise false.
        
        {format_instructions}
        
        Text: {query}
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        
        llm = self.llm_nano_cold
        chain = prompt | llm | parser
        
        with get_openai_callback() as cb:
            try:
                relation = chain.invoke({'query': text})
                current_app.logger.debug(f"relation.related:{relation.related}")
                
            except OutputParserException as e:
                current_app.logger.debug(f"Failed to parse LLM response")
                current_app.logger.debug(f"Arguments {e.args[0]}")
                relation = {"error": True}
        
        # Access the token counts after the LLM call
        current_app.logger.info(f"Total Tokens: {cb.total_tokens}")
        current_app.logger.info(f"Prompt Tokens: {cb.prompt_tokens}")
        current_app.logger.info(f"Completion Tokens: {cb.completion_tokens}")
        return relation
    
    
    
    def getNationality(self, text:str)->Nations:
        K_nation_descriptions.korean_nations_descriptions
        # Step 3: Create an instance of the PydanticOutputParser
        parser = PydanticOutputParser(pydantic_object=Nations)
        template="""글을 읽고 해당하는 한국 역사 속 국가/시대 이름을 알려줘.
        Here are the available options with brief descriptions: {options_with_descriptions}.

Your response must be a single item from the list. Follow the specified format instructions below.
        {format_instructions}
        Text: {text}
        """
        options_with_descriptions = "\n".join([
    f"* **{nation}**: {desc}" for nation, desc in K_nation_descriptions.korean_nations_descriptions.items()
])

        prompt = PromptTemplate(
            template=template,
            input_variables=["text"],
            partial_variables={
                "options_with_descriptions": options_with_descriptions,
                "format_instructions": parser.get_format_instructions()
            }
        )
        llm = self.llm_nano_cold
        # llm = self.llm_mini_cold
        chain = prompt | llm | parser
        
        with get_openai_callback() as cb:
            try:
                nation = chain.invoke({"text": text})
                current_app.logger.debug(f"relation.related:{nation.name}")
                
            except OutputParserException as e:
                # TODO : priority low,  add fallback.
                current_app.logger.debug(f"Failed to parse LLM response")
                current_app.logger.debug(f"Arguments {e.args[0]}")
                relation = {"error": True}
        # Access the token counts after the LLM call
        current_app.logger.info(f"Total Tokens: {cb.total_tokens}")
        current_app.logger.info(f"Prompt Tokens: {cb.prompt_tokens}")
        current_app.logger.info(f"Completion Tokens: {cb.completion_tokens}")
        
        return nation
        
    def getMaterial(self, text:str)->Meterial:
        Material_descriptions.material_descriptions
        
        # Step 3: Create an instance of the PydanticOutputParser
        parser = PydanticOutputParser(pydantic_object=Meterial)
        template="""글을 읽고 해당 유물 혹은 설명에 부합하는 재료를 알려줘
        Here are the available options with brief descriptions: {options_with_descriptions}.

Your response must be a single item from the list. Follow the specified format instructions below.
        {format_instructions}
        Text: {text}
        """
        options_with_descriptions = "\n".join([
    f"* **{mat}**: {desc}" for mat, desc in Material_descriptions.material_descriptions.items()
])

        prompt = PromptTemplate(
            template=template,
            input_variables=["text"],
            partial_variables={
                "options_with_descriptions": options_with_descriptions,
                "format_instructions": parser.get_format_instructions()
            }
        )
        llm = self.llm_nano_cold
        # llm = self.llm_mini_cold
        chain = prompt | llm | parser
        
        with get_openai_callback() as cb:
            try:
                material = chain.invoke({"text": text})
                current_app.logger.debug(f"relation.related:{material.name}")
                
            except OutputParserException as e:
                # TODO : priority low,  add fallback.
                current_app.logger.debug(f"Failed to parse LLM response")
                current_app.logger.debug(f"Arguments {e.args[0]}")
                relation = {"error": True}
        # Access the token counts after the LLM call
        current_app.logger.info(f"Total Tokens: {cb.total_tokens}")
        current_app.logger.info(f"Prompt Tokens: {cb.prompt_tokens}")
        current_app.logger.info(f"Completion Tokens: {cb.completion_tokens}")
        
        return material