



from langchain.chains import LLMChain
import os
from typing import Dict

from langchain_openai import ChatOpenAI
import logging
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException 
from langchain.prompts import PromptTemplate

from relic_app.dto.llmserviceDTO import KorRelation, Material_descriptions, Material, Nations, K_nation_descriptions, Purpose, Purpose_descriptions
from langchain_community.callbacks import get_openai_callback
from dotenv import load_dotenv
load_dotenv()


import logging
logger = logging.getLogger(__name__)

class LLMServiceObjet:
    
    def __init__(self):
        

        openaiMINI = os.getenv("OPENAI_MINI_MODEL")
        openaiNANO = os.getenv("OPENAI_NANO_MODEL")
        
        # API KEY Loads automatically
        self.llm_mini_cold = ChatOpenAI(model=openaiMINI,temperature=0) 
        self.llm_nano_cold = ChatOpenAI(model=openaiNANO,temperature=0)
        self.llm_mini_warm = ChatOpenAI(model=openaiMINI,temperature=0.1) 
        self.llm_nano_warm = ChatOpenAI(model=openaiNANO,temperature=0.1)


    def isKorHisRelated(self,text:str)->KorRelation:
        
        logger.debug("isKoreHistoryRelated().")
        # Checks the context and findout if it is related to korean history. 
        # If not, it will not be used for query
        # result = {"related": True, "error": False}
        

        
        parser = PydanticOutputParser(pydantic_object=KorRelation)
        template = """Read the text and check whether if the text is related to the Korean History or korean artefacts. It can be related to modern history., if so mark related as True, if not mark it false. If you are not sure on the result mark unsure as True, otherwise false.
        
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
                logger.debug(f"relation.related:{relation.related}")
                
            except OutputParserException as e:
                logger.debug(f"Failed to parse LLM response")
                logger.debug(f"Arguments {e.args[0]}")
                relation = {"error": True}
        
        # Access the token counts after the LLM call
        logger.info(f"Total Tokens: {cb.total_tokens}")
        logger.info(f"Prompt Tokens: {cb.prompt_tokens}")
        logger.info(f"Completion Tokens: {cb.completion_tokens}")
        return relation
    
    
    
    
    def getNationality(self, text:str)->Nations:
        K_nation_descriptions.korean_nations_descriptions
        # Step 3: Create an instance of the PydanticOutputParser
        parser = PydanticOutputParser(pydantic_object=Nations)
        template="""글을 읽고 해당하는 한국 역사 속 국가/시대 이름을 알려줘.
        Here are the available options with brief descriptions: {options_with_descriptions}.

Your response must be a single item from the list. Follow the specified format instructions below. Second optional must not be equal to the first.
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
        logger.debug("getNationality(). prompt created.")
        nation = None
        llm = self.llm_nano_cold
        # llm = self.llm_mini_cold
        chain = prompt | llm | parser
        
        with get_openai_callback() as cb:
            try:
                nation:Nations = chain.invoke({"text": text})
                logger.debug(f"relation.related:{nation.name}")
                logger.debug(nation.model_dump_json())
                
            except OutputParserException as e:
                # TODO : priority low,  add fallback.
                logger.debug(f"Failed to parse LLM response")
                logger.debug(f"Arguments {e.args[0]}")
                relation = {"error": True}
        # Access the token counts after the LLM call
        logger.info(f"Total Tokens: {cb.total_tokens}")
        logger.info(f"Prompt Tokens: {cb.prompt_tokens}")
        logger.info(f"Completion Tokens: {cb.completion_tokens}")
        
        return nation
        
    def getMaterial(self, text:str)->Material:
        Material_descriptions.material_descriptions
        
        # Step 3: Create an instance of the PydanticOutputParser
        parser = PydanticOutputParser(pydantic_object=Material)
        template="""글을 읽고 해당 유물 혹은 설명에 부합하는 재료를 알려줘, 
        Here are the available options with brief descriptions: {options_with_descriptions}.

Your response must be a single item from the list. Follow the specified format instructions below. Second optional must not be equal to the first.
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
                material:Material = chain.invoke({"text": text})
                logger.debug(f"relation.related:{material.name}")
                logger.debug(material.model_dump_json())
                
            except OutputParserException as e:
                # TODO : priority low,  add fallback.
                logger.debug(f"Failed to parse LLM response")
                logger.debug(f"Arguments {e.args[0]}")
                relation = {"error": True}
        # Access the token counts after the LLM call
        logger.info(f"Total Tokens: {cb.total_tokens}")
        logger.info(f"Prompt Tokens: {cb.prompt_tokens}")
        logger.info(f"Completion Tokens: {cb.completion_tokens}")
        
        return material
    
    
    
    
    def getPurpose(self, text:str)->Purpose:
        Purpose_descriptions.purpose_descriptions
        
        # Step 3: Create an instance of the PydanticOutputParser
        parser = PydanticOutputParser(pydantic_object=Purpose)
        template="""글을 읽고 해당 유물 혹은 글 내용에서 유추할 수 있는 주 용도를 알려줘. 가장 간단한 기능을 우선하고 부차적인 것은 무시해.
        Here are the available options with brief descriptions: {options_with_descriptions}.

Your response must be a single item from the list. Follow the specified format instructions below. Second optional must not be equal to the first.
        {format_instructions}
        Text: {text}
        """
        options_with_descriptions = "\n".join([
    f"* **{pur}**: {desc}" for pur, desc in Purpose_descriptions.purpose_descriptions.items()
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
                purpose:Purpose = chain.invoke({"text": text})
                logger.debug(purpose.model_dump_json())
                logger.debug(f"relation.related:{purpose.name}")    
                
            except OutputParserException as e:
                # TODO : priority low,  add fallback.
                logger.debug(f"Failed to parse LLM response")
                logger.debug(f"Arguments {e.args[0]}")
                relation = {"error": True}
        # Access the token counts after the LLM call
        logger.info(f"Total Tokens: {cb.total_tokens}")
        logger.info(f"Prompt Tokens: {cb.prompt_tokens}")
        logger.info(f"Completion Tokens: {cb.completion_tokens}")
        
        return purpose
    
    
llmService = LLMServiceObjet()