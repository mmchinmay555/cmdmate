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
    
    def query_explain(self, query: str) -> str:
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
                        "Avoid any formatting like code blocks or markdown."
                        "Just the plain text explanation. And keep the explaination well within 100-150 words."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0
        )
        explanation = response.choices[0].message.content.strip()
        return "\n"+explanation+"\n"
    
    def query_getCommit(self, git_diff: str) -> list[str]:
        prompt = f"Git diff:\n{git_diff}"
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are CmdMate, a git commit message assistant. "
                        "Given a git diff, generate exactly 3 concise one-liner commit messages in past tense (e.g., 'Added', 'Implemented', 'Fixed') "
                        "Write them in plain text only. "
                        "Each must start with '- ' and be on its own line. "
                        "Do NOT wrap them in [ ], do NOT use quotes, and do NOT separate with commas. "
                        "Correct format:\n"
                        "- First commit message\n"
                        "- Second commit message\n"
                        "- Third commit message"
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.3
        )
        commit_messages = response.choices[0].message.content.strip().split('\n')
        commit_messages = [msg.strip() for msg in commit_messages if msg.strip()][:3]

        return "\nSample commit messages\n\n" + "\n".join(commit_messages)+"\n"
    
    def query_response_from_input(self, input: str, query: str) -> str:
        prompt = (
            f"Based on the following input, respond to the user's query:\n\n"
            f"Input:\n{input}\n\n"
            f"Query:\n{query}"
        )
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are CmdMate, a helpful assistant."
                        "Provide clear and concise responses for user questions."
                        "Keep responses brief, simple, and easy to understand."
                        "Avoid formatting like code blocks, quotes, or markdown."
                        "Also avoid this ** formatting."
                        "Just plain text responses."
                        "Keep the response well within 100-150 words."
                        "Only exceed 150 words if absolutely necessary, and never go above 300 words."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0
        )

        response = response.choices[0].message.content.strip()
        return "\n"+response+"\n"
    
# Future features
    # def query_explain
    # def query_commit_help
    # def query_sugest
    # def query_news