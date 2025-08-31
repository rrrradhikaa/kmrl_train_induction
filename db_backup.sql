--
-- PostgreSQL database dump
--

\restrict MNMLpkx8V0g8fx6NZXDbf16Sy7qDnmasCv9heEP9yz7cRiWOPNmXAkZOeJkFsgq

-- Dumped from database version 14.19
-- Dumped by pg_dump version 14.19

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: branding_priorities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.branding_priorities (
    train_id character varying(50) NOT NULL,
    coach_id character varying(50) NOT NULL,
    brand_task text NOT NULL,
    priority text NOT NULL,
    deadline date NOT NULL,
    owner_team character varying(100) NOT NULL
);


ALTER TABLE public.branding_priorities OWNER TO postgres;

--
-- Name: cleaning_slots; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cleaning_slots (
    train_id character varying(50) NOT NULL,
    coach_id character varying(50) NOT NULL,
    slot_id character varying(50) NOT NULL,
    location character varying(100) NOT NULL,
    cleaning_time timestamp without time zone NOT NULL,
    cleaning_type text NOT NULL,
    assigned_cleaner character varying(100) NOT NULL
);


ALTER TABLE public.cleaning_slots OWNER TO postgres;

--
-- Name: fitness_certificates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fitness_certificates (
    train_id character varying(50) NOT NULL,
    coach_id character varying(50) NOT NULL,
    fitness_check_date date NOT NULL,
    fitness_status character varying(20) NOT NULL,
    defects_found text,
    certificate_id character varying(50) NOT NULL,
    issued_by character varying(100),
    valid_till date,
    odometer_km integer,
    remarks text
);


ALTER TABLE public.fitness_certificates OWNER TO postgres;

--
-- Name: job_cards; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_cards (
    train_id character varying(50) NOT NULL,
    coach_id character varying(50) NOT NULL,
    job_id character varying(50) NOT NULL,
    task text NOT NULL,
    status text NOT NULL,
    assigned_to character varying(100) NOT NULL,
    scheduled_date timestamp without time zone NOT NULL
);


ALTER TABLE public.job_cards OWNER TO postgres;

--
-- Name: mileage_balancing; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mileage_balancing (
    train_id character varying(50) NOT NULL,
    coach_id character varying(50) NOT NULL,
    odometer_km integer NOT NULL,
    balance_action text NOT NULL,
    next_due_km integer NOT NULL,
    remarks text NOT NULL
);


ALTER TABLE public.mileage_balancing OWNER TO postgres;

--
-- Name: stabling_geometry; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stabling_geometry (
    train_id character varying(50) NOT NULL,
    coach_id character varying(50) NOT NULL,
    stable_id character varying(50) NOT NULL,
    length_m integer NOT NULL,
    width_m integer NOT NULL,
    height_m integer NOT NULL,
    yard_location character varying(100) NOT NULL
);


ALTER TABLE public.stabling_geometry OWNER TO postgres;

--
-- Data for Name: branding_priorities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.branding_priorities (train_id, coach_id, brand_task, priority, deadline, owner_team) FROM stdin;
T001	C004	Interior Posters	High	2025-09-23	Branding-Alpha
T001	C018	Interior Posters	High	2025-09-28	Branding-Alpha
T002	C007	Logo Update	High	2025-09-14	Branding-Alpha
T002	C018	Digital Display Branding	Low	2025-09-02	Branding-Alpha
T003	C006	Logo Update	Low	2025-09-03	Branding-Beta
T003	C004	Digital Display Branding	Medium	2025-09-06	Branding-Beta
T004	C002	Interior Posters	High	2025-09-12	Branding-Alpha
T004	C020	Full Paint	Medium	2025-09-04	Branding-Alpha
T005	C008	Safety Stickers	Medium	2025-09-12	Branding-Beta
T005	C015	Full Paint	High	2025-09-04	Branding-Beta
T006	C009	Safety Stickers	High	2025-08-29	Branding-Beta
T006	C018	Digital Display Branding	Medium	2025-09-15	Branding-Beta
T007	C011	Digital Display Branding	Medium	2025-09-22	Branding-Gamma
T007	C009	Logo Update	High	2025-09-27	Branding-Beta
T008	C007	Digital Display Branding	Low	2025-08-26	Branding-Gamma
T008	C009	Interior Posters	Medium	2025-09-14	Branding-Alpha
T009	C019	Logo Update	High	2025-09-11	Branding-Beta
T009	C017	Full Paint	Low	2025-09-13	Branding-Beta
T010	C006	Digital Display Branding	High	2025-09-01	Branding-Beta
T010	C020	Logo Update	High	2025-09-03	Branding-Beta
\.


--
-- Data for Name: cleaning_slots; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cleaning_slots (train_id, coach_id, slot_id, location, cleaning_time, cleaning_type, assigned_cleaner) FROM stdin;
T001	C004	SLOT-001	Station-D	2025-08-31 07:00:00	Deep Clean	Cleaner-33
T001	C018	SLOT-002	Depot-B	2025-08-30 22:00:00	Quick Sanitize	Cleaner-33
T002	C007	SLOT-003	Station-D	2025-08-28 08:00:00	Full Wash	Cleaner-11
T002	C018	SLOT-004	Yard-C	2025-08-25 10:00:00	Quick Sanitize	Cleaner-22
T003	C006	SLOT-005	Depot-A	2025-08-25 07:00:00	Quick Sanitize	Cleaner-11
T003	C004	SLOT-006	Depot-A	2025-08-30 14:00:00	Full Wash	Cleaner-22
T004	C002	SLOT-007	Yard-C	2025-08-24 18:00:00	Quick Sanitize	Cleaner-22
T004	C020	SLOT-008	Yard-C	2025-08-26 05:00:00	Quick Sanitize	Cleaner-11
T005	C008	SLOT-009	Depot-A	2025-08-27 17:00:00	Full Wash	Cleaner-33
T005	C015	SLOT-010	Depot-B	2025-08-21 07:00:00	Quick Sanitize	Cleaner-33
T006	C009	SLOT-011	Yard-C	2025-08-21 15:00:00	Full Wash	Cleaner-22
T006	C018	SLOT-012	Yard-C	2025-08-28 14:00:00	Quick Sanitize	Cleaner-11
T007	C011	SLOT-013	Depot-A	2025-08-31 16:00:00	Quick Sanitize	Cleaner-22
T007	C009	SLOT-014	Yard-C	2025-08-30 07:00:00	Full Wash	Cleaner-22
T008	C007	SLOT-015	Depot-B	2025-08-21 19:00:00	Quick Sanitize	Cleaner-33
T008	C009	SLOT-016	Yard-C	2025-08-29 10:00:00	Quick Sanitize	Cleaner-33
T009	C019	SLOT-017	Yard-C	2025-08-25 15:00:00	Full Wash	Cleaner-11
T009	C017	SLOT-018	Station-D	2025-08-24 22:00:00	Full Wash	Cleaner-22
T010	C006	SLOT-019	Station-D	2025-08-21 06:00:00	Deep Clean	Cleaner-11
T010	C020	SLOT-020	Yard-C	2025-08-24 12:00:00	Deep Clean	Cleaner-33
\.


--
-- Data for Name: fitness_certificates; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fitness_certificates (train_id, coach_id, fitness_check_date, fitness_status, defects_found, certificate_id, issued_by, valid_till, odometer_km, remarks) FROM stdin;
T001	C004	2025-08-31	Fail	Door sensor fault	FC-T001-C004-20250831	Inspector-101	2025-09-07	46579	OK
T001	C018	2025-08-30	Pass	\N	FC-T001-C018-20250830	Inspector-101	2025-09-29	17811	OK
T002	C007	2025-08-28	Pass	\N	FC-T002-C007-20250828	Inspector-101	2025-09-27	157127	Recheck in next cycle
T002	C018	2025-08-25	Pass	\N	FC-T002-C018-20250825	Inspector-339	2025-09-24	82926	OK
T003	C006	2025-08-25	Pass	\N	FC-T003-C006-20250825	Inspector-101	2025-09-24	66443	Monitor noise
T003	C004	2025-08-30	Pass	\N	FC-T003-C004-20250830	Inspector-204	2025-09-29	100165	Monitor noise
T004	C002	2025-08-24	Pass	\N	FC-T004-C002-20250824	Inspector-204	2025-09-23	30656	Monitor noise
T004	C020	2025-08-26	Pass	\N	FC-T004-C020-20250826	Inspector-339	2025-09-25	28233	OK
T005	C008	2025-08-27	Restricted	Door sensor fault	FC-T005-C008-20250827	Inspector-101	2025-09-03	109647	Monitor noise
T005	C015	2025-08-21	Fail	Door sensor fault	FC-T005-C015-20250821	Inspector-204	2025-08-28	103132	Recheck in next cycle
T006	C009	2025-08-21	Pass	\N	FC-T006-C009-20250821	Inspector-339	2025-09-20	176455	Recheck in next cycle
T006	C018	2025-08-28	Pass	\N	FC-T006-C018-20250828	Inspector-204	2025-09-27	80765	Recheck in next cycle
T007	C011	2025-08-31	Pass	\N	FC-T007-C011-20250831	Inspector-101	2025-09-30	92694	Follow-up required
T007	C009	2025-08-30	Pass	\N	FC-T007-C009-20250830	Inspector-339	2025-09-29	198196	Monitor noise
T008	C007	2025-08-21	Pass	\N	FC-T008-C007-20250821	Inspector-339	2025-09-20	130285	Recheck in next cycle
T008	C009	2025-08-29	Pass	\N	FC-T008-C009-20250829	Inspector-339	2025-09-28	151289	Monitor noise
T009	C019	2025-08-25	Restricted	Minor oil leak	FC-T009-C019-20250825	Inspector-204	2025-09-01	67493	Recheck in next cycle
T009	C017	2025-08-24	Pass	\N	FC-T009-C017-20250824	Inspector-101	2025-09-23	38743	Recheck in next cycle
T010	C006	2025-08-21	Pass	\N	FC-T010-C006-20250821	Inspector-101	2025-09-20	110864	Follow-up required
T010	C020	2025-08-24	Pass	\N	FC-T010-C020-20250824	Inspector-339	2025-09-23	13009	OK
\.


--
-- Data for Name: job_cards; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.job_cards (train_id, coach_id, job_id, task, status, assigned_to, scheduled_date) FROM stdin;
T001	C004	JC-001	Lighting Fix	In Progress	Tech-202	2025-09-08 00:00:00
T001	C018	JC-002	Air Conditioning Check	Completed	Tech-404	2025-09-07 00:00:00
T002	C007	JC-003	Lighting Fix	Completed	Tech-303	2025-09-03 00:00:00
T002	C018	JC-004	Wheel Alignment	Completed	Tech-202	2025-08-30 00:00:00
T003	C006	JC-005	Lighting Fix	Pending	Tech-101	2025-09-03 00:00:00
T003	C004	JC-006	Door Repair	In Progress	Tech-101	2025-08-31 00:00:00
T004	C002	JC-007	Brake Check	In Progress	Tech-404	2025-09-02 00:00:00
T004	C020	JC-008	Air Conditioning Check	Pending	Tech-404	2025-08-30 00:00:00
T005	C008	JC-009	Sensor Calibration	In Progress	Tech-202	2025-09-03 00:00:00
T005	C015	JC-010	Air Conditioning Check	Pending	Tech-202	2025-08-28 00:00:00
T006	C009	JC-011	Brake Check	In Progress	Tech-101	2025-08-22 00:00:00
T006	C018	JC-012	Air Conditioning Check	In Progress	Tech-101	2025-09-05 00:00:00
T007	C011	JC-013	Brake Check	In Progress	Tech-202	2025-09-05 00:00:00
T007	C009	JC-014	Brake Check	Completed	Tech-202	2025-09-02 00:00:00
T008	C007	JC-015	Air Conditioning Check	In Progress	Tech-303	2025-08-29 00:00:00
T008	C009	JC-016	Door Repair	Completed	Tech-202	2025-09-04 00:00:00
T009	C019	JC-017	Wheel Alignment	Pending	Tech-101	2025-08-30 00:00:00
T009	C017	JC-018	Door Repair	Pending	Tech-101	2025-08-27 00:00:00
T010	C006	JC-019	Sensor Calibration	Completed	Tech-101	2025-08-23 00:00:00
T010	C020	JC-020	Lighting Fix	In Progress	Tech-202	2025-08-30 00:00:00
\.


--
-- Data for Name: mileage_balancing; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mileage_balancing (train_id, coach_id, odometer_km, balance_action, next_due_km, remarks) FROM stdin;
T001	C004	46579	Wheel Rotation	55333	OK
T001	C018	17811	Wheel Rotation	23273	Check Next Cycle
T002	C007	157127	Wheel Rotation	168758	OK
T002	C018	82926	Axle Lube	96315	Monitor Wear
T003	C006	66443	Wheel Rotation	81000	Replace Soon
T003	C004	100165	Suspension Adjust	113797	Replace Soon
T004	C002	30656	Axle Lube	38436	Check Next Cycle
T004	C020	28233	Axle Lube	34771	Replace Soon
T005	C008	109647	Axle Lube	117806	Replace Soon
T005	C015	103132	Wheel Rotation	117263	OK
T006	C009	176455	Suspension Adjust	186466	OK
T006	C018	80765	Wheel Rotation	88208	OK
T007	C011	92694	Wheel Rotation	107587	Replace Soon
T007	C009	198196	Wheel Rotation	210392	Check Next Cycle
T008	C007	130285	Suspension Adjust	141623	Monitor Wear
T008	C009	151289	Wheel Rotation	161218	Check Next Cycle
T009	C019	67493	Suspension Adjust	75493	Replace Soon
T009	C017	38743	Suspension Adjust	45794	Check Next Cycle
T010	C006	110864	Suspension Adjust	119190	OK
T010	C020	13009	Suspension Adjust	22972	Monitor Wear
\.


--
-- Data for Name: stabling_geometry; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stabling_geometry (train_id, coach_id, stable_id, length_m, width_m, height_m, yard_location) FROM stdin;
T001	C004	STB-001	21	4	5	Yard-1
T001	C018	STB-002	24	4	4	Yard-2
T002	C007	STB-003	24	4	5	Yard-2
T002	C018	STB-004	20	4	5	Yard-2
T003	C006	STB-005	24	3	4	Yard-3
T003	C004	STB-006	21	4	5	Yard-1
T004	C002	STB-007	23	4	5	Yard-1
T004	C020	STB-008	24	4	5	Yard-2
T005	C008	STB-009	21	4	4	Yard-1
T005	C015	STB-010	24	3	5	Yard-3
T006	C009	STB-011	22	3	5	Yard-3
T006	C018	STB-012	25	4	5	Yard-1
T007	C011	STB-013	23	4	4	Yard-2
T007	C009	STB-014	23	4	4	Yard-1
T008	C007	STB-015	25	3	5	Yard-1
T008	C009	STB-016	21	4	4	Yard-3
T009	C019	STB-017	23	3	5	Yard-2
T009	C017	STB-018	22	4	4	Yard-2
T010	C006	STB-019	25	3	4	Yard-2
T010	C020	STB-020	23	3	5	Yard-1
\.


--
-- Name: fitness_certificates fitness_certificates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fitness_certificates
    ADD CONSTRAINT fitness_certificates_pkey PRIMARY KEY (certificate_id);


--
-- PostgreSQL database dump complete
--

\unrestrict MNMLpkx8V0g8fx6NZXDbf16Sy7qDnmasCv9heEP9yz7cRiWOPNmXAkZOeJkFsgq

