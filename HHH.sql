-- Tabelle: Gast
CREATE TABLE Gast (
    gastid INT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
);

-- Tabelle: Hotel
CREATE TABLE Hotel (
    hotelID INT PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    rating DOUBLE
);

-- Tabelle: Room
CREATE TABLE Room (
    roomID INT PRIMARY KEY,
    hotelID INT,
    number VARCHAR(20),
    type VARCHAR(50),
    price DOUBLE,
    available BOOLEAN,
    FOREIGN KEY (hotelID) REFERENCES Hotel(hotelID)
);

-- Tabelle: Buchung
CREATE TABLE Buchung (
    buchungid INT PRIMARY KEY,
    gastid INT,
    startdate DATE,
    enddate DATE,
    status VARCHAR(50),
    FOREIGN KEY (gastid) REFERENCES Gast(gastid)
);

-- Tabelle: Zahlung
CREATE TABLE Zahlung (
    paymentID INT PRIMARY KEY,
    bookingID INT,
    amount DOUBLE,
    paymentDate DATE,
    status VARCHAR(50),
    FOREIGN KEY (bookingID) REFERENCES Buchung(buchungid)
);

-- Tabelle: Zimmerbelegung (Join-Tabelle für M:N-Beziehung)
CREATE TABLE Zimmerbelegung (
    buchungid INT,
    roomid INT,
    PRIMARY KEY (buchungid, roomid),
    FOREIGN KEY (buchungid) REFERENCES Buchung(buchungid),
    FOREIGN KEY (roomid) REFERENCES Room(roomid)
);