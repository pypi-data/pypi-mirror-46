from ost.utilities import *


###################################################
################### Base Class  ###################
###################################################


class OST(object):

    global session
    global token


    def __init__(self, read_path, save_path):
        self.read_path = read_path
        self.save_path = save_path


    def download(self, **kwargs):
        response = requests.get(self.url)
        compressed_file = BytesIO(response.content)
        decompressed_file = GzipFile(fileobj=compressed_file)
        srt2 = rename_srt(self.file)
        with open(self.save_path + srt2, 'wb') as output:
            output.write(decompressed_file.read())
        return "Subtitles downloaded!"


    def run(self):
        pass


class TV(OST):


    def tv_search(self, file, **kwargs):
        self.file = file
        se_info = get_se_info(self.file)
        f = File(self.file)
        self.hash_file = f.get_hash()
        data = get_sub_data(self.hash_file)
        if len(data) > 0:
            accurate = []
            p = re.compile('\w\d\d\w\d\d', re.IGNORECASE)
            for i in range(len(data)):
                if se_info[0] in p.findall(data[i]['SubFileName']) or se_info[1] in p.findall(data[i]['SubFileName']):
                    accurate.append(i)
            if len(accurate):
                self.url = data[accurate[0]].get("SubDownloadLink")
                self.srt = data[accurate[0]].get("SubFileName")
                print("Subtitles found!")
        else:
            print(file + ": subtitles not found!")


class MOVIE(OST):


    def movie_search(self, file, **kwargs):
        self.file = file
        f = File(file)
        self.hash_file = f.get_hash()
        data = get_sub_data(self.hash_file)
        if len(data) > 0:
            self.url = data[0].get("SubDownloadLink")
            self.srt = data[0].get("SubFileName")
            return "Subtitles found!"
        return "Subtitles not found!"




for file in files:
    tv = TV(path, path)
    tv.tv_search(file)
    if hasattr(tv, "url"):
        tv.download()





