USE eByMazon;

INSERT INTO User(username, password,userType)
VALUES ('admin','password',TRUE),('selina81','1031',FALSE),('hebe83','0330',FALSE),
      ('ella84','0618',FALSE),('feng33','0325',FALSE),('ran90','1203',FALSE),
      ('lu7','0420',FALSE),('ying96','0999',FALSE),('du11','0214',FALSE),
       ('dele22','1111',FALSE);

INSERT INTO OU(ouID, name, cardNumber,email,address,state,phone) VALUES
(2,'Selina Ren','1234567890123456','sren@gmail.com','Taipei 101', 'NY', 9171201031),
(3,'Hebe Tian','0987654321098765','htian@gmail.com','Xinzhu 102','NJ',9174050330),
(4,'Ella Chen','1357924680123456','schen@aol.com','PingDong 103', 'CA', 9177700618),
(7, 'Han Lu', '1234560987610293', 'hlu777@yahoo.com','BeiJing 104','WI', 9177770420),
(6,'Ran Peng','1234987650123456','rpeng@gmail.com','Beijing 101', 'TX', 9171990123),
(5,'Feng Xiao','1232467832498432','fxiao@aol.com','Xichuan 886','PA',9170325330),
(8,'Ying Li','1223342341254525','yli@aol.com','Shangjing 113', 'MI', 9170214334),
(9, 'Du Aa', '2011092334905', 'aadu@yahoo.com','Dangchi 704','TN', 9177110701),
(10,'Xu Chen', '201121334905', 'xuC@yahoo.com','DongGong 555','TN', 9177353701);

INSERT INTO OUstatus(ouID, moneySpend, status) VALUES (2,10.31, 0),(3,0,0),(4,0,0),(5, 777, 1),(6,90, 2), (7,540,1),(8,44,3),(9, 59, 2),(10,45,3);

INSERT INTO GUapplications(username,email,name,cardNumber,address,state,phone) VALUES
('bon18','bonbon@tian.com','Bon Tian','2001938436634','TaoYuan 1023','NJ',9175550330),
('crystine21', 'crystine@gmail.com', 'Crystine Leo', '1232454232', 'Korean Town', 'NY', 9173405968),
('david12', 'david@gmail.com', 'David Yuhas', '12454324123', 'Disney', 'CA', 6463829485);

INSERT INTO Appeal(ouID, message) VALUES (6, 'I very like eByMazon\n please put me back'),(9,'Please do not suspend me');

-- INSERT INTO ItemInfo(itemID, image, title, priceType, saleStatus)

INSERT INTO FriendList(ownerID, friendID, discount) VALUES (2,3,0.05),(3,2,0.10),(4,2,0.03),(2,7,0.05),(7,6,0.05),(7,2,0.05),(8,7,0.15),(7,3,0.05);

INSERT INTO MessageSent(senderID, receiverID, message,sendTime) VALUES
(2,3,'Good Morning!','2019-05-01 09:34:21'),
(3,2,'How have you been?','2019-05-01 11:24:21'),
(2,3,'Great, Thank you purchasing my item!','2019-05-01 14:03:21'),
(3,2,'No problem! Your item is great.','2019-05-02 12:03:21'),
(2,3,'Thanks!','2019-05-02 17:23:21'),
(4,2,'Hi, I want to be your friend','2019-05-06 13:33:21'),
(7,2,'Selina, do you sell earphone?','2019-05-08 13:34:21'),
(2,7,'Yes, I do.','2019-05-09 10:34:21'),
(2,7,'I will post it now, thanks for asking.','2019-05-09 10:35:21'),
(7,2,'No problem!','2019-05-09 11:27:21');

INSERT INTO ItemOwner(itemID, ownerID) VALUES
(1,2),(2,2),(3,2),(4,2),(5,2),(6,3),(7,3),(8,7),(9,2),(10,2),(11,7),(12,7);



-- SELECT friendID,discount,username FROM FriendList
--   JOIN User ON friendID=ID
--   WHERE ownerID = 2;
--
-- DELETE FROM FriendList WHERE ownerID=8 AND friendID = 7;
