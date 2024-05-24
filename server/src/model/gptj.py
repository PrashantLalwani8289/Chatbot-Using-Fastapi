
import os
from dotenv import load_dotenv
import requests
import json
import google.generativeai as genai





load_dotenv()



class GPT:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')

    #     self.url = os.environ.get('MODEL_URL')
    #     self.headers = {
    #         "Authorization": f"Bearer {os.environ.get('HUGGINFACE_INFERENCE_TOKEN')}"}
    #     self.payload = {
    #         "inputs": "",
    #         "parameters": {
    #             "return_full_text": False,
    #             "use_cache": True,
    #             "max_new_tokens": 25
    #         }

    #     }

    


    def query(self, input: str) -> list:
        genai.configure(api_key=self.api_key)
        input = f"Human : ${input}.  Bot :" 
        self.model = genai.GenerativeModel('gemini-pro')
        response = self. model.generate_content(input, stream=True)
    #   print(response)
        data = ""
        for chunk in response:
            # print(chunk.text)
            temp = chunk.text
            for ch in temp:
                if ch == "\n":
                    data += ""

                elif ch == "**":
                    data += " "
                elif ch == "*":
                    data += ""
                else:
                    data += ch
    

        # data = data[9:]
        # print(tempdata)
        print(data)
        return data
    #     self.payload["inputs"] = input
    #     data = json.dumps(self.payload)
    #     response = requests.request(
    #         "POST", self.url, headers=self.headers, data=data)
    #     print(json.loads(response.content.decode("utf-8")))
    #     return json.loads(response.content.decode("utf-8"))

if __name__ == "__main__":
    GPT().query("Will artificial intelligence help humanity conquer the universe?")
