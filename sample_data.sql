INSERT INTO pilot VALUES
    (1,'Elena','Martinez','Spanish','EU-12478','2025-06-30',2504),
    (2,'Viktor','Petrov',NULL,'EU-67890','2024-08-15',3220),
    (3,'Isabelle','Leclerc','French','EU-54321','2026-05-12',2873),
    (4,'Luca','Moretti','Italian','EU-13579','2023-09-08',2187);

INSERT INTO flight_pilot_link_table VALUES
    (1,4), (1,2), (1,12), (1,18), (2,18), (2,1),
    (2,12), (2,20), (2,30), (2,35), (1,35), (1,25),
    (1,3), (4,5), (3,6), (3,8), (2,8), (2,7),
    (1,9), (4,10), (3,11), (2,11), (4,12), (2,13),
    (1,14), (2,15), (2,16), (3,16), (4,17), (2,17),
    (1,19), (2,21), (3,22), (3,21), (4,23), (2,23),
    (1,24), (3,24), (3,25), (3,26), (3,27), (3,28),
    (1,29), (2,31), (2,32), (3,33), (3,34), (1,34),
    (4,34), (4,35), (2,36), (4,36), (4,37), (2,37),
    (2,38), (3,38), (1,39), (1,40), (2,40), (3,39);

INSERT INTO aircraft VALUES
    (1,'Airbus','A320','G-VPME'), (2,'Boeing','737','N62907'), (3,'Boeing','777','N24462'), (4,'Airbus','A330','9V-GBU'),
    (5,'Airbus','A320','9V-OEH'), (6,'Boeing','777','N60958'), (7,'Airbus','A330','G-SQVK'), (8,'Boeing','737','N65111'),
    (9,'Airbus','A320','9V-AEJ'), (10,'Airbus','A320','N79206'), (11,'Airbus','A320','N75096'), (12,'Airbus','A330','9V-DNB'),
    (13,'Airbus','A330','N86541'), (14,'Airbus','A330','G-GOQW'), (15,'Boeing','737','G-DOLJ'), (16,'Boeing','737','9V-KTN'),
    (17,'Boeing','737','G-KTNQ'), (18,'Boeing','777','G-SCJD'), (19,'Boeing','777','G-JRVO'), (20,'Boeing','777','9V-SXL');

INSERT INTO aircraft_type VALUES
    ('Airbus','A330',277,11750), ('Boeing','777',368,10820),
    ('Boeing','737',215,7084), ('Airbus','A320',186,6150);


INSERT INTO flight VALUES
    (1,'BA0011',3,'2023-11-28T18:55:00+00:00','2023-11-29T15:51:00+00:00','LHR','SIN',285), (2,'BA0011',6,'2023-11-29T18:55:00+00:00','2023-11-30T15:51:00+00:00','LHR','SIN',295),
    (3,'BA0011',18,'2023-11-30T18:55:00+00:00','2023-12-01T15:51:00+00:00','LHR','SIN',310), (4,'BA0011',19,'2023-12-01T18:55:00+00:00','2023-12-02T15:51:00+00:00','LHR','SIN',252),
    (5,'BA0011',20,'2023-12-02T18:55:00+00:00','2023-12-03T15:51:00+00:00','LHR','SIN',152), (6,'BA0016',3,'2023-11-28T23:05:00+00:00','2023-11-29T05:25:00+00:00','SIN','LHR',175),
    (7,'BA0016',6,'2023-11-29T23:05:00+00:00','2023-11-30T05:25:00+00:00','SIN','LHR',122), (8,'BA0016',18,'2023-11-30T23:05:00+00:00','2023-12-01T05:25:00+00:00','SIN','LHR',192),
    (9,'BA0016',19,'2023-12-01T23:05:00+00:00','2023-12-02T05:25:00+00:00','SIN','LHR',115), (10,'BA0016',20,'2023-12-02T23:05:00+00:00','2023-12-03T05:25:00+00:00','SIN','LHR',262),
    (11,'BA0016',3,'2023-11-27T16:25:00+00:00','2023-11-27T21:38:00+00:00','SYD','SIN',195), (12,'BA4694',2,'2023-11-28T05:29:00+00:00','2023-11-28T08:47:00+00:00','JFK','MIA',168),
    (13,'BA4946',8,'2023-11-28T08:55:00+00:00','2023-11-28T11:50:00+00:00','MIA','EWR',150), (14,'BA1444',15,'2023-11-28T07:45:00+00:00','2023-11-28T09:10:00+00:00','LHR','EDI',185),
    (15,'BA1433',2,'2023-12-04T13:00:00+00:00','2023-12-04T14:25:00+00:00','EDI','LHR',162), (16,'BA1435',17,'2023-12-08T06:10:00+00:00','2023-12-08T07:45:00+00:00','EDI','LHR',122),
    (17,'BA1443',8,'2023-12-08T07:35:00+00:00','2023-12-08T09:10:00+00:00','EDI','LHR',182), (18,'BA1439',15,'2023-12-08T08:30:00+00:00','2023-12-08T10:05:00+00:00','EDI','LHR',165),
    (19,'BA1441',16,'2023-12-08T09:50:00+00:00','2023-12-08T11:25:00+00:00','EDI','LHR',147), (20,'BA1437',17,'2023-12-08T13:35:00+00:00','2023-12-08T15:00:00+00:00','EDI','LHR',180),
    (21,'BA1414',2,'2023-11-30T06:45:00+00:00','2023-11-30T08:10:00+00:00','LHR','BHD',95), (22,'BA1418',8,'2023-11-30T08:55:00+00:00','2023-11-30T10:20:00+00:00','LHR','BHD',115),
    (23,'BA0117',1,'2023-11-28T08:20:00+00:00','2023-11-28T11:25:00+00:00','LHR','JFK',175), (24,'BA0117',4,'2023-11-29T08:20:00+00:00','2023-11-29T11:25:00+00:00','LHR','JFK',152),
    (25,'BA0175',5,'2023-11-29T09:35:00+00:00','2023-11-29T12:45:00+00:00','LHR','JFK',177), (26,'BA1516',7,'2023-11-29T10:35:00+00:00','2023-11-29T13:45:00+00:00','LHR','JFK',220),
    (27,'BA0185',9,'2023-11-29T10:45:00+00:00','2023-11-29T14:00:00+00:00','LHR','EWR',167), (28,'BA0117',10,'2023-12-02T08:20:00+00:00','2023-12-02T11:25:00+00:00','LHR','JFK',180),
    (29,'BA0169',11,'2023-12-05T12:30:00+00:00','2023-12-06T09:10:00+00:00','LHR','PVG',137), (30,'BA0031',13,'2023-11-28T17:40:00+00:00','2023-11-29T14:15:00+00:00','LHR','HKG',253),
    (31,'BA0031',14,'2023-11-29T17:40:00+00:00','2023-11-30T14:40:00+00:00','LHR','HKG',240), (32,'BA0031',1,'2023-11-30T17:40:00+00:00','2023-12-01T14:40:00+00:00','LHR','HKG',177),
    (33,'BA0031',4,'2023-12-01T17:40:00+00:00','2023-12-02T14:40:00+00:00','LHR','HKG',245), (34,'BA0027',5,'2023-12-01T20:45:00+00:00','2023-12-02T17:45:00+00:00','LHR','HKG',165),
    (35,'BA0143',7,'2023-11-28T11:10:00+00:00','2023-11-29T01:15:00+00:00','LHR','DEL',255), (36,'BA0257',9,'2023-11-28T18:50:00+00:00','2023-11-29T08:46:00+00:00','LHR','DEL',125),
    (37,'BA0032',10,'2023-11-29T23:00:00+00:00','2023-11-30T05:45:00+00:00','HKG','LHR',111), (38,'BA0032',11,'2023-11-30T23:00:00+00:00','2023-12-01T05:45:00+00:00','HKG','LHR',115),
    (39,'BA0028',12,'2023-11-30T23:40:00+00:00','2023-12-01T06:25:00+00:00','HKG','LHR',277), (40,'BA0032',13,'2023-12-01T23:00:00+00:00','2023-12-02T05:45:00+00:00','HKG','LHR',182);

DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('aircraft',20);
INSERT INTO sqlite_sequence VALUES('flight',40);
INSERT INTO sqlite_sequence VALUES('pilot',4);