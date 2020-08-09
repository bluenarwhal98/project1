from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.urls import reverse 
import re
from . import util
from random import seed, randint


def index(request):

	#if search function used, redirect to result func.
	if request.method == "POST":
		query = str(request.POST['query'])
		return HttpResponseRedirect(reverse('result', args=(query,)))
	#otherwise, a GET call will load the index page
	else:
	    return render(request, "encyclopedia/index.html", {
	        "entries": util.list_entries()
	    })




def entry(request, title):

	entry = util.get_entry(title)
	entry_title = title
	if entry == None:
		listing = []
		entries = util.list_entries()
		for entry in entries:
			if len(re.findall(f"(?:{(entry_title.lower())})+", entry.lower())) >=1:
				listing.append(entry)
			if len(listing) <= 0:
				raise Http404(f"There are no related searches for {entry_title}")
		return HttpResponseRedirect(reverse('result', args=(entry_title,)))

	return render(request, "encyclopedia/entry.html", {"entry": entry, "entry_title": entry_title})


def result(request, query):
	#Check if search query exactly matches an exiting post title
	entry = util.get_entry(query)
	if entry == None:
		#If not, compile a list of post titles that contain the query as a sub-string (case-insensitive)
		listing = []
		entries = util.list_entries()
		for entry in entries:
			if len(re.findall(f"(?:{(query.lower())})+", entry.lower())) >=1:
				listing.append(entry)
		#send error message if there are no related searches
		if len(listing) <= 0:
			raise Http404(f"There are no related searches for {query}")
		#otherwise render the results page
		return render(request, "encyclopedia/result.html", {"listing":listing, "query":query})
	else:
		#if there is a title that matches the search query, redirect to entry func. instead
		return HttpResponseRedirect(reverse('entry', args=(query,)))

def create(request):
	#For accessing page
	if request.method == "GET":
		return render(request, "encyclopedia/create.html")
	else:
	#for creating new posts
		new_title = str(request.POST['title'])
		new_entry = str(request.POST['entry'])

		#check if there is a title and entry

		if new_title == None or new_entry == None:
			raise Http404(f"Please fill in the title and entry before submission!")

		#check if post title already exists
		if util.get_entry(new_title) == True:
			raise Http404(f"{new_title} already exists!")

		#save entry
		util.save_entry(new_title, new_entry)

		return HttpResponseRedirect(reverse('entry', args=(new_title)))

def edit(request, title):
		#If command is GET to access the edit page
		if request.method == "GET":
			entry = util.get_entry(title)
			entry_title = title
			#return HttpResponse(f"hey")
			return render(request, "encyclopedia/edit.html", {"entry":entry, "entry_title":entry_title})

			#return render(request, "encyclopedia/edit.html", {"entrys": entrys, "entrys_title": entrys_title})
		#Else if POST for editing entry
		else:
			edited_entry = str(request.POST['edited'])
			util.save_entry(title, edited_entry)

			return HttpResponseRedirect(reverse('entry', args=(title,)))

def random(request):
	#draw list of current entries
	entries = util.list_entries()
	#generate random number
	seed(1)
	randnum = randint(0,len(entries))
	#select entry
	entry_title = entries[randnum]

	return HttpResponseRedirect(reverse('entry', args=(entry_title,)))









