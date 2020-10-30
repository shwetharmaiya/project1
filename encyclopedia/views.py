import os 
from django.shortcuts import render

from . import util
from markdown2 import Markdown

def index(request):
	searched= []
	if request.method == 'POST':
		item = request.POST["q"]
		if(item):
			entries = util.list_entries()
			for entry in entries:
				if (entry.lower() == item.lower()): 
					entrydata= util.get_entry(entry)
					markdowner=Markdown()	
					return render(request, "encyclopedia/entries.html", {
						"entry": markdowner.convert(entrydata),
						"entrytitle": entry
					})
				else:
					if item.lower() in entry.lower():
						searched.append(entry)
			return render(request, "encyclopedia/search.html", {
				'searched': searched
			})	
		else:
			return render(request, "encyclopedia/index.html", {
				"entries": util.list_entries()
	    })
	else: 
	    return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries()
	    })

def data(request, entry):
	entries = util.list_entries()
	if entry in entries:
		entrydata= util.get_entry(entry)
		markdowner=Markdown()
		return render(request, "encyclopedia/entries.html", {
			"entry": markdowner.convert(entrydata),
			"entrytitle": entry
		})
	else:
		return render(request, "encyclopedia/error.html", {
			"message": "The requested page was not found"
		})
