CREATE TABLE agency(
  agency_id             TEXT,
  agency_name           TEXT,
  agency_url            TEXT,
  agency_timezone       TEXT,
  agency_lang           TEXT,
  agency_phone          TEXT,
  agency_fare_url       TEXT,
  agency_email          TEXT
);
CREATE TABLE stops(
  stop_id               TEXT,
  stop_code             TEXT,
  stop_name             TEXT,
  stop_desc             TEXT,
  stop_lat              TEXT,
  stop_lon              TEXT,
  zone_id               TEXT,
  stop_url              TEXT,
  location_type         TEXT,
  parent_station        TEXT,
  stop_timezone         TEXT,
  wheelchair_boarding   TEXT,
  level_id              TEXT,
  platform_code         TEXT
);
CREATE TABLE routes(
  route_id              TEXT,
  agency_id             TEXT,
  route_short_name      TEXT,
  route_long_name       TEXT,
  route_desc            TEXT,
  route_type            TEXT,
  route_url             TEXT,
  route_color           TEXT,
  route_text_color      TEXT,
  route_sort_order      TEXT,
  continuous_pickup     TEXT,
  continuous_dropoff    TEXT,
  RouteGroup            TEXT
);
CREATE TABLE trips(
  route_id              TEXT,
  service_id            TEXT,
  trip_id               TEXT,
  trip_headsign         TEXT,
  trip_short_name       TEXT,
  direction_id          TEXT,
  block_id              TEXT,
  shape_id              TEXT,
  wheelchair_accessible TEXT,
  bikes_allowed         TEXT
);
CREATE TABLE stop_times(
  trip_id               TEXT,
  arrival_time          TEXT,
  departure_time        TEXT,
  stop_id               TEXT,
  stop_sequence         TEXT,
  stop_headsign         TEXT,
  pickup_type           TEXT,
  drop_off_type         TEXT,
  continuous_pickup     TEXT,
  continuous_dropoff    TEXT,
  shape_dist_traveled   TEXT,
  timepoint             TEXT
);
CREATE TABLE calendar(
  service_id            TEXT,
  monday                TEXT,
  tuesday               TEXT,
  wednesday             TEXT,
  thursday              TEXT,
  friday                TEXT,
  saturday              TEXT,
  sunday                TEXT,
  start_date            TEXT,
  end_date              TEXT
);
CREATE TABLE calendar_dates(
  service_id            TEXT,
  date                  TEXT,
  exception_type        TEXT
);
CREATE TABLE fare_attributes(
  fare_id               TEXT,
  price                 TEXT,
  currency_type         TEXT,
  payment_method        TEXT,
  transfers             TEXT,
  agency_id             TEXT,
  transfer_duration     TEXT
);
CREATE TABLE fare_rules(
  fare_id               TEXT,
  route_id              TEXT,
  origin_id             TEXT,
  destination_id        TEXT,
  contains_id           TEXT
);
CREATE TABLE shapes(
  shape_id              TEXT,
  shape_pt_lat          TEXT,
  shape_pt_lon          TEXT,
  shape_pt_sequence     TEXT,
  shape_dist_traveled   TEXT
);
CREATE TABLE frequencies(
  trip_id               TEXT,
  start_time            TEXT,
  end_time              TEXT,
  headway_secs          TEXT,
  exact_times           TEXT
);
CREATE TABLE transfers(
  from_stop_id          TEXT,
  to_stop_id            TEXT,
  transfer_type         TEXT,
  min_transfer_time     TEXT
);
CREATE TABLE pathways(
  pathway_id            TEXT,
  from_stop_id          TEXT,
  to_stop_id            TEXT,
  pathway_mode          TEXT,
  is_bidirectional      TEXT,
  length                TEXT,
  traversal_time        TEXT,
  stair_count           TEXT,
  max_slope             TEXT,
  min_width             TEXT,
  signposted_as         TEXT,
  reversed_signposted_as TEXT
);
CREATE TABLE levels(
  level_id              TEXT,
  level_index           TEXT,
  level_name            TEXT
);
CREATE TABLE feed_info(
  feed_publisher_name   TEXT,
  feed_publisher_url    TEXT,
  feed_lang             TEXT,
  default_lang          TEXT,
  feed_start_date       TEXT,
  feed_end_date         TEXT,
  feed_version          TEXT,
  feed_contact_email    TEXT,
  feed_contact_url      TEXT
);
CREATE TABLE translations(
  table_name            TEXT,
  field_name            TEXT,
  language              TEXT,
  translation           TEXT,
  record_id             TEXT,
  record_sub_id         TEXT,
  field_value           TEXT
);
CREATE TABLE attributions(
  attribution_id        TEXT,
  agency_id             TEXT,
  route_id              TEXT,
  trip_id               TEXT,
  organization_name     TEXT,
  is_producer           TEXT,
  is_operator           TEXT,
  is_authority          TEXT,
  attribution_url       TEXT,
  attribution_email     TEXT,
  attribution_phone     TEXT
);
CREATE TABLE vehicle_positions(
  id                    SERIAL PRIMARY KEY,
  timestamp             TEXT,
  trip                  TEXT,
  vehicle               TEXT,
  lat                   TEXT,
  lng                   TEXT,
  bearing               TEXT,
  speed                 TEXT,
  vehicle_timestamp     TEXT,
  congestion            TEXT,
  occupancy             TEXT
);
CREATE TABLE alert(
  id                    SERIAL PRIMARY KEY,
  active_period         TEXT,
  informed_entity       TEXT,
  cause                 TEXT,
  effect                TEXT,
  url                   TEXT,
  header_text           TEXT,
  description_text      TEXT
);
CREATE TABLE trip_update(
  id                    SERIAL PRIMARY KEY,
  trip                  TEXT,
  vehicle               TEXT,
  stop_time_update      TEXT,
  timestamp             TEXT,
  delay                 TEXT
);