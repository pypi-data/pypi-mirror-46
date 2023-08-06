from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
import requests
from io import BytesIO
from glob import glob
from gzip import GzipFile
# from xmlrpc.client import ServerProxy, Transport


##################################################################
###################  Utility/Helper Functions  ###################
##################################################################

# url = 'http://api.opensubtitles.org/xml-rpc'
# server = ServerProxy(url)
# token = server.LogIn('rlirey@gmail.com', '443182lotr', 'eng', 'Butter v1')['token']
# sub_id = 1952848198
# resp = server.DownloadSubtitles(token, [1952848198])

# server.CheckMovieHash(token, ['fad1a77982bab11e'])


session = OpenSubtitles()


def rename_srt(file):
    new_srt = file.split("/")[-1].split(".")[0] + ".srt"
    return new_srt


def get_se_info(file):
    import re
    p = re.compile('\w\d\d\w\d\d', re.IGNORECASE)
    se_info = p.findall(file)[0]
    return (se_info.upper(), se_info.lower())


def get_sub_data(hash_file):
    global session
    data = session.search_subtitles([{'sublanguageid':'eng', 'moviehash':hash_file}])
    return data


def get_sub_id(hash_file):
    global session
    data = session.search_subtitles([{'moviehash':hash_file}])
    return data
