import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./pinup.json")
firebase_admin.initialize_app(cred)
Db = firestore.client()


# Create your views here.
def Scraper(url):
    USER_AGENT = 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    cnt = session.get(f"https://www.amazon.in/s?k={url}").text
    return cnt

# res = Scraper()
# soup = BeautifulSoup(res, 'html.parser')
# for sup in soup.find_all('li', {'class': 'bn-group'}):
#     itms = []
#     for itm in sup.find_all('li', {'class': 'bn-link'}):
#         print(itm)
#         itms.append(f"{itm.findChild()}")
#     prod.append({
#         'Name': f"{sup.findChild('strong').text}",
#         'Cnts': itms
#     })
def home(request):
    print("Initializing...")
    cnt = {}
    Ref = Db.collection("GeM")
    prods = Ref.stream()

    for prod in prods:
        cnt[prod.id] = prod.to_dict()

    return render(request, "Home.html", {'Prods': cnt})


def prod(request, p_nm):
    prod = Db.collection("GeM").document(p_nm).get().to_dict()
    prod['ID'] = p_nm
    res = Scraper("Samsung+Galaxy+Tab+S6+Lite+LTE+P619N")
    soup = BeautifulSoup(res, 'html.parser')
    itms = []
    # print(soup.find_all()
    for sup in soup.find_all('div', {'data-component-type': 's-search-result'})[:5]:
        itm = {
            'src': sup.find('img', {'class': 's-image'})['src'],
            'name': sup.find('div', {'data-cy': 'title-recipe'}).text,
            'price': sup.find('span', {'class': 'a-price-whole'}).text
        }
        itms.append(itm)
        print(itms)
        # for itm in sup.find_all('li', {'class': 'bn-link'}):
        #     print(itm)
        #     itms.append(f"{itm.findChild()}")
        # prod.append({
        #     'Name': f"{sup.findChild('strong').text}",
        #     'Cnts': itms
        # })
    ctx = {
        'Prod': prod,
        'Comps': itms,
    }

    return render(request, "Prod.html", ctx)
