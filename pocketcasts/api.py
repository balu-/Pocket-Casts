"""Unofficial API for pocketcasts.com"""
import requests
from .podcast import Podcast
from .episode import Episode

__version__ = "0.3.0"
__author__ = "balu-"
__url__ = "https://github.com/balu-/Pocket-Casts"


class Pocketcasts(object):
    """The main class for making getting and setting information from the server"""
    def __init__(self, email, password):
        """

        Args:
            email (str): email of user
            password (str): password of user
        """
        self._username = email
        self._password = password

        self._session = requests.Session()
        self._apiToken = ""
        self._login()

    def _make_req(self, url, method='GET', data=None):
        """Makes a HTTP GET/POST request

        Args:
            url (str): The URL to make the request to
            method (str, optional): The method to use. Defaults to 'GET'
            data (dict):  data to send with a POST request. Defaults to None.

        Returns: 
            requests.response.models.Response: A response object

        """
        headers = None
        if self._apiToken != "":
            headers = {"Authorization": "Bearer "+self._apiToken}

        if method == 'JSON':
            req = requests.Request('POST', url, json=data, cookies=self._session.cookies, headers=headers)
        elif method == 'POST' or data:
            req = requests.Request('POST', url, data=data, cookies=self._session.cookies, headers=headers)
        elif method == 'GET':
            req = requests.Request('GET', url, cookies=self._session.cookies, headers=headers)
        else:
            raise Exception("Invalid method")
        prepped = req.prepare()
        return self._session.send(prepped)

    def _login(self):
        """Authenticate using "https://play.pocketcasts.com/users/sign_in"

        Returns:
            bool: True is successful

        Raises:
            Exception: If login fails

        :return: 
        """
        login_url = "https://api.pocketcasts.com/user/login"
        data = {"email": self._username, "password": self._password}
        attempt = self._make_req(login_url, data=data)
        if attempt.status_code != 200:
            raise Exception("Login Failed")
        else:
            self._apiToken = attempt.json()['token']
            return True

    def get_podcast(self, podcast_uuid):
        page_req = self._make_req("https://cache.pocketcasts.com/podcast/full/"+str(podcast_uuid)+"/0/3/1000").json()
        pcast_json = page_req['podcast']
        pcast = Podcast(pcast_json.pop('uuid'), self, **pcast_json)
        return pcast

    def get_episode(self, episode_uuid):
        """Get all the Episode data

        Args:
            episode_uuid (str): uuid of the episode to be fetched
            podcast (Podcast): (optional) podcast object if alreay availiable (will be fetched otherwise)

        Returns:
            Episode: A object of the type Episode with all the data in it

        Raises:
            Exception: If the episode might not be optained

        """
        page_req = self._make_req("https://api.pocketcasts.com/user/episode", method="POST",data={"uuid": episode_uuid})
        page = page_req.json()
        uuid = page.pop('uuid')
        pod_uuid = page.pop('podcastUuid')
        ep = Episode(uuid, self, pod_uuid, **page)
        return ep


    def get_up_next(self, full_data=False):
        """Get the podcast episodes that are in the list to be played

        Args:
            full_data (bool): if true the full dataset of each episode will be fetched otherwise only some attributes are deliverd

        Returns:
            list: A list of episodes as Episode objects

        Raises:
            Exception: If the list cannot be obtained

        """
        page_req = self._make_req("https://api.pocketcasts.com/up_next/list", method="POST", data={"version":2})
        page = page_req.json()
        results = []
        for episode in page['episodes']:
            uuid = episode.pop('uuid')
            pod_uuid = episode.pop('podcast')
            if full_data:
                ep = self.get_episode(uuid)
            else:
                ep = Episode(uuid, self, pod_uuid, **episode)
            results.append(ep)
        return results

    def get_new_releases(self, full_data=False):
        """Get newly released podcasts from a user's subscriptions

         Args:
            full_data (bool): if true the full dataset of each episode will be fetched otherwise only some attributes are deliverd

        Returns:
            List[pocketcasts.episode.Episode]: A list of episodes
        """
        attempt = self._make_req('https://api.pocketcasts.com/user/new_releases', method='POST', data={})
        results = []
        for episode in attempt.json()['episodes']:
            pod_uuid = episode['podcastUuid']
            uuid = episode.pop('uuid')
            if full_data:
                ep = self.get_episode(uuid)
            else:
                ep = Episode(uuid, self, pod_uuid, **episode)
            results.append(ep)
        return results

    def get_in_progress(self, full_data=False):
        """Get all in progress episodes

         Args:
            full_data (bool): if true the full dataset of each episode will be fetched otherwise only some attributes are deliverd

        Returns:
            List[pocketcasts.episode.Episode]: A list of episodes

        """
        attempt = self._make_req('https://api.pocketcasts.com/user/in_progress', method='POST')
        results = []
        for episode in attempt.json()['episodes']:
            pod_uuid = episode['podcastUuid']
            uuid = episode.pop('uuid')
            if full_data:
                ep = self.get_episode(uuid)
            else:
                ep = Episode(uuid, self, pod_uuid, **episode)
            results.append(ep)
        return results

    def get_listening_history(self, full_data=False):
        """Get listening History

         Args:
            full_data (bool): if true the full dataset of each episode will be fetched otherwise only some attributes are deliverd

        Returns:
            List[pocketcasts.episode.Episode]: A list of episodes

        """
        attempt = self._make_req('https://api.pocketcasts.com/user/history', method='POST')
        results = []
        for episode in attempt.json()['episodes']:
            pod_uuid = episode['podcastUuid']
            uuid = episode.pop('uuid')
            if full_data:
                ep = self.get_episode(uuid)
            else:
                ep = Episode(uuid, self, pod_uuid, **episode)
            results.append(ep)
        return results

"""    def update_playing_status(self, podcast, episode, status=Episode.PlayingStatus.Unplayed):
        ""Update the playing status of an episode
        
        Args:
            podcast (pocketcasts.Podcast): A podcast class
            episode (pocketcasts.Episode): An episode class to be updated
            status (int): 0 for unplayed, 2 for playing, 3 for played. Defaults to 0.

        ""
        if status not in [0, 2, 3]:
            raise Exception('Invalid status.')
        data = {
            'playing_status': status,
            'podcast_uuid': podcast.uuid,
            'uuid': episode.uuid
        }
        self._make_req("https://play.pocketcasts.com/web/episodes/update_episode_position.json", data=data)

    def update_played_position(self, podcast, episode, position):
        ""Update the current play duration of an episode

        Args:
            podcast (pocketcasts.Podcast): A podcast class 
            episode (pocketcasts.Episode): An episode class to be updated
            position (int): A time in seconds

        Returns:
            bool: True if update is successful
            
        Raises:
            Exception: If update fails

        ""
        data = {
            'playing_status': episode.playing_status,
            'podcast_uuid': podcast.uuid,
            'uuid': episode.uuid,
            'duration': episode.duration,
            'played_up_to': position
        }
        attempt = self._make_req("https://play.pocketcasts.com/web/episodes/update_episode_position.json",
                                 method='JSON', data=data)
        if attempt.json()['status'] != 'ok':
            raise Exception('Sorry your update failed.')
        return True
"""
