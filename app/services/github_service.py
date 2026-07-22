from abc import ABC, abstractmethod


class GitHubService(ABC):
    """
    Defines the business capabilities our AI agent expects from GitHub.

    This interface hides all MCP implementation details from the rest
    of the application.
    """

    @abstractmethod
    async def download_workflow_logs(
        self,
        owner: str,
        repository: str,
        run_id: int,
    ):
        """
        Download workflow logs.
        """
        pass

    @abstractmethod
    async def get_workflow_run(
        self,
        owner: str,
        repository: str,
        run_id: int,
    ):
        """
        Get workflow information.
        """
        pass

    @abstractmethod
    async def get_repository_file(
        self,
        owner: str,
        repository: str,
        path: str,
    ):
        """
        Read a repository file.
        """
        pass

    @abstractmethod
    async def create_branch(
        self,
        owner: str,
        repository: str,
        branch_name: str,
    ):
        """
        Create a new branch.
        """
        pass

    @abstractmethod
    async def update_file(
        self,
        owner: str,
        repository: str,
        path: str,
        content: str,
        message: str,
    ):
        """
        Update a repository file.
        """
        pass

    @abstractmethod
    async def create_pull_request(
        self,
        owner: str,
        repository: str,
        title: str,
        body: str,
        head: str,
        base: str,
    ):
        """
        Create a pull request.
        """
        pass

    @abstractmethod
    async def rerun_workflow(
        self,
        owner: str,
        repository: str,
        run_id: int,
    ):
        """
        Re-run a workflow.
        """
        pass

    # async def get_workflow_details(self, payload: dict):
    #     """
    #     Extract workflow information from webhook payload.
    #     """

    #     workflow_run = payload.get("workflow_run", {})

    #     return {
    #         "run_id": workflow_run.get("id"),
    #         "workflow_name": workflow_run.get("name"),
    #         "status": workflow_run.get("status"),
    #         "conclusion": workflow_run.get("conclusion"),
    #     }