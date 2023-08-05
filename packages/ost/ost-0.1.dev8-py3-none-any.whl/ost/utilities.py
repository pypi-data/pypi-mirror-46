from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
import requests
from io import BytesIO
from glob import glob
from gzip import GzipFile


##################################################################
###################  Utility/Helper Functions  ###################
##################################################################


def rename_srt(file):
    new_srt = file.split("/")[-1].split(".")[0] + ".srt"
    return new_srt


def get_se_info(file):
    se_info = file.split("/")[-1].split(".")[0].split(" ")[-1]
    return se_info


def get_sub_data(hash_file):
    data = session.search_subtitles([{'sublanguageid':'eng', 'moviehash':hash_file}])
    return data
