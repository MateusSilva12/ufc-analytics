# ufc_stats_scraper.py - VERSÃO CORRIGIDA
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import os
BASE = "http://ufcstats.com"  # CORRIGIDO: http em vez de https

def get_event_links(page_url):
    try:
        r = requests.get(page_url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "lxml")
        links = []
        for a in soup.select("a.b-link.b-link_style_black"):
            href = a.get("href")
            if href and "/event-details/" in href:
                links.append(href)
        return links
    except Exception as e:
        print(f"Erro ao acessar {page_url}: {e}")
        return []

def parse_fight_table(event_url):
    try:
        r = requests.get(event_url, timeout=10)
        soup = BeautifulSoup(r.content, "lxml")
        fight_rows = soup.select("table.b-fight-details__table tbody tr")
        fights = []
        
        for row in fight_rows:
            cols = [td.get_text(strip=True) for td in row.select("td")]
            if len(cols) >= 7:
                fights.append({
                    "event_url": event_url,
                    "fighter_1": cols[1],
                    "fighter_2": cols[2],
                    "weight_class": cols[3] if len(cols) > 3 else None,
                    "method": cols[4] if len(cols) > 4 else None,
                    "round": cols[5] if len(cols) > 5 else None,
                    "time": cols[6] if len(cols) > 6 else None
                })
        return fights
    except Exception as e:
        print(f"Erro no evento {event_url}: {e}")
        return []

def scrape_events(start_page=1, end_page=1, out_csv="data/ufc_fights_basic.csv"):
    all_fights = []
    
    for p in range(start_page, end_page+1):
        page_url = f"{BASE}/statistics/events/completed?page={p}"
        print(f"📄 Lendo página {p}: {page_url}")
        
        try:
            event_links = get_event_links(page_url)
            print(f"  📎 Encontrados {len(event_links)} eventos")
        except Exception as e:
            print(f"  ❌ Falha ao pegar links: {e}")
            continue
            
        for ev in event_links:
            try:
                fights = parse_fight_table(ev)
                all_fights.extend(fights)
                print(f"  ✅ Evento: {len(fights)} lutas")
            except Exception as e:
                print(f"  ❌ Evento falhou: {e}")
            time.sleep(1)
        
        time.sleep(2)

    if all_fights:
        df = pd.DataFrame(all_fights)
        os.makedirs("data", exist_ok=True)
        df.to_csv(out_csv, index=False)
        print(f"💾 Salvo: {out_csv} - {len(df)} lutas")
    else:
        print("❌ Nenhuma luta coletada")
        
    return pd.DataFrame(all_fights) if all_fights else pd.DataFrame()

if __name__ == "__main__":
    df = scrape_events(start_page=1, end_page=1, out_csv="data/ufc_fights_basic.csv")
    print(f"📦 Shape final: {df.shape}")