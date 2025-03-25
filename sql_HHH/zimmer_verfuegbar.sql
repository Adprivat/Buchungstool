SELECT r.*
FROM Room r
WHERE r.roomid NOT IN (
    SELECT zb.roomid
    FROM Zimmerbelegung zb
    JOIN Buchung b ON zb.buchungid = b.buchungid
    WHERE '<Startdatum>' <= b.enddate AND '<Enddatum>' >= b.startdate
);