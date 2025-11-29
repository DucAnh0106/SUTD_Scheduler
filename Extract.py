from bs4 import BeautifulSoup
from datetime import datetime

#This function is meant to use to clean the extracted data from html, 
#make it readable by machine (Google calendar can read)
def clean_data(date_str, time_str):
    Current_year = str( datetime.now().year )
    
    #split the date str -> get sth like 4 Nov 2025 only
    date_str = date_str + " " + Current_year
    date_str_split = date_str.split(" ")
    date_str = f"{date_str_split[1]} {date_str_split[2]} {date_str_split[3]}"
    
    #split the time_str
    time_str_split = time_str.split(" - ")
    
    #get 2 combined string 4 Nov 2025 9:00AM -> 4 Nov 2025 11:30AM
    start = date_str + " " + time_str_split[0]
    end = date_str + " " + time_str_split[1]
    
    #convert 2 strings above to machine readable language
    start_object = datetime.strptime(start, '%d %b %Y %I:%M%p')
    end_object = datetime.strptime(end, '%d %b %Y %I:%M%p')
    
    
    return start_object.isoformat(), end_object.isoformat()

#This function is used for extracting data
def Extract_from_html(html_file):
    #Load raw html file in
    soup = BeautifulSoup(html_file, "html.parser")
    #Find the table
    table = soup.find("table", id = "WEEKLY_SCHED_HTMLAREA")

    #Find first table row and loop through table header -> get dates
    row_list = table.find_all("tr")
    first_row = row_list[0]

    header_list = first_row.find_all("th")
    dates_list = []
    
    for i in range( len(header_list) ):
        #the only the readable text inside the tag content and remove whitespace by strip
        dates = header_list[i].get_text(separator = ' ', strip = True)     
        if dates != 'Time':
            dates_list.append(dates)
    #=> finish extracting all the dates
    
    time_tracker = 0
   
    final_schedule = []
    #This part is taking the time rows into account (8:00AM, 9:00AM ...)
    tracker = [0] * 7
    row_list.remove( row_list[0] )
    data_rows = row_list

    for row in data_rows:
        # Get all <td> tags in this specific row
        cells = row.find_all("td")
        
        if time_tracker > 0:
            html_cell_index = 0
            time_tracker -= 1
        
        else:
            # We need an index to know which 'td' we are grabbing from the HTML list
            # We start at 1 because index 0 is the "Time" label (e.g., "9:00AM")
            html_cell_index = 1 
            if cells:
                # Check if this Time cell spans multiple rows
                time_rowspan = int(cells[0].get('rowspan', 1))
                if time_rowspan > 1:
                    time_tracker = time_rowspan - 1
        
        # Loop through the 7 virtual days (0=Mon, 1=Tue...)
        for day_index in range(7):
            
            if tracker[day_index] > 0:
                tracker[day_index] -= 1
                continue # Skip to the next day

            if html_cell_index < len(cells):
                # Grab the cell
                current_cell = cells[html_cell_index]
                
                #if rowspan exists and > 0, update tracker[day_index] in order to block later row
                rowspanned = int( current_cell.get('rowspan', 1) )
                if rowspanned > 1:
                    tracker[day_index] = rowspanned - 1
                    
                #It's extraction time!!!!!!
                if current_cell.find("span"):
                    class_data = current_cell.span.get_text(separator = "|", strip = True)
                    components = class_data.split("|")
                    
                    #get the cleaner to clean the data and have the final input for gg calendar
                    start_iso, end_iso = clean_data(dates_list[day_index], components[3])
                    
                    final_schedule.append({
                        'Course name': components[1], 
                        'Description': components[2], 
                        'Location': components[4],
                        'Start' : start_iso,
                        'End' : end_iso})
                    
                    #format: Class|Course name|Type|Time|Location
                    #we only need Course name, type, time, location 
                
                # Move to the next HTML cell for the next day
                html_cell_index += 1
    
    return final_schedule

