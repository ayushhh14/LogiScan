import json
from pathlib import Path

from models.schemas import LogisticsDocument


def save_json(
    data: LogisticsDocument,
    output_path: str
) -> None:
    """
    Save structured document information as JSON.
    """

    path = Path(output_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data.model_dump(),
            file,
            indent=4,
            ensure_ascii=False
        )