import json
from typing import Annotated
from pydantic import Field

Output = Annotated[list[str], Field(
    description="JSON-encoded response data from the tool",
    examples=[json.dumps({"key": "value"})]
)]


def mcp_output(description: str = "JSON-encoded response data from the tool", examples: list[str] = None) -> type[Output]:
    """
    Factory function to create an Output type with custom description and examples.

    Args:
        description: A description of the output data.
        examples: A list of example JSON strings representing the output.

    Returns:
        A new Output type with the specified description and examples.
    """
    return Annotated[list[str], Field(description=description, examples=examples or [])]
