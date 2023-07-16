from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DocumentForm, QueryForm
from .classes import Document
from datetime import datetime as dt

# Create your views here.
def index_document(request):
    form = DocumentForm()
    if request.method == 'POST':
        try:
            form = DocumentForm(request.POST)

            if form.is_valid():
                document = form.cleaned_data['document']

                # Creating a Document object to perform various methods on data gotten
                search_engine = Document('searchengineafex')
                stemmed_document = search_engine.process_indexing(document)

                # Store data in DB
                data = {
                    'document': document,
                    'stemmed_document':  stemmed_document,
                    'date': dt.now()
                }
                store_data = search_engine.insert_document(data=data, collection_name='documents')

                if store_data == False:
                    messages.error(request, 'Document not stored successfully!')
                else:
                    messages.success(request, 'Document has been indexed and is ready for searching!')
            
            else:
                messages.warning(request, 'Input not filled properly!')
        
        except Exception as e:
            messages.warning(request, 'An Error Occured!')
    
    context = {
        'form': form
    }

    return render(request, 'index.html', context=context)

def search_documents(request):
    form = QueryForm()
    if request.method == 'POST':
        try:
            form = QueryForm(request.POST)

            if form.is_valid():
                query = form.cleaned_data['query']

                # Creating a Document object to perform various methods on data gotten
                search_engine = Document('searchengineafex')
                stemmed_query = search_engine.process_indexing(query)

                # Search data in DB
                search_data = search_engine.query_document(keywords=stemmed_query, collection_name='documents')
                if len(search_data) == 0:
                    messages.info(request,'No matching document found with the given keyword/phrase!')
                    return redirect('/')
                
                # Rank results
                documents = search_data
                rank = search_engine.rank_documents(query=query, corpus=documents, n=len(documents))

                context = {
                    'form': form,
                    'documents': rank
                }
                
                return render(request, 'search.html', context=context)
                
        except Exception as e:
            messages.warning(request, 'An Error Occured!')
    
    context = {
        'form': form
    }
    return render(request, 'search.html', context=context)