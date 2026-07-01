def classify_memory(text):
    lower = text.lower()

    project_words = [
        "build",
        "building",
        "create",
        "creating",
        "develop",
        "developing",
        "project",
        "working on"
    ]

    for word in project_words:
        if word in lower:
            return "project", 8

    goal_words = [
        "want to become",
        "dream",
        "goal",
        "aspire"
    ]

    for word in goal_words:
        if word in lower:
            return "goal", 9

    preference_words = [
        "favorite",
        "favourite",
        "prefer",
        "like",
        "love"
    ]

    for word in preference_words:
        if word in lower:
            return "preference", 7

    return "general", 5


def reclassify_memories():
    memory = load_memory()

    for item in memory["memories"]:
        category, importance = (
            classify_memory(
                item["text"]
            )
        )

        item["category"] = category
        item["importance"] = importance

    save_memory(memory)
