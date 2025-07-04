--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0 (Debian 17.0-1.pgdg120+1)
-- Dumped by pg_dump version 17.0 (Debian 17.0-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE asao_db;
--
-- Name: asao_db; Type: DATABASE; Schema: -; Owner: asao_dd
--

CREATE DATABASE asao_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE asao_db OWNER TO asao_dd;

\connect asao_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: asao_dd
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO asao_dd;

--
-- Name: product; Type: TABLE; Schema: public; Owner: asao_dd
--

CREATE TABLE public.product (
    name character varying NOT NULL,
    link character varying NOT NULL,
    seller_id integer,
    id integer NOT NULL
);


ALTER TABLE public.product OWNER TO asao_dd;

--
-- Name: product_data; Type: TABLE; Schema: public; Owner: asao_dd
--

CREATE TABLE public.product_data (
    product_id integer NOT NULL,
    date_receipt timestamp without time zone NOT NULL,
    ozon_card_price double precision,
    discount_price double precision,
    base_price double precision NOT NULL,
    star_count double precision NOT NULL,
    review_count integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.product_data OWNER TO asao_dd;

--
-- Name: product_data_id_seq; Type: SEQUENCE; Schema: public; Owner: asao_dd
--

CREATE SEQUENCE public.product_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.product_data_id_seq OWNER TO asao_dd;

--
-- Name: product_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: asao_dd
--

ALTER SEQUENCE public.product_data_id_seq OWNED BY public.product_data.id;


--
-- Name: product_id_seq; Type: SEQUENCE; Schema: public; Owner: asao_dd
--

CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.product_id_seq OWNER TO asao_dd;

--
-- Name: product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: asao_dd
--

ALTER SEQUENCE public.product_id_seq OWNED BY public.product.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: asao_dd
--

CREATE TABLE public."user" (
    name character varying NOT NULL,
    email character varying NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public."user" OWNER TO asao_dd;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: asao_dd
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO asao_dd;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: asao_dd
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: user_passes; Type: TABLE; Schema: public; Owner: asao_dd
--

CREATE TABLE public.user_passes (
    user_id integer NOT NULL,
    hash_pass character varying NOT NULL,
    date_pass timestamp without time zone NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.user_passes OWNER TO asao_dd;

--
-- Name: user_passes_id_seq; Type: SEQUENCE; Schema: public; Owner: asao_dd
--

CREATE SEQUENCE public.user_passes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_passes_id_seq OWNER TO asao_dd;

--
-- Name: user_passes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: asao_dd
--

ALTER SEQUENCE public.user_passes_id_seq OWNED BY public.user_passes.id;


--
-- Name: product id; Type: DEFAULT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public.product ALTER COLUMN id SET DEFAULT nextval('public.product_id_seq'::regclass);


--
-- Name: product_data id; Type: DEFAULT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public.product_data ALTER COLUMN id SET DEFAULT nextval('public.product_data_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: user_passes id; Type: DEFAULT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public.user_passes ALTER COLUMN id SET DEFAULT nextval('public.user_passes_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: asao_dd
--

COPY public.alembic_version (version_num) FROM stdin;
125e12adf826
\.


--
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: asao_dd
--

COPY public.product (name, link, seller_id, id) FROM stdin;
╨Ь╨╛╨╗╨╛╤В╨╛╨║ ╤Б╨╗╨╡╤Б╨░╤А╨╜╤Л╨╣ 600 ╨│, ╤Ж╨╡╨╗╤М╨╜╨╛╨╝╨╡╤В╨░╨╗╨╗╨╕╤З╨╡╤Б╨║╨╕╨╣, ╨┤╨▓╤Г╤Е╨║╨╛╨╝╨┐╨╛╨╜╨╡╨╜╤В╨╜╨░╤П ╤А╤Г╨║╨╛╤П╤В╨║╨░ Denzel	https://www.ozon.ru/product/molotok-slesarnyy-600-g-tselnometallicheskiy-dvuhkomponentnaya-rukoyatka-denzel-1589044035/?at=vQtrZ7BpjsrAkxwXF8QzKk4TyZy8y2cK0wEqWuv9rBNg&avtc=1&avte=4&avts=1739234849&keywords=%D0%BC%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%BA+%D1%81%D0%BB%D0%B5%D1%81%D0%B0%D1%80%D0%BD%D1%8B%D0%B9+600+%D0%B3	1	1589044035
╨Ь╨╛╨╗╨╛╤В╨╛╨║ ╤Б╨╗╨╡╤Б╨░╤А╨╜╤Л╨╣ 600╨│, ╨║╤А╤Г╨│╨╗╤Л╨╣ ╨▒╨╛╨╡╨║, ╤Ж╨╕╨╜╨║, ╨┤╨╡╤А╨╡╨▓╤П╨╜╨╜╨░╤П ╤А╤Г╤З╨║╨░, ╨Я╨Р╨Ю ╨У╨╛╤А╨╕╨╖╨╛╨╜╤В ╨а╨╛╤Б╤Б╨╕╤П	https://www.ozon.ru/product/molotok-slesarnyy-600g-kruglyy-boek-tsink-derevyannaya-ruchka-pao-gorizont-rossiya-1483407940/?at=K8tZk2AzvHn4l7zJuGWyN5DUmgKV8lu6Q9LBEFy68AMj&avtc=1&avte=4&avts=1739234849&keywords=%D0%BC%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%BA+%D1%81%D0%BB%D0%B5%D1%81%D0%B0%D1%80%D0%BD%D1%8B%D0%B9+600+%D0%B3	1	1483407940
╨ж╨╡╨╗╤М╨╜╨╛╨╝╨╡╤В╨░╨╗╨╗╨╕╤З╨╡╤Б╨║╨╕╨╣ ╤Б╨╗╨╡╤Б╨░╤А╨╜╤Л╨╣ ╨╝╨╛╨╗╨╛╤В╨╛╨║ Denzel 600 ╨│, ╨┤╨▓╤Г╤Е╨║╨╛╨╝╨┐╨╛╨╜╨╡╨╜╤В╨╜╨░╤П ╤А╤Г╨║╨╛╤П╤В╨║╨░ 10404	https://www.ozon.ru/product/tselnometallicheskiy-slesarnyy-molotok-denzel-600-g-dvuhkomponentnaya-rukoyatka-10404-1513899353/?at=36tWvp86Jcrg8qorT9VV3VNT5GlpJlsxzJqWOIlqzgK&avtc=1&avte=4&avts=1739234849&keywords=%D0%BC%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%BA+%D1%81%D0%BB%D0%B5%D1%81%D0%B0%D1%80%D0%BD%D1%8B%D0%B9+600+%D0%B3	1	1513899353
╨Ь╨╛╨╗╨╛╤В╨╛╨║ ╤Б╤В╤А╨╛╨╕╤В╨╡╨╗╤М╨╜╤Л╨╣ ╨б╨Ш╨С╨а╨в╨Х╨е, ╤Б ╨▒╨╛╨╣╨║╨╛╨╝ ╨▓╨╡╤Б╨╛╨╝ 600 ╨│ ╨╕ ╤Д╨╕╨▒╨╡╤А╨│╨╗╨░╤Б╨╛╨▓╨╛╨╣ ╨╛╨▒╤А╨╡╨╖╨╕╨╜╨╡╨╜╨╜╨╛╨╣ ╤А╤Г╨║╨╛╤П╤В╨║╨╛╨╣, ╨╝╨╛╨╗╨╛╤В╨╛╨║ ╤Б╨╗╨╡╤Б╨░╤А╨╜╤Л╨╣, 10325	https://www.ozon.ru/product/molotok-stroitelnyy-sibrteh-s-boykom-vesom-600-g-i-fiberglasovoy-obrezinennoy-rukoyatkoy-molotok-359892494/?at=oZt6mrojLczQzMpyHO6QNkjcllOjr7c7M05wxf6ZJ3yP&avtc=1&avte=4&avts=1739234849&keywords=%D0%BC%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%BA+%D1%81%D0%BB%D0%B5%D1%81%D0%B0%D1%80%D0%BD%D1%8B%D0%B9+600+%D0%B3	1	359892494
╨Ь╨╛╨╗╨╛╤В╨╛╨║ ╤Б╨╗╨╡╤Б╨░╤А╨╜╤Л╨╣ ╤Ж╨╡╨╗╤М╨╜╨╛╨╝╨╡╤В╨░╨╗╨╗╨╕╤З╨╡╤Б╨║╨╕╨╣ ╤Б ╨┤╨▓╤Г╤Е╨║╨╛╨╝╨┐╨╛╨╜╨╡╤В╨╜╨╛╨╣ ╤А╤Г╨║╨╛╤П╤В╨║╨╛╨╣ 600╨│	https://www.ozon.ru/product/molotok-slesarnyy-tselnometallicheskiy-s-dvuhkomponetnoy-rukoyatkoy-600g-1758884002/?at=LZtl2RoypTAo8gqzuJNmPDPHWWA7vVUOjXB3pInMjyQx&avtc=1&avte=4&avts=1739234849&keywords=%D0%BC%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%BA+%D1%81%D0%BB%D0%B5%D1%81%D0%B0%D1%80%D0%BD%D1%8B%D0%B9+600+%D0%B3	1	1758884002
╨Ь╨╛╨╗╨╛╤В╨╛╨║ ╤Б╨╗╨╡╤Б╨░╤А╨╜╤Л╨╣, 600 ╨│, ╤Д╨╕╨▒╨╡╤А╨│╨╗╨░╤Б╨╛╨▓╨░╤П ╨╛╨▒╤А╨╡╨╖╨╕╨╜╨╡╨╜╨╜╨░╤П ╤А╤Г╨║╨╛╤П╤В╨║╨░ Matrix	https://www.ozon.ru/product/molotok-slesarnyy-600-g-fiberglasovaya-obrezinennaya-rukoyatka-matrix-537132378/?at=pZtpZnl1NfYr0zZ9tOAYALgCWXqx2mHXqZV68toYJN5o&avtc=1&avte=4&avts=1739234849&keywords=%D0%BC%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%BA+%D1%81%D0%BB%D0%B5%D1%81%D0%B0%D1%80%D0%BD%D1%8B%D0%B9+600+%D0%B3	1	537132378
╨Ь╨╛╨╗╨╛╤В╨╛╨║ ╤Б╨╗╨╡╤Б╨░╤А╨╜╤Л╨╣ 600 ╨│ RAGE by VIRA	https://www.ozon.ru/product/molotok-slesarnyy-600-g-rage-by-vira-166158164/?at=ywtA3rjqzc0KPxzpt3p55OlI10L20mHm4QYqzcg8EqJo&avtc=1&avte=4&avts=1739234849&keywords=%D0%BC%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%BA+%D1%81%D0%BB%D0%B5%D1%81%D0%B0%D1%80%D0%BD%D1%8B%D0%B9+600+%D0%B3	1	166158164
╨Ь╨╛╨╗╨╛╤В╨╛╨║ ╤Б╨╗╨╡╤Б╨░╤А╨╜╤Л╨╣ 600 ╨│, ╤Ж╨╡╨╗╤М╨╜╨╛╨╝╨╡╤В╨░╨╗╨╗╨╕╤З╨╡╤Б╨║╨╕╨╣, ╨┤╨▓╤Г╤Е╨║╨╛╨╝╨┐╨╛╨╜╨╡╨╜╤В╨╜╨░╤П ╤А╤Г╨║╨╛╤П╤В╨║╨░ Denzel 10404	https://www.ozon.ru/product/molotok-slesarnyy-600-g-tselnometallicheskiy-dvuhkomponentnaya-rukoyatka-denzel-10404-1108781317/?at=lRt6l2905cJjwYZLUKRymLNHY6ND0VcEwZM53SBmrz4k&avtc=1&avte=4&avts=1739234849&keywords=%D0%BC%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%BA+%D1%81%D0%BB%D0%B5%D1%81%D0%B0%D1%80%D0%BD%D1%8B%D0%B9+600+%D0%B3	1	1108781317
╨Ь╨╛╨╗╨╛╤В╨╛╨║ ╤Б╨╗╨╡╤Б╨░╤А╨╜╤Л╨╣ ╨Ъ╨Ю╨С╨Р╨Ы╨м╨в 600 ╨│, ╤Д╨╕╨▒╨╡╤А╨│╨╗╨░╤Б╨╛╨▓╨░╤П ╤А╤Г╨║╨╛╤П╤В╨║╨░	https://www.ozon.ru/product/molotok-slesarnyy-kobalt-600-g-fiberglasovaya-rukoyatka-692927499/?at=MZtvYqoM0h2LVYXzhQoWJGZU07m48ru5955yxcQzom7N&avtc=1&avte=4&avts=1739234849&keywords=%D0%BC%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%BA+%D1%81%D0%BB%D0%B5%D1%81%D0%B0%D1%80%D0%BD%D1%8B%D0%B9+600+%D0%B3	1	692927499
╨Ь╨╛╨╗╨╛╤В╨╛╨║ ╤Б╨╗╨╡╤Б╨░╤А╨╜╤Л╨╣ ╨║╨╛╨▓╨░╨╜╤Л╨╣ ╤Б ╤Д╨╕╨▒╨╡╤А╨│╨╗╨░╤Б╤Б╨╛╨▓╨╛╨╣ ╤А╤Г╨║╨╛╤П╤В╨║╨╛╨╣ 600 ╨│ DERZHI	https://www.ozon.ru/product/molotok-slesarnyy-kovanyy-s-fiberglassovoy-rukoyatkoy-600-g-derzhi-1774746330/?at=MZtvYqoM0h7VwxXBUZO24jum9Qv69uYPVMKMi2jK5GM&avtc=1&avte=4&avts=1739234849&keywords=%D0%BC%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%BA+%D1%81%D0%BB%D0%B5%D1%81%D0%B0%D1%80%D0%BD%D1%8B%D0%B9+600+%D0%B3	1	1774746330
╨Ь╨╛╨╗╨╛╤В╨╛╨║ ╤Б╤В╤А╨╛╨╕╤В╨╡╨╗╤М╨╜╤Л╨╣ DENZEL, ╤Ж╨╡╨╗╤М╨╜╨╛╨╝╨╡╤В╨░╨╗╨╗╨╕╤З╨╡╤Б╨║╨╕╨╣, ╤Б ╨▒╨╛╨╣╨║╨╛╨╝ ╨▓╨╡╤Б╨╛╨╝ 600 ╨│ ╨╕ ╨┤╨▓╤Г╤Е╨║╨╛╨╝╨┐╨╛╨╜╨╡╨╜╤В╨╜╨╛╨╣ ╤А╤Г╨║╨╛╤П╤В╨║╨╛╨╣, ╨╝╨╛╨╗╨╛╤В╨╛╨║ ╤Б╨╗╨╡╤Б╨░╤А╨╜╤Л╨╣, 10404	https://www.ozon.ru/product/molotok-stroitelnyy-denzel-tselnometallicheskiy-s-boykom-vesom-600-g-i-dvuhkomponentnoy-967993235/?at=gpt4JAgOxu2DjxPWUqOEX5zSl41JLltAGkLolSz643oW&avtc=1&avte=4&avts=1739234849&keywords=%D0%BC%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%BA+%D1%81%D0%BB%D0%B5%D1%81%D0%B0%D1%80%D0%BD%D1%8B%D0%B9+600+%D0%B3	1	967993235
\.


--
-- Data for Name: product_data; Type: TABLE DATA; Schema: public; Owner: asao_dd
--

COPY public.product_data (product_id, date_receipt, ozon_card_price, discount_price, base_price, star_count, review_count, id) FROM stdin;
1589044035	2025-04-22 02:46:45.932224	0	1090	1472	5	2	1
1483407940	2025-04-22 02:46:47.93278	456	470	646	4.9	347	2
1513899353	2025-04-22 02:46:50.933172	0	1180	1430	5	5	3
359892494	2025-04-22 02:46:52.933645	0	687	862	4.9	676	4
1758884002	2025-04-22 02:46:54.934111	824	887	2000	4.9	11	5
537132378	2025-04-22 02:46:56.934413	0	887	1246	5	19	6
166158164	2025-04-22 02:46:59.931351	608	654	1974	4.9	4070	7
1108781317	2025-04-22 02:47:03.931784	0	1123	1606	4.9	67	8
692927499	2025-04-22 02:47:05.932312	553	595	1100	4.9	588	9
692927499	2025-04-22 02:47:09.932648	560	599	1100	4.9	588	10
692927499	2025-04-22 02:47:13.933018	540	595	1000	4.9	588	11
692927499	2025-04-22 02:47:17.933364	570	600	1120	4.9	588	12
692927499	2025-04-22 02:47:20.933812	575	610	1128	4.9	588	13
1774746330	2025-04-22 02:47:23.934248	553	596	994	4.9	15	14
967993235	2025-04-22 02:47:25.934574	0	1094	1400	4.9	4098	15
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: asao_dd
--

COPY public."user" (name, email, id) FROM stdin;
Demidos	l3h4denik@yandex.ru	1
\.


--
-- Data for Name: user_passes; Type: TABLE DATA; Schema: public; Owner: asao_dd
--

COPY public.user_passes (user_id, hash_pass, date_pass, id) FROM stdin;
1	$2b$12$1/nGDACdD0Z4ltD.ttJuGOG6m.P74JCvUvvWEgbe3cT1526XTZtXe	2025-04-06 17:41:32.817364	1
1	$2b$12$jkW2jCfYOQELxWiDqd07rOfwrKpwmUoVyyVLh8yHnOZtY0VKosU0S	2025-04-06 17:44:46.05342	2
1	$2b$12$oOwTnQsRP9vw.bQ18yAT3.9hbo5lRZ9xOgngZ9IRNL.j5O39AxlLK	2025-04-06 18:48:16.761354	3
\.


--
-- Name: product_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: asao_dd
--

SELECT pg_catalog.setval('public.product_data_id_seq', 15, true);


--
-- Name: product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: asao_dd
--

SELECT pg_catalog.setval('public.product_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: asao_dd
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- Name: user_passes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: asao_dd
--

SELECT pg_catalog.setval('public.user_passes_id_seq', 3, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: product pk_product; Type: CONSTRAINT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT pk_product PRIMARY KEY (id);


--
-- Name: product_data pk_product_data; Type: CONSTRAINT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public.product_data
    ADD CONSTRAINT pk_product_data PRIMARY KEY (id);


--
-- Name: user pk_user; Type: CONSTRAINT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT pk_user PRIMARY KEY (id);


--
-- Name: user_passes pk_user_passes; Type: CONSTRAINT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public.user_passes
    ADD CONSTRAINT pk_user_passes PRIMARY KEY (id);


--
-- Name: user uq_user_email; Type: CONSTRAINT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT uq_user_email UNIQUE (email);


--
-- Name: user uq_user_name; Type: CONSTRAINT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT uq_user_name UNIQUE (name);


--
-- Name: product_data fk_product_data_product_id_product; Type: FK CONSTRAINT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public.product_data
    ADD CONSTRAINT fk_product_data_product_id_product FOREIGN KEY (product_id) REFERENCES public.product(id);


--
-- Name: product fk_product_seller_id_user; Type: FK CONSTRAINT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT fk_product_seller_id_user FOREIGN KEY (seller_id) REFERENCES public."user"(id);


--
-- Name: user_passes fk_user_passes_user_id_user; Type: FK CONSTRAINT; Schema: public; Owner: asao_dd
--

ALTER TABLE ONLY public.user_passes
    ADD CONSTRAINT fk_user_passes_user_id_user FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

