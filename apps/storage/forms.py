from django import forms

from apps.storage.models import File


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
