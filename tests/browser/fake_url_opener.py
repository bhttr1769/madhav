class FakeResponse:

    def __init__(self):

        self.status = 200

    def read(self):

        return b"""
        <html>
            <body>
                Hello Madhav
            </body>
        </html>
        """

    def __enter__(self):

        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):

        pass


class FakeUrlOpener:

    def open(
        self,
        url,
    ):

        return FakeResponse()