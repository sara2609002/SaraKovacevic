const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const debugBtn = document.getElementById('debug-btn');
const debugPanel = document.getElementById('debug-panel');
const keywordCount = document.getElementById('keyword-count');
const relevanceScore = document.getElementById('relevance-score');
const currentSeason = document.getElementById('current-season');
const userIntent = document.getElementById('user-intent');

function addMessage(text, sender, data = {}) {
    const msg = document.createElement('div');
    msg.className = 'message ' + sender;
    
    if (sender === 'bot' && data.keywords && data.keywords.length > 0) {
        const keywordsDiv = document.createElement('div');
        keywordsDiv.className = 'keywords-detected-subtle';
        keywordsDiv.innerHTML = `🔍 MonteGuide prepoznao: <span class="keywords-subtle">${data.keywords.join(', ')}</span>`;
        msg.appendChild(keywordsDiv);
        
        keywordCount.textContent = data.keywords.length;
        relevanceScore.textContent = data.relevance_score || 0;
        if (currentSeason) currentSeason.textContent = data.season || '-';
        if (userIntent) userIntent.textContent = data.intent || '-';
        
        if (data.confidence) {
            const confidenceDiv = document.createElement('div');
            confidenceDiv.className = `confidence-indicator confidence-${data.confidence}`;
            confidenceDiv.textContent = data.confidence.toUpperCase();
            msg.appendChild(confidenceDiv);
        }
    }
    
    // Dodaj source indicator
    if (sender === 'bot' && data.source) {
        const sourceDiv = document.createElement('div');
        sourceDiv.className = 'source-indicator';
        const sourceText = data.source === 'openai' ? '🤖 AI odgovor' : '🔍 Trie pretraga';
        sourceDiv.innerHTML = `${sourceText}`;
        msg.appendChild(sourceDiv);
    }
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-content';
    
    if (sender === 'bot') {
        textDiv.innerHTML = formatBotMessage(text, data);
    } else {
        textDiv.textContent = text;
    }
    
    msg.appendChild(textDiv);
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function formatBotMessage(text, data) {
    let formattedText = text;
    
    formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formattedText = formattedText.replace(/• (.*?)(?=\n|$)/g, '<li>$1</li>');
    formattedText = formattedText.replace(/(<li>.*?<\/li>\s*)+/g, function(match) {
        return '<ul class="bot-list">' + match + '</ul>';
    });
    
    formattedText = formattedText.replace(/🎯 \*\*(.*?)\*\*/g, '<h4 class="section-title">🎯 $1</h4>');
    formattedText = formattedText.replace(/🍽️ \*\*(.*?)\*\*/g, '<h4 class="section-title">🍽️ $1</h4>');
    formattedText = formattedText.replace(/🚗 \*\*(.*?)\*\*/g, '<h4 class="section-title">🚗 $1</h4>');
    formattedText = formattedText.replace(/⚡ \*\*(.*?)\*\*/g, '<h4 class="section-title">⚡ $1</h4>');
    formattedText = formattedText.replace(/💡 \*\*(.*?)\*\*/g, '<h4 class="section-title">💡 $1</h4>');
    
    formattedText = formattedText.replace(/\n/g, '<br>');
    
    if (data.keywords && data.keywords.some(kw => ['budva', 'kotor', 'durmitor', 'podgorica', 'herceg novi'].includes(kw))) {
        const destination = data.keywords.find(kw => ['budva', 'kotor', 'durmitor', 'podgorica', 'herceg novi'].includes(kw));
        formattedText += generateActionButtons(destination);
    }
    
    return formattedText;
}

function generateActionButtons(destination) {
    return `
        <div class="action-buttons">
            <button class="action-btn" data-query="${destination} atrakcije">
                🎯 Atrakcije
            </button>
            <button class="action-btn" data-query="${destination} restorani">
                🍽️ Restorani
            </button>
            <button class="action-btn" data-query="${destination} aktivnosti">
                ⚡ Aktivnosti
            </button>
            <button class="action-btn" data-query="${destination} praktične info">
                💡 Praktične info
            </button>
        </div>
    `;
}

function showDebugInfo(debugData) {
    const debugContent = document.getElementById('debug-content');
    let html = `
        <div><strong>Unos:</strong> "${debugData.input}"</div>
        <div><strong>Riječi:</strong> [${debugData.words.join(', ')}]</div>
        <div><strong>Trie pretraga:</strong></div>
    `;
    
    debugData.trie_search_results.forEach(result => {
        const status = result.found_in_trie ? '✅' : '❌';
        html += `<div class="search-path">${status} "${result.word}" - ${result.found_in_trie ? 'PRONAĐENO' : 'NIJE PRONAĐENO'}</div>`;
    });
    
    html += `<div><strong>Finalni rezultat:</strong> [${debugData.found_keywords.join(', ')}]</div>`;
    debugContent.innerHTML = html;
    debugPanel.classList.remove('hidden');
}

// FUNKCIJA ZA SLANJE PORUKE
async function sendMessage(messageText) {
    if (!messageText) return;
    
    addMessage(messageText, 'user');
    addMessage('Analiziram ključne riječi...', 'bot');

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: messageText })
        });
        const data = await response.json();
        
        // Ukloni "loading" poruku
        chatWindow.removeChild(chatWindow.lastChild);
        addMessage(data.answer, 'bot', data);
        
    } catch (error) {
        chatWindow.removeChild(chatWindow.lastChild);
        addMessage('Greška u komunikaciji sa serverom.', 'bot');
    }
}

// EVENT LISTENER ZA FORM
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (!text) return;
    
    userInput.value = '';
    await sendMessage(text);
});

// DEBUG BUTTON
debugBtn.addEventListener('click', async () => {
    const text = userInput.value.trim();
    if (!text) {
        alert('Unesite tekst za debug analizu');
        return;
    }
    
    try {
        const response = await fetch('/debug', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const debugData = await response.json();
        showDebugInfo(debugData);
    } catch (error) {
        alert('Greška u debug analizi');
    }
});

// KLJUČNA IZMJENA - EVENT DELEGATION ZA DUGMIĆE
document.addEventListener('click', function(event) {
    // Provjeri da li je kliknuti element action button
    if (event.target && event.target.classList.contains('action-btn')) {
        console.log('Dugme kliknuto!'); // Za debug
        
        event.preventDefault();
        event.stopPropagation();
        
        const query = event.target.getAttribute('data-query');
        console.log('Query:', query); // Za debug
        
        if (query) {
            // Direktno pozovi sendMessage funkciju
            sendMessage(query);
        }
    }
});

// ZATVARANJE DEBUG PANELA
document.addEventListener('click', (e) => {
    if (debugPanel && !debugPanel.contains(e.target) && e.target !== debugBtn) {
        debugPanel.classList.add('hidden');
    }
});

// POČETNA PORUKA
window.addEventListener('load', function() {
    addMessage('🗺️ Zdravo! Ja sam MonteGuide. Pitajte me o destinacijama u Crnoj Gori kao što su Budva, Kotor, Herceg Novi ili Podgorica.', 'bot');
});
