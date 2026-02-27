import json
from typing import Annotated
from pydantic import Field

Output = Annotated[list[str], Field(
    description="JSON-encoded response data from the tool",
    examples=[json.dumps({"key": "value"})]
)]
