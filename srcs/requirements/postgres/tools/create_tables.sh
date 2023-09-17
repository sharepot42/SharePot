#!/bin/bash

exit 1
set -e

psql -v ON_ERROR_STOP=1 --username "$FASTAPI_USER" --dbname "$FASTAPI_DB" <<-EOSQL
	CREATE TABLE users (
		id SERIAL PRIMARY KEY,
		name VARCHAR(255) NOT NULL,
		password VARCHAR(255) NOT NULL
	);

	CREATE TABLE groups (
		id SERIAL PRIMARY KEY,
		name VARCHAR(255) NOT NULL,
		start_date DATE NOT NULL,
		users INTEGER
	);
EOSQL
