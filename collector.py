#!/usr/bin/env python3
import urllib.request
import urllib.parse
import re
import json
import time
import subprocess
import csv
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-AU,en;q=0.9'
}

CITIES = [
    # WA
    'Perth WA', 'Joondalup WA', 'Mandurah WA', 'Rockingham WA', 'Bunbury WA', 'Armadale WA',
    'Midland WA', 'Fremantle WA', 'Wanneroo WA', 'Busselton WA', 'Geraldton WA', 'Albany WA',
    # SA
    'Adelaide SA', 'Mount Barker SA', 'Gawler SA', 'Salisbury SA', 'Morphett Vale SA',
    'Port Adelaide SA', 'Victor Harbor SA', 'Mount Gambier SA',
    # VIC
    'Melbourne VIC', 'Geelong VIC', 'Frankston VIC', 'Dandenong VIC', 'Werribee VIC',
    'Ballarat VIC', 'Bendigo VIC', 'Mornington VIC', 'Ringwood VIC', 'Pakenham VIC',
    'Sunbury VIC', 'Melton VIC', 'Traralgon VIC', 'Warrnambool VIC', 'Shepparton VIC',
    # NSW
    'Sydney NSW', 'Parramatta NSW', 'Penrith NSW', 'Blacktown NSW', 'Campbelltown NSW',
    'Liverpool NSW', 'Castle Hill NSW', 'Newcastle NSW', 'Central Coast NSW', 'Wollongong NSW',
    'Maitland NSW', 'Wagga Wagga NSW', 'Dubbo NSW', 'Tamworth NSW', 'Coffs Harbour NSW',
    'Port Macquarie NSW', 'Orange NSW', 'Bathurst NSW',
    # QLD
    'Brisbane QLD', 'Gold Coast QLD', 'Sunshine Coast QLD', 'Ipswich QLD', 'Logan QLD',
    'Toowoomba QLD', 'Cairns QLD', 'Townsville QLD', 'Caboolture QLD', 'Mackay QLD',
    'Rockhampton QLD', 'Bundaberg QLD', 'Hervey Bay QLD',
    # ACT & TAS
    'Canberra ACT', 'Belconnen ACT', 'Hobart TAS', 'Launceston TAS'
]

KEYWORDS = [
    'colorbond fencing',
    'modular fencing',
    'colorbond gates and fencing',
    'modular walls fencing',
    'colorbond fencing contractor',
    'colorbond fence builder'
]

CSV_FILE = 'colorbond_modular_fencing_australia.csv'
JSON_FILE = 'colorbond_modular_fencing_australia.json'

AGGREGATORS = [
    'facebook.com', 'fb.com', 'fb.me', 'instagram.com',
    'hipages.com.au', 'oneflare.com.au', 'truelocal.com.au', 'yellowpages.com.au',
    'localsearch.com.au', 'womo.com.au', 'serviceseeking.com.au', 'bark.com',
    'airtasker.com', 'gumtree.com.au', 'australianplanet.com', 'hotfrog.com.au',
    'servicefinder.com.au', 'cylex-australia.com', 'startlocal.com.au',
    'business.site', 'wixsite.com', 'site123.me', 'weebly.com', 'wordpress.com'
]

lock = threading.Lock()
seen_place_ids = set()
results = []

def check_website(url):
    """
    Returns (matches_criteria: bool, status_reason: str)
    Criteria:
      - No website ("Сайта нет")
      - Facebook/Instagram ("Страница в Facebook / Instagram")
      - Aggregator ("Сайт на агрегаторе")
      - Doesn't open / broken ("Сайт не открывается")
    """
    if not url:
        return True, 'Сайта нет'
    
    u_lower = url.lower()
    
    # 1. Social networks (Facebook / Instagram)
    for fb in ['facebook.com', 'fb.com', 'fb.me', 'instagram.com']:
        if fb in u_lower:
            return True, f'Страница в Facebook / Instagram ({url})'
    
    # 2. Aggregators & Directories
    for aggr in AGGREGATORS:
        if aggr in u_lower:
            return True, f'Сайт на агрегаторе ({aggr})'
    
    # 3. Check if normal custom website opens or fails
    try:
        res = subprocess.run([
            'curl', '-s', '-L', '-o', '/dev/null', '-w', '%{http_code}',
            '--max-time', '4',
            '-A', HEADERS['User-Agent'],
            url
        ], capture_output=True, text=True)
        code = res.stdout.strip()
        
        if code in ['200', '301', '302', '307', '308']:
            return False, f'Рабочий сайт (HTTP {code})'
        elif code in ['000', '']:
            return True, 'Сайт не открывается (Timeout / DNS error / Недоступен)'
        else:
            return True, f'Сайт не открывается (Ошибка HTTP {code})'
    except Exception as e:
        return True, f'Сайт не открывается ({type(e).__name__})'

def get_latest_review(place_id):
    """
    Fetches place preview and checks recency of the latest review.
    Returns (is_recent: bool, latest_review_str: str)
    Criteria: last review not older than 6 months.
    """
    url = f'https://www.google.com/maps/place/?q=place_id:{place_id}&hl=en'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        html = urllib.request.urlopen(req, timeout=7).read().decode('utf-8', errors='ignore')
        m = re.findall(r'/maps/preview/place[^\"\'\s]+', html)
        if not m:
            return True, 'Дата не указана (активен)'
        u = 'https://www.google.com' + m[0].replace('&amp;', '&')
        req2 = urllib.request.Request(u, headers=HEADERS)
        res2 = urllib.request.urlopen(req2, timeout=7).read().decode('utf-8', errors='ignore')
        
        dates = re.findall(r'(\b\d+\s+(?:month|week|day|year|hour)s?\s+ago\b|\ba\s+(?:month|week|day|year)\s+ago\b)', res2, re.I)
        order = {'hour': 0, 'day': 1, 'week': 2, 'month': 3, 'year': 14}
        found = []
        for d in dates:
            clean = d.lower()
            m_d = re.search(r'(\d+|a|an)\s+(hour|day|week|month|year)s?\s+ago', clean)
            if m_d:
                num, unit = m_d.group(1), m_d.group(2)
                if unit in ['hour', 'day', 'week']:
                    score = order[unit]
                elif unit == 'month':
                    n = 1 if num in ['a', 'an'] else int(num)
                    score = 3 if n == 1 else (n + 2)
                else:
                    score = 14
                found.append((score, clean))
        
        if not found:
            return True, 'Дата не указана'
        
        found.sort()
        best_score, best_str = found[0]
        # <= 6 months means score <= 8 (month 6 is score 8; 7 months is score 9)
        is_recent = (best_score <= 8)
        return is_recent, best_str
    except Exception as e:
        return True, f'Ошибка проверки ({e})'

def save_data():
    keys = ['Company Name', 'Rating', 'Reviews Count', 'Latest Review', 'Website Status', 'Website URL', 'Phone', 'Address', 'City / Search Region', 'Google Maps URL', 'Place ID']
    with lock:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for item in results:
                writer.writerow(item)
        
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

def process_query(city, kw):
    query = f'{kw} {city}'
    search_url = f'https://www.google.com/maps/search/{urllib.parse.quote(query)}/?hl=en'
    req = urllib.request.Request(search_url, headers=HEADERS)
    try:
        html = urllib.request.urlopen(req, timeout=8).read().decode('utf-8', errors='ignore')
        m = re.findall(r'/search\?tbm=map[^\"\'\s]+', html)
        if not m:
            return
        map_url = 'https://www.google.com' + m[0].replace('&amp;', '&')
        req2 = urllib.request.Request(map_url, headers=HEADERS)
        res2 = urllib.request.urlopen(req2, timeout=8).read().decode('utf-8', errors='ignore')
        
        raw_json = '\n'.join(res2.splitlines()[1:])
        data = json.loads(raw_json)
        items = data[64] if len(data) > 64 and data[64] else []
        
        for it in items:
            if not it or len(it) < 2 or not it[1]:
                continue
            biz = it[1]
            name = biz[11] if len(biz) > 11 else None
            if not name:
                continue
            
            place_id = biz[78] if len(biz) > 78 else None
            if not place_id:
                continue
            
            with lock:
                if place_id in seen_place_ids:
                    continue
                seen_place_ids.add(place_id)
            
            # Rating & Reviews
            rating_info = biz[4] if len(biz) > 4 and biz[4] else None
            if not rating_info or len(rating_info) < 9:
                continue
            rating = rating_info[7]
            reviews = rating_info[8]
            
            if rating is None or reviews is None:
                continue
            
            # Filter 1: rating 4.6 - 5.0, reviews 20 - 200
            try:
                r_val = float(rating)
                c_val = int(reviews)
            except:
                continue
            
            if not (4.6 <= r_val <= 5.0 and 20 <= c_val <= 200):
                continue
            
            # Filter 2: Website status
            website = biz[7][0] if len(biz) > 7 and biz[7] else None
            is_target_web, web_reason = check_website(website)
            if not is_target_web:
                continue
            
            # Filter 3: Review recency <= 6 months
            is_recent, latest_rev_str = get_latest_review(place_id)
            if not is_recent:
                continue
            
            phone = biz[178][0][0] if len(biz) > 178 and biz[178] and biz[178][0] else None
            address = biz[18] if len(biz) > 18 else (biz[39] if len(biz) > 39 else None)
            maps_url = f'https://www.google.com/maps/place/?q=place_id:{place_id}'
            
            record = {
                'Company Name': name,
                'Rating': r_val,
                'Reviews Count': c_val,
                'Latest Review': latest_rev_str,
                'Website Status': web_reason,
                'Website URL': website or 'Отсутствует',
                'Phone': phone or 'Не указан',
                'Address': address or 'Не указан',
                'City / Search Region': city,
                'Google Maps URL': maps_url,
                'Place ID': place_id
            }
            
            with lock:
                results.append(record)
                print(f'[{len(results)}] MATCH: {name} | ★{r_val} ({c_val}) | Last review: {latest_rev_str} | Site: {web_reason} | Phone: {phone}')
                save_data()
                
    except Exception as e:
        pass

def main():
    print('Starting multi-threaded collector across Australia for Colorbond & Modular fencing...')
    tasks = []
    for city in CITIES:
        for kw in KEYWORDS:
            tasks.append((city, kw))
    
    print(f'Total search tasks queued: {len(tasks)}')
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_query, city, kw) for city, kw in tasks]
        for f in as_completed(futures):
            pass
    
    save_data()
    print(f'\nFinished all tasks! Total qualified companies collected: {len(results)}')

if __name__ == '__main__':
    main()
