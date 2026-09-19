import json
from pathlib import Path

from typing import Any
import boto3
from botocore.exceptions import ClientError


def detect_file_text() -> None:
    client = boto3.client("textract")

    file_path = str(Path(__file__).parent / "images" / "lista.jpeg")
    with open(file_path, "rb") as f:
        document_bytes = f.read()

    try:
        response = client.detect_document_text(Document={"Bytes": document_bytes})
        with open("response.json", "w") as response_file:
            response_file.write(json.dumps(response))
    except ClientError as e:
        print(f"Erro processando documento: {e}")


def get_lines() -> list[str]:
    try:
        with open("response.json", "r") as f:
            data = json.loads(f.read())
            blocks = data["Blocks"]
        return [block["Text"] for block in blocks if block["BlockType"] == "LINE"]  # type: ignore
    except IOError:
        detect_file_text()
    return []


if __name__ == "__main__":
    for line in get_lines():
        print(line)