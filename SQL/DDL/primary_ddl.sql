CREATE TABLE album
(
    album_id  INT          NOT NULL,
    title     VARCHAR(160) NOT NULL,
    artist_id INT          NOT NULL,
    CONSTRAINT album_pkey PRIMARY KEY (album_id)
);

CREATE TABLE artist
(
    artist_id INT NOT NULL,
    name      VARCHAR(120),
    CONSTRAINT artist_pkey PRIMARY KEY (artist_id)
);

CREATE TABLE customer
(
    customer_id    INT         NOT NULL,
    first_name     VARCHAR(40) NOT NULL,
    last_name      VARCHAR(20) NOT NULL,
    company        VARCHAR(80),
    support_rep_id INT,
    contact_id INT,
    address_info_id INT,
    CONSTRAINT customer_pkey PRIMARY KEY (customer_id)
);

CREATE TABLE employee
(
    employee_id INT         NOT NULL,
    last_name   VARCHAR(20) NOT NULL,
    first_name  VARCHAR(20) NOT NULL,
    title       VARCHAR(30),
    reports_to  INT,
    birth_date  TIMESTAMP,
    hire_date   TIMESTAMP,
    contact_id INT,
    address_info_id INT,
    CONSTRAINT employee_pkey PRIMARY KEY (employee_id)
);

CREATE TABLE genre
(
    genre_id INT NOT NULL,
    name     VARCHAR(120),
    CONSTRAINT genre_pkey PRIMARY KEY (genre_id)
);

CREATE TABLE invoice
(
    invoice_id          INT            NOT NULL,
    customer_id         INT            NOT NULL,
    invoice_date        TIMESTAMP      NOT NULL,
    billing_address     VARCHAR(70),
    billing_city        VARCHAR(40),
    billing_state       VARCHAR(40),
    billing_country     VARCHAR(40),
    billing_postal_code VARCHAR(10),
    total               NUMERIC(10, 2) NOT NULL,
    CONSTRAINT invoice_pkey PRIMARY KEY (invoice_id)
);

CREATE TABLE invoice_line
(
    invoice_line_id INT            NOT NULL,
    invoice_id      INT            NOT NULL,
    track_id        INT            NOT NULL,
    unit_price      NUMERIC(10, 2) NOT NULL,
    quantity        INT            NOT NULL,
    CONSTRAINT invoice_line_pkey PRIMARY KEY (invoice_line_id)
);

CREATE TABLE media_type
(
    media_type_id INT NOT NULL,
    name          VARCHAR(120),
    CONSTRAINT media_type_pkey PRIMARY KEY (media_type_id)
);

CREATE TABLE playlist
(
    playlist_id INT NOT NULL,
    name        VARCHAR(120),
    CONSTRAINT playlist_pkey PRIMARY KEY (playlist_id)
);

CREATE TABLE playlist_track
(
    playlist_id INT NOT NULL,
    track_id    INT NOT NULL,
    CONSTRAINT playlist_track_pkey PRIMARY KEY (playlist_id, track_id)
);

CREATE TABLE track
(
    track_id      INT            NOT NULL,
    name          VARCHAR(200)   NOT NULL,
    album_id      INT,
    media_type_id INT            NOT NULL,
    genre_id      INT,
    composer      VARCHAR(220),
    milliseconds  INT            NOT NULL,
    bytes         INT,
    unit_price    NUMERIC(10, 2) NOT NULL,
    CONSTRAINT track_pkey PRIMARY KEY (track_id)
);

CREATE TABLE price
(
    price_id SERIAL PRIMARY KEY,
    value    NUMERIC(10, 2) NOT NULL,
    date     TIMESTAMP      NOT NULL,
    track_id INT            NOT NULL
);

CREATE TABLE Contact
(
    contact_id INT PRIMARY KEY,
    phone      VARCHAR(50),
    fax        VARCHAR(50),
    email      VARCHAR(100),
    CONSTRAINT contact_pkey PRIMARY KEY (contact_id)
);

CREATE TABLE AddressInfo
(
    address_info_id SERIAL PRIMARY KEY,
    address         TEXT,
    city            TEXT,
    state           TEXT,
    country         TEXT,
    postalcode      TEXT,
    phone           TEXT,
    fax             TEXT,
    email           TEXT,
    CONSTRAINT address_info_pkey PRIMARY KEY (address_info_id)
);