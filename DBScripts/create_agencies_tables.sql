CREATE TABLE agencies(
  id                    SERIAL PRIMARY KEY,
  agency_name           TEXT NOT NULL,
  city                  TEXT,
  country               TEXT,
  static                TEXT,
  static_format         TEXT,
  realtime_format       TEXT,
  trip_updates          TEXT,
  trip_updates_freq     TEXT,
  service_alerts        TEXT,
  service_alerts_freq   TEXT,
  vehicle_positions    TEXT,
  vehicle_positions_freq TEXT,
  api_access_required   BOOLEAN NOT NULL,
  notes                 TEXT,
  active                BOOLEAN NOT NULL
);