SELECT b.*, r.*
FROM Buchung b
JOIN Zimmerbelegung zb ON b.buchungid = zb.buchungid
JOIN Room r ON zb.roomid = r.roomid;