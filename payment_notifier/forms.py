from django import forms
from .models import *

class MessageForm(forms.ModelForm):

    attach_pdf = forms.BooleanField(widget = forms.CheckboxInput,required=False)

    class Meta:

        model = Message
        fields = ('message_text',)

    def clean_message_text(self):
        message_text = self.cleaned_data.get('message_text')
        if message_text == "" or message_text == None:
            raise forms.ValidationError("message cannot be empty")
     
        return message_text


class UserNamesForm(forms.Form):

    usernames = forms.CharField(widget = forms.Textarea,help_text = "Enter the Names of users seperated by commas")
    group_no = forms.CharField(help_text = "required")
    
    def clean_usernames(self):
        usernames = self.cleaned_data.get('usernames').split(',')

        for username in usernames:
            if not userDetails.objects.filter(name=username).exists():
                raise forms.ValidationError(username+" doesn't exist in database")       
        return usernames


