from django.shortcuts import render
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact_us/contact.html', {
                'form': form,
                'success': True  # Pass success flag to template
            })
    else:
        form = ContactForm()
    return render(request, 'contact_us/contact.html', {'form': form})
