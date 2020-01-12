import logging
import os

import django
import yaml as yaml
import datetime

from django.shortcuts import render
from django.utils.crypto import random

import config
from manage import DEFAULT_SETTINGS_MODULE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)
django.setup()
from memes.models import Meme

logging.basicConfig(
    level=logging.INFO,
    filename='memes/display_logs.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
)


def save_vars(hour, post_id, filename='memes/temp_vars.yml'):
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


def load_vars(filename='memes/temp_vars.yml'):
    """
    Loads temporary variables that will be kept during script runs. Due to this, new meme will be served every hour.
    :param filename: name of vars file.
    :return hour, post_id
    """
    with open(filename, 'r') as stream:
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


def am_or_pm(hour):
    """Returns 24h hour in 12h format and hour specifier (am or pm)"""
    if 0 <= hour <= 12:
        return hour, 'AM'
    else:
        return hour - 12, 'PM'


def index(request):
    try:
        now = datetime.datetime.now()
        day = now.strftime("%A")

        # applicable on Saturday and Sunday
        if day not in config.valid_days:
            save_vars(0, 'None')
            next_hour, hour_type = am_or_pm(config.start_hour)
            logging.info(f'Showing no-display page')
            return render(request, 'no_display.html', {'next_day': config.valid_days[0],
                                                       'next_hour': next_hour,
                                                       'hour_type': hour_type})

        # if Monday to Friday
        else:
            # night time to early morning
            if now.hour < config.start_hour:
                save_vars(0, 'None')
                next_hour, hour_type = am_or_pm(config.start_hour)
                logging.info(f'Showing no-display page')
                return render(request, 'no_display.html', {'next_day': day,
                                                           'next_hour': next_hour,
                                                           'hour_type': hour_type})

            # late afternoon
            elif now.hour >= config.end_hour:
                next_day = config.valid_days[(config.valid_days.index(day) + 1) % len(config.valid_days)]
                save_vars(0, 'None')
                next_hour, hour_type = am_or_pm(config.start_hour)
                logging.info(f'Showing no-display page')
                return render(request, 'no_display.html', {'next_day': next_day,
                                                           'next_hour': next_hour,
                                                           'hour_type': hour_type})

            # valid display hours
            else:
                meme = None
                # if some memes have been already shown
                if os.path.exists('memes/temp_vars.yml'):
                    prev_hour, prev_id = load_vars()

                    # load the same meme as before if hour hasn't changed
                    if not prev_hour < now.hour:
                        memes = Meme.objects.all().filter(valid=True).filter(post_id=prev_id)
                        if memes:
                            meme = memes[0]
                            logging.info(f'Showing same meme as before, post_id: {meme.post_id}')

                # in all other cases (no temp_vars file, new hour)
                if not meme:
                    meme = random_meme()
                    logging.info(f'Showing new meme, post_id: {meme.post_id}')

                update_count_and_save(meme)
                save_vars(now.hour, meme.post_id)

                next_hour, hour_type = am_or_pm(now.hour + 1)
                return render(request, 'display.html', {
                    'image_url': meme.image_url,
                    'next_hour': next_hour,
                    'hour_type': hour_type})

    except Exception as e:
        logging.exception("Exception occurred")
        return render(request, 'no_display.html', {
            'next_day': 'As soon as possible',
            'next_hour': 'error occured :(',
            'hour_type': ''})

