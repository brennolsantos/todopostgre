# ToDO Rest API

This Rest API uses PostgreSQL, Docker and Django to implements
a ToDo application. The application implement Tasks and Alarms

# Tasks

A small note where the users can write anything they want to do,
with each tasks only showed to its respective user. The tasks have
a dead_line, and if the current date is up-to 3 or more days over the
dead_line, the task is removed by a special view

# Alarms

Alarms is similar to Tasks, but they only can be showed if the alarm-date
is the current date or up-to 2 days over. If is 3 or more days over, the alarms
are removed by a special view

## URLS

# api/

- api/tasks - POST, GET, PUT, DELETE
- api/alarms - POST, GET, PUT, DELETE

# auth/

- auth/token-auth - POST
- auth/register - POST

The user can be registeres using the default django model user
