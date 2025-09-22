

from dotenv import load_dotenv
load_dotenv()
import os



class EmuseumService:
    
    def __init__(self):
        self.emuseumURL = os.getenv('EMUSESUM_URL')
        self.apiKey = os.getenv('EMUSEUM_KEY')
        
        pass 
    
    
    def getItemsByName(self,name:str,lang:str = "korean"):
        pass
    
    
    def getItemsByKeywords(self,name:str,author:str,
                           id:str=None,museumCode:str=None,
                           nationalityCode:str=None,meterialCode:str=None,
                           purposeCode:str=None,sizeRangeCode:str=None,
                           placeLandCode:str=None,designationCode:str=None,
                           indexWord:str=None):
