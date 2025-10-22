# fight_stats_scraper_real.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import os

BASE = "http://ufcstats.com"

def parse_fight_page_correct(fight_url):
    """Coleta TODOS os dados reais das páginas de lutas"""
    try:
        print(f"    📊 Coletando dados de: {fight_url}")
        r = requests.get(fight_url, timeout=10)
        soup = BeautifulSoup(r.content, "lxml")
        
        stats = {"fight_url": fight_url}
        
        # 1. COLETAR NOMES DOS LUTADORES
        fighters = []
        fighter_elements = soup.select('h3.b-fight-details__person-name')
        for elem in fighter_elements:
            name = elem.get_text(strip=True)
            if name and name not in ['W', 'L']:  # Ignorar W/L
                fighters.append(name)
        
        if len(fighters) >= 2:
            stats["fighter_1"] = fighters[0]
            stats["fighter_2"] = fighters[1]
        else:
            # Fallback: procurar em outros lugares
            alt_fighters = soup.select('a.b-link.b-link_style_black')
            for link in alt_fighters:
                if '/fighter-details/' in link.get('href', ''):
                    fighters.append(link.get_text(strip=True))
            if len(fighters) >= 2:
                stats["fighter_1"] = fighters[0]
                stats["fighter_2"] = fighters[1]
        
        # 2. COLETAR RESULTADO (QUEM VENCEU)
        result_elements = soup.select('div.b-fight-details__person')
        for i, elem in enumerate(result_elements):
            if 'win' in elem.get('class', []) or 'W' in elem.get_text():
                if i == 0:
                    stats["winner"] = "fighter_1"
                else:
                    stats["winner"] = "fighter_2"
                break
        
        # 3. COLETAR MÉTODO DA VITÓRIA
        method_elem = soup.find('i', class_='b-fight-details__text-item_first')
        if method_elem:
            stats["method"] = method_elem.get_text(strip=True).replace('Method:', '').strip()
        
        # 4. COLETAR TODAS AS ESTATÍSTICAS DAS TABELAS
        tables = soup.select('table.b-fight-details__table')
        
        for table_idx, table in enumerate(tables):
            # Pegar título da tabela
            title_elem = table.find_previous('div', class_='b-fight-details__table-head')
            table_title = title_elem.get_text(strip=True) if title_elem else f"table_{table_idx}"
            
            # Processar cada linha da tabela
            rows = table.select('tr')[1:]  # Pular cabeçalho
            
            for row in rows:
                cols = [td.get_text(strip=True) for td in row.select('td')]
                if len(cols) >= 3:
                    metric_name = cols[1]
                    fighter1_val = cols[0]
                    fighter2_val = cols[2]
                    
                    # Salvar dados brutos
                    stats[f"{metric_name}_1"] = fighter1_val
                    stats[f"{metric_name}_2"] = fighter2_val
                    
                    # Tentar extrair números (ex: "3 of 5" -> 3, 5)
                    if ' of ' in fighter1_val and ' of ' in fighter2_val:
                        try:
                            f1_made, f1_attempt = map(int, fighter1_val.split(' of '))
                            f2_made, f2_attempt = map(int, fighter2_val.split(' of '))
                            
                            stats[f"{metric_name}_1_made"] = f1_made
                            stats[f"{metric_name}_1_attempt"] = f1_attempt
                            stats[f"{metric_name}_2_made"] = f2_made
                            stats[f"{metric_name}_2_attempt"] = f2_attempt
                            stats[f"{metric_name}_diff"] = f1_made - f2_made
                            
                        except:
                            pass
        
        print(f"    ✅ Coletado: {stats.get('fighter_1', '?')} vs {stats.get('fighter_2', '?')}")
        print(f"    📈 Estatísticas: {len([k for k in stats.keys() if k not in ['fight_url', 'fighter_1', 'fighter_2']])} dados")
        
        return stats
        
    except Exception as e:
        print(f"    ❌ Erro na luta {fight_url}: {e}")
        return {"fight_url": fight_url}

def scrape_real_fight_stats(events_csv="data/ufc_fights_basic.csv", out_csv="data/ufc_fights_real_data.csv"):
    """Coleta dados reais de todas as lutas"""
    try:
        df_events = pd.read_csv(events_csv)
        print(f"📊 Eventos carregados: {len(df_events)}")
    except Exception as e:
        print(f"❌ Erro ao carregar eventos: {e}")
        return pd.DataFrame()
    
    all_stats = []
    processed_urls = set()
    
    if "event_url" in df_events.columns:
        event_urls = df_events["event_url"].unique()
        print(f"🎯 Processando {len(event_urls)} eventos...")
    else:
        print("❌ Coluna 'event_url' não encontrada")
        return pd.DataFrame()
    
    # Coletar URLs de lutas de cada evento
    fight_urls = []
    for i, event_url in enumerate(event_urls):
        print(f"\n📅 Evento {i+1}/{len(event_urls)}: {event_url}")
        try:
            r = requests.get(event_url, timeout=10)
            soup = BeautifulSoup(r.content, "lxml")
            
            # Encontrar todas as lutas do evento
            for a in soup.find_all('a', href=True):
                href = a['href']
                if '/fight-details/' in href and href not in processed_urls:
                    fight_urls.append(href)
                    processed_urls.add(href)
            
            print(f"  🔗 {len(fight_urls)} lutas acumuladas")
            time.sleep(1)
        except Exception as e:
            print(f"  ❌ Erro no evento: {e}")
    
    print(f"\n🥊 TOTAL DE {len(fight_urls)} LUTAS PARA COLETAR")
    
    # Coletar dados detalhados de cada luta
    for i, fight_url in enumerate(fight_urls):
        print(f"\n🔍 Luta {i+1}/{len(fight_urls)}")
        try:
            fight_stats = parse_fight_page_correct(fight_url)
            all_stats.append(fight_stats)
        except Exception as e:
            print(f"❌ Erro na luta {i+1}: {e}")
        
        time.sleep(1)  # Respeitar o servidor
    
    # Salvar dados
    if all_stats:
        df_real = pd.DataFrame(all_stats)
        os.makedirs("data", exist_ok=True)
        df_real.to_csv(out_csv, index=False)
        
        print(f"\n🎉 DADOS REAIS COLETADOS!")
        print(f"💾 Salvo: {out_csv}")
        print(f"📊 Total: {len(df_real)} lutas com dados reais")
        print(f"📈 Colunas coletadas: {len(df_real.columns)}")
        print(f"🔢 Dados numéricos: {len([c for c in df_real.columns if 'made' in c or 'attempt' in c])}")
        
        # Mostrar amostra
        print("\n📋 Amostra dos dados:")
        sample_cols = [c for c in df_real.columns if any(x in c for x in ['fighter', 'winner', 'method', 'strike', 'takedown'])]
        print(df_real[sample_cols].head(3) if sample_cols else df_real.head(3))
        
        return df_real
    else:
        print("❌ Nenhum dado coletado")
        return pd.DataFrame()

if __name__ == "__main__":
    scrape_real_fight_stats()