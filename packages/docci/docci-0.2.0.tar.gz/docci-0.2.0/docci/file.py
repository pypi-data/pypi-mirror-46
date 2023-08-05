"""
Utils for file manipulations like extracting file name from path
"""
import base64
import io
import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Union
from urllib.parse import urlencode


def extract_file_name(path: str) -> str:
    """
    >>> extract_file_name("tests/test_api.py")
    'test_api.py'
    """
    return os.path.basename(path)


@dataclass
class FileAttachment:
    """
    Class for file abstraction
    """

    name: str
    content: bytes = field(repr=False)

    @property
    def name_without_extension(self) -> str:
        """
        >>> FileAttachment("sample.py", b"").name_without_extension
        'sample'
        """
        return self.name.rsplit(".", 1)[0]

    @property
    def extension(self) -> str:
        """
        >>> FileAttachment("sample.py", b"").extension
        'py'
        """
        return self.name.rsplit(".", 1)[-1]

    @property
    def content_stream(self) -> io.BytesIO:
        """Return file attachment content as bytes stream"""
        return io.BytesIO(self.content)

    @property
    def content_base64(self) -> bytes:
        """Convert content to base64 binary string"""
        return base64.b64encode(self.content)

    @property
    def content_disposition(self) -> Dict[str, str]:
        """
        Convert file name to urlencoded Content-Disposition header

        >>> FileAttachment("sample.py", b"").content_disposition
        {'Content-Disposition': 'attachment; filename=sample.py'}
        """
        file_name = urlencode({"filename": self.name})
        return {"Content-Disposition": f'attachment; {file_name}'}

    def save(self, path: Optional[str] = None) -> None:
        """
        Save file to disk
        """
        path = path or self.name
        with open(path, "wb") as f:
            f.write(self.content)

    @classmethod
    def load(cls, path: str) -> 'FileAttachment':
        """
        Load file from disk
        """
        assert os.path.exists(path), f'No such file: "{path}"'
        with open(path, "rb") as f:
            return FileAttachment(extract_file_name(path), f.read())

    @classmethod
    def load_from_base64(cls, base64_str: Union[str, bytes], name: str) -> 'FileAttachment':
        """
        Load file from base64 string
        """
        return FileAttachment(name, base64.b64decode(base64_str))
