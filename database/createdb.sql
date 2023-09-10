BEGIN;

CREATE TABLE IF NOT EXISTS root (
    id bigserial PRIMARY KEY,
    url varchar(255) NOT NULL,
    CONSTRAINT unique_url UNIQUE (url)
);

CREATE TABLE IF NOT EXISTS page (
    id bigserial PRIMARY KEY,
    root_id integer NOT NULL,
    title varchar(255) NOT NULL,
    url varchar(255) NOT NULL,
    html bytea NOT NULL,
    FOREIGN KEY(root_id) REFERENCES root(id),
    CONSTRAINT unique_page UNIQUE (title, url)
);

COMMIT;
