from bs4 import BeautifulSoup
import requests
import json
import string

url= "https://www.atlasdasaude.pt/doencasAaZ/"

def extrair_pagina(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    div_doencas = soup.find_all("div", class_="views-row")

    res = {}

    for div in div_doencas:
        a = div.find("h3").find("a")

        designacao = a.text.strip()
        link = a.get("href")

        descricao_curta = div.find(
            "div", class_="views-field-body"
        ).get_text(strip=True)

        res[designacao] = {
            "descricao_curta": descricao_curta,
            "link": link
        }

    return res


def extrair_conceito(link):
    url_base = "https://www.atlasdasaude.pt"

    html = requests.get(url_base + link).text
    soup = BeautifulSoup(html, "html.parser")

    conteudo = soup.select_one("div.field-name-body div.field-item")

    if conteudo:
        return conteudo.get_text(" ", strip=True)

    return ""

res = {}

for letra in string.ascii_lowercase:
    print(f"A extrair página{url+letra}")
    pagina = extrair_pagina(url + letra)

    for doenca, info in pagina.items():
        print(f"A extrair designação completa...")
        descricao_completa = extrair_conceito(info["link"])

        res[doenca] = {
            "descricao_curta": info["descricao_curta"],
            "descricao_completa": descricao_completa
        }


f_out= open("doencas.json", "w", encoding="utf-8")
json.dump(res, f_out, indent=4,ensure_ascii=False)
f_out.close()
print("Concluído")