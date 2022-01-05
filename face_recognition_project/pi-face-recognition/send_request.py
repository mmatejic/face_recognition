import requests
import io
from PIL import Image
url = 'http://localhost:8000/verify/'

files = {'media': open(r'c:\users\mihailo.matejic\Desktop\DSC_0010.JPG', 'rb')}

response = requests.post(url, files=files)
print(response.content.decode())