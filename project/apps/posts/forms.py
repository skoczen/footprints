from django import forms
from posts.models import Fantastic, Post, Read, Author
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    title = forms.CharField(required=False, widget=forms.HiddenInput())
    body = forms.CharField(required=False, widget=forms.HiddenInput())
    is_draft = forms.BooleanField(required=False)
    
    class Meta:
        model = Post
        fields = (
            "title",
            "body",
            # "slug",
            # "published",
            "written_on",
            "is_draft",
            # "display_type",
            "dayone_image",
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

class SocialShareForm(forms.ModelForm):
    publish_now = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        model = Post
        fields = (
            "twitter_status_text",
            "facebook_status_text",
            "twitter_publish_intent",
            "facebook_publish_intent",
            "twitter_include_image",
            "publish_now",
            "email_publish_intent",
        )


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=255,
        label='Publication Name',
        help_text="The name your posts will be published under.",
        widget=forms.TextInput(attrs={'placeholder': 'Nom de Plume'}),
    )

    def signup(self, request, user):
        print "signup"
        author = Author.objects.get_or_create(user=user)[0]
        print author
        if "uuid" in request.session:
            uuid = request.session["uuid"]
            Fantastic.objects.filter(uuid=uuid).update(reader=author)
            Read.objects.filter(uuid=uuid).update(reader=author)

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.save()
            
class BlogForm(forms.ModelForm):
    blog_name = forms.CharField(
        max_length=255,
        label='Blog Name',
        help_text="The name of your blog. This will show up in page titles and google results.",
        widget=forms.TextInput(attrs={'placeholder': 'Adventures in Awesome'}),
    )
    blog_domain = forms.CharField(
        max_length=255,
        label='Blog Domain',
        help_text="Your domain, i.e. blog.inkandfeet.com.  You don't need the 'http://' part.",
        widget=forms.TextInput(attrs={'placeholder': 'blog.myawesomesite.com'}),
    )
    redirects = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Author
        fields = ("blog_name", "blog_domain", "blog_header", "blog_footer")

class BlogUserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=255,
        label='Publication Name',
        help_text="The name your posts will be published under.",
        widget=forms.TextInput(attrs={'placeholder': 'Nom de Plume'}),
    )

    class Meta:
        model = User
        fields = ("first_name",)

class AccountForm(forms.ModelForm):
    
    password = forms.CharField(
        max_length=255,
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}),
        required=False
    )

    class Meta:
        model = User
        fields = ("email", )

    def save(self):
        if self.cleaned_data['password'] and self.cleaned_data['password'] != "":
            self.instance.set_password(self.cleaned_data['password'])
            self.instance.save()

