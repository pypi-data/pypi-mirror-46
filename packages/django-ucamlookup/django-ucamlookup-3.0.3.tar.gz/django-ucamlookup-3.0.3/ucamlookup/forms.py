from django import forms
from django.contrib.auth.models import User


class UserCreationForm(forms.ModelForm):  # noqa: F811
    username = forms.RegexField(label="Username", max_length=30, regex=r'^[a-z][a-z0-9]{3,7}$', help_text="Required.",
                                error_messages={'invalid': "Invalid crsid format"})

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            "A user with that username already exists.",
            code='duplicate_username',
        )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user
