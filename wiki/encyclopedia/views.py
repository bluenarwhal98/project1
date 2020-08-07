from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.urls import reverse 
import re
from . import util


def result(request, query):
	entry = util.get_entry(query)
	if entry == None:
		listing = []
		entries = util.list_entries()
		for entry in entries:
			if len(re.findall(f"(?:{(query.lower())})+", entry.lower())) >=1:
				listing.append(entry)
		if len(listing) <= 0:
			raise Http404(f"There are no related searches for {query}")
		return render(request, "encyclopedia/result.html", {"listing":listing, "query":query})
	else:
		return HttpResponseRedirect(reverse('entry', args=(query,)))
	
		



def index(request):

	if request.method == "POST":
		query = str(request.POST['query'])
		return HttpResponseRedirect(reverse('result', args=(query,)))
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









