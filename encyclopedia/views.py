import os 
from django.shortcuts import render
from django import forms
from . import util
from markdown2 import Markdown
import random

markdowner=Markdown()

class Search(forms.Form):
	item = forms.CharField(widget = forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))
class Post(forms.Form):
    title = forms.CharField(label= "Title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')
class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')

def index(request):
	searched= []
	if request.method == 'POST':
		item = request.POST["q"]
		if(item):
			entries = util.list_entries()
			for entry in entries:
				if (entry.lower() == item.lower()): 
					entrydata= util.get_entry(entry)	
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

def dataentry(request, entry):
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

def create(request):
	if request.method == 'POST':
		form = Post(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			textarea = form.cleaned_data["textarea"]
			entries = util.list_entries()
			if title in entries:
				return render(request, "encyclopedia/error.html", {
					"message": "Page already exists."
				})		
			else:
				util.save_entry(title, textarea)
				page = util.get_entry(title)
				page_converted = markdowner.convert(page)
				context = {
					'entry': page_converted,
					'entrytitle': title
				}
				return render(request, "encyclopedia/entries.html", context)
	else:
		return render(request, "encyclopedia/create.html", {
			"post": Post()
		})
def edit(request, title):
	if request.method == 'GET':
		page = util.get_entry(title)
		context = {
            'form': Search(),
            'edit': Edit(initial={'textarea': page}),
            'title': title
        }
		return render(request, "encyclopedia/edit.html", context)
	else:
		form = Edit(request.POST)
		if form.is_valid():
			textarea = form.cleaned_data["textarea"]
			util.save_entry(title, textarea)
			page = util.get_entry(title)
			page_converted = markdowner.convert(page)
			context = {
				'entry': page_converted,
				'entrytitle': title
			}
			return render(request, "encyclopedia/entries.html", context)
def randomPage(request):
	if request.method== 'GET':
		entries = util.list_entries()
		n = random.randint(0, len(entries) - 1 ) # returns a random integer
		page_random = entries[n]
		page = util.get_entry(page_random)
		page_converted = markdowner.convert(page)
		context = {
			'entry': page_converted,
			'entrytitle': page_random
		}
		return render(request, "encyclopedia/entries.html", context)