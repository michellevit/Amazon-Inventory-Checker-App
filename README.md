# Amazon Inventory Checker App


![Django Version](https://img.shields.io/badge/Django-4.0.3-0c4a30.svg)
![Python Version](https://img.shields.io/badge/Python-3.10.4-ffdb4f.svg)
![React Version](https://img.shields.io/badge/React-18.2.0-61dafb.svg)


An application that intakes an Amazon order request spreadsheet, calculates the total requested inventory, allows users to input their actual inventory, and calculates the optimal orders to confirm based on inventory and the minimum order value threshold (to keep shipping costs reasonable).


## Table of Contents
- [How to Use](#how-to-use)
- [How to Create a Virtual Environment](#how-to-venv)
- [Troubelshooting](#troubleshooting)


## How to Use<a name="how-to-use"></a>
- After making code changes to file_processor.py - run: 
  - `.\rebuild-app.bat`


## How to Create a Virtual Environment<a name="how-to-venv"></a>
- Ensure Python is installed on your system
- Open a terminal
- Navigate to project's root directory
- Run: `python -m venv venv`
- Activate the virtual environment: `.\venv\Scripts\activate`
- If you have a requirements.txt file:
  - Run: `pip install -r requirements.txt`


## Troubleshooting<a name="troubleshooting"></a>
- Make sure app is closed before running `.\rebuild-app`


Project Directory:
Amazon-Inventory-Checker-App
| - build/
| - dist/
| | - file_processor
| - resources
| | - app_icon.ico
| - uploaded_files/
| - venv/
| - file_processor.py
| - file_processor.spec
| - requirements.txt



*** 


# Pull Request: Add Blog Subscription Feature

## Summary
This pull request introduces a new subscription feature to Andrew Paxson's website, enabling visitors to subscribe for email notifications whenever a new blog post is published. The feature leverages a Cloudflare Worker to handle API requests and integrates with Mailchimp for managing subscriptions and sending notifications.

## Enhancements:

### RSS Generator Script:
 - Added a script to generate an RSS feed (rss.xml) for blog posts.
### Subscribe Component:
 - Implemented a Subscribe component that allows users to submit their email and first name to subscribe to blog updates.
- Integrated the component into relevant pages of the website.

### Cloudflare Worker:
 - Added reference code for a Cloudflare Worker (subscribe-worker.js) to handle API requests to Mailchimp.

### README Updates:
  - Updated the README with instructions for setting up the website on Cloudflare.
  - Provided detailed steps for setting up the Cloudflare Worker and configuring a Mailchimp RSS-to-email campaign.

## Important Notes:

### Setup Required:

 - The subscription feature requires additional setup steps to function correctly. These steps involve configuring a Cloudflare Worker and setting up a Mailchimp RSS-to-email campaign.
- Detailed setup instructions are provided in the README under the section 'How to Set Up the Blog Mailing List'

### Why a Cloudflare Worker:
- Cloudflare Workers provide a serverless solution for backend functionality, which is essential for the free tier as it does not support traditional backend services. This allows for handling API requests securely and efficiently.

### Estimated Setup Time:
 - The entire setup process, including configuring Mailchimp and the Cloudflare Worker, should take less than 30 minutes.

Please review the changes and let me know if there are any questions or further adjustments needed. Thank you!

