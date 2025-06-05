import os
from flask import Flask, request, jsonify, send_from_directory, session
from trie import Trie
from keywords import TOURISM_KEYWORDS, DESTINATION_DATABASE
from datetime import datetime

# Globalna varijabla za čuvanje razgovora
conversation_memory = {}

try:
    from openai import OpenAI
    # Zamijenite sa vašim API ključem
    client = OpenAI(api_key="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")
    OPENAI_AVAILABLE = True
    print("✓ OpenAI klijent uspješno inicijalizovan")
except Exception as e:
    print(f"❌ OpenAI greška: {e}")
    OPENAI_AVAILABLE = False

app = Flask(__name__, static_folder='static')
app.secret_key = 'monte-guide-secret-key-2024'

# Inicijalizuj Trie
trie = Trie()
for kw in TOURISM_KEYWORDS:
    trie.insert(kw)

def get_or_create_conversation(user_id):
    """Dobij ili kreiraj razgovor za korisnika"""
    if user_id not in conversation_memory:
        conversation_memory[user_id] = {
            'messages': [
                {
                    "role": "system", 
                    "content": """Ti si MonteGuide, turistički vodič za Crnu Goru. 

TVOJA BAZA ZNANJA:
- Budva: turistička prestonica, 35 plaža, Stari grad, Citadela, noćni život
- Kotor: UNESCO baština, fjord, Stari grad, tvrđava Sv. Jovana  
- Podgorica: glavni grad, Millennium most, Stara Varoš
- Herceg Novi: grad stepenica, Kanli Kula, botanička bašta
- Tivat: Porto Montenegro, aerodrom, marina

UDALJENOSTI:
- Podgorica-Budva: 65km (1h)
- Kotor-Budva: 25km (30min)
- Podgorica-Kotor: 90km (1.5h)
- Herceg Novi-Kotor: 30km (30min)
- Tivat-Budva: 20km (25min)

PRAVILA:
1. Odgovaraj na srpskom jeziku
2. Pamti šta je korisnik već pitao i nadovezuj se
3. Za hotele, smještaj, restorane daj konkretne preporuke
4. Fokusiraj se na Crnu Goru
5. Budi prijazan, koristan i informativan
6. Ako korisnik pita o nečemu što si već spomenuo, pozovi se na to"""
                }
            ],
            'created': datetime.now(),
            'last_activity': datetime.now()
        }
    
    conversation_memory[user_id]['last_activity'] = datetime.now()
    return conversation_memory[user_id]

def add_message_to_conversation(user_id, role, content):
    """Dodaj poruku u razgovor"""
    conversation = get_or_create_conversation(user_id)
    conversation['messages'].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    
    # Ograniči na poslednih 25 poruka da ne prekoračimo token limit
    if len(conversation['messages']) > 25:
        conversation['messages'] = [conversation['messages'][0]] + conversation['messages'][-24:]

def get_openai_response_with_memory(user_input, user_id):
    """Koristi OpenAI sa memorijom razgovora"""
    if not OPENAI_AVAILABLE:
        return {
            "answer": "AI sistem trenutno nije dostupan. Pokušajte sa konkretnim pitanjem o destinacijama u Crnoj Gori.",
            "source": "fallback",
            "confidence": "nizak"
        }
    
    try:
        # Dodaj korisničku poruku u memoriju
        add_message_to_conversation(user_id, "user", user_input)
        
        # Dobij kompletnu istoriju razgovora
        conversation = get_or_create_conversation(user_id)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation['messages'],
            max_tokens=500,
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content
        
        # Dodaj AI odgovor u memoriju
        add_message_to_conversation(user_id, "assistant", ai_response)
        
        return {
            "answer": ai_response,
            "source": "openai_with_memory",
            "confidence": "ai_generated"
        }
        
    except Exception as e:
        print(f"OpenAI greška: {e}")
        return {
            "answer": "Izvinjavam se, došlo je do greške sa AI sistemom. Pokušajte ponovo.",
            "source": "error",
            "confidence": "nizak"
        }

def get_destination_info(destination, intent):
    """Vrati informacije o destinaciji iz baze"""
    if destination not in DESTINATION_DATABASE:
        return f"Nemam informacije o destinaciji '{destination}'."
    
    data = DESTINATION_DATABASE[destination]
    
    if 'atrakcije' in intent.lower():
        response = f"🎯 **TOP ATRAKCIJE - {destination.upper()}**\n\n"
        for i, atrakcija in enumerate(data['atrakcije'], 1):
            response += f"{i}. {atrakcija}\n"
        response += f"\n💡 *Pitajte: '{destination} restorani' ili '{destination} aktivnosti'*"
        return response
    
    elif 'restorani' in intent.lower():
        response = f"🍽️ **NAJBOLJI RESTORANI - {destination.upper()}**\n\n"
        for i, restoran in enumerate(data['restorani'], 1):
            response += f"{i}. {restoran}\n"
        response += f"\n💡 *Pitajte: '{destination} atrakcije' ili '{destination} aktivnosti'*"
        return response
    
    elif 'aktivnosti' in intent.lower():
        response = f"⚡ **AKTIVNOSTI - {destination.upper()}**\n\n"
        for i, aktivnost in enumerate(data['aktivnosti'], 1):
            response += f"{i}. {aktivnost}\n"
        response += f"\n💡 *Pitajte: '{destination} restorani' ili '{destination} praktične info'*"
        return response
    
    elif 'praktične' in intent.lower() or 'info' in intent.lower():
        response = f"💡 **PRAKTIČNE INFORMACIJE - {destination.upper()}**\n\n"
        for key, value in data['praktične_info'].items():
            response += f"• **{key.replace('_', ' ').title()}**: {value}\n"
        response += f"\n💡 *Pitajte: '{destination} atrakcije' ili '{destination} restorani'*"
        return response
    
    else:
        # Opšti pregled destinacije
        response = f"🏛️ **{destination.upper()}**\n\n"
        response += f"{data['opis']}\n\n"
        response += "**Top atrakcije:**\n"
        for atrakcija in data['atrakcije'][:3]:
            response += f"• {atrakcija}\n"
        response += f"\n💡 *Pitajte: '{destination} restorani' ili '{destination} aktivnosti'*"
        return response

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    
    # Generiši ili dobij user ID iz session
    if 'user_id' not in session:
        session['user_id'] = f"user_{datetime.now().timestamp()}"
    user_id = session['user_id']
    
    # Prepoznaj ključne riječi
    keywords = trie.extract_keywords_advanced(user_input)
    
    # Mapiranje varijanti na osnovne gradove
    city_mapping = {
        'budvu': 'budva', 'budvi': 'budva', 'budvom': 'budva',
        'kotoru': 'kotor', 'kotora': 'kotor', 'kotorem': 'kotor', 'kotore': 'kotor',
        'podgoricu': 'podgorica', 'podgorice': 'podgorica', 'podgorici': 'podgorica',
        'herceg novim': 'herceg novi', 'herceg novom': 'herceg novi', 'herceg novog': 'herceg novi',
        'tivtu': 'tivat', 'tivta': 'tivat', 'tivtom': 'tivat'
    }
    
    # Normalizuj ključne riječi
    normalized_keywords = []
    for kw in keywords:
        if kw in city_mapping:
            normalized_keywords.append(city_mapping[kw])
        else:
            normalized_keywords.append(kw)
    
    # Pronađi destinaciju
    destinations = [kw for kw in normalized_keywords if kw in DESTINATION_DATABASE]
    
    # HIBRIDNA LOGIKA SA MEMORIJOM
    if destinations and any(word in user_input.lower() for word in ['atrakcije', 'restorani', 'aktivnosti', 'praktične', 'info']):
        # Koristi bazu podataka za specifične zahtjeve o destinacijama
        destination = destinations[0]
        answer = get_destination_info(destination, user_input)
        
        # Dodaj u memoriju
        add_message_to_conversation(user_id, "user", user_input)
        add_message_to_conversation(user_id, "assistant", answer)
        
        return jsonify({
            "answer": answer,
            "keywords": normalized_keywords,
            "confidence": "visok",
            "source": "database_with_memory",
            "intent": "destination_specific",
            "season": "ljeto",
            "keyword_count": len(normalized_keywords),
            "relevance_score": len(normalized_keywords) * 15
        })
    
    elif destinations and len(normalized_keywords) == 1:
        # Opšti pregled destinacije iz baze
        destination = destinations[0]
        answer = get_destination_info(destination, user_input)
        
        # Dodaj u memoriju
        add_message_to_conversation(user_id, "user", user_input)
        add_message_to_conversation(user_id, "assistant", answer)
        
        return jsonify({
            "answer": answer,
            "keywords": normalized_keywords,
            "confidence": "visok",
            "source": "database_with_memory",
            "intent": "destination_overview",
            "season": "ljeto",
            "keyword_count": len(normalized_keywords),
            "relevance_score": len(normalized_keywords) * 15
        })
    
    else:
        # Koristi OpenAI sa memorijom za sve ostalo
        ai_response = get_openai_response_with_memory(user_input, user_id)
        return jsonify({
            "answer": ai_response["answer"],
            "keywords": normalized_keywords,
            "confidence": ai_response["confidence"],
            "source": ai_response["source"],
            "intent": "general_with_memory",
            "season": "ljeto",
            "keyword_count": len(normalized_keywords),
            "relevance_score": len(normalized_keywords) * 5
        })

@app.route("/debug", methods=["POST"])
def debug_trie():
    user_input = request.json.get("message", "")
    words = user_input.lower().split()
    
    debug_info = {
        "input": user_input,
        "words": words,
        "trie_search_results": [],
        "found_keywords": trie.extract_keywords_advanced(user_input),
        "openai_available": OPENAI_AVAILABLE
    }
    
    for word in words:
        exists = trie.search(word)
        debug_info["trie_search_results"].append({
            "word": word,
            "found_in_trie": exists
        })
    
    return jsonify(debug_info)

@app.route("/clear_memory", methods=["POST"])
def clear_memory():
    """Obriši memoriju razgovora"""
    if 'user_id' in session:
        user_id = session['user_id']
        if user_id in conversation_memory:
            del conversation_memory[user_id]
        return jsonify({"status": "Memorija obrisana", "user_id": user_id})
    return jsonify({"status": "Nema aktivne sesije"})

@app.route("/memory_status", methods=["GET"])
def memory_status():
    """Provjeri status memorije"""
    if 'user_id' in session:
        user_id = session['user_id']
        if user_id in conversation_memory:
            conv = conversation_memory[user_id]
            return jsonify({
                "has_memory": True,
                "message_count": len(conv['messages']) - 1,  # -1 jer ne računamo system message
                "created": conv['created'].isoformat(),
                "last_activity": conv['last_activity'].isoformat()
            })
    return jsonify({"has_memory": False})

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    print("🚀 MonteGuide pokrenut na http://127.0.0.1:5000")
    if OPENAI_AVAILABLE:
        print("🤖 OpenAI integracija: AKTIVNA")
        print("💾 Memorija razgovora: AKTIVNA")
    else:
        print("❌ OpenAI integracija: NEAKTIVNA")
    print("-" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)
