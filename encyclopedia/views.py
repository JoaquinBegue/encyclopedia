from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
import markdown2

from . import util

class SearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(attrs={
        "class": "search",
        "name": "q",
        "placeholder": "Search Encyclopedia"}))


def index(request):
    form = SearchForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": form
    })

def entry(request, title):
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/entry.html", {"title": title,
                                                           "content": markdown2.markdown(content)})
    else:
        return render(request, "encyclopedia/error.html", {"error": 1})
    
def search(request, q=''):
    if request.method == "GET":

        entries = []
        for entry in util.list_entries():
            if q.upper() in entry.upper():
                entries.append(entry)

        return render(request, "encyclopedia/search.html", {"q": q, "entries": entries})


    elif request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            for entry in util.list_entries():
                if q.upper() == entry.upper():
                    return HttpResponseRedirect(reverse("entry",
                                    kwargs={"title": entry}))
                
            return HttpResponseRedirect(reverse("search",
                                            kwargs={"q": q}))
        
        else:
            return HttpResponseRedirect(reverse("index"))