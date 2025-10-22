# debug_detalhado.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://ufcstats.com/statistics/fighters?char=a&page=all"

def debug_detalhado():
    r = requests.get(BASE_URL, timeout=10)
    soup = BeautifulSoup(r.content, "lxml")
    
    print("=== DEBUG DETALHADO DA ESTRUTURA DA TABELA ===")
    
    # Pegar as primeiras 3 linhas de dados
    rows = soup.select("tr.b-statistics__table-row")[1:4]
    
    for i, row in enumerate(rows):
        cols = row.select("td")
        print(f"\n=== LINHA {i+1} ===")
        
        for j, col in enumerate(cols):
            text = col.get_text(strip=True)
            print(f"Coluna {j}: '{text}'")
        
        # Verificar se tem links (para nome)
        links = row.select("a")
        print(f"Links encontrados: {len(links)}")
        for link in links:
            print(f"  Link: {link.get('href')} -> {link.get_text(strip=True)}")

if __name__ == "__main__":
    debug_detalhado()