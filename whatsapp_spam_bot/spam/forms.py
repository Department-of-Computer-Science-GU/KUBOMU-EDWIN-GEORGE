from django import forms

class MessageForm(forms.Form):
    contact_name = forms.CharField(label='Contact or Group Name', max_length=100)
    message = forms.CharField(label='Message', widget=forms.Textarea)
    num_messages = forms.IntegerField(label='Number of Messages', min_value=1)
