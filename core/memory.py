"""Mémoire persistante ORION AI"""
import json
from pathlib import Path
from datetime import datetime

MEMORY_DIR = Path("memory")

class Memory:
    def __init__(self):
        self.short_term = {}
        (MEMORY_DIR / "long_term").mkdir(parents=True, exist_ok=True)
        (MEMORY_DIR / "episodic").mkdir(parents=True, exist_ok=True)

    # ── Court terme (RAM) ──────────────────────
    def remember(self, key: str, value, permanent: bool = False):
        self.short_term[key] = value
        if permanent:
            self._save(key, value)

    def recall(self, key: str):
        if key in self.short_term:
            return self.short_term[key]
        return self._load(key)

    def forget(self, key: str):
        self.short_term.pop(key, None)
        path = MEMORY_DIR / "long_term" / f"{key}.json"
        if path.exists():
            path.unlink()

    # ── Long terme (fichiers JSON) ─────────────
    def _save(self, key: str, value):
        path = MEMORY_DIR / "long_term" / f"{key}.json"
        path.write_text(
            json.dumps({"key": key, "value": value, "updated_at": str(datetime.now())},
                       ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def _load(self, key: str):
        path = MEMORY_DIR / "long_term" / f"{key}.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8")).get("value")
        return None

    # ── Mémoire épisodique (événements) ────────
    def log_event(self, agent_id: str, event: str):
        path = MEMORY_DIR / "episodic" / f"{agent_id}.json"
        events = []
        if path.exists():
            events = json.loads(path.read_text(encoding="utf-8"))
        events.append({"event": event, "timestamp": str(datetime.now())})
        events = events[-50:]  # Garder les 50 derniers
        path.write_text(json.dumps(events, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_events(self, agent_id: str) -> list:
        path = MEMORY_DIR / "episodic" / f"{agent_id}.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return []

    # ── Résumé ─────────────────────────────────
    def summary(self) -> dict:
        long_term = list((MEMORY_DIR / "long_term").glob("*.json"))
        episodic = list((MEMORY_DIR / "episodic").glob("*.json"))
        return {
            "short_term_count": len(self.short_term),
            "long_term_count": len(long_term),
            "episodic_count": len(episodic),
            "agents_in_memory": [f.stem for f in long_term]
        }