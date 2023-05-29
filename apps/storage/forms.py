from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from apps.storage.models import File, FileShare

User = get_user_model()


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            "file",
        ]

    def save(self, commit: bool = True, *args, **kwargs) -> "File":
        """
        Saves the instance of the File model.

        Args:
            commit (bool): Indicates whether the instance should be saved to the database.

        Returns:
            instance: The instance of the File model that was saved.
        """
        # Get the instance of the File model
        instance: "File" = super().save(commit=False, *args, **kwargs)

        # Process the data or perform any necessary operations
        # For example, you can set the name of the file automatically
        instance.name = instance.file.name

        if commit:
            instance.save()

        return instance


class FileShareForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}), label="User Email"
    )

    class Meta:
        model = FileShare
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError("User with this email does not exist.")
        return user

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.cleaned_data["email"]
        if commit:
            instance.save()
        return instance
