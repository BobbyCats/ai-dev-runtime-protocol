ENTRYPOINT = "meeting.delete"


def build_delete_plan(selection_id: str) -> dict[str, str]:
    return {
        "entrypoint": ENTRYPOINT,
        "selection_id": selection_id,
        "intent": "delete meeting by user-selected card",
    }


def delete_selected_meeting(selection_id: str, visible_cards: list[dict[str, object]], store) -> dict[str, str]:
    """BUG: this executor resolves by visible_index instead of stable meeting_id."""
    card = next(card for card in visible_cards if card["card_id"] == selection_id)
    deleted = store.delete_by_index(int(card["visible_index"]))
    return {"deleted_meeting_id": deleted["meeting_id"], "selection_id": selection_id}
