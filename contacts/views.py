from django.shortcuts import render
from .forms import ContactForm

def addcontact(request):
    templates = "contact.html"

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

    else:
        form = ContactForm()
    context = {
        'form' : form,
    }
    return render(request, templates, context)
