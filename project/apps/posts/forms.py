from django import forms
from django.contrib.auth.models import User


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=255,
        label='Publication Name',
        help_text="The name your poems will be published under.",
        widget=forms.TextInput(attrs={'placeholder': 'Nom de Plume'}),
    )
    
    def signup(self, request, user):
        poet = Poet.objects.get_or_create(user=user)[0]
        if "uuid" in request.session:
            uuid = request.session["uuid"]
            Fantastic.objects.filter(uuid=uuid).update(reader=poet)
            Read.objects.filter(uuid=uuid).update(reader=poet)

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.save()