from abc import ABC, abstractmethod
from instructor import OpenAISchema
from typing import Any

class BaseTool(ABC, OpenAISchema):
    @abstractmethod
    async def run(self):
        pass
    
    async def execute(self, args_str: str):
        """
        Executes the tool with the provided arguments.
        """
        args = self.model_validate_json(args_str)
        return await args.run()
    
    # Remove "title" field for all tools parameters
    class Config:
        @staticmethod
        def json_schema_extra(schema: dict[str, Any], model: type['BaseTool']) -> None:
            for prop in schema.get('properties', {}).values():
                prop.pop('title', None)