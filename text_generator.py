import json

def generate_text(name: str, date: str, segment: str, content: str) -> str:
    return (
        f"Good day, everyone! This is {name}, your news reporter. Today is {date}. "
        f"Coming up next, we have a special segment: {segment}. "
        f"{content}. "
        f"Thank you for watching. This is your news reporter signing off."
    )

def load_config(filepath: str = "config.json") -> dict:
    with open(filepath, "r") as file:
        return json.load(file)

config = load_config()

text = generate_text(name=config["speaker_info"]["name"],
                    date=config["content_info"]["date"],
                    segment=config["content_info"]["segment"],
                    content=config["content_info"]["content"])
