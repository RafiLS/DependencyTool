from typing import Type, List
from src.domain.i_analysis_tool import IAnalysisTool

class ToolRegistry:

    _tools: List[Type[IAnalysisTool]] = []

    @classmethod
    def register(cls, tool_class: Type[IAnalysisTool]):
        cls._tools.append(tool_class)
        return tool_class

    @classmethod
    def get_all(cls) -> List[IAnalysisTool]:
        return [tool_class() for tool_class in cls._tools]