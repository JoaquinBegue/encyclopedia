from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
import markdown2
from random import choice
from . import util

class SearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(attrs={
            "class": "search",
            "name": "q",
            "placeholder": "Search Encyclopedia"
        }))
    
class NewPageForm(forms.Form):
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


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(content),
            "search_form": SearchForm()
        })
    
    else:
        return render(request, "encyclopedia/error.html", {
            "error": 1,
            "search_form": SearchForm()
        })
    

def search(request, q=''):
    if request.method == "GET":

        entries = []
        for entry in util.list_entries():
            if q.upper() in entry.upper():
                entries.append(entry)

        return render(request, "encyclopedia/search.html", {
            "q": q,
            "entries": entries,
            "search_form": SearchForm()
        })


    elif request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            for entry in util.list_entries():
                if q.upper() == entry.upper():
                    return HttpResponseRedirect(reverse("entry", kwargs={
                        "title": entry
                    }))
                
            return HttpResponseRedirect(reverse("search", kwargs={
                "q": q
            }))
        
        else:
            return HttpResponseRedirect(reverse("index"))


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html", {
            "new_page_form": NewPageForm(),
            "search_form": SearchForm()
        })
    
    elif request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            if form.cleaned_data["title"] in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "error": 2
                })
            
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
        
        return render(request, "encyclopedia/new_page.html", {
            "new_page_form": form,
            "search_form": SearchForm()
        })
    



def random(request):
    return HttpResponseRedirect(reverse("entry", kwargs={
        "title": choice(util.list_entries())
    }))