from django.db import models
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage as DjangoEmailMessage
from django.conf import settings  


class EmailSettings(models.Model):
    email_host = models.CharField(max_length=255, default='smtp.gmail.com')
    email_port = models.IntegerField(default=587)
    email_use_tls = models.BooleanField(default=True)
    email_host_user = models.EmailField(default='mohmmedshaker69@gmail.com')
    email_host_password = models.CharField(default='qwjs resc ecdg bcxu', max_length=255)
    default_from_email = models.EmailField(default='mohmmedshaker69@gmail.com')

    class Meta:
        db_table = "shared_mail_setting"

    def save(self, *args, **kwargs):

        if self.pk is None and EmailSettings.objects.exists():
            raise ValidationError("Only one instance of EmailSettings can exist.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email_host_user
    



class EmailGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "shared_mail_group"

    def __str__(self):
        return self.name
    

class Emails(models.Model):
    email_group = models.ForeignKey(EmailGroup, on_delete=models.CASCADE)
    email = models.TextField()




class EmailMessage(models.Model):
    groups = models.ManyToManyField(EmailGroup, related_name='email_messages')  
    subject = models.CharField(max_length=255)
    attachment = models.FileField(upload_to='email_attachments/', null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='email_photos/', null=True, blank=True)  

    def __str__(self):
        
        return self.subject

    def send_email(self):
        # Get email settings
        email_settings = EmailSettings.objects.first()
        if not email_settings:
            raise ValueError("Email settings not configured")
        print(f"Using settings: {email_settings.email_host_user}")

        # Dynamically update Django email settings
        settings.EMAIL_HOST = email_settings.email_host
        settings.EMAIL_PORT = email_settings.email_port
        settings.EMAIL_USE_TLS = email_settings.email_use_tls
        settings.EMAIL_HOST_USER = email_settings.email_host_user
        settings.EMAIL_HOST_PASSWORD = email_settings.email_host_password

        # Get all recipient emails from related groups
        recipients = []
        for group in self.groups.all():
            group_emails = Emails.objects.filter(email_group=group)
            recipients.extend([email.email.strip() for email in group_emails])
        recipients = list(set(recipients))  # Remove duplicates
        print(f"Recipients: {recipients}")

        if not recipients:
            raise ValueError("No recipients found for this message")

        # Send a separate email to each recipient
        for recipient in recipients:
            # Create email message for this recipient
            email_message = DjangoEmailMessage(
                subject=self.subject,
                body=self.text or '',
                from_email=email_settings.default_from_email,
                to=[recipient]  # Only one recipient per email
            )
            
            if self.attachment:
                print(f"Attaching file: {self.attachment.path} for {recipient}")
                email_message.attach_file(self.attachment.path)
            
            print(f"Sending email to {recipient}...")
            email_message.send(fail_silently=False)