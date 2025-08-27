# imghdr.py
# بسيط ويفحص ترويسة الملفات لتحديد نوع الصورة (jpeg, png, gif, bmp, tiff, webp)

def _read_header(fh):
    try:
        if hasattr(fh, "read"):
            pos = fh.tell() if hasattr(fh, "tell") else None
            data = fh.read(32)
            if pos is not None:
                try:
                    fh.seek(pos)
                except Exception:
                    pass
            return data
        else:
            with open(fh, "rb") as f:
                return f.read(32)
    except Exception:
        return b""

def what(file, h=None):
    """
    file: ملف أو مسار أو كائن قابل للقراءة
    h: بيانات رأسية يمكن إرسالها مباشرة لتسريع الفحص
    """
    if h is None:
        h = _read_header(file)
    if not h:
        return None
    if isinstance(h, str):
        h = h.encode('latin-1', errors='ignore')

    # JPEG
    if h.startswith(b'\xff\xd8'):
        return "jpeg"
    # PNG
    if h.startswith(b'\x89PNG\r\n\x1a\n'):
        return "png"
    # GIF
    if h[:6] in (b'GIF87a', b'GIF89a'):
        return "gif"
    # BMP
    if h.startswith(b'BM'):
        return "bmp"
    # TIFF (little/big endian)
    if h.startswith(b'II*\x00') or h.startswith(b'MM\x00*'):
        return "tiff"
    # WEBP (RIFF....WEBP)
    if len(h) >= 12 and h.startswith(b'RIFF') and h[8:12] == b'WEBP':
        return "webp"
    return None
