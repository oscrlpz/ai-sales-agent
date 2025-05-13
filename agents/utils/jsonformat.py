import json


def json_to_dict(response: str) -> dict:
    """Convert the response string to a JSON object.

    Args:
        response (str): The response string to convert.

    Returns:
        dict: The converted JSON object.
    """
    response = response.replace("'", '"')
    response = response.replace("\n", "")
    response = response.replace(" ", "")
    # if ```json is present, remove it and the closing ```
    if response.startswith("```json"):
        response = response[7:]
    if response.endswith("```"):
        response = response[:-3]
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON: {e}")
