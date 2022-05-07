from django.shortcuts import render
from .forms import ContactForm
from contact.models import Contact
from BabyStore.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMultiAlternatives

# Create your views here.

# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'contact/success.html')
#     form = ContactForm()
#     context = {'form': form}
#     return render(request, 'store/contact.html', context)


def contact(request):
    form = ContactForm()
    if request.POST.get('btnSendMessage'):
        form = ContactForm(request.POST, Contact)
        if form.is_valid():
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.email = form.cleaned_data['email']
            post.phone_number = form.cleaned_data['phone_number']
            post.subject = form.cleaned_data['subject']
            post.message = form.cleaned_data['message']
            post.save()

            msg = EmailMultiAlternatives(post.subject, post.message, EMAIL_HOST_USER, [post.email, 'taphoanamiya.st1@gmail.com'])
            msg.attach_alternative(post.message, 'text/html')
            msg.send()

            return render(request, 'contact/success.html')

    form = ContactForm()
    context = {'form': form}
    return render(request, 'store/contact.html', context)
