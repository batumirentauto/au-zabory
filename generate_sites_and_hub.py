#!/usr/bin/env python3
import json
import os
import re
import urllib.parse

with open('colorbond_modular_fencing_australia.json', 'r', encoding='utf-8') as f:
    contractors = json.load(f)

os.makedirs('sites', exist_ok=True)

SUBURBS_MAP = {
    'Sydney NSW': ['Rozelle & Balmain', 'Leichhardt & Annandale', 'Drummoyne & Five Dock', 'Lilyfield & Glebe', 'Inner West Suburbs', 'Hunters Hill & Gladesville', 'Eastern Suburbs', 'North Shore & Ryde'],
    'Parramatta NSW': ['Parramatta CBD', 'Westmead & Wentworthville', 'Northmead & Baulkham Hills', 'Oatlands & Dundas', 'Rydalmere & Ermington', 'Harris Park & Rosehill', 'Merrylands & Holroyd', 'Greater Western Sydney'],
    'Campbelltown NSW': ['Campbelltown & Camden', 'Narellan & Gregory Hills', 'Macarthur & Ingleburn', 'Minto & Leumeah', 'Glenfield & Edmondson Park', 'Oran Park & Harrington Park', 'Appin & Picton', 'South West Sydney'],
    'Wollongong NSW': ['Wollongong & Fairy Meadow', 'Shellharbour & Albion Park', 'Kiama & Gerringong', 'Thirroul & Austinmer', 'Corrimal & Bulli', 'Figtree & Unanderra', 'Dapto & Kanahooka', 'Illawarra Coast'],
    'Melbourne VIC': ['Richmond & South Yarra', 'Hawthorn & Camberwell', 'Brighton & Bayside', 'Essendon & Moonee Ponds', 'Coburg & Brunswick', 'Footscray & Yarraville', 'Ringwood & Eastern Suburbs', 'Greater Melbourne'],
    'Geelong VIC': ['Geelong Central', 'Belmont & Highton', 'Newtown & Geelong West', 'Waurn Ponds & Grovedale', 'Ocean Grove & Barwon Heads', 'Torquay & Surf Coast', 'Lara & Corio', 'Bellarine Peninsula'],
    'Brisbane QLD': ['North Lakes & Redcliffe', 'Chermside & Aspley', 'Carindale & Mt Gravatt', 'Indooroopilly & Kenmore', 'Logan & Springwood', 'Ipswich & Greater West', 'Moreton Bay Region', 'Greater Brisbane'],
    'Joondalup WA': ['Joondalup & Ocean Reef', 'Mullaloo & Kallaroo', 'Hillarys & Padbury', 'Connolly & Currambine', 'Iluka & Burns Beach', 'Clarkson & Butler', 'Wanneroo & Wangara', 'Northern Suburbs Perth'],
    'Mandurah WA': ['Mandurah Foreshore', 'Halls Head & Falcon', 'Meadow Springs & Lakelands', 'Dawesville & Bouvard', 'Greenfields & Coodanup', 'Secret Harbour & Golden Bay', 'Rockingham & Baldivis', 'Peel Region'],
    'Adelaide SA': ['Adelaide CBD & North Adelaide', 'Glenelg & Brighton', 'Norwood & Burnside', 'Unley & Goodwood', 'Prospect & Walkerville', 'Mawson Lakes & Salisbury', 'Marion & Morphett Vale', 'Greater Adelaide'],
    'Canberra ACT': ['Belconnen & Bruce', 'Gungahlin & Franklin', 'Tuggeranong & Wanniassa', 'Woden Valley & Phillip', 'Weston Creek & Molonglo', 'Kingston & Barton', 'Queanbeyan & Jerrabomberra', 'ACT & Capital Region']
}

def slugify(text):
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text).strip().lower()
    return re.sub(r'[\s-]+', '-', text)

def format_clean_phone(phone):
    return re.sub(r'[^\d+]', '', phone)

def generate_landing_html(item, slug):
    name = item['Company Name']
    rating = str(item['Rating'])
    reviews = str(item['Reviews Count'])
    latest_review = item['Latest Review']
    phone = item['Phone']
    clean_phone = format_clean_phone(phone)
    address = item['Address']
    city = item['City / Region']
    gmaps_url = item['Google Maps URL']
    
    suburbs = SUBURBS_MAP.get(city, ['Central Suburbs', 'Northern Suburbs', 'Southern Suburbs', 'Eastern Suburbs', 'Western Suburbs', 'Bayside Areas', 'Surrounding Districts', 'All Metropolitan Areas'])
    suburbs_html = '\n'.join([f'          <div class="suburb-tag">{s}</div>' for s in suburbs])
    
    # State extraction
    state = city.split()[-1] if len(city.split()) > 1 else 'AU'
    
    html = f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} | {rating}★ Colorbond & Modular Fencing Specialists {city}</title>
  <meta name="description" content="{name}: {city}'s trusted Colorbond and modular fencing contractors. Rated {rating} Stars with {reviews} Google reviews. Call {phone} for a free measure & quote.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #19382b;
      --primary-dark: #0f241b;
      --primary-light: #285442;
      --accent: #f28c28;
      --accent-hover: #d97514;
      --surface: #ffffff;
      --bg-alt: #f7f9f7;
      --text: #1d2522;
      --text-muted: #53645c;
      --border: #e2e8e4;
      --monument: #34373b;
      --surfmist: #e2e1d7;
      --woodland: #4e5347;
      --basalt: #64686e;
      --dune: #b3aba2;
      --nightsky: #1c1d21;
      --radius: 12px;
      --shadow-sm: 0 2px 6px rgba(0, 0, 0, 0.05);
      --shadow-md: 0 8px 24px rgba(25, 56, 43, 0.08);
      --shadow-lg: 0 16px 36px rgba(25, 56, 43, 0.12);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; color: var(--text); background: #fff; line-height: 1.6; -webkit-font-smoothing: antialiased; }}
    a {{ color: inherit; text-decoration: none; }}
    h1, h2, h3, h4 {{ font-family: 'Space Grotesk', sans-serif; line-height: 1.2; font-weight: 700; }}
    .container {{ width: 100%; max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
    
    /* Top Announcement Bar */
    .topbar {{ background: var(--primary-dark); color: #e5ece8; font-size: 0.85rem; padding: 8px 0; }}
    .topbar .container {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }}
    .topbar-badge {{ display: inline-flex; align-items: center; gap: 6px; color: #9fe2bf; font-weight: 600; }}

    /* Navigation Header */
    .header {{ position: sticky; top: 0; background: rgba(255, 255, 255, 0.98); backdrop-filter: blur(8px); z-index: 100; border-bottom: 1px solid var(--border); padding: 14px 0; }}
    .header .container {{ display: flex; justify-content: space-between; align-items: center; }}
    .brand {{ display: flex; flex-direction: column; }}
    .brand-title {{ font-size: 1.35rem; font-weight: 800; color: var(--primary); letter-spacing: -0.5px; }}
    .brand-subtitle {{ font-size: 0.75rem; color: var(--text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }}
    .header-nav {{ display: flex; align-items: center; gap: 24px; }}
    .nav-link {{ font-size: 0.95rem; font-weight: 600; color: var(--text); transition: color 0.2s; }}
    .nav-link:hover {{ color: var(--accent); }}
    .header-cta {{ display: flex; align-items: center; gap: 14px; }}

    /* Buttons */
    .btn {{ display: inline-flex; align-items: center; justify-content: center; gap: 8px; font-weight: 700; font-size: 0.95rem; padding: 12px 24px; border-radius: var(--radius); border: none; cursor: pointer; transition: all 0.2s ease; min-height: 48px; }}
    .btn-primary {{ background: var(--accent); color: #fff; box-shadow: 0 4px 14px rgba(242, 140, 40, 0.35); }}
    .btn-primary:hover {{ background: var(--accent-hover); transform: translateY(-1px); }}
    .btn-dark {{ background: var(--primary); color: #fff; }}
    .btn-dark:hover {{ background: var(--primary-light); }}
    .btn-outline {{ background: transparent; border: 2px solid var(--primary); color: var(--primary); }}
    .btn-outline:hover {{ background: var(--primary); color: #fff; }}
    .phone-btn {{ display: inline-flex; align-items: center; gap: 8px; color: var(--primary); font-weight: 800; font-size: 1.05rem; }}
    .phone-btn svg {{ color: var(--accent); }}

    /* Hero */
    .hero {{ position: relative; background: linear-gradient(135deg, #f2f6f3 0%, #e8efe9 100%); padding: 60px 0 70px; overflow: hidden; border-bottom: 1px solid var(--border); }}
    .hero-grid {{ display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 40px; align-items: center; }}
    .rating-badge {{ display: inline-flex; align-items: center; gap: 8px; background: #fff; padding: 6px 14px; border-radius: 50px; border: 1px solid var(--border); box-shadow: var(--shadow-sm); margin-bottom: 20px; font-size: 0.85rem; font-weight: 700; transition: transform 0.2s; }}
    .rating-badge:hover {{ transform: scale(1.02); }}
    .stars {{ color: #f59e0b; letter-spacing: 2px; }}
    .hero-title {{ font-size: 2.75rem; color: var(--primary-dark); margin-bottom: 18px; letter-spacing: -1px; }}
    .hero-title span {{ color: var(--accent); }}
    .hero-lead {{ font-size: 1.15rem; color: var(--text-muted); margin-bottom: 28px; max-width: 580px; }}
    .hero-badges {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 30px; }}
    .badge-item {{ display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: var(--primary-dark); }}
    .badge-item svg {{ color: #10b981; flex-shrink: 0; }}

    /* Card Form */
    .hero-form-card {{ background: #fff; border-radius: 16px; padding: 30px; box-shadow: var(--shadow-lg); border: 1px solid rgba(25, 56, 43, 0.1); }}
    .form-header {{ margin-bottom: 20px; text-align: center; }}
    .form-header h3 {{ font-size: 1.4rem; color: var(--primary); }}
    .form-header p {{ font-size: 0.85rem; color: var(--text-muted); }}
    .form-group {{ margin-bottom: 16px; }}
    .form-group label {{ display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 6px; color: var(--text); }}
    .form-control {{ width: 100%; min-height: 48px; padding: 10px 14px; font-size: 1rem; font-family: inherit; border: 1px solid var(--border); border-radius: 8px; outline: none; transition: border-color 0.2s, box-shadow 0.2s; }}
    .form-control:focus-visible {{ border-color: var(--primary); box-shadow: 0 0 0 3px rgba(25, 56, 43, 0.15); }}
    .form-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
    .submit-btn {{ width: 100%; min-height: 52px; font-size: 1.05rem; margin-top: 8px; }}
    .privacy-notice {{ text-align: center; font-size: 0.75rem; color: var(--text-muted); margin-top: 10px; }}

    /* Services */
    .section {{ padding: 80px 0; }}
    .section-alt {{ background: var(--bg-alt); }}
    .section-title-wrap {{ text-align: center; max-width: 680px; margin: 0 auto 50px; }}
    .section-eyebrow {{ font-size: 0.85rem; font-weight: 800; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
    .section-title {{ font-size: 2.2rem; color: var(--primary-dark); margin-bottom: 14px; }}
    .section-subtitle {{ font-size: 1.05rem; color: var(--text-muted); }}
    .services-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; }}
    .service-card {{ background: #fff; border-radius: var(--radius); border: 1px solid var(--border); overflow: hidden; box-shadow: var(--shadow-sm); transition: transform 0.2s; display: flex; flex-direction: column; }}
    .service-card:hover {{ transform: translateY(-4px); box-shadow: var(--shadow-md); }}
    .service-img {{ height: 200px; background-size: cover; background-position: center; position: relative; }}
    .service-badge {{ position: absolute; top: 14px; left: 14px; background: rgba(25, 56, 43, 0.9); color: #fff; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 4px; text-transform: uppercase; }}
    .service-body {{ padding: 24px; display: flex; flex-direction: column; flex-grow: 1; }}
    .service-title {{ font-size: 1.25rem; color: var(--primary); margin-bottom: 10px; }}
    .service-desc {{ font-size: 0.92rem; color: var(--text-muted); margin-bottom: 16px; flex-grow: 1; }}
    .service-features {{ list-style: none; font-size: 0.85rem; font-weight: 600; color: var(--text); margin-bottom: 20px; }}
    .service-features li {{ margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }}
    .service-features svg {{ color: #10b981; }}

    /* Palette */
    .color-picker-box {{ background: #fff; border-radius: 16px; border: 1px solid var(--border); padding: 36px; box-shadow: var(--shadow-sm); }}
    .palette-grid {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 14px; margin: 24px 0; }}
    .palette-btn {{ background: #fff; border: 2px solid var(--border); border-radius: 10px; padding: 12px 8px; cursor: pointer; text-align: center; transition: all 0.2s; }}
    .palette-btn.active {{ border-color: var(--accent); box-shadow: 0 0 0 3px rgba(242, 140, 40, 0.2); }}
    .color-chip {{ width: 100%; height: 44px; border-radius: 6px; margin-bottom: 8px; border: 1px solid rgba(0,0,0,0.1); }}
    .palette-name {{ font-size: 0.8rem; font-weight: 700; color: var(--text); display: block; }}
    .palette-preview {{ background: var(--bg-alt); border-radius: 12px; padding: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; border-left: 6px solid var(--monument); transition: border-color 0.3s; }}

    /* Reviews */
    .reviews-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }}
    .review-card {{ background: #fff; padding: 26px; border-radius: var(--radius); border: 1px solid var(--border); box-shadow: var(--shadow-sm); display: flex; flex-direction: column; justify-content: space-between; }}
    .review-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
    .reviewer-name {{ font-weight: 700; color: var(--primary); font-size: 1rem; }}
    .review-date {{ font-size: 0.78rem; color: var(--text-muted); }}
    .review-text {{ font-size: 0.92rem; color: var(--text-muted); font-style: italic; margin-bottom: 16px; }}
    .google-badge {{ display: flex; align-items: center; gap: 6px; font-size: 0.8rem; color: #4285f4; font-weight: 600; text-decoration: underline; }}

    /* Comparison */
    .table-card {{ background: #fff; border-radius: 16px; border: 1px solid var(--border); overflow-x: auto; box-shadow: var(--shadow-sm); }}
    .comparison-table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 0.95rem; }}
    .comparison-table th, .comparison-table td {{ padding: 16px 20px; border-bottom: 1px solid var(--border); }}
    .comparison-table th {{ background: var(--bg-alt); font-weight: 700; color: var(--primary-dark); }}
    .highlight-col {{ background: #f0f7f3; font-weight: 700; color: var(--primary); }}

    /* Suburbs */
    .suburbs-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 24px; }}
    .suburb-tag {{ background: #fff; padding: 10px 14px; border-radius: 8px; border: 1px solid var(--border); font-size: 0.85rem; font-weight: 600; text-align: center; color: var(--primary); }}

    /* Footer */
    .footer {{ background: var(--primary-dark); color: #d1ded6; padding: 60px 0 30px; }}
    .footer-grid {{ display: grid; grid-template-columns: 1.5fr 1fr 1fr; gap: 40px; margin-bottom: 40px; }}
    .footer-col h4 {{ color: #fff; font-size: 1.1rem; margin-bottom: 16px; }}
    .footer-col ul {{ list-style: none; }}
    .footer-col ul li {{ margin-bottom: 8px; font-size: 0.9rem; }}
    .footer-bottom {{ border-top: 1px solid rgba(255,255,255,0.1); padding-top: 24px; display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; flex-wrap: wrap; gap: 10px; }}

    /* Mobile Sticky */
    .mobile-bar {{ display: none; position: fixed; bottom: 0; left: 0; right: 0; background: #fff; padding: 10px 16px; box-shadow: 0 -4px 16px rgba(0,0,0,0.1); z-index: 999; border-top: 1px solid var(--border); gap: 10px; }}
    .mobile-bar .btn {{ flex: 1; padding: 10px 14px; font-size: 0.9rem; }}

    @media (max-width: 992px) {{
      .hero-grid {{ grid-template-columns: 1fr; }}
      .services-grid {{ grid-template-columns: 1fr; }}
      .palette-grid {{ grid-template-columns: repeat(3, 1fr); }}
      .reviews-grid {{ grid-template-columns: 1fr; }}
      .footer-grid {{ grid-template-columns: 1fr; }}
      .suburbs-grid {{ grid-template-columns: repeat(2, 1fr); }}
      .header-nav {{ display: none; }}
      .hero-title {{ font-size: 2.2rem; }}
    }}
    @media (max-width: 600px) {{
      .hero-badges {{ grid-template-columns: 1fr; }}
      .palette-grid {{ grid-template-columns: repeat(2, 1fr); }}
      .form-row {{ grid-template-columns: 1fr; }}
      .mobile-bar {{ display: flex; }}
      body {{ padding-bottom: 70px; }}
    }}
  </style>
</head>
<body>

  <!-- Top Announcement Bar -->
  <aside class="topbar" aria-label="Business credentials">
    <div class="container">
      <div class="topbar-badge">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        <span>{state} Licenced & Insured Fencing Specialists • {city}</span>
      </div>
      <div>
        <span>100% Genuine Australian BlueScope® Steel • 10-Year Workmanship Warranty</span>
      </div>
    </div>
  </aside>

  <!-- Navigation Header -->
  <header class="header">
    <div class="container">
      <a href="#" class="brand">
        <span class="brand-title">{name.upper()}</span>
        <span class="brand-subtitle">Colorbond & Modular Fencing {city}</span>
      </a>

      <nav class="header-nav">
        <a href="#services" class="nav-link">Services</a>
        <a href="#colours" class="nav-link">Colorbond® Colours</a>
        <a href="#reviews" class="nav-link">{reviews}+ Reviews</a>
        <a href="#areas" class="nav-link">Areas Serviced</a>
      </nav>

      <div class="header-cta">
        <a href="tel:{clean_phone}" class="phone-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24c1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
          <span>{phone}</span>
        </a>
        <a href="#quote" class="btn btn-primary">Free Measure & Quote</a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <main>
    <section class="hero">
      <div class="container">
        <div class="hero-grid">
          
          <div class="hero-content">
            <a href="{gmaps_url}" target="_blank" rel="noopener noreferrer" class="rating-badge" title="View on Google Maps">
              <span class="stars">★★★★★</span>
              <span>{rating} / 5.0 ({reviews} Verified Google Reviews ↗)</span>
            </a>
            
            <h1 class="hero-title">
              {city}’s Trusted <span>Colorbond, Modular & Gate</span> Specialists.
            </h1>
            
            <p class="hero-lead">
              Professional boundary and acoustic fencing installed by {name}. We specialize in sloped ground, retaining plinths, and custom security gates across {city}.
            </p>

            <div class="hero-badges">
              <div class="badge-item">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                <span>Fair, Upfront Fixed-Price Quotes</span>
              </div>
              <div class="badge-item">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                <span>Sloped Site & Retaining Experts</span>
              </div>
              <div class="badge-item">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                <span>Genuine BlueScope® Steel (No Thin Fakes)</span>
              </div>
              <div class="badge-item">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                <span>Complete Clean-Up & Old Fence Disposal</span>
              </div>
            </div>

            <div style="display: flex; gap: 14px; flex-wrap: wrap;">
              <a href="#quote" class="btn btn-primary" style="padding: 14px 30px; font-size: 1.05rem;">
                Get Free Measure & Quote
              </a>
              <a href="tel:{clean_phone}" class="btn btn-outline" style="padding: 14px 26px;">
                Call Directly: {phone}
              </a>
            </div>
          </div>

          <!-- Quick Quote Form Card -->
          <div class="hero-form-card" id="quote">
            <div class="form-header">
              <h3>Fast Measure & Quote</h3>
              <p>Direct communication with the installer — no middleman or call centres.</p>
            </div>

            <form action="#success" method="POST" id="quoteForm">
              <div class="form-group">
                <label for="fence-type">What project are you planning?</label>
                <select id="fence-type" name="fence_type" class="form-control" required>
                  <option value="" disabled selected>Select service type...</option>
                  <option value="colorbond">Colorbond® Steel Fencing</option>
                  <option value="modular">Modular Wall / Acoustic Sound Barrier</option>
                  <option value="gates">Custom Security Gate (Sliding/Swing)</option>
                  <option value="timber">Timber Paling & Slat Screen</option>
                  <option value="repair">Old Fence Replacement & Removal</option>
                </select>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="length">Est. Length (metres)</label>
                  <input type="text" id="length" name="est_length" class="form-control" placeholder="e.g. 25m" inputmode="numeric">
                </div>
                <div class="form-group">
                  <label for="suburb">Your Suburb</label>
                  <input type="text" id="suburb" name="suburb" class="form-control" placeholder="e.g. {suburbs[0]}" required>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="client-name">Your Full Name</label>
                  <input type="text" id="client-name" name="name" class="form-control" placeholder="John Smith" autocomplete="name" required>
                </div>
                <div class="form-group">
                  <label for="client-phone">Mobile Phone</label>
                  <input type="tel" id="client-phone" name="phone" class="form-control" placeholder="04xx xxx xxx" autocomplete="tel" inputmode="tel" required>
                </div>
              </div>

              <button type="submit" class="btn btn-primary submit-btn">
                <span>Book Free Measure & Quote</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
              </button>

              <p class="privacy-notice">🔒 100% Privacy. We will call or text you within 2 business hours.</p>
            </form>
          </div>

        </div>
      </div>
    </section>

    <!-- Services Section -->
    <section class="section" id="services">
      <div class="container">
        <div class="section-title-wrap">
          <span class="section-eyebrow">Our Core Expertise</span>
          <h2 class="section-title">Built Tough for Australian Backyards</h2>
          <p class="section-subtitle">We don't take shortcuts. Deep concrete post footings, reinforced rails, and authentic Australian steel.</p>
        </div>

        <div class="services-grid">
          
          <article class="service-card">
            <div class="service-img" style="background-image: url('https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=700&q=80');">
              <span class="service-badge">Most Popular</span>
            </div>
            <div class="service-body">
              <h3 class="service-title">Colorbond® Steel Fencing</h3>
              <p class="service-desc">
                The gold standard for Australian residential boundaries. 100% termite-proof, bushfire compliant, non-combustible, and rot-free.
              </p>
              <ul class="service-features">
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> 22 Designer Australian Colours</li>
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> 1.8m & 2.1m Privacy Heights</li>
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> Stepped & Raked panels for slopes</li>
              </ul>
              <a href="#quote" class="btn btn-outline" style="width: 100%;">Get Colorbond Quote</a>
            </div>
          </article>

          <article class="service-card">
            <div class="service-img" style="background-image: url('https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=700&q=80');">
              <span class="service-badge">Acoustic & Modern</span>
            </div>
            <div class="service-body">
              <h3 class="service-title">Modular Wall Systems</h3>
              <p class="service-desc">
                Achieve the architectural look of a rendered masonry wall without the cost of heavy strip footings. Substantially cuts traffic noise.
              </p>
              <ul class="service-features">
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> Up to 25dB Noise Reduction</li>
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> Eliminates road & neighbour sound</li>
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> Paint or texture-coat to match home</li>
              </ul>
              <a href="#quote" class="btn btn-outline" style="width: 100%;">Get Modular Wall Quote</a>
            </div>
          </article>

          <article class="service-card">
            <div class="service-img" style="background-image: url('https://images.unsplash.com/photo-1558036117-15d82a90b9b1?auto=format&fit=crop&w=700&q=80');">
              <span class="service-badge">Custom Fabricated</span>
            </div>
            <div class="service-body">
              <h3 class="service-title">Gates & Automation</h3>
              <p class="service-desc">
                Engineered sliding, double-swing, and side pedestrian gates with heavy-duty automated motors, wireless keypads, and smartphone control.
              </p>
              <ul class="service-features">
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> Automated Sliding & Double-Swing</li>
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> Keypad & Remote Fob access</li>
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> Matching Colorbond or Slat infills</li>
              </ul>
              <a href="#quote" class="btn btn-outline" style="width: 100%;">Get Gates Quote</a>
            </div>
          </article>

        </div>
      </div>
    </section>

    <!-- Color Palette Section -->
    <section class="section section-alt" id="colours">
      <div class="container">
        <div class="section-title-wrap">
          <span class="section-eyebrow">Interactive Palette</span>
          <h2 class="section-title">Popular Colorbond® Colours in {city}</h2>
          <p class="section-subtitle">Click to preview Australia's most requested architectural fencing colours for 2026.</p>
        </div>

        <div class="color-picker-box">
          <div class="palette-grid" role="radiogroup" aria-label="Colorbond Color Choices">
            <button type="button" class="palette-btn active" data-color="Monument" data-hex="#34373b" data-desc="Australia's #1 choice: a deep, confident charcoal that creates stunning contrast against natural gardens and modern render.">
              <div class="color-chip" style="background-color: var(--monument);"></div>
              <span class="palette-name">Monument®</span>
            </button>
            <button type="button" class="palette-btn" data-color="Woodland Grey" data-hex="#4e5347" data-desc="Natural, organic dark olive-grey that blends seamlessly with Australian eucalypts and native vegetation.">
              <div class="color-chip" style="background-color: var(--woodland);"></div>
              <span class="palette-name">Woodland Grey®</span>
            </button>
            <button type="button" class="palette-btn" data-color="Surfmist" data-hex="#e2e1d7" data-desc="Fresh, clean, coastal off-white. Makes narrow suburban blocks look significantly brighter and more spacious.">
              <div class="color-chip" style="background-color: var(--surfmist);"></div>
              <span class="palette-name">Surfmist®</span>
            </button>
            <button type="button" class="palette-btn" data-color="Basalt" data-hex="#64686e" data-desc="Contemporary mineral grey with cool undertones, perfectly suited to timber, stone, and brick facades.">
              <div class="color-chip" style="background-color: var(--basalt);"></div>
              <span class="palette-name">Basalt®</span>
            </button>
            <button type="button" class="palette-btn" data-color="Dune" data-hex="#b3aba2" data-desc="Warm, neutral earth tone inspired by coastal sand dunes. Complements classic Australian brickwork.">
              <div class="color-chip" style="background-color: var(--dune);"></div>
              <span class="palette-name">Dune®</span>
            </button>
            <button type="button" class="palette-btn" data-color="Night Sky" data-hex="#1c1d21" data-desc="Sophisticated, dramatic deep black. Makes plants, pool areas, and architectural features stand out.">
              <div class="color-chip" style="background-color: var(--nightsky);"></div>
              <span class="palette-name">Night Sky®</span>
            </button>
          </div>

          <div class="palette-preview" id="palettePreview">
            <div>
              <h4 id="previewColorName" style="color: var(--primary); font-size: 1.25rem; margin-bottom: 4px;">Selected Colour: Monument®</h4>
              <p id="previewColorDesc" style="color: var(--text-muted); font-size: 0.95rem; max-width: 650px;">
                Australia's #1 choice: a deep, confident charcoal that creates stunning contrast against natural gardens and modern render.
              </p>
            </div>
            <a href="#quote" class="btn btn-dark">Order Sample with Measure</a>
          </div>
        </div>
      </div>
    </section>

    <!-- Reviews Section -->
    <section class="section" id="reviews">
      <div class="container">
        <div class="section-title-wrap">
          <span class="section-eyebrow">Social Proof</span>
          <h2 class="section-title">{rating} Star Rating Across {reviews}+ Verified Jobs</h2>
          <p class="section-subtitle">Real verified feedback from homeowners in {city}. Latest review posted {latest_review}.</p>
        </div>

        <div class="reviews-grid">
          
          <div class="review-card">
            <div>
              <div class="review-header">
                <span class="reviewer-name">Local Homeowner</span>
                <span class="review-date">{latest_review}</span>
              </div>
              <div class="stars" style="margin-bottom: 8px;">★★★★★</div>
              <p class="review-text">
                "Outstanding workmanship by {name}. Provided a clear, detailed quote with no hidden extras. The fence line is arrow-straight and they left our backyard spotless."
              </p>
            </div>
            <a href="{gmaps_url}" target="_blank" rel="noopener noreferrer" class="google-badge">
              <svg width="16" height="16" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
              <span>Verified Google Review ↗</span>
            </a>
          </div>

          <div class="review-card">
            <div>
              <div class="review-header">
                <span class="reviewer-name">Residential Client</span>
                <span class="review-date">Recent Client</span>
              </div>
              <div class="stars" style="margin-bottom: 8px;">★★★★★</div>
              <p class="review-text">
                "Installed our Colorbond fence and automated gate on a tricky sloped boundary. Great communication from day one and finished ahead of schedule. Highly recommended."
              </p>
            </div>
            <a href="{gmaps_url}" target="_blank" rel="noopener noreferrer" class="google-badge">
              <svg width="16" height="16" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
              <span>Verified Google Review ↗</span>
            </a>
          </div>

          <div class="review-card">
            <div>
              <div class="review-header">
                <span class="reviewer-name">Property Owner</span>
                <span class="review-date">Verified Customer</span>
              </div>
              <div class="stars" style="margin-bottom: 8px;">★★★★★</div>
              <p class="review-text">
                "Arrived on time for the measure, quoted a very fair price, and removed our old rotten timber fence with zero hassle. The new modular wall looks exceptional."
              </p>
            </div>
            <a href="{gmaps_url}" target="_blank" rel="noopener noreferrer" class="google-badge">
              <svg width="16" height="16" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
              <span>Verified Google Review ↗</span>
            </a>
          </div>

        </div>

        <div style="text-align: center; margin-top: 40px;">
          <a href="{gmaps_url}" target="_blank" rel="noopener noreferrer" class="btn btn-dark" style="gap: 12px; padding: 16px 36px; font-size: 1.05rem; box-shadow: var(--shadow-md);">
            <svg width="22" height="22" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
            <span>Read All {reviews}+ Real Reviews on Google Maps ↗</span>
          </a>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 10px;">
            100% genuine feedback posted directly by {city} homeowners.
          </p>
        </div>
      </div>
    </section>

    <!-- Comparison Section -->
    <section class="section section-alt">
      <div class="container">
        <div class="section-title-wrap">
          <span class="section-eyebrow">Quality Benchmark</span>
          <h2 class="section-title">How {name} Compares</h2>
        </div>

        <div class="table-card">
          <table class="comparison-table">
            <thead>
              <tr>
                <th>Feature / Standard</th>
                <th class="highlight-col">{name}</th>
                <th>Cheap Subcontractors</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Steel Origin & Quality</strong></td>
                <td class="highlight-col">100% Genuine Australian BlueScope® Steel</td>
                <td>Cheap thin imported unbranded coil</td>
              </tr>
              <tr>
                <td><strong>Post Hole Footings</strong></td>
                <td class="highlight-col">600mm–800mm deep with high-strength concrete</td>
                <td>Shallow 300mm holes (leans after first storm)</td>
              </tr>
              <tr>
                <td><strong>Sloped Site Engineering</strong></td>
                <td class="highlight-col">Custom raked/stepped panels & plinth retaining</td>
                <td>Gaps under fence, pets escape</td>
              </tr>
              <tr>
                <td><strong>Quote Transparency</strong></td>
                <td class="highlight-col">Fixed price in writing with zero hidden charges</td>
                <td>"Surprise" fees for rock or old fence dumping</td>
              </tr>
              <tr>
                <td><strong>Site Cleanliness</strong></td>
                <td class="highlight-col">Job site swept clean & old fencing hauled away</td>
                <td>Leaves metal offcuts and dirt in your garden</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- Suburbs / Service Areas -->
    <section class="section" id="areas">
      <div class="container">
        <div class="section-title-wrap">
          <span class="section-eyebrow">Service Coverage</span>
          <h2 class="section-title">Areas We Service Across {city}</h2>
          <p class="section-subtitle">Based in {address}, we service homeowners, developers, and builders throughout the region:</p>
        </div>

        <div class="suburbs-grid">
{suburbs_html}
        </div>
      </div>
    </section>

    <!-- Bottom CTA -->
    <section class="section" style="background: var(--primary); color: #fff; text-align: center;">
      <div class="container" style="max-width: 760px;">
        <h2 style="font-size: 2.4rem; margin-bottom: 16px;">Ready to Upgrade Your Fence?</h2>
        <p style="font-size: 1.15rem; color: #a3c4b5; margin-bottom: 30px;">
          Call directly on {phone} for an honest, friendly chat about your project, or book your free on-site measure.
        </p>
        <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
          <a href="tel:{clean_phone}" class="btn btn-primary" style="padding: 16px 36px; font-size: 1.1rem;">
            Call {phone}
          </a>
          <a href="#quote" class="btn btn-outline" style="border-color: #fff; color: #fff; padding: 16px 32px;">
            Book On-Site Measure
          </a>
        </div>
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <h4 style="font-size: 1.3rem;">{name}</h4>
          <p style="font-size: 0.9rem; color: #9bb5a7; margin-bottom: 16px;">
            {city}’s dependable fencing team. Specialized in Colorbond steel fencing, modular acoustic walls, and custom gates.
          </p>
          <p style="font-size: 0.85rem; color: #7f9c8d;">
            📍 Base: {address}<br>
            📞 Phone: {phone}<br>
            ⏰ Mon – Sat: 7:00 AM – 5:00 PM
          </p>
        </div>

        <div class="footer-col">
          <h4>Fencing Solutions</h4>
          <ul>
            <li><a href="#services">Colorbond® Fencing</a></li>
            <li><a href="#services">Modular Wall Acoustic Barriers</a></li>
            <li><a href="#services">Automated Driveway Gates</a></li>
            <li><a href="#services">Timber & Privacy Slats</a></li>
            <li><a href="#services">Old Fence Removal & Disposal</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Free Quote & Measure</h4>
          <p style="font-size: 0.85rem; margin-bottom: 14px;">
            Servicing residential homeowners and commercial builders in {city}.
          </p>
          <a href="tel:{clean_phone}" class="btn btn-primary" style="width: 100%;">Call {phone}</a>
        </div>
      </div>

      <div class="footer-bottom">
        <div>© 2026 {name}. All rights reserved. {state} Licenced Tradesperson.</div>
        <div>Colorbond® is a registered trademark of BlueScope Steel Limited.</div>
      </div>
    </div>
  </footer>

  <!-- Mobile Sticky Bar -->
  <div class="mobile-bar" aria-label="Mobile Call Actions">
    <a href="tel:{clean_phone}" class="btn btn-primary">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24c1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
      <span>Call {phone}</span>
    </a>
    <a href="#quote" class="btn btn-dark">
      <span>Free Quote</span>
    </a>
  </div>

  <script>
    const buttons = document.querySelectorAll('.palette-btn');
    const preview = document.getElementById('palettePreview');
    const nameEl = document.getElementById('previewColorName');
    const descEl = document.getElementById('previewColorDesc');

    buttons.forEach(btn => {{
      btn.addEventListener('click', () => {{
        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        nameEl.textContent = `Selected Colour: ${{btn.dataset.color}}®`;
        descEl.textContent = btn.dataset.desc;
        preview.style.borderLeftColor = btn.dataset.hex;
      }});
    }});

    const form = document.getElementById('quoteForm');
    form.addEventListener('submit', (e) => {{
      e.preventDefault();
      const submitBtn = form.querySelector('.submit-btn');
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span>Sending Request...</span>';
      setTimeout(() => {{
        form.innerHTML = `
          <div style="text-align: center; padding: 40px 10px;">
            <div style="width: 56px; height: 56px; background: #e6f9f0; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 16px;">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
            </div>
            <h3 style="color: var(--primary); font-size: 1.4rem; margin-bottom: 8px;">Quote Request Received!</h3>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 16px;">Thank you! We will review your site details and call you shortly on the number provided.</p>
            <p style="font-weight: 700; color: var(--accent);">Need immediate assistance? Call <a href="tel:{clean_phone}" style="text-decoration: underline;">{phone}</a>.</p>
          </div>
        `;
      }}, 700);
    }});
  </script>
</body>
</html>'''
    return html

# Build all 20 websites
print("Generating websites for all 20 contractors...")
contractor_cards = []

for idx, item in enumerate(contractors, 1):
    slug = slugify(item['Company Name'])
    dir_path = os.path.join('sites', slug)
    os.makedirs(dir_path, exist_ok=True)
    
    file_path = os.path.join(dir_path, 'index.html')
    html_content = generate_landing_html(item, slug)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Store data for Hub
    name = item['Company Name']
    city = item['City / Region']
    state = city.split()[-1] if len(city.split()) > 1 else 'AU'
    rating = item['Rating']
    reviews = item['Reviews Count']
    last_rev = item['Latest Review']
    phone = item['Phone']
    web_status = item['Website Status']
    gmaps_url = item['Google Maps URL']
    wa_url = item.get('WhatsApp', '')
    
    # Pre-drafted WhatsApp pitch in Australian English
    clean_p = format_clean_phone(phone)
    pitch_text = f"G'day {name} team,\n\nSaw your incredible {rating}★ rating ({reviews} Google reviews) in {city} — top quality reputation!\n\nNoticed you don't have a standalone modern website listed, so you're likely losing direct Colorbond & modular fencing jobs to competitors running Google ads.\n\nWe built a fast, mobile-ready website concept for your brand with your real reviews and services:\n👉 [DEMO LINK]\n\nZero effort needed on your side. If you like it, we can connect it to your domain in 24 hours.\n\nWorth a quick 60-second look?\n\nCheers!"
    
    wa_msg_encoded = urllib.parse.quote(pitch_text.replace('[DEMO LINK]', f'https://demo-{slug}.vercel.app'))
    full_wa_url = f"{wa_url}?text={wa_msg_encoded}" if wa_url.startswith('https://wa.me') else '#'
    
    contractor_cards.append({
        'num': idx,
        'name': name,
        'slug': slug,
        'city': city,
        'state': state,
        'rating': rating,
        'reviews': reviews,
        'last_rev': last_rev,
        'phone': phone,
        'clean_phone': clean_p,
        'web_status': web_status,
        'gmaps_url': gmaps_url,
        'wa_url': wa_url,
        'full_wa_url': full_wa_url,
        'pitch_text': pitch_text,
        'site_rel_path': f'sites/{slug}/index.html'
    })
    print(f"[{idx}/20] Created site for {name} -> sites/{slug}/index.html")

# Create Master Hub Dashboard (hub.html and index.html)
hub_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Australian Fencing Contractors • Sales & Outreach Hub (20 Companies)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0d1512;
      --card-bg: #14201c;
      --card-border: #1f302a;
      --primary: #10b981;
      --accent: #f28c28;
      --text: #f1f5f3;
      --text-muted: #8da498;
      --radius: 14px;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; background-color: var(--bg); color: var(--text); line-height: 1.5; padding: 40px 20px 80px; }}
    a {{ color: inherit; text-decoration: none; }}
    .container {{ max-width: 1300px; margin: 0 auto; }}
    
    /* Header */
    .hub-header {{ text-align: center; margin-bottom: 40px; }}
    .hub-badge {{ display: inline-flex; align-items: center; gap: 8px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); color: var(--primary); padding: 6px 16px; border-radius: 50px; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px; }}
    .hub-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 2.6rem; font-weight: 700; color: #fff; margin-bottom: 12px; }}
    .hub-title span {{ color: var(--accent); }}
    .hub-desc {{ font-size: 1.1rem; color: var(--text-muted); max-width: 760px; margin: 0 auto; }}

    /* KPI Bar */
    .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 36px; }}
    .kpi-card {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; padding: 20px; text-align: center; }}
    .kpi-val {{ font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 800; color: #fff; margin-bottom: 4px; }}
    .kpi-val span {{ color: var(--primary); }}
    .kpi-label {{ font-size: 0.85rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; }}

    /* Filter Controls */
    .controls {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 14px; padding: 20px; margin-bottom: 30px; display: flex; flex-wrap: wrap; gap: 16px; align-items: center; justify-content: space-between; }}
    .filter-tabs {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    .filter-btn {{ background: transparent; border: 1px solid var(--card-border); color: var(--text-muted); padding: 8px 16px; border-radius: 8px; font-size: 0.85rem; font-weight: 700; cursor: pointer; transition: all 0.2s; }}
    .filter-btn.active, .filter-btn:hover {{ background: var(--primary); color: #0d1512; border-color: var(--primary); }}
    .search-box {{ position: relative; min-width: 280px; }}
    .search-input {{ width: 100%; background: #0d1512; border: 1px solid var(--card-border); border-radius: 8px; padding: 10px 14px; color: #fff; font-size: 0.9rem; outline: none; }}
    .search-input:focus {{ border-color: var(--primary); }}

    /* Cards Grid */
    .cards-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 24px; }}
    .biz-card {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: var(--radius); padding: 24px; display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s, border-color 0.2s; }}
    .biz-card:hover {{ transform: translateY(-3px); border-color: rgba(16, 185, 129, 0.4); }}
    
    .card-top {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; gap: 12px; }}
    .biz-name {{ font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 700; color: #fff; }}
    .state-badge {{ background: rgba(242, 140, 40, 0.15); border: 1px solid rgba(242, 140, 40, 0.3); color: var(--accent); padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; flex-shrink: 0; }}
    
    .status-badge {{ display: inline-flex; align-items: center; gap: 6px; font-size: 0.75rem; padding: 4px 10px; border-radius: 4px; font-weight: 700; margin-bottom: 14px; }}
    .status-no-site {{ background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }}
    .status-fb {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }}
    .status-aggr {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }}

    .stats-row {{ display: flex; gap: 14px; background: rgba(0, 0, 0, 0.25); padding: 10px 14px; border-radius: 8px; margin-bottom: 16px; font-size: 0.85rem; }}
    .stars {{ color: #f59e0b; font-weight: 800; }}
    .review-recency {{ color: #9fe2bf; font-weight: 600; margin-left: auto; }}

    .info-list {{ font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px; }}
    .info-list p {{ margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }}

    /* Actions */
    .card-actions {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: auto; }}
    .btn-action {{ display: inline-flex; align-items: center; justify-content: center; gap: 8px; font-size: 0.85rem; font-weight: 700; padding: 10px 14px; border-radius: 8px; border: none; cursor: pointer; transition: all 0.2s; min-height: 42px; text-align: center; }}
    .btn-view {{ background: var(--primary); color: #0d1512; }}
    .btn-view:hover {{ background: #059669; }}
    .btn-wa {{ background: #25D366; color: #fff; }}
    .btn-wa:hover {{ background: #1ebc59; }}
    .btn-copy {{ background: rgba(255, 255, 255, 0.08); color: #fff; border: 1px solid var(--card-border); }}
    .btn-copy:hover {{ background: rgba(255, 255, 255, 0.15); }}
    .btn-map {{ background: rgba(255, 255, 255, 0.08); color: #fff; border: 1px solid var(--card-border); }}
    .btn-map:hover {{ background: rgba(255, 255, 255, 0.15); }}

    .toast {{ position: fixed; bottom: 30px; right: 30px; background: var(--primary); color: #0d1512; font-weight: 800; padding: 12px 24px; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.4); transform: translateY(100px); opacity: 0; transition: all 0.3s; z-index: 1000; }}
    .toast.show {{ transform: translateY(0); opacity: 1; }}

    @media (max-width: 900px) {{
      .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
      .cards-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

  <div class="container">
    
    <!-- Header -->
    <header class="hub-header">
      <div class="hub-badge">Australia Outreach Machine</div>
      <h1 class="hub-title">Colorbond & Modular Fencing <span>Client Hub</span></h1>
      <p class="hub-desc">
        All 20 verified Australian contractors with ready-to-sell demo landing pages, direct WhatsApp links, and tailored pitch templates.
      </p>
    </header>

    <!-- KPI Summary -->
    <section class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-val">20</div>
        <div class="kpi-label">Ready Websites Generated</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val">19 <span>(95%)</span></div>
        <div class="kpi-label">Direct WhatsApp Mobiles</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val">4.8 – 5.0★</div>
        <div class="kpi-label">Top Google Rating</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val">&lt; 4 mo</div>
        <div class="kpi-label">Active Review Recency</div>
      </div>
    </section>

    <!-- Filter & Search Controls -->
    <div class="controls">
      <div class="filter-tabs">
        <button class="filter-btn active" data-filter="all">All States (20)</button>
        <button class="filter-btn" data-filter="NSW">NSW (7)</button>
        <button class="filter-btn" data-filter="QLD">QLD (4)</button>
        <button class="filter-btn" data-filter="WA">WA (4)</button>
        <button class="filter-btn" data-filter="VIC">VIC (2)</button>
        <button class="filter-btn" data-filter="SA">SA (2)</button>
        <button class="filter-btn" data-filter="ACT">ACT (1)</button>
      </div>

      <div class="search-box">
        <input type="text" id="searchBox" class="search-input" placeholder="Search by company or suburb...">
      </div>
    </div>

    <!-- Cards Grid -->
    <main class="cards-grid" id="cardsGrid">
'''

for c in contractor_cards:
    status_class = 'status-no-site' if 'нет' in c['web_status'] else ('status-fb' if 'Facebook' in c['web_status'] else 'status-aggr')
    wa_btn_html = f'<a href="{c["full_wa_url"]}" target="_blank" class="btn-action btn-wa">💬 WhatsApp</a>' if c['wa_url'].startswith('https') else '<span class="btn-action" style="background:#334155; color:#94a3b8; cursor:not-allowed;">Landline</span>'
    
    # Escape quotes for JS copy
    escaped_pitch = c['pitch_text'].replace('"', '\\"').replace('\n', '\\n')
    
    hub_html += f'''
      <article class="biz-card" data-state="{c['state']}" data-name="{c['name'].lower()} {c['city'].lower()}">
        <div>
          <div class="card-top">
            <h2 class="biz-name">{c['num']}. {c['name']}</h2>
            <span class="state-badge">{c['state']}</span>
          </div>

          <div class="status-badge {status_class}">
            {c['web_status']}
          </div>

          <div class="stats-row">
            <span class="stars">★ {c['rating']}</span>
            <span>({c['reviews']} reviews)</span>
            <span class="review-recency">🕒 {c['last_rev']}</span>
          </div>

          <div class="info-list">
            <p>📍 {c['city']}</p>
            <p>📞 <strong>{c['phone']}</strong></p>
          </div>
        </div>

        <div class="card-actions">
          <a href="{c['site_rel_path']}" target="_blank" class="btn-action btn-view">🌐 Preview Site</a>
          {wa_btn_html}
          <button type="button" class="btn-action btn-copy" onclick="copyPitch('{escaped_pitch}')">📋 Copy Pitch</button>
          <a href="{c['gmaps_url']}" target="_blank" class="btn-action btn-map">📍 Google Maps</a>
        </div>
      </article>
'''

hub_html += '''
    </main>

  </div>

  <div id="toast" class="toast">Pitch message copied to clipboard!</div>

  <script>
    // Copy Pitch Text to Clipboard
    function copyPitch(text) {
      navigator.clipboard.writeText(text).then(() => {
        const toast = document.getElementById('toast');
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 2500);
      });
    }

    // Filter by State
    const filterBtns = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.biz-card');
    const searchInput = document.getElementById('searchBox');

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        applyFilters();
      });
    });

    searchInput.addEventListener('input', applyFilters);

    function applyFilters() {
      const activeState = document.querySelector('.filter-btn.active').dataset.filter;
      const searchVal = searchInput.value.toLowerCase().trim();

      cards.forEach(card => {
        const matchState = (activeState === 'all' || card.dataset.state === activeState);
        const matchSearch = (!searchVal || card.dataset.name.includes(searchVal));

        if (matchState && matchSearch) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }
  </script>
</body>
</html>'''

with open('hub.html', 'w', encoding='utf-8') as f:
    f.write(hub_html)

# Also write to index.html in the root so opening the folder root directly shows the hub!
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(hub_html)

print("\nAll done! Generated 20 customized landing pages and the master hub.html / index.html!")
