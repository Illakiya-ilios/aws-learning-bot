class ShortTermMemory:
    def __init__(self):
        self.store = {}

    def add(self, user_id, role, content):
        if user_id not in self.store:
            self.store[user_id] = []
        self.store[user_id].append({"role": role, "content": content})
        self.store[user_id] = self.store[user_id][-10:]

    def get(self, user_id):
        return self.store.get(user_id, [])

class LongTermMemory:
    def __init__(self):
        self.progress = {}

    def initialize_user(self, user_id, certification):
        self.progress[user_id] = {
            "certification": certification,
            "current_section": None,
            "completed_sections": [],
            "scores": {},
            "weak_topics": [],
            "learning_pace": "normal"
        }

    def update_score(self, user_id, section, score):
        self.progress[user_id]["scores"][section] = score

        if score < 70:
            self.progress[user_id]["weak_topics"].append(section)

    def get(self, user_id):
        return self.progress.get(user_id)
