class EventStore:
    def __init__(self, items: list[dict[str, str]]) -> None:
        self.items = list(items)

    def delete_by_index(self, visible_index: int) -> dict[str, str]:
        return self.items.pop(visible_index - 1)

    def delete_by_meeting_id(self, meeting_id: str) -> dict[str, str]:
        for index, item in enumerate(self.items):
            if item["meeting_id"] == meeting_id:
                return self.items.pop(index)
        raise KeyError(meeting_id)

    def get_titles(self) -> list[str]:
        return [item["title"] for item in self.items]
