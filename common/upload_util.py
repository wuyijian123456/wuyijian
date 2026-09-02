from pathlib import Path


def build_upload_file(file_path: str, field_name: str = "file") -> dict:
    """
    构建文件上传参数（用于 requests 上传）

    Args:
        file_path:  本地文件路径
        field_name: 表单字段名（默认 "file"）

    Returns:
        {field_name: (filename, file_object, mime_type)}

    Example:
        files = build_upload_file("data/avatar.png")
        requests.post(url, files=files, headers=headers)
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"上传文件不存在: {path}")

    # 常见 MIME 类型映射
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".pdf": "application/pdf",
        ".txt": "text/plain",
        ".json": "application/json",
        ".csv": "text/csv",
        ".zip": "application/zip",
    }
    mime_type = mime_map.get(path.suffix.lower(), "application/octet-stream")

    return {field_name: (path.name, open(path, "rb"), mime_type)}