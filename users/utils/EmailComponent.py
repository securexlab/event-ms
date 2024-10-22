from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def password_reset_email(url,user_email):
    """
    Send a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    subject = "Password Reset From SecureX-Lab"
    context = {'url': url}
    body = f'Hey, here is the link to reset your password as you requested.'
    html_content = render_to_string('password-reset-email.html', context)
    
    try:
        email = EmailMultiAlternatives(
            subject,
            body,
            from_email='jethalalgada1902@gmail.com',
            to=[user_email],
        )
        email.attach_alternative(html_content, 'text/html') 
        email.send()
        print('Email sent successfully!')
    except Exception as e:
        print(f"An error occurred: {e}")