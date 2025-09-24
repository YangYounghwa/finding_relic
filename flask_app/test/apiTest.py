
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services', 'emuseumService')))

from EmuseumService import emuseum
from pprint import pprint



# result = emuseum.getItemsByKeywords(name="백제",numOfRows=5)
# print(result)




result2 = emuseum.getDetailInfo(id='PS0100100101101235600000')
# print(result2)





