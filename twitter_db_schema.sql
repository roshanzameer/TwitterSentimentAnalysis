--
-- PostgreSQL database dump
--

-- Dumped from database version 11.4 (Debian 11.4-1.pgdg90+1)
-- Dumped by pg_dump version 11.4 (Debian 11.4-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public."TwitterData" DROP CONSTRAINT "TwitterData_pkey";
ALTER TABLE public."TwitterData" ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public."TwitterData_id_seq";
DROP TABLE public."TwitterData";
SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: TwitterData; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."TwitterData" (
    id integer NOT NULL,
    tweet_id bigint,
    date timestamp(4) without time zone,
    tweets character varying(500),
    sentiment text,
    username text,
    location character varying(100),
    hashtags character varying(200),
    retweet_count int
    
);


ALTER TABLE public."TwitterData" OWNER TO postgres;

--
-- Name: TwitterData_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."TwitterData_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."TwitterData_id_seq" OWNER TO postgres;

--
-- Name: TwitterData_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."TwitterData_id_seq" OWNED BY public."TwitterData".id;


--
-- Name: TwitterData id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."TwitterData" ALTER COLUMN id SET DEFAULT nextval('public."TwitterData_id_seq"'::regclass);


--
-- Data for Name: TwitterData; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."TwitterData" (id, date, tweets, sentiment) FROM stdin;
\.


--
-- Name: TwitterData_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."TwitterData_id_seq"', 782, true);


--
-- Name: TwitterData TwitterData_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."TwitterData"
    ADD CONSTRAINT "TwitterData_pkey" PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

