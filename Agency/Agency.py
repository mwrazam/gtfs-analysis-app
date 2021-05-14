class Agency():
    def __init__(self, name, city, country, static, static_format, realtime_format, trip_updates, trip_updates_freq, service_alerts, service_alerts_freq, vehicle_positions, vehicle_positions_freq, api_access_required, notes):
        self.name = name
        self.city = city
        self.country = country
        self.static = static
        self.static_format = static_format
        self.realtime_format = realtime_format
        self.trip_updates = trip_updates
        self.trip_updates_freq = trip_updates_freq
        self.service_alerts = service_alerts
        self.service_alerts_freq = service_alerts_freq
        self.vehicle_positions = vehicle_positions
        self.vehicle_positions_freq = vehicle_positions_freq
        self.api_access_required = api_access_required
        self.notes = notes = notes
        self.active = False

    def set_active(self, status):
        self.active = status