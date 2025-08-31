import os
from openai import OpenAI

class CmdMate:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API")
        if not self.api_key:
            raise ValueError("API key is required. Set it via constructor or environment variable.")
        self.client = OpenAI(api_key=self.api_key)

    def query_command(self, query: str, os_name: str) -> str:
        prompt = f"Operating System: {os_name}\nQuery: {query}"
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are CmdMate, an assistant that converts natural language "
                        "to terminal commands. Respond ONLY with the command, "
                        "no explanations or code blocks. Do not wrap the command in ```bash or ``` blocks."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0
        )
        command = response.choices[0].message.content.strip()
        if command.startswith("```"):
            command = "\n".join(command.splitlines()[1:-1])
        return command
    
    def query_explain(self,query: str) -> str:
        prompt = f"Explain the following : {query}"
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are CmdMate, a helpful assistant. "
                        "Provide clear and concise explanations for user questions. "
                        "Keep responses brief and simple and easy to understand."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0
        )
        explanation = response.choices[0].message.content.strip()
        return explanation
    
# Future features
    # def query_explain
    # def query_commit_help
    # def query_sugest
    # def query_news