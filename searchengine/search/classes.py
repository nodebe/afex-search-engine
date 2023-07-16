import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv
from .models import client
from .utils import log_error

load_dotenv()

class SearchEngine:
    def __init__(self, db_name):
        # Connect to DB using the database name
        self.db_name = db_name
        self.db = client[db_name]
    
    def process_indexing(self, document:str):
        try:
            normalized_document = self.normalize_document(document)
            stemmed_document = self.stem_document(normalized_document)

            return stemmed_document
        
        except Exception as e:
            log_error(file='search/classes.py', function='SearchEngine - process_indexing', error=str(e))
            raise Exception

    def tokenize_document(self, document:str):
        tokens = word_tokenize(document)

        return tokens

    def filter_document(self, document:str) -> str:
        '''Remove stopwords like 'in', 'at' from the document'''
        tokens = self.tokenize_document(document)

        stop_words =  set(stopwords.words('english'))
        filtered_tokens = [token for token in tokens if not token in stop_words]
        filtered_document = ' '.join(filtered_tokens)

        return filtered_document
    
    def normalize_document(self, document:str) -> list:
        tokenized_document = self.filter_document(document)
        normalized_document = tokenized_document.lower().split(' ')

        return normalized_document

    def stem_document(self, document:list) -> list:
        stemmer = PorterStemmer()
        stemmed_document = [stemmer.stem(word) for word in document]

        return stemmed_document

class Document(SearchEngine):
    
    def insert_document(self, data:dict, collection_name:str) -> bool:
        '''
        INPUT:
            data: {
                document: str,
                stemmed_document: list,
                date: DateTime
            }
        SUCCESS OUTPUT:
            64b393a098fbcba5d66d1c6e
        FAIL OUTPUT:
            False
        '''
        try:
            self.collection = self.db[collection_name]
            result = self.collection.insert_one(data)

            return True

        except Exception as e:
            log_error(file='search/classes.py', function='Document - insert_document', error=str(e))
            return False

    def query_document(self, keywords:list, collection_name:str) -> list:
        '''Search collection using the keywords'''

        # Build the query using the $in operators
        query = {
            'stemmed_document': {
                '$in': keywords
            }
        }

        try:
            self.collection = self.db[collection_name]
            matching_documents = self.collection.find(query)

            raw_documents = [result['document'] for result in matching_documents]

            return raw_documents

        except Exception as e:
            log_error(file='search/classes.py', function='Document - query_document', error=str(e))
            raise Exception
        
    def rank_documents(self, query:str, corpus:list, n:int) -> list:

        try:
            # Creating our document indexes
            tokenized_corpus = [doc.split(' ') for doc in corpus]
            bm25 = BM25Okapi(tokenized_corpus)

            # Ranking the documents using the passed in query
            tokenized_query = self.tokenize_document(query)
            ranked_documents = bm25.get_top_n(tokenized_query, corpus, n)

            return ranked_documents
        
        except Exception as e:
            log_error(file='search/classes.py', function='Document - rank_documents', error=str(e))
            raise Exception
