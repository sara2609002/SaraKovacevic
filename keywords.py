# PROŠIRENA LISTA KLJUČNIH RIJEČI
TOURISM_KEYWORDS = [
    # Destinacije - osnovni oblici
    "budva", "kotor", "perast", "herceg novi", "bar", "ulcinj", "cetinje", "podgorica", 
    "žabljak", "pljevlja", "tivat", "nikšić", "bijelo polje", "danilovgrad", "plav", 
    "gusinje", "andrijevica", "rožaje",
    
    # Destinacije - morfološke varijante
    "budvu", "budvi", "budvom", "budve",
    "kotoru", "kotora", "kotorem", "kotore",
    "podgoricu", "podgorice", "podgoricom", "podgoricama", "podgorici",
    "herceg novom", "herceg novog", "herceg novim", "herceg nove",
    
    # Prirodne atrakcije
    "skadarsko jezero", "durmitor", "tara", "biogradska gora", "lovćen", "prokletije", 
    "kanjon tiare", "kanjon morače", "ada bojana", "boka kotorska", "rijeka crnojevića", 
    "pavlova strana", "ostrog", "vrmac", "sinjajevina",
    
    # Plaže i more
    "sveti stefan", "svetog stefana", "svetom stefanu", "kraljičina plaža", "miločer", 
    "velika plaža", "sutomore", "petrovac", "buljarica", "jazu", "plavi horizonti",
    
    # Aktivnosti
    "rafting", "hiking", "biciklizam", "ronjenje", "jedrenje", "skijanje", "paraglajding", 
    "kanjoning", "planinarenje", "krstarenje", "posmatranje ptica",
    
    # Gastronomija
    "crnogorska kuhinja", "priganice", "sir", "med", "vino vranac", "riblji specijaliteti", 
    "kačamak", "cicvara", "njeguški pršut", "masline", "riblja čorba",
    
    # Ostalo
    "nacionalni park", "stari grad", "tvrđava", "pećina", "vidikovac", "muzej", 
    "manifestacija", "festival", "tradicija", "folklor", "običaji", "rezervat prirode",
    "restoran", "hotel", "plaža", "atrakcije", "izlet", "aktivnosti", "praktične", 
    "info", "informacije", "praktične info",
]

# BAZA ZNANJA - Detaljne informacije o destinacijama
DESTINATION_DATABASE = {
    'budva': {
        'opis': 'Budva je turistička prestonica Crne Gore, poznata po svojih 35 plaža i bogatom noćnom životu.',
        'atrakcije': [
            'Stari grad Budva (XV vijek) - kameni lavirint sa crkvama i muzejima',
            'Citadela - tvrđava sa spektakularnim pogledom na more',
            'Plaža Mogren - najromantičnija plaža, skrivena između stijena',
            'Plaža Jaz - najveća plaža, idealna za festivale i sport',
            'Slovenska plaža - 2km dugačka gradska plaža sa svim sadržajima'
        ],
        'restorani': [
            'Restoran Jadran (Stari grad) - tradicionalna crnogorska kuhinja',
            'Dukley Beach Lounge - luksuzni restoran sa pogledom na more',
            'Konoba Stari Grad - autentična atmosfera, domaća jela',
            'Restaurant Azzurro - italijanska kuhinja, terasa na moru'
        ],
        'izleti': [
            'Sveti Stefan (15min) - luksuzno ostrvo-hotel',
            'Petrovac (20min) - mirna plaža sa crkvom na stijeni',
            'Skadarsko jezero (1h) - boat tour i degustacija vina',
            'Kotor (45min) - UNESCO baština, fjord i planine'
        ],
        'aktivnosti': [
            'Noćni život - Top Hill, Trocadero, Splendid Casino',
            'Vodeni sportovi - jet ski, parasailing, banana boat',
            'Diving - ronilački centri, podvodne pećine',
            'Shopping - TQ Plaza, lokalni suveniri u Starom gradu'
        ],
        'praktične_info': {
            'parking': 'Javni parking kod Starog grada 2€/sat, besplatan noću',
            'transport': 'Gradski autobus 1€, taksi 5-15€ po gradu',
            'plaže': 'Ležaljke 10-25€/dan, besplatni dijelovi na svakoj plaži',
            'wifi': 'Besplatan u većini kafića i restorana'
        }
    },
    
    'kotor': {
        'opis': 'Kotor je UNESCO baština od 1979, srednjovjekovni grad u najljepšem fjordu Mediterana.',
        'atrakcije': [
            'Stari grad Kotor - lavirint kamenih ulica iz XII vijeka',
            'Tvrđava Sv. Jovana - 1355 stepenica, pogled na Boku Kotorsku',
            'Katedrala Sv. Tripuna - romanička arhitektura, relikvije svetaca',
            'Pomorski muzej - istorija Boke, modeli brodova',
            'Gradske zidine - 4.5km dugačke, najbolje očuvane na Jadranu'
        ],
        'restorani': [
            'Galion - fine dining, pogled na fjord, mediteranska kuhinja',
            'Konoba Scala Santa - skriveni dragulj, domaća pasta',
            'Restoran Bastion - terasa na zidinama, romantična atmosfera',
            'Bokeski Gusti - tradicionalni specijaliteti, lokalni ambijent'
        ],
        'izleti': [
            'Perast i Gospa od Škrpjela (30min) - barokni grad i umjetno ostrvo',
            'Lovćen (1h) - nacionalni park, Njegošev mauzolej',
            'Herceg Novi (30min) - grad stepenica i mimoza',
            'Blue Cave (45min) - boat tour, plavlja pećina'
        ],
        'aktivnosti': [
            'Hiking do tvrđave - 2h uspon, nezaboravan pogled',
            'Kayaking po fjordu - obilazak skrivenih uvala',
            'Cycling - staze oko Boke, rent-a-bike 15€/dan',
            'Boat tours - Perast, Blue Cave, swimming stops'
        ],
        'praktične_info': {
            'parking': 'Van zidina 1€/sat, rezervišite unaprijed ljeti',
            'ulaznice': 'Tvrđava 8€, kombinovana karta za muzeje 15€',
            'najbolje_vrijeme': 'Rano ujutru (7-9h) ili kasno popodne (17-19h)',
            'dress_code': 'Udobna obuća za stepenice, kapa za sunce'
        }
    },
    
    'podgorica': {
        'opis': 'Podgorica je glavni grad Crne Gore, moderni centar sa bogatom kulturom i istorijom.',
        'atrakcije': [
            'Stara Varoš - istorijski dio sa džamijama i starim kućama',
            'Millennium most - moderni simbol grada',
            'Hram Hristovog Vaskrsenja - najveći pravoslavni hram',
            'Ribnica - rijeka kroz centar grada',
            'Gorica brdo - park sa pogledom na grad'
        ],
        'restorani': [
            'Pod Volat - tradicionalna crnogorska kuhinja',
            'Restoran Hemingway - internacionalna kuhinja',
            'Konoba Badanj - lokalni specijaliteti',
            'Restaurant Leonardo - fine dining'
        ],
        'izleti': [
            'Skadarsko jezero (45min) - boat tour, vino',
            'Ostrog manastir (1h) - svetinja u stijeni',
            'Cetinje (45min) - stara prestonica',
            'Lovćen (1.5h) - nacionalni park'
        ],
        'aktivnosti': [
            'Shopping - Delta City, Mall of Montenegro',
            'Noćni život - kafići i klubovi u centru',
            'Kulturni sadržaji - pozorišta, galerije',
            'Sport - stadioni, sportski centri'
        ],
        'praktične_info': {
            'parking': 'Javni parking 1€/sat, garaže 2€/sat',
            'transport': 'Gradski autobus 0.8€, taksi 2-8€',
            'aerodrom': '12km od centra, bus 1€, taksi 15€',
            'wifi': 'Besplatan u centru grada i kafićima'
        }
    },
    
    'herceg novi': {
        'opis': 'Herceg Novi je grad na ulazu u Boku Kotorsku, poznat po bogatoj istoriji, botaničkim baštama i festivalima.',
        'atrakcije': [
            'Kanli Kula - tvrđava iz XV vijeka sa panoramskim pogledom',
            'Forte Mare - primorska tvrđava iz XIV vijeka',
            'Spanjola - austrijska tvrđava iz XIX vijeka',
            'Stari grad - kamene ulice sa venetskim i turskim uticajima',
            'Botanička bašta - mediteranska flora i egzotične biljke'
        ],
        'restorani': [
            'Konoba Feral - tradicionalna kuhinja, svježa riba',
            'Restoran Gradska Kafana - lokalni specijaliteti',
            'Konoba Herceg - autentična atmosfera, domaća vina',
            'Restaurant Jadran - mediteranska kuhinja, terasa na moru'
        ],
        'izleti': [
            'Mamula ostrvo (30min) - istorijska tvrđava na ostrvu',
            'Blue Cave (45min) - boat tour, kristalno plava voda',
            'Kotor (30min) - UNESCO baština, Stari grad',
            'Perast (20min) - barokni grad, Gospa od Škrpjela'
        ],
        'aktivnosti': [
            'Festival mimoza (februar) - proslava dolaska proljeća',
            'Filmski festival (avgust) - međunarodni filmski događaj',
            'Diving - ronilački centri, podvodne atrakcije',
            'Hiking - staze oko Orjena, planinski turizam'
        ],
        'praktične_info': {
            'parking': 'Javni parking u centru 1€/sat, besplatan noću',
            'transport': 'Autobuska stanica, taksi 3-10€ po gradu',
            'plaže': 'Gradska plaža besplatna, privatne plaže 5-15€/dan',
            'wifi': 'Besplatan u kafićima i javnim prostorima'
        }
    }
}

# SEZONSKE KLJUČNE RIJEČI
SEASONAL_KEYWORDS = {
    'ljeto': ['plaža', 'more', 'sunčanje', 'kupanje', 'festival'],
    'zima': ['skijanje', 'snijeg', 'spa', 'wellness', 'kulturni sadržaji'],
    'proljeće': ['hiking', 'planinarenje', 'cvjetanje', 'obilasci'],
    'jesen': ['berba grožđa', 'vino', 'lovstvo', 'priroda']
}

# KLJUČNE RIJEČI PO NAMJERI
INTENT_KEYWORDS = {
    'planning': ['plan', 'itinerar', 'ruta', 'preporuč', 'savjet', 'organizuj'],
    'booking': ['rezerv', 'book', 'hotel', 'smještaj', 'noćenje', 'apartman'],
    'activity': ['aktivnost', 'šta da', 'gdje da', 'kako da', 'zabava'],
    'weather': ['vrijeme', 'kiša', 'sunce', 'temperatura', 'prognoza'],
    'food': ['hrana', 'restoran', 'jelo', 'gastronomija', 'specijalitet']
}
