from django import forms
from posts.models import Fantastic, Post, Read, Author
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    title = forms.CharField(required=False, widget=forms.HiddenInput())
    body = forms.CharField(required=False, widget=forms.HiddenInput())
    is_draft = forms.BooleanField(required=False, widget=forms.HiddenInput())
    audio_url = forms.CharField(required=False, widget=forms.TextInput())
    video_url = forms.CharField(required=False, widget=forms.TextInput())

    class Meta:
        model = Post
        fields = (
            "title",
            "body",
            # "slug",
            "written_on",
            "is_draft",
            # "display_type",
            "allow_comments",
            "show_draft_revisions",
            "show_published_revisions",
            "audio_url",
            "video_url",
        )


class FantasticForm(forms.ModelForm):
    on = forms.BooleanField(required=False, widget=forms.HiddenInput())
    reader = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Fantastic
        fields = (
            "on",
        )


class ReadForm(forms.ModelForm):
    reader = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Read
        fields = (
            # "reader",
        )


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=255,
        label='Publication Name',
        help_text="The name your posts will be published under.",
        widget=forms.TextInput(attrs={'placeholder': 'Nom de Plume'}),
    )

    def signup(self, request, user):
        author = Author.objects.get_or_create(user=user)[0]
        if "uuid" in request.session:
            uuid = request.session["uuid"]
            Fantastic.objects.filter(uuid=uuid).update(reader=author)
            Read.objects.filter(uuid=uuid).update(reader=author)

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.save()


class AccountForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=255,
        label='Publication Name',
        help_text="The name your posts will be published under.",
        widget=forms.TextInput(attrs={'placeholder': 'Nom de Plume'}),
    )
    password = forms.CharField(
        max_length=255,
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}),
        required=False
    )

    class Meta:
        model = User
        fields = ("first_name", "email",)

    def save(self):
        if self.cleaned_data['password'] and self.cleaned_data['password'] != "":
            self.instance.set_password(self.cleaned_data['password'])
            self.instance.save()
