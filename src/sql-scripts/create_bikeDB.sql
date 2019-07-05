-- Database: bikes

-- DROP DATABASE bikes;

CREATE DATABASE bikes
    WITH 
    OWNER = bike_admin
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

    -- Table: public."bikeLocations"

-- DROP TABLE public."bikeLocations";

CREATE TABLE public."bikeLocations"
(
    id integer NOT NULL DEFAULT nextval('"bikeLocations_id_seq"'::regclass),
    "bikeId" integer NOT NULL,
    "providerId" integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    CONSTRAINT "bikeLocations_pkey" PRIMARY KEY (id)
        INCLUDE("bikeId", "timestamp"),
    CONSTRAINT "providerId" FOREIGN KEY ("providerId")
        REFERENCES public.provider (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;


-- Table: public.provider

-- DROP TABLE public.provider;

CREATE TABLE public.provider
(
    id integer NOT NULL,
    name character(10) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT provider_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

-- Table: public.stations

-- DROP TABLE public.stations;

CREATE TABLE public.stations
(
    id integer NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    "firstListed" timestamp without time zone NOT NULL,
    "lastListed" timestamp without time zone NOT NULL,
    CONSTRAINT stations_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;