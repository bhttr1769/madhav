
import os
import importlib


PLUGINS = []
PLUGIN_STATUS = {}


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

            PLUGIN_STATUS[
                module_name
            ] = True


load_plugins()


def handle_plugins(
    user_input
):
    for plugin in PLUGINS:

        module_name = (
            plugin.__name__
            .split(".")[-1]
        )

        if not PLUGIN_STATUS.get(
            module_name,
            True
        ):
            continue

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


def get_plugins():
    return (
        PLUGIN_STATUS.copy()
    )


def enable_plugin(
    name
):
    if name in PLUGIN_STATUS:
        PLUGIN_STATUS[name] = True
        return True

    return False


def disable_plugin(
    name
):
    if name in PLUGIN_STATUS:
        PLUGIN_STATUS[name] = False
        return True

    return False
