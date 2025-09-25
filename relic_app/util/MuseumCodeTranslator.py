


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
        """
        try:
            with open(self.filepath, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    code = row.get('code')
                    nameKr = row.get('nameKr')
                    parentCode = row.get('parentCode')

                    if code and nameKr:
                        # Map code to all data for potential future use
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
        return self.name_to_code.get(nameKr)

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