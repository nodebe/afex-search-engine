from django import forms

class DocumentForm(forms.Form):
    document = forms.CharField(widget=forms.Textarea(attrs = {'placeholder':'Enter Document ...'}), label=False)

class QueryForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Search Query ...'}), label=False)