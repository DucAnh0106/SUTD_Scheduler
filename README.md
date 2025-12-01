# 🗓️SUTD Schedules to Google Calendar
This tool scrapes your weekly schedule from SUTD portal and automatically syncs it to your Google Calendar

## ⭐Key notes⭐:
- You only have to go through the below setting up process once.
=> For subsequent times, the program already knows who you are so you just need to press run and log into MyPortal (make sure you still keep the program in your computer, if not then you have to repeat the setting up)
- At the beginning of every term, you must run the program again to get your schedules to Google Calendar


## 1️⃣ First to do
**Step 1**: Open your web browser and go to [Google Cloud Console](https://console.cloud.google.com/)

**Step 2**: In the top bar, click the project drop down (it might say 'My first project') next to the text **Google Cloud**
* Click **New project**
* Give the project a name and click **Create** (No need to state organization)
* Wait for the project to be successfully created

**Step 3**: Enable Google Calendar API
* Navigate to the **APIs & Services** dashboard.
* Click **"+ Enable APIs and service"** at the top
* Scroll down and search for **Google Calendar API**
* Click on that button and Click the **Enable** button

**Step 4**: 
* In the leftside bar, go to overview and press **Get Started**
* Name your app, and choose your own email as the user support email
* For audience, choose external
* For contact information, you can choose any email of yours
* After that, you finish and press **Create**

**Step 5**: Create a JSON file that the python scripts need to talk to google calendar
* Go back to **Google Cloud console*
* Look for **APIs & Services** again
* In the top bar, click **"+ Create credentials"** and select **OAuth client ID**
* Select **Desktop app** from the drop down menu and click **Create**
* After that, a window will pop up and just click **DOWNLOAD JSON**
* Rename it to **credentials.json**

## Main Process

Which operating system are you using?

* [**Mac OS**](#mac-os)
* [**Windows**](#windows)

### Mac OS

**Option 1**: 'I just need my schedules synced to Google Calendar'
* Download this Mach-O file via this [link](https://github.com/DucAnh0106/SUTD_Scheduler/releases/download/v1.0.0/main)
* Create a folder in your Desktop and name it **"SUTD_Scheduler"**
* Put your **credentials.json** file inside this folder
* Open your terminal (Command + Space -> Type "terminal" and press Enter)

Then, copy and paste these one by one in your terminal:
```
cd Desktop/SUTD_Scheduler
chmod +x main
./main
```
* Wait a bit and follow the steps on the screen


**Option 2**: 'I want to run the code myself'
* Make sure you have python installed in your IDE (e.g Visual studio code)
* Download the ZIP file from GitHub repo,unzip and open it in your IDE
* In your IDE terminal, copy and paste this line:
```
pip install selenium undetected-chromedriver google-auth-oauthlib google-auth-httplib2 google-api-python-client beautifulsoup4
```
* After that, just run main.py and follow the steps on the screen


### Windows

**Option 1**: 'I just need my schedules synced to Google Calendar'
* Download this .exe file via this [link](https://github.com/DucAnh0106/SUTD_Scheduler/releases/download/v1.0.0/main.exe)
* Create a folder in your Desktop and name it **"SUTD_Scheduler"**
* Put your **credentials.json** file inside this folder
* Go to **SUTD_Scheduler** folder then double-click on the main.exe file
* After that, just follow the steps on the screen

**Option 2**: 'I want to run the code myself'
* Make sure you have python installed in your IDE (e.g Visual studio code)
* Download the ZIP file from GitHub repo,unzip and open it in your IDE
* In your IDE terminal, copy and paste this line:
```
pip install selenium undetected-chromedriver google-auth-oauthlib google-auth-httplib2 google-api-python-client beautifulsoup4
```
* After that, just run main.py and follow the steps on the screen
