# Flask based web app blog(using MongoDB as database)

## What can it does?

- Having a basic access control, one need to login to modify blog's contents.
- Add and delete a markdown text blog with date and time assigned.
- Contents are divided into 3 category, "Today", "Incoming" and "Past 7 days"
- Contents are displyed in a descending order of their date and time (latest first).
- Contents are stored in MongoDB(you need to set up some config).

## What do you need to make it work?
-  A MongoDB database(either on your system or online).
-  Then modify memos/credentials.ini options(see that file).
- 'make start' or 'make run'
