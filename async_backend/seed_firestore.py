"""
Seed Firestore with initial region data for Indian states, union territories,
cities, and special zones, plus sample live updates.

Usage:
    python seed_firestore.py

Collection names are read from config.py — nothing is hardcoded.
Idempotent: re-running overwrites with the same data.
"""

import sys
from datetime import datetime, timedelta, timezone

from config import get_config


REGIONS = [
    # =========================================================================
    # STATES & UNION TERRITORIES
    # =========================================================================
    {
        "id": "delhi",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Secular cosmopolitan culture blending Mughal and modern heritage",
            "Street food capital — paratha, chaat, kebab traditions in Old Delhi",
            "Mughal architectural heritage — Red Fort, Jama Masjid, Humayun's Tomb",
        ],
        "legal_rules": [
            "Alcohol legal with license (drinking age 25)",
            "Odd-even traffic rule may apply during pollution season",
            "Firecrackers banned during Diwali (green crackers only)",
        ],
        "behavioral_notes": [
            "Queue culture is weak — expect crowds",
            "Bargaining expected in markets like Sarojini and Chandni Chowk",
            "Auto-rickshaw drivers may not use meters — negotiate fare upfront",
        ],
    },
    {
        "id": "karnataka",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Kannada",
        "cultural_markers": [
            "Temple etiquette important — dress conservatively",
            "Silk saree and sandalwood tradition",
            "Mysore Dasara is a major festival",
        ],
        "legal_rules": [
            "Alcohol regulated: dry days enforced on national holidays and elections",
            "Plastic ban in effect — carry cloth bags",
            "Cow slaughter banned",
        ],
        "behavioral_notes": [
            "Remove footwear at temples and many homes",
            "Respectful dress expected at religious sites",
            "Kannada signage dominant — English less common outside Bangalore",
        ],
    },
    {
        "id": "maharashtra",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Marathi",
        "cultural_markers": [
            "Ganesh Chaturthi is the biggest festival",
            "Warkari pilgrimage tradition to Pandharpur",
            "Lavani and Tamasha folk art traditions",
        ],
        "legal_rules": [
            "Beef ban enforced — possession and sale prohibited",
            "Alcohol: permit system in some areas, legal drinking age 25",
            "Noise restrictions after 10 PM strictly enforced in residential areas",
        ],
        "behavioral_notes": [
            "Use right hand for giving and receiving",
            "Shoes off in homes — always",
            "Local train etiquette: do not block doors, women's compartments reserved",
        ],
    },
    {
        "id": "tamil_nadu",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Tamil",
        "cultural_markers": [
            "Dravidian cultural pride — strong regional identity",
            "Pongal is the biggest festival (January harvest)",
            "Classical Bharatanatyam dance tradition",
            "Temple towns with strict religious customs",
        ],
        "legal_rules": [
            "TASMAC state-run liquor shops only — no private liquor stores",
            "Jallikattu (bull-taming) legally permitted during Pongal",
            "Anti-conversion laws in effect",
        ],
        "behavioral_notes": [
            "Tamil language preference very strong — Hindi may not be understood or welcomed",
            "Remove footwear at all temples without exception",
            "Vegetarian food widely available — non-veg restaurants are clearly marked",
        ],
    },
    {
        "id": "telangana",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Telugu",
        "cultural_markers": [
            "Bathukamma flower festival unique to Telangana",
            "Biryani culture — Hyderabadi dum biryani is a state icon",
            "Kakatiya dynasty heritage — Warangal Fort, Thousand Pillar Temple",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 21",
            "Cow slaughter banned under Telangana Animal Preservation Act",
            "Plastic carry bags below 50 microns banned statewide",
        ],
        "behavioral_notes": [
            "Telugu and Urdu both widely spoken — bilingual culture",
            "Elders addressed with respectful suffixes like 'garu'",
            "Hospitality is strong — refusing offered food/tea can be seen as rude",
        ],
    },
    {
        "id": "west_bengal",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Bengali",
        "cultural_markers": [
            "Durga Puja is the grandest cultural event — pandal-hopping tradition",
            "Rabindranath Tagore's literary and musical legacy pervasive",
            "Sweets culture — rosogolla, sandesh, mishti doi are iconic",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 21",
            "Cow slaughter legal in West Bengal unlike most Indian states",
            "Noise pollution rules enforced during immersion processions",
        ],
        "behavioral_notes": [
            "Addressing elders as 'dada' (brother) or 'didi' (sister) is common and respectful",
            "Intellectual and literary discussions valued — 'adda' (informal chat) culture",
            "Fish and rice are dietary staples — vegetarian options exist but non-veg is the norm",
        ],
    },
    {
        "id": "gujarat",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Gujarati",
        "cultural_markers": [
            "Navratri celebrated with massive Garba and Dandiya Raas gatherings",
            "Predominantly vegetarian food culture — dhokla, thepla, fafda, jalebi",
            "Textile heritage — Patola silk sarees from Patan, bandhani tie-dye",
        ],
        "legal_rules": [
            "Gujarat is a dry state — alcohol sale and consumption prohibited without permit",
            "Foreign tourists and visitors can obtain a temporary liquor permit",
            "Cow slaughter punishable with life imprisonment under Gujarat Animal Preservation Act",
        ],
        "behavioral_notes": [
            "Vegetarianism is the norm — many families are strictly vegetarian",
            "Business and trading culture deeply embedded — Gujaratis are known for entrepreneurship",
            "Guests are treated with great hospitality — 'Atithi Devo Bhava' (guest is God) taken seriously",
        ],
    },
    {
        "id": "rajasthan",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Royal Rajput heritage — forts, palaces, and havelis across the state",
            "Vibrant textile traditions — block printing from Jaipur, tie-dye bandhani",
            "Desert culture — camel fairs, folk music (Manganiar and Langa musicians)",
        ],
        "legal_rules": [
            "Alcohol legal but heavily taxed; drinking age 25",
            "Some areas near temples and religious sites are dry zones",
            "Cow slaughter banned — strict enforcement",
        ],
        "behavioral_notes": [
            "Greeting with 'Khamma Ghani' or 'Padharo Mhare Desh' (welcome) is traditional",
            "Conservative dress norms in rural areas — women often wear ghunghat (veil)",
            "Hospitality is deeply valued — guests offered water and chai immediately",
        ],
    },
    {
        "id": "uttar_pradesh",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Spiritual heartland — Varanasi, Ayodhya, Mathura, Allahabad (Prayagraj)",
            "Awadhi cuisine tradition — kebabs, biryanis, and Lucknowi culinary heritage",
            "Mughal architectural legacy — Taj Mahal, Fatehpur Sikri, Agra Fort",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 25",
            "Cow slaughter strictly banned — UP Prevention of Cow Slaughter Act",
            "Anti-conversion ordinance (UP Freedom of Religion Act) in effect",
        ],
        "behavioral_notes": [
            "Touching feet of elders (pranam/charan sparsh) is customary and expected",
            "Religious sensitivity high — respect for both Hindu and Muslim traditions",
            "Hindi is the sole working language — English not widely spoken outside cities",
        ],
    },
    {
        "id": "punjab",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Punjabi",
        "cultural_markers": [
            "Sikh Gurdwara culture — langar (community kitchen) open to all",
            "Bhangra and Giddha folk dance traditions",
            "Rich agricultural identity — wheat fields, Baisakhi harvest festival",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 25",
            "Cow slaughter banned under Punjab Prohibition of Cow Slaughter Act",
            "Stubble burning regulations enforced seasonally (often violated)",
        ],
        "behavioral_notes": [
            "Warmth and hospitality are hallmarks — 'Sat Sri Akal' is the common greeting",
            "Generous food culture — refusing food is considered impolite",
            "Head covering required when entering any Gurdwara",
        ],
    },
    {
        "id": "haryana",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Haryanvi folk traditions — Saang (folk theatre) and Ragini music",
            "Strong wrestling and sports culture — Haryana produces many Olympic athletes",
            "Agricultural heartland — Baisakhi and Teej are major festivals",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 25",
            "Cow slaughter banned — Haryana Gauvansh Sanrakshan and Gausamvardhan Act strict enforcement",
            "Khap panchayat (village council) influence exists in rural areas despite legal limits",
        ],
        "behavioral_notes": [
            "Conservative social norms especially in rural areas",
            "Respect for elders is paramount — 'Tau' (uncle) used as respectful address for older men",
            "Dairy-heavy diet — milk, lassi, ghee, and curd are staples",
        ],
    },
    {
        "id": "kerala",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Malayalam",
        "cultural_markers": [
            "Onam festival with Pookalam (flower carpet), Vallam Kali (boat races), and Onasadya feast",
            "Kathakali classical dance-drama and Kalaripayattu martial art traditions",
            "Backwater houseboat culture in Alleppey (Alappuzha) and Kumarakom",
        ],
        "legal_rules": [
            "Alcohol heavily restricted — only 5-star hotels and government-run Bevco outlets sell liquor",
            "Hartals (strikes/shutdowns) called by political parties can disrupt transport unexpectedly",
            "Plastic ban enforced — single-use plastics prohibited",
        ],
        "behavioral_notes": [
            "High literacy rate — English widely understood alongside Malayalam",
            "Religious harmony notable — Hindu, Muslim, and Christian communities coexist closely",
            "Tipping not traditionally expected but appreciated at restaurants",
        ],
    },
    {
        "id": "goa",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Konkani",
        "cultural_markers": [
            "Portuguese colonial heritage — churches, Latin Quarter in Fontainhas, Goan-Portuguese cuisine",
            "Beach and shack culture — Calangute, Baga, Anjuna, Palolem beaches",
            "Carnival tradition in February — street parades, floats, and King Momo festivities",
        ],
        "legal_rules": [
            "Alcohol is cheap and widely available — drinking age 18 (lowest in India)",
            "Casinos are legal — floating casinos on the Mandovi River in Panaji",
            "Uniform Civil Code applies in Goa — unique among Indian states",
        ],
        "behavioral_notes": [
            "Relaxed 'susegad' (laid-back) lifestyle is the defining cultural attitude",
            "Siesta culture — many shops close between 1 PM and 4 PM",
            "Respect for the environment expected on beaches — littering fines enforced",
        ],
    },
    {
        "id": "madhya_pradesh",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Heart of India — UNESCO sites including Sanchi Stupa, Bhimbetka rock shelters, Khajuraho temples",
            "Tribal culture significant — Gond, Bhil, and Baiga communities with distinct art and music",
            "Wildlife sanctuaries — Kanha, Bandhavgarh, Pench national parks for tiger safaris",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 21",
            "Cow slaughter banned — Madhya Pradesh Gau Vansh Pratishedh Adhiniyam",
            "Anti-conversion law (MP Freedom of Religion Act) in effect",
        ],
        "behavioral_notes": [
            "Conservative and traditional social norms in smaller towns",
            "Hindi spoken with distinctive Malwi, Bundeli, or Nimadi regional accents",
            "Food culture is strongly vegetarian in many regions, especially among Jain and Hindu communities",
        ],
    },
    {
        "id": "odisha",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Odia",
        "cultural_markers": [
            "Jagannath Puri temple and the annual Rath Yatra (chariot festival) are central to identity",
            "Odissi classical dance tradition — one of India's eight classical dance forms",
            "Konark Sun Temple — UNESCO World Heritage Site with iconic stone chariot architecture",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 21",
            "Cow slaughter banned under Odisha Prevention of Cow Slaughter Act",
            "Single-use plastic banned in all urban areas",
        ],
        "behavioral_notes": [
            "Odia people known for gentle, polite demeanor",
            "Rice is the absolute staple — meals without rice feel incomplete",
            "Temple towns like Puri have strict vegetarian zones near the Jagannath temple",
        ],
    },
    {
        "id": "assam",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Assamese",
        "cultural_markers": [
            "Bihu festival (Rongali, Kongali, Bhogali) with traditional Bihu dance and music",
            "Tea garden culture — Assam produces over half of India's tea",
            "One-horned rhinoceros habitat — Kaziranga National Park is a UNESCO World Heritage Site",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 21",
            "Cattle slaughter banned under Assam Cattle Preservation Act 2021",
            "Inner Line Permit not required for Assam but needed for neighboring NE states",
        ],
        "behavioral_notes": [
            "Offering gamosa (traditional woven towel) is the highest mark of respect and welcome",
            "Tea is offered in every household — refusing is impolite",
            "Assamese people value simplicity and understatement — boasting is frowned upon",
        ],
    },
    {
        "id": "himachal_pradesh",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Himalayan hill station culture — British colonial-era architecture in Shimla and Dalhousie",
            "Kullu Dussehra festival — week-long celebration unique to the Kullu Valley",
            "Pahari (hill) culture — traditional wooden temple architecture, Himachali cap (topi) is cultural identity",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 25",
            "Plastic bags banned across the state — strictly enforced at tourist spots",
            "No construction allowed within certain distances of forests and rivers",
        ],
        "behavioral_notes": [
            "Hill people are warm but reserved — greet with 'Namaste' and folded hands",
            "Roads are narrow and winding — honking is a safety norm, not aggression",
            "Local pahadi food (siddu, dham) offered warmly to visitors — accept graciously",
        ],
    },
    {
        "id": "uttarakhand",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Devbhoomi (Land of Gods) — Char Dham pilgrimage (Badrinath, Kedarnath, Gangotri, Yamunotri)",
            "Yoga and spiritual capital of the world — Rishikesh and Haridwar on the Ganges",
            "Garhwali and Kumaoni folk culture — distinct hill traditions, music, and cuisine",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 25",
            "Non-vegetarian food and alcohol prohibited in holy towns like Haridwar and Rishikesh",
            "Char Dham Yatra registration mandatory — biometric ID required for pilgrims",
        ],
        "behavioral_notes": [
            "Spiritual sensibility is strong — respect for religious sites is essential",
            "Adventure tourism norms — follow guide instructions for rafting, trekking",
            "Mountain etiquette: do not litter on trekking trails — 'Leave No Trace' enforced",
        ],
    },
    {
        "id": "jammu_and_kashmir",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Kashmiri",
        "cultural_markers": [
            "Mughal gardens of Srinagar — Shalimar Bagh, Nishat Bagh, Chashme Shahi",
            "Pashmina shawl weaving tradition — centuries-old artisan craft",
            "Wazwan feast tradition — multi-course Kashmiri banquet with rogan josh, gushtaba, yakhni",
        ],
        "legal_rules": [
            "Section 144 (prohibitory orders) can be imposed at short notice in sensitive areas",
            "Photography restricted near military installations and certain border areas",
            "Alcohol available in licensed hotels and shops but not widely consumed socially",
        ],
        "behavioral_notes": [
            "Kashmiris greet with 'Aadab' or 'As-Salaam-Alaikum' — reciprocate respectfully",
            "Hospitality through kehwa (Kashmiri saffron tea) and noon chai (pink salt tea) is customary",
            "Political discussions are sensitive — avoid unsolicited opinions on the political situation",
        ],
    },
    {
        "id": "ladakh",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Ladakhi",
        "cultural_markers": [
            "Tibetan Buddhist monastery culture — Hemis, Thiksey, Diskit monasteries",
            "Ladakh Festival in September and Hemis Festival (masked dances) are major events",
            "Stark high-altitude desert landscape — Pangong Lake, Nubra Valley, Khardung La pass",
        ],
        "legal_rules": [
            "Inner Line Permit (ILP) required for certain areas — Nubra Valley, Pangong, Hanle",
            "Restricted Area Permit needed for foreign nationals in some zones",
            "Environmental regulations strict — no littering, camping only in designated areas",
        ],
        "behavioral_notes": [
            "'Julley' is the universal greeting — means hello, thank you, and goodbye",
            "Altitude sickness is real — acclimatize for 24-48 hours in Leh before trekking",
            "Buddhist prayer flags and mani walls should always be passed from the left (clockwise)",
        ],
    },
    {
        "id": "sikkim",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Nepali",
        "cultural_markers": [
            "Buddhist monastery culture — Rumtek, Pemayangtse, Enchey monasteries",
            "Kanchenjunga (third highest peak) dominates the landscape and spiritual identity",
            "Organic state — Sikkim became India's first fully organic state in 2016",
        ],
        "legal_rules": [
            "Inner Line Permit required for Nathula Pass and restricted border areas",
            "Restricted Area Permit needed for foreign nationals visiting certain areas",
            "Plastic water bottles banned in certain protected areas — carry reusable bottles",
        ],
        "behavioral_notes": [
            "Nepali is the lingua franca — also Bhutia, Lepcha, and Limbu spoken",
            "People are gentle and soft-spoken — aggression and loud behavior are culturally jarring",
            "Alcohol (local tongba and chang) widely consumed — but respect monastery zones",
        ],
    },
    {
        "id": "meghalaya",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Khasi",
        "cultural_markers": [
            "Matrilineal society — children take the mother's surname, youngest daughter inherits property",
            "Living root bridges of Cherrapunji (Sohra) — UNESCO tentative list, centuries-old Khasi engineering",
            "Wettest place on Earth — Mawsynram and Cherrapunji receive extreme rainfall",
        ],
        "legal_rules": [
            "Inner Line Permit not required for Indian citizens but check advisories",
            "Restricted Area Permit needed for foreign nationals in certain border areas",
            "Autonomous District Councils govern tribal areas with customary laws",
        ],
        "behavioral_notes": [
            "Khasi, Jaintia, and Garo tribes have distinct customs — learn which area you are in",
            "Christianity is the majority religion — church on Sundays is important, shops may be closed",
            "Betel nut (kwai) chewing is ubiquitous — offered as a sign of welcome",
        ],
    },
    {
        "id": "andhra_pradesh",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Telugu",
        "cultural_markers": [
            "Tirupati Balaji (Tirumala Venkateswara Temple) — richest and most visited Hindu temple in the world",
            "Kuchipudi classical dance tradition originated here",
            "Spicy Andhra cuisine — known for heavy use of red chilies, gunpowder (podi), and pickles",
        ],
        "legal_rules": [
            "Alcohol regulated — government pushing towards prohibition in phases",
            "Cow slaughter banned under AP Prohibition of Cow Slaughter Act",
            "Tirupati temple has strict dress code and conduct rules enforced by TTD (Tirumala Tirupati Devasthanams)",
        ],
        "behavioral_notes": [
            "Respectful suffix 'garu' used when addressing anyone — essential social etiquette",
            "Meals traditionally eaten on banana leaves during festivals and special occasions",
            "Telugu pride strong — the language was recently conferred classical language status",
        ],
    },
    {
        "id": "bihar",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Buddhist heritage — Bodh Gaya (where Buddha attained enlightenment), Nalanda ancient university ruins",
            "Chhath Puja — ancient Vedic festival dedicated to the Sun God, unique to Bihar and eastern UP",
            "Madhubani (Mithila) painting tradition — intricate folk art recognized globally",
        ],
        "legal_rules": [
            "Bihar is a dry state since 2016 — complete prohibition of alcohol, strict penalties",
            "Cow slaughter banned",
            "Caste-based discrimination laws strictly on the books though social hierarchies persist",
        ],
        "behavioral_notes": [
            "Touching feet of elders is standard practice and a sign of deep respect",
            "Bihari hospitality is generous — sattu, litti-chokha offered warmly to guests",
            "Hindi and Bhojpuri/Magahi/Maithili spoken — Maithili has its own literary tradition",
        ],
    },
    {
        "id": "jharkhand",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Tribal heritage — Santhal, Munda, Oraon, Ho tribes with rich folk traditions",
            "Sarhul festival — spring celebration of Sal trees sacred to tribal communities",
            "Mineral-rich state — known as India's mining hub (coal, iron ore, mica)",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 21",
            "Cow slaughter banned under Jharkhand Bovine Animal Prohibition of Slaughter Act",
            "Tribal land transfer restrictions — non-tribals cannot buy tribal land (Chotanagpur Tenancy Act)",
        ],
        "behavioral_notes": [
            "Tribal customs respected — festivals like Karma and Sarhul have community participation",
            "Rice-based diet predominant — rice beer (handia) is traditional in tribal areas",
            "People are hospitable but reserved — earn trust through respectful engagement",
        ],
    },
    {
        "id": "chhattisgarh",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Tribal diversity — Bastar Dussehra is a 75-day tribal festival unlike mainstream Dussehra",
            "Dhokra (bell metal) casting artisan tradition — ancient lost-wax technique",
            "Rich folk dance traditions — Panthi, Raut Nacha, Sua Naach",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 21",
            "Cow slaughter banned under Chhattisgarh Agricultural Cattle Preservation Act",
            "Some areas in Bastar region may have restricted access due to security advisories",
        ],
        "behavioral_notes": [
            "Chhattisgarhi (dialect of Hindi) is the daily language — Hindi understood everywhere",
            "Tribal areas have distinct social protocols — take local guidance before visiting",
            "Rice and lentils are staple — 'bore baasi' (fermented rice) is a traditional breakfast",
        ],
    },

    # =========================================================================
    # CITIES
    # =========================================================================

    # --- 1. Mumbai (Maharashtra) ---
    {
        "id": "mumbai",
        "type": "city",
        "parent_region": "maharashtra",
        "dominant_language": "Marathi",
        "cultural_markers": [
            "Dabba (tiffin) delivery culture — Mumbai's dabbawalas deliver 200,000+ lunches daily with Six Sigma accuracy",
            "Bollywood film industry capital — Film City in Goregaon, studios across Andheri",
            "Marine Drive (Queen's Necklace) and Gateway of India are iconic waterfront landmarks",
            "Vada pav is the city's street food identity — found at virtually every street corner",
        ],
        "legal_rules": [
            "No-honking zones enforced in parts of South Mumbai — fines for violations",
            "Plastic bags banned citywide — fines up to Rs 25,000 for repeated violations",
            "BMC enforces strict building code — unauthorized constructions face demolition",
        ],
        "behavioral_notes": [
            "Local trains are the lifeline — learn the etiquette: do not block doors, women's compartments strictly reserved",
            "Rush hour trains are extremely crowded (8-10 AM, 6-8 PM) — avoid luggage during peak",
            "Street food (vada pav, pav bhaji, bhel puri) is iconic — Mumbaikars eat on the go",
        ],
    },

    # --- 2. Delhi / New Delhi ---
    {
        "id": "new_delhi",
        "type": "city",
        "parent_region": "delhi",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "India Gate, Rashtrapati Bhavan, and Parliament House form the ceremonial capital axis designed by Lutyens",
            "Chandni Chowk — one of India's oldest markets, dating to Mughal emperor Shah Jahan's era",
            "Paranthe Wali Gali in Old Delhi — legendary lane of stuffed paratha shops operating since the 1870s",
            "Qutub Minar, Humayun's Tomb, and Lotus Temple represent centuries of architectural heritage",
        ],
        "legal_rules": [
            "Odd-even vehicle rationing scheme activated during severe pollution episodes — fines for violation",
            "Delhi Metro has strict no-eating, no-drinking rules — fines enforced",
            "Green crackers only during Diwali — traditional firecrackers banned by Supreme Court order",
        ],
        "behavioral_notes": [
            "Bargaining is expected and essential in markets — fixed price only in malls",
            "Auto-rickshaw and taxi drivers may refuse meters — use app-based cabs or negotiate upfront",
            "Delhi belly is real — acclimatize with bottled water and street food gradually",
        ],
    },

    # --- 3. Bangalore / Bengaluru ---
    {
        "id": "bangalore",
        "type": "city",
        "parent_region": "karnataka",
        "dominant_language": "Kannada",
        "cultural_markers": [
            "IT hub — India's Silicon Valley with campuses of Infosys, Wipro, and hundreds of startups in Koramangala, HSR Layout, and Whitefield; Electronic City is the original IT corridor",
            "Pub and craft beer scene — Toit, Arbor Brewing, Windmills Craftworks, and microbreweries on 12th Main Indiranagar; Bangalore introduced India to the craft beer revolution",
            "Garden city — Lalbagh Botanical Garden (established 1760 by Hyder Ali) hosts biannual flower shows; Cubbon Park is the green lung of the CBD",
            "Masala dosa institutions — Vidyarthi Bhavan (est. 1943, Basavanagudi), MTR (est. 1924, Lalbagh), and CTR (Central Tiffin Room, Malleshwaram) are culinary pilgrimages",
            "Weekend getaway culture — Skandagiri night trek, Nandi Hills sunrise, Coorg coffee plantations, and Mysuru palace are popular 1-2 day escapes from the city",
        ],
        "legal_rules": [
            "Pubs and bars must close by 11:30 PM (1 AM on weekends in designated entertainment zones like MG Road, Brigade Road, Indiranagar)",
            "Vehicle emission checks enforced at random by transport department — PUC certificate mandatory; fines for expired certificates",
            "BBMP enforces strict no-plastic rules — single-use plastic bags banned; carry cloth bags when shopping; vendors fined for distributing plastic bags",
            "BMTC buses and Namma Metro have no-eating rules — fines for violations on metro; Purple Line (Baiyappanahalli-Mysuru Road) and Green Line (Nagasandra-Silk Institute) operational",
            "Noise restrictions after 10 PM in residential areas — BBMP and police enforce limits especially around Koramangala, Indiranagar, and JP Nagar; pubs face license action for violations",
        ],
        "behavioral_notes": [
            "English widely spoken in tech corridors — but learning basic Kannada ('Swalpa adjust maadi' = please adjust a little, 'Guru' = respectful term for driver/shopkeeper) earns genuine goodwill",
            "Traffic is notoriously bad — Silk Board junction, ORR, and Marathahalli are daily bottlenecks; plan extra 30-60 minutes during peak hours (8:30-10:30 AM, 5:30-8:30 PM); Namma Metro is the fastest option where available",
            "Auto-rickshaw meters are mandatory but often ignored — insist on meter or use Ola/Uber/Rapido; meter fare starts at Rs 30; auto drivers often refuse short-distance trips",
            "Bangalore weather is its biggest draw — pleasant 18-28°C most of the year; October-November brings heavy rains; carry an umbrella from June to November",
            "Key areas to know — MG Road and Brigade Road for nightlife; Koramangala and Indiranagar for dining and cafes; Jayanagar and Basavanagudi for old Bangalore charm; Whitefield and Electronic City for IT campuses; Malleshwaram and Rajajinagar for traditional shopping",
        ],
    },

    # --- 4. Hyderabad (Telangana) ---
    {
        "id": "hyderabad",
        "type": "city",
        "parent_region": "telangana",
        "dominant_language": "Telugu",
        "cultural_markers": [
            "Charminar and surrounding Laad Bazaar — iconic 1591 monument and bangle-shopping market",
            "Hyderabadi dum biryani — slow-cooked rice and meat dish, city's most famous culinary export (Paradise, Bawarchi, Shah Ghouse)",
            "HITEC City and Gachibowli form the IT corridor — major tech hub rivaling Bangalore",
            "Golconda Fort — 13th-century fort famous for its acoustic architecture and diamond mining history",
        ],
        "legal_rules": [
            "GHMC enforces encroachment removal drives — street vendors face periodic displacement",
            "Traffic police use AI-based e-challan system — red light and helmet violations auto-detected",
            "Noise regulations enforced around the Hussain Sagar lake area and heritage zones",
        ],
        "behavioral_notes": [
            "Urdu and Telugu both spoken widely — the city has a unique Deccani Urdu dialect called Hyderabadi Hindi",
            "Biryani is serious business — locals have strong opinions about which restaurant is best",
            "Irani chai (served in Irani cafes like Nimrah, Cafe Bahar) is a daily ritual — pair with Osmania biscuits",
        ],
    },

    # --- 5. Chennai (Tamil Nadu) ---
    {
        "id": "chennai",
        "type": "city",
        "parent_region": "tamil_nadu",
        "dominant_language": "Tamil",
        "cultural_markers": [
            "Marina Beach — second longest urban beach in the world, evening promenade tradition",
            "December Music and Dance Season (Margazhi) — six-week Carnatic music and Bharatanatyam festival, largest cultural event in South Asia",
            "Kapaleeshwarar Temple in Mylapore — 7th-century Dravidian temple central to city identity",
            "Filter coffee culture — 'degree coffee' served in steel davara-tumbler set is iconic",
        ],
        "legal_rules": [
            "TASMAC shops only for alcohol — bars exist but liquor stores are all state-run",
            "Chennai Traffic Police enforce helmet rules strictly — two-wheelers fined on the spot",
            "Beach sand removal and beach construction strictly prohibited — CRZ (Coastal Regulation Zone) enforced",
        ],
        "behavioral_notes": [
            "Tamil pride is very strong — Hindi is often not spoken and not always welcome; English is the preferred second language",
            "Idli, dosa, sambar, and filter coffee are breakfast non-negotiables — the city runs on them",
            "Conservative dress norms at temples — Kapaleeshwarar and Parthasarathy temples enforce strict dress codes",
        ],
    },

    # --- 6. Kolkata (West Bengal) ---
    {
        "id": "kolkata",
        "type": "city",
        "parent_region": "west_bengal",
        "dominant_language": "Bengali",
        "cultural_markers": [
            "Durga Puja — UNESCO Intangible Cultural Heritage, thousands of artistic pandals across the city for five days in October",
            "Howrah Bridge (Rabindra Setu) and Victoria Memorial are iconic landmarks",
            "Literary and intellectual capital — College Street book market, Presidency University, Coffee House adda tradition",
            "Rosogolla, mishti doi, kosha mangsho (slow-cooked mutton), and Kolkata biryani (with egg and potato) define the food scene",
        ],
        "legal_rules": [
            "Hand-pulled rickshaws still exist in limited areas — subject to ongoing regulation and phase-out attempts",
            "Kolkata Police enforce noise limits during Durga Puja immersion processions (Supreme Court guidelines)",
            "No-vehicle zones in parts of central Kolkata during festivals — Park Street and Esplanade restricted",
        ],
        "behavioral_notes": [
            "'Dada' (elder brother) is the universal respectful address for men; 'Didi' for women",
            "Adda (informal intellectual conversation over tea) is a cherished daily ritual — not wasting time, it's culture",
            "Kolkatans are passionate about football (East Bengal vs Mohun Bagan rivalry), Rabindranath Tagore, and fish",
        ],
    },

    # --- 7. Pune (Maharashtra) ---
    {
        "id": "pune",
        "type": "city",
        "parent_region": "maharashtra",
        "dominant_language": "Marathi",
        "cultural_markers": [
            "Oxford of the East — Savitribai Phule Pune University, Fergusson College, and Deccan College are academic landmarks",
            "Shaniwar Wada — 18th-century Peshwa fort-palace in the city center, symbol of Maratha heritage",
            "Osho International Meditation Resort in Koregaon Park attracts global seekers",
            "Misal pav, vada pav, and mastani (thick milkshake from Sujata Mastani) are signature foods",
        ],
        "legal_rules": [
            "Pune Traffic Police enforce no-honking zones in areas like FC Road and JM Road",
            "Noise restrictions after 10 PM strictly enforced — Pune residents frequently file noise complaints",
            "PMC (Pune Municipal Corporation) enforces strict waste segregation — wet and dry waste separation mandatory",
        ],
        "behavioral_notes": [
            "Pune has a strong Brahmin cultural influence — many traditional vegetarian eateries",
            "Cycling culture growing with dedicated lanes — locals proud of the city's relatively clean air",
            "IT parks (Hinjewadi, Kharadi) have transformed the city — mix of traditional Puneri and cosmopolitan tech culture",
        ],
    },

    # --- 8. Ahmedabad (Gujarat) ---
    {
        "id": "ahmedabad",
        "type": "city",
        "parent_region": "gujarat",
        "dominant_language": "Gujarati",
        "cultural_markers": [
            "Sabarmati Ashram — Mahatma Gandhi's headquarters during the independence movement",
            "UNESCO World Heritage City (2017) — first in India; old city's pols (traditional residential clusters) and carved wooden havelis",
            "Navratri Garba in Ahmedabad is the largest dance festival — GMDC ground hosts 10,000+ dancers nightly",
            "Manek Chowk transforms from jewelry market by day to street food heaven at night — famous for khaman, dabeli, and gola",
        ],
        "legal_rules": [
            "Dry city in a dry state — alcohol strictly prohibited unless you hold a valid liquor permit",
            "AMC (Ahmedabad Municipal Corporation) enforces building heritage conservation rules in the Walled City",
            "BRTS (Bus Rapid Transit System) lanes are dedicated — no private vehicles allowed in BRTS corridors",
        ],
        "behavioral_notes": [
            "Vegetarianism is the norm — the city is predominantly vegetarian; non-veg eateries exist but are distinctly separate",
            "Business culture is strong — Ahmedabadis are entrepreneurial; many family-run textile businesses",
            "Early riser city — morning chai stalls open by 5 AM, markets active by 7 AM",
        ],
    },

    # --- 9. Jaipur (Rajasthan) ---
    {
        "id": "jaipur",
        "type": "city",
        "parent_region": "rajasthan",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Pink City — buildings in the old city painted terracotta pink since 1876 for Prince Albert's visit",
            "Hawa Mahal (Palace of Winds), Amber Fort, City Palace, and Jantar Mantar (UNESCO) are landmark attractions",
            "Johari Bazaar and Bapu Bazaar for traditional Rajasthani jewelry, textiles, and block-printed fabrics",
            "Dal baati churma, ghewar (sweet), and pyaaz ki kachori are signature Jaipur dishes",
        ],
        "legal_rules": [
            "Heritage zone building restrictions — strict rules on construction height and facade alterations in the Walled City",
            "Elephant rides at Amber Fort regulated — animal welfare guidelines now enforced",
            "Alcohol available but some areas near temples are dry — carry permit if purchasing for hotel consumption",
        ],
        "behavioral_notes": [
            "Shopkeepers in tourist areas quote 3-5x the real price — bargaining is expected and necessary",
            "Conservative dress preferred especially in the old city — women should consider covering shoulders and knees",
            "Jaipur shuts down early — most markets close by 8-9 PM; nightlife is limited compared to metros",
        ],
    },

    # --- 10. Lucknow (Uttar Pradesh) ---
    {
        "id": "lucknow",
        "type": "city",
        "parent_region": "uttar_pradesh",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "City of Nawabs — Awadhi culture of tehzeeb (etiquette), adab (respect), and refinement",
            "Tunday Kababi (est. 1905) and Aminabad's kebab stalls define the world-famous Lucknowi kebab tradition — galouti, kakori, seekh",
            "Bara Imambara (1784) with its Bhool Bhulaiya (labyrinth) and Rumi Darwaza gateway are architectural marvels",
            "Chikankari hand-embroidery tradition — centuries-old white threadwork on fabric, a Lucknow specialty",
        ],
        "legal_rules": [
            "Alcohol legal but area-specific restrictions near religious sites in the old city",
            "LDA (Lucknow Development Authority) heritage conservation rules apply in Husainabad and Aminabad areas",
            "Traffic police enforce lane discipline on Hazratganj and Vidhan Sabha Marg — challans for violations",
        ],
        "behavioral_notes": [
            "Lucknowi tehzeeb (manners) is famous — 'Pehle aap' (after you) culture; politeness is deeply valued",
            "Food portions are generous — refusing extra helpings repeatedly is the polite norm before accepting",
            "Urdu-Hindi blend (Hindustani) is spoken with a distinctive Lucknowi accent and vocabulary",
        ],
    },

    # --- Chandigarh UT (parent region for the city) ---
    {
        "id": "chandigarh_ut",
        "type": "state",
        "parent_region": None,
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Le Corbusier's planned city — the only city in India designed by a world-renowned architect",
            "Shared capital of both Punjab and Haryana — unique administrative arrangement",
            "Sukhna Lake, Rock Garden, and the Capitol Complex define the city's identity",
        ],
        "legal_rules": [
            "Union Territory administered by central government — not governed by Punjab or Haryana",
            "Strict traffic challan system — one of the highest traffic fine enforcement rates in India",
            "Building heights capped in most sectors to preserve Le Corbusier's original urban plan",
        ],
        "behavioral_notes": [
            "Punjabi cultural influence dominant — Punjabi and Hindi spoken interchangeably",
            "One of India's highest per capita income cities — affluent, orderly, and well-maintained",
            "Residents are proud of the city's green cover and planned infrastructure",
        ],
    },

    # --- 11. Chandigarh (Punjab/Haryana) ---
    {
        "id": "chandigarh",
        "type": "city",
        "parent_region": "chandigarh_ut",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Le Corbusier's planned city — Capitol Complex (UNESCO World Heritage Site), Open Hand Monument, and sector-grid layout",
            "Rock Garden by Nek Chand — 40-acre sculpture garden made entirely from recycled waste and found objects",
            "Sukhna Lake — man-made reservoir at the Shivalik foothills, popular for rowing and evening walks",
            "Sector 17 plaza is the city's central shopping and gathering hub — designed as a pedestrian precinct",
        ],
        "legal_rules": [
            "Union Territory — administered directly by the central government, not by Punjab or Haryana",
            "Strict traffic enforcement — Chandigarh Traffic Police known for heavy challans; helmet and seatbelt rules rigidly enforced",
            "No-construction beyond ground+3 floors in most residential sectors — strict height restrictions maintain the Le Corbusier plan",
        ],
        "behavioral_notes": [
            "Punjabi culture dominant — Punjabi and Hindi spoken interchangeably; Haryanvi less common in the city",
            "One of India's cleanest and most organized cities — residents take pride in civic order",
            "Evening culture of walking along Sukhna Lake and eating out in Sector 26 and 35 food streets",
        ],
    },

    # --- 12. Kochi (Kerala) ---
    {
        "id": "kochi",
        "type": "city",
        "parent_region": "kerala",
        "dominant_language": "Malayalam",
        "cultural_markers": [
            "Fort Kochi — Portuguese, Dutch, and British colonial layers; Chinese fishing nets (cheena vala) at the waterfront since 14th century",
            "Kochi-Muziris Biennale — India's largest contemporary art festival held in Fort Kochi warehouses",
            "Jew Town and Paradesi Synagogue (1568) in Mattancherry — one of the oldest active synagogues in the Commonwealth",
            "Kerala seafood cuisine — karimeen (pearl spot fish), meen pollichathu (fish in banana leaf), and appam with stew",
        ],
        "legal_rules": [
            "Alcohol available only at Bevco outlets and 5-star hotels — beer/wine parlors have separate licensing",
            "Kochi Metro is India's first metro with a transgender-inclusive workforce — progressive civic policies",
            "GCDA (Greater Cochin Development Authority) enforces CRZ rules strictly in the backwater and coastal areas",
        ],
        "behavioral_notes": [
            "Cosmopolitan and tolerant — Hindu, Muslim, Christian, and Jewish communities have coexisted for centuries",
            "English widely spoken — Kochi is one of the most English-friendly cities in South India",
            "Kathakali performances at Kerala Kathakali Centre and Greenix Village are cultural must-sees, not tourist traps",
        ],
    },

    # --- 13. Thiruvananthapuram (Kerala) ---
    {
        "id": "thiruvananthapuram",
        "type": "city",
        "parent_region": "kerala",
        "dominant_language": "Malayalam",
        "cultural_markers": [
            "Sri Padmanabhaswamy Temple — richest temple in the world with vaults containing billions in gold and gems",
            "Kovalam Beach — crescent-shaped beach with lighthouse, one of India's earliest international beach destinations",
            "Napier Museum and Kuthiramalika (Horse Palace) showcase Kerala's art and royal heritage",
            "Puttu and kadala curry, avial, and Kerala parotta with beef fry are local food staples",
        ],
        "legal_rules": [
            "Temple dress code strictly enforced at Padmanabhaswamy — men must wear mundu (dhoti), women sari or salwar; no western wear",
            "Bevco liquor shops are the only legal retail outlets for alcohol — long queues common on weekends",
            "CRZ (Coastal Regulation Zone) restrictions enforced along the coastline — no construction within 200m of high tide line",
        ],
        "behavioral_notes": [
            "Government employee culture strong — the city revolves around the Secretariat and administrative offices",
            "Malayali intellectual tradition — high newspaper readership, politically aware citizenry",
            "Onam Sadya (vegetarian feast on banana leaf) is the city's grandest culinary tradition — 26+ dishes served",
        ],
    },

    # --- 14. Goa / Panaji ---
    {
        "id": "panaji",
        "type": "city",
        "parent_region": "goa",
        "dominant_language": "Konkani",
        "cultural_markers": [
            "Fontainhas Latin Quarter — colorful Portuguese-era houses, narrow streets, and heritage tile work",
            "Church of Our Lady of the Immaculate Conception (1541) — whitewashed Baroque church overlooking the main square",
            "Mandovi River promenade and floating casinos — Deltin Royale is India's largest offshore casino",
            "Goan fish curry rice (xitt kodi), pork vindaloo, bebinca (layered coconut dessert) define the cuisine",
        ],
        "legal_rules": [
            "Drinking age 18 — alcohol widely and cheaply available; no restricted timings for most bars",
            "Casino gambling legal — regulated by the Goa Public Gambling Act; offshore casinos on the Mandovi",
            "Beach shack licenses are seasonal (October-May) — shacks must be dismantled during monsoon",
        ],
        "behavioral_notes": [
            "Susegad (contented, laid-back) attitude is not laziness — it's the Goan philosophy of life",
            "Afternoon siesta is real — many shops and businesses close between 1 PM and 4 PM",
            "Locals speak Konkani at home, but Portuguese influences linger in names, food, and architecture",
        ],
    },

    # --- 15. Varanasi (Uttar Pradesh) ---
    {
        "id": "varanasi",
        "type": "city",
        "parent_region": "uttar_pradesh",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Oldest continuously inhabited city in the world — spiritual capital of Hinduism on the Ganges",
            "Dashashwamedh Ghat evening Ganga Aarti — spectacular nightly fire ritual with Vedic chanting",
            "Kashi Vishwanath Temple (Jyotirlinga) — one of the 12 most sacred Shiva temples, rebuilt and expanded with the Kashi Vishwanath Corridor",
            "Banarasi silk sarees — handwoven brocade with gold and silver zari thread, a centuries-old craft tradition",
        ],
        "legal_rules": [
            "Non-vegetarian food and alcohol prohibited in the vicinity of Kashi Vishwanath Temple and many ghats",
            "Photography restrictions at certain ghats during cremation rituals — Manikarnika and Harishchandra ghats",
            "Drone flying banned near the ghats and temple corridor — security enforcement strict since the corridor opening",
        ],
        "behavioral_notes": [
            "Death is not taboo here — open-air cremations at Manikarnika Ghat are a sacred, not morbid, tradition",
            "Touts and self-appointed guides are persistent at ghats — politely decline or agree on a fixed price beforehand",
            "Boat rides on the Ganges at dawn are the quintessential experience — negotiate boat prices firmly",
        ],
    },

    # --- 16. Amritsar (Punjab) ---
    {
        "id": "amritsar",
        "type": "city",
        "parent_region": "punjab",
        "dominant_language": "Punjabi",
        "cultural_markers": [
            "Harmandir Sahib (Golden Temple) — holiest Gurdwara in Sikhism, gold-plated shrine in the Amrit Sarovar (pool of nectar)",
            "Langar at the Golden Temple — the world's largest free community kitchen serving 75,000-100,000 meals daily",
            "Jallianwala Bagh — site of the 1919 massacre, now a national memorial with bullet-marked walls",
            "Amritsari kulcha, chole, lassi, and tandoori chicken from Beera Chicken House and Kesar Da Dhaba (est. 1916) are legendary",
        ],
        "legal_rules": [
            "Golden Temple premises — no tobacco, alcohol, or drugs; shoes must be removed; head must be covered",
            "Wagah Border ceremony area has security protocols — arrive 2-3 hours early; no bags allowed in the stadium",
            "Heritage zone restrictions around the Golden Temple — no high-rise construction in the immediate vicinity",
        ],
        "behavioral_notes": [
            "Cover your head before entering any Gurdwara — scarves available for free at the entrance",
            "Sikh hospitality is legendary — if invited to eat, do not refuse; it is offered with love",
            "Wagah Border ceremony is a patriotic spectacle — arrive early (by 3 PM in winter) for good seats",
        ],
    },

    # --- 17. Udaipur (Rajasthan) ---
    {
        "id": "udaipur",
        "type": "city",
        "parent_region": "rajasthan",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "City of Lakes — Lake Pichola, Fateh Sagar Lake, and the Lake Palace (Taj hotel) floating on the water",
            "City Palace complex — largest palace complex in Rajasthan, seat of the Mewar dynasty for 400+ years",
            "Miniature painting tradition — Mewar school of painting with intricate depictions of courtly and religious scenes",
            "Shilpgram crafts village and Bagore Ki Haveli evening folk dance shows showcase living Rajasthani culture",
        ],
        "legal_rules": [
            "Lake Pichola and Fateh Sagar have restricted boating zones — only authorized boats allowed",
            "Heritage building regulations — no modern construction allowed that alters the old city skyline around the lakes",
            "Alcohol available in hotels and licensed restaurants but many areas near temples are dry",
        ],
        "behavioral_notes": [
            "Udaipur is romantic and tourist-friendly — less aggressive touts compared to Jaipur or Jodhpur",
            "Respect for the Mewar royal family (Custodian of the City Palace) remains strong among locals",
            "Evening sunset views from rooftop restaurants near Gangaur Ghat are the cultural ritual — expect crowds",
        ],
    },

    # --- 18. Mysuru / Mysore (Karnataka) ---
    {
        "id": "mysuru",
        "type": "city",
        "parent_region": "karnataka",
        "dominant_language": "Kannada",
        "cultural_markers": [
            "Mysore Palace (Amba Vilas) — Indo-Saracenic masterpiece illuminated with 97,000 bulbs on Sundays and during Dasara",
            "Mysore Dasara — 10-day state festival culminating in a grand Jamboo Savari (elephant procession) on Vijayadashami",
            "Devaraja Market — 130-year-old market selling Mysore jasmine, sandalwood, silk, and spices",
            "Mysore pak (ghee-based sweet from Guru Sweet Mart, est. 1935), Mysore masala dosa, and filter coffee define the food culture",
        ],
        "legal_rules": [
            "Heritage zone restrictions around Mysore Palace — no commercial alterations allowed to surrounding buildings",
            "Chamundi Hill temple has a regulated vehicle route — parking and access controlled especially during festivals",
            "Noise restrictions enforced during Dasara — amplified music permissions require police NOC",
        ],
        "behavioral_notes": [
            "Mysore is quieter, cleaner, and more traditional than Bangalore — a slower, gentler pace of life",
            "Royalty is still respected — the Wadiyar family participates in Dasara events and the public reveres them",
            "Yoga tourism is significant — Ashtanga yoga practitioners come from worldwide to study at KPJAYI (K. Pattabhi Jois Institute)",
        ],
    },

    # --- 19. Coimbatore (Tamil Nadu) ---
    {
        "id": "coimbatore",
        "type": "city",
        "parent_region": "tamil_nadu",
        "dominant_language": "Tamil",
        "cultural_markers": [
            "Manchester of South India — textile and cotton mill heritage; Tirupur nearby is India's knitwear capital",
            "Isha Yoga Center (Isha Foundation) and the 112-foot Adiyogi Shiva statue at the foothills of the Velliangiri Mountains",
            "Marudhamalai Murugan Temple on the hill and Perur Pateeswarar Temple are important pilgrimage sites",
            "Coimbatore is known for its unique variant of South Indian food — Kongunad cuisine featuring kola urundai (meatballs), chicken biryani with seeraga samba rice",
        ],
        "legal_rules": [
            "TASMAC shops only for alcohol — state-run outlets; bars in hotels have separate licenses",
            "Coimbatore Corporation enforces industrial emission norms strictly — air quality monitoring in industrial areas",
            "Plastic ban enforcement is active — cloth bags expected at all markets and shops",
        ],
        "behavioral_notes": [
            "Coimbatore people are known for business acumen — the city has one of the highest densities of small and medium industries",
            "Kongunad Tamil dialect is distinct from Chennai Tamil — locals are proud of their Kongu identity",
            "Conservative and family-oriented city — nightlife is minimal compared to Chennai or Bangalore",
        ],
    },

    # --- 20. Madurai (Tamil Nadu) ---
    {
        "id": "madurai",
        "type": "city",
        "parent_region": "tamil_nadu",
        "dominant_language": "Tamil",
        "cultural_markers": [
            "Meenakshi Amman Temple — towering gopurams (gateway towers) with 33,000 sculptures; one of India's grandest temples",
            "Madurai is one of the oldest continuously inhabited cities in India — over 2,500 years old, mentioned in Sangam literature",
            "Jallikattu (bull-taming) during Pongal — Madurai's Alanganallur is the most famous arena",
            "Jigarthanda (cold dessert drink of milk, almond gum, sarsaparilla syrup, and ice cream) is unique to Madurai — Famous Jigarthanda is the iconic shop",
        ],
        "legal_rules": [
            "Meenakshi Temple has strict dress code — no shorts, sleeveless tops, or leather items inside",
            "Photography banned inside the sanctum of Meenakshi Temple — cameras/phones confiscated if rules violated",
            "TASMAC liquor shops only — no private alcohol retail",
        ],
        "behavioral_notes": [
            "Madurai Tamil is considered the purest form of the language — locals take immense pride in it",
            "Temple rituals dominate daily life — Meenakshi Temple's morning and evening puja schedules shape local routines",
            "Extremely hot climate — locals rest during 12 PM-3 PM; plan outdoor activities for early morning or evening",
        ],
    },

    # --- 21. Bhopal (Madhya Pradesh) ---
    {
        "id": "bhopal",
        "type": "city",
        "parent_region": "madhya_pradesh",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "City of Lakes — Upper Lake (Bhojtal, 11th century) and Lower Lake define the city's geography",
            "Taj-ul-Masajid — one of the largest mosques in Asia, reflecting Bhopal's Nawabi heritage",
            "Bharat Bhavan — multi-arts complex designed by Charles Correa, hosting tribal art, theatre, and poetry",
            "Bhopali gosht (mutton), biryani-pilaf, and poha-jalebi (breakfast staple) define the food culture",
        ],
        "legal_rules": [
            "Bhopal Gas Tragedy (1984) legacy — industrial safety regulations in Bhopal are among the strictest in India",
            "BMC enforces heritage zone restrictions around the old city and lake areas",
            "Alcohol legal but restricted timings for bars — most close by 11 PM",
        ],
        "behavioral_notes": [
            "Bhopal has a Nawabi culture of politeness — 'Janab' and 'Begum Sahiba' still used as respectful forms of address",
            "Poha and jalebi for breakfast is a Bhopali ritual — every neighborhood has a favorite poha stall",
            "The city is surprisingly green and spread out — cycling around the lakes is a growing local trend",
        ],
    },

    # --- 22. Indore (Madhya Pradesh) ---
    {
        "id": "indore",
        "type": "city",
        "parent_region": "madhya_pradesh",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "India's cleanest city — won the Swachh Survekshan award multiple consecutive times (7 times as of 2023)",
            "Sarafa Bazaar — jewelry market by day, famous street food market by night (opens after 8 PM)",
            "Rajwada Palace (Holkar dynasty, 18th century) in the old city center is the historical heart",
            "Street food capital of MP — dal bafla, poha, garadu (yam fry), sabudana khichdi, bhutte ka kees (corn dish) from Chappan Dukan (56 Shops)",
        ],
        "legal_rules": [
            "Waste segregation and cleanliness norms are strictly enforced — IMC (Indore Municipal Corporation) fines for littering",
            "Alcohol legal; bars and restaurants have standard closing times around 11 PM",
            "Traffic enforcement increasingly strict — e-challans for traffic violations common",
        ],
        "behavioral_notes": [
            "Indoris take immense pride in their city's cleanliness — do not litter; you will be noticed",
            "Street food culture is a nightly social event — Sarafa and Chappan Dukan are crowded from 8 PM to midnight",
            "Malwi dialect of Hindi spoken with a distinctive musical intonation — warm and humorous conversational style",
        ],
    },

    # --- 23. Bhubaneswar (Odisha) ---
    {
        "id": "bhubaneswar",
        "type": "city",
        "parent_region": "odisha",
        "dominant_language": "Odia",
        "cultural_markers": [
            "Temple City — over 700 temples including the Lingaraj Temple (11th century), Mukteshwar Temple, and Rajarani Temple",
            "Dhauli Peace Pagoda — site where Emperor Ashoka embraced Buddhism after the Kalinga War (261 BCE)",
            "Tribal museum (Museum of Tribal Arts and Artifacts) showcases Odisha's 62 tribal communities",
            "Dalma (lentil-vegetable stew), chena poda (cheese dessert), and pakhala bhata (fermented rice) are signature dishes",
        ],
        "legal_rules": [
            "Lingaraj Temple — entry restricted to Hindus only; strict dress code enforcement",
            "BDA (Bhubaneswar Development Authority) enforces heritage zone buffer rules around ancient temples",
            "Alcohol legal but not sold near temple zones — state-run outlets in designated areas",
        ],
        "behavioral_notes": [
            "Odia people are known for humility and politeness — soft-spoken interaction is the norm",
            "Rice is the absolute staple of every meal — asking for roti as a primary carb may seem unusual",
            "Rath Yatra fever grips the city even though the main event is in Puri — Bhubaneswar has its own smaller processions",
        ],
    },

    # --- 24. Guwahati (Assam) ---
    {
        "id": "guwahati",
        "type": "city",
        "parent_region": "assam",
        "dominant_language": "Assamese",
        "cultural_markers": [
            "Kamakhya Temple on Nilachal Hill — one of 51 Shakti Peethas, famous for Ambubachi Mela (annual fertility festival)",
            "Gateway to Northeast India — Guwahati is the transport hub for the Seven Sisters states",
            "Brahmaputra River defines the city — Umananda Island (smallest inhabited river island) sits mid-river",
            "Assamese thali with rice, dal, masor tenga (sour fish curry), khar (alkaline dish), and pitha (rice cakes) is the food identity",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 21 — but restrictions during Bihu festival days",
            "Inner Line Permit not needed for Assam itself but required to visit Arunachal Pradesh, Nagaland, Mizoram from Guwahati",
            "Kamakhya Temple has restricted photography in inner sanctum and specific dress norms",
        ],
        "behavioral_notes": [
            "Offering a gamosa (woven cotton towel) is the Assamese way of showing respect and welcome",
            "Bihu celebrations in April (Rongali Bihu) are exuberant — the city celebrates for a full week",
            "Northeast identity is distinct from mainland India — sensitivity about being called 'Chinese' or 'Nepali' is important",
        ],
    },

    # --- 25. Shimla (Himachal Pradesh) ---
    {
        "id": "shimla",
        "type": "city",
        "parent_region": "himachal_pradesh",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Former summer capital of British India — The Ridge, Mall Road, Christ Church (1857), and Viceregal Lodge define the colonial heritage",
            "Kalka-Shimla heritage railway (UNESCO World Heritage) — toy train journey through 102 tunnels and 800+ bridges",
            "Jakhu Temple (Hanuman temple at 2,455m) offers panoramic Himalayan views and is the city's highest point",
            "Shimla's siddu (steamed stuffed bread), Himachali dham (festive meal), and Tudkiya Bhath (spiced rice) are local specialties",
        ],
        "legal_rules": [
            "Vehicle restrictions on Mall Road — no vehicles allowed on the pedestrian promenade",
            "Plastic bags banned across Shimla — strict fines enforced especially in the main tourist areas",
            "Construction regulations are strict — building permits tightly controlled to prevent hillside destabilization",
        ],
        "behavioral_notes": [
            "Shimla is walkable and meant to be walked — the Ridge and Mall Road are the social centers",
            "Winter (December-February) brings heavy snowfall — the city transforms but roads become treacherous",
            "Himachali people are reserved but friendly — a simple 'Namaste' with folded hands goes a long way",
        ],
    },

    # --- 26. Dehradun (Uttarakhand) ---
    {
        "id": "dehradun",
        "type": "city",
        "parent_region": "uttarakhand",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Elite boarding school tradition — Doon School, Welham, Rashtriya Indian Military College shape the city's educational prestige",
            "Forest Research Institute (FRI) — colonial-era Greco-Roman architecture campus; largest of its kind in Asia",
            "Robber's Cave (Gucchu Pani) and Sahastradhara (Thousand Fold Spring) are popular natural attractions",
            "Dehradun is the gateway to Mussoorie (Queen of Hills), Haridwar, and Rishikesh — a transit hub for pilgrims and trekkers",
        ],
        "legal_rules": [
            "Dehradun Municipal Corporation enforces hill construction norms — no building beyond sanctioned floors",
            "Alcohol legal — but Haridwar (just 50 km away) is completely dry; no alcohol allowed",
            "Traffic police enforce pollution-under-control (PUC) certificate checks regularly",
        ],
        "behavioral_notes": [
            "City has a cantonment and old-money culture — Rajpur Road and Clement Town have a relaxed, tree-lined ambiance",
            "Mix of Garhwali hill culture and plains culture — both Hindi and Garhwali spoken",
            "Bakeries (like Ellora's and Kumar's) are a Dehradun institution — bread and pastries are a colonial-era legacy",
        ],
    },

    # --- 27. Rishikesh (Uttarakhand) ---
    {
        "id": "rishikesh",
        "type": "city",
        "parent_region": "uttarakhand",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Yoga Capital of the World — hundreds of ashrams including Parmarth Niketan, Sivananda Ashram, and the Beatles Ashram (Maharishi Mahesh Yogi's ashram)",
            "Laxman Jhula and Ram Jhula — iconic suspension bridges over the Ganges (Laxman Jhula closed to foot traffic due to structural concerns, replaced by a new bridge)",
            "White-water rafting on the Ganges — Shivpuri to Rishikesh stretch is India's most popular rafting route",
            "Triveni Ghat evening Ganga Aarti — smaller and more intimate than Varanasi's but equally spiritual",
        ],
        "legal_rules": [
            "Rishikesh is a holy city — alcohol and non-vegetarian food are completely banned within city limits",
            "Plastic bags and bottles discouraged — many ashrams and cafes refuse single-use plastic",
            "River rafting regulated by the Uttarakhand government — licensed operators only, safety gear mandatory",
        ],
        "behavioral_notes": [
            "Respect ashram rules — silence zones, fixed meal times, no shoes indoors, dress modestly",
            "The international yoga community is large — English widely spoken in cafes and ashrams along the riverside",
            "Cow traffic on the bridges and roads is normal — patience and gentle navigation required",
        ],
    },

    # --- 28. Srinagar (Jammu & Kashmir) ---
    {
        "id": "srinagar",
        "type": "city",
        "parent_region": "jammu_and_kashmir",
        "dominant_language": "Kashmiri",
        "cultural_markers": [
            "Dal Lake and Nigeen Lake with shikaras and houseboats — staying on a houseboat is the quintessential Srinagar experience",
            "Mughal Gardens — Shalimar Bagh, Nishat Bagh, and Chashme Shahi terraced gardens from the 17th century",
            "Pashmina shawl and Kashmiri carpet weaving — artisan traditions passed through generations in the old city",
            "Wazwan feast (36-course Kashmiri banquet) — rogan josh, gushtaba, tabak maaz, and rista are signature dishes",
        ],
        "legal_rules": [
            "Security situation requires awareness — periodic curfews, internet shutdowns, and Section 144 orders can happen",
            "Photography near military installations, bunkers, and certain bridges is strictly prohibited",
            "Shikara and houseboat rates regulated by the J&K Tourism Department — printed rate cards available",
        ],
        "behavioral_notes": [
            "Kashmiris welcome tourists warmly with kehwa (saffron-almond tea) — accepting is a sign of respect",
            "Political situation is sensitive — avoid initiating political conversations unless invited",
            "Bargaining in the floating market and shikara bazaar is expected — start at 40-50% of quoted price",
        ],
    },

    # --- 29. Leh (Ladakh) ---
    {
        "id": "leh",
        "type": "city",
        "parent_region": "ladakh",
        "dominant_language": "Ladakhi",
        "cultural_markers": [
            "Leh Palace (17th century, modeled after the Potala Palace) overlooks the town from a hilltop",
            "Shanti Stupa (1991, Japanese Buddhist) — white-domed stupa with panoramic views of the Leh valley",
            "Changspa and Main Bazaar — traveler hub with cafes, Ladakhi jewelry, and pashmina shops",
            "Thukpa (Tibetan noodle soup), momos, skyu (Ladakhi pasta stew), and butter tea are the food staples",
        ],
        "legal_rules": [
            "Inner Line Permit required for Nubra Valley, Pangong Lake, Tso Moriri, and Hanle — obtainable at DC office in Leh",
            "Foreign nationals need a Protected Area Permit (PAP) and must travel in groups of 2+ for restricted zones",
            "No camping outside designated campsites — environmental protection rules strictly enforced by the administration",
        ],
        "behavioral_notes": [
            "'Julley' is the greeting for hello, thank you, and goodbye — use it generously",
            "Acclimatize for at least 24-48 hours upon arrival — altitude sickness is a serious risk at 3,500m",
            "Ladakhi culture is Tibetan Buddhist — walk clockwise around stupas and mani walls, spin prayer wheels clockwise",
        ],
    },

    # --- 30. Gangtok (Sikkim) ---
    {
        "id": "gangtok",
        "type": "city",
        "parent_region": "sikkim",
        "dominant_language": "Nepali",
        "cultural_markers": [
            "MG Marg — pedestrianized main street with cafes, shops, and mountain views; the heart of Gangtok",
            "Rumtek Monastery — seat of the Karmapa, one of the most important Tibetan Buddhist monasteries outside Tibet",
            "Enchey Monastery and Do Drul Chorten (stupa) represent the city's Buddhist spiritual identity",
            "Momos, thukpa, gundruk (fermented leafy greens), phagshapa (pork with radish), and tongba (millet beer) define the cuisine",
        ],
        "legal_rules": [
            "Inner Line Permit required for Nathula Pass (India-China border) — obtain from Gangtok Tourism Office; closed on Mondays and Tuesdays",
            "Tobacco products banned across Sikkim — Sikkim is India's first tobacco-free state in public spaces",
            "Protected Area Permit needed for foreign nationals to visit most areas outside Gangtok",
        ],
        "behavioral_notes": [
            "Sikkimese people are gentle and soft-spoken — loud, aggressive behavior is culturally out of place",
            "Clean city — littering is taken seriously; Gangtok takes visible pride in cleanliness",
            "Respect Buddhist sites — do not touch or sit on prayer stones, stupas, or monastery artifacts",
        ],
    },

    # --- 31. Shillong (Meghalaya) ---
    {
        "id": "shillong",
        "type": "city",
        "parent_region": "meghalaya",
        "dominant_language": "Khasi",
        "cultural_markers": [
            "Scotland of the East — rolling hills, pine forests, and colonial-era churches and bungalows",
            "Live music and rock/blues culture — Shillong is India's rock music capital; Bob Dylan-inspired cafe culture in Police Bazaar",
            "Iewduh (Bara Bazaar) — largest traditional market in Northeast India, selling everything from local produce to handloomed textiles",
            "Jadoh (rice cooked with pork), tungrymbai (fermented soybean), doh khlieh (pork salad), and kwai (betel nut) define the food culture",
        ],
        "legal_rules": [
            "Autonomous District Council (Khasi Hills) administers traditional laws alongside state laws in tribal areas",
            "Alcohol legal; drinking age 21 — local rice beer (kiad) widely available",
            "Inner Line Permit not required for Shillong but may be needed for remote areas near the Bangladesh border",
        ],
        "behavioral_notes": [
            "Khasi society is matrilineal — family name passes through the mother; respect this unique social structure",
            "English is widely spoken alongside Khasi — Shillong is one of the most English-literate cities in India",
            "Church attendance on Sundays is significant — many shops in predominantly Christian areas close or open late",
        ],
    },

    # --- 32. Visakhapatnam (Andhra Pradesh) ---
    {
        "id": "visakhapatnam",
        "type": "city",
        "parent_region": "andhra_pradesh",
        "dominant_language": "Telugu",
        "cultural_markers": [
            "City of Destiny (Vizag) — Ramakrishna Beach, Rishikonda Beach, and Kailasagiri hilltop park along the coastline",
            "INS Kurusura Submarine Museum — decommissioned submarine on RK Beach, one of India's few submarine museums",
            "Simhachalam Temple (Varaha Narasimha Swamy) — 11th-century Odia-Dravidian temple on Simhachalam hill",
            "Vizag is known for its seafood — bamboo chicken (cooked inside bamboo), fish pulusu (tamarind-based fish curry), and Andhra-style prawns",
        ],
        "legal_rules": [
            "AP government alcohol restrictions apply — limited number of licensed outlets",
            "Navy and defense zones along the coast have restricted access and photography bans",
            "CRZ (Coastal Regulation Zone) enforcement along the beach — no construction in regulated zones",
        ],
        "behavioral_notes": [
            "Vizag has a defense and navy culture — city is home to the Eastern Naval Command; respect for armed forces is strong",
            "Telugu spoken with a distinctive north-coastal Uttarandhra accent — different from Hyderabad Telugu",
            "Friendly and laid-back coastal city vibe — less formal than Hyderabad, with strong seafood and beach culture",
        ],
    },

    # --- 33. Jodhpur (Rajasthan) ---
    {
        "id": "jodhpur",
        "type": "city",
        "parent_region": "rajasthan",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Blue City — old city houses painted indigo blue, visible dramatically from Mehrangarh Fort",
            "Mehrangarh Fort — one of India's largest and best-preserved forts, perched on a 125m cliff, housing an outstanding museum",
            "Umaid Bhawan Palace — Art Deco royal residence, part palace museum, part Taj hotel, part royal family home",
            "Mirchi bada (chili fritter), mawa kachori, makhaniya lassi, and pyaaz ki kachori from Shahi Samosa are Jodhpur's street food icons",
        ],
        "legal_rules": [
            "Heritage zone around Mehrangarh — strict restrictions on construction height and facade modifications",
            "Alcohol available in hotels but dry days enforced strictly — check calendar before planning",
            "Camel/horse ride operators at forts regulated — use only government-authorized guides and operators",
        ],
        "behavioral_notes": [
            "Marwari culture is strong — traditional Rajput hospitality involves offering water and buttermilk to guests",
            "Summers are brutally hot (45C+) — locals follow early morning and late evening routines; midday rest is standard",
            "Jodhpuri suits (bandhgala) originated here — the city has a strong tailoring tradition",
        ],
    },

    # --- 34. Agra (Uttar Pradesh) ---
    {
        "id": "agra",
        "type": "city",
        "parent_region": "uttar_pradesh",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Taj Mahal — UNESCO World Heritage Site, Mughal emperor Shah Jahan's marble mausoleum for Mumtaz Mahal (1632-1653)",
            "Agra Fort (UNESCO) — massive red sandstone Mughal fort with Diwan-i-Am, Diwan-i-Khas, and Sheesh Mahal",
            "Fatehpur Sikri (38 km) — abandoned Mughal capital built by Akbar, UNESCO World Heritage Site",
            "Petha (translucent sweet made from ash gourd) is Agra's signature sweet — Panchhi Petha (est. 1950s) is the most famous brand",
        ],
        "legal_rules": [
            "Taj Trapezium Zone (TTZ) environmental regulations — industrial emissions heavily restricted within 10,400 sq km around the Taj",
            "Drone flying banned in the Taj Mahal security zone",
            "Taj Mahal closed on Fridays (except for namaz at the mosque) — plan visits accordingly",
        ],
        "behavioral_notes": [
            "Touts and unauthorized guides are aggressive at the Taj — only use ASI (Archaeological Survey of India) authorized guides",
            "Pollution and Yamuna river cleanliness are persistent concerns — the marble has faced yellowing from pollution",
            "Agra is a day-trip city for many tourists — but staying overnight allows sunrise and sunset Taj views",
        ],
    },

    # --- 35. Patna (Bihar) ---
    {
        "id": "patna",
        "type": "city",
        "parent_region": "bihar",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Ancient city of Pataliputra — capital of the Maurya and Gupta empires, over 2,500 years of history",
            "Golghar (1786) — British-era beehive-shaped granary with panoramic city and Ganges views from the top",
            "Mahavir Mandir near Patna Junction — one of the most visited Hanuman temples in India",
            "Litti chokha (roasted wheat balls with mashed vegetables), sattu paratha, and Patna's thekua (sweet snack) define the food culture",
        ],
        "legal_rules": [
            "Bihar is a dry state — complete alcohol prohibition; possession and consumption lead to arrest and heavy fines",
            "Patna Municipal Corporation waste management rules — segregation mandatory",
            "Chhath Puja ghat preparations involve temporary road closures and traffic diversions near the Ganges",
        ],
        "behavioral_notes": [
            "Chhath Puja (October/November) is the most important festival — the city comes to a standstill for the rituals",
            "Respect for elders is paramount — touching feet (pranam) is standard greeting for older people",
            "Bhojpuri and Magahi dialects commonly spoken alongside Hindi — Maithili in northern parts of the state",
        ],
    },

    # --- 36. Ranchi (Jharkhand) ---
    {
        "id": "ranchi",
        "type": "city",
        "parent_region": "jharkhand",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "City of Waterfalls — Dassam Falls, Hundru Falls, and Jonha Falls within 40 km radius of the city",
            "Tagore Hill — where Rabindranath Tagore's elder brother Jyotirindranath Tagore lived; hilltop with city views",
            "Tribal culture presence — Sarhul (spring festival) and Karma (harvest festival) celebrated with community dancing",
            "Dhuska (deep-fried rice-lentil pancake), litti chokha, and handia (rice beer) are local food specialties",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 21 — but tribal areas may have customary rules on alcohol",
            "Jharkhand Tenancy Act protects tribal land — land transactions in scheduled areas require special permissions",
            "Traffic enforcement is growing but still evolving — helmet and seatbelt compliance improving",
        ],
        "behavioral_notes": [
            "Ranchi was the birthplace of MS Dhoni — cricket culture is passionate; JSCA International Stadium is a source of local pride",
            "Tribal and non-tribal populations coexist — sensitivity to tribal customs in surrounding areas is important",
            "Pleasant climate year-round (compared to neighboring Bihar) — Ranchi is on a plateau at 650m elevation",
        ],
    },

    # --- 37. Raipur (Chhattisgarh) ---
    {
        "id": "raipur",
        "type": "city",
        "parent_region": "chhattisgarh",
        "dominant_language": "Hindi",
        "cultural_markers": [
            "Naya Raipur (Atal Nagar) — one of India's newest planned smart cities, the new capital of Chhattisgarh since state formation in 2000",
            "Purkhouti Muktangan — open-air museum showcasing Chhattisgarh's tribal art, culture, and architecture",
            "Mahant Ghasidas Memorial Museum — repository of tribal artifacts, inscriptions, and archaeological finds",
            "Bore baasi (fermented cold rice), chila (rice flour pancake), fara (steamed rice dumplings), and aamat (tribal mixed vegetable stew) are local specialties",
        ],
        "legal_rules": [
            "Alcohol legal; drinking age 21 — state-run and private liquor shops available",
            "Raipur Development Authority enforces smart city construction norms in Naya Raipur zone",
            "Industrial emission norms enforced — Raipur has steel plants and sponge iron factories on the outskirts",
        ],
        "behavioral_notes": [
            "Chhattisgarhi dialect is the daily language — standard Hindi understood but locals prefer Chhattisgarhi",
            "Rice is the absolute dietary staple — 'chawal' (rice) is non-negotiable in every meal",
            "Rapidly developing city — infrastructure is improving but public transport is still limited; autos and cabs are primary",
        ],
    },

    # --- 38. Nagpur (Maharashtra) ---
    {
        "id": "nagpur",
        "type": "city",
        "parent_region": "maharashtra",
        "dominant_language": "Marathi",
        "cultural_markers": [
            "Orange City — Nagpur is India's largest orange trading hub; Nagpur oranges (Citrus reticulata) are a GI-tagged product",
            "Zero Mile Stone — geographical center of India, located at the old British survey marker in the city center",
            "Deekshabhoomi — the site where Dr. B.R. Ambedkar embraced Buddhism in 1956 with 600,000 followers; a major Buddhist pilgrimage site",
            "Saoji cuisine — fiery, oil-rich mutton and chicken gravies unique to Nagpur; tarri poha (spiced poha with curry) is the breakfast staple",
        ],
        "legal_rules": [
            "Maharashtra beef ban applies — but Nagpur's Vidarbha region has distinct cultural food practices",
            "Nagpur Municipal Corporation enforces noise and pollution norms — tree-cutting requires NMC permission",
            "Nagpur Metro recently operational — follow metro etiquette rules similar to Delhi Metro",
        ],
        "behavioral_notes": [
            "Nagpuri Marathi (Varhadi dialect) is distinct from Pune/Mumbai Marathi — locals are proud of this identity",
            "Politically important city — RSS headquarters (Sangh Bhavan) is in Nagpur, and it is a site of winter legislature sessions",
            "Summers are extreme (45C+) — the city empties during May; locals adapt with early morning routines",
        ],
    },

    # --- 39. Surat (Gujarat) ---
    {
        "id": "surat",
        "type": "city",
        "parent_region": "gujarat",
        "dominant_language": "Gujarati",
        "cultural_markers": [
            "Diamond capital of the world — 90% of the world's diamonds are cut and polished in Surat",
            "Textile city — Surat produces a massive share of India's synthetic fabric, especially for sarees",
            "Locho, khaman, surti undhiyu (winter mixed vegetable dish), ghari (sweet pastry) — Surat is arguably Gujarat's food capital",
            "Dutch Cemetery and Surat Castle — remnants of the city's history as India's first major port for European traders",
        ],
        "legal_rules": [
            "Dry city in a dry state — alcohol strictly prohibited; permits theoretically available but rarely issued",
            "SMC (Surat Municipal Corporation) is known for very strict cleanliness enforcement — the city transformed after the 1994 plague",
            "Diamond industry has its own informal regulatory ecosystem — trust-based transactions in Varachha and Mahidharpura",
        ],
        "behavioral_notes": [
            "Surati people are known for food obsession — the city eats out more than almost any other Indian city",
            "Garba during Navratri is a citywide phenomenon — massive community gatherings nightly for nine days",
            "Business-first culture — Surat runs on trade and commerce; conversations often lead back to business",
        ],
    },

    # --- 40. Kozhikode / Calicut (Kerala) ---
    {
        "id": "kozhikode",
        "type": "city",
        "parent_region": "kerala",
        "dominant_language": "Malayalam",
        "cultural_markers": [
            "City of Spices — Vasco da Gama landed here in 1498, opening the spice trade route to Europe",
            "Kozhikode halwa (made with coconut oil, rice flour, and jaggery at SM Street's iconic sweet shops) and Kozhikode biryani (with distinctive Malabar flavors) are legendary",
            "Kuttichira — historic Muslim quarter with ancient mosques, including Mishkal Mosque (14th century, built like a Chinese pagoda)",
            "Tali Temple, Mananchira Square, and the beach (Kozhikode Beach) form the cultural triangle of the city center",
        ],
        "legal_rules": [
            "Bevco liquor outlets only — Kerala's state-run alcohol retail system applies",
            "Kozhikode Corporation enforces heritage conservation in the old Kuttichira and SM Street areas",
            "Hartals (political strikes) called by parties can shut down the city unexpectedly — check local news",
        ],
        "behavioral_notes": [
            "Moplah (Malabar Muslim) culture is distinctive — cuisine, language (Mappila Malayalam), and customs differ from other Kerala regions",
            "Kozhikode is a food city above all — locals will debate biryani shops and halwa brands with passion",
            "Friendly and cosmopolitan — the city has a long tradition of welcoming outsiders, rooted in its trading port history",
        ],
    },

    # =========================================================================
    # SPECIAL ZONES
    # =========================================================================
    {
        "id": "meenakshi_temple",
        "type": "zone",
        "parent_region": "tamil_nadu",
        "dominant_language": "Tamil",
        "cultural_markers": [
            "One of the most important Hindu temples in India",
            "Dravidian architecture masterpiece",
            "Active place of worship — not just a tourist site",
        ],
        "legal_rules": [
            "Strict dress code: no shorts, sleeveless tops, or revealing clothing",
            "Photography prohibited inside sanctum sanctorum",
            "Non-Hindus may have restricted access to certain inner areas",
        ],
        "behavioral_notes": [
            "Shoe removal required — use the shoe counter",
            "Maintain silence and decorum inside the temple",
            "Follow the queue system for darshan (viewing of deity)",
            "Mobile phones must be on silent",
        ],
    },
    {
        "id": "skandagiri_trek",
        "type": "zone",
        "parent_region": "karnataka",
        "dominant_language": "Kannada",
        "cultural_markers": [
            "Skandagiri (also called Kalavara Durga) is a 1,350m hill fortress about 70 km from Bangalore — one of the most popular night treks in South India",
            "Ancient Tipu Sultan-era fort ruins at the summit — stone walls, arched gateways, and a small temple remain from the 18th-century fortification",
            "Famous for its sunrise trek above the clouds — trekkers start at 2-3 AM to reach the peak by dawn and witness a stunning sea of clouds below",
            "The trail passes through scrubland, rocky terrain, and forested patches — the final ascent is steep and requires scrambling over boulders",
        ],
        "legal_rules": [
            "Online booking mandatory through Karnataka Eco Tourism Development Board (Jungle Lodges) — walk-ins are NOT allowed; book at https://www.junglelodges.com or authorized portals",
            "Trek permits are limited to a fixed number per day (typically 100-150 trekkers) — slots fill up fast especially on weekends; book 1-2 weeks in advance",
            "Night trek batches start at specific times (usually 2 AM-4 AM) — latecomers are turned away; arrive at the base at least 30 minutes before your slot",
            "Trekking outside designated trail is prohibited — the area is part of a reserved forest; straying off-path can lead to fines by forest department",
            "Littering is strictly prohibited — carry-in carry-out policy enforced; plastic bottles and food wrappers must be brought back",
            "Campfires and cooking at the summit are not allowed — the fort area is an archaeological and forest-protected zone",
        ],
        "behavioral_notes": [
            "Carry a headlamp or strong flashlight for the night trek — the trail is unlit and has loose rocks; phone flashlights are insufficient",
            "Wear proper trekking shoes with grip — the rocky sections near the summit are slippery especially with morning dew; avoid sports shoes or sandals",
            "Carry at least 2 liters of water per person — there are no water sources on the trail; dehydration is the most common issue",
            "Temperature at the summit can drop to 8-12°C at night even when Bangalore is 20°C — carry a warm layer and windbreaker",
            "The descent is harder on the knees than the climb — take it slow on the rocky sections; trekking poles recommended",
            "Guides provided by the booking authority accompany each batch — follow their instructions; do not attempt the trek without the authorized group",
        ],
    },
    {
        "id": "nandi_hills",
        "type": "zone",
        "parent_region": "karnataka",
        "dominant_language": "Kannada",
        "cultural_markers": [
            "Nandi Hills (Nandidurga) is an ancient hill fortress at 1,478m — just 60 km from Bangalore, it is the city's most popular weekend getaway",
            "Tipu Sultan's Summer Residence (Tipu's Drop) — a cliffside viewpoint from where prisoners were reportedly pushed; now a scenic overlook with panoramic views",
            "Bhoga Nandeeshwara Temple at the base — a 9th-century Chola-era temple dedicated to Lord Shiva, one of Karnataka's oldest functioning temples",
            "Famous for sunrise views — during winter months (October-February) the hills are often above the clouds creating a spectacular sea-of-clouds panorama",
        ],
        "legal_rules": [
            "Entry timing strictly enforced — gates open at 6 AM and close at 6 PM; no overnight stays allowed on the hilltop",
            "Vehicle entry fee: Rs 75 per car, Rs 25 per two-wheeler — parking at the top is limited; during weekends expect long queues from 7 AM onward",
            "Drone flying prohibited within the Nandi Hills area — forest department and district administration enforce the ban",
            "Alcohol and smoking prohibited on the hilltop — the area includes temple grounds and is a family-oriented destination",
            "Speed limit of 20 km/h enforced on the ghat road — 15 hairpin bends with blind curves; overtaking prohibited",
        ],
        "behavioral_notes": [
            "Arrive before 6 AM on weekends to avoid traffic — the single-lane ghat road creates 1-2 hour traffic jams on weekend mornings",
            "Weekday visits are significantly less crowded and more enjoyable — the sunrise experience is the same but without the weekend rush",
            "Cycling up Nandi Hills is popular among Bangalore's cycling community — the 8 km climb averages 6% gradient; start early from the base",
            "Carry your own food and water — there is a small KSTDC canteen at the top but it has limited options and long queues on weekends",
            "Monkeys are aggressive near the food stalls — keep food items in closed bags; do not feed or tease them",
        ],
    },
]


def _build_live_updates():
    now = datetime.now(timezone.utc)
    ttl_short = timedelta(hours=24)
    ttl_medium = timedelta(hours=72)
    ttl_long = timedelta(days=14)

    return [
        {
            "id": "lu_karnataka_dry_day",
            "region_id": "karnataka",
            "category": "legal",
            "severity": "high",
            "summary": "Dry day in Karnataka today due to state holiday. Alcohol sale is prohibited across the state including bars, restaurants, and retail outlets.",
            "source_links": ["https://excise.karnataka.gov.in"],
            "source_type": "government",
            "confidence_score": 0.92,
            "effective_from": now,
            "expires_at": now + ttl_short,
            "last_updated": now,
        },
        {
            "id": "lu_bangalore_metro_green_line_extension",
            "region_id": "bangalore",
            "category": "transport",
            "severity": "low",
            "summary": "Namma Metro Green Line extension to Silk Institute now operational. New stations: Konanakunte Cross, Doddakallasandra, Vajrahalli, Talaghattapura, Silk Institute. Services run 5 AM to 11 PM.",
            "source_links": ["https://english.bmrc.co.in"],
            "source_type": "government",
            "confidence_score": 0.95,
            "effective_from": now - timedelta(days=30),
            "expires_at": now + timedelta(days=120),
            "last_updated": now,
        },
        {
            "id": "lu_bangalore_traffic_orr",
            "region_id": "bangalore",
            "category": "transport",
            "severity": "medium",
            "summary": "Heavy traffic congestion expected on Outer Ring Road (ORR) between Silk Board and Marathahalli due to ongoing metro construction. Diversions in place near Agara Lake and Ibbalur. Use Sarjapur Road or Old Airport Road as alternate routes.",
            "source_links": ["https://btp.gov.in"],
            "source_type": "government",
            "confidence_score": 0.88,
            "effective_from": now,
            "expires_at": now + ttl_long,
            "last_updated": now,
        },
        {
            "id": "lu_bangalore_weather_pleasant",
            "region_id": "bangalore",
            "category": "weather",
            "severity": "low",
            "summary": "Bangalore weather today: Clear skies, temperature 16°C-27°C. Pleasant conditions ideal for outdoor activities. UV index moderate — sunscreen recommended for midday outings. No rain expected this week.",
            "source_links": ["https://mausam.imd.gov.in"],
            "source_type": "government",
            "confidence_score": 0.90,
            "effective_from": now,
            "expires_at": now + ttl_short,
            "last_updated": now,
        },
        {
            "id": "lu_bangalore_water_supply",
            "region_id": "bangalore",
            "category": "safety",
            "severity": "medium",
            "summary": "BWSSB announces scheduled water supply disruption in Whitefield, Mahadevapura, and KR Puram zones due to Cauvery pipeline maintenance. Store water in advance. Normal supply resumes next morning.",
            "source_links": ["https://bwssb.gov.in"],
            "source_type": "government",
            "confidence_score": 0.90,
            "effective_from": now,
            "expires_at": now + timedelta(hours=36),
            "last_updated": now,
        },
        {
            "id": "lu_skandagiri_weekend_slots",
            "region_id": "skandagiri_trek",
            "category": "safety",
            "severity": "medium",
            "summary": "Skandagiri night trek weekend slots are fully booked for this weekend. Next available slots in 1 week. Book via Jungle Lodges website. Weekday slots (Tue-Thu) still available for next week.",
            "source_links": ["https://www.junglelodges.com"],
            "source_type": "government",
            "confidence_score": 0.85,
            "effective_from": now,
            "expires_at": now + ttl_medium,
            "last_updated": now,
        },
        {
            "id": "lu_nandi_hills_weekend_rush",
            "region_id": "nandi_hills",
            "category": "transport",
            "severity": "medium",
            "summary": "Nandi Hills expecting heavy weekend rush. Traffic police will enforce one-way ghat road system from 5 AM to 10 AM on Saturday and Sunday. Arrive before 5:30 AM to avoid 1-2 hour vehicle queues.",
            "source_links": ["https://btp.gov.in"],
            "source_type": "government",
            "confidence_score": 0.82,
            "effective_from": now,
            "expires_at": now + ttl_medium,
            "last_updated": now,
        },
        {
            "id": "lu_bangalore_bbmp_pothole_drive",
            "region_id": "bangalore",
            "category": "transport",
            "severity": "low",
            "summary": "BBMP undertaking pothole-filling drive on major roads including Hosur Road, Bellary Road, and Tumkur Road this week. Expect lane closures during non-peak hours (10 AM-4 PM). Report potholes via BBMP Sahaaya app.",
            "source_links": ["https://bbmp.gov.in"],
            "source_type": "government",
            "confidence_score": 0.80,
            "effective_from": now,
            "expires_at": now + ttl_long,
            "last_updated": now,
        },
        {
            "id": "lu_karnataka_shivaratri",
            "region_id": "karnataka",
            "category": "cultural",
            "severity": "low",
            "summary": "Maha Shivaratri celebrations across Karnataka. Major pujas at Murdeshwar, Gokarna Mahabaleshwar, and Nandi Hills Shiva temple. Expect large crowds at temples, traffic diversions near major temple towns.",
            "source_links": ["https://karnataka.gov.in"],
            "source_type": "government",
            "confidence_score": 0.88,
            "effective_from": now,
            "expires_at": now + ttl_long,
            "last_updated": now,
        },
        {
            "id": "lu_mumbai_train_delay",
            "region_id": "mumbai",
            "category": "transport",
            "severity": "medium",
            "summary": "Western line delays expected due to track maintenance between Andheri and Borivali. Mega block on Sunday from 10 AM to 4 PM. Plan extra 30-45 minutes on weekdays. Use Central or Harbour line alternatives.",
            "source_links": ["https://westernrailway.gov.in"],
            "source_type": "government",
            "confidence_score": 0.85,
            "effective_from": now,
            "expires_at": now + ttl_medium,
            "last_updated": now,
        },
        {
            "id": "lu_mumbai_coastal_road",
            "region_id": "mumbai",
            "category": "transport",
            "severity": "low",
            "summary": "Mumbai Coastal Road (Marine Drive to Worli) now fully operational in both directions. Cuts travel time from South Mumbai to Bandra from 45 min to 12 min during peak hours. No tolls currently. Speed limit 80 km/h.",
            "source_links": ["https://mcgm.gov.in"],
            "source_type": "government",
            "confidence_score": 0.92,
            "effective_from": now - timedelta(days=45),
            "expires_at": now + timedelta(days=120),
            "last_updated": now,
        },
        {
            "id": "lu_delhi_aqi",
            "region_id": "delhi",
            "category": "safety",
            "severity": "medium",
            "summary": "Delhi AQI moderate (150-200) today. Improvement from last week's poor levels. Outdoor exercise advisable only in morning hours (6-8 AM). N95 masks recommended for sensitive individuals. GRAP Stage 1 measures continue.",
            "source_links": ["https://cpcb.nic.in"],
            "source_type": "government",
            "confidence_score": 0.95,
            "effective_from": now,
            "expires_at": now + ttl_short,
            "last_updated": now,
        },
        {
            "id": "lu_delhi_metro_new_line",
            "region_id": "new_delhi",
            "category": "transport",
            "severity": "low",
            "summary": "Delhi Metro Phase IV construction ongoing near Janakpuri West, Maujpur, and Aerocity. Expect traffic diversions and road closures in these areas. DMRC Silver Line (Aerocity-Tughlakabad) testing in progress.",
            "source_links": ["https://delhimetrorail.com"],
            "source_type": "government",
            "confidence_score": 0.88,
            "effective_from": now - timedelta(days=14),
            "expires_at": now + timedelta(days=60),
            "last_updated": now,
        },
        {
            "id": "lu_mysuru_palace_illumination",
            "region_id": "mysuru",
            "category": "cultural",
            "severity": "low",
            "summary": "Mysuru Palace Sunday illumination continues year-round. Palace lit with 97,000 bulbs from 7 PM to 7:45 PM every Sunday. Entry Rs 70 for Indians, Rs 200 for foreigners. Less crowded in February — ideal time to visit.",
            "source_links": ["https://mysorepalace.karnataka.gov.in"],
            "source_type": "government",
            "confidence_score": 0.90,
            "effective_from": now,
            "expires_at": now + timedelta(days=60),
            "last_updated": now,
        },
        {
            "id": "lu_hampi_festival",
            "region_id": "hampi",
            "category": "cultural",
            "severity": "low",
            "summary": "Hampi Utsav (cultural festival) scheduled for early March. Dance, music, and puppet shows at the ruins. Accommodation in Hospet fills up fast — book hotels 2-3 weeks in advance.",
            "source_links": ["https://karnataka.gov.in/tourism"],
            "source_type": "government",
            "confidence_score": 0.78,
            "effective_from": now,
            "expires_at": now + timedelta(days=30),
            "last_updated": now,
        },
    ]


def _get_storage_client(cfg):
    if cfg.TEST_MODE:
        from app.services.local_file_client import LocalFileClient
        return LocalFileClient(cfg)
    else:
        from app.services.firestore_client import FirestoreClient
        return FirestoreClient(cfg)


def seed_all():
    cfg = get_config()
    fs = _get_storage_client(cfg)

    mode = "local file" if cfg.TEST_MODE else "Firestore"
    print(f"  Mode: {mode}")

    region_count = 0
    for region in REGIONS:
        doc_id = region["id"]
        data = {k: v for k, v in region.items() if k != "id"}
        fs.set_document(cfg.COLLECTION_REGIONS, doc_id, data)
        region_count += 1
        print(f"  Seeded region: {doc_id}")

    live_updates = _build_live_updates()
    update_count = 0
    for update in live_updates:
        doc_id = update["id"]
        data = {k: v for k, v in update.items() if k != "id"}
        fs.set_document(cfg.COLLECTION_LIVE_UPDATES, doc_id, data)
        update_count += 1
        print(f"  Seeded live_update: {doc_id}")

    print(f"\nDone. Seeded {region_count} regions and {update_count} live updates.")
    return region_count + update_count


if __name__ == "__main__":
    print("Seeding Firestore...\n")
    try:
        seed_all()
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        print("Make sure GOOGLE_CLOUD_PROJECT and credentials are set in .env", file=sys.stderr)
        sys.exit(1)
