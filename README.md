# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Architecture Explanation
The cloud architecture consists of a client web app, a postgres cloud db and an Azure Queue & Function
to handle the emails notification. This solves the issue of sending many emails without affecting the
performance of the application.


## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource            | Service Tier                       | Monthly Cost |
|---------------------------|------------------------------------|--------------|
| *Azure Postgres Database* | General Purpose, D8ds v4, 8 vCores | $ 520.34     |
| *Azure Service Bus*       | Premium                            | $ 677.08     |
| *App Service*             | Premium V2                         | $ 146.00     |
| *Azure Functions*         | Premium                            | $ 155.27     |        
| *Storage Accounts*        | Premium                            | $ 150.00     |
Total: $1,804.64 / month