
import unittest

from reverie import *
from global_methods import *


class Test(unittest.TestCase):

    def test_emoji(self):
           
            
            pronunciatio = "🙂0️⃣🤲🏿"#🙂0️⃣🤲🏿
          
            result = convert_emoji2img(pronunciatio)
            print(result)
                
                      


if __name__ == '__main__':
    unittest.main()