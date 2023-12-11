from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

import markdown2
from random import choice

from . import util
from . import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": forms.SearchForm()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(content),
            "search_form": forms.SearchForm()
        })
    
    else:
        return render(request, "encyclopedia/error.html", {
            "error": 1,
            "search_form": forms.SearchForm()
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
            "search_form": forms.SearchForm()
        })


    elif request.method == "POST":
        form = forms.SearchForm(request.POST)
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


def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "new_entry_form": forms.NewEntryForm(),
            "search_form": forms.SearchForm()
        })
    
    elif request.method == "POST":
        form = forms.NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                messages.error(request, f"Entry title '{title}' already in use.")
                return render(request, "encyclopedia/new.html", {
                    "new_entry_form": form,
                    "search_form": forms.SearchForm()
                })
            
            content = form.cleaned_data["content"]
            util.save_entry(title, content)

            return HttpResponseRedirect(reverse("index"))
        
        return render(request, "encyclopedia/new.html", {
            "new_entry_form": form,
            "search_form": forms.SearchForm()
        })


def edit(request, entry):
    if request.method == "GET":
        content = util.get_entry(entry)
        form = forms.EditEntryForm({"content": content})

        return render(request, "encyclopedia/edit.html", {
            "title": entry,
            "form": form
        })
    
    elif request.method == "POST":
        form = forms.EditEntryForm(request.POST)

        if form.is_valid():
            util.save_entry(entry, form.cleaned_data["content"])

            return HttpResponseRedirect(reverse("entry", kwargs={"title": entry}))
        
        return render(request, "encyclopedia/edit.html", {
            "title": entry,
            "form": form
        })

def random(request):
    return HttpResponseRedirect(reverse("entry", kwargs={
        "title": choice(util.list_entries())
    }))