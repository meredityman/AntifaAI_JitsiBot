class Interface:
    def __init__(self, **kwargs):
        pass

    def message(self, user : str, data : dict) -> list:
        raise NotImplementedError()

    def start(self) -> list:
        return []

    def stop(self) -> list:
        return []