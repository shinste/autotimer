import pygetwindow as gw
import time
import sqlite3
from datetime import date
# import threading
# import queue

    # Initializing the database
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
    # print(f"Timer has stopped for {timed_program}")
    # conversion to minutes timed
    if timed_program:
        time_spent_min = (end_time - start_time) / 60
        # check how many times this program shows up (1 or 0)
        cursor.execute("SELECT COUNT(*) FROM program_usage WHERE program_name = ?", (timed_program,))
        count = cursor.fetchone()[0]
        cursor.execute("SELECT DISTINCT date FROM program_usage WHERE program_name = ?", (timed_program,))
        date_list = cursor.fetchall()
        # print(date_list)
        # last_date = cursor.fetch()[0]
        notToday = True
        for dates in date_list:
            if str(date_program) in dates:
                notToday = False
        # if this program hasn't been seen in database we add it as a row
        # print(notToday)
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
    
# def start():
#     start_time = time.time()
#     date_program = date.today()
#     timed_program = active_program
#     print(f"Timer for {active_program} has Started!")

def program_order():
    cursor.execute("SELECT program_name, time_spent_mins FROM program_usage WHERE date = ? ORDER BY time_spent_mins DESC", (date_program,))
    list_programs = cursor.fetchall()
    for pair in list_programs:
        name, time = pair
        time = round(time, 2)
        if time > .5:
            if time < 60:
                print(f"You've Spent {time} Minutes on {name} Today!")
                time = round(time, 2)
            else:
                hours = round(time // 60, 0)
                time = time - hours * 60 
                time = round(time, 2)
                print(f"You've Spent {hours} Hour(s) and {time} Minutes on {name} Today!")

while True:
    try:
        #capturing the active window and record the name into a variable
        active_window = gw.getActiveWindow()
        if active_window:
            active_program = active_window.title
            
            # 
            if active_program:
                # I don't want powershell to be timed since its my terminal
                if "PowerShell" not in active_program:
                    if "YouTube" in active_program:
                        active_program = "YouTube"
                    elif "LeetCode" in active_program:
                        active_program = "Leet Code"
                    active_program = active_program.split(" - ")[-1]
                    if active_program != timed_program:
                        if timed_program != None:
                                end_time()
                        start_time = time.time()
                        date_program = date.today()
                        timed_program = active_program
                        # print(f"Timer for {active_program} has Started!")
                # this is to stop the timer if a tab is being changed to powershell
                elif timed_program != None:
                    end_time()
                    timed_program = None
                
        time.sleep(1)

    except KeyboardInterrupt:
        end_time()
        program_order()
        conn.close()
        break
    
# input_queue = queue.Queue()

# main_thread = threading.Thread(target=main)
# main_thread.start()
    
    