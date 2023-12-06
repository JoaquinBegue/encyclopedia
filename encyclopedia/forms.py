from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(attrs={
            "class": "search",
            "name": "q",
            "placeholder": "Search Encyclopedia"
        }))
    
class NewEntryForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
            "class": "title-input",
            "name": "title",
            "placeholder": "Title"
            }))
    
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
            "class": "content-input",
            "name": "content",
            "placeholder": "Page content (formatted in markdown)"
        }))
    
class EditEntryForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
            "class": "content-input",
            "name": "content",
            "placeholder": "Page content (formatted in markdown)"
        }))