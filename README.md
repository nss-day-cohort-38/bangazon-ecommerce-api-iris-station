# Bangazon Django RESTful App 

This is the back-end counterpart to the full-stack [Bangazon eCommerce Web App](https://github.com/nss-day-cohort-38/bangazon-ecommerce-web-app-iris-station). A full description of the app can be found there. 

# Project Setup

1. Clone the repo and cd into it:

    `git clone git@github.com:nss-day-cohort-38/bangazon-ecommerce-api-iris-station.git && cd $_`

1. Set up your virtual environment:

    `python -m venv bangazonEnv`

1. Activate virtual environment:

    `source ./bangazonEnv/bin/activate`

1. Install dependencies:

    `pip install -r requirements.txt`

1. Run migrations:

    `python manage.py makemigrations`
    `python manage.py migrate`

1. Load fixtures:

    `python manage.py loaddata */fixtures/*.json`

1. Start the API server:

    `python manage.py runserver`

1. Follow the [steps on the front-end web app readme](https://github.com/nss-day-cohort-38/bangazon-ecommerce-web-app-iris-station) to view the web app in your browser

## Technology Utilized
1. Django
1. Python
1. SQLite
1. Fixtures
1. ORM & SQL queries
1. Models
1. API Endpoint Views  
1. Testing with unittest
1. User authentication with authtoken
1. url routing

## Contributors
- [Kurt Krafft](https://github.com/kurtkrafft1)
- [Andrew Green](https://github.com/agreen2601)
- [Trinity Terry](https://github.com/TrinityTerry)
- [Keith Potempa](https://github.com/keithrpotempa)
- [Matt Crook](https://github.com/MattCrook)

## ERD
Here is our [Bangazon eCommerce ERD](https://dbdiagram.io/d/5eb4d6d639d18f5553fedfb5).