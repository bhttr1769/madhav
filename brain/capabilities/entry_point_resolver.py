import importlib


class EntryPointResolver:
    def resolve(
        self,
        entry_point: str,
    ) -> object:
        if not isinstance(entry_point, str):
            raise TypeError(
                "entry_point must be a string"
            )

        if not entry_point.strip():
            raise ValueError(
                "entry_point must not be empty"
            )

        try:
            module_path, attribute_name = (
                entry_point.rsplit(".", 1)
            )
        except ValueError as exc:
            raise ValueError(
                "entry_point must use "
                "'module.path.Attribute' format"
            ) from exc

        if not module_path or not attribute_name:
            raise ValueError(
                "entry_point must use "
                "'module.path.Attribute' format"
            )

        module = importlib.import_module(
            module_path
        )

        try:
            return getattr(
                module,
                attribute_name,
            )
        except AttributeError as exc:
            raise AttributeError(
                f"entry point not found: {entry_point}"
            ) from exc