from enum import Enum


class EventType(str, Enum):
    """
    All event types supported by the Store Intelligence platform.
    """

    ENTRY = "ENTRY"
    EXIT = "EXIT"
    REENTRY = "REENTRY"

    ZONE_ENTER = "ZONE_ENTER"
    ZONE_EXIT = "ZONE_EXIT"
    ZONE_DWELL = "ZONE_DWELL"

    BILLING_QUEUE_JOIN = "BILLING_QUEUE_JOIN"
    BILLING_QUEUE_ABANDON = "BILLING_QUEUE_ABANDON"