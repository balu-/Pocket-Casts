import os
import unittest
import pocketcasts


USERNAME = os.environ.get('POCKETCAST_USER')
PASSWORD = os.environ.get('POCKETCAST_PASSWORD')

class PocketcastTest(unittest.TestCase):
    pocket = pocketcasts.Pocketcasts(USERNAME, PASSWORD)
    
    def test_invalid_method(self):
        self.assertRaises(Exception, self.pocket._make_req, 'test', method='INVALID')

    def test_invalid_login(self):
        self.assertRaises(Exception, pocketcasts.Pocketcasts, 'test', 'INVALID')

    def test_get_podcast(self):
        response = self.pocket.get_podcast('12012c20-0423-012e-f9a0-00163e1b201c')
        # check title
        t = response.title
        self.assertTrue(isinstance(t,str))
        self.assertTrue(t != "")

    def test_get_up_next(self):
        response = self.pocket.get_up_next()

    def test_get_new_releases(self):
        response = self.pocket.get_new_releases()

    def test_get_in_progress(self):
        response = self.pocket.get_in_progress()
        if len(response)>0:
            p = response[0].podcast
            self.assertTrue( p != None )
"""
    def test_update_playing_status(self):
        pod = self.pocket.get_podcast("12012c20-0423-012e-f9a0-00163e1b201c")
        epi = self.pocket.get_podcast_episodes(pod)[-1]
        epi.playing_status = 3

    def test_invalid_update_playing_status(self):
        pod = self.pocket.get_podcast("12012c20-0423-012e-f9a0-00163e1b201c")
        epi = self.pocket.get_podcast_episodes(pod)[-1]
        with self.assertRaises(Exception) as context:
            epi.playing_status = 'invalid'
            self.assertTrue('Sorry your update failed.' in context.exception)

    def test_update_played_position(self):
        pod = self.pocket.get_podcast("12012c20-0423-012e-f9a0-00163e1b201c")
        epi = self.pocket.get_podcast_episodes(pod)[-1]
        epi.played_up_to = 2

    def test_invalid_played_position(self):
        pod = self.pocket.get_podcast("12012c20-0423-012e-f9a0-00163e1b201c")
        epi = self.pocket.get_podcast_episodes(pod)[-1]
        with self.assertRaises(Exception) as context:
            epi.played_up_to = 'invalid'
            self.assertTrue('Sorry your update failed.' in context.exception)
    """

if __name__ == '__main__':
    unittest.main(warnings='ignore')
    #unittest.main()
