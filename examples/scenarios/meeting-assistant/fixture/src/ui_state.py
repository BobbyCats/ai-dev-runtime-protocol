def visible_meeting_cards(meetings: list[dict[str, str]]) -> list[dict[str, object]]:
    cards = []
    for visible_index, meeting in enumerate(meetings, start=1):
        cards.append(
            {
                "card_id": f"card-{visible_index}",
                "meeting_id": meeting["meeting_id"],
                "visible_index": visible_index,
                "title": meeting["title"],
            }
        )
    return cards
