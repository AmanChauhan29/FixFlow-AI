from app.observations.base import ObservationHandler


class ActionsGetObservationHandler(ObservationHandler):

    def extract(self, result) -> str:
        raise NotImplementedError