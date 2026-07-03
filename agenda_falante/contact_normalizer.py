from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable


def normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", name).strip()


def normalize_phone(phone: str) -> str:
    cleaned = re.sub(r"\D+", "", phone)
    if cleaned.startswith("55") and len(cleaned) > 11:
        cleaned = cleaned[2:]
    if len(cleaned) == 10:
        cleaned = "55" + cleaned
    elif len(cleaned) == 11 and not cleaned.startswith("55"):
        cleaned = "55" + cleaned
    return "+" + cleaned if cleaned else ""


def split_first_last_name(full_name: str) -> tuple[str, str]:
    cleaned = normalize_name(full_name)
    if not cleaned:
        return "", ""
    parts = cleaned.split(" ")
    first_name = parts[0]
    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
    return first_name, last_name


def normalize_contacts(contacts: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    normalized: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for contact in contacts:
        full_name = normalize_name(str(contact.get("full_name", "")))
        if not full_name:
            continue
        first_name, last_name = split_first_last_name(full_name)
        phones: list[str] = []
        for phone in contact.get("phones", []):
            normalized_phone = normalize_phone(str(phone))
            if normalized_phone and normalized_phone not in phones:
                phones.append(normalized_phone)
        emails = []
        for email in contact.get("emails", []):
            cleaned = normalize_name(str(email)).lower()
            if cleaned and cleaned not in emails:
                emails.append(cleaned)
        organization = normalize_name(str(contact.get("organization", "")))
        source = str(contact.get("source", ""))
        digest = hashlib.sha1(
            "|".join([source.lower(), full_name.lower(), ",".join(phones), ",".join(emails), organization.lower()]).encode(
                "utf-8"
            )
        ).hexdigest()
        if digest in seen_ids:
            continue
        seen_ids.add(digest)
        normalized.append(
            {
                "contact_id": digest,
                "full_name": full_name,
                "first_name": first_name,
                "last_name": last_name,
                "phones": phones,
                "emails": emails,
                "organization": organization,
                "source": source,
            }
        )
    return normalized
