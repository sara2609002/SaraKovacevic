import unicodedata
import re

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.frequency = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.morphology_rules = self._load_morphology_rules()
        self.variant_mapping = {}
    
    def _load_morphology_rules(self):
        return {
            'city_variants': {
                'budva': ['budvu', 'budvi', 'budvom', 'budve'],
                'kotor': ['kotoru', 'kotora', 'kotorem', 'kotore'],
                'podgorica': ['podgoricu', 'podgorice', 'podgoricom', 'podgoricama', 'podgorici'],
                'herceg novi': ['herceg novom', 'herceg novog', 'herceg novim', 'herceg nove'],
                'sveti stefan': ['svetog stefana', 'svetom stefanu', 'sveti stefan']
            },
            'endings': ['om', 'u', 'a', 'e', 'i', 'ima', 'ama', 'ove', 'ih', 'oj', 'em', 'vu', 'vi', 'vom',
                       'uješ', 'uje', 'ujem', 'ujemo', 'ujete', 'uju', 'ći', 'ti', 'iti', 'ati'],
            'prefixes': ['na', 'u', 'iz', 'do', 'od', 'za', 'po', 'pre']
        }
    
    def _normalize_word(self, word):
        normalized = unicodedata.normalize('NFD', word.lower())
        normalized = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
        
        # Posebno mapiranje za česte riječi
        word_mappings = {
            'budvu': 'budva',
            'budvi': 'budva', 
            'budvom': 'budva',
            'kotoru': 'kotor',
            'kotora': 'kotor',
            'kotorom': 'kotor',
            'podgoricu': 'podgorica',
            'podgorice': 'podgorica',
            'podgoricom': 'podgorica',
            'podgorici': 'podgorica',
            'herceg novom': 'herceg novi',
            'herceg novog': 'herceg novi',
            'herceg novim': 'herceg novi',
        }
        
        if normalized in word_mappings:
            return word_mappings[normalized]
        
        # Standardna normalizacija
        for ending in sorted(self.morphology_rules['endings'], key=len, reverse=True):
            if normalized.endswith(ending) and len(normalized) > len(ending) + 2:
                return normalized[:-len(ending)]
        
        return normalized
    
    def insert(self, word):
        # Dodaj osnovnu riječ
        self._insert_word(word.lower())
        
        # Dodaj normalizovanu verziju
        normalized = self._normalize_word(word)
        if normalized != word.lower():
            self._insert_word(normalized)
            self.variant_mapping[normalized] = word.lower()
        
        # Dodaj sve varijante iz morfoloških pravila
        for base_word, variants in self.morphology_rules['city_variants'].items():
            if word.lower() == base_word:
                for variant in variants:
                    self._insert_word(variant)
                    self.variant_mapping[variant] = base_word
    
    def _insert_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.frequency += 1
    
    def search(self, word):
        # Prvo pokušaj direktno
        if self._search_direct(word.lower()):
            return True
        
        # Zatim pokušaj normalizovano
        normalized = self._normalize_word(word)
        return self._search_direct(normalized)
    
    def _search_direct(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def get_search_path(self, word):
        node = self.root
        path = []
        word_lower = word.lower()
        
        for char in word_lower:
            if char not in node.children:
                path.append({"char": char, "found": False})
                return path
            node = node.children[char]
            path.append({"char": char, "found": True})
        
        path.append({"is_complete_word": node.is_end})
        return path
    
    def extract_keywords_advanced(self, text):
        words = re.findall(r'\b\w+\b', text.lower())
        found = set()
        
        # Provjeri pojedinačne riječi
        for word in words:
            if self.search(word):
                original = self._find_original_keyword(word)
                if original:
                    found.add(original)
        
        # Provjeri dvočlane kombinacije (herceg novi, sveti stefan)
        for i in range(len(words) - 1):
            two_word = f"{words[i]} {words[i+1]}"
            if self.search(two_word):
                original = self._find_original_keyword(two_word)
                if original:
                    found.add(original)
        
        return list(found)
    
    def _find_original_keyword(self, word):
        from keywords import TOURISM_KEYWORDS
        
        # Provjeri mapiranje varijanti
        if word in self.variant_mapping:
            return self.variant_mapping[word]
        
        # Direktno mapiranje
        word_mappings = {
            'budvu': 'budva',
            'budvi': 'budva',
            'budvom': 'budva',
            'kotoru': 'kotor',
            'kotora': 'kotor',
            'podgoricu': 'podgorica',
            'podgorice': 'podgorica',
            'podgorici': 'podgorica',
            'herceg novom': 'herceg novi',
            'herceg novog': 'herceg novi',
            'herceg novim': 'herceg novi',
        }
        
        if word in word_mappings:
            return word_mappings[word]
        
        # Standardno traženje
        for keyword in TOURISM_KEYWORDS:
            if self._normalize_word(keyword) == self._normalize_word(word):
                return keyword
            if keyword.lower() == word.lower():
                return keyword
        
        return word
