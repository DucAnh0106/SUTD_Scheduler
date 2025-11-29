#These functions are for processing and uploading data
from check_empty import is_week_empty
from Extract import clean_data, Extract_from_html
from Get_Calendar_Service import get_calendar_service
import time
import multiprocessing
import sys

#These functions are for web scraping
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

def main():
    print("--- GOOGLE AUTHENTICATION ---")
    print("Checking for Google credentials...")
    
    # This line blocks the program until login is finished.
    # Nothing below this line runs until service is created successfully.
    try:
        service = get_calendar_service()
        print("Success! Connected to Google Calendar.")
    except Exception as e:
        print(f"Error connecting to Google: {e}")
        input("Press Enter to exit...") # Keeps`` window open so users can read error
        return

    print("\n--- SUTD LOGIN ---")
    print("Launching Browser...")
    
    # Now we start the Selenium part
    driver = uc.Chrome()
    driver.get("https://myportal.sutd.edu.sg")
    
    #THIS PART IS FOR LOGGING IN AND PRESSING 'My record' AND 'My Weekly Schedule' BUTTONS
    #My record button
    print("Please Log In...")
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CLASS_NAME,"PSHYPERLINKNOUL"))
    )
    print("Logged in. Navigating...")

    My_record_button = driver.find_element(By.CLASS_NAME,"PSHYPERLINKNOUL")
    My_record_button.click()

    #My weekly schedule button
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID,"ADMN_S20160108140638335703604"))
    )
    My_weekly_schedule_button = driver.find_element(By.ID,"ADMN_S20160108140638335703604")
    My_weekly_schedule_button.click()
    
    
    
    #This part is for switching frame (html code inside this frame is secured)
    #That's why we need to switch to this frame to access the below buttons
    
    # Switch frame (do once only)
    print("Switching to Iframe...")
    WebDriverWait(driver, 30).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "ptifrmtgtframe"))
    )
    print("We are inside Iframe now.")
    
    # Enable 'Show AM/PM'
    try:
        ampm_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DERIVED_CLASS_S_SHOW_AM_PM"))
        )
        # Only click if it's NOT currently checked
        if not ampm_checkbox.is_selected():
            driver.execute_script("arguments[0].click();", ampm_checkbox)
            print("  -> Checked 'Show AM/PM'")
        else:
            print("  -> 'Show AM/PM' already active.")
    except Exception as e:
        print(f"  -> Warning: Could not find AM/PM checkbox: {e}")
        
    #Enable 'Show Class Title'
    try:
        title_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DERIVED_CLASS_S_SSR_DISP_TITLE"))
        )
        if not title_checkbox.is_selected():
            driver.execute_script("arguments[0].click();", title_checkbox)
            print("  -> Checked 'Show Class Title'")
        else:
            print("  -> 'Show Class Title' already active.")
    except Exception as e:
        print(f"  -> Warning: Could not find Title checkbox: {e}")

    #Click 'Refresh Calendar' (after 'AM/PM' and 'Show Class Title' is checked)
    print("  -> Clicking 'Refresh Calendar'...")
    # We find the button by its value text since IDs can vary
    refresh_btn = driver.find_element(By.XPATH, "//input[@value='Refresh Calendar']")
    driver.execute_script("arguments[0].click();", refresh_btn)
    
    #WAIT FOR REFRESH
    #Wait for the spinner to appear and then disappear, or just wait for the table to reload
    time.sleep(5)
            
    #This variable is used for counting empty weeks (week with no classes) 
    #(Mainly create this in case there's a recess week, program only stop
    # if there are more than 2 empty weeks)      
    num_of_empty_weeks = 0
    
    #Main Operation
    while True:
        if num_of_empty_weeks >= 2:
            break
        
        print(f"\n--- PROCESSING WEEK  ---")

        #1: GET THE ANCHOR(The Date Text) (Week of Date - Date)
        #We need to know what the current date is, so we can wait for it to change later.
        #We based on this one to know exactly we are looking at the new schedule not old one
        try:
            date_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "PSGROUPBOXLABEL"))
            )
            old_date_text = date_element.text
            print(f"Current Date: {old_date_text}")
        except:
            print("Warning: Could not read date text. Timing might be off.")
            old_date_text = ""

        #Find the table part in html code( actually no need but still put in:)
        table_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "WEEKLY_SCHED_HTMLAREA"))
        )
        
        #2: SCRAPING
        #This is the raw html code we get for every page
        current_html = table_element.get_attribute('outerHTML')

        is_empty = is_week_empty(current_html)
        if is_empty:
            num_of_empty_weeks += 1
            print(f"Result: Week is EMPTY")
        else:
            print(f"Result: Week has CLASSES")

        #3: CLICKING NEXT WEEK
        try:
            # Find the button again (it refreshes every week)
            next_week_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "DERIVED_CLASS_S_SSR_NEXT_WEEK"))
            )
            # Use JavaScript click (More reliable for PeopleSoft)
            driver.execute_script("arguments[0].click();", next_week_btn)
            print("Clicked Next...")
            
        except Exception as e:
            print(f"Error clicking next (End of Term?): {e}")
            break

        #4: ACTUALLY WAIT FOR PAGE TO CHANGE (based on the Anchor text)
        # This prevents the loop from running again until the text "Week of..." actually changes!
        print("Waiting for page update...")
        try:
            WebDriverWait(driver, 15).until(
                lambda d: d.find_element(By.CLASS_NAME, "PSGROUPBOXLABEL").text != old_date_text
            )
            print("Page updated successfully.")
        except:
            print("Timeout waiting for date change. Moving on...")
        
        print("\nAll done! Schedule updated.")
        
        
        #5: UPLOADING TO GOOGLE CALENDAR
        # (Use the 'service' variable you created in Step 1)
        
        #Get the final_schedule dictionary of class in a week for uploading
        #The data inside this dictionary is machine readable
        final_schedule = Extract_from_html(current_html)
        
        #UPLOADING (how many classes)
        print(f"Ready to upload {len(final_schedule)} events.")

        for item in final_schedule:
            #1: Prepare the "Envelope"(The Event Body)
            event_body = {
                'summary': item['Course name'],     #Course name (e.g: Modelling and Analysis)
                'location': item['Location'],       #Room (e.g: 1.414)
                'description': item['Description'], #Type (e.g: Cohort Based Learning)
                'start': {
                    'dateTime': item['Start'],      #ISO format time (for GG calendar)
                    'timeZone': 'Asia/Singapore',   #Time zone
                },
                'end': {
                    'dateTime': item['End'],
                    'timeZone': 'Asia/Singapore',
                },
            }
            
            #2: Hand it to Google API to process
            try:
                event_result = service.events().insert(calendarId='primary', body=event_body).execute()
                
                print(f"Uploaded: {item['Course name']} ({item['Start']})")
                
            except Exception as e:
                print(f"Error uploading {item['Course name']}: {e}")



#Only when we execute the main.py -> the program will run
#if import this file to another file, never work
if __name__ == '__main__':
    # <--- CRITICAL FIX: PREVENTS INFINITE LOOP ON WINDOWS
    multiprocessing.freeze_support() 
    
    try:
        main()
    except Exception as e:
        print(f"Program failed: {e}")
