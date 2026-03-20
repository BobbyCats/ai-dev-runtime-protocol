from calendar_agent import build_delete_plan, delete_selected_meeting
from event_store import EventStore
from ui_state import visible_meeting_cards


def main() -> str:
    store = EventStore(
        [
            {"meeting_id": "meeting-1", "title": "Roadmap Review"},
            {"meeting_id": "meeting-2", "title": "Design Critique"},
            {"meeting_id": "meeting-3", "title": "Hiring Sync"},
        ]
    )
    cards = visible_meeting_cards(store.items)
    plan = build_delete_plan(selection_id="card-2")
    result = delete_selected_meeting(selection_id="card-2", visible_cards=cards, store=store)
    return f"{plan['entrypoint']} -> {result['deleted_meeting_id']}"


if __name__ == "__main__":
    print(main())
