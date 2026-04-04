import os
import json
from datetime import datetime
import time

CONTENT_DIR = "data/content_ready"

def check_and_post():
    files = os.listdir(CONTENT_DIR)

    for file in files:
        path = os.path.join(CONTENT_DIR, file)

        with open(path) as f:
            content = json.load(f)

        scheduled_time = datetime.strptime(
            content["scheduled_time"], "%Y-%m-%d %H:%M:%S"
        )

        if datetime.now() >= scheduled_time:
            print("🚀 Posting:", content["caption"])

            os.rename(
                path,
                f"data/content_posted/{file}"
            )

            print("✅ Moved to posted")

while True:
    check_and_post()
    time.sleep(10)