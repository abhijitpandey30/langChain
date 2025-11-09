# handlers/chat_model_start_handler.py
from langchain.callbacks.base import BaseCallbackHandler
from pyboxen import boxen


class ChatModelStartHandler(BaseCallbackHandler):
    """Custom callback that prints out chat messages when a ChatModel starts."""

    def on_chat_model_start(
        self,
        serialized,
        messages,
        *,
        run_id,
        parent_run_id=None,
        tags=None,
        metadata=None,
        **kwargs,
    ):
        print("\n\n\n======== Sending Messages ========\n")
        if not messages or not isinstance(messages, list):
            print("⚠️  No messages to display.")
            return

        # messages is a list of message lists; we take the first
        for message in messages[0]:
            msg_type = getattr(message, "type", "unknown")
            content = getattr(message, "content", "")

            # System message
            if msg_type == "system":
                boxen_print(content, title="System", color="yellow")

            # Human user message
            elif msg_type == "human":
                boxen_print(content, title="Human", color="green")

            # Model deciding to call a tool
            elif msg_type == "ai" and "function_call" in getattr(
                message, "additional_kwargs", {}
            ):
                call = message.additional_kwargs["function_call"]
                tool_name = call.get("name", "unknown_tool")
                args = call.get("arguments", "")
                boxen_print(
                    f"Running tool `{tool_name}` with args: {args}",
                    title="AI (function call)",
                    color="cyan",
                )

            # Model output (normal AI text)
            elif msg_type == "ai":
                boxen_print(content, title="AI", color="blue")

            # Function output
            elif msg_type == "function":
                boxen_print(content, title="Function", color="purple")

            # Fallback
            else:
                boxen_print(content, title=msg_type.capitalize(), color="gray")


def boxen_print(*args, **kwargs):
    """Prints a nicely formatted box to the console."""
    print(boxen(*args, **kwargs))
