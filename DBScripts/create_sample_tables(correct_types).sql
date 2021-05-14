CREATE TABLE agencies(
  agency_id             TEXT          NOT NULL,
  agency_name           TEXT          NOT NULL,
  agency_url            TEXT          NOT NULL,
  agency_timezone       TEXT          NOT NULL,
  agency_lang           TEXT,
  agency_phone          TEXT,
  agency_fare_url       TEXT,
  agency_email          TEXT
);
CREATE TABLE stops(
  stop_id               INT PRIMARY KEY,
  stop_code             TEXT,
  stop_name             TEXT,
  stop_desc             TEXT,
  stop_lat              NUMERIC(14, 8),
  stop_lon              NUMERIC(14, 8),
  zone_id               INT,
  stop_url              TEXT,
  location_type         INT,
  parent_station        INT,
  stop_timezone         TEXT,
  wheelchair_boarding   INT,
  level_id              INT,
  platform_code         INT
);
CREATE TABLE routes(
  route_id              INT PRIMARY KEY,
  agency_id             INT,
  route_short_name      TEXT,
  route_long_name       TEXT,
  route_desc            TEXT,
  route_type            INT,
  route_url             TEXT,
  route_color           TEXT,
  route_text_color      TEXT,
  route_sort_order      INT,
  continuous_pickup     INT,
  continuous_dropoff    INT
);
CREATE TABLE trips(
  route_id              INT NOT NULL,
  service_id            INT NOT NULL,
  trip_id               INT PRIMARY KEY,
  trip_headsign         TEXT,
  trip_short_name       TEXT,
  direction_id          INT,
  block_id              INT,
  shape_id              INT,
  wheelchair_accessible INT,
  bikes_allowed         INT
);
CREATE TABLE stop_times(
  trip_id               INT NOT NULL,
  arrival_time          TIME,
  departure_time        TIME,
  stop_id               INT,
  stop_sequence         INT CHECK (stop_sequence >= 0) NOT NULL,
  stop_headsign         TEXT,
  pickup_type           INT,
  drop_off_type         INT,
  continuous_pickup     INT,
  continuous_dropoff    INT,
  shape_dist_traveled   FLOAT CHECK (shape_dist_traveled >= 0),
  timepoint INT
);
CREATE TABLE calendar(
  service_id            INT PRIMARY KEY,
  monday                INT NOT NULL,
  tuesday               INT NOT NULL,
  wednesday             INT NOT NULL,
  thursday              INT NOT NULL,
  friday                INT NOT NULL,
  saturday              INT NOT NULL,
  start_date            DATE NOT NULL,
  end_date              DATE NOT NULL
);
CREATE TABLE calendar_dates(
  service_id            INT NOT NULL,
  _date                 DATE NOT NULL,
  exception_type        INT
);
CREATE TABLE fare_attributes(
  fare_id               INT PRIMARY KEY,
  price                 FLOAT CHECK (price >= 0) NOT NULL,
  currency_type         TEXT NOT NULL,
  payment_method        INT NOT NULL,
  transfers             INT NOT NULL,
  agency_id             INT,
  transfer_duration     INT CHECK (transfer_duration >= 0)
);
CREATE TABLE fare_rules(
  fare_id               INT NOT NULL,
  route_id              INT,
  origin_id             INT,
  destination_id        INT,
  contains_id           INT
);
CREATE TABLE shapes(
  shape_id              INT PRIMARY KEY,
  shape_pt_lat          NUMERIC(14, 8) NOT NULL,
  shape_pt_lon          NUMERIC(14, 8) NOT NULL,
  shape_pt_sequence     INT CHECK (shape_pt_sequence >= 0) NOT NULL,
  shape_dist_traveled   FLOAT CHECK (shape_dist_traveled >= 0)
);
CREATE TABLE frequencies(
  trip_id               INT NOT NULL,
  start_time            TIME NOT NULL,
  end_time              TIME NOT NULL,
  headway_secs          INT CHECK (headway_secs >= 0) NOT NULL,
  exact_times           INT
);
CREATE TABLE transfers(
  from_stop_id          INT NOT NULL,
  to_stop_id            INT NOT NULL,
  transfer_type         INT NOT NULL,
  min_transfer_time     INT CHECK (min_transfer_time >= 0)
);
CREATE TABLE pathways(
  pathway_id            INT PRIMARY KEY,
  from_stop_id          INT NOT NULL,
  to_stop_id            INT NOT NULL,
  pathway_mode          INT NOT NULL,
  is_bidirectional      INT NOT NULL,
  length                FLOAT CHECK (length >= 0),
  traversal_time        INT CHECK (traversal_time >= 0),
  stair_count           INT,
  max_slope             FLOAT,
  min_width             FLOAT CHECK (min_width >= 0),
  signposted_as         TEXT,
  reversed_signposted_as TEXT
);
CREATE TABLE levels(
  level_id              INT PRIMARY KEY,
  level_index           FLOAT NOT NULL,
  level_name            TEXT
);
CREATE TABLE feed_info(
  feed_publisher_name   TEXT NOT NULL,
  feed_publisher_url    TEXT NOT NULL,
  feed_lang             TEXT NOT NULL,
  default_lang          TEXT,
  feed_start_date       DATE,
  feed_end_date         DATE,
  feed_version          TEXT,
  feed_contact_email    TEXT,
  feed_contact_url      TEXT
);
CREATE TABLE translations(
  table_name            TEXT NOT NULL,
  field_name            TEXT NOT NULL,
  language              TEXT NOT NULL,
  translation           TEXT NOT NULL,
  record_id             TEXT,
  record_sub_id         TEXT,
  field_value           TEXT
);
CREATE TABLE attributions(
  attribution_id        TEXT,
  agency_id             TEXT,
  route_id              TEXT,
  trip_id               TEXT,
  organization_name     TEXT NOT NULL,
  is_producer           INT,
  is_operator           INT,
  is_authority          INT,
  attribution_url       TEXT,
  attribution_email     TEXT,
  attribution_phone     TEXT
);