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
    print("LFNEJKFNJKL")
    if request.method == "GET":

        entries = []
        for entry in util.list_entries():
            if q.upper() in entry.upper():
                entries.append(entry)

        return render(request, "encyclopedia/search.html", {"q": q, "entries": entries})


    elif request.method == "POST":
        form = forms.Form(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            for entry in util.list_entries():
                if q.upper() == entry.upper():
                    return HttpResponseRedirect(reverse("entry",
                                    kwargs={"title": entry}))
                
            return HttpResponseRedirect(reverse("search",
                                            kwargs={"q": q}))


