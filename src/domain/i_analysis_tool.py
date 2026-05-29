from abc import ABC, abstractmethod

class IAnalysisTool(ABC):

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def analyze(self, project_path: str, github_repo: str, dependencies: list) -> dict:
        pass