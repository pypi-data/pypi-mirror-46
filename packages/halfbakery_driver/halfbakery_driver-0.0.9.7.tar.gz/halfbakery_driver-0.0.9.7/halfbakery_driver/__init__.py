__site_url__ = 'http://www.halfbakery.com'

import os
import metadrive

from metadrive import utils
from metadrive._requests import get_drive

from halfbakery_driver.api import (
    Topic,
    Comment
)


def _login(
        username=None,
        password=None,
        profile='default',
        recreate_profile=False,
        proxies='default',
        drive=None):
    '''
    Creates, serializes and saves session
    ( utils.save_session_data )
    '''

    if drive is None:
        if proxies is not None:
            drive = get_drive(profile=profile, recreate_profile=recreate_profile, proxies=proxies)
        else:
            drive = get_drive(profile=profile, recreate_profile=recreate_profile)

    # drive = session
    # session = requests.Session()
    # session.metaname = utils.get_metaname('halfbakery')
    # session_data = utils.load_session_data(namespace='halfbakery')

    # if session_data:
    #     session.cookies.update(
    #         requests.utils.cookiejar_from_dict(
    #             session_data))
    #     return session

    if not username and password:
        credential = utils.get_or_ask_credentials(
            namespace='halfbakery',
            variables=['username', 'password'])

        username = credential['username']
        password = credential['password']

    drive.get('http://www.halfbakery.com/lr/')

    if drive.response.ok:
        drive.get('http://www.halfbakery.com/lr/',
             params={
                 'username': username,
                 'password': password,
                 'login': 'login'})

        if drive.response.ok:
            # sign-in successful #
            return drive
        else:
            raise Exception(
                'Could not signin: {}'.format(
                    drive.response.status_code))
    else:
        raise Exception(
            'Failed to open Halfbakery: {}'.format(
                drive.response.status_code))


def _harvest(query=None, limit=None, get_detail=False):
    '''
    Combines login, get, search into a procudure
    sufficient to generate full-fledged items.
    '''

    drive = _login()

    for item in Topic._filter(
            query=query,
            session=drive,
            get_detail=get_detail,
            limit=limit):

        yield item
