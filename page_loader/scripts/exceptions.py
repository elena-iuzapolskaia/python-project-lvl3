class AppInternalError(Exception):
    pass


class BadInputError(AppInternalError):
    pass


class LinkError(AppInternalError):
    pass
