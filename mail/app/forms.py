from django import forms
from .models import EmailSettings, EmailGroup, Emails, EmailMessage

class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = '__all__'

class EmailGroupForm(forms.ModelForm):
    class Meta:
        model = EmailGroup
        fields = '__all__'

class EmailsForm(forms.ModelForm):
    class Meta:
        model = Emails
        fields = '__all__'

class EmailMessageForm(forms.ModelForm):
    class Meta:
        model = EmailMessage
        fields = '__all__'  # Using all fields instead of limited set
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
            'groups': forms.CheckboxSelectMultiple(),
        }