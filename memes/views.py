import os

import django
import yaml as yaml
from django.http import HttpResponse
import datetime
import pickle

from django.utils.crypto import random

from manage import DEFAULT_SETTINGS_MODULE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)
django.setup()
from memes.models import Meme


def save_vars(hour, post_id, filename='temp_vars.yml'):
    """
    Saves temporary variables that will be kept during script runs. Due to this, new meme will be served every hour.
    :param hour: the hour when last meme was first loaded
    :param post_id: the post_id of last loaded meme.
    :param filename: name of vars file.
    """
    temp_vars = {
        'prev_hour': hour,
        'prev_id': post_id,
    }
    with open(filename, 'w') as outfile:
        yaml.dump(temp_vars, outfile, default_flow_style=False)


def load_vars(filename='temp_vars.yml'):
    """
    Loads temporary variables that will be kept during script runs. Due to this, new meme will be served every hour.
    :param filename: name of vars file.
    :return hour, post_id
    """
    with open("temp_vars.yml", 'r') as stream:
        temp_vars = yaml.safe_load(stream)

    return temp_vars['prev_hour'], temp_vars['prev_id']


def random_meme():
    """Chooses random meme"""
    memes = Meme.objects.all().filter(valid=True).filter(views=0)
    if not memes:
        memes = Meme.objects.all().filter(valid=True)

    meme = random.choice(memes)
    return meme


def update_count_and_save(meme):
    """Adds 1 to meme views and saves it"""
    meme.views += 1
    meme.save()


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# pseudo config todo
start_hour = 8  # todo
end_hour = 18  # todo
valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

now = datetime.datetime.now()

day = now.strftime("%A")  # todo
day = 'Tuesday'  # todo

# applicable on Saturday and Sunday
if day not in valid_days:
    save_vars(0, 'None')

# if Monday to Friday
else:
    # night time
    if now.hour < start_hour:
        save_vars(0, 'None')

    # late afternoon
    elif now.hour >= end_hour:
        next_day = valid_days[(valid_days.index(day) + 1) % len(valid_days)]
        save_vars(0, 'None')

    # valid display hours
    else:
        meme = None
        # if some memes have been already shown
        if os.path.exists('temp_vars.yml'):
            prev_hour, prev_id = load_vars()

            # load the same meme as before if hour hasn't changed
            if not prev_hour < now.hour:
                memes = Meme.objects.all().filter(valid=True).filter(post_id=prev_id)
                if memes:
                    meme = memes[0]

        # in all other cases (no temp_vars file, new hour)
        if not meme:
            meme = random_meme()

        update_count_and_save(meme)
        save_vars(now.hour, meme.post_id)
