#!/usr/bin/env python3
import urllib.request
import re
import json
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-AU,en;q=0.9"
}

with open("colorbond_modular_fencing_australia.json", "r", encoding="utf-8") as f:
    contractors = json.load(f)

extracted_all = []

for idx, c in enumerate(contractors, start=1):
    name = c["Company Name"]
    gmaps_url = c.get("Google Maps URL", "")
    pid = gmaps_url.split("place_id:")[-1] if "place_id:" in gmaps_url else ""
    
    print(f"\n[{idx}/20] Fetching real data for: {name} (Place ID: {pid})...")
    
    place_data = {
        "index": idx,
        "name": name,
        "slug": c.get("slug", ""),
        "place_id": pid,
        "rating": c.get("Rating", 5.0),
        "reviews_count": c.get("Reviews Count", 0),
        "city": c.get("City / Region", ""),
        "address": c.get("Address", ""),
        "phone": c.get("Phone", ""),
        "gmaps_url": gmaps_url,
        "reviews": [],
        "real_photos": []
    }
    
    if not pid:
        extracted_all.append(place_data)
        continue
        
    try:
        url = f"https://www.google.com/maps/place/?q=place_id:{pid}&hl=en"
        req = urllib.request.Request(url, headers=HEADERS)
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        m = re.findall(r"/maps/preview/place[^\x22\x27\s]+", html)
        if not m:
            print("  -> No preview place URL found, skipping preview parse")
            extracted_all.append(place_data)
            continue
            
        u = "https://www.google.com" + m[0].replace("&amp;", "&")
        req2 = urllib.request.Request(u, headers=HEADERS)
        res2 = urllib.request.urlopen(req2, timeout=10).read().decode("utf-8", errors="ignore")
        
        raw_json = "\n".join(res2.splitlines()[1:])
        pdata = json.loads(raw_json)
        place = pdata[6]
        
        # Check place[175][9][0][0] for reviews
        if len(place) > 175 and place[175] and len(place[175]) > 9 and place[175][9]:
            rev_block = place[175][9][0][0] if len(place[175][9]) > 0 and len(place[175][9][0]) > 0 else []
            for item in rev_block:
                r = item[0]
                
                # Author
                author = "Local Homeowner"
                try:
                    if len(r) > 1 and r[1] and len(r[1]) > 4 and len(r[1][4]) > 5:
                        author = r[1][4][5][0]
                except:
                    pass
                
                # Rating
                rating_val = 5
                try:
                    if len(r) > 2 and r[2] and len(r[2]) > 0 and isinstance(r[2][0], list):
                        rating_val = r[2][0][0]
                except:
                    pass
                
                # Date & text
                flat = []
                def flatten(o):
                    if isinstance(o, list):
                        for sub in o: flatten(sub)
                    elif isinstance(o, str):
                        flat.append(o)
                flatten(item)
                
                date_val = next((s for s in flat if "ago" in s.lower() and len(s) < 30), "Recent client")
                
                texts = [s for s in flat if not s.startswith("http") and not s.startswith("2ahU") and not s.startswith("0x") and not s.startswith("//") and len(s) > 25 and "ago" not in s]
                text_val = max(texts, key=len, default="")
                
                # Photos in review
                review_photos = [s for s in flat if s.startswith("https://lh3.googleusercontent.com") and "=k-no" in s]
                for p_url in review_photos:
                    if p_url not in place_data["real_photos"]:
                        place_data["real_photos"].append(p_url)
                        
                if text_val:
                    place_data["reviews"].append({
                        "author": author,
                        "rating": rating_val,
                        "date": date_val,
                        "text": text_val
                    })
                    print(f"  + Review by {author} ({rating_val}★, {date_val}): {text_val[:65]}...")
                    
        print(f"  Total extracted reviews: {len(place_data['reviews'])}, real photos: {len(place_data['real_photos'])}")
        
    except Exception as e:
        print(f"  Error fetching: {e}")
        
    extracted_all.append(place_data)
    time.sleep(1)

with open("contractors_real_reviews.json", "w", encoding="utf-8") as f:
    json.dump(extracted_all, f, ensure_ascii=False, indent=2)

print("\nSaved all real data to contractors_real_reviews.json!")
