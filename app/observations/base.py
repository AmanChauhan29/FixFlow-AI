from abc import ABC, abstractmethod


class ObservationHandler(ABC):

    @abstractmethod
    def extract(self, result) -> str:
        """
        Convert raw MCP response into a concise observation.
        """
        raise NotImplementedError