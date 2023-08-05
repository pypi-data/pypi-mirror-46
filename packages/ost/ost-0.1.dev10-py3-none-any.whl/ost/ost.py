from ost.utilities import *


###################################################
################### Base Class  ###################
###################################################


class OST(object):

    global session
    global token

    def __init__(self):
        pass

    def download(self, save_path, **kwargs):
        response = requests.get(self.url)
        compressed_file = BytesIO(response.content)
        decompressed_file = GzipFile(fileobj=compressed_file)
        srt2 = rename_srt(self.file)
        with open(save_path + srt2, 'wb') as output:
            output.write(decompressed_file.read())
        return "Subtitles downloaded!"


class TV(OST):


    def tv_search(self, file, **kwargs):
        self.file = file
        se_info = get_se_info(self.file)
        f = File(self.file)
        hash_file = f.get_hash()
        data = get_sub_data(hash_file)
        if len(data) > 0:
            accurate = []
            for i in range(len(data)):
                if se_info in data[i]['SubFileName'].split("."):
                    accurate.append(i)
            self.url = data[accurate[0]].get("SubDownloadLink")
            self.srt = data[accurate[0]].get("SubFileName")
            return "Subtitles found!"
        return file.split("/")[-1].split(".")[0] + ": subtitles not found!"


class MOVIE(OST):


    def movie_search(self, file, **kwargs):
        self.file = file
        f = File(file)
        hash_file = f.get_hash()
        data = get_sub_data(hash_file)
        if len(data) > 0:
            self.url = data[0].get("SubDownloadLink")
            self.srt = data[0].get("SubFileName")
            return "Subtitles found!"
        return "Subtitles not found!"











