import json
import os
from datetime import datetime


class Orion:
    def __init__(self):
        with open("config/config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.name = self.config["name"]
        self.memory_file = self.config["memory"]

    def remember(self, message):
        os.makedirs("memory", exist_ok=True)

        data = []

        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r", encoding="utf-8") as f:
                data = json.load(f)

        data.append({
            "date": str(datetime.now()),
            "message": message
        })

        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def status(self):
        return {
            "name": self.name,
            "version": self.config["version"],
            "status": "actif"
        }


if __name__ == "__main__":
    orion = Orion()
    print(orion.status())
    orion.remember("Initialisation du système ORION AI")