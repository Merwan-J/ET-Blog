from django.shortcuts import render
from .forms import ContactForm
from .models import Message
from django.shortcuts import reverse,redirect

# Create your views here.


def contact_view(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('contact'))
        else:
            print("#########form not valid") 
            return redirect(reverse('contact'))   

    return render(request,'contact.html',{'form':form})