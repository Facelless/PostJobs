import requests
from bs4 import BeautifulSoup
import time

URL = "https://br.jobrapido.com/?w=developer&l=brasil&r=auto&shm=all"

WEBHOOK_URL = "https://discord.com/api/webhooks/1336694808982585396/6Hri02ZnDo2T9tT3mxWDPxzF81ugb_sUTpL7S_PTEPDyN6RvFolBC415Y2BFp3NassS5"

sent_titles = []

def fetch_and_send_vacancies():
    response = requests.get(URL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        main_div = soup.find(class_="main-content-wrapper")

        if main_div:
            result_items = main_div.find_all(class_="result-item")

            if result_items:
                for div_ in result_items:
                    _title = div_.find(class_="result-item__title")
                    _location = div_.find(class_="result-item__location")
                    _company = div_.find(class_="result-item__company")
                    _link = div_.find(class_="result-item__link")

                    _title_text = _title.get_text(strip=True) if _title else "Sem título"
                    _location_text = _location.get_text(strip=True) if _location else "Sem localização"
                    _company_text = _company.get_text(strip=True) if _company else "Sem empresa"
                    _link_url = _link['href'] if _link else "Sem link"


                    if _title_text not in sent_titles:
                        embed = {
                            "embeds": [
                                {
                                    "title": _title_text,
                                    "description": f"**Localização:** {_location_text}\n**Empresa:** {_company_text}",
                                    "url": _link_url,
                                    "color": 5814783,
                                    "footer": {
                                        "text": "Jobrapido - Vagas de Desenvolvimento"
                                    }
                                }
                            ]
                        }

                        response = requests.post(WEBHOOK_URL, json=embed)

                        if response.status_code == 204:
                            print(f"Vaga '{_title_text}' enviada com sucesso!")
                            sent_titles.append(_title_text)
                        else:
                            print(f"Erro ao enviar a vaga '{_title_text}': {response.status_code}")
            else:
                print("Nenhuma 'result-item' encontrada!")
        else:
            print("Div principal não encontrada!")
    else:
        print("Erro ao acessar a página. Status code:", response.status_code)


while True:
    fetch_and_send_vacancies()

    print("Aguardando 30 minutos para verificar novas vagas...")
    time.sleep(1)
