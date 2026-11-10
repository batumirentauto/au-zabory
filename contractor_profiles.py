import os
import json
import re
import html
import urllib.parse

# 1. Load real data
with open('colorbond_modular_fencing_australia.json', 'r', encoding='utf-8') as f:
    raw_contractors = json.load(f)

with open('contractors_real_reviews.json', 'r', encoding='utf-8') as f:
    real_data = json.load(f)

real_by_place_id = {c['place_id']: c for c in real_data}
real_by_name = {c['name']: c for c in real_data}

# Pool of verified real Australian fencing photos (from real contractors) for fallbacks
all_real_photos_pool = []
for c in real_data:
    all_real_photos_pool.extend(c['real_photos'])

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def clean_phone_number(p):
    return re.sub(r'[^\d+]', '', p)

# Suburbs mapping
SUBURBS_MAP = {
    'Sydney NSW': ['Blacktown', 'Castle Hill', 'Parramatta', 'Penrith', 'Liverpool', 'Campbelltown', 'Hornsby', 'Northern Beaches', 'Sutherland Shire', 'Cronulla', 'Ryde', 'Baulkham Hills'],
    'Melbourne VIC': ['Frankston', 'Dandenong', 'Berwick', 'Werribee', 'Point Cook', 'Geelong', 'Craigieburn', 'Sunbury', 'Mornington Peninsula', 'Ringwood', 'Box Hill'],
    'Brisbane QLD': ['Ipswich', 'Logan City', 'Caboolture', 'Chermside', 'Capalaba', 'Redcliffe', 'Springfield', 'Cleveland', 'North Lakes', 'Underwood', 'Sunnybank'],
    'Perth WA': ['Joondalup', 'Mandurah', 'Rockingham', 'Armadale', 'Fremantle', 'Midland', 'Baldivis', 'Canning Vale', 'Morley', 'Scarborough', 'Ellenbrook'],
    'Adelaide SA': ['Mawson Lakes', 'Marion', 'Salisbury', 'Morphett Vale', 'Golden Grove', 'Glenelg', 'Mount Barker', 'Gawler', 'Hallett Cove', 'Norwood'],
    'Canberra ACT': ['Belconnen', 'Tuggeranong', 'Gungahlin', 'Woden Valley', 'Queanbeyan', 'Weston Creek', 'Fyshwick', 'Bruce', 'Kambah', 'Franklin']
}

# Colorbond colors
COLORBOND_COLOURS = [
    {"name": "Monument®", "hex": "#383E42", "desc": "Deep charcoal. Australia's #1 color."},
    {"name": "Woodland Grey®", "hex": "#4D4F4B", "desc": "Subtle green-grey olive modern tone."},
    {"name": "Surfmist®", "hex": "#D8D9D0", "desc": "Crisp off-white, heat reflective."},
    {"name": "Dover White™", "hex": "#E3E4DF", "desc": "Bright clean white architectural finish."},
    {"name": "Basalt®", "hex": "#5D6063", "desc": "Modern mid-tone mineral grey."},
    {"name": "Ironstone®", "hex": "#353E4B", "desc": "Deep navy steel blue-grey tone."},
    {"name": "Shale Grey™", "hex": "#8A8D8F", "desc": "Silvery stone grey, airy neutral."},
    {"name": "Night Sky®", "hex": "#1F2022", "desc": "Pure architectural satin black."}
]

# Contractor Personalities, Specialties, and Review Translations
CONTRACTOR_PROFILES = {
    "Underwood Fencing and Gates": {
        "lead_name": "Max",
        "lead_name_ru": "Макс",
        "specialty_en": "Colorbond® Boundary & Retaining Wall Privacy Fencing",
        "specialty_ru": "Заборы Colorbond® на склонах, подпорные стенки и автоматические ворота",
        "services": [
            {
                "title_en": "Sloped & Retaining Wall Colorbond®",
                "title_ru": "Заборы Colorbond® на склонах и подпорных стенках",
                "badge_en": "Customer Favourite",
                "badge_ru": "Лидер заказов",
                "desc_en": "Precision stepped Colorbond fencing mounted seamlessly along sloped ground and on top of retaining walls. Built to handle heavy ground pressure.",
                "desc_ru": "Ступенчатый монтаж Colorbond на сложных перепадах высот и подпорных стенках. Усиленный каркас, рассчитанный на подвижки грунта.",
                "features_en": ["Retaining wall mounting", "Stepped stepped panels", "Genuine BlueScope® steel"],
                "features_ru": ["Монтаж по верху подпорных стенок", "Ступенчатая подгонка под рельеф", "Оригинальная сталь BlueScope®"]
            },
            {
                "title_en": "Modular Acoustic Boundary Walls",
                "title_ru": "Модульные шумоизоляционные стены",
                "badge_en": "Noise Reduction",
                "badge_ru": "Шумоизоляция",
                "desc_en": "Eliminate traffic noise and nosy neighbours with solid modular wall systems. Up to 25dB noise dampening with a luxury rendered look.",
                "desc_ru": "Качественная звукоизоляция до 25 дБ и вид монолитной каменной стены без дорогого ленточного фундамента.",
                "features_en": ["Up to 25dB noise reduction", "Rendered textured finish", "Rapid installation"],
                "features_ru": ["Снижение шума трассы и соседей", "Фактурная отделка под фасад", "Быстрый чистый монтаж"]
            },
            {
                "title_en": "Automated Sliding & Swing Gates",
                "title_ru": "Автоматические откатные и распашные ворота",
                "badge_en": "Custom Motorised",
                "badge_ru": "Автоматика под ключ",
                "desc_en": "Heavy-duty electric driveway gates matched to your Colorbond fence. Powered by durable Italian motors with remote and smartphone access.",
                "desc_ru": "Мощные откатные и распашные ворота в цвет забора. Надежная автоматика, пульты ДУ и управление со смартфона.",
                "features_en": ["Heavy duty steel frame", "Remote & keypad entry", "Colour-matched infill"],
                "features_ru": ["Усиленная рама", "Пульты ДУ и кодовая панель", "100% совпадение по цвету"]
            }
        ],
        "reviews_ru": [
            "Профессионализм высшего уровня и исключительное отношение к клиенту! Макс проделал потрясающую работу: не только идеально смонтировал забор, но и решил сложнейший вопрос с уклоном на границе участка.",
            "Мы долго мучились с нашим покосившимся забором из блоков и не знали, что делать. Макс приехал, сразу предложил надежное решение и за 2 дня установил новый забор Colorbond с идеальной линией.",
            "Макс делал для нас уже два проекта, и мы в восторге от обоих. С ним легко и приятно общаться, все сделано в срок и без единой скрытой доплаты.",
            "Мы доверяем Максу все наши строительные проекты на протяжении многих лет и даже не думаем искать кого-то другого. Его внимание к деталям и аккуратность выше всяких похвал.",
            "Макс проделал отличную работу по установке приватного ограждения прямо по верху подпорной стенки в нашем заднем саду. Очень надежно и выглядит на миллион."
        ]
    },
    "Affordable Fencing Company": {
        "lead_name": "Arthur and Kiri",
        "lead_name_ru": "Артур и Кири",
        "specialty_en": "Old Timber Fence Replacement & Custom Gates",
        "specialty_ru": "Замена старых деревянных заборов на Colorbond и калитки под ключ",
        "services": [
            {
                "title_en": "Rotten Timber to Colorbond® Upgrade",
                "title_ru": "Замена старого деревянного забора на Colorbond®",
                "badge_en": "Fast Turnaround",
                "badge_ru": "Быстрая замена",
                "desc_en": "We safely dismantle and remove your leaning, rotting timber fence and replace it with arrow-straight genuine BlueScope Colorbond in 48 hours.",
                "desc_ru": "Аккуратный демонтаж и вывоз старого гнилого деревянного забора. Монтаж нового стального забора Colorbond за 48 часов.",
                "features_en": ["Full timber disposal included", "Termite & fire proof", "No maintenance painting"],
                "features_ru": ["Вывоз и утилизация старого забора", "Защита от термитов и огня", "Никакой покраски на 20+ лет"]
            },
            {
                "title_en": "Custom Aluminium Slat & Side Gates",
                "title_ru": "Калитки и ворота из алюминиевых ламелей",
                "badge_en": "Secure Access",
                "badge_ru": "Безопасность",
                "desc_en": "Architectural pedestrian side gates and double driveway gates. Premium powder coating, heavy-duty latching and keyed locks.",
                "desc_ru": "Стильные боковые калитки и распашные ворота. Порошковая покраска в тон фасада, врезные замки и надежная фурнитура.",
                "features_en": ["Rust-free aluminium", "Keyed lock sets", "Precision alignment"],
                "features_ru": ["Не ржавеет у моря", "Замки с ключом", "Идеальный зазор и геометрия"]
            },
            {
                "title_en": "Perimeter Privacy Fencing (1.8m - 2.1m)",
                "title_ru": "Высокие заборы для полной приватности",
                "badge_en": "Full Privacy",
                "badge_ru": "Максимальная приватность",
                "desc_en": "Complete screening from neighbours and streets. Reinforced posts set deep in 600mm concrete footings to withstand coastal winds.",
                "desc_ru": "Полная изоляция участка от посторонних глаз. Столбы бетонируются на глубину от 600 мм для стойкости к сильным ветрам.",
                "features_en": ["1.8m & 2.1m heights available", "Deep concrete footings", "Wind-resistant frame"],
                "features_ru": ["Высота 1.8 м и 2.1 м", "Глубокое бетонирование столбов", "Устойчивость к штормам"]
            }
        ],
        "reviews_ru": [
            "Отличный сервис и результат от Кири! Наш старый деревянный забор буквально падал, но Кири оперативно приехал, все демонтировал и поставил новый великолепный забор.",
            "Артур и Кири — настоящие профи, приехали точно по графику, работать с ними было одно удовольствие. Сделка и монтаж прошли без малейших заминок.",
            "Эти ребята — лучшие в своем деле, невероятно честные и приятные в общении мастера. Другие компании заламывали цены, а тут все четко и прозрачно.",
            "Очень довольна новой калиткой, которую установили Affordable Fencing в Марубре. Кири и Артур были вежливы, приехали вовремя и оставили за собой идеальную чистоту."
        ]
    },
    "Anthony's Fencing": {
        "lead_name": "Nick",
        "lead_name_ru": "Ник",
        "specialty_en": "Feature Fencing & Backyard Transformations",
        "specialty_ru": "Дизайнерские заборы, ламели и полное преображение участков",
        "services": [
            {
                "title_en": "Designer Feature Fencing",
                "title_ru": "Дизайнерские акцентные заборы",
                "badge_en": "Architectural",
                "badge_ru": "Премиум стиль",
                "desc_en": "Elevate your property value with modern horizontal slat infills, contrasting post trims, and seamless architectural fence panels.",
                "desc_ru": "Современные горизонтальные ламели, контрастные темные столбы и премиальная эстетика, увеличивающая стоимость дома.",
                "features_en": ["Horizontal slat screens", "Contemporary colour pairings", "Zero visible fixings"],
                "features_ru": ["Горизонтальные жалюзи/ламели", "Контрастные цветовые сочетания", "Скрытый монтаж без саморезов наружу"]
            },
            {
                "title_en": "Boundary Colorbond® Systems",
                "title_ru": "Капитальные заборы Colorbond®",
                "badge_en": "Heavy Duty",
                "badge_ru": "Надежный каркас",
                "desc_en": "Engineered for Australian storm conditions. Australian Bluescope steel with heavy-gauge posts and secure bottom rail locking.",
                "desc_ru": "Проверенная защита от австралийских штормов. Австралийская сталь BlueScope с усиленными стойками и защитой от подкопа.",
                "features_en": ["Bluescope Colorbond steel", "Storm-grade posts", "10-year warranty"],
                "features_ru": ["Сталь BlueScope Colorbond", "Штормостойкие столбы", "Гарантия 10 лет"]
            },
            {
                "title_en": "Custom Security Access Gates",
                "title_ru": "Калитки и ворота с контролем доступа",
                "badge_en": "Custom Built",
                "badge_ru": "Индивидуальный размер",
                "desc_en": "Fabricated to exact millimetre tolerances. Heavy-duty magnetic latches, deadlock options, and smooth hinge movement.",
                "desc_ru": "Изготовление точно по миллиметрам вашего проема. Магнитные доводчики, надежные замки и плавный ход петель.",
                "features_en": ["Magnetic security latches", "Custom widths & heights", "Deadlock integration"],
                "features_ru": ["Магнитные защелки", "Любая ширина проема", "Врезные надежные замки"]
            }
        ],
        "reviews_ru": [
            "Когда Ник пришел на замер, я сразу понял, что найму именно его. Честный, открытый, сразу вник в нюансы и сделал забор просто безупречно.",
            "Не могу нахвалиться работой Anthony's Fencing. Мой старый забор разваливался, а Ник превратил границу участка в настоящее произведение искусства.",
            "Отличный опыт работы с Ником: вежливый, пунктуальный, настоящий мастер своего дела. Забор стоит как влитой по лазерному уровню.",
            "Наш задний двор буквально преобразился! Ник только что завершил акцентную декоративную стену-ограждение. Результат превзошел все ожидания!",
            "Anthony's Fencing сделали невероятную работу от первого звонка до финальной уборки. Качество материалов и сборки высшего класса."
        ]
    },
    "Highline Fencing": {
        "lead_name": "Andrei Petushkov",
        "lead_name_ru": "Андрей Петушков",
        "specialty_en": "Certified Pool Safety Fencing & Colorbond Repairs",
        "specialty_ru": "Сертифицированные ограждения для бассейнов и ремонт Colorbond",
        "services": [
            {
                "title_en": "Certified Pool Fencing Compliance",
                "title_ru": "Сертифицированные заборы для бассейнов",
                "badge_en": "AS1926.1 Certified",
                "badge_ru": "Сертификат безопасности",
                "desc_en": "Fully compliant glass and aluminium pool barriers meeting strict Australian Council safety standards. Guaranteed first-time signoff.",
                "desc_ru": "Полное соответствие строгим австралийским стандартам безопасности AS1926.1. Гарантия прохождения инспекции с первого раза.",
                "features_en": ["Toughened safety glass", "Self-closing magnetic latches", "Council compliance certified"],
                "features_ru": ["Закаленное безопасное стекло", "Самозакрывающиеся замки", "Официальный сертификат для совета"]
            },
            {
                "title_en": "Colorbond® Height Extensions & Repair",
                "title_ru": "Наращивание высоты и ремонт Colorbond®",
                "badge_en": "Fast Response",
                "badge_ru": "Быстрый ремонт",
                "desc_en": "Add slat extensions to existing fences for privacy compliance around pools. Fast replacement of storm-damaged or buckled panels.",
                "desc_ru": "Установка ламельных надстроек на существующий забор для приватности у бассейна. Замена погнутых штормом листов и стоек.",
                "features_en": ["Colorbond extension screens", "Storm repair specialists", "Exact colour matching"],
                "features_ru": ["Надставки для приватности", "Срочный ремонт после бури", "Точный подбор заводского цвета"]
            },
            {
                "title_en": "Boundary Privacy Fencing",
                "title_ru": "Капитальные межевые заборы",
                "badge_en": "Zero Maintenance",
                "badge_ru": "Без ухода",
                "desc_en": "Clean, crisp Colorbond perimeter fencing installed with precision laser leveling. Built to withstand blistering heat and heavy rain.",
                "desc_ru": "Аккуратная установка по лазерному нивелиру. Стойкость к австралийской жаре и ливням без растрескивания и ржавчины.",
                "features_en": ["Bluescope steel warranty", "No rot or warping", "Neat property finish"],
                "features_ru": ["Заводская гарантия BlueScope", "Не гниет и не коробится", "Идеально ровная линия"]
            }
        ],
        "reviews_ru": [
            "Когда мы строили бассейн, нам срочно потребовалось нарастить высоту забора для соблюдения норм. Highline Fencing сделали все оперативно и помогли пройти сертификацию без проблем.",
            "Мы в восторге от нового забора! Он выглядит просто фантастически и кардинально преобразил фасад нашего дома.",
            "Андрей из Highline Fencing проделал отличную, солидную работу. Коммуникация была прозрачной, смета точной, а работа выполнена точно в срок.",
            "Андрей отлично починил наш сломанный забор Colorbond строго в оговоренные сроки и по очень разумной цене. Рекомендую!",
            "Highline fencing (Андрей Петушков) — проверенная и честная компания. Мы очень довольны новым забором, Андрей был невероятно вежлив и профессионален."
        ]
    },
    "DIY Dale": {
        "lead_name": "Dale and Allen",
        "lead_name_ru": "Дейл и Аллен",
        "specialty_en": "Woodland Grey Slat Systems, Pool & Leaning Fence Alignment",
        "specialty_ru": "Ламельные системы Woodland Grey, ограждения бассейнов и выравнивание заборов",
        "services": [
            {
                "title_en": "Modern Slat Privacy Systems",
                "title_ru": "Ламельные заборы Woodland Grey",
                "badge_en": "Modern Look",
                "badge_ru": "Хит сезона",
                "desc_en": "Sleek horizontal slat fencing in Woodland Grey and Monument. Provides 80% privacy with airflow, perfect for suburban front yards.",
                "desc_ru": "Стильные горизонтальные ламели в цветах Woodland Grey и Monument. Обеспечивают приватность при свободной циркуляции воздуха.",
                "features_en": ["Powder coated durability", "Custom slat gap spacing", "Ideal for front courtyards"],
                "features_ru": ["Стойкая порошковая окраска", "Регулируемый зазор ламелей", "Идеально для палисадников"]
            },
            {
                "title_en": "Leaning Fence Straightening & Realignment",
                "title_ru": "Выравнивание и укрепление покосившихся заборов",
                "badge_en": "Restoration",
                "badge_ru": "Ремонт и спасение",
                "desc_en": "Don't spend thousands on a full rebuild if your posts can be reinforced. We reset shifting footings and install steel bracing.",
                "desc_ru": "Не переплачивайте за полную замену, если забор можно выровнять. Укрепляем фундаменты стоек и монтируем стальные усилители.",
                "features_en": ["Save on rebuild costs", "Post reinforcement", "Concrete anchor reset"],
                "features_ru": ["Экономия на замене", "Усиление стоек сталью", "Перезаливка анкерных оснований"]
            },
            {
                "title_en": "Black Chainwire & Boundary Fencing",
                "title_ru": "Черная сетка Chainwire и заборы Colorbond",
                "badge_en": "Durable & Practical",
                "badge_ru": "Практичность",
                "desc_en": "Heavy duty galvanized and PVC coated black chainwire for large boundaries, dog enclosures, and tennis courts.",
                "desc_ru": "Оцинкованная и покрытая черным ПВХ сетка-рабица для больших периметров, вольеров для собак и спортивных зон.",
                "features_en": ["PVC coated black wire", "Galvanized steel pipe frame", "Cost-effective perimeter"],
                "features_ru": ["Черная стойкая оплетка", "Оцинкованный трубный каркас", "Выгодная цена за метр"]
            }
        ],
        "reviews_ru": [
            "Очень доволен новым забором, который Дейл установил у нас дома. Дизайн из ламелей цвета Woodland Grey выглядит аккуратно и очень современно.",
            "Горячо рекомендую Дейла: он заменил ограждение вокруг нашего бассейна великолепным новым забором, который моментально прошел инспекцию на соответствие нормам.",
            "Недавно обратились в DIY Dale, чтобы исправить забор, который начал заваливаться на одну сторону. Результат идеальный — стоит мертво!",
            "Дейл и его отец Аллен проделали фантастическую работу по установке сетчатого забора chain wire. Для них не было ничего невозможного, работали с душой."
        ]
    },
    "STRAIGHT ARROW PROJECTS": {
        "lead_name": "Tim",
        "lead_name_ru": "Тим",
        "specialty_en": "Retaining Walls with Integrated Colorbond® Fencing",
        "specialty_ru": "Подпорные стенки с интегрированными заборами Colorbond®",
        "services": [
            {
                "title_en": "Integrated Retaining Wall & Fencing",
                "title_ru": "Подпорные стены с интегрированным забором",
                "badge_en": "All-in-One",
                "badge_ru": "Комплекс под ключ",
                "desc_en": "No need for two separate contractors. We engineer concrete sleeper retaining walls and anchor heavy Colorbond fences directly on top.",
                "desc_ru": "Вам не нужно нанимать двух разных подрядчиков. Мы возводим бетонные подпорные стены и монтируем забор Colorbond прямо в стальные двутавры.",
                "features_en": ["Engineered steel I-beams", "Concrete sleeper walling", "Seamless boundary finish"],
                "features_ru": ["Стальные двутавровые балки", "Бетонные армированные плиты", "Единая гарантия на конструкцию"]
            },
            {
                "title_en": "Colorbond® Residential Perimeter Fencing",
                "title_ru": "Капитальные заборы Colorbond®",
                "badge_en": "Arrow Straight",
                "badge_ru": "Идеальная геометрия",
                "desc_en": "Laser-calibrated boundary lines with deep concrete footings. Built from genuine BlueScope steel with matching post caps and trims.",
                "desc_ru": "Идеально прямая линия забора по лазерному нивелиру. Глубокая заливка бетоном, оригинальная австралийская сталь BlueScope.",
                "features_en": ["Laser levelled alignment", "Heavy duty C-posts", "BlueScope 10-year warranty"],
                "features_ru": ["Лазерная юстировка линии", "Усиленные стойки C-профиля", "Заводская гарантия BlueScope"]
            },
            {
                "title_en": "Heavy-Duty Gates & Landscape Prep",
                "title_ru": "Усиленные ворота и подготовка участка",
                "badge_en": "Turnkey",
                "badge_ru": "Полная подготовка",
                "desc_en": "Site clearing, earthmoving, boundary grading, and custom welded double gates built to withstand daily use without sagging.",
                "desc_ru": "Расчистка границы, планировка грунта мини-экскаватором и сварные ворота с диагональным усилением от провисания.",
                "features_en": ["Site excavation included", "Anti-sag gate frame", "Drop bolts & keyed latches"],
                "features_ru": ["Земляные работы под ключ", "Жесткая рама против провисания", "Качественные засовы и замки"]
            }
        ],
        "reviews_ru": [
            "Недавно обратился в Straight Arrow Projects для комплексной замены старой подпорной стенки и ограждения бассейна. Тим выполнил работу феноменально!",
            "Тим просто великолепен! Он сделал для нашего нового дома весь комплекс: забор, подпорную стенку и ландшафтные работы. Соседи постоянно спрашивают контакты.",
            "Тим и его бригада проделали невероятную работу, решив серьезнейшую проблему с дренажом и перепадом грунта на нашем участке. Очень рекомендую!",
            "Недавно нанял Straight Arrow Projects для установки забора Colorbond. Четкая коммуникация, приехали минута в минуту, сделали быстрее графика.",
            "Мы недавно заказали забор Colourbond и калитки у Straight Arrow. Все сделано на высшем уровне, прочно, ровно и красиво."
        ]
    },
    "Mighty Fencing": {
        "lead_name": "Ota",
        "lead_name_ru": "Ота",
        "specialty_en": "Fast Turnaround Residential Colorbond® & Acoustic Walls",
        "specialty_ru": "Быстрый монтаж заборов Colorbond® и акустических стен",
        "services": [
            {
                "title_en": "Rapid Turnaround Colorbond®",
                "title_ru": "Срочный монтаж заборов Colorbond®",
                "badge_en": "Fast Install",
                "badge_ru": "Монтаж за 48ч",
                "desc_en": "From quote to completion in record time. Fully stocked with popular Monument and Woodland Grey profiles for immediate dispatch.",
                "desc_ru": "От замера до готового забора за считанные дни. Постоянный складской запас популярных профилей в цветах Monument и Woodland Grey.",
                "features_en": ["In-stock BlueScope steel", "Same-week installation", "Transparent upfront quote"],
                "features_ru": ["Профиль в наличии на складе", "Установка на той же неделе", "Фиксированная честная цена"]
            },
            {
                "title_en": "Modular Acoustic Walls",
                "title_ru": "Акустические модульные ограждения",
                "badge_en": "Peace & Quiet",
                "badge_ru": "Тишина во дворе",
                "desc_en": "Dense composite acoustic panels designed to shield outdoor living areas from suburban and road noise.",
                "desc_ru": "Плотные сэндвич-панели для надежной защиты зоны отдыха и террасы от шума проезжей части и соседей.",
                "features_en": ["High sound transmission loss", "Sleek contemporary look", "Thermal insulation"],
                "features_ru": ["Эффективное поглощение шума", "Современный минималистичный дизайн", "Долговечные материалы"]
            },
            {
                "title_en": "Matching Pedestrian & Driveway Gates",
                "title_ru": "Калитки и въездные ворота в тон забора",
                "badge_en": "Secure Fit",
                "badge_ru": "Надежный замок",
                "desc_en": "Solid welded steel frames clad with matching Colorbond sheets. Durable stainless steel hardware and smooth ball-bearing hinges.",
                "desc_ru": "Цельносварные стальные рамы с обшивкой в тон основного забора. Нержавеющая фурнитура и надежные петли на подшипниках.",
                "features_en": ["Ball-bearing hinges", "Stainless hardware", "Zero wobble fit"],
                "features_ru": ["Петли на подшипниках", "Нержавеющий крепеж", "Плавный ход без скрипа"]
            }
        ],
        "reviews_ru": [
            "Горячо рекомендую! Весь процесс от первого замера до установки прошел абсолютно гладко. Команда работала слаженно и профессионально.",
            "Мы получили отличный опыт сотрудничества с Отой и его командой из Mighty Fencing. Забор поставили за один день, идеальное качество!",
            "Тим и Ота помогли оперативно решить проблему со штормовым повреждением забора. Сделали аккуратно, быстро и по отличной цене."
        ]
    },
    "TJ Fencing": {
        "lead_name": "Travis (TJ)",
        "lead_name_ru": "Трэвис (TJ)",
        "specialty_en": "Laser-Straight Posts in Tough & Rocky Ground",
        "specialty_ru": "Идеально прямые заборы в сложном каменистом грунте",
        "services": [
            {
                "title_en": "Hard Ground & Rocky Soil Colorbond®",
                "title_ru": "Монтаж Colorbond® в скальном и тяжелом грунте",
                "badge_en": "Heavy Excavation",
                "badge_ru": "Мощная техника",
                "desc_en": "Rocky clay or tree roots? We use heavy hydraulic augers to bore deep 600mm+ holes for rock-solid stability in any terrain.",
                "desc_ru": "Каменистая глина или мощные корни? Используем мощные гидравлические буры для бурения на глубину 600+ мм под фундаменты стоек.",
                "features_en": ["Hydraulic hole boring", "Extra deep footings", "Guaranteed plumb posts"],
                "features_ru": ["Механизированное бурение", "Увеличенная глубина бетонирования", "Гарантированная вертикаль"]
            },
            {
                "title_en": "Standard & High Privacy Boundary",
                "title_ru": "Приватные заборы высотой 1.8м и 2.1м",
                "badge_en": "100% Privacy",
                "badge_ru": "Полный комфорт",
                "desc_en": "Complete perimeter protection with interlocking Colorbond panels that never rot, peel, or warp in the Australian sun.",
                "desc_ru": "Качественная замковая система панелей Colorbond. Защита от солнца и коррозии без деформации и рассыхания.",
                "features_en": ["Genuine BlueScope steel", "Termite and fire proof", "Clean modern finish"],
                "features_ru": ["Сталь BlueScope", "Не боится термитов и огня", "Современный строгий вид"]
            },
            {
                "title_en": "Custom Steel Frame Gates",
                "title_ru": "Ворота на жестком стальном каркасе",
                "badge_en": "Heavy Duty",
                "badge_ru": "Усиленный профиль",
                "desc_en": "Tough 50x50mm steel box section frames that never warp or sag, even under heavy daily use.",
                "desc_ru": "Каркас из профильной трубы 50х50 мм, сваренный с диагональными распорками — никаких перекосов со временем.",
                "features_en": ["50x50mm box section", "Diagonal bracing", "Heavy duty D-latch"],
                "features_ru": ["Труба 50х50 мм", "Диагональное усиление", "Удобная двусторонняя защелка"]
            }
        ],
        "reviews_ru": [
            "Без колебаний рекомендую услуги TJ Fencing. Трэвис и его команда работают быстро, пунктуально и на высочайшем профессиональном уровне.",
            "Очень довольна работой, которую Трэвис проделал с моим забором Colorbond. Цена была весьма разумной, забор выглядит потрясающе!"
        ]
    },
    "Armstrong Fencing and Landscaping": {
        "lead_name": "Armstrong Team",
        "lead_name_ru": "Команда Armstrong",
        "specialty_en": "Concrete Sleeper Retaining Walls & Hybrid Fencing",
        "specialty_ru": "Подпорные стены из бетонных плит и комбинированные заборы",
        "services": [
            {
                "title_en": "Concrete Sleeper Retaining & Fencing",
                "title_ru": "Подпорные стенки из плит с установкой забора",
                "badge_en": "Lifetime Strength",
                "badge_ru": "На века",
                "desc_en": "Reinforced concrete sleepers slotted into galvanised steel uprights with fence posts integrated directly into the steel H-beams.",
                "desc_ru": "Армированные бетонные плиты в стальных оцинкованных стойках с креплением забора прямо в тело подпорной стены.",
                "features_en": ["Galvanised steel H-beams", "Engineered structural stability", "Full soil retention"],
                "features_ru": ["Оцинкованные H-балки", "Расчет несущей способности", "Удержание любых масс грунта"]
            },
            {
                "title_en": "Colorbond® & Timber Hybrid Boundaries",
                "title_ru": "Заборы Colorbond® и комбинированные решения",
                "badge_en": "Modern & Classic",
                "badge_ru": "Популярный выбор",
                "desc_en": "The best of both worlds: modern zero-maintenance Colorbond steel panels combined with treated hardwood plinths and posts.",
                "desc_ru": "Идеальное сочетание: не требующие ухода стальные листы Colorbond с обработанными деревянными цокольными плитами.",
                "features_en": ["Treated timber plinths", "Keep pets & soil contained", "Clean level fence line"],
                "features_ru": ["Нижняя цокольная доска plinth", "Защита от подкопа собаками", "Ровный уровень без щелей"]
            },
            {
                "title_en": "Boundary Landscaping & Clean Finish",
                "title_ru": "Благоустройство границы и полная уборка",
                "badge_en": "Complete Care",
                "badge_ru": "Чистая работа",
                "desc_en": "Complete garden bed preparation, soil levelling, and debris carting so your property is showroom ready upon completion.",
                "desc_ru": "Подсыпка грунта, планировка клумб вдоль забора и полный вывоз строительного мусора после завершения работ.",
                "features_en": ["Garden bed reshaping", "Complete debris disposal", "Spotless property handover"],
                "features_ru": ["Формирование посадочной полосы", "Полная утилизация мусора", "Идеальный порядок на участке"]
            }
        ],
        "reviews_ru": [
            "Команда Armstrong сделала феноменальную работу с подпорной стенкой и забором. Участок был со сложным уклоном, но они справились безупречно.",
            "Отличная организация работ: привезли материалы, за 2 дня залили фундаменты и смонтировали забор. Очень доволен результатом!",
            "Ребята настоящие трудяги. Работали аккуратно, сохранили все посадки в саду и поставили забор точно по меже."
        ]
    },
    "JP Fencing & More Pty Ltd": {
        "lead_name": "JP",
        "lead_name_ru": "Джей Пи",
        "specialty_en": "22 Colorbond® Designer Colours & Motorised Sliding Gates",
        "specialty_ru": "22 дизайнерских цвета Colorbond® и автоматические откатные ворота",
        "services": [
            {
                "title_en": "Full Colorbond® Colour Range",
                "title_ru": "Все 22 цвета палитры Colorbond®",
                "badge_en": "Full Palette",
                "badge_ru": "Оригинал BlueScope",
                "desc_en": "Choose from genuine BlueScope shades including Monument, Basalt, Dover White, and Shale Grey with exact matching caps and rails.",
                "desc_ru": "Все оригинальные цвета BlueScope: Monument, Basalt, Dover White, Shale Grey и другие с точным попаданием в тон кровли и фасада.",
                "features_en": ["22 authentic colours", "Matching capping & rails", "Heat-reflective technology"],
                "features_ru": ["22 фирменных оттенка", "Планки и заглушки в цвет", "Технология отражения тепла"]
            },
            {
                "title_en": "Motorised Sliding & Driveway Gates",
                "title_ru": "Откатные ворота с мощным электроприводом",
                "badge_en": "Automated",
                "badge_ru": "Комфорт и статус",
                "desc_en": "Smooth running cantilever and track sliding gates with heavy-duty gear racks, safety sensors, and wireless keypads.",
                "desc_ru": "Плавные откатные ворота по направляющему рельсу. Зубчатая рейка из стали, датчики безопасности и беспроводные пульты.",
                "features_en": ["High torque electric motor", "Infrared obstacle sensors", "Keypad & smartphone access"],
                "features_ru": ["Мощный итальянский мотор", "Инфракрасные датчики препятствий", "Пульт и кодовая панель"]
            },
            {
                "title_en": "Horizontal Slat Privacy Screens",
                "title_ru": "Горизонтальные алюминиевые ламели",
                "badge_en": "Airflow & Privacy",
                "badge_ru": "Стиль и вентиляция",
                "desc_en": "Aluminium slat panels for carports, front fences, and air conditioner screening. Never rusts and never needs painting.",
                "desc_ru": "Алюминиевые экраны для навесов, фасадных заборов и маскировки блоков кондиционеров. Не ржавеет и не требует окраски.",
                "features_en": ["Marine-grade aluminium", "Custom gap spacing", "Sleek contemporary look"],
                "features_ru": ["Анодированный алюминий", "Регулируемый зазор", "Современный минимализм"]
            }
        ],
        "reviews_ru": [
            "JP проделал великолепную работу с нашим новым забором Colorbond и автоматическими воротами. Все работает плавно и тихо, цвет Monument идеально подошел к дому.",
            "Очень рекомендую JP Fencing! Быстрый выезд на замер, четкая смета без сюрпризов и высочайшее качество монтажа.",
            "Отличная работа, парни за 3 дня огородили весь участок более 60 метров. Все швы и стыки идеальные."
        ]
    },
    "JD Fence Masters": {
        "lead_name": "JD",
        "lead_name_ru": "Джей Ди",
        "specialty_en": "Stepped Colorbond® on Slopes & Under-Fence Plinths",
        "specialty_ru": "Ступенчатый монтаж Colorbond® на склонах и цокольные плиты",
        "services": [
            {
                "title_en": "Stepped Slope Fencing",
                "title_ru": "Ступенчатый монтаж на участках с уклоном",
                "badge_en": "Slope Experts",
                "badge_ru": "Сложный рельеф",
                "desc_en": "Custom stepped panel heights to maintain consistent privacy without leaving awkward gaps beneath the bottom rail.",
                "desc_ru": "Точный расчет ступеней забора для сохранения приватности без провисаний и некрасивых зазоров снизу.",
                "features_en": ["No bottom gaps", "Uniform stepped heights", "Reinforced downhill posts"],
                "features_ru": ["Никаких щелей снизу", "Одинаковая высота ступеней", "Усиленные нижние столбы"]
            },
            {
                "title_en": "Concrete & Steel Under-Fence Plinths",
                "title_ru": "Цокольные подпорные плиты под забор",
                "badge_en": "Retaining Power",
                "badge_ru": "Защита от подкопа",
                "desc_en": "Heavy duty concrete plinths that retain up to 300mm of garden soil and stop dogs from digging under the fence.",
                "desc_ru": "Прочные цокольные плиты, выдерживающие подпор грунта до 300 мм и исключающие подкопы домашними питомцами.",
                "features_en": ["Retains garden soil", "Dog proof boundary", "Locks into fence posts"],
                "features_ru": ["Удерживает почву клумб", "Защита от подкопа собаками", "Надежный паз в стойках"]
            },
            {
                "title_en": "Matching Pedestrian Access Gates",
                "title_ru": "Калитки из профильной трубы с замком",
                "badge_en": "Lockable",
                "badge_ru": "Безопасность",
                "desc_en": "Welded steel frames with internal drop bolts, stainless steel hinges, and deadbolt security latches.",
                "desc_ru": "Сварные рамы с надежными петлями, защитой от взлома и врезными замками под ключ.",
                "features_en": ["Welded steel box frame", "Deadbolt security", "Smooth closing"],
                "features_ru": ["Прочный коробчатый профиль", "Надежный врезной замок", "Легкое закрывание"]
            }
        ],
        "reviews_ru": [
            "JD — настоящий мастер своего дела! У нас сложный участок на склоне, но забор получился ровным как стрела, каждая ступень выверена идеально.",
            "Отличная работа по установке забора с цокольными плитами plinths. Собака теперь не может подкопать, а клумбы держат форму.",
            "Быстро, надежно и по очень приятной цене. Рекомендую JD Fence Masters всем соседям в Брисбене!"
        ]
    },
    "Bayside Fencing & Gates": {
        "lead_name": "Michael",
        "lead_name_ru": "Майкл",
        "specialty_en": "Heavy-Duty Electric Gates & Coastal Rust-Proof Fencing",
        "specialty_ru": "Мощные автоматические ворота и коррозионностойкие прибрежные заборы",
        "services": [
            {
                "title_en": "Heavy Duty Automated Security Gates",
                "title_ru": "Автоматические въездные ворота высокой безопасности",
                "badge_en": "High Security",
                "badge_ru": "Надежная автоматика",
                "desc_en": "Bespoke electric sliding and swing driveway gates engineered to protect your property with remote access control.",
                "desc_ru": "Индивидуальные откатные и распашные въездные ворота с итальянскими моторами, пультами ДУ и кодовой клавиатурой.",
                "features_en": ["Heavy duty motor gear", "Smartphone app control", "Keypad & intercom ready"],
                "features_ru": ["Мощный редукторный привод", "Управление через приложение", "Подключение домофона"]
            },
            {
                "title_en": "Coastal Rust-Resistant Colorbond®",
                "title_ru": "Прибрежный забор Colorbond® с защитой от соли",
                "badge_en": "Coastal Grade",
                "badge_ru": "Морской климат",
                "desc_en": "Specialized corrosion-resistant coatings specifically formulated for bayside environments exposed to sea air and high humidity.",
                "desc_ru": "Специальная сталь с улучшенным антикоррозийным цинк-алюминиевым покрытием для зон вблизи океана и залива.",
                "features_en": ["Salt air protection", "Bluescope Ultra grade", "Stainless steel screws"],
                "features_ru": ["Стойкость к морской соли", "Класс BlueScope Ultra", "Нержавеющие саморезы"]
            },
            {
                "title_en": "Privacy Slat Boundary Dividers",
                "title_ru": "Приватные секционные экраны",
                "badge_en": "Modern Vibe",
                "badge_ru": "Приватность",
                "desc_en": "Stylish privacy dividers to shield pools, entertaining decks, and side pathways from view.",
                "desc_ru": "Эстетичные экраны для защиты зоны бассейна, террасы для барбекю и боковых проходов от взглядов соседей.",
                "features_en": ["Custom height screens", "Airflow friendly", "Powder coated aluminium"],
                "features_ru": ["Высота до 2.4 метров", "Пропускает свежий бриз", "Порошковое покрытие"]
            }
        ],
        "reviews_ru": [
            "Майкл спроектировал и установил новые автоматические ворота безопасности на нашем участке. Мы невероятно довольны результатом — все работает как часы!",
            "Отличный сервис от Майкла! Наш прибрежный забор начал ржаветь от соленого воздуха, Майкл заменил его на специальный Colorbond Ultra. Выглядит великолепно.",
            "Профессионал высочайшего уровня. Ворота открываются абсолютно бесшумно, качественная автоматика и безупречный монтаж."
        ]
    },
    "Hernsley Fencing Services": {
        "lead_name": "Tony",
        "lead_name_ru": "Тони",
        "specialty_en": "Old Rotten Timber Removal & Acoustic Modular Noise Barriers",
        "specialty_ru": "Демонтаж старых деревянных заборов и шумозащитные модульные стены",
        "services": [
            {
                "title_en": "Rotten Timber Demolition & Colorbond® Upgrade",
                "title_ru": "Снос старых заборов и установка Colorbond®",
                "badge_en": "Full Removal",
                "badge_ru": "Вывоз мусора",
                "desc_en": "We take down hazardous, rotting timber fences, pull out old timber stumps, and install pristine new Colorbond fencing.",
                "desc_ru": "Аккуратно валим аварийные гнилые деревянные заборы, корчуем старые пни стоек и монтируем ровный долговечный Colorbond.",
                "features_en": ["Old fence stump removal", "Green waste disposal", "Clean property boundary"],
                "features_ru": ["Удаление старых столбов", "Полная утилизация отходов", "Чистая ровная граница"]
            },
            {
                "title_en": "Acoustic Noise Dampening Walls",
                "title_ru": "Шумоизоляционные акустические стены",
                "badge_en": "Quiet Living",
                "badge_ru": "Акустический комфорт",
                "desc_en": "Block loud traffic, train, or neighbour noise with high-density acoustic modular panels. Beautiful rendered stone look.",
                "desc_ru": "Подавление шума оживленных дорог и железных дорог с помощью плотных звукопоглощающих сэндвич-панелей.",
                "features_en": ["Heavy acoustic core", "Rendered finish options", "Dramatically cut noise"],
                "features_ru": ["Плотное шумопоглощающее ядро", "Фактурная отделка под камень", "Снижение шума в 4 раза"]
            },
            {
                "title_en": "Powder Coated Aluminium Gates",
                "title_ru": "Алюминиевые калитки с порошковой покраской",
                "badge_en": "Rust Free",
                "badge_ru": "Не ржавеет",
                "desc_en": "Lightweight, rigid aluminium side gates with key-lockable D-latches that never rust or need oiling.",
                "desc_ru": "Легкие и жесткие боковые калитки с надежными замками, которые не заклинивают и не ржавеют со временем.",
                "features_en": ["Lightweight & rigid", "No rust ever", "Keyed deadlock"],
                "features_ru": ["Жесткость без лишнего веса", "Никакой коррозии", "Замок с комплектом ключей"]
            }
        ],
        "reviews_ru": [
            "Тони — один из лучших мастеров, к которым я когда-либо обращался! Он быстро заменил наш разваливающийся деревянный забор на шикарный Colorbond.",
            "Тони и его бригада выполнили для нас несколько проектов по ограждению. Они просто великолепны: быстро, суперэффективно и предельно аккуратно!",
            "Очень благодарен Тони за работу. Старый забор вывезли под чистую, новый поставили за день, ни одной соринки во дворе не оставили."
        ]
    },
    "Sentry Fencing": {
        "lead_name": "Matt",
        "lead_name_ru": "Мэтт",
        "specialty_en": "Storm Damage Emergency Replacements & Horizontal Slat Screens",
        "specialty_ru": "Срочная замена после штормов и горизонтальные ламели",
        "services": [
            {
                "title_en": "Storm Damage Emergency Boundary Replacement",
                "title_ru": "Срочная замена забора после штормов",
                "badge_en": "Storm Ready",
                "badge_ru": "Срочный выезд",
                "desc_en": "Did recent storms blow your fence down? Matt provides priority emergency quotes for insurance and rebuilds up to 40m+ boundaries fast.",
                "desc_ru": "Шторм повалил забор? Мэтт оперативно подготовит смету для страховой компании и восстановит до 40+ метров забора в кратчайшие сроки.",
                "features_en": ["Insurance quotes provided", "Extra deep footings", "Reinforced wind posts"],
                "features_ru": ["Официальные сметы для страховых", "Углубленные фундаменты", "Усиленные ветровые стойки"]
            },
            {
                "title_en": "Horizontal Aluminium Slat Screens",
                "title_ru": "Горизонтальные алюминиевые ламели",
                "badge_en": "Modern Privacy",
                "badge_ru": "Современный стиль",
                "desc_en": "Sleek architectural privacy screens for front elevations, bin storage, and pool borders with custom spacing.",
                "desc_ru": "Стильные горизонтальные ламели для парадного фасада, зоны мусорных баков и бассейна с любым шагом зазора.",
                "features_en": ["Architectural slat look", "Durable powder coat", "Zero rot or termite risk"],
                "features_ru": ["Премиальный фасадный вид", "Стойкое порошковое покрытие", "Не боится влаги и насекомых"]
            },
            {
                "title_en": "Full Colorbond® Boundary Fencing",
                "title_ru": "Капитальные межевые заборы Colorbond®",
                "badge_en": "Perimeter Guard",
                "badge_ru": "Полная защита",
                "desc_en": "Tough BlueScope steel panels with interlocking seams that block prying eyes and protect your backyard.",
                "desc_ru": "Надежные стальные листы с замковым соединением внахлест, защищающие двор от посторонних взглядов и ветра.",
                "features_en": ["Genuine BlueScope steel", "10-year warranty", "Laser straight lines"],
                "features_ru": ["Сталь BlueScope с маркировкой", "10 лет заводской гарантии", "Лазерный уровень по всей длине"]
            }
        ],
        "reviews_ru": [
            "Мэтт из Sentry Fencing выполнил фантастическую работу по установке горизонтального ламельного забора. Очень довольны качеством!",
            "В октябре Мэтт заменил наш старый 33-метровый деревянный забор на великолепный Colorbond. Все сделано быстро, ровно и профессионально.",
            "Наш задний забор повалило недавним ураганом. Мэтт моментально нашел окно в графике, приехал и восстановил границу участка в идеальном виде.",
            "Быстро, профессионально и доступно! Мэтт заменил весь периметр, убрал за собой весь мусор. Отличный парень и первоклассный мастер."
        ]
    },
    "BLC FENCING": {
        "lead_name": "Team BLC",
        "lead_name_ru": "Команда BLC",
        "specialty_en": "Safe Asbestos Fence Removal & Shared Boundary 50/50 Splits",
        "specialty_ru": "Безопасный демонтаж асбестовых заборов и межевые заборы на двоих с соседом",
        "services": [
            {
                "title_en": "Licensed Asbestos Fence Removal & Disposal",
                "title_ru": "Лицензированный демонтаж асбестовых заборов",
                "badge_en": "EPA Compliant",
                "badge_ru": "Безопасный снос",
                "desc_en": "Old broken fibro or asbestos fence? We handle licensed, EPA-compliant removal and transport with zero health hazard to your family.",
                "desc_ru": "Старый асбестоцементный забор треснул? Проводим сертифицированный демонтаж с увлажнением, упаковкой и утилизацией по нормам безопасности.",
                "features_en": ["EPA-approved disposal", "Hazard-free family safety", "Council clearance paperwork"],
                "features_ru": ["Сертифицированный вывоз", "Полная безопасность семьи", "Официальные акты утилизации"]
            },
            {
                "title_en": "Shared Neighbor Dividing Fences (50/50 Billing)",
                "title_ru": "Межевые заборы с раздельным счетом 50/50",
                "badge_en": "Neighbor Friendly",
                "badge_ru": "Счет 50/50",
                "desc_en": "We make dividing fence projects easy by providing split invoicing directly to both neighbours, avoiding awkward money conversations.",
                "desc_ru": "Делаем замену межевого забора комфортной: выставляем раздельные официальные счета каждому из соседей по 50%.",
                "features_en": ["Split 50/50 neighbor quotes", "Both sides color matched", "Full conflict-free resolution"],
                "features_ru": ["Раздельные счета для соседей", "Одинаково красивый вид с двух сторон", "Без конфликтов и споров"]
            },
            {
                "title_en": "WA Certified Pool Compliance Fencing",
                "title_ru": "Ограждения для бассейнов по стандартам WA",
                "badge_en": "Council Approved",
                "badge_ru": "Нормы WA",
                "desc_en": "Aluminium tube and glass pool fencing fully certified to Western Australia council barrier standards with self-latching gates.",
                "desc_ru": "Ограждения бассейнов из алюминия и стекла, строго соответствующие стандартам безопасности Западной Австралии.",
                "features_en": ["Self-latching safety gates", "Council pass guarantee", "Corrosion proof"],
                "features_ru": ["Самозащелкивающиеся замки", "Гарантия сдачи инспектору", "Стойкость к химии бассейна"]
            }
        ],
        "reviews_ru": [
            "Фантастический сервис! Наш старый асбестовый забор упал во время сильного шторма. BLC быстро приехали на замер и оперативно смонтировали новый забор.",
            "Огромное спасибо команде BLC! Отличный сервис, забор Colourbond выглядит просто потрясающе. Быстро, аккуратно и очень качественно.",
            "Мы нанимали BLC Fencing для замены межевого забора между нами и соседями. От первой сметы до сдачи объекта — все на 5 звезд!"
        ]
    },
    "Fenced Right WA": {
        "lead_name": "Lucas",
        "lead_name_ru": "Лукас",
        "specialty_en": "Heavy-Duty Post Installation & High-Wind Engineering",
        "specialty_ru": "Усиленные столбы и расчет на повышенные ветровые нагрузки",
        "services": [
            {
                "title_en": "High-Wind Engineered Colorbond®",
                "title_ru": "Штормостойкие заборы Colorbond® с усилением",
                "badge_en": "Wind Proof",
                "badge_ru": "Ветроустойчивость",
                "desc_en": "Built specifically for WA coastal gusts. Reinforced gauge posts set deep in quick-set 25MPa concrete to ensure zero wobbling.",
                "desc_ru": "Специальная сборка под прибрежные порывистые ветры. Усиленные стойки и высокомарочный бетон 25 МПа — никакой болтанки.",
                "features_en": ["25MPa high strength concrete", "Deep post embedment", "Storm gust rated"],
                "features_ru": ["Высокомарочный бетон 25 МПа", "Глубокая посадка стоек", "Расчет на шквалистые порывы"]
            },
            {
                "title_en": "Double Access Driveway & Side Gates",
                "title_ru": "Двойные въездные ворота и калитки",
                "badge_en": "Heavy Frame",
                "badge_ru": "Сварная рама",
                "desc_en": "Rigid welded steel box frames with drop bolts, heavy duty pad-bolt latches, and smooth swing clearance for boat or caravan access.",
                "desc_ru": "Жесткие сварные рамы из профильной трубы для заезда катеров, трейлеров и внедорожников. Мощные запоры и легкий ход.",
                "features_en": ["Wide caravan access", "Anti-sag bracing", "Keyed lock compatibility"],
                "features_ru": ["Широкий проем для авто", "Диагональное усиление", "Замки с защитой от взлома"]
            },
            {
                "title_en": "Transparent Communication & Daily Updates",
                "title_ru": "Прозрачность и отчеты на каждом этапе",
                "badge_en": "No Surprises",
                "badge_ru": "Без сюрпризов",
                "desc_en": "Lucas keeps you updated at every step: from arrival time to material delivery and final walkthrough.",
                "desc_ru": "Лукас лично держит связь на каждом этапе: от точного времени доставки материалов до финальной совместной приемки.",
                "features_en": ["Direct tradie phone contact", "Fixed price quote", "Clean property signoff"],
                "features_ru": ["Прямой контакт с мастером", "Фиксированная цена без доплат", "Сдача участка в чистоте"]
            }
        ],
        "reviews_ru": [
            "Не могу нахвалиться Fenced Right: профессионально, точно в срок и с отличной коммуникацией. Безусловно, лучший опыт работы со строителями в WA!",
            "С Лукасом было невероятно приятно работать, он держал меня в курсе каждого этапа проекта. Очень аккуратный и честный мастер.",
            "Обратился по рекомендации друга. Лукас приехал ровно в назначенное время, подробно все объяснил и сделал забор на высшем уровне.",
            "С удовольствием рекомендую Fenced Right WA! Мне нужно было срочно заменить секцию забора — Лукас откликнулся моментально и все исправил."
        ]
    },
    "Fencing Rockingham": {
        "lead_name": "Jimmy and Alex",
        "lead_name_ru": "Джимми и Алекс",
        "specialty_en": "Fast Turnaround Competitive Colorbond & Aftercare Support",
        "specialty_ru": "Конкурентные цены на Colorbond, быстрый монтаж и гарантийное обслуживание",
        "services": [
            {
                "title_en": "Rockingham Boundary Colorbond®",
                "title_ru": "Заборы Colorbond® по лучшей цене в Рокингеме",
                "badge_en": "Best Value",
                "badge_ru": "Выгодная цена",
                "desc_en": "High quality BlueScope Colorbond fencing at direct contractor rates. Straightforward quoting with zero hidden callout fees.",
                "desc_ru": "Качественная сталь BlueScope Colorbond по прямым ценам мастеров без посредников и накруток. Честная смета за погонный метр.",
                "features_en": ["Direct tradie pricing", "Fast measure & quote", "Genuine BlueScope panels"],
                "features_ru": ["Честная цена от мастеров", "Бесплатный оперативный замер", "Оригинальные панели BlueScope"]
            },
            {
                "title_en": "Heavy Duty Steel Post Driveway Gates",
                "title_ru": "Въездные ворота на усиленных стальных столбах",
                "badge_en": "Solid Post",
                "badge_ru": "Мощные столбы",
                "desc_en": "Custom fabricated gates hung on 75x75mm or 100x100mm heavy steel posts that never lean or drag on the driveway.",
                "desc_ru": "Ворота на мощных столбах 75х75 мм или 100х100 мм, которые никогда не провисают и не цепляют плитку въезда.",
                "features_en": ["Heavy 75mm/100mm posts", "Welded square frames", "Heavy duty barrel hinges"],
                "features_ru": ["Столбы 75-100 мм", "Сварной профиль", "Мощные гаражные петли"]
            },
            {
                "title_en": "Attentive Aftercare & Warranty Service",
                "title_ru": "Внимательный сервис и гарантийная поддержка",
                "badge_en": "100% Care",
                "badge_ru": "Гарантия качества",
                "desc_en": "Jimmy stands behind every single job. If you ever need an adjustment or hinge tweak, we are there same day.",
                "desc_ru": "Джимми лично отвечает за каждый установленный забор. Если потребуется регулировка замка или петли — приезжаем без лишних слов.",
                "features_en": ["Same day aftercare", "Workmanship guarantee", "Local Rockingham crew"],
                "features_ru": ["Оперативный выезд", "Гарантия на все узлы", "Местная бригада мастеров"]
            }
        ],
        "reviews_ru": [
            "Джимми был великолепен от начала и до конца! Очень оперативная и конкурентная смета, приехали точно в назначенное время, сделали идеально.",
            "Чрезвычайно доволен и впечатлен работой Джимми и его команды по установке ворот! Отличная цена и великолепное качество сборки.",
            "Джимми и Алекс проделали выдающуюся работу по установке нашего забора. Работали без перекуров, были вежливы и профессиональны.",
            "Заборы от Джимми — это настоящее качество. А их постгарантийное обслуживание — просто топ-уровень. Приезжают по первому зову!"
        ]
    },
    "Hanson Fencing & Gate": {
        "lead_name": "Peter",
        "lead_name_ru": "Питер",
        "specialty_en": "Custom Side Gates, Slat Infill Panels & Full Boundaries",
        "specialty_ru": "Индивидуальные боковые калитки, ламельные вставки и заборы",
        "services": [
            {
                "title_en": "Custom Side Gates & Slat Infill Panels",
                "title_ru": "Боковые калитки и секционные ламели",
                "badge_en": "Custom Craft",
                "badge_ru": "Точный размер",
                "desc_en": "Custom measured and welded side gates with horizontal slat inserts. Powder coated to blend seamlessly with your brickwork or render.",
                "desc_ru": "Точное изготовление калиток под ваш проем с горизонтальными ламелями. Порошковая окраска в тон кирпича или штукатурки дома.",
                "features_en": ["Precision opening fit", "Key lockable security", "Powder coated finish"],
                "features_ru": ["Подгонка точно в размер", "Врезной замок с ключами", "Стойкая порошковая краска"]
            },
            {
                "title_en": "High Privacy Colorbond® Boundaries",
                "title_ru": "Заборы Colorbond® максимальной приватности",
                "badge_en": "Complete Privacy",
                "badge_ru": "Полная тишина",
                "desc_en": "Up to 2.1m high fencing built to keep suburban neighbours out of view and contain family pets safely inside.",
                "desc_ru": "Заборы высотой до 2.1 метра для полной изоляции двора от посторонних и безопасного выгула домашних питомцев.",
                "features_en": ["2.1m height options", "Interlocking sheets", "BlueScope steel warranty"],
                "features_ru": ["Высота до 2.1 метра", "Плотный нахлест листов", "Заводская гарантия BlueScope"]
            },
            {
                "title_en": "Sloped Ground Stepped Installation",
                "title_ru": "Монтаж на участках с перепадом высот",
                "badge_en": "Stepped Fit",
                "badge_ru": "Без перекосов",
                "desc_en": "Custom stepped heights with matching bottom plinths so your boundary fence follows natural property contours without gaps.",
                "desc_ru": "Аккуратная ступенька по уровню с установкой нижних доборных планок, закрывающих щели на уклонах.",
                "features_en": ["Ground contour hugging", "Bottom plinth sealing", "Clean aesthetic steps"],
                "features_ru": ["Повторение рельефа участка", "Устранение нижних щелей", "Эстетичные ровные уступы"]
            }
        ],
        "reviews_ru": [
            "Горячо рекомендую Hanson Fencing! Цены были очень разумными, а итоговым качеством забора и калитки я доволен на все 100%.",
            "С самого начала Питер очень детально и грамотно составил смету на нашу боковую калитку и секционные панели. Бригада приехала и сделала все быстро и четко.",
            "Я очень тщательно выбирал подрядчика для замены нашего забора. Питер предложил лучшие условия, отличное качество материалов и сделал все на совесть."
        ]
    },
    "Valente Fencing": {
        "lead_name": "Peter and Luke (Valente Brothers)",
        "lead_name_ru": "Питер и Люк (братья Валенте)",
        "specialty_en": "Brother-Built Precision Fencing, Gate Repairs & Spotless Cleanup",
        "specialty_ru": "Семейное качество от братьев Валенте: заборы, ворота и идеальная чистота",
        "services": [
            {
                "title_en": "Precision Brother-Built Colorbond®",
                "title_ru": "Капитальные заборы Colorbond® от братьев Валенте",
                "badge_en": "Family Owned",
                "badge_ru": "Семейное качество",
                "desc_en": "No sub-contractors. Peter and Luke handle your job personally from the initial measure to the final screw.",
                "desc_ru": "Никаких наемных субподрядчиков. Питер и Люк лично делают ваш забор от первого замера до последнего самореза.",
                "features_en": ["Owners on site every day", "Laser level precision", "BlueScope guaranteed"],
                "features_ru": ["Мастера лично на объекте", "Лазерный нивелир на каждом метре", "Оригинальная сталь BlueScope"]
            },
            {
                "title_en": "Gate Repairs, Rehangs & Alignments",
                "title_ru": "Ремонт, перевешивание и регулировка ворот",
                "badge_en": "Expert Fix",
                "badge_ru": "Срочный ремонт",
                "desc_en": "Sticking gates, dragging latches, or shifted posts? We re-weld, re-hinge, and reset gate posts so they swing effortlessly.",
                "desc_ru": "Заедает калитка, задевают створки или повело столб? Перевариваем, меняем петли и выравниваем рамы для легкого открывания одним пальцем.",
                "features_en": ["Fix dragging gates", "Heavy duty bearing hinges", "Padlock and latch reset"],
                "features_ru": ["Устранение провисаний", "Петли на подшипниках", "Надежная регулировка замков"]
            },
            {
                "title_en": "Spotless Yard Cleanup Guarantee",
                "title_ru": "Гарантия идеальной чистоты на участке",
                "badge_en": "Clean Finish",
                "badge_ru": "Чистый двор",
                "desc_en": "We respect your home. All metal shavings, concrete rubble, and old fence pieces are loaded into our trucks and removed.",
                "desc_ru": "Уважение к вашему дому: вся металлическая стружка собирается магнитом, бетонные сколы и обрезки вывозятся под чистую.",
                "features_en": ["Magnetic metal cleanup", "Rubble hauled away", "Garden beds respected"],
                "features_ru": ["Магнитная уборка стружки", "Полный вывоз строительного лома", "Бережное отношение к газону"]
            }
        ],
        "reviews_ru": [
            "У меня была небольшая задача — починить калитку, которая провисла. Братья Валенте откликнулись моментально, приехали и сделали все на совесть!",
            "Горячо рекомендую Valente Fencing! Питер работал совершенно автономно, не отвлекая нас, все сделали идеально и убрали за собой каждую соринку.",
            "Мы невероятно счастливы с нашим новым забором от Valente Fencing. Питер и Люк — исключительные профессионалы и очень приятные люди.",
            "Не могу нахвалиться Питером и Люком! Они проделали потрясающую работу по установке забора и ворот, все точно по уровню.",
            "С Valente Fencing было фантастически приятно иметь дело от первого звонка до финальной приемки. Рекомендую всем в Аделаиде!"
        ]
    },
    "Guardian fencing": {
        "lead_name": "Shane",
        "lead_name_ru": "Шейн",
        "specialty_en": "3-Sided Property Perimeter Colorbond, Black Chainwire & Double Gates",
        "specialty_ru": "Ограждение участков с 3 сторон, черная сетка chainwire и двойные ворота",
        "services": [
            {
                "title_en": "Full 3-Sided Property Perimeter Colorbond®",
                "title_ru": "Комплексное ограждение участка с трех сторон",
                "badge_en": "Perimeter Pack",
                "badge_ru": "Комплекс 3 стороны",
                "desc_en": "Complete turnkey perimeter replacement for entire properties. Laser-straight boundary lines, sturdy corner bracing, and BlueScope steel.",
                "desc_ru": "Полная замена периметра участка под ключ по трем границам. Мощные угловые столбы, усиленные перемычки и сталь BlueScope.",
                "features_en": ["Complete property perimeter", "Heavy duty corner posts", "Coordinated neighbour approvals"],
                "features_ru": ["Полный охват всех 3 сторон", "Усиленные угловые столбы", "Помощь в согласовании с соседями"]
            },
            {
                "title_en": "Black Chainwire & Boundary Security",
                "title_ru": "Черная сетка Chainwire для фасадов и границ",
                "badge_en": "Durable & Open",
                "badge_ru": "Практичность",
                "desc_en": "Sleek black PVC coated chainwire fencing. Durable, corrosion-proof, and unobtrusive border solution for homes and acreages.",
                "desc_ru": "Черная сетка в защитной оболочке из ПВХ на стальном трубном каркасе. Идеально для палисадников, просторных участков и собак.",
                "features_en": ["Black PVC coated wire", "Galvanised pipe framework", "High visibility with security"],
                "features_ru": ["Черное защитное ПВХ покрытие", "Оцинкованный каркас", "Обзорность и защита от проникновения"]
            },
            {
                "title_en": "Colourbond Aluminium Slat Double Gates",
                "title_ru": "Двойные ворота из ламелей Colourbond",
                "badge_en": "Double Gate",
                "badge_ru": "Широкий заезд",
                "desc_en": "Custom manufactured double swing gates designed for trailers, caravans, and backyard access with heavy duty drop pins.",
                "desc_ru": "Распашные двойные ворота для заезда прицепов, лодок и автодомов. Усиленные нижние фиксаторы и надежные замки.",
                "features_en": ["Wide vehicular access", "Dual drop bolts", "Matched to boundary fencing"],
                "features_ru": ["Широкий въезд для спецтехники", "Двойные стопорные штыри", "Идеальное совпадение по цвету"]
            }
        ],
        "reviews_ru": [
            "Огромное спасибо Шейну и его команде за ограждение нашего участка сразу с трех сторон! Шейн был надежен, держал слово и сделал все идеально.",
            "Я нанял Шейна поставить забор из черной сетки chain wire на фасаде нашего дома. Качество работы исключительное, забор преобразил вид дома!",
            "Шейн из Guardian Fencing заменил мои старые ворота на великолепные двойные ворота из алюминиевых ламелей Colourbond. Очень доволен результатом!",
            "Шейн сделал потрясающий забор для нас в апреле. Пунктуальный, честный, материалы высочайшего качества. Однозначно 5 звезд!",
            "Горячо рекомендую Шейна из Guardian Fencing для любых задач по заборам. Надежный, дружелюбный и преданный своему делу мастер."
        ]
    }
}

print("Contractor profiles mapped successfully for all 20 companies!")
