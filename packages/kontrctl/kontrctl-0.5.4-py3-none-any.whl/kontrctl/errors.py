import click


class KontrCtlError(click.ClickException):
    pass


class ResourceNotFoundError(KontrCtlError):
    def __init__(self, collection_name: str, name: str):
        super().__init__(f"Cannot find resource in {collection_name} with identifier: {name}")


class RemoteNotSetError(KontrCtlError):
    def __init__(self):
        super().__init__(f"Remote is not set.")


class ContentNotChangedError(KontrCtlError):
    def __init__(self):
        super(ContentNotChangedError, self).__init__("Content was not edited - no update")


class LoginNotSuccessfulError(KontrCtlError):
    def __init__(self):
        super(LoginNotSuccessfulError, self).__init__("Login was not successful")
