from django import forms


class EmailForm(forms.Form):
    """
    Form to send an email to a student
    """

    subject = forms.CharField()
    from_mail = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)