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
##### Added Features
    1.  Sort the items in the homepage by four features
        - user views
        - user ratings 
        - price low to high 
        - price high to low 
    2. Like or dislike items on sale by ordinary users, except the owner
    3. Users can buy more than one quantity of the fixed price item upto to the total number available.
    4. Users able to see all the price details before they confirm the purchase 
    5. Rating the item after transaction dealed with comments
    6. Sellers can approve the deal (ship the item) or decline the deal, 
       all money transactions make after the item being shipped by the seller. 
    7. Super users are allow to edit the taboo list




