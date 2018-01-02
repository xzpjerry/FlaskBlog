# Flask based web app memo(using MongoDB)

## What can it does?

- Add and delete a text memo with date and time assigned.
- Memos are divided into 3 category, "Today", "Incoming" and "Past 7 days"(memo that is 7 days ago will not be displyed).
- Memos are displyed in a descending order of their date and time (latest first).
- Memos are stored in MongoDB(you need to set up some config).

## What do you need to make it work?
-  A MongoDB database(either on your system or online).
-  Then modify memos/credentials.ini options(see that file).
- 'make start' or 'make run'