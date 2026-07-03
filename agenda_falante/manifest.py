from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def build_contacts_manifest(contacts: Iterable[dict[str, object]]) -> dict[str, object]:
    items = []
    for contact in contacts:
        items.append(
            {
                "contact_id": contact["contact_id"],
                "full_name": contact["full_name"],
                "first_name": contact["first_name"],
                "last_name": contact["last_name"],
                "phones": contact["phones"],
                "emails": contact["emails"],
                "organization": contact["organization"],
                "source": contact.get("source", ""),
            }
        )
    return {"manifest_type": "contacts_normalized", "contacts": items}


def write_contacts_manifest(manifest: dict[str, object], path: str | Path) -> None:
    Path(path).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

