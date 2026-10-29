# GGJournal
Game tracker and backlogger, made as a final project of Harvard's CS50x

#### Description:

A personal Game-Tracking Web Application that allows for user to create their own personal lists. Made using **Flask**, **Python**, **SQLite3**, **HTML**, **CSS** and **Javascript**, utilizing the **RAWG Database API**.

You can create any amounts of lists and add games to them, with the games existing or not and search for any games on the RAWG Video Game Database, organizing your lists the way you prefer!

## How to Use

Follow the steps below to run the project locally.
All required dependencies are already listed in requirements.txt, ready for download.

1. Download the project

2. Create a Virtual Environment
Creating a venv is necessary so the project runs in an isolated and clean environment.


Mac / Linux

```python3 -m venv venv```

```source venv/bin/activate```


Windows (PowerShell)

```python -m venv venv```

```venv\Scripts\activate```


If done sucessfully, it should show (venv) before your terminal command prompt

3. Install dependencies

To install the project dependencies, run:

```pip install -r requirements.txt```

**This installs Flask, CS50 library, Requests, and all other libraries needed for the application.**

4. Prepare the database

Inside the project, a small helper file is included (db.py) that initializes the database structure if it does not exist.

Before running the application, you may need to create an empty SQLite database file in the project root using:

```touch ggjournal.db```

Then run:

```python db.py```

This will generate:

- ggjournal.db

- users table

- lists table

- games table

If the database already exists, it won't affect your data nor structure.

Note: The SQLite database file is created in the project root directory.

5. Run the application

With the venv activated, start Flask:

```python app.py```

Then access on your browser (or click the link on the flask terminal):

```http://127.0.0.1:5000```

6. Using the Application

Once running, you can:

- Register an account

- Log in

- Create multiple personalized game lists

- Search games using the RAWG API

- Add games directly from the search results

- Add custom games manually

- Edit games and lists

- Remove anything as needed

All data is stored locally in SQLite, tied uniquely to your account.

7. API KEYS

The project supports a .env file for API keys:

RAWG_KEY=# (RAWG API Key)
SECRET_KEY=# (Flash Key)

Just fill in the # with your own keys. The RAWG Key is received on the RAWG website and the Flask Secret Key is a series of your own custom characters.

There is a file called .env.example, rename the file to .env and fill in the #.

## How to get a RAWG API Key?

Go to the RAWG website (url: https://rawg.io), create an account and on the API page, fill in the form about the API and how you will use it. After that, you will receive the Key and you can safely paste it on the **RAWG_KEY=** field on the .env file

## Project Overview

GGJournal provides a clean and intuitive way for users to manage their personal game collections. After registering and logging in, each user gains access to a private workspace where they can:

- Create multiple personalized game lists

- Add games manually or import data using the RAWG API

- Edit or delete lists and entries

- Store notes, cover URLs, and dates for organizational purposes

- Search games externally and insert them directly into any list

- Maintain persistent data tied to their account through local SQLite storage

## API Integration (RAWG)

The RAWG API was chosen for being free, well-documented, and relevant to the context of video game cataloging.

## Why this project?

The inspiration for this project comes from a personal habit I share with a close friend.
For years, every time we finished a game together, we manually recorded the date, personal notes, achievements, and any relevant memories inside a shared Discord channel. It became our informal “gaming journal”, allowing us to look back at each year, compare our progress, and revisit stories and moments tied to different playthroughs.

However, this process was entirely manual—typing titles by hand, searching for images ourselves, keeping dates organized, and managing long lists. There was no structure, no database, and no way to visualize or organize the information beyond a simple chat log.

GGJournal was born from the desire to transform that shared ritual into something more meaningful, efficient, and technically sophisticated. I wanted a platform capable of:

- tracking games in a clean and structured way;

- automatically pulling game data through an API;

- allowing each user to maintain multiple personalized lists;

- storing memories through notes, dates, and images;

and ultimately serving as a digital “gaming diary”.

This project is both a personal tribute to that shared experience and an opportunity to apply full-stack development concepts.

## Use of AI

The usage of AI in some parts of the code were fundamental for structure suggestions, configurations with files like .env and .venv, some suggestions, error handlings and answering some questions.

#### AI used:
Chat GPT

#### Where:
- Some CSS Properties and positions;
- helpers.py structure and functionalities;
- app.py error handler and user dependent routes (for example: *"@app.route("/lists/<int:list_id>/edit"*));
- Some HTML files structures, specially in the layout.html;
- Troubleshooting with some code and SQLite3 errors (including the creation of the db.py for using the database elsewhere)
