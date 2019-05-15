# eByMazon
Mini e-Business platform combine features from eBay and amazon system, implemented using python and MySQL.



## Get Started
Below is instruction to run our project in your local machine. 

#### Prerequisites
- [Python3](https://www.python.org/downloads/)
- [MariaDB](https://mariadb.org/)

#### Steps
1.Clone and install modules
```
git clone https://github.com/jinchen1036/eByMazon.git
cd eByMazon
pip3 install -r requirements.txt
```

2.Go to db_init.py in DB_Create folder, enter your username and password for your own mysql

3.Run python file to start initialize eByMazon database
```
python3 DB_Create/db_init.py
```

4.Go to GlobalVariable.py in scr folder, enter your username and password for your own mysql

5.Run the Manager.py to start our application
```
python3 scr/Manager.py
```

## Note
For the users in our system -> Check the insertValues.sql in DB_Create folder 

##### Required Features
    1. Guest Users
        - Search and browse through the items on sale.
        - View the ordinary users comments for the fixed item
        - Sign up to be the ordinary user
    2. Ordinary Users
        - Search, browse, and purchase the items on sale.
        - Edit profile, password
        - Post fixed price item or bidding item
        - View transaction history
        - View Complains and Warnings
        - Edit friend list
        - Communicate with friends
        - Various condition on warning will be added by the system
        - Automatically promote or depromote to VIP status with various constraints
        - Suspend by system if receive two or more warnings, allow to appeal.
        - Allow to give complain to the purchased item
        - Allow to deal a sale
    3. Super Users
        - Manage GU Applications (approve or decline)
        - View all the transaction
        - Manage OU Appeals (approve or decline)
        - View all the OU informations
        - Remove OU based on judgement
        - Manage the post items by OU (approve or decline)
        - Process the complains by OU (justify or decline) 
        - Remove the items that already been approved
        - View OU Blacklist and Item Blacklist
    4. Homepage
        - For GU: Items list in the order by popularity (keyword search frequency by GU and OU) 
        - For OU: Items list in the order by OU likeness (keyword search frequency of login OU)
        
##### Creative Features
    1.  Sort the items in the homepage by four features
        - user views
        - user ratings 
        - price low to high 
        - price high to low 
    2. Super Users allow to edit the taboo list
    3. Ordinary Users
        - Allow to buy more than one quantity of the fixed price item up to the total available amount.
        - View all the price details before they confirm the purchase 
        - Like or dislike products, can only choose to like or dislike once. 
        - Owner cannot like his/her own product.
        - Rate and comments the items they purchased successfully.
        - Add friends with different discounts, delete friend, communicate with friends, and change friends' discount
        - Bidding transaction will be handled automatically by the system when reach bidding end time, and the second higher bidder will automocally purchased the bidding item.
        - All money transactions make after the item being shipped by the seller (approve the deal)  
    


