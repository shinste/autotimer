import pygetwindow as gw
import time
import sqlite3
from datetime import date


#initializing the database
conn = sqlite3.connect('program_usage.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS program_usage (program_name TEXT, time_spent_mins REAL, date REAL)')

active_program = None
start_time = None
timed_program = None
prev_program = None
date_program = None

print("The Autotimer has Started")


# method to end the timer for the specific program and input that
# time to the database. Will update existing time but will create
# new entry if this is that programs first time being timed.
def end_time():
    # record end time
    end_time = time.time()
    if timed_program:
        # conversion to minutes timed
        time_spent_min = (end_time - start_time) / 60
        # check how many times this program shows up (1 or 0)
        cursor.execute("SELECT COUNT(*) FROM program_usage WHERE program_name = ?", (timed_program,))
        count = cursor.fetchone()[0]
        #check dates
        cursor.execute("SELECT DISTINCT date FROM program_usage WHERE program_name = ?", (timed_program,))
        date_list = cursor.fetchall()
        #checking to see if the recorded time is in the right day
        notToday = True
        for dates in date_list:
            if str(date_program) in dates:
                notToday = False
        # if this program hasn't been seen in database or a different day we add it as a row
        if count == 0 or notToday:
            cursor.execute('INSERT INTO program_usage (program_name, time_spent_mins, date) VALUES (?, ?, ?)',
                    (timed_program, time_spent_min, date_program))
        # otherwise we just update existing row
        else:
            cursor.execute("UPDATE program_usage SET time_spent_mins = time_spent_mins + ? WHERE program_name = ? AND date = ?",
                    (time_spent_min, timed_program, date_program))
        #commit changes
        notToday = True
        conn.commit()

def program_order():
    cursor.execute("SELECT program_name, time_spent_mins FROM program_usage WHERE date = ? ORDER BY time_spent_mins DESC", (date_program,))
    list_programs = cursor.fetchall()
    for pair in list_programs:
        name, time = pair
        time = round(time, 2)
        #dont include programs for times that are less than half a minute
        if time > .5:
            #output when time is less than an hour
            if time < 60:
                time = round(time, 2)
                print(f"You've Spent {time} Minutes on {name} Today!")
            else:
            #conversion for when time is over an hour
                hours = round(time // 60, 0)
                time = time - hours * 60 
                time = round(time, 2)
                print(f"You've Spent {hours} Hour(s) and {time} Minutes on {name} Today!")

while True:
    try:
        #capturing the active window and record the name into a variable
        active_window = gw.getActiveWindow()
        #execute if theres a valid window
        if active_window:
            #capturing title of active window
            active_program = active_window.title
            if active_program:
                #I don't want powershell to be timed since its my terminal
                if "PowerShell" not in active_program:
                    #customizing code to individually time youtube and leetcode
                    if "YouTube" in active_program:
                        active_program = "YouTube"
                    elif "LeetCode" in active_program:
                        active_program = "Leet Code"
                    #I only want the tab title
                    active_program = active_program.split(" - ")[-1]
                    #if the new program not equal to prev program we must update variables
                    #and end time for prev program
                    if active_program != timed_program:
                        if timed_program != None:
                                end_time()
                        start_time = time.time()
                        date_program = date.today()
                        timed_program = active_program
                # this is to stop the timer if a tab is being changed to powershell
                elif timed_program != None:
                    end_time()
                    timed_program = None
        #waits 1 second before continuing while loop
        time.sleep(1)

    except KeyboardInterrupt:
        end_time()
        program_order()
        conn.close()
        break
    
