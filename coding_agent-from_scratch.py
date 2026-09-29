import inspect
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Any, Tuple
from pathlib import Path

load_dotenv()

openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
SYSTEM_PROMPT = """

"""

YOU_COLOR = "\u001b[94m"
ASSISTANT_COLOR = "\u001b[93m"
RESET_COLOR = "\u001b[0m"

def resolve_abs_path(path_str: str) -> Path:
    path = Path(path_str).expanduser()  # 例如 "~/data/file.txt" → /home/alice/data/file.txt
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return path

def read_file_tool(filename: str) -> Dict[str, Any]:
    []

def list_files_tool(path: str) -> Dict[str, Any]:
    []

def edit_file_tool(path: str, old_str: str, new_str: str) -> Dict[str, Any]:
    return {}

TOOL_REGISTRY = {
    "read_file": read_file_tool,
    "list_files": list_files_tool,
    "edit_file": edit_file_tool
}

def get_tool_str_representation(tool_name: str) -> str:
    return ""

def create_full_system_prompt() -> str:
    return ""

def extract_tool_invocations(text: str) -> List[Tuple[str, Dict[str, Any]]]:
    return []

def execute_llm_call(conversation: List[Dict[str, str]]) -> str:
    return ""

def run_coding_agent_loop():
    pass

if __name__ == "__main__":
    run_coding_agent_loop()