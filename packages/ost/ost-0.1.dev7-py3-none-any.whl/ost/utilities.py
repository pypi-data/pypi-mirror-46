from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
from os import path
import requests
from io import BytesIO
from glob import glob
import gzip


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


def search_file(file):
    se_info = get_se_info(file)
    f = File(file)
    hash_file = f.get_hash()
    data = get_sub_data(hash_file)
    if len(data) > 0:
        accurate = []
        for i in range(len(data)):
            if se_info in data[i]['SubFileName'].split("."):
                accurate.append(i)
        url = data[accurate[0]].get("SubDownloadLink")
        srt = data[accurate[0]].get("SubFileName")
        return url, srt
    return se_info + ": subtitles not found!"


def file_download(file, url, srt, save_path):
    response = requests.get(url)
    compressed_file = BytesIO(response.content)
    decompressed_file = gzip.GzipFile(fileobj=compressed_file)
    srt2 = rename_srt(file)
    with open(save_path+srt2, 'wb') as output:
        output.write(decompressed_file.read())


def download_many(files):
    files = sorted(files)
    for file in files:
        try:
            url, srt = search_file(file)
            file_download(file, url, srt, '/Users/ireyx001/Downloads/Subtitles/')
        except:
            continue
