


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
                
                code_key_to_use = 'code'
                # Check the actual header row read by DictReader
                if reader.fieldnames and reader.fieldnames[0].startswith('['):
                    # The first column key is corrupted (e.g., 'code'), so we use that full key.
                    code_key_to_use = reader.fieldnames[0]
                # Else, we assume the key is the standard 'code'
                
                # --- Begin reading data rows ---
                for row in reader:
                    # Use the dynamically determined key for the 'code' column
                    code = row.get(code_key_to_use)
                    
                    # 'nameKr' and 'parentCode' keys should be safe from the prefix issue
                    nameKr = row.get('nameKr')
                    parentCode = row.get('parentCode')

                    if code and nameKr:
                        # Map code to all data for potential future use
                        nameKr = nameKr.strip() # Ensure CSV keys are clean
                        self.code_to_name[code] = nameKr
                        
                    if nameKr and code:
                        # Map nameKr to code
                        self.name_to_code[nameKr] = code

                    if code and parentCode:
                        # Map code to its parentCode
                        self.code_to_parent[code] = parentCode

        except FileNotFoundError:
            print(f"Error: The file '{self.filepath}' was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

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
            # DEBUGGING: Log when a converter is called before initialization
            logger.error(f"Converter not loaded when looking up '{nameKr}'")
            return None
        
        cleaned_nameKr = nameKr.strip() # FIX 2: Strip whitespace from the input (LLM output)
        result = self.name_to_code.get(cleaned_nameKr)
        
        if result is None:
            # DEBUGGING: Log failure details
            # Check the raw input string to see if it contains hidden chars
            raw_input_repr = cleaned_nameKr.encode('unicode_escape')
            logger.debug(f"Code conversion failed for input: '{cleaned_nameKr}' (Raw: {raw_input_repr})")
            logger.debug(f"Input string length: {len(cleaned_nameKr)}. Source file: {Path(self.filepath).name}")
            # This logic will now explicitly show you if the input string contains non-visible characters.

        return result

    def code_to_parent(self, code):
        """
        Converts a 'code' to its corresponding 'parentCode'.

        Args:
            code (str): The code to look up.

        Returns:
            str: The corresponding 'parentCode' or None if not found.
        """
        return self.code_to_parent.get(code)
    
    
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