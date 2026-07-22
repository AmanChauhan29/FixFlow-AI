
from app.observations.action_get import ActionsGetObservationHandler


class ObservationRegistry:

    def __init__(self):
        self.handlers = {
            "actions_get": ActionsGetObservationHandler()
        }

    def register(
        self,
        tool_name,
        handler
    ):
        self.handlers[tool_name] = handler

    def get(
        self,
        tool_name
    ):
        return self.handlers.get(tool_name)