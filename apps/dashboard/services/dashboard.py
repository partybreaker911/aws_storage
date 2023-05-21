from apps.storage.models import File


class DashboardService:
    @staticmethod
    def get_files_for_user(user):
        return File.objects.filter(user=user)

    @staticmethod
    def count_files(user):
        return File.objects.filter(user=user).count()
