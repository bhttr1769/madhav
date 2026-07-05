_last_action = None


def set_action(
    action_type,
    data
):
    global _last_action

    _last_action = {
        "type": action_type,
        "data": data
    }


def get_action():
    return _last_action


def clear():
    global _last_action
    _last_action = None