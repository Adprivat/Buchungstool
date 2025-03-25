SELECT b.*
FROM Buchung b
JOIN Zimmerbelegung zb ON b.buchungid = zb.buchungid
WHERE zb.roomid = <Zimmer-ID>;