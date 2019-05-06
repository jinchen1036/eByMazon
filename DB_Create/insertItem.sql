USE eByMazon;
INSERT INTO ItemView(itemID) VALUES (1),(2),(3),(4),(5),(6);

-- INSERT INTO KeywordRecord(keyword, itemID) VALUES
-- ('CD',1),('SHE',1),('DVD',2),('SHE',2),
-- ('BOOK',3),('HARRY POTTER',3),('J. K. ROWLING',3),
-- ('BOOK',4),('THE HUNGER GAMES',4),('SUZANNE COLLINS',4),
-- ('LAPTOP',5),('SAMSUNG',5),('17 INCH',5),
-- ('APPLE',6),('MAC BOOK',6),('13 INCH',6);

INSERT INTO FixedPrice(itemID, price, availableNum) VALUES
(1,15.99,10),(2,17.79,20),(3,7.99,5),(4,12.50,20);

INSERT INTO ItemBid(itemID, startPrice) VALUES (5,300),(6,800);
INSERT INTO BidRecord (itemID,bidderID, bidPrice) VALUES (5,4,320),(5,2,330),(5,5,350);
INSERT INTO Transaction(itemID, buyerID, singlePrice, priceTotal, numDeal, shippingStatus)
VALUES (1,7,15.99,16.40,1,FALSE ),(1,6,15.99,17.30,1,TRUE),(2,5,7.99,9,1,FALSE),(2,6,7.99,18,2,FALSE),(1,9,22,24,1,FALSE );
INSERT INTO Complaint(itemID, complainerID, description, justified) VALUES
(1,7,'Arrive Too Late',TRUE),(1,6,'Broken Item',FALSE),(2,9,'Wrong Shipment',FALSE );
INSERT INTO ItemRate(itemID,raterID, rating,description) VALUES
(1,6,4,'Good Product'),(1,7,3,'Nice Sound');
-- Electronic, Home, Grocery, Clothes,Furniture,Education,Music
INSERT INTO Category(category, itemID) VALUES
('Music',1),('Music',2),('Education',3),('Education',4),('Electronic',5),('Electronic',6);

INSERT INTO Taboo(word) VALUES ('subway'),('CSC'),('TG'),('super'),('winner');

INSERT INTO ouBlacklist VALUES ('block123'),('test123');

INSERT INTO Appeal(ouID, message) VALUES(9,'I WANT TO APPEAL!');

INSERT INTO Notification VALUES ('Dolls'),('Phone'),('Ink');
INSERT INTO searchKeyword(keyword, frequency) VALUES ('DVD', 3),('CD', 6),('Book', 8),('Computer', 7);
INSERT INTO Warning(ouID, warningID,description) VALUES (3, 0,'Low Rating'), (2, 1,'2 compliants');

