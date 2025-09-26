# Code to str
# str to code

from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
import csv
import os

import logging
logger = logging.getLogger(__name__)

class CodeConverter:
    """
    A class to handle data from a CSV file with columns 'code', 'parentCode', 'level', 'nameKr'.
    It provides methods for efficient data lookups.
    """
    def __init__(self):
        """
        Initializes the CSVHandler by loading data from the specified file.

        Args:
            filepath (str): The path to the CSV file.
        """
        
        self.code_to_name = {}
        self.name_to_code = {}
        self.code_to_parent = {}
        
        self.loaded=False
        
    def init_app(self,filepath):
        self.filepath = filepath
        self._load_data()
        self.loaded=True

    def _load_data(self):
        """
        Internal method to load data from the CSV file into dictionaries for fast lookups.
        FIX: Dynamically handles the corrupted 'code' column header created by the '' prefix.
        """
        try:
            with open(self.filepath, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # FIX 1: Dynamically determine the correct key for the 'code' column.
                # If the first fieldname starts with the prefix (e.g., 'code'), use that.
                code_key_to_use = 'code'
                if reader.fieldnames and reader.fieldnames[0].endswith('code'):
                    code_key_to_use = reader.fieldnames[0]
                
                for row in reader:
                    # Use the dynamically determined key for the 'code' column
                    code = row.get(code_key_to_use)
                    nameKr = row.get('nameKr')
                    parentCode = row.get('parentCode')

                    # This condition now passes because 'code' is correctly retrieved.
                    if code and nameKr:
                        # FIX 2: Strip whitespace from CSV nameKr key (for robustness)
                        nameKr = nameKr.strip() 
                        # Map code to all data for potential future use
                        self.code_to_name[code] = nameKr
                        
                    if nameKr and code:
                        # Dictionary now gets populated here.
                        self.name_to_code[nameKr] = code

                    if code and parentCode:
                        # Map code to its parentCode
                        self.code_to_parent[code] = parentCode
            logger.debug(f"CodeConverter loaded {len(self.name_to_code)} names from {Path(self.filepath).name}")

        except FileNotFoundError:
            logger.error(f"Error: The file '{self.filepath}' was not found.")
        except Exception as e:
            logger.error(f"An error occurred while reading the file: {e}")

    def code_to_nameKr(self, code):
        """
        Converts a 'code' to its corresponding 'nameKr'.
        
        Args:
            code (str): The code to look up.

        Returns:
            str: The corresponding 'nameKr' or None if not found.
        """
        if self.loaded==False:
            raise
            # raise some error here.
        
        return self.code_to_name.get(code)

    def nameKr_to_code(self, nameKr):
        """
        Converts a 'nameKr' to its corresponding 'code'.

        Args:
            nameKr (str): The name to look up.

        Returns:
            str: The corresponding 'code' or None if not found.
        """
        if self.loaded==False:
            logger.error(f"Converter not loaded when looking up '{nameKr}'")
            return None
        
        # FIX 3: Strip whitespace from the input (LLM output) before lookup
        cleaned_nameKr = nameKr.strip()
        result = self.name_to_code.get(cleaned_nameKr)
        
        if result is None:
            # DEBUGGING: Log failure details
            raw_input_repr = cleaned_nameKr.encode('unicode_escape')
            logger.debug(f"Code conversion failed for input: '{cleaned_nameKr}' (Raw: {raw_input_repr})")
            logger.debug(f"Input string length: {len(cleaned_nameKr)}. Source file: {Path(self.filepath).name}")

        return result
    
    
script_dir = Path(__file__).parent.resolve()

material_file_path = script_dir / '..' / 'data' / "material_code.csv"
purpose_file_path = script_dir / '..' / 'data' / 'purpose_code.csv'
nationality_file_path = script_dir / '..' / 'data' / 'nation_code.csv'
museum_file_path = script_dir / '..' / 'data' / 'museum_code.csv'
sizeRange_file_path = script_dir / '..' / 'data' / 'sizeRange_code.csv'

materialConverter = CodeConverter()
materialConverter.init_app(filepath=material_file_path)

purposeConverter = CodeConverter()
purposeConverter.init_app(filepath=purpose_file_path)

nationalityConverter = CodeConverter()
nationalityConverter.init_app(filepath=nationality_file_path)

museumConverter = CodeConverter()
museumConverter.init_app(filepath=museum_file_path)

sizeRangeConverter = CodeConverter()
sizeRangeConverter.init_app(filepath=sizeRange_file_path)