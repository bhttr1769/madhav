LINE = "─" * 30


def line():
    print(LINE)


def section(
    title
):
    print()
    line()
    print(title.upper())
    line()
    print()


def success(
    message
):
    print(f"✓ {message}")


def error(
    message
):
    print(f"✗ {message}")


def warning(
    message
):
    print(f"⚠ {message}")


def info(
    message
):
    print(f"ℹ {message}")


def blank():
    print()