import zipfile
from pathlib import Path


class Archivation:
    def create_archive(self, source_file_path: Path, archive_file_path: Path) -> None:
        """
        Creates a new archive from a source file.

        :param source_file_path: The path to the source file to be archived.
        :param archive_file_path: The path to the archive file to be created.
        """
        with zipfile.ZipFile(archive_file_path, "w") as zipf:
            zipf.write(source_file_path, arcname=source_file_path.name)
