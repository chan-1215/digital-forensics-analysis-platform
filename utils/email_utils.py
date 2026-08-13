from email import policy
from email.parser import BytesParser


def _extract_body(message):
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            disposition = part.get_content_disposition()
            if content_type == "text/plain" and disposition != "attachment":
                try:
                    return part.get_content()
                except Exception:
                    payload = part.get_payload(decode=True) or b""
                    return payload.decode(part.get_content_charset() or "utf-8", errors="replace")
        return ""

    try:
        return message.get_content()
    except Exception:
        payload = message.get_payload(decode=True) or b""
        return payload.decode(message.get_content_charset() or "utf-8", errors="replace")


def analyze_eml(path):
    """Parse basic headers, body and attachment metadata from an .eml file."""
    with open(path, "rb") as f:
        message = BytesParser(policy=policy.default).parse(f)

    attachments = []
    for part in message.iter_attachments():
        attachments.append({
            "filename": part.get_filename() or "(unnamed)",
            "content_type": part.get_content_type(),
            "size": len(part.get_payload(decode=True) or b""),
        })

    return {
        "from": message.get("From", ""),
        "to": message.get("To", ""),
        "cc": message.get("Cc", ""),
        "subject": message.get("Subject", ""),
        "date": message.get("Date", ""),
        "message_id": message.get("Message-ID", ""),
        "body": _extract_body(message),
        "attachments": attachments,
    }
