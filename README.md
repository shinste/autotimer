# Autotimer Script

## Introduction
This Python script is my very first project that serves the purpose of timing how long a user spends on each program on their computer. I wanted to create something that I would find myself using everyday; this gives me extra motivation to implement features that are very practical to the user. In this script we utilize the 'pygetwindow' library to track the time spent on each program and use a SQLite database to store it.

## Features
* Tracks the time spent on active programs
* Uses a SQLite database to store the time
* Customizes timings for specific programs within Chrome (Youtube, LeetCode)
* Excludes specific programs from being timed (PowerShell Terminal)

## Get Started
### Installation
The only library that needs to be installed is pygetwindow. To install, run 'pip install pygetwindow' on your terminal.

## How it Works
### Initial
* Creates a SQLite database if one hasn't already been made by the program previously.
* Prints a confirmation message: "The Autotimer has Started".
### Start of tracking
* Grabs the program name, checks if it's a valid program (excluding PowerShell)
* Separate general Chrome programs from the Youtube and LeetCode Chrome programs 
* Checks whether the current program is the first occurrence of tracking and starts the timer for that program
* If the script has been timing a program, it will check if there has been a change and start the timer for the new program while ending the time for the old program
### Database Updating
* Updates the times in the database, and handles new program entries
* Will separately record program times for the current date
### Display
* Once you end the program, it will display the tracked times for each program (Ordered by most usage)

## Notes
* Script will run every second for accurate tracking
* Programs with less than 30 seconds of usage are not displayed at the end
