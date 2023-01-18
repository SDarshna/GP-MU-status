# GP-MU-status
Script to check where a GP MU has logged in from/ How many GP Users have connected from a country location

Input:
/MU_Status.py --help                   
usage: MU_Status.py [-h] [-t1 T1SECRET] [-option OPTION] [-user USER]
                    [-loc LOCATION]

Checking MU Status

optional arguments:
  -h, --help            show this help message and exit
  -t1 T1SECRET, --T1Secret T1SECRET
                        Input secret file in .yml format for the tenant(T1)
  -option OPTION, --Option OPTION
                        user/loc to query based on user or location
  -user USER, --User USER
                        Given a user, check the location from where the user is
                        logged in
  -loc LOCATION, --Location LOCATION
                        Given a User location country, list the mobile Users
(base) dsubashchand@M-JY4VCQYQ64 MU status % 

Input CLI:
1. To check the location of a MU given GP user name: 
./MU_Status.py -t1 T1-secret.yml -user alice1@panwsase.com  -option user
2. To check the number of GP users connected from "Unisted States" country location
./MU_Status.py -t1 T1-secret.yml -loc "United States"  -option loc      

Output:
1. 
+---------------------+---------------+-------------+-----------------------+
| GP-User-Name        | User Location | PA Location | User Country Location |
+=====================+===============+=============+=======================+
| alice1@panwsase.com | Zimmerman     | US Central  | United States         |
+---------------------+---------------+-------------+-----------------------+
2. 
+--------------------------+---------------+-------------+-----------------------+
| GP-User-Name             | User Location | PA Location | User Country Location |
+==========================+===============+=============+=======================+
| AliceCooper@panwsase.com | San Jose      | US Central  | United States         |
+--------------------------+---------------+-------------+-----------------------+
| alice1@panwsase.com      | Zimmerman     | US Central  | United States         |
+--------------------------+---------------+-------------+-----------------------+
