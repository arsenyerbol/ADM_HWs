import pandas as pd
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from string import punctuation
from nltk.corpus import stopwords
from IPython.core.display import display, HTML

import json


def detect_stable(s):
    if type(s) == str:
        try:
            l = detect(s)
            return l
        except LangDetectException as e:
            return None
    else:
        return None
    

class SearchEngine:
    
    def __init__(self, 
                 stemmer, 
                 tokenizer, 
                 drop_stopwords=True, 
                 drop_punctuation=True, 
                 stopwordset=None, 
                 vocabulary=None):
        self.stemmer = stemmer
        self.tokenizer = tokenizer
        self.drop_stopwords = drop_stopwords
        self.drop_punctuation = drop_punctuation
        if stopwordset is None:
            from nltk.corpus import stopwords
            self.stopwordset = set(stopwords.words())
            
        if self.drop_stopwords:
            from nltk.corpus import stopwords
            self.stopwordset = set(stopwords.words())
            
        if vocabulary is None:
            self.vocabulary = {}
        else:
            self.vocabulary = vocabulary
            
        self.data_filename = None
    
    def add_to_vocab(self, plot_tokens, book_id):
        for token in plot_tokens:
            i = self.vocabulary.get(token)
            if i is None:
                self.vocabulary[token] = [book_id]
            if i is not None:
                self.vocabulary[token].append(book_id)
        return True
    
    
    def build_inverted_index(self, data_filename):
        self.data_filename = data_filename
        df = pd.read_csv(data_filename, sep='\t', error_bad_lines=False)
        df = df.dropna(subset=['bookTitle', 'bookId', 'url'])
        df['lang'] = df['Plot'].apply(detect_stable)
        df = df[df['lang'] == 'en']
        df['Plot_tokens'] = df['Plot'].apply(self.nlp_processor)
        isok = df.apply(lambda x: self.add_to_vocab(x['Plot_tokens'], x['bookId']), axis=1).all()
        return isok, df
        
    def nlp_processor(self, x):
        x = x.translate(str.maketrans('', '', punctuation))
        if self.drop_stopwords:
            tokens = [self.stemmer.stem(w.lower()) for w in self.tokenizer(x) if w.lower()
                      not in self.stopwordset]
        else:
             tokens = [self.stemmer.stem(w.lower()) for w in self.tokenizer(x)]           
        
        return tokens
    
    
    def conjunctive_search(self, query):
        if len(self.vocabulary.keys()) < 1:
            raise Exception("Index not initialized. use build_inverted_index method.")
        tokens = self.nlp_processor(query)
        first = True
        for t in tokens:
            if first:
                results = set(self.vocabulary[t])
                first = False
            else:
                results = results.intersection(set(self.vocabulary[t]))
        return results

    def render_results(self, results, at_k=5, query=None):
        
        if self.data_filename is None:
            raise Exception("Index not initialized. No data filename provided")
        
        res = list(results['bookId']) + [0]
        
        df = pd.read_csv(self.data_filename, 
                         sep='\t', 
                         error_bad_lines=False, 
                         skiprows=lambda x: x not in res, 
                         usecols=['url', 'bookTitle', 'Plot']
                        )
        
        
        serp = df[:at_k]
        
        if query is None:
            for ind in range(at_k):
                s = serp.iloc[ind]
                r = results.iloc[ind]
                display(HTML(f"""<h3><a href="{s["url"]}" target="_blank">{s["bookTitle"]}</a></h3>
                <p>Book Id: <a href="{s["url"]}" target="_blank">{r['bookId']:.0f}</a></p>
                <p>{self.replace_with_italic(s["Plot"], self.nlp_processor(query))}</p>"""))  
        else:
            for ind in range(at_k):
                s = serp.iloc[ind]
                r = results.iloc[ind]
                
                if 'sim' in results.columns:
                    cosine_str = f"<p>Cosine score: {r['sim']*100:.2f}</p>"
                else:
                    cosine_str = ""
                
                display(HTML(f"""<h3><a href="{s["url"]}" target="_blank">{s["bookTitle"]}</a></h3>
                <p>Book Id: <a href="{s["url"]}" target="_blank">{r['bookId']:.0f}</a></p>
                {cosine_str}
                <p>{self.replace_with_italic(s["Plot"], self.nlp_processor(query))}</p>"""))
                
    def replace_with_italic(self, s, tokens):
        for t in tokens:
            s = (s
                 .replace(t, f'<i style="background-color: #000000; color: #ffff00">{t}</i>')
                 .replace(t.capitalize(), f'<i style="background-color: #000000; color: #ffff00">{t.capitalize()}</i>'))
        return s
        
    
    def dump_vocab(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.vocabulary, f)
            
    def load_vocab(self, filename):
        with open(filename, 'r') as f:
            self.vocabulary = json.load(f)
            
    def add_data_fname(self, fname):
        self.data_filename = fname
