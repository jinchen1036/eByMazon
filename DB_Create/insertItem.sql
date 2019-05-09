USE eByMazon;
INSERT INTO ItemView(itemID,frequency) VALUES
(1,20),(2,15),(3,0),(4,0),(5,10),(6,12),(7,9),(8,0),(9,30),(10,7),(11,33),(12,22);

-- INSERT INTO KeywordRecord(keyword, itemID) VALUES
-- ('CD',1),('SHE',1),('DVD',2),('SHE',2),
-- ('BOOK',3),('HARRY POTTER',3),('J. K. ROWLING',3),
-- ('BOOK',4),('THE HUNGER GAMES',4),('SUZANNE COLLINS',4),
-- ('LAPTOP',5),('SAMSUNG',5),('17 INCH',5),
-- ('APPLE',6),('MAC BOOK',6),('13 INCH',6);

INSERT INTO FixedPrice(itemID, price, availableNum) VALUES
(1,15.99,10),(2,17.79,30),(3,7.99,5),(4,12.50,20),(7,213.22,5),(8,57.50,50),(10,78.99,20),(11,9.99,100),(12,17.77,30);

INSERT INTO ItemBid(itemID, startPrice) VALUES (5,300),(6,800),(9,330);

INSERT INTO BidRecord (itemID,bidderID, bidPrice) VALUES
(5,4,320),(5,5,330),(5,3,350),(6,7,850),(6,3,900),(9,3,340),(9,5,350),(9,4,360),(9,6,500);

INSERT INTO Transaction(itemID, buyerID, singlePrice, priceTotal, numDeal, shippingStatus) VALUES
(1,3,15.99,51.75,3,FALSE ),
(12,3,17.77,19.17,1,TRUE ),
(10,3,78.99, 170.42,2,TRUE),
(11,3, 9.99, 107.76,10,FALSE ),
(1,6,15.99,17.30,1,TRUE),
(2,3,17.79,38.38,2,FALSE),
(2,5,17.79,18.32,1,TRUE),
(1,9,22,24,1,FALSE),
(12,4,17.77,39.18,2,FALSE),
(10,4,78.99,87.09,1,TRUE),
(11,5,9.99,20.58,2,FALSE),
(7,2,213.22, 210.82,1,FALSE),
(1,7,15.99,15.47,1,FALSE );


INSERT INTO Complaint(itemID, complainerID, description, justified) VALUES
(1,6,'Arrive Too Late',TRUE),(2,5,'Broken Item',FALSE),(10,4,'Wrong Shipment',FALSE);


INSERT INTO ItemRate(itemID,raterID, rating,description) VALUES
(1,6,4,'Good Product but long time delivery'),(2,5,1,'Broken DVD, cannot play'),(10,4, 3.5,'Taste Good'),
(12,3,5,'Great Music'),(10,3,5,'Smell so Good. I love it!!!!');

-- Electronic, Home, Grocery, Clothes,Furniture,Education,Music
-- INSERT INTO Category(category, itemID) VALUES
-- ('Music',1),('Music',2),('Education',3),('Education',4),('Electronic',5),('Electronic',6);

INSERT INTO Taboo(word) VALUES ('subway'),('CSC'),('TG'),('super'),('winner');

INSERT INTO ouBlacklist VALUES ('block123'),('test123');


INSERT INTO Notification VALUES ('headphone'),('Phone'),('ink');

INSERT INTO searchKeyword(keyword, frequency) VALUES ('Chocolate', 3),('watch', 6),('CD', 8),('Computer', 7);
-- INSERT INTO Warning(ouID, warningID,description) VALUES (3, 0,'Low Rating'), (2, 1,'2 compliants');

