import json
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta

NZT = timezone(timedelta(hours=12))  # NZST UTC+12 (Apr-Sep); change to 13 for NZDT (Oct-Mar)

# Fix Windows console encoding for unicode output
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PROMPT_FILE = "prompts/post_prompt.txt"

def run_claude():
    with open(PROMPT_FILE, encoding="utf-8") as f:
        prompt_text = f.read()

    result = subprocess.run(
        "claude -p --output-format text",
        input=prompt_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        shell=True
    )
    return result.stdout

def generate_content():
    output = run_claude()

    # Extract JSON from output — handles preamble text and markdown code blocks
    output = output.strip()
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', output, re.DOTALL)
    if match:
        output = match.group(1)
    else:
        # Try to find a bare JSON object
        match = re.search(r'\{.*\}', output, re.DOTALL)
        if match:
            output = match.group(0)

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        print("FAILED to parse Claude output")
        print(output)
        return

    now = datetime.now(NZT)
    content = {
        "id": now.strftime("%Y%m%d%H%M"),
        "media_path": "media/videos/sample.mp4",
        "scheduled_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "ready",
        **data,
    }

    filename = f"data/content_ready/{content['id']}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)

    print("AI Content created:", filename)
    print("Research:", content["research_summary"])
    print("Angle:", content["content_angle"])

generate_content()
