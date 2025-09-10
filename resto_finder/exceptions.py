class CoreBaseError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class LLMCallError(CoreBaseError):
    def __init__(self, *args):
        super().__init__(*args)


class PlacesError(CoreBaseError):
    def __init__(self, *args):
        super().__init__(*args)


class ServiceBaseError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ParseQueryError(ServiceBaseError):
    def __init__(self, *args):
        super().__init__(*args)


class GetPlaceFromFSQError(ServiceBaseError):
    def __init__(self, *args):
        super().__init__(*args)
