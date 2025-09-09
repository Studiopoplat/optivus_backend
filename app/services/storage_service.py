import uuid
from fastapi import UploadFile
from app.utils.supabase_client import supabase

async def upload_to_supabase(file: UploadFile, folder="kyc"):
    file_ext = (file.filename or "file").split(".")[-1]
    file_name = f"{folder}/{uuid.uuid4()}.{file_ext}"

    content = await file.read()

    res = supabase.storage.from_("documents").upload(
        file_name,
        content,
        {"cacheControl": "3600", "upsert": False}
    )

    if isinstance(res, dict) and res.get("error"):
        raise Exception(f"Supabase upload failed: {res['error']}")

    public_url = supabase.storage.from_("documents").get_public_url(file_name)
    return public_url

