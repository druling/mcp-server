from src.core.dtos.mcp_context import MCPContext
from src.core.enums.CustomHeader import CustomHeader


def get_mcp_context_header(context: MCPContext):
    if context is None:
        return {}
    return {
        CustomHeader.X_PROFILE_ID.value: context.user_id,
        CustomHeader.X_SECRET_ID.value: context.secret_id,
        CustomHeader.X_ENTITY_ID.value: context.entity_id,
        CustomHeader.X_ENTITY_TYPE.value: context.entity_type,
    }
