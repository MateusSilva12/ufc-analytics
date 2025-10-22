# ufc_fighters_scraper.py - VERSÃO FINAL CORRIGIDA
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "http://ufcstats.com/statistics/fighters?char={}&page=all"
LETTERS = list("abcdefghijklmnopqrstuvwxyz")

def scrape_fighters():
    all_data = []
    for letter in LETTERS:
        url = BASE_URL.format(letter)
        print(f"Lendo {url}")
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.content, "lxml")
            rows = soup.select("tr.b-statistics__table-row")
            
            for row in rows[1:]:  # pular cabeçalho
                cols = row.select("td")
                if len(cols) < 10:  # Agora são 10 colunas!
                    continue
                
                # ORDEM CORRETA baseada no debug:
                first_name = cols[0].get_text(strip=True)
                last_name = cols[1].get_text(strip=True)
                full_name = f"{first_name} {last_name}".strip()
                
                nickname = cols[2].get_text(strip=True)
                height = cols[3].get_text(strip=True)
                weight = cols[4].get_text(strip=True)
                reach = cols[5].get_text(strip=True)
                stance = cols[6].get_text(strip=True)
                
                # CORREÇÃO: Wins, Losses, Draws estão nas colunas 7, 8, 9
                try:
                    wins = int(cols[7].get_text(strip=True)) if cols[7].get_text(strip=True) else 0
                except:
                    wins = 0
                
                try:
                    losses = int(cols[8].get_text(strip=True)) if cols[8].get_text(strip=True) else 0
                except:
                    losses = 0
                
                try:
                    draws = int(cols[9].get_text(strip=True)) if cols[9].get_text(strip=True) else 0
                except:
                    draws = 0
                
                all_data.append({
                    "Name": full_name,
                    "Nickname": nickname,
                    "Height": height,
                    "Weight": weight,
                    "Reach": reach,
                    "Stance": stance,
                    "Wins": wins,
                    "Losses": losses,
                    "Draws": draws
                })
            
            time.sleep(0.3)
        except Exception as e:
            print(f"Erro em {letter}: {e}")
            continue
    
    df = pd.DataFrame(all_data)
    df.to_csv("data/ufc_fighters.csv", index=False)
    print(f"Salvo: data/ufc_fighters.csv - {len(df)} lutadores")
    
    # Verificação
    print("\n=== DADOS CORRETOS ===")
    print(f"Total de vitórias: {df['Wins'].sum()}")
    print(f"Total de derrotas: {df['Losses'].sum()}")
    print(f"Exemplo - Lutador com mais vitórias:")
    top_winner = df.loc[df['Wins'].idxmax()]
    print(f"  {top_winner['Name']}: {top_winner['Wins']} vitórias")
    
    return df

if __name__ == "__main__":
    df = scrape_fighters()