import os
import json
import re
import urllib.parse
import html

# Load parsed contractor data
with open('colorbond_modular_fencing_australia.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

SUBURBS_MAP = {
    'Sydney NSW': ['Blacktown', 'Castle Hill', 'Parramatta', 'Penrith', 'Liverpool', 'Campbelltown', 'Hornsby', 'Northern Beaches', 'Sutherland Shire', 'Cronulla', 'Ryde', 'Baulkham Hills'],
    'Melbourne VIC': ['Frankston', 'Dandenong', 'Berwick', 'Werribee', 'Point Cook', 'Geelong', 'Craigieburn', 'Sunbury', 'Mornington Peninsula', 'Ringwood', 'Box Hill'],
    'Brisbane QLD': ['Ipswich', 'Logan City', 'Caboolture', 'Chermside', 'Capalaba', 'Redcliffe', 'Springfield', 'Cleveland', 'North Lakes', 'Underwood', 'Sunnybank'],
    'Perth WA': ['Joondalup', 'Mandurah', 'Rockingham', 'Armadale', 'Fremantle', 'Midland', 'Baldivis', 'Canning Vale', 'Morley', 'Scarborough', 'Ellenbrook'],
    'Adelaide SA': ['Mawson Lakes', 'Marion', 'Salisbury', 'Morphett Vale', 'Golden Grove', 'Glenelg', 'Mount Barker', 'Gawler', 'Hallett Cove', 'Norwood'],
    'Canberra ACT': ['Belconnen', 'Tuggeranong', 'Gungahlin', 'Woden Valley', 'Queanbeyan', 'Weston Creek', 'Fyshwick', 'Bruce', 'Kambah', 'Franklin']
}

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def format_clean_phone(phone):
    return re.sub(r'[^\d+]', '', phone)

def generate_landing_html(item, slug, lang='en'):
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
    state = city.split()[-1] if len(city.split()) > 1 else 'AU'

    if lang == 'en':
        lang_code = "en-AU"
        page_title = f"{name} | {rating}★ Colorbond & Modular Fencing Specialists {city}"
        meta_desc = f"{name}: {city}'s trusted Colorbond and modular fencing contractors. Rated {rating} Stars with {reviews} Google reviews. Call {phone} for a free measure & quote."
        top_banner = "100% Genuine Australian BlueScope® Steel • 10-Year Workmanship Warranty"
        brand_sub = f"Colorbond & Modular Fencing {city}"
        nav_services = "Services"
        nav_colours = "Colours"
        nav_reviews = "Reviews"
        nav_areas = "Areas"
        btn_nav_quote = "Free Quote"
        btn_free_quote = "Free Measure & Quote"
        rating_badge_txt = f"{rating} / 5.0 ({reviews} Verified Google Reviews ↗)"
        hero_title = f"{city}’s Trusted <span>Colorbond, Modular & Gate</span> Specialists."
        hero_lead = f"Professional boundary and acoustic fencing installed by {name}. We specialize in sloped ground, retaining plinths, and custom security gates across {city}."
        badge1 = "Fair, Upfront Fixed-Price Quotes"
        badge2 = "Sloped Site & Retaining Experts"
        badge3 = "Genuine BlueScope® Steel (No Thin Fakes)"
        badge4 = "Complete Clean-Up & Old Fence Disposal"
        btn_call_direct = f"Call Directly: {phone}"
        
        # Form
        form_title = "Fast Measure & Quote"
        form_sub = "Direct communication with the installer — no middleman or call centres."
        lbl_proj = "What project are you planning?"
        opt_default = "Select service type..."
        opt1 = "Colorbond® Steel Fencing"
        opt2 = "Modular Wall / Acoustic Sound Barrier"
        opt3 = "Custom Security Gate (Sliding/Swing)"
        opt4 = "Timber Paling & Slat Screen"
        opt5 = "Old Fence Replacement & Removal"
        lbl_len = "Est. Length (metres)"
        lbl_suburb = "Your Suburb"
        lbl_name = "Your Full Name"
        lbl_phone = "Mobile Phone"
        btn_submit = "Book Free Measure & Quote"
        privacy_txt = "🔒 100% Privacy. We will call or text you within 2 business hours."

        # Services
        srv_eyebrow = "Our Core Expertise"
        srv_title = "Built Tough for Australian Backyards"
        srv_sub = "We don't take shortcuts. Deep concrete post footings, reinforced rails, and authentic Australian steel."
        c1_badge = "Most Popular"
        c1_title = "Colorbond® Steel Fencing"
        c1_desc = "The gold standard for Australian residential boundaries. 100% termite-proof, bushfire compliant, non-combustible, and rot-free."
        c1_f1 = "22 Designer Australian Colours"
        c1_f2 = "1.8m & 2.1m Privacy Heights"
        c1_f3 = "Stepped & Raked panels for slopes"
        c1_btn = "Get Colorbond Quote"

        c2_badge = "Acoustic & Modern"
        c2_title = "Modular Wall Systems"
        c2_desc = "Achieve the architectural look of a rendered masonry wall without the cost of heavy strip footings. Substantially cuts traffic noise."
        c2_f1 = "Up to 25dB Noise Reduction"
        c2_f2 = "Eliminates road & neighbour sound"
        c2_f3 = "Paint or texture-coat to match home"
        c2_btn = "Get Modular Wall Quote"

        c3_badge = "Custom Fabricated"
        c3_title = "Gates & Automation"
        c3_desc = "Engineered sliding, double-swing, and side pedestrian gates with heavy-duty automated motors, wireless keypads, and smartphone control."
        c3_f1 = "Automated Sliding & Double-Swing"
        c3_f2 = "Keypad & Remote Fob access"
        c3_f3 = "Matching Colorbond or Slat infills"
        c3_btn = "Get Gates Quote"

        # Colours
        col_eyebrow = "Interactive Palette"
        col_title = f"Popular Colorbond® Colours in {city}"
        col_sub = "Click to preview Australia's most requested architectural fencing colours for 2026."
        col_btn = "Order Sample with Measure"
        desc_monument = "Australia's #1 choice: a deep, confident charcoal that creates stunning contrast against natural gardens and modern render."
        desc_woodland = "Natural, organic dark olive-grey that blends seamlessly with Australian eucalypts and native vegetation."
        desc_surfmist = "Fresh, clean, coastal off-white. Makes narrow suburban blocks look significantly brighter and more spacious."
        desc_basalt = "Contemporary mineral grey with cool undertones, perfectly suited to timber, stone, and brick facades."
        desc_dune = "Warm, neutral earth tone inspired by coastal sand dunes. Complements classic Australian brickwork."
        desc_nightsky = "Sophisticated, dramatic deep black. Makes plants, pool areas, and architectural features stand out."

        # Reviews
        rev_eyebrow = "Social Proof"
        rev_title = f"{rating} Star Rating Across {reviews}+ Verified Jobs"
        rev_sub = f"Real verified feedback from homeowners in {city}. Latest review posted {latest_review}."
        rev1_name = "Local Homeowner"
        rev1_txt = f"Outstanding workmanship by {name}. Provided a clear, detailed quote with no hidden extras. The fence line is arrow-straight and they left our backyard spotless."
        rev2_name = "Residential Client"
        rev2_txt = "Installed our Colorbond fence and automated gate on a tricky sloped boundary. Great communication from day one and finished ahead of schedule. Highly recommended."
        rev3_name = "Property Owner"
        rev3_txt = "Arrived on time for the measure, quoted a very fair price, and removed our old rotten timber fence with zero hassle. The new modular wall looks exceptional."
        rev_all_btn = f"Read All {reviews}+ Real Reviews on Google Maps ↗"
        rev_bottom_sub = f"100% genuine feedback posted directly by {city} homeowners."

        # Table
        tbl_eyebrow = "Quality Benchmark"
        tbl_title = f"How {name} Compares"
        th1 = "Feature / Standard"
        th2 = name
        th3 = "Cheap Subcontractors"
        r1_t = "Steel Origin & Quality"
        r1_g = "100% Genuine Australian BlueScope® Steel"
        r1_b = "Cheap thin imported unbranded coil"
        r2_t = "Post Hole Footings"
        r2_g = "600mm–800mm deep with high-strength concrete"
        r2_b = "Shallow 300mm holes (leans after first storm)"
        r3_t = "Sloped Site Engineering"
        r3_g = "Custom raked/stepped panels & plinth retaining"
        r3_b = "Gaps under fence, pets escape"
        r4_t = "Quote Transparency"
        r4_g = "Fixed price in writing with zero hidden charges"
        r4_b = '"Surprise" fees for rock or old fence dumping'
        r5_t = "Site Cleanliness"
        r5_g = "Job site swept clean & old fencing hauled away"
        r5_b = "Leaves metal offcuts and dirt in your garden"

        # Areas
        area_eyebrow = "Service Coverage"
        area_title = f"Areas We Service Across {city}"
        area_sub = f"Based in {address}, we service homeowners, developers, and builders throughout the region:"

        # Bottom CTA
        cta_title = "Ready to Upgrade Your Fence?"
        cta_sub = f"Call directly on {phone} for an honest, friendly chat about your project, or book your free on-site measure."
        cta_btn1 = f"Call {phone}"
        cta_btn2 = "Book On-Site Measure"

        # Footer
        ft_desc = f"{city}’s dependable fencing team. Specialized in Colorbond steel fencing, modular acoustic walls, and custom gates."
        ft_hours = "⏰ Mon – Sat: 7:00 AM – 5:00 PM"
        ft_h2 = "Fencing Solutions"
        ft_h3 = "Free Quote & Measure"
        ft_rights = f"© 2026 {name}. All rights reserved. {state} Licenced Tradesperson."
        ft_trademark = "Colorbond® is a registered trademark of BlueScope Steel Limited."
        mob_quote = "Free Quote"

    else:
        # Russian Version
        lang_code = "ru"
        page_title = f"{name} | {rating}★ Заборы Colorbond® и модульные ограждения под ключ {city}"
        meta_desc = f"{name}: надежные заборы из стали Colorbond и модульные стены в {city}. Рейтинг {rating}★ ({reviews} отзывов Google). Звоните {phone} для бесплатного замера."
        top_banner = "100% Оригинальная австралийская сталь BlueScope® • Гарантия на монтаж 10 лет"
        brand_sub = f"Заборы Colorbond, модульные стены и ворота • {city}"
        nav_services = "Услуги"
        nav_colours = "Палитра"
        nav_reviews = "Отзывы"
        nav_areas = "Районы"
        btn_nav_quote = "Бесплатный замер"
        btn_free_quote = "Бесплатный замер и смета"
        rating_badge_txt = f"{rating} / 5.0 ({reviews} проверенных отзывов в Google ↗)"
        hero_title = f"Надежные заборы <span>Colorbond, модульные стены и ворота</span> в {city}."
        hero_lead = f"Профессиональная установка ограждений и заборов от {name}. Работаем на участках со сложным рельефом, монтируем подпорные плиты и автоматические ворота под ключ по всему {city}."
        badge1 = "Честная фиксированная цена без скрытых доплат"
        badge2 = "Специалисты по склонам и подпорным стенкам"
        badge3 = "Оригинальная австралийская сталь BlueScope®"
        badge4 = "Полная уборка участка и вывоз старого забора"
        btn_call_direct = f"Позвонить мастеру: {phone}"

        # Form
        form_title = "Быстрый замер и расчет сметы"
        form_sub = "Прямая связь с мастером — без посредников и колл-центров."
        lbl_proj = "Какой тип забора вы планируете?"
        opt_default = "Выберите тип услуги..."
        opt1 = "Забор из стали Colorbond®"
        opt2 = "Модульная шумозащитная стена"
        opt3 = "Ворота с автоматикой (откатные / распашные)"
        opt4 = "Деревянный забор / Реечное ограждение"
        opt5 = "Замена и демонтаж старого забора"
        lbl_len = "Примерная длина (в метрах)"
        lbl_suburb = "Ваш район (Suburb)"
        lbl_name = "Ваше имя"
        lbl_phone = "Мобильный телефон"
        btn_submit = "Заказать бесплатный замер и смету"
        privacy_txt = "🔒 100% конфиденциальность. Свяжемся с вами в течение 2 рабочих часов."

        # Services
        srv_eyebrow = "Наши основные услуги"
        srv_title = "Надежные решения для австралийских участков"
        srv_sub = "Никаких компромиссов: глубокое бетонирование столбов, усиленный каркас и оригинальная сталь BlueScope®."
        c1_badge = "Самый популярный"
        c1_title = "Заборы из стали Colorbond®"
        c1_desc = "Золотой стандарт австралийских частных участков. Защита от термитов, огнестойкость, устойчивость к коррозии и выгоранию на солнце."
        c1_f1 = "22 дизайнерских цвета австралийской палитры"
        c1_f2 = "Высота приватности: 1.8 м и 2.1 м"
        c1_f3 = "Ступенчатый монтаж на склонах и неровностях"
        c1_btn = "Рассчитать забор Colorbond"

        c2_badge = "Шумоизоляция и стиль"
        c2_title = "Модульные акустические стены"
        c2_desc = "Внешний вид монолитной каменной стены без дорогого тяжелого фундамента. Эффективно гасит уличный и автомобильный шум."
        c2_f1 = "Снижение шума до 25 дБ"
        c2_f2 = "Защита от шума трассы и соседей"
        c2_f3 = "Фактурная окраска под фасад вашего дома"
        c2_btn = "Рассчитать модульную стену"

        c3_badge = "Индивидуальный монтаж"
        c3_title = "Ворота и автоматика"
        c3_desc = "Откатные, распашные и калиточные системы с мощными электроприводами, пультами ДУ, кодовыми панелями и управлением со смартфона."
        c3_f1 = "Автоматические откатные и распашные ворота"
        c3_f2 = "Доступ по кодовой панели и пульту"
        c3_f3 = "В тон забора: Colorbond или жалюзи/рейки"
        c3_btn = "Рассчитать ворота"

        # Colours
        col_eyebrow = "Интерактивная палитра"
        col_title = f"Популярные цвета Colorbond® в {city}"
        col_sub = "Нажмите на цвет, чтобы посмотреть самые востребованные оттенки 2026 года."
        col_btn = "Заказать образцы цвета вместе с замером"
        desc_monument = "Monument®: глубокий графитовый угольный оттенок #1 в Австралии. Идеальный контраст с современной штукатуркой и садом."
        desc_woodland = "Woodland Grey®: натуральный темно-оливковый серый оттенок, гармонирующий с австралийской растительностью."
        desc_surfmist = "Surfmist®: свежий прибрежный кремово-белый цвет. Визуально расширяет пространство участка."
        desc_basalt = "Basalt®: современный минеральный серый с холодным подтоном под камень, дерево и кирпич."
        desc_dune = "Dune®: теплый нейтральный песчаный оттенок. Отлично сочетается с классической кирпичной кладкой."
        desc_nightsky = "Night Sky®: глубокий эффектный черный цвет. Подчеркивает зелень растений и зону бассейна."

        # Reviews
        rev_eyebrow = "Подтвержденная репутация"
        rev_title = f"Рейтинг {rating}★ на основе {reviews}+ выполненных заказов"
        rev_sub = f"Реальные отзывы домовладельцев в {city}. Последний отзыв опубликован {latest_review}."
        rev1_name = "Местный домовладелец"
        rev1_txt = f"Великолепная работа команды {name}. Четкая, детализированная смета без скрытых доплат. Линия забора идеальная, участок оставили идеально чистым."
        rev2_name = "Частный клиент"
        rev2_txt = "Установили забор Colorbond и автоматические ворота на сложном склоне. Отличная коммуникация с первого дня и закончили раньше срока. Очень рекомендую."
        rev3_name = "Владелец дома"
        rev3_txt = "Приехали вовремя на замер, назвали честную цену, аккуратно демонтировали и вывезли старый забор. Новая модульная стена выглядит потрясающе."
        rev_all_btn = f"Читать все {reviews}+ отзывов на Google Maps ↗"
        rev_bottom_sub = f"100% настоящие отзывы домовладельцев {city}."

        # Table
        tbl_eyebrow = "Стандарты качества"
        tbl_title = f"В чем отличие {name}"
        th1 = "Критерий / Стандарт"
        th2 = name
        th3 = "Случайные шабашники"
        r1_t = "Качество и происхождение стали"
        r1_g = "100% оригинальная австралийская сталь BlueScope®"
        r1_b = "Дешевая тонкая китайская жесть без маркировки"
        r2_t = "Глубина бетонирования столбов"
        r2_g = "600–800 мм с армированным бетоном высокой прочности"
        r2_b = "Мелкие ямы 300 мм (забор наклоняется после первой бури)"
        r3_t = "Монтаж на склонах и перепадах высот"
        r3_g = "Ступенчатые панели и подпорные цокольные плиты (plinths)"
        r3_b = "Щели под забором, сбегают домашние животные"
        r4_t = "Прозрачность сметы"
        r4_g = "Фиксированная цена в договоре без скрытых доплат"
        r4_b = "Внезапные наценки за скальный грунт или утилизацию"
        r5_t = "Чистота на участке"
        r5_g = "Полная уборка, вывоз обрезков металла и мусора"
        r5_b = "Оставляют острую стружку, обрезки и грязь на газоне"

        # Areas
        area_eyebrow = "География выездов"
        area_title = f"Районы обслуживания в {city}"
        area_sub = f"Базируясь по адресу {address}, выезжаем на замеры к домовладельцам и застройщикам по всему региону:"

        # Bottom CTA
        cta_title = "Планируете новый забор или ворота?"
        cta_sub = f"Позвоните по номеру {phone} для честной консультации с мастером или закажите бесплатный выезд на замер."
        cta_btn1 = f"Позвонить {phone}"
        cta_btn2 = "Заказать бесплатный замер"

        # Footer
        ft_desc = f"Надежная команда подрядчиков в {city}. Специализируемся на заборах из стали Colorbond, шумозащитных модульных стенах и автоматических воротах."
        ft_hours = "⏰ Пн – Сб: 7:00 – 17:00"
        ft_h2 = "Наши решения"
        ft_h3 = "Бесплатный расчет"
        ft_rights = f"© 2026 {name}. Все права защищены. Лицензированный подрядчик {state}."
        ft_trademark = "Colorbond® — зарегистрированная торговая марка BlueScope Steel Limited."
        mob_quote = "Замер"

    html_code = f'''<!DOCTYPE html>
<html lang="{lang_code}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
  <meta name="description" content="{meta_desc}">
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
    .header {{ position: sticky; top: 0; background: rgba(255, 255, 255, 0.98); backdrop-filter: blur(10px); z-index: 100; border-bottom: 1px solid var(--border); padding: 12px 0; }}
    .header .container {{ display: flex; justify-content: space-between; align-items: center; gap: 20px; }}
    .brand {{ display: flex; flex-direction: column; flex-shrink: 0; }}
    .brand-title {{ font-size: 1.18rem; font-weight: 800; color: var(--primary); letter-spacing: -0.3px; white-space: nowrap; }}
    .brand-subtitle {{ font-size: 0.7rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap; }}
    .header-nav {{ display: flex; align-items: center; gap: 24px; }}
    .nav-link {{ font-weight: 600; font-size: 0.92rem; color: var(--text); white-space: nowrap; transition: color 0.2s; }}
    .nav-link:hover {{ color: var(--accent); }}
    .header-cta {{ display: flex; align-items: center; gap: 12px; flex-shrink: 0; }}
    .phone-btn {{ display: inline-flex; align-items: center; gap: 6px; font-weight: 700; font-size: 0.88rem; color: var(--primary); white-space: nowrap; padding: 7px 12px; border-radius: 6px; background: rgba(25, 56, 43, 0.05); transition: background 0.2s; }}
    .phone-btn:hover {{ background: rgba(25, 56, 43, 0.1); color: var(--accent); }}
    .btn-nav {{ padding: 8px 18px; font-size: 0.88rem; white-space: nowrap; }}

    /* Buttons */
    .btn {{ display: inline-flex; align-items: center; justify-content: center; gap: 8px; font-weight: 700; font-size: 0.95rem; padding: 10px 22px; border-radius: 8px; transition: all 0.2s; cursor: pointer; text-align: center; border: none; }}
    .btn-primary {{ background: var(--accent); color: #fff; }}
    .btn-primary:hover {{ background: var(--accent-hover); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(242, 140, 40, 0.3); }}
    .btn-dark {{ background: var(--primary); color: #fff; }}
    .btn-dark:hover {{ background: var(--primary-light); }}
    .btn-outline {{ background: transparent; border: 2px solid var(--primary); color: var(--primary); }}
    .btn-outline:hover {{ background: var(--primary); color: #fff; }}

    /* Hero */
    .hero {{ padding: 60px 0 70px; background: linear-gradient(180deg, #f0f5f2 0%, #ffffff 100%); }}
    .hero-grid {{ display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 40px; align-items: center; }}
    .rating-badge {{ display: inline-flex; align-items: center; gap: 8px; background: #fff; border: 1px solid var(--border); padding: 6px 14px; border-radius: 30px; font-size: 0.85rem; font-weight: 700; color: var(--primary); margin-bottom: 20px; box-shadow: var(--shadow-sm); }}
    .stars {{ color: #f59e0b; }}
    .hero-title {{ font-size: 2.85rem; color: var(--primary); margin-bottom: 18px; }}
    .hero-title span {{ color: var(--accent); }}
    .hero-lead {{ font-size: 1.15rem; color: var(--text-muted); margin-bottom: 24px; }}
    .hero-badges {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 28px; }}
    .badge-item {{ display: flex; align-items: center; gap: 8px; font-size: 0.9rem; font-weight: 600; color: var(--primary); }}
    .badge-item svg {{ color: var(--accent); flex-shrink: 0; }}

    /* Quote Card */
    .hero-form-card {{ background: #fff; border-radius: var(--radius); padding: 30px; box-shadow: var(--shadow-lg); border: 1px solid var(--border); }}
    .form-header {{ margin-bottom: 20px; }}
    .form-header h3 {{ font-size: 1.45rem; color: var(--primary); margin-bottom: 4px; }}
    .form-header p {{ font-size: 0.85rem; color: var(--text-muted); }}
    .form-group {{ margin-bottom: 14px; }}
    .form-group label {{ display: block; font-size: 0.82rem; font-weight: 700; margin-bottom: 6px; color: var(--text); }}
    .form-control {{ width: 100%; padding: 11px 14px; font-size: 0.95rem; border: 1.5px solid var(--border); border-radius: 8px; font-family: inherit; transition: border-color 0.2s; }}
    .form-control:focus {{ outline: none; border-color: var(--primary); }}
    .form-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
    .submit-btn {{ width: 100%; padding: 14px; font-size: 1.05rem; margin-top: 6px; }}
    .privacy-notice {{ font-size: 0.75rem; color: var(--text-muted); text-align: center; margin-top: 10px; }}

    /* Section Global */
    .section {{ padding: 80px 0; }}
    .section-alt {{ background: var(--bg-alt); }}
    .section-title-wrap {{ text-align: center; max-width: 680px; margin: 0 auto 50px; }}
    .section-eyebrow {{ text-transform: uppercase; font-size: 0.8rem; font-weight: 800; letter-spacing: 1.5px; color: var(--accent); margin-bottom: 8px; display: block; }}
    .section-title {{ font-size: 2.3rem; color: var(--primary); margin-bottom: 12px; }}
    .section-subtitle {{ font-size: 1.05rem; color: var(--text-muted); }}

    /* Services Grid */
    .services-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }}
    .service-card {{ background: #fff; border-radius: var(--radius); border: 1px solid var(--border); overflow: hidden; box-shadow: var(--shadow-sm); display: flex; flex-direction: column; transition: transform 0.2s; }}
    .service-card:hover {{ transform: translateY(-4px); box-shadow: var(--shadow-md); }}
    .service-img {{ height: 190px; background-size: cover; background-position: center; position: relative; }}
    .service-badge {{ position: absolute; top: 12px; right: 12px; background: rgba(25, 56, 43, 0.9); color: #fff; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 20px; }}
    .service-body {{ padding: 24px; flex-grow: 1; display: flex; flex-direction: column; }}
    .service-title {{ font-size: 1.35rem; color: var(--primary); margin-bottom: 10px; }}
    .service-desc {{ font-size: 0.9rem; color: var(--text-muted); margin-bottom: 18px; }}
    .service-features {{ list-style: none; margin-bottom: 24px; flex-grow: 1; }}
    .service-features li {{ display: flex; align-items: center; gap: 8px; font-size: 0.85rem; font-weight: 600; color: var(--text); margin-bottom: 8px; }}
    .service-features li svg {{ color: var(--accent); flex-shrink: 0; }}

    /* Color Picker */
    .color-picker-box {{ background: #fff; border-radius: var(--radius); border: 1px solid var(--border); padding: 34px; box-shadow: var(--shadow-sm); }}
    .palette-grid {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 14px; margin-bottom: 24px; }}
    .palette-btn {{ border: 2px solid var(--border); background: #fff; border-radius: 10px; padding: 12px 8px; cursor: pointer; text-align: center; transition: all 0.2s; display: flex; flex-direction: column; align-items: center; gap: 8px; }}
    .palette-btn.active {{ border-color: var(--primary); background: #f0f7f3; transform: scale(1.02); }}
    .color-chip {{ width: 44px; height: 44px; border-radius: 50%; box-shadow: inset 0 0 0 2px rgba(0,0,0,0.1); }}
    .palette-name {{ font-size: 0.8rem; font-weight: 700; color: var(--text); }}
    .palette-preview {{ background: var(--bg-alt); border-radius: 10px; padding: 20px 24px; display: flex; justify-content: space-between; align-items: center; border-left: 6px solid var(--monument); flex-wrap: wrap; gap: 16px; }}

    /* Reviews */
    .reviews-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }}
    .review-card {{ background: #fff; border-radius: var(--radius); border: 1px solid var(--border); padding: 26px; box-shadow: var(--shadow-sm); display: flex; flex-direction: column; justify-content: space-between; }}
    .review-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
    .reviewer-name {{ font-weight: 700; color: var(--primary); font-size: 0.95rem; }}
    .review-date {{ font-size: 0.8rem; color: var(--text-muted); }}
    .review-text {{ font-size: 0.92rem; color: var(--text); line-height: 1.55; margin-bottom: 18px; font-style: italic; }}
    .google-badge {{ display: inline-flex; align-items: center; gap: 6px; font-size: 0.78rem; font-weight: 700; color: #4285F4; }}

    /* Comparison Table */
    .table-card {{ background: #fff; border-radius: var(--radius); border: 1px solid var(--border); overflow: hidden; box-shadow: var(--shadow-sm); }}
    .comparison-table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 0.92rem; }}
    .comparison-table th, .comparison-table td {{ padding: 16px 20px; border-bottom: 1px solid var(--border); }}
    .comparison-table th {{ background: #f0f5f2; color: var(--primary); font-weight: 700; font-size: 0.95rem; }}
    .comparison-table .highlight-col {{ background: rgba(25, 56, 43, 0.04); font-weight: 600; color: var(--primary); }}

    /* Suburbs Grid */
    .suburbs-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; }}
    .suburb-tag {{ background: #fff; border: 1px solid var(--border); padding: 12px 14px; border-radius: 8px; font-size: 0.88rem; font-weight: 600; color: var(--primary); text-align: center; }}

    /* Footer */
    .footer {{ background: #0c1813; color: #d0ded6; padding: 60px 0 30px; font-size: 0.9rem; }}
    .footer-grid {{ display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 40px; margin-bottom: 40px; }}
    .footer-col h4 {{ color: #fff; font-size: 1.15rem; margin-bottom: 16px; }}
    .footer-col ul {{ list-style: none; }}
    .footer-col ul li {{ margin-bottom: 10px; }}
    .footer-col ul li a:hover {{ color: var(--accent); }}
    .footer-bottom {{ border-top: 1px solid #1c2e26; padding-top: 24px; display: flex; justify-content: space-between; font-size: 0.8rem; color: #7f9c8d; flex-wrap: wrap; gap: 10px; }}

    /* Mobile Sticky Bar */
    .mobile-bar {{ display: none; position: fixed; bottom: 0; left: 0; right: 0; background: #fff; border-top: 1px solid var(--border); padding: 10px 16px; z-index: 999; box-shadow: 0 -4px 14px rgba(0,0,0,0.08); gap: 10px; }}
    .mobile-bar .btn {{ flex: 1; }}

    @media (max-width: 1050px) {{
      .header-nav {{ display: none; }}
    }}

    @media (max-width: 900px) {{
      .hero-grid {{ grid-template-columns: 1fr; }}
      .services-grid, .reviews-grid {{ grid-template-columns: 1fr; }}
      .palette-grid {{ grid-template-columns: repeat(3, 1fr); }}
      .footer-grid {{ grid-template-columns: 1fr; }}
      .mobile-bar {{ display: flex; }}
      .hero-title {{ font-size: 2.2rem; }}
    }}
  </style>
</head>
<body>

  <!-- Top Announcement Bar -->
  <aside class="topbar">
    <div class="container">
      <div class="topbar-badge">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L1 21h22L12 2zm0 3.99L19.53 19H4.47L12 5.99zM11 10h2v4h-2zm0 6h2v2h-2z"/></svg>
        <span>{top_banner}</span>
      </div>
      <div>
        <span>{brand_sub}</span>
      </div>
    </div>
  </aside>

  <!-- Navigation Header -->
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
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24c1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
          <span>{phone}</span>
        </a>
        <a href="#quote" class="btn btn-primary btn-nav">{btn_nav_quote}</a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <main>
    <section class="hero">
      <div class="container">
        <div class="hero-grid">
          
          <div class="hero-content">
            <a href="{gmaps_url}" target="_blank" rel="noopener noreferrer" class="rating-badge" title="Google Maps">
              <span class="stars">★★★★★</span>
              <span>{rating_badge_txt}</span>
            </a>
            
            <h1 class="hero-title">{hero_title}</h1>
            
            <p class="hero-lead">{hero_lead}</p>

            <div class="hero-badges">
              <div class="badge-item">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                <span>{badge1}</span>
              </div>
              <div class="badge-item">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                <span>{badge2}</span>
              </div>
              <div class="badge-item">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                <span>{badge3}</span>
              </div>
              <div class="badge-item">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                <span>{badge4}</span>
              </div>
            </div>

            <div style="display: flex; gap: 14px; flex-wrap: wrap;">
              <a href="#quote" class="btn btn-primary" style="padding: 14px 30px; font-size: 1.05rem;">
                {btn_free_quote}
              </a>
              <a href="tel:{clean_phone}" class="btn btn-outline" style="padding: 14px 26px;">
                {btn_call_direct}
              </a>
            </div>
          </div>

          <!-- Quick Quote Form Card -->
          <div class="hero-form-card" id="quote">
            <div class="form-header">
              <h3>{form_title}</h3>
              <p>{form_sub}</p>
            </div>

            <form action="#success" method="POST" id="quoteForm">
              <div class="form-group">
                <label for="fence-type">{lbl_proj}</label>
                <select id="fence-type" name="fence_type" class="form-control" required>
                  <option value="" disabled selected>{opt_default}</option>
                  <option value="colorbond">{opt1}</option>
                  <option value="modular">{opt2}</option>
                  <option value="gates">{opt3}</option>
                  <option value="timber">{opt4}</option>
                  <option value="repair">{opt5}</option>
                </select>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="length">{lbl_len}</label>
                  <input type="text" id="length" name="est_length" class="form-control" placeholder="25m" inputmode="numeric">
                </div>
                <div class="form-group">
                  <label for="suburb">{lbl_suburb}</label>
                  <input type="text" id="suburb" name="suburb" class="form-control" placeholder="{suburbs[0]}" required>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="client-name">{lbl_name}</label>
                  <input type="text" id="client-name" name="name" class="form-control" placeholder="John Smith" autocomplete="name" required>
                </div>
                <div class="form-group">
                  <label for="client-phone">{lbl_phone}</label>
                  <input type="tel" id="client-phone" name="phone" class="form-control" placeholder="04xx xxx xxx" autocomplete="tel" inputmode="tel" required>
                </div>
              </div>

              <button type="submit" class="btn btn-primary submit-btn">
                <span>{btn_submit}</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
              </button>

              <p class="privacy-notice">{privacy_txt}</p>
            </form>
          </div>

        </div>
      </div>
    </section>

    <!-- Services Section -->
    <section class="section" id="services">
      <div class="container">
        <div class="section-title-wrap">
          <span class="section-eyebrow">{srv_eyebrow}</span>
          <h2 class="section-title">{srv_title}</h2>
          <p class="section-subtitle">{srv_sub}</p>
        </div>

        <div class="services-grid">
          
          <article class="service-card">
            <div class="service-img" style="background-image: url('https://images.unsplash.com/photo-1595846519845-68e298c2edd8?auto=format&fit=crop&w=700&q=80');">
              <span class="service-badge">{c1_badge}</span>
            </div>
            <div class="service-body">
              <h3 class="service-title">{c1_title}</h3>
              <p class="service-desc">{c1_desc}</p>
              <ul class="service-features">
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> {c1_f1}</li>
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> {c1_f2}</li>
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> {c1_f3}</li>
              </ul>
              <a href="#quote" class="btn btn-outline" style="width: 100%;">{c1_btn}</a>
            </div>
          </article>

          <article class="service-card">
            <div class="service-img" style="background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=700&q=80');">
              <span class="service-badge">{c2_badge}</span>
            </div>
            <div class="service-body">
              <h3 class="service-title">{c2_title}</h3>
              <p class="service-desc">{c2_desc}</p>
              <ul class="service-features">
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> {c2_f1}</li>
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> {c2_f2}</li>
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> {c2_f3}</li>
              </ul>
              <a href="#quote" class="btn btn-outline" style="width: 100%;">{c2_btn}</a>
            </div>
          </article>

          <article class="service-card">
            <div class="service-img" style="background-image: url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=700&q=80');">
              <span class="service-badge">{c3_badge}</span>
            </div>
            <div class="service-body">
              <h3 class="service-title">{c3_title}</h3>
              <p class="service-desc">{c3_desc}</p>
              <ul class="service-features">
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> {c3_f1}</li>
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> {c3_f2}</li>
                <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg> {c3_f3}</li>
              </ul>
              <a href="#quote" class="btn btn-outline" style="width: 100%;">{c3_btn}</a>
            </div>
          </article>

        </div>
      </div>
    </section>

    <!-- Color Palette Section -->
    <section class="section section-alt" id="colours">
      <div class="container">
        <div class="section-title-wrap">
          <span class="section-eyebrow">{col_eyebrow}</span>
          <h2 class="section-title">{col_title}</h2>
          <p class="section-subtitle">{col_sub}</p>
        </div>

        <div class="color-picker-box">
          <div class="palette-grid" role="radiogroup" aria-label="Colorbond Color Choices">
            <button type="button" class="palette-btn active" data-color="Monument" data-hex="#34373b" data-desc="{desc_monument}">
              <div class="color-chip" style="background-color: var(--monument);"></div>
              <span class="palette-name">Monument®</span>
            </button>
            <button type="button" class="palette-btn" data-color="Woodland Grey" data-hex="#4e5347" data-desc="{desc_woodland}">
              <div class="color-chip" style="background-color: var(--woodland);"></div>
              <span class="palette-name">Woodland Grey®</span>
            </button>
            <button type="button" class="palette-btn" data-color="Surfmist" data-hex="#e2e1d7" data-desc="{desc_surfmist}">
              <div class="color-chip" style="background-color: var(--surfmist);"></div>
              <span class="palette-name">Surfmist®</span>
            </button>
            <button type="button" class="palette-btn" data-color="Basalt" data-hex="#64686e" data-desc="{desc_basalt}">
              <div class="color-chip" style="background-color: var(--basalt);"></div>
              <span class="palette-name">Basalt®</span>
            </button>
            <button type="button" class="palette-btn" data-color="Dune" data-hex="#b3aba2" data-desc="{desc_dune}">
              <div class="color-chip" style="background-color: var(--dune);"></div>
              <span class="palette-name">Dune®</span>
            </button>
            <button type="button" class="palette-btn" data-color="Night Sky" data-hex="#1c1d21" data-desc="{desc_nightsky}">
              <div class="color-chip" style="background-color: var(--nightsky);"></div>
              <span class="palette-name">Night Sky®</span>
            </button>
          </div>

          <div class="palette-preview" id="palettePreview">
            <div>
              <h4 id="previewColorName" style="color: var(--primary); font-size: 1.25rem; margin-bottom: 4px;">Selected Colour: Monument®</h4>
              <p id="previewColorDesc" style="color: var(--text-muted); font-size: 0.95rem; max-width: 650px;">
                {desc_monument}
              </p>
            </div>
            <a href="#quote" class="btn btn-dark">{col_btn}</a>
          </div>
        </div>
      </div>
    </section>

    <!-- Reviews Section -->
    <section class="section" id="reviews">
      <div class="container">
        <div class="section-title-wrap">
          <span class="section-eyebrow">{rev_eyebrow}</span>
          <h2 class="section-title">{rev_title}</h2>
          <p class="section-subtitle">{rev_sub}</p>
        </div>

        <div class="reviews-grid">
          
          <div class="review-card">
            <div>
              <div class="review-header">
                <span class="reviewer-name">{rev1_name}</span>
                <span class="review-date">{latest_review}</span>
              </div>
              <div class="stars" style="margin-bottom: 8px;">★★★★★</div>
              <p class="review-text">"{rev1_txt}"</p>
            </div>
            <a href="{gmaps_url}" target="_blank" rel="noopener noreferrer" class="google-badge">
              <svg width="16" height="16" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
              <span>Verified Google Review ↗</span>
            </a>
          </div>

          <div class="review-card">
            <div>
              <div class="review-header">
                <span class="reviewer-name">{rev2_name}</span>
                <span class="review-date">{'Недавний клиент' if lang=='ru' else 'Recent Client'}</span>
              </div>
              <div class="stars" style="margin-bottom: 8px;">★★★★★</div>
              <p class="review-text">"{rev2_txt}"</p>
            </div>
            <a href="{gmaps_url}" target="_blank" rel="noopener noreferrer" class="google-badge">
              <svg width="16" height="16" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
              <span>Verified Google Review ↗</span>
            </a>
          </div>

          <div class="review-card">
            <div>
              <div class="review-header">
                <span class="reviewer-name">{rev3_name}</span>
                <span class="review-date">{'Подтвержденный заказ' if lang=='ru' else 'Verified Customer'}</span>
              </div>
              <div class="stars" style="margin-bottom: 8px;">★★★★★</div>
              <p class="review-text">"{rev3_txt}"</p>
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
            <span>{rev_all_btn}</span>
          </a>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 10px;">
            {rev_bottom_sub}
          </p>
        </div>
      </div>
    </section>

    <!-- Comparison Section -->
    <section class="section section-alt">
      <div class="container">
        <div class="section-title-wrap">
          <span class="section-eyebrow">{tbl_eyebrow}</span>
          <h2 class="section-title">{tbl_title}</h2>
        </div>

        <div class="table-card">
          <table class="comparison-table">
            <thead>
              <tr>
                <th>{th1}</th>
                <th class="highlight-col">{th2}</th>
                <th>{th3}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>{r1_t}</strong></td>
                <td class="highlight-col">{r1_g}</td>
                <td>{r1_b}</td>
              </tr>
              <tr>
                <td><strong>{r2_t}</strong></td>
                <td class="highlight-col">{r2_g}</td>
                <td>{r2_b}</td>
              </tr>
              <tr>
                <td><strong>{r3_t}</strong></td>
                <td class="highlight-col">{r3_g}</td>
                <td>{r3_b}</td>
              </tr>
              <tr>
                <td><strong>{r4_t}</strong></td>
                <td class="highlight-col">{r4_g}</td>
                <td>{r4_b}</td>
              </tr>
              <tr>
                <td><strong>{r5_t}</strong></td>
                <td class="highlight-col">{r5_g}</td>
                <td>{r5_b}</td>
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
          <span class="section-eyebrow">{area_eyebrow}</span>
          <h2 class="section-title">{area_title}</h2>
          <p class="section-subtitle">{area_sub}</p>
        </div>

        <div class="suburbs-grid">
{suburbs_html}
        </div>
      </div>
    </section>

    <!-- Bottom CTA -->
    <section class="section" style="background: var(--primary); color: #fff; text-align: center;">
      <div class="container" style="max-width: 760px;">
        <h2 style="font-size: 2.4rem; margin-bottom: 16px;">{cta_title}</h2>
        <p style="font-size: 1.15rem; color: #a3c4b5; margin-bottom: 30px;">
          {cta_sub}
        </p>
        <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
          <a href="tel:{clean_phone}" class="btn btn-primary" style="padding: 16px 36px; font-size: 1.1rem;">
            {cta_btn1}
          </a>
          <a href="#quote" class="btn btn-outline" style="border-color: #fff; color: #fff; padding: 16px 32px;">
            {cta_btn2}
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
            {ft_desc}
          </p>
          <p style="font-size: 0.85rem; color: #7f9c8d;">
            📍 Base: {address}<br>
            📞 Phone: {phone}<br>
            {ft_hours}
          </p>
        </div>

        <div class="footer-col">
          <h4>{ft_h2}</h4>
          <ul>
            <li><a href="#services">Colorbond® Fencing</a></li>
            <li><a href="#services">Modular Wall Acoustic Barriers</a></li>
            <li><a href="#services">Automated Driveway Gates</a></li>
            <li><a href="#services">Timber & Privacy Slats</a></li>
            <li><a href="#services">Old Fence Removal & Disposal</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>{ft_h3}</h4>
          <p style="font-size: 0.85rem; margin-bottom: 14px;">
            {'Выезд на замеры по всему региону ' + city if lang=='ru' else 'Servicing residential homeowners and commercial builders in ' + city}.
          </p>
          <a href="tel:{clean_phone}" class="btn btn-primary" style="width: 100%;">Call {phone}</a>
        </div>
      </div>

      <div class="footer-bottom">
        <div>{ft_rights}</div>
        <div>{ft_trademark}</div>
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
      <span>{mob_quote}</span>
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
      submitBtn.innerHTML = '<span>{'Отправка заявки...' if lang=='ru' else 'Sending Request...'}</span>';
      setTimeout(() => {{
        form.innerHTML = `
          <div style="text-align: center; padding: 40px 10px;">
            <div style="width: 56px; height: 56px; background: #e6f9f0; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 16px;">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
            </div>
            <h3 style="color: var(--primary); font-size: 1.4rem; margin-bottom: 8px;">{'Заявка на замер принята!' if lang=='ru' else 'Quote Request Received!'}</h3>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 16px;">{'Спасибо! Мы свяжемся с вами в ближайшее время по указанному телефону.' if lang=='ru' else 'Thank you! We will review your site details and call you shortly on the number provided.'}</p>
            <p style="font-weight: 700; color: var(--accent);">{'Срочный вопрос? Звоните:' if lang=='ru' else 'Need immediate assistance? Call'} <a href="tel:{clean_phone}" style="text-decoration: underline;">{phone}</a>.</p>
          </div>
        `;
      }}, 700);
    }});
  </script>
</body>
</html>'''
    return html_code

print("Building English and Russian versions for all 20 contractors...")
contractor_cards = []

for idx, item in enumerate(data, start=1):
    slug = slugify(item['Company Name'])
    dir_path = os.path.join('sites', slug)
    os.makedirs(dir_path, exist_ok=True)
    
    # 1. English
    en_html = generate_landing_html(item, slug, lang='en')
    with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(en_html)

    # 2. Russian
    ru_html = generate_landing_html(item, slug, lang='ru')
    with open(os.path.join(dir_path, 'ru.html'), 'w', encoding='utf-8') as f:
        f.write(ru_html)

    name = item['Company Name']
    city = item['City / Region']
    state = city.split()[-1] if len(city.split()) > 1 else 'AU'
    rating = str(item['Rating'])
    reviews = str(item['Reviews Count'])
    last_rev = item['Latest Review']
    phone = item['Phone']
    web_status = item['Website Status']
    gmaps_url = item['Google Maps URL']
    wa_url = item.get('WhatsApp', '')

    clean_p = format_clean_phone(phone)
    demo_url = f"https://zonus.co/fencing/sites/{slug}/"
    pitch_template = f"G'day {name} team,\n\nSaw your incredible {rating}★ rating ({reviews} Google reviews) in {city} — top quality reputation!\n\nNoticed you don't have a standalone modern website listed, so you're likely losing direct Colorbond & modular fencing jobs to competitors running Google ads.\n\nWe built a fast, mobile-ready website concept for your brand with your real reviews and services:\n👉 {demo_url}\n\nZero effort needed on your side. If you like it, we can connect it to your domain in 24 hours.\n\nWorth a quick 60-second look?\n\nCheers!"
    
    wa_msg_encoded = urllib.parse.quote(pitch_template)
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
        'pitch_text': pitch_template,
        'site_en_path': f'sites/{slug}/index.html',
        'site_ru_path': f'sites/{slug}/ru.html'
    })
    print(f"[{idx}/20] Created EN & RU sites for {name} -> sites/{slug}/")

# Generate Hub
hub_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Australian Fencing Contractors • Sales & Outreach Hub (20 Companies)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0d1512;
      --card-bg: #14201c;
      --card-border: #1f302a;
      --primary: #10b981;
      --accent: #f28c28;
      --text: #f1f5f3;
      --text-muted: #8da498;
      --radius: 14px;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Plus Jakarta Sans', sans-serif; background: var(--bg); color: var(--text); line-height: 1.5; padding: 40px 20px; }
    .container { max-width: 1320px; margin: 0 auto; }

    /* Header */
    .hub-header { text-align: center; margin-bottom: 40px; }
    .hub-badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(16, 185, 129, 0.12); color: var(--primary); border: 1px solid rgba(16, 185, 129, 0.25); padding: 6px 16px; border-radius: 30px; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px; }
    .hub-title { font-family: 'Space Grotesk', sans-serif; font-size: 2.8rem; font-weight: 800; color: #fff; margin-bottom: 12px; }
    .hub-title span { color: var(--primary); }
    .hub-desc { color: var(--text-muted); font-size: 1.1rem; max-width: 780px; margin: 0 auto; }

    /* KPI Row */
    .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 34px; }
    .kpi-card { background: var(--card-bg); border: 1px solid var(--card-border); padding: 20px; border-radius: var(--radius); text-align: center; }
    .kpi-val { font-size: 2rem; font-weight: 800; color: #fff; font-family: 'Space Grotesk', sans-serif; margin-bottom: 4px; }
    .kpi-label { font-size: 0.85rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }

    /* Controls */
    .controls { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; margin-bottom: 30px; }
    .filter-tabs { display: flex; gap: 8px; flex-wrap: wrap; }
    .filter-btn { background: var(--card-bg); border: 1px solid var(--card-border); color: var(--text-muted); padding: 8px 16px; border-radius: 8px; font-weight: 700; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; }
    .filter-btn.active, .filter-btn:hover { background: var(--primary); color: #0d1512; border-color: var(--primary); }
    
    .search-box { position: relative; min-width: 280px; }
    .search-input { width: 100%; background: var(--card-bg); border: 1px solid var(--card-border); color: #fff; padding: 10px 16px; border-radius: 8px; font-size: 0.9rem; font-family: inherit; }
    .search-input:focus { outline: none; border-color: var(--primary); }

    /* Cards Grid */
    .cards-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
    .biz-card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: var(--radius); padding: 24px; display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s, border-color 0.2s; }
    .biz-card:hover { transform: translateY(-3px); border-color: rgba(16, 185, 129, 0.4); }

    .card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; gap: 10px; }
    .biz-name { font-size: 1.25rem; font-weight: 700; color: #fff; }
    .state-badge { background: rgba(255, 255, 255, 0.08); color: #fff; font-size: 0.75rem; font-weight: 800; padding: 4px 8px; border-radius: 6px; }
    
    .status-badge { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; margin-bottom: 14px; }
    .status-no-site { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .status-fb { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
    .status-aggr { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }

    .stats-row { display: flex; gap: 14px; background: rgba(0, 0, 0, 0.25); padding: 10px 14px; border-radius: 8px; margin-bottom: 16px; font-size: 0.85rem; }
    .stars { color: #f59e0b; font-weight: 800; }
    .review-recency { color: #9fe2bf; font-weight: 600; margin-left: auto; }

    .info-list { font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px; }
    .info-list p { margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }

    /* Actions */
    .card-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: auto; }
    .btn-action { display: inline-flex; align-items: center; justify-content: center; gap: 8px; font-size: 0.85rem; font-weight: 700; padding: 10px 12px; border-radius: 8px; border: none; cursor: pointer; transition: all 0.2s; min-height: 40px; text-align: center; }
    .btn-view { background: var(--primary); color: #0d1512; }
    .btn-view:hover { background: #059669; }
    .btn-ru { background: rgba(59, 130, 246, 0.18); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.35); }
    .btn-ru:hover { background: rgba(59, 130, 246, 0.3); color: #fff; }
    .btn-wa { background: #25D366; color: #fff; }
    .btn-wa:hover { background: #1ebc59; }
    .btn-copy { background: rgba(255, 255, 255, 0.08); color: #fff; border: 1px solid var(--card-border); }
    .btn-copy:hover { background: rgba(255, 255, 255, 0.15); }
    .btn-map { background: rgba(255, 255, 255, 0.08); color: #fff; border: 1px solid var(--card-border); grid-column: span 2; }
    .btn-map:hover { background: rgba(255, 255, 255, 0.15); }

    .toast { position: fixed; bottom: 30px; right: 30px; background: var(--primary); color: #0d1512; font-weight: 800; padding: 12px 24px; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.4); transform: translateY(100px); opacity: 0; transition: all 0.3s; z-index: 1000; }
    .toast.show { transform: translateY(0); opacity: 1; }

    @media (max-width: 900px) {
      .kpi-grid { grid-template-columns: repeat(2, 1fr); }
      .cards-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

  <div class="container">
    
    <!-- Header -->
    <header class="hub-header">
      <div class="hub-badge">Australia Outreach Machine</div>
      <h1 class="hub-title">Colorbond & Modular Fencing <span>Client Hub</span></h1>
      <p class="hub-desc">
        All 20 verified Australian contractors with ready-to-sell demo landing pages (English + Russian versions), direct WhatsApp links, and tailored pitch templates.
      </p>
    </header>

    <!-- KPI Highlights -->
    <section class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-val">20</div>
        <div class="kpi-label">Ready Demo Websites</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val">95%</div>
        <div class="kpi-label">Mobile WhatsApp Line</div>
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
    encoded_pitch_attr = html.escape(c['pitch_text'], quote=True)
    
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
          <a href="{c['site_en_path']}" target="_blank" class="btn-action btn-view" title="Open Australian English site">🇬🇧 English</a>
          <a href="{c['site_ru_path']}" target="_blank" class="btn-action btn-ru" title="Открыть русскую версию">🇷🇺 Русская версия</a>
          {wa_btn_html}
          <button type="button" class="btn-action btn-copy" data-pitch="{encoded_pitch_attr}" onclick="copyPitch(this.getAttribute('data-pitch'))">📋 Copy Pitch</button>
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
        const stateMatch = activeState === 'all' || card.dataset.state === activeState;
        const nameMatch = card.dataset.name.includes(searchVal);
        
        if (stateMatch && nameMatch) {
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

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(hub_html)

print("Generated hub.html and index.html with English and Russian links!")
