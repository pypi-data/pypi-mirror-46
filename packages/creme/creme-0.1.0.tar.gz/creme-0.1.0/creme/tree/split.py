import abc


class Splitter(abc.ABC):

    @abc.abstractmethod
    def __call__(self) -> bool:
        """Returns a `bool` indicating to go left or right."""
