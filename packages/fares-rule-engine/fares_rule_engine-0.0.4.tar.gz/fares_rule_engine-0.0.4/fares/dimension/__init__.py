from fares.dimension.dimension import SlotDimensions, UserDimensions


def resolve_slot_dimensions(slot):
    return {
        "slot.od_cluster_session": (
            slot[SlotDimensions.ORIGIN_CLUSTER_ID],
            slot[SlotDimensions.DESTINATION_CLUSTER_ID],
            slot[SlotDimensions.SESSION],
        ),
        "slot.origin_cluster_id": slot[SlotDimensions.ORIGIN_CLUSTER_ID],
        "slot.destination_cluster_id": slot[SlotDimensions.DESTINATION_CLUSTER_ID],
        "slot.session": slot[SlotDimensions.SESSION],
        "slot.route_id": slot[SlotDimensions.ROUTE_ID],
        "slot.start_time": slot[SlotDimensions.START_TIME],
    }


def resolve_user_dimensions(user):
    return {
        "user.pass_purchase_count": user[UserDimensions.PASS_PURCHASE_COUNT],
        "user.id": user[UserDimensions.ID],
    }
