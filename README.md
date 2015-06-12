# WufooDateScraper
Python program to search for entries in a wufoo form based on a string date

This program is used to scrape the entries in a wufoo form and look for strings
being used as dates that are on or after "today minus x" number of days.

Our use case for this program is that we were using Wufoo to allow someone to register for
events. We wanted to have the user select from a drop down box of available dates, but
we cannot use date conditions as selection criteria on non-date type fields. We couldn't use
a date picker field because this would have allowed the user to select any date, not just those we specified.
Since a user might be registering for an event date weeks or months in advance, it was not always easy to find
registrations for recent events in our entry list.
Using this program, we could see who had registered for an event date within the last week and follow up
appropriately
This could also be easily modified to look for name of individuals who have registered for upcoming events.

setup.py is included for creating a standalone executable via py2exe. 
