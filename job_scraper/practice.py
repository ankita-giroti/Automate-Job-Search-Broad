import base64
import json
import os
from dotenv import load_dotenv

load_dotenv()

cookies = os.environ.get('COOKIES_DATA')
decoded_str = base64.b64decode(cookies).decode('utf-8')
print(f"Total length: {len(decoded_str)}")
print(f"End of string: {decoded_str[-20:]}")
json.loads(decoded_str)