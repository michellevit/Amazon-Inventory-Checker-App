# Boilerplate Code for Django-React-PostgreSQL-Heroku App

![Django Version](https://img.shields.io/badge/Django-4.0.3-0c4a30.svg)
![Python Version](https://img.shields.io/badge/Python-3.10.4-ffdb4f.svg)
![React Version](https://img.shields.io/badge/React-18.2.0-61dafb.svg)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791.svg)
![Heroku](https://img.shields.io/badge/Platform-Heroku-6762a6.svg)


Boilerplate code for setting up a Django-React-PostgreSQL application on Heroku. 


## Table of Contents
- [Prerequisites](#prerequisites)
- [How To Set Up Project](#how-to-set-up) 
- [Useful Heroku Commands](#heroku-commands)


## Prerequisites<a name="prerequisites"></a>
- A GitHub account
- Git installed on your computer
- A Heroku account
- Optional: Heroku CLI installed on your computer (if using database, and also makes debugging easier)


## How To Set Up Project<a name="how-to-set-up"></a>
- Create your new repository from the Template (aka this repository)
  - Click the 'Use this template' green button at the top right of this page
  - Select 'Create a new repository' 
    - Provide a name, description, and set it to public or private
    - Click 'Create repository' 
- Set up your project locally
  - After creating your repository from the template, you need to set it up on your local machine for development
  - Open a terminal on your computer
  - Navigate into the folder you would like your project to reside in
    - e.g. `cd ~/Projects`
  - Clone the repository
    - `git clone https://github.com/USERNAME/REPOSITORY_NAME.git`
    - Note: replace USERNAME and REPOSITORY_NAME with your actual GitHub username and the name of the new repository you just created (NOT the boilerplate template)
  - Navigate into the project directory
    - `cd REPOSITORY_NAME`
  -Check the remote setup to verify that the repository URL has been set correctly
    - `git remote -v`
  - Now you can start making changes to the project:
    - To add changes: `git add .`
    - To commit change: `git commit -m "Your message"`
    - To push changes to GitHub: `git push origin main`
- Create an account with Heroku
  - Create a new app for your project
  - Set up the app
    - Resources Tab: 
      - In the Add-ons section search ‘Heroku Postgres’ + submit order form to add it
    - Deploy Tab:
      - In the Deployment method section, select GitHub (connect to GitHub)
      - Connect to your GitHub and search for the repo you created and connect it
      -	Click the button ‘Enable Automatic Deploys’
      - Note: now whenever you push a change to your GitHub repository, Heroku will deploy a new version of your app
    - Settings Tab: 
      - Config Vars section - select 'Reveal Config Vars button:
        - Allowed Hosts:
          - KEY: DJANGO_ALLOWED_HOSTS
          - VALUE: a list of hosts separated by commas, like ‘yourapp.herokuapp.com, yourcustomdomain.com’
          - NOTES: 
            - Do not use single or double quotes around the URLs
            - Separate urls with commas
        - Django secret key: 
          - KEY: DJANGO_SECRET_KEY
          - VALUE: *generate a secret key*
          - To generate a secret key:
            - Use website:
              - https://djecrety.ir/ 
            - Use Script:
              - Ensure python is installed
              - Open powershell terminal and navigate to project root dir
              - Run `python ./generate_django_secret_key.py`
              - Copy-paste the result into the config var ‘Value’ field
      - Buildpack section: 
        - Add buildpack: nodejs
        - Add buildpack: ruby
        - NOTE: nodejs buildpack must be before ruby!
    - Configure SSL:
      - Select ‘Automatic Certificate Management’ and click next
    - Optional: set a custom domain:
      - Click add domain, enter the domain name, click next
      - If the domain is a Root domain: ALIAS
      - If the domain is a non-root domain: CNAME
- Optional/Considerations:
  - Change favicon: reactapp/public/favicon
  - Change website title: reactapp/public/index.html
  - Add namespace for controllers: ‘api’
  - Download the Heroku CLI (see useful Heroku commands)

## Useful Heroku Commands <a name="heroku-commands"></a>
- Login: `heroku login`
- View Error Logs: `heroku logs -a [your app name]`
- Restart App: `heroku restart -a [your app name]`
- Database - Make Migrations: `heroku run python manage.py migrate -a your-app-name`
- Database - Migrate Changes: `heroku run python manage.py migrate -a [your app name]`
- Run the Django Shell: `heroku run python manage.py shell -a [your app name]`
- Seed the Database: `heroku run python manage.py seed -a [your app name]
