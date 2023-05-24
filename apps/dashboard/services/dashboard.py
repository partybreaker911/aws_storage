from apps.storage.models import File
from apps.accounts.models import RSAKeyPair


class DashboardService:
    @staticmethod
    def get_files_for_user(user):
        return File.objects.filter(user=user)

    @staticmethod
    def count_files(user):
        return File.objects.filter(user=user).count()

    @staticmethod
    def get_keys_for_user(user):
        return RSAKeyPair.objects.get(user=user)
