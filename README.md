# Real Estate Management System

## Steps to reproduce this project:
### 1. Clone the repository
```git clone https://github.com/Skanda-P-R/Real-Estate-Management-System.git```

### 2. Install Dependencies
```pip install -r requirements.txt```

### 3. Install Xampp
Download and install the XAMPP tool **Version 8.0.30** from [here](https://www.apachefriends.org/download.html).

### 4. Import the SQL template and data
- Run the XAMPP Control Panel application, and Click on "Start" button for Apache and MySQL Module.
- Then Click on the "Admin" button for MySQL Module. A page with URL http://localhost/phpmyadmin/ will open, here follow the below steps:
  - Click on "Databases" in the top toolbar
  - In the "Create database" input section, type the "Database name" as ```real_estate_db```, then click the "Create" button.
  - Then, the newly created database opens up. NOw in the top toolbar, select the "Import" button, then click on "Choose File", then navigate to this cloned repository, and select the ```real_estate_db.sql``` file.
  - Then scroll all the way below, and Click on "Import" button. Now, all the tables would be successly imported.

### 5. Run the Flask Server
Navigate to this cloned repository, and run: ```python app.py```. Then open http://127.0.0.1:5000/ in your browser, the web app would be displayed.

### Note:
These are the user emails and passwords set:
- skandapr@gmail.com | Admin
  - skanda@12345
- sneha@gmail.com | Owner
  - sneha@12345
- phaniraj@gmail.com | Customer
  - phaniraj@12345
- rekha@gmail.com | Customer
  - Rekha@12345
- vaibhav@yahoo.in | Owner
  - Vaibhav@12345

The emails can be found out in the ```users``` table in the database, but the passwords are encrypted, hence, you can use these users from the database, or register your own users.

### 6. Deploy the Application to the web
1. Visit https://ngrok.com/ and sign in if you have an account, or sign up by creating a new account.
2. Next in this repository path, type the command ```ngrok config add-authtoken your_auth_token```. Replace ```your_auth_token``` with your ngrok auth token, which can be found in your dashboard.
3. Next, run ```python app.py```, which will run the flask server, and the website. Don't forget to start the MySQL server from the XAMPP Control Panel too.
4. Finally, open one more cmd in the same repository path, and run ```ngrok http 5000```. The ngrok instance will run, and a URL for the website will be generated, which will be somthing like this: ```https://1111-2222-3333-4444-5555-6666.ngrok-free.app```. You can use this link on any device, and access the Real Estate Management System anywhere, anytime, anyplace.