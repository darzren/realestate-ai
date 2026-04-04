import json
import subprocess
from datetime import datetime

PROMPT_FILE = "prompts/post_prompt.txt"

def run_claude():
    with open(PROMPT_FILE, encoding="utf-8") as f:
        prompt_text = f.read()

    result = subprocess.run(
        ["claude", "-p", "--output-format", "text"],
        input=prompt_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        shell=True
    )
    return result.stdout

def generate_content():
    output = run_claude()

    # Strip markdown code block if present
    output = output.strip()
    if output.startswith("```"):
        output = output.split("```", 2)[1]
        if output.startswith("json"):
            output = output[4:]
        output = output.rsplit("```", 1)[0].strip()

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        print("❌ Failed to parse Claude output")
        print(output)
        return

    content = {
        "id": datetime.now().strftime("%Y%m%d%H%M"),
        "media_path": "media/videos/sample.mp4",
        "scheduled_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "ready",
        **data
    }

    filename = f"data/content_ready/{content['id']}.json"

    with open(filename, "w") as f:
        json.dump(content, f, indent=2)

    print("✅ AI Content created:", filename)

generate_content()