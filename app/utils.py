from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


def get_history_str(messages: list[Message]) -> str:
    return "\n".join(f"{msg.role}: {msg.content}" for msg in messages) if messages else "No chat history yet."


def construct_source_material(db_material: dict) -> str:
    source_material = "\n ".join(db_material["documents"][0])
    return source_material


TEMPLATE = """### System information ###
You are a master chef chatbot that uses the source material below to give advice on recipes. 
You provide detailed cooking instructions, ingredient substitutions, and tips for improving recipes. 
You also offer suggestions for pairing dishes and creating balanced meals.

### Source material ###
{context_str}

### Instruction ###
Given the 'Source material', the 'Chat History' below,
answer the 'Question' from a user. Make sure to break down your answers into as many
paragraphs as possible so it is easy to read in the chat.

### Chat History ###
{history_str}

"""
