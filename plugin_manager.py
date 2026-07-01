import os
import importlib


PLUGINS = []


def load_plugins():
    plugins_dir = "plugins"

    for file in os.listdir(plugins_dir):
        if (
            file.endswith(".py")
            and file != "__init__.py"
        ):
            module_name = (
                file[:-3]
            )

            module = (
                importlib.import_module(
                    f"plugins.{module_name}"
                )
            )

            PLUGINS.append(module)


load_plugins()


def handle_plugins(
    user_input
):
    for plugin in PLUGINS:
        try:
            handled = (
                plugin.handle(
                    user_input
                )
            )

            if handled:
                return True

        except Exception as e:
            print(
                f"\nPlugin error "
                f"({plugin.__name__}): "
                f"{e}\n"
            )

    return False
