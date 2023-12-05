from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
            if q in entry:
                entries.append(entry)
        
        return render(request, "encyclopedia.html", {"q": q, "entries": entries})