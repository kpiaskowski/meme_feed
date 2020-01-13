## Description
Welcome to meme feed. It will show you latest memes related to machine learning. It downloads memes from fanpages on facebook and displays them between 7am and 9pm, Monday to Friday. All params are located in `config.py`. 

## Requirements
django >= 2.2.5
facebook-scrapper = 0.1.5
pyyaml = 5.3

## First run
1. Create all necessary databases:
    1. `python manage.py makemigrations`
    2. `python manage.py migrate`
    3. `python manage.py createsuperuser` (recommended: user pi, password raspberry)

## Regular run
There are two processes that need to run at the same time: meme updating and django server
#### Meme update
1. In root dir, run `export PYTHONPATH=`pwd`:PYTHONPATH$`
2. `cd memes`
If you want to run single time update (for example scrape as much memes as possible before running server live), run `python update.py --single_run`. You can specify number of pages to visit as well as fanpage names (see update.py argparse)

If you want to run update continuously, run `python update.py --continuous_run`. You can set params as above. This will update memes every 12h.

#### Server run
Given the memes are being updated regularly, it is time to run server:
1. In root dir, run `export PYTHONPATH=`pwd`:PYTHONPATH$`
2. `python manage.py runserver`
3. Go to `http://127.0.0.1:8000/memes/` for memes or to `http://127.0.0.1:8000/admin/` for admin page.
