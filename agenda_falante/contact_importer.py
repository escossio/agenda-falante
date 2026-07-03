from __future__ import annotations

import hashlib
import csv
import re
from pathlib import Path
from typing import Iterable


def _unfold_vcard_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw_line in text.splitlines():
        if raw_line.startswith((" ", "\t")) and lines:
            lines[-1] += raw_line[1:]
        else:
            lines.append(raw_line)
    return lines


def _parse_vcard_properties(lines: Iterable[str]) -> dict[str, list[str]]:
    props: dict[str, list[str]] = {}
    for line in lines:
        if not line or line.startswith("BEGIN:") or line.startswith("END:"):
            continue
        if ":" not in line:
            continue
        key_part, value = line.split(":", 1)
        key = key_part.split(";", 1)[0].strip().upper()
        props.setdefault(key, []).append(value.strip())
    return props


def _split_name_parts(full_name: str) -> tuple[str, str, str]:
    cleaned = re.sub(r"\s+", " ", full_name).strip()
    if not cleaned:
        return "", "", ""
    parts = cleaned.split(" ")
    first_name = parts[0]
    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
    return cleaned, first_name, last_name


def _stable_contact_id(source: str, name: str, phones: list[str], emails: list[str], organization: str) -> str:
    payload = "|".join(
        [
            source.strip().lower(),
            name.strip().lower(),
            ",".join(phones),
            ",".join(emails),
            organization.strip().lower(),
        ]
    )
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def import_vcf(path: str | Path) -> list[dict[str, object]]:
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    contacts: list[dict[str, object]] = []
    card_lines: list[str] = []
    in_card = False
    for line in _unfold_vcard_lines(text):
        if line.strip().upper() == "BEGIN:VCARD":
            in_card = True
            card_lines = [line]
            continue
        if in_card:
            card_lines.append(line)
        if line.strip().upper() == "END:VCARD" and in_card:
            props = _parse_vcard_properties(card_lines)
            full_name = props.get("FN", [""])[0]
            phones = [v for v in props.get("TEL", []) if v.strip()]
            emails = [v for v in props.get("EMAIL", []) if v.strip()]
            organization = props.get("ORG", [""])[0]
            if not full_name.strip():
                in_card = False
                continue
            cleaned_name, first_name, last_name = _split_name_parts(full_name)
            contact = {
                "source": "vcf",
                "full_name": cleaned_name,
                "first_name": first_name,
                "last_name": last_name,
                "phones": phones,
                "emails": emails,
                "organization": organization.strip(),
            }
            contact["contact_id"] = _stable_contact_id(
                contact["source"],
                contact["full_name"],
                contact["phones"],
                contact["emails"],
                contact["organization"],
            )
            contacts.append(contact)
            in_card = False
    return contacts


def import_csv(path: str | Path) -> list[dict[str, object]]:
    with Path(path).open(encoding="utf-8", errors="ignore", newline="") as handle:
        reader = csv.DictReader(handle)
        contacts: list[dict[str, object]] = []
        for row in reader:
            full_name = (
                row.get("full_name")
                or row.get("display_name")
                or row.get("nome")
                or row.get("name")
                or ""
            ).strip()
            if not full_name:
                continue
            phones: list[str] = []
            for key, value in row.items():
                if key is None or value is None:
                    continue
                normalized_key = key.strip().lower()
                if normalized_key in {"phone", "phone_number", "telefone"} or normalized_key.startswith("phone_") or normalized_key.startswith("telefone_"):
                    cleaned = value.strip()
                    if cleaned:
                        phones.append(cleaned)
            emails: list[str] = []
            for key, value in row.items():
                if key is None or value is None:
                    continue
                normalized_key = key.strip().lower()
                if normalized_key in {"email", "email_address"} or normalized_key.startswith("email_"):
                    cleaned = value.strip()
                    if cleaned:
                        emails.append(cleaned)
            organization = (row.get("organization") or row.get("empresa") or "").strip()
            cleaned_name, first_name, last_name = _split_name_parts(full_name)
            contact = {
                "source": "csv",
                "full_name": cleaned_name,
                "first_name": first_name,
                "last_name": last_name,
                "phones": phones,
                "emails": emails,
                "organization": organization,
            }
            contact["contact_id"] = _stable_contact_id(
                contact["source"],
                contact["full_name"],
                contact["phones"],
                contact["emails"],
                contact["organization"],
            )
            contacts.append(contact)
    return contacts
