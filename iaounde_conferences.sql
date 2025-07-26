--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Ubuntu 17.5-1.pgdg22.04+1)
-- Dumped by pg_dump version 17.5 (Ubuntu 17.5-1.pgdg22.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
-- SET transaction_timeout = 0;  -- Ligne commentée pour compatibilité PostgreSQL 15
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: conferences; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.conferences (
    id integer NOT NULL,
    nom character varying(200) NOT NULL,
    periode_debut date NOT NULL,
    periode_fin date NOT NULL,
    logo character varying(255),
    description text,
    lien_site character varying(500) NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    created_by integer
);

ALTER TABLE public.conferences OWNER TO postgres;

--
-- Name: conferences_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.conferences_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.conferences_id_seq OWNER TO postgres;

--
-- Name: conferences_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.conferences_id_seq OWNED BY public.conferences.id;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(20),
    is_active boolean,
    created_at timestamp without time zone
);

ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;

--
-- Name: conferences id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conferences ALTER COLUMN id SET DEFAULT nextval('public.conferences_id_seq'::regclass);

--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);

--
-- Data for Name: conferences; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.conferences (id, nom, periode_debut, periode_fin, logo, description, lien_site, created_at, updated_at, created_by) FROM stdin;
1	IAOUNDE-GRENOBLE	2025-06-24	2025-06-26	20250725_192923_photo_2025-07-25_19-25-38.jpg	The workshop brought together researchers and professionals—including startup founders and representatives from government ministries—from both Cameroon and France.\r\n\r\nPresentations covered several domains where the use of AI is particularly relevant, such as agriculture, healthcare, governance, energy, and culture. Issues related to the protection of personal data were also discussed.\r\n\r\nThe audience included a diverse range of participants, with both junior and senior contributors actively engaged.\r\n\r\nThe workshop also served as a catalyst for new collaborative initiatives. For instance, the Ministry of Public Procurement of Cameroon and Grenoble INP–UGA are currently discussing the signing of a Memorandum of Understanding (MoU), marking the beginning of a long-term and intensive collaboration.	https://iaounde.com/	2025-07-25 18:29:23.596943	2025-07-25 18:29:23.596947	1
2	IAOUNDE-AMBAN	2025-07-28	2025-07-30	20250725_200128_IA_OUNDE_Votre_story_2.png	The workshop, organized by the ESTLC (Higher School of Transport, Logistics, and Commerce) of the University of Ebolowa at Ambam, brought together researchers and professionals — including startup founders and representatives from government ministries — from both Cameroon and France.\r\n\r\nPresentations covered several domains where the use of AI is particularly relevant, including:\r\n    Transportation, Logistics, Commerce ,Agricultur, Healthcare,Energy\r\nIssues related to the protection of personal data were also discussed.\r\nThe audience included a diverse range of participants, from junior researchers and students to senior industry and academic experts, all actively engaged in the discussions.\r\nThe workshop also served as a catalyst for new collaborative initiatives. For instance, the Ministry of Transport of Cameroon and Grenoble INP–UGA are currently discussing the signing of a Memorandum of Understanding (MoU), marking the beginning of a long-term and intensive c	https://amban.iaounde.com/	2025-07-25 19:01:28.740733	2025-07-25 19:01:28.740739	1
\.

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password_hash, role, is_active, created_at) FROM stdin;
1	admin	admin@iaounde.com	pbkdf2:sha256:600000$xpJEypwQVRkGUrXl$9c16660cecde13ea56bca453dd222a4454c79f18df431632522e3acbccf8b7b8	super_admin	t	2025-07-25 18:22:33.127462
\.

--
-- Name: conferences_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.conferences_id_seq', 2, true);

--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);

--
-- Name: conferences conferences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conferences
    ADD CONSTRAINT conferences_pkey PRIMARY KEY (id);

--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);

--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);

--
-- Name: conferences conferences_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conferences
    ADD CONSTRAINT conferences_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

--
-- PostgreSQL database dump complete
--
