import os
import json
import html

# Load Underwood review photos
with open('underwood_review_photos.json', 'r', encoding='utf-8') as f:
    review_photos = json.load(f)

from contractor_profiles import CONTRACTOR_PROFILES, COLORBOND_COLOURS, SUBURBS_MAP, clean_phone_number

with open('colorbond_modular_fencing_australia.json', 'r', encoding='utf-8') as f:
    raw_contractors = json.load(f)

item = [c for c in raw_contractors if c['Company Name'] == 'Underwood Fencing and Gates'][0]
profile = CONTRACTOR_PROFILES['Underwood Fencing and Gates']

with open('contractors_real_reviews.json', 'r', encoding='utf-8') as f:
    real_data = json.load(f)

c_real = [c for c in real_data if c['name'] == 'Underwood Fencing and Gates'][0]

def build_pilot_html(lang='en'):
    name = item['Company Name']
    rating = str(item['Rating'])
    reviews_count = str(item['Reviews Count'])
    phone = item['Phone']
    clean_phone = clean_phone_number(phone)
    address = item['Address']
    city = item['City / Region']
    gmaps_url = item['Google Maps URL']
    lead_name = profile['lead_name'] if lang == 'en' else profile['lead_name_ru']
    
    # AI generated service images
    img_service_1 = "../../images/service_colorbond_sloped.jpg"
    img_service_2 = "../../images/service_modular_wall.jpg"
    img_service_3 = "../../images/service_automated_gate.jpg"
    
    services_list = profile['services']
    s1 = services_list[0]
    s2 = services_list[1]
    s3 = services_list[2]
    
    s1_title = s1['title_en'] if lang == 'en' else s1['title_ru']
    s1_badge = s1['badge_en'] if lang == 'en' else s1['badge_ru']
    s1_desc = s1['desc_en'] if lang == 'en' else s1['desc_ru']
    s1_f = s1['features_en'] if lang == 'en' else s1['features_ru']
    
    s2_title = s2['title_en'] if lang == 'en' else s2['title_ru']
    s2_badge = s2['badge_en'] if lang == 'en' else s2['badge_ru']
    s2_desc = s2['desc_en'] if lang == 'en' else s2['desc_ru']
    s2_f = s2['features_en'] if lang == 'en' else s2['features_ru']
    
    s3_title = s3['title_en'] if lang == 'en' else s3['title_ru']
    s3_badge = s3['badge_en'] if lang == 'en' else s3['badge_ru']
    s3_desc = s3['desc_en'] if lang == 'en' else s3['desc_ru']
    s3_f = s3['features_en'] if lang == 'en' else s3['features_ru']

    suburbs = SUBURBS_MAP.get(city, ['Blacktown', 'Castle Hill', 'Parramatta', 'Penrith', 'Liverpool', 'Campbelltown', 'Hornsby', 'Northern Beaches', 'Sutherland Shire', 'Cronulla', 'Ryde', 'Baulkham Hills'])
    suburbs_html = '\n'.join([f'          <div class="suburb-tag">{s}</div>' for s in suburbs])

    if lang == 'en':
        lang_code = "en-AU"
        page_title = f"{name} | {rating}★ Colorbond & Modular Fencing Specialists {city}"
        meta_desc = f"{name}: {city}'s trusted Colorbond and modular fencing contractors. Rated {rating} Stars with {reviews_count} Google reviews. Speak directly with {lead_name} on {phone} for a free measure & quote."
        top_banner = "100% Genuine Australian BlueScope® Steel • 10-Year Workmanship Warranty"
        brand_sub = f"Colorbond & Modular Fencing • {city}"
        nav_services = "Services"
        nav_colours = "Colours"
        nav_reviews = "Reviews"
        nav_areas = "Areas"
        nav_btn = "Free Quote"
        
        hero_badge = f"★ {rating} / 5.0 ({reviews_count} verified Google reviews)"
        hero_h1 = f"Premium Colorbond® & Modular Fencing in {city}"
        hero_p = f"Professional fencing and custom gate installation by {name}. Directly managed on-site by {lead_name}. We specialise in sloped ground, retaining plinths, and storm-resistant boundary security across {city}."
        
        feat_1 = "Fixed price guarantee — zero hidden extras"
        feat_2 = f"Direct contact with {lead_name} & team"
        feat_3 = "100% Australian BlueScope® Steel"
        feat_4 = "Site cleanup & old fence removal included"
        
        hero_btn_quote = "Get a Free Measure & Quote"
        hero_btn_call = f"Call {lead_name}: {phone}"
        
        form_title = "Instant Measure & Quote"
        form_sub = f"Speak directly with {lead_name} — no pushy salesmen or call centres."
        form_type_label = "What type of fence do you need?"
        form_opt_1 = "Colorbond® Steel Fencing"
        form_opt_2 = "Modular Acoustic Sound Wall"
        form_opt_3 = "Custom Automated / Side Gate"
        form_opt_4 = "Sloped Ground Retaining & Fencing"
        form_len_label = "Estimated Length (Metres)"
        form_suburb_label = "Your Suburb"
        form_name_label = "Your Name"
        form_phone_label = "Mobile Phone Number"
        form_submit = "Request Free Measure & Quote →"
        form_privacy = "100% Privacy Protected. We will contact you within 2 business hours."
        
        services_kicker = "OUR CORE SERVICES"
        services_title = f"Engineered Fencing Solutions for {city} Properties"
        services_sub = "Zero shortcuts: 600mm+ concrete post foundations, heavy-gauge C-posts, and genuine BlueScope® steel panels."
        
        colours_kicker = "COLORBOND® STEEL PALETTE"
        colours_title = "Australia's Most Loved Architectural Colours"
        colours_sub = "Engineered with Activate® technology to resist the Australian sun, peeling, cracking, and harsh UV rays."
        
        reviews_kicker = "REAL CUSTOMER FEEDBACK & PHOTOS"
        reviews_title = f"Verified Google Reviews & Project Photos"
        reviews_sub = f"Read unedited feedback from real homeowners in {city}. Client-uploaded photos are shown directly with the project reviews below."
        reviews_btn_all = f"Read All {reviews_count}+ Reviews on Google Maps ↗"
        
        areas_kicker = "SERVICE COVERAGE"
        areas_title = f"Proudly Serving Homeowners Throughout {city}"
        areas_sub = "Prompt on-site measure and quote visits across all surrounding metropolitan suburbs."
        
        cta_title = f"Ready to Transform Your Boundary with {name}?"
        cta_sub = f"Book an on-site measure with {lead_name}. We will evaluate your boundary levels, check underground services, and provide a fixed-price itemised quote."
        cta_btn = "Book Free On-Site Measure"
        cta_direct = f"Or call {lead_name} directly on"
        
        footer_rights = f"© 2026 {name}. All rights reserved. Licensed fencing and structural contractor in {city}."
        calc_btn_text = "Get Price Estimate"
        photo_label = "Photos attached by client:"
        mobile_call = f"Call {lead_name}"
        mobile_quote = "Free Quote"
    else:
        lang_code = "ru"
        page_title = f"{name} | Заборы Colorbond® и модульные стены {city} — Смета онлайн"
        meta_desc = f"{name}: надежные заборы Colorbond и модульные стены в {city}. Рейтинг {rating}★ ({reviews_count} отзывов в Google). Связь напрямую с мастером ({lead_name}) по тел. {phone}."
        top_banner = "100% Оригинальная австралийская сталь BlueScope® • Гарантия на монтаж 10 лет"
        brand_sub = f"Заборы Colorbond, модульные стены и ворота • {city}"
        nav_services = "Услуги"
        nav_colours = "Палитра"
        nav_reviews = "Отзывы"
        nav_areas = "Районы"
        nav_btn = "Заказать расчет"
        
        hero_badge = f"★ {rating} / 5.0 ({reviews_count} проверенных отзывов в Google)"
        hero_h1 = f"Надежные заборы Colorbond®, модульные стены и ворота в {city}"
        hero_p = f"Профессиональная установка ограждений от {name}. Руководитель работ — {lead_name}. Работаем со сложным рельефом, монтируем подпорные плиты и автоматические ворота под ключ по всему {city}."
        
        feat_1 = "Фиксированная честная цена без доплат"
        feat_2 = f"Прямой контакт с мастером ({lead_name})"
        feat_3 = "Оригинальная австралийская сталь BlueScope®"
        feat_4 = "Полная уборка участка и вывоз старого забора"
        
        hero_btn_quote = "Бесплатный замер и смета"
        hero_btn_call = f"Позвонить мастеру: {phone}"
        
        form_title = "Быстрый замер и расчет сметы"
        form_sub = f"Прямая связь с мастером ({lead_name}) — без посредников и накруток."
        form_type_label = "Какой тип забора вы планируете?"
        form_opt_1 = "Забор из стали Colorbond®"
        form_opt_2 = "Модульная акустическая стена"
        form_opt_3 = "Ворота / калитка с замком"
        form_opt_4 = "Забор на склоне с подпорными плитами"
        form_len_label = "Примерная длина (в метрах)"
        form_suburb_label = "Ваш район (Suburb)"
        form_name_label = "Ваше имя"
        form_phone_label = "Мобильный телефон"
        form_submit = "Заказать бесплатный замер и смету →"
        form_privacy = "100% конфиденциальность. Свяжемся с вами в течение 2 рабочих часов."
        
        services_kicker = "НАШИ ОСНОВНЫЕ УСЛУГИ"
        services_title = f"Надежные решения для участков в {city}"
        services_sub = "Никаких компромиссов: глубокое бетонирование столбов от 600 мм, усиленный каркас и оригинальная сталь BlueScope®."
        
        colours_kicker = "ПАЛИТРА COLORBOND®"
        colours_title = "Самые популярные цвета австралийских заборов"
        colours_sub = "Заводское полимерное покрытие по технологии Activate®: защита от выгорания, ржавчины и ультрафиолета."
        
        reviews_kicker = "РЕАЛЬНЫЕ ОТЗЫВЫ И ФОТОГРАФИИ КЛИЕНТОВ"
        reviews_title = f"Отзывы клиентов и прикрепленные фото объектов"
        reviews_sub = f"Подлинные отзывы жителей {city} из Google Maps. Фотографии заборов показаны непосредственно внутри отзывов тех клиентов, которые их загрузили."
        reviews_btn_all = f"Смотреть все {reviews_count}+ отзывов в Google Maps ↗"
        
        areas_kicker = "ЗОНА ОБСЛУЖИВАНИЯ"
        areas_title = f"Работаем по всем районам {city}"
        areas_sub = "Оперативный выезд на бесплатный замер в любой пригород и окрестности."
        
        cta_title = f"Готовы обновить забор с гарантией 10 лет?"
        cta_sub = f"Запишитесь на замер с мастером ({lead_name}). Мы снимем точные уровни рельефа, учтем подземные коммуникации и предоставим прозрачную смету."
        cta_btn = "Записаться на бесплатный замер"
        cta_direct = f"Или позвоните мастеру напрямую:"
        
        footer_rights = f"© 2026 {name}. Все права защищены. Лицензированный подрядчик по ограждениям в {city}."
        calc_btn_text = "Рассчитать стоимость"
        photo_label = "Фотографии от клиента к отзыву:"
        mobile_call = "Позвонить"
        mobile_quote = "Заказать замер"

    # Build Reviews with attached photos
    ru_translations = profile.get('reviews_ru', [])
    reviews_html = []
    for idx, r in enumerate(c_real['reviews'][:4]):
        author = r['author']
        r_rating = r['rating']
        date_en = r['date']
        text_en = r['text']
        
        date_ru = date_en.replace('a month ago', '1 месяц назад') \
                         .replace('months ago', 'месяца назад') \
                         .replace('a week ago', '1 неделю назад') \
                         .replace('weeks ago', 'недели назад') \
                         .replace('a year ago', '1 год назад') \
                         .replace('years ago', 'года назад') \
                         .replace('Edited', 'изменено')
        
        text_ru = ru_translations[idx] if idx < len(ru_translations) else text_en
        date_disp = date_en if lang == 'en' else date_ru
        text_disp = text_en if lang == 'en' else text_ru
        
        attached = review_photos.get(author, [])
        photos_html = ""
        if attached:
            img_tags = "".join([f'<a href="{p}" target="_blank" class="review-photo-link"><img src="{p}" alt="Photo by {html.escape(author)}" class="review-photo-thumb" loading="lazy"></a>' for p in attached])
            photos_html = f'''
            <div class="review-attached-photos">
              <div class="review-photos-label">📸 {photo_label} ({len(attached)})</div>
              <div class="review-photos-grid">
                {img_tags}
              </div>
            </div>'''
        
        card = f'''          <div class="review-card">
            <div>
              <div class="review-header">
                <span class="reviewer-name">{html.escape(author)}</span>
                <span class="review-date">{html.escape(date_disp)}</span>
              </div>
              <div class="stars" style="margin-bottom: 8px;">★★★★★</div>
              <p class="review-text">"{html.escape(text_disp)}"</p>
              {photos_html}
            </div>
            <a href="{gmaps_url}" target="_blank" rel="noopener noreferrer" class="google-badge">
              <svg width="16" height="16" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
              <span>{'Проверенный отзыв в Google' if lang=='ru' else 'Verified Google Review'}</span>
            </a>
          </div>'''
        reviews_html.append(card)
    reviews_block = "\n".join(reviews_html)

    # Colours cards HTML
    colours_html = []
    for c in COLORBOND_COLOURS:
        colours_html.append(f'''          <div class="colour-card" data-colour="{c['name']}" data-hex="{c['hex']}">
            <div class="colour-swatch" style="background-color: {c['hex']};"></div>
            <div class="colour-name">{c['name']}</div>
            <div class="colour-desc">{c['desc']}</div>
          </div>''')
    colours_block = "\n".join(colours_html)

    return f'''<!DOCTYPE html>
<html lang="{lang_code}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <meta name="referrer" content="no-referrer">
  <title>{html.escape(page_title)}</title>
  <meta name="description" content="{html.escape(meta_desc)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #19382B;
      --primary-light: #285542;
      --accent: #F28C28;
      --accent-hover: #D97517;
      --monument: #383E42;
      --bg: #FAFAF7;
      --surface: #FFFFFF;
      --border: #E5E7EB;
      --text: #1F2937;
      --text-muted: #6B7280;
      --radius: 12px;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 4px 14px rgba(0,0,0,0.08);
      --shadow-lg: 0 10px 30px rgba(0,0,0,0.12);
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    
    html, body {{
      max-width: 100%;
      overflow-x: hidden;
      -webkit-text-size-adjust: 100%;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      -webkit-font-smoothing: antialiased;
    }}

    /* Global iOS input zoom fix */
    input, select, textarea {{
      font-size: 16px !important;
    }}

    .container {{
      max-width: 1220px;
      margin: 0 auto;
      padding: 0 20px;
    }}

    /* Top Banner */
    .top-banner {{
      background: var(--primary);
      color: #fff;
      font-size: 0.8rem;
      font-weight: 600;
      text-align: center;
      padding: 8px 16px;
      letter-spacing: 0.3px;
    }}

    /* Header */
    .header {{
      position: sticky;
      top: 0;
      background: rgba(255, 255, 255, 0.98);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      z-index: 1000;
      border-bottom: 1px solid var(--border);
      padding: 12px 0;
    }}
    .header .container {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }}
    .brand {{
      display: flex;
      flex-direction: column;
      flex-shrink: 1;
      min-width: 0;
      text-decoration: none;
    }}
    .brand-title {{
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--primary);
      letter-spacing: -0.3px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .brand-subtitle {{
      font-size: 0.68rem;
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      white-space: nowrap;
    }}
    .header-nav {{
      display: flex;
      align-items: center;
      gap: 22px;
      flex-shrink: 1;
    }}
    .nav-link {{
      font-weight: 600;
      font-size: 0.9rem;
      color: var(--text);
      white-space: nowrap;
      text-decoration: none;
      transition: color 0.2s;
    }}
    .nav-link:hover {{ color: var(--accent); }}
    
    .header-cta {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }}
    .phone-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-weight: 700;
      font-size: 0.88rem;
      color: var(--primary);
      white-space: nowrap !important;
      padding: 8px 14px;
      border-radius: 8px;
      background: rgba(25, 56, 43, 0.06);
      text-decoration: none;
      transition: background 0.2s;
    }}
    .phone-btn:hover {{ background: rgba(25, 56, 43, 0.12); color: var(--accent); }}
    
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-weight: 700;
      font-size: 0.9rem;
      padding: 9px 20px;
      border-radius: 8px;
      transition: all 0.2s;
      cursor: pointer;
      text-align: center;
      border: none;
      text-decoration: none;
      white-space: nowrap !important;
      flex-shrink: 0;
    }}
    .btn-primary {{
      background: var(--accent);
      color: #fff;
    }}
    .btn-primary:hover {{
      background: var(--accent-hover);
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(242, 140, 40, 0.3);
    }}
    .btn-dark {{
      background: var(--primary);
      color: #fff;
    }}
    .btn-dark:hover {{
      background: var(--primary-light);
    }}

    /* Hero Section */
    .hero {{
      padding: 56px 0 64px;
      background: linear-gradient(180deg, #FFFFFF 0%, var(--bg) 100%);
      border-bottom: 1px solid var(--border);
    }}
    .hero-grid {{
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 48px;
      align-items: center;
    }}
    .hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      background: #FFF4E5;
      color: #B45309;
      font-weight: 700;
      font-size: 0.85rem;
      border-radius: 20px;
      margin-bottom: 20px;
    }}
    .hero h1 {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 2.75rem;
      font-weight: 700;
      color: var(--primary);
      line-height: 1.15;
      margin-bottom: 20px;
      letter-spacing: -1px;
    }}
    .hero-desc {{
      font-size: 1.1rem;
      color: var(--text-muted);
      margin-bottom: 28px;
      line-height: 1.6;
    }}
    .hero-features {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 32px;
    }}
    .hero-feature-item {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.92rem;
      font-weight: 600;
      color: var(--text);
    }}
    .hero-feature-item svg {{
      color: var(--accent);
      flex-shrink: 0;
    }}
    .hero-actions {{
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
    }}

    /* Hero Form Card */
    .quote-card {{
      background: #fff;
      padding: 32px;
      border-radius: var(--radius);
      border: 1px solid var(--border);
      box-shadow: var(--shadow-lg);
    }}
    .quote-card h3 {{
      font-size: 1.3rem;
      font-weight: 800;
      color: var(--primary);
      margin-bottom: 6px;
    }}
    .quote-card p {{
      font-size: 0.88rem;
      color: var(--text-muted);
      margin-bottom: 22px;
    }}
    .form-group {{
      margin-bottom: 16px;
    }}
    .form-group label {{
      display: block;
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}
    .form-control {{
      width: 100%;
      padding: 12px 14px;
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: 16px !important;
      background: #FAFAF7;
      transition: border-color 0.2s, background 0.2s;
    }}
    .form-control:focus {{
      outline: none;
      border-color: var(--primary);
      background: #fff;
    }}
    .form-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }}

    /* Section Headers */
    .section {{
      padding: 72px 0;
    }}
    .section-header {{
      text-align: center;
      max-width: 760px;
      margin: 0 auto 52px;
    }}
    .section-kicker {{
      font-size: 0.82rem;
      font-weight: 800;
      color: var(--accent);
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-bottom: 12px;
    }}
    .section-title {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 2.2rem;
      font-weight: 700;
      color: var(--primary);
      line-height: 1.25;
      margin-bottom: 16px;
      letter-spacing: -0.5px;
    }}
    .section-sub {{
      font-size: 1.05rem;
      color: var(--text-muted);
      line-height: 1.6;
    }}

    /* Services Grid */
    .services-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 28px;
    }}
    .service-card {{
      background: #fff;
      border-radius: var(--radius);
      border: 1px solid var(--border);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-sm);
      transition: transform 0.2s, box-shadow 0.2s;
    }}
    .service-card:hover {{
      transform: translateY(-4px);
      box-shadow: var(--shadow-md);
    }}
    .service-img-wrap {{
      position: relative;
      height: 230px;
      overflow: hidden;
      background: #E2E8F0;
    }}
    .service-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.3s ease;
    }}
    .service-card:hover .service-img {{
      transform: scale(1.03);
    }}
    .service-badge {{
      position: absolute;
      top: 14px;
      right: 14px;
      background: rgba(25, 56, 43, 0.88);
      color: #fff;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 5px 12px;
      border-radius: 20px;
      backdrop-filter: blur(4px);
      z-index: 2;
    }}
    .service-body {{
      padding: 24px;
      flex: 1;
      display: flex;
      flex-direction: column;
    }}
    .service-body h3 {{
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 10px;
    }}
    .service-body p {{
      font-size: 0.92rem;
      color: var(--text-muted);
      line-height: 1.55;
      margin-bottom: 20px;
    }}
    .service-features {{
      list-style: none;
      margin-top: auto;
      margin-bottom: 20px;
    }}
    .service-features li {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.88rem;
      color: var(--text);
      margin-bottom: 8px;
      font-weight: 500;
    }}
    .service-features li svg {{
      color: var(--accent);
      flex-shrink: 0;
    }}

    /* Colours Grid */
    .colours-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
    }}
    .colour-card {{
      background: #fff;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s;
      cursor: pointer;
    }}
    .colour-card:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
      border-color: var(--accent);
    }}
    .colour-swatch {{
      height: 90px;
      border-radius: 8px;
      margin-bottom: 12px;
      border: 1px solid rgba(0,0,0,0.1);
    }}
    .colour-name {{
      font-weight: 700;
      font-size: 0.95rem;
      color: var(--primary);
      margin-bottom: 4px;
    }}
    .colour-desc {{
      font-size: 0.82rem;
      color: var(--text-muted);
      line-height: 1.4;
    }}

    /* Reviews Grid with Attached Customer Photos */
    .reviews-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 24px;
      margin-bottom: 36px;
    }}
    .review-card {{
      background: #fff;
      border-radius: var(--radius);
      border: 1px solid var(--border);
      padding: 28px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .review-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}
    .reviewer-name {{
      font-weight: 700;
      color: var(--primary);
      font-size: 1rem;
    }}
    .review-date {{
      font-size: 0.82rem;
      color: var(--text-muted);
    }}
    .stars {{
      color: #F59E0B;
      font-size: 1rem;
      letter-spacing: 2px;
    }}
    .review-text {{
      font-size: 0.95rem;
      color: var(--text);
      line-height: 1.6;
      margin-bottom: 16px;
      font-style: italic;
    }}
    
    /* Attached Customer Photos */
    .review-attached-photos {{
      margin-top: 14px;
      margin-bottom: 18px;
      padding-top: 14px;
      border-top: 1px dashed var(--border);
    }}
    .review-photos-label {{
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 8px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .review-photos-grid {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .review-photo-link {{
      display: block;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--border);
      transition: transform 0.2s, box-shadow 0.2s;
    }}
    .review-photo-link:hover {{
      transform: scale(1.05);
      box-shadow: var(--shadow-md);
      border-color: var(--accent);
    }}
    .review-photo-thumb {{
      width: 82px;
      height: 82px;
      object-fit: cover;
      display: block;
    }}

    .google-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-muted);
      text-decoration: none;
      padding: 6px 10px;
      background: #F3F4F6;
      border-radius: 6px;
      width: fit-content;
    }}
    .google-badge:hover {{ color: var(--primary); }}

    /* Suburbs Areas */
    .suburbs-grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: center;
      max-width: 900px;
      margin: 0 auto;
    }}
    .suburb-tag {{
      background: #fff;
      border: 1px solid var(--border);
      padding: 8px 16px;
      border-radius: 20px;
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text);
      box-shadow: var(--shadow-sm);
    }}

    /* CTA Section */
    .cta-banner {{
      background: var(--primary);
      color: #fff;
      padding: 72px 0;
      text-align: center;
    }}
    .cta-banner h2 {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 2.5rem;
      margin-bottom: 16px;
      letter-spacing: -0.5px;
    }}
    .cta-banner p {{
      font-size: 1.15rem;
      color: rgba(255,255,255,0.85);
      max-width: 680px;
      margin: 0 auto 32px;
    }}
    .cta-actions {{
      display: flex;
      gap: 16px;
      justify-content: center;
      align-items: center;
      flex-wrap: wrap;
    }}

    /* Footer */
    .site-footer {{
      background: #11251C;
      color: rgba(255,255,255,0.7);
      padding: 40px 0;
      font-size: 0.88rem;
      text-align: center;
    }}

    /* Mobile Sticky Bottom Call & Quote Bar */
    .mobile-bottom-bar {{
      display: none;
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: rgba(255, 255, 255, 0.98);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-top: 1px solid var(--border);
      padding: 10px 14px;
      z-index: 9999;
      box-shadow: 0 -4px 16px rgba(0,0,0,0.08);
    }}
    .mobile-bottom-bar-inner {{
      display: grid;
      grid-template-columns: 1fr 1.2fr;
      gap: 10px;
      max-width: 500px;
      margin: 0 auto;
    }}
    .btn-mobile-call {{
      background: var(--primary);
      color: #fff;
      font-weight: 700;
      font-size: 0.88rem;
      padding: 12px 10px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      text-decoration: none;
    }}
    .btn-mobile-quote {{
      background: var(--accent);
      color: #fff;
      font-weight: 700;
      font-size: 0.88rem;
      padding: 12px 10px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      text-decoration: none;
    }}

    /* ========================================================
       SMARTPHONE RESPONSIVE BREAKPOINTS (max-width: 768px)
       ======================================================== */
    @media (max-width: 768px) {{
      body {{
        padding-bottom: 68px; /* space for sticky bar */
      }}
      .mobile-bottom-bar {{
        display: block;
      }}
      .container {{
        padding: 0 14px;
      }}
      
      /* Top Banner */
      .top-banner {{
        font-size: 0.72rem;
        padding: 6px 10px;
        line-height: 1.35;
      }}
      
      /* Header */
      .header {{
        padding: 8px 0;
      }}
      .header .container {{
        gap: 8px;
        padding: 0 14px;
      }}
      .brand-title {{
        font-size: 0.92rem;
        letter-spacing: -0.2px;
      }}
      .brand-subtitle {{
        display: none;
      }}
      .header-nav {{
        display: none !important;
      }}
      .phone-btn {{
        display: none !important;
      }}
      .header-cta .btn {{
        padding: 7px 12px;
        font-size: 0.8rem;
        border-radius: 6px;
      }}
      
      /* Hero */
      .hero {{
        padding: 24px 0 32px;
      }}
      .hero-grid {{
        grid-template-columns: 1fr;
        gap: 28px;
      }}
      .hero-badge {{
        font-size: 0.75rem;
        padding: 4px 10px;
        margin-bottom: 12px;
      }}
      .hero h1 {{
        font-size: 1.75rem;
        line-height: 1.2;
        margin-bottom: 14px;
        letter-spacing: -0.5px;
      }}
      .hero-desc {{
        font-size: 0.92rem;
        line-height: 1.55;
        margin-bottom: 18px;
      }}
      .hero-features {{
        grid-template-columns: 1fr;
        gap: 8px;
        margin-bottom: 22px;
      }}
      .hero-feature-item {{
        font-size: 0.85rem;
      }}
      .hero-actions {{
        flex-direction: column;
        width: 100%;
        gap: 8px;
      }}
      .hero-actions .btn {{
        width: 100%;
        padding: 13px;
        font-size: 0.95rem;
      }}
      
      /* Quote Form */
      .quote-card {{
        padding: 20px 16px;
        border-radius: 12px;
      }}
      .quote-card h3 {{
        font-size: 1.15rem;
      }}
      .quote-card p {{
        font-size: 0.82rem;
        margin-bottom: 16px;
      }}
      .form-row {{
        grid-template-columns: 1fr;
        gap: 12px;
      }}
      .form-control {{
        font-size: 16px !important;
        padding: 11px 12px;
      }}
      
      /* Sections */
      .section {{
        padding: 42px 0;
      }}
      .section-header {{
        margin-bottom: 28px;
      }}
      .section-kicker {{
        font-size: 0.72rem;
        letter-spacing: 1px;
        margin-bottom: 8px;
      }}
      .section-title {{
        font-size: 1.55rem;
        line-height: 1.25;
        margin-bottom: 10px;
      }}
      .section-sub {{
        font-size: 0.88rem;
        line-height: 1.5;
      }}
      
      /* Services */
      .services-grid {{
        grid-template-columns: 1fr;
        gap: 20px;
      }}
      .service-card {{
        border-radius: 12px;
      }}
      .service-img-wrap {{
        height: 190px;
      }}
      .service-body {{
        padding: 18px 16px;
      }}
      .service-body h3 {{
        font-size: 1.15rem;
        margin-bottom: 8px;
      }}
      .service-body p {{
        font-size: 0.86rem;
        line-height: 1.5;
        margin-bottom: 16px;
      }}
      .service-features li {{
        font-size: 0.82rem;
        margin-bottom: 6px;
      }}
      .service-body .btn {{
        padding: 11px;
        font-size: 0.88rem;
      }}
      
      /* Colours */
      .colours-grid {{
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
      }}
      .colour-card {{
        padding: 10px;
        border-radius: 10px;
      }}
      .colour-swatch {{
        height: 60px;
        margin-bottom: 8px;
      }}
      .colour-name {{
        font-size: 0.82rem;
      }}
      .colour-desc {{
        font-size: 0.72rem;
        line-height: 1.35;
      }}
      
      /* Reviews */
      .reviews-grid {{
        grid-template-columns: 1fr;
        gap: 16px;
        margin-bottom: 24px;
      }}
      .review-card {{
        padding: 18px 16px;
        border-radius: 12px;
      }}
      .reviewer-name {{
        font-size: 0.95rem;
      }}
      .review-date {{
        font-size: 0.78rem;
      }}
      .review-text {{
        font-size: 0.88rem;
        line-height: 1.55;
        margin-bottom: 14px;
      }}
      .review-attached-photos {{
        margin-top: 12px;
        margin-bottom: 14px;
        padding-top: 12px;
      }}
      .review-photos-label {{
        font-size: 0.72rem;
        margin-bottom: 8px;
      }}
      .review-photos-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
      }}
      .review-photo-link {{
        aspect-ratio: 1 / 1;
        border-radius: 8px;
      }}
      .review-photo-thumb {{
        width: 100%;
        height: 100%;
        object-fit: cover;
      }}
      
      /* Suburbs */
      .suburbs-grid {{
        gap: 6px;
      }}
      .suburb-tag {{
        padding: 6px 12px;
        font-size: 0.78rem;
      }}
      
      /* CTA Banner */
      .cta-banner {{
        padding: 44px 0;
      }}
      .cta-banner h2 {{
        font-size: 1.6rem;
        line-height: 1.25;
      }}
      .cta-banner p {{
        font-size: 0.9rem;
        margin-bottom: 22px;
      }}
      .cta-actions {{
        flex-direction: column;
        width: 100%;
        gap: 10px;
      }}
      .cta-actions .btn {{
        width: 100%;
        padding: 13px;
        font-size: 0.95rem;
      }}
      
      /* Footer */
      .site-footer {{
        padding: 30px 0;
        font-size: 0.78rem;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Banner -->
  <div class="top-banner">
    {top_banner}
  </div>

  <!-- Header -->
  <header class="header">
    <div class="container">
      <a href="#" class="brand">
        <span class="brand-title">{name.upper()}</span>
        <span class="brand-subtitle">{brand_sub}</span>
      </a>

      <nav class="header-nav">
        <a href="#services" class="nav-link">{nav_services}</a>
        <a href="#colours" class="nav-link">{nav_colours}</a>
        <a href="#reviews" class="nav-link">{nav_reviews}</a>
        <a href="#areas" class="nav-link">{nav_areas}</a>
      </nav>

      <div class="header-cta">
        <a href="tel:{clean_phone}" class="phone-btn">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          <span>{phone}</span>
        </a>
        <a href="#quote" class="btn btn-primary">{nav_btn}</a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero" id="quote">
    <div class="container hero-grid">
      <div>
        <div class="hero-badge">
          {hero_badge}
        </div>
        <h1>{hero_h1}</h1>
        <p class="hero-desc">{hero_p}</p>

        <div class="hero-features">
          <div class="hero-feature-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
            <span>{feat_1}</span>
          </div>
          <div class="hero-feature-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
            <span>{feat_2}</span>
          </div>
          <div class="hero-feature-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
            <span>{feat_3}</span>
          </div>
          <div class="hero-feature-item">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
            <span>{feat_4}</span>
          </div>
        </div>

        <div class="hero-actions">
          <a href="#quote-form" class="btn btn-primary">{hero_btn_quote}</a>
          <a href="tel:{clean_phone}" class="btn btn-dark">{hero_btn_call}</a>
        </div>
      </div>

      <!-- Hero Quote Form -->
      <div class="quote-card" id="quote-form">
        <h3>{form_title}</h3>
        <p>{form_sub}</p>
        <form onsubmit="event.preventDefault(); alert('{'Спасибо за заявку! Мы свяжемся с вами в течение 2 часов.' if lang=='ru' else 'Thank you! We will contact you within 2 business hours.'}');">
          <div class="form-group">
            <label>{form_type_label}</label>
            <select class="form-control" required>
              <option value="colorbond">{form_opt_1}</option>
              <option value="modular">{form_opt_2}</option>
              <option value="gates">{form_opt_3}</option>
              <option value="retaining">{form_opt_4}</option>
            </select>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>{form_len_label}</label>
              <input type="number" class="form-control" placeholder="e.g. 45" required>
            </div>
            <div class="form-group">
              <label>{form_suburb_label}</label>
              <input type="text" class="form-control" placeholder="e.g. {suburbs[0]}" required>
            </div>
          </div>
          <div class="form-group">
            <label>{form_name_label}</label>
            <input type="text" class="form-control" placeholder="John Smith" required>
          </div>
          <div class="form-group">
            <label>{form_phone_label}</label>
            <input type="tel" class="form-control" placeholder="04xx xxx xxx" required>
          </div>
          <button type="submit" class="btn btn-primary" style="width: 100%; padding: 14px; font-size: 1rem;">{form_submit}</button>
          <div style="font-size: 0.75rem; color: var(--text-muted); text-align: center; margin-top: 10px;">
            🔒 {form_privacy}
          </div>
        </form>
      </div>
    </div>
  </section>

  <!-- Core Services Section (with Custom Generated AI Images) -->
  <section class="section" id="services">
    <div class="container">
      <div class="section-header">
        <div class="section-kicker">{services_kicker}</div>
        <h2 class="section-title">{services_title}</h2>
        <p class="section-sub">{services_sub}</p>
      </div>

      <div class="services-grid">
        <!-- Service 1 -->
        <article class="service-card">
          <div class="service-img-wrap">
            <img src="{img_service_1}" alt="{s1_title}" class="service-img" loading="lazy">
            <span class="service-badge">{s1_badge}</span>
          </div>
          <div class="service-body">
            <h3>{s1_title}</h3>
            <p>{s1_desc}</p>
            <ul class="service-features">
              {''.join([f'<li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>{f}</li>' for f in s1_f])}
            </ul>
            <a href="#quote-form" class="btn btn-primary" style="width: 100%;">{calc_btn_text}</a>
          </div>
        </article>

        <!-- Service 2 -->
        <article class="service-card">
          <div class="service-img-wrap">
            <img src="{img_service_2}" alt="{s2_title}" class="service-img" loading="lazy">
            <span class="service-badge">{s2_badge}</span>
          </div>
          <div class="service-body">
            <h3>{s2_title}</h3>
            <p>{s2_desc}</p>
            <ul class="service-features">
              {''.join([f'<li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>{f}</li>' for f in s2_f])}
            </ul>
            <a href="#quote-form" class="btn btn-primary" style="width: 100%;">{calc_btn_text}</a>
          </div>
        </article>

        <!-- Service 3 -->
        <article class="service-card">
          <div class="service-img-wrap">
            <img src="{img_service_3}" alt="{s3_title}" class="service-img" loading="lazy">
            <span class="service-badge">{s3_badge}</span>
          </div>
          <div class="service-body">
            <h3>{s3_title}</h3>
            <p>{s3_desc}</p>
            <ul class="service-features">
              {''.join([f'<li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>{f}</li>' for f in s3_f])}
            </ul>
            <a href="#quote-form" class="btn btn-primary" style="width: 100%;">{calc_btn_text}</a>
          </div>
        </article>
      </div>
    </div>
  </section>

  <!-- Colours Section -->
  <section class="section" id="colours">
    <div class="container">
      <div class="section-header">
        <div class="section-kicker">{colours_kicker}</div>
        <h2 class="section-title">{colours_title}</h2>
        <p class="section-sub">{colours_sub}</p>
      </div>

      <div class="colours-grid">
        {colours_block}
      </div>
    </div>
  </section>

  <!-- Verified Real Customer Reviews with Customer Attached Photos -->
  <section class="section" id="reviews" style="background: #FFFFFF; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);">
    <div class="container">
      <div class="section-header">
        <div class="section-kicker">{reviews_kicker}</div>
        <h2 class="section-title">{reviews_title}</h2>
        <p class="section-sub">{reviews_sub}</p>
      </div>

      <div class="reviews-grid">
        {reviews_block}
      </div>

      <div style="text-align: center;">
        <a href="{gmaps_url}" target="_blank" rel="noopener noreferrer" class="btn btn-dark" style="padding: 13px 28px;">
          {reviews_btn_all}
        </a>
      </div>
    </div>
  </section>

  <!-- Service Areas -->
  <section class="section" id="areas">
    <div class="container">
      <div class="section-header">
        <div class="section-kicker">{areas_kicker}</div>
        <h2 class="section-title">{areas_title}</h2>
        <p class="section-sub">{areas_sub}</p>
      </div>

      <div class="suburbs-grid">
        {suburbs_html}
      </div>
    </div>
  </section>

  <!-- Call to Action Banner -->
  <section class="cta-banner">
    <div class="container">
      <h2>{cta_title}</h2>
      <p>{cta_sub}</p>
      <div class="cta-actions">
        <a href="#quote-form" class="btn btn-primary" style="padding: 14px 32px; font-size: 1.05rem;">{cta_btn}</a>
        <a href="tel:{clean_phone}" class="btn btn-dark" style="padding: 14px 28px; font-size: 1.05rem; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3);">
          {cta_direct} {phone}
        </a>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <p>{footer_rights}</p>
    </div>
  </footer>

  <!-- Mobile Sticky Bottom Bar -->
  <div class="mobile-bottom-bar">
    <div class="mobile-bottom-bar-inner">
      <a href="tel:{clean_phone}" class="btn-mobile-call">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        <span>{mobile_call}</span>
      </a>
      <a href="#quote" class="btn-mobile-quote">
        <span>{mobile_quote} →</span>
      </a>
    </div>
  </div>

</body>
</html>'''

# Write Underwood pilot files
site_dir = os.path.join('sites', 'underwood-fencing-and-gates')
with open(os.path.join(site_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(build_pilot_html(lang='en'))

with open(os.path.join(site_dir, 'ru.html'), 'w', encoding='utf-8') as f:
    f.write(build_pilot_html(lang='ru'))

print("Pilot Underwood Fencing and Gates site rebuilt with mobile-first responsive architecture!")
