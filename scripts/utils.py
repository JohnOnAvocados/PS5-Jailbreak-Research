from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Iterable

ROOT = Path(".")
INBOX = ROOT / "inbox"
INTERMEDIATE = ROOT / "intermediate"
GRAPH = ROOT / "graph"
WIKI = ROOT / "wiki"
OBSIDIAN = ROOT / "obsidian" / "vault"
REPORTS = ROOT / "reports"

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "are", "was", "were",
    "into", "than", "then", "them", "they", "their", "about", "have",
    "has", "had", "can", "could", "should", "would", "will", "when", "where",
    "what", "which", "who", "whom", "whose", "how", "why", "also", "but", "not",
    "use", "used", "using", "over", "under", "between", "within", "each", "all",
    "any", "may", "might", "must", "more", "most", "less", "very", "some",
    "such", "via", "per", "out", "up", "down", "on", "off", "in", "of", "to",
    "a", "an", "is", "it", "as", "at", "by", "be", "or", "if", "we", "you",
    "i", "our", "your", "its"
}

LAYER_KEYWORDS = {
    "boot_chain": {"boot", "secure boot", "chain of trust", "root of trust", "loader", "signed boot"},
    "firmware": {"firmware", "update", "patch", "pup", "resilience", "integrity measurement"},
    "hardware": {"hardware", "cpu", "gpu", "memory", "storage", "motherboard", "psp"},
    "cpu_architecture": {"amd", "zen", "arm", "trustzone", "el0", "el1", "el2", "el3", "architecture"},
    "hypervisor": {"hypervisor", "virtualization", "vm", "isolation", "guest"},
    "kernel": {"kernel", "syscall", "lsm", "module", "privilege", "scheduler"},
    "memory_protection": {"aslr", "cfi", "stack", "heap", "overflow", "memory safety", "protection"},
    "threat_modeling": {"stride", "attacker", "threat", "risk", "mitre", "owasp"},
    "security_model": {"security", "trust", "verification", "isolation", "confidential"},
    "system_overview": {"overview", "architecture", "system", "platform"},
}

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()

def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\t ]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def strip_html(text: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return normalize_whitespace(text)

def extract_urls(text: str) -> list[str]:
    return re.findall(r'https?://[^\s)\]}>]+', text)

def extract_wikilinks(text: str) -> list[str]:
    return re.findall(r"\[\[(.+?)\]\]", text)

def title_from_text(text: str) -> str:
    for line in text.splitlines():
        line = line.strip("# ").strip()
        if line:
            return line[:120]
    return "Untitled"

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_") or "untitled"

def first_sentences(text: str, max_sentences: int = 3) -> str:
    parts = re.split(r"(?<=[.!?])\s+", normalize_whitespace(text))
    return " ".join(parts[:max_sentences]).strip()

def tokenize(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_\-]{2,}", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 2]

def top_concepts(text: str, limit: int = 12) -> list[str]:
    counts = {}
    for tok in tokenize(text):
        if tok.isdigit():
            continue
        counts[tok] = counts.get(tok, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [k for k, _ in ranked[:limit]]

def classify_layer(text: str) -> str:
    tl = text.lower()
    scored = {}
    for layer, keywords in LAYER_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in tl:
                score += 1
        scored[layer] = score
    best = max(scored, key=scored.get)
    return best if scored[best] > 0 else "system_overview"

def jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 0.0
    return len(sa & sb) / max(1, len(sa | sb))

def safe_json_dump(path: Path, payload) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
