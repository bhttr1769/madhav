def handle(user_input):
    if (
        user_input.lower()
        == "hello"
    ):
        print(
            "\nMadhav: "
            "Hello Parth!\n"
        )
        return True

    return False
