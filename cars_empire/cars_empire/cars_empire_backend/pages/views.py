from django.shortcuts import render, get_object_or_404
from .models import InfoPage
from .forms import ContactMessageForm
from django.core.mail import send_mail
from django.conf import settings

# Info page view

def info_page(request, slug):
    page = get_object_or_404(InfoPage, slug=slug, is_active=True)
    return render(request, 'pages/info_page.html', {'page': page})

# Contact Us view

def contact_us(request):
    success = False
    error = None
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            message_obj = form.save()
            # Send email
            try:
                send_mail(
                    subject=f"Contact Us: {message_obj.subject}",
                    message=f"Name: {message_obj.name}\nEmail: {message_obj.email}\n\n{message_obj.message}",
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                    recipient_list=["contact@carsempire.net"],
                    fail_silently=False,
                )
                success = True
            except Exception as e:
                error = str(e)
        else:
            error = "Please correct the errors below."
    else:
        form = ContactMessageForm()
    return render(request, 'pages/contact_us.html', {'form': form, 'success': success, 'error': error})
