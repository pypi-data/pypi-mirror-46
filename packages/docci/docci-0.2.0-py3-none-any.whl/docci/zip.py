"""
Utils for working with zip archives
"""
import io
from typing import Union, Iterable, Sequence
from zipfile import ZipFile

from docci.file import FileAttachment


def list_zip_files(
    zip_file: Union[str, io.BytesIO, ZipFile, FileAttachment]
) -> Sequence[FileAttachment]:
    """
    List zip archive files
    """

    def zip_file_generator(zip_file: ZipFile) -> Iterable[FileAttachment]:
        for filename in zip_file.namelist():
            content = zip_file.read(filename)
            yield FileAttachment(filename, content)

    if isinstance(zip_file, FileAttachment):
        zip_file = ZipFile(zip_file.content_stream)

    if isinstance(zip_file, (str, io.BytesIO)):
        zip_file = ZipFile(zip_file)

    return list(zip_file_generator(zip_file))
