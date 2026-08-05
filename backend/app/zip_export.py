import io
import zipfile


def build_zip(index_html: str, filename: str = "index.html") -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, index_html)
    return buf.getvalue()
