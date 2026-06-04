STAFF_DWELL_THRESHOLD = 40


class StaffClassifier:

    def __init__(self):

        self.visitor_total_dwell = {}

    def record_dwell(
        self,
        visitor_id,
        dwell_seconds
    ):

        self.visitor_total_dwell[
            visitor_id
        ] = (
            self.visitor_total_dwell.get(
                visitor_id,
                0
            ) + dwell_seconds
        )

    def is_staff(
        self,
        visitor_id
    ):

        return (
            self.visitor_total_dwell.get(
                visitor_id,
                0
            ) >= STAFF_DWELL_THRESHOLD
        )

    def get_customers(self):

        return {
            v
            for v in self.visitor_total_dwell
            if not self.is_staff(v)
        }
