# pdf_labeler.py

from llm_openrouter import query_mistral
import json
import re


def create_markdown_prompt(content: str) -> str:
    return f"""
Label the following PDF content using markdown-style tags.

Use this format:
# Title: ...
## Subtitle: ...
**Paragraph:** ...
- Bullet: ...
> Reference: ...

Rules:
- Do NOT wrap in markdown code blocks like ```json
- Do NOT explain anything
- Do NOT output JSON or YAML
- Bullet points (•, o, -) should be converted to "- Bullet: ..."

Content:
\"\"\"
{content}
\"\"\"
"""

def label_pdf_content_markdown(text: str) -> str:
    prompt = create_markdown_prompt(text)
    response = query_mistral(prompt)
    return response.strip()
