import requests
import io
import base64
import pytesseract
from bs4 import BeautifulSoup
from PIL import Image

if __name__ == '__main__':
    domain = "nortom.eu"
    url = "https://whois.eurid.eu/pl/search/?domain=" + domain
    #request html from URL
    res = requests.get(url, headers={'User-Agent': 'Mozilla/6.0 (Windows NT 6.3; Win64; x64)'})
    #create BS parser
    soup = BeautifulSoup(res.text, features="html.parser")
    #find all rows with informtation
    all_values=soup.find_all("div", {"class": "stat-value"})
    try:
        #fetch domain name

        domain_name = all_values[0].next_element
        #fetch registration name
        registration_date = all_values[2].next_element

        #It is necessary fetch all labels to check if domain owner is  (displayed data is different)
        
        #Change this variable if your language is different than polish
        label = "Organizacja"

        if(soup.find_all("div", {"class": "stat-label"})[7].next_element == label):
            #fetch image in form of base64
            email = all_values[10].img['src'].split('base64,')[-1].strip()
        else:
            #fetch image in form of base64
            email = all_values[8].img['src'].split('base64,')[-1].strip()

        #create PIL Image for OCR
        email = Image.open(io.BytesIO(base64.b64decode(email)))
        bg = Image.new("RGB", email.size, (255,255,255))
        bg.paste(email,email)
        print
        print(domain_name)
        print(registration_date)
        #print email after OCR
        print(pytesseract.image_to_string(bg))
    except:
        print("Could not scrap information")
