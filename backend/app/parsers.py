import re, json, datetime as dt
from pathlib import Path
from typing import List, Dict
from pdfminer.high_level import extract_text

# WhatsApp regex
WA_RE = re.compile(
    r"^\[(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})\] (.*?): (.*)$"
)

def parse_pdf(path: Path) -> List[Dict]:
    text = extract_text(str(path))
    # naive split per page using form feed char
    slides = text.split("\f")
    out = []
    for idx, slide in enumerate(slides, 1):
        if slide.strip():
            out.append(
                {
                    "text": slide.strip(),
                    "metadata": {"source": "pdf", "slide": idx, "file": path.name},
                }
            )
    return out

def parse_whatsapp(path: Path) -> List[Dict]:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            m = WA_RE.match(line)
            if not m:
                continue
            date_str, time_str, author, msg = m.groups()
            try:
                ts = dt.datetime.strptime(date_str + " " + time_str, "%d/%m/%y %H:%M")
            except ValueError:
                continue
            out.append(
                {
                    "text": msg.strip(),
                    "metadata": {
                        "source": "whatsapp",
                        "author": author,
                        "ts": ts.isoformat(),
                        "line": line_no,
                        "file": path.name,
                    },
                }
            )
    return out
