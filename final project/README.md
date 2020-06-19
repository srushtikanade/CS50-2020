# CS50 ENVISION
## Introduction
It is a web application that helps to increase productivity.
### languages used
Python,sql for databse querying, javaScript to add interactivity(especially for pomodoro), flask,css,html on the major
#### contents
- planner
- thoughts/idea board
- pomodoro timer
- study cards
- statistics over productivity
- history of all these in descending order

##### specific features
The proj.db database contains 4 tables which are linked by user_id to the user table.
you can change username and password, passwords are hashed for security concerns.
each input for the above contents must be 5 letter min, submit button disabled otherwise.
Particular Error message displayed to make user find the error.
In the index page, tasks,thoughts and cards displayed are limited to Only last 5 entries.
I have used google charts to display the perfomances but have to make them dynamic by using number of entries of each component by querying the database for those inputs and finding their length(for eg.len(tasks/task_id)).
After pomodoro timer goes off, it asks the user for response and records it to display in the table below.
With the current grasp of concepts I could accomplish till these features, planning on adding/altering a few after more practice to acheive competency.

