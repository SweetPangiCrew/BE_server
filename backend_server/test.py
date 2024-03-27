
import unittest
import json

class Test(unittest.TestCase):

    def test_emoji(self):
            with open('emoji.json', 'r') as file:
                emojis = json.load(file)
                print("counts: "+str(len(emojis)))
                apple_emojis = [item for index, item in enumerate(emojis) if item["has_img_apple"]]
               
                
            pronunciatio = "🙂0️⃣🤲🏿"#🙂0️⃣🤲🏿
            unicode_code_point = ""
            unicode_debug_name = ""
            unicode_image_name = ""
            #print("len:"+str(len(pronunciatio)))
    
            pre_emoji = ""
            for emoji in pronunciatio:
                print(emoji)
           
                emoji_unicode = format(ord(emoji), '04X')
               
                matching_item= [item for index, item in enumerate(apple_emojis) if item["unified"] == str(emoji_unicode).upper() and item["category"] != "Component"]
                
                if len(matching_item) > 0 :
                    unicode_image_name += matching_item[0]["image"] + " "
                    if(pre_emoji != "") :
                           matching_item= [item for index, item in enumerate(apple_emojis) if item["unified"] == str(pre_emoji).upper()]
                           if len(matching_item) > 0 :
                                unicode_image_name += matching_item[0]["image"] + " "
                    pre_emoji = ""
                else : 
                    if(pre_emoji != "") : pre_emoji += "-"
                    pre_emoji += emoji_unicode
                    #print(pre_emoji)


            if(pre_emoji != "") :
                    matching_item= [item for index, item in enumerate(apple_emojis) if item["unified"] == str(pre_emoji).upper() and item["category"] != "Component"]
                    if len(matching_item) > 0 :
                                unicode_image_name += matching_item[0]["image"] + " "
            
            print(unicode_image_name)
                
                      


if __name__ == '__main__':
    unittest.main()