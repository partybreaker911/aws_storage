from apps.storage.models import File
from apps.accounts.models import RSAKeyPair


class FileUploadService:
    @classmethod
    def upload_file(cls, user, name, file):
        rsa_key_pair = RSAKeyPair.objects.get(user=user)

        # Create a new File object
        file_obj = File(user=user, name=name, file=file)

        # Save the file object to the database
        file_obj.save()

        return file_obj
