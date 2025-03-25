SELECT r.*
FROM Room r
JOIN Zimmerbelegung zb ON r.roomid = zb.roomid
JOIN Buchung b ON zb.buchungid = b.buchungid
WHERE '<Datum>' BETWEEN b.startdate AND b.enddate;

/*SELECT r.*
FROM Room r
JOIN Zimmerbelegung zb ON r.roomid = zb.roomid
JOIN Buchung b ON zb.buchungid = b.buchungid
WHERE '<Startdatum>' <= b.enddate AND '<Enddatum>' >= b.startdate;*/