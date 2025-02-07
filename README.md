# Real Estate Management System

## Steps to reproduce this project:
### 1. Clone the repository
```git clone https://github.com/Skanda-P-R/Real-Estate-Management-System.git```

### 2. Install Dependencies
```pip install -r requirements.txt```

### 3. Install Xampp
Download and install the XAMPP tool from [here](https://www.apachefriends.org/download.html).

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
