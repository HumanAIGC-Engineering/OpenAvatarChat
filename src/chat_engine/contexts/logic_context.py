from chat_engine.contexts.common_module_context import CommonModuleContext


class LogicContext(CommonModuleContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
