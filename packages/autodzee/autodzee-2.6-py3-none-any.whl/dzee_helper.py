
import deezer as deezer
import mega as megaz
import requests, json, os, shutil, uuid
localdir = os.getcwd()
headers = {'content-type': 'application/json',
               'Authorization': 'Token 68784f7a0ec89731722b714d4d3c40c2f2c9302e'}
def crawl_auto(gmail, password, arl, sv):
    dez = deezer.Login(gmail, password, arl)
    tracks = requests.get("http://54.39.49.17:8030/api/tracks/?status=0&sv={}".format(sv)).json()['results']
    for track in tracks:
        print("Update Status audio: " + str(track['deezer_id']) + " - " + track['title'] + " - " + track['artist'])
        track['status'] = True
        try:
            requests.put("http://54.39.49.17:8030/api/tracks/{}/".format(track['id']),
                         data=json.dumps(track), headers=headers)
        except:
            requests.put("http://54.39.49.17:8030/api/tracks/{}/".format(track['id']),
                         data=json.dumps(track), headers=headers)
            pass

    for track in tracks:
        try:
            print("crawl audio: " + str(track['deezer_id']) + " - " + track['title'] + " - " + track['artist'])
            track['status'] = True
            track = dez.download(track['deezer_id'], track, True)
            if (os.path.exists(track['url_128'])):
                track['error_code'] = 0
            else:
                track['error_code'] = 1
            try:
                requests.put("http://54.39.49.17:8030/api/tracks/{}/".format(track['id']),
                             data=json.dumps(track), headers=headers)
            except:
                requests.put("http://54.39.49.17:8030/api/tracks/{}/".format(track['id']),
                             data=json.dumps(track), headers=headers)
                pass
        except Exception as e:
            print("error Download:" + str(e))
            pass
def find_audio(deezer_id):
    tracks = requests.get("http://54.39.49.17:8030/api/tracks/?deezer_id={}".format(deezer_id)).json()['results']
    return tracks
def get_info(deezer_id):
    dez = deezer.Login("mun87081@cndps.com", "asd123a@", "6afe8dd1218df2ae7927210aeca25ef17bc46920072ea72ddf16225eeabf79637d84b43e37f0e2f0c0a6a280d60d5516223e7c4f3270f6a32e8062e4832fb2e6f9c66b8c2f4072f9845061dd3b0ce45e9d5c981b4c8537be3fbf9fd609b14e56")
    track={}
    track_j=requests.get("https://api.deezer.com/track/"+deezer_id).json()
    track['deezer_id']=track_j['id']
    track['title']=track_j['title'][:255]
    track['title_short'] = track_j['title_short'][:255]
    track['isrc'] =  track_j['isrc']
    track['duration'] = track_j['duration']
    track['rank'] = track_j['rank']
    track['explicit_lyrics'] = track_j['explicit_lyrics']
    track['status']=1
    track['artist']= track_j['artist']['name']
    track = dez.download(track['deezer_id'], track)
    if (os.path.exists(track['url_128'])):
        sub_artist = track['url_128'].rsplit('/', 1)[0]
        print(megaz.put(sub_artist, "/music/deezer/"))
        track['error_code'] = 0
        try:
            requests.post("http://54.39.49.17:8030/api/tracks",
                         data=json.dumps(track), headers=headers)
        except:
            requests.post("http://54.39.49.17:8030/api/tracks",
                          data=json.dumps(track), headers=headers)

    return track
def download_mega(link,local=localdir+"/track/"):
    try:
        os.makedirs(local)
    except FileExistsError:
        pass
    path=local + uuid.uuid4().hex+".mp3"
    megaz.get(path,link)
    return path
def download_audio(deezer_id):
    tracks=find_audio(deezer_id)
    if len(tracks) == 0:
        return get_info(deezer_id)
    else:
        track=tracks[0]
        if track['url_128'] !=None:
            url=track['url_128']
            if track['url_320'] != None:
                url=track['url_320']
            path_mega=megaz.find(url.rsplit('/',1)[1],"/music/deezer/")
            if("/music/deezer/" in path_mega):
                track['url_local'] = download_mega(path_mega)
            else:
                dez = deezer.Login("mun87081@cndps.com", "asd123a@",
                                   "6afe8dd1218df2ae7927210aeca25ef17bc46920072ea72ddf16225eeabf79637d84b43e37f0e2f0c0a6a280d60d5516223e7c4f3270f6a32e8062e4832fb2e6f9c66b8c2f4072f9845061dd3b0ce45e9d5c981b4c8537be3fbf9fd609b14e56")
                track = dez.download(track['deezer_id'], track)
                if (os.path.exists(track['url_128'])):
                    url = track['url_128']
                    if track['url_320'] != None:
                        url = track['url_320']
                    track['url_local']=localdir+"/track/"+uuid.uuid4().hex+".mp3"
                    shutil.copyfile(url,track['url_local'])
                    track['error_code'] = 0
                    track['status']=1
                    try:
                        requests.put("http://54.39.49.17:8030/api/tracks/{}/".format(track['id']),
                                     data=json.dumps(track), headers=headers)
                    except:
                        requests.put("http://54.39.49.17:8030/api/tracks/{}/".format(track['id']),
                                     data=json.dumps(track), headers=headers)
                    try:
                        os.remove(track['url_128'])
                        if (os.path.exists(track['url_320'])):
                            os.remove(track['url_320'])
                        if (os.path.exists(track['url_flac'])):
                            os.remove(track['url_flac'])
                    except OSError as e:
                        print("Error: %s - %s." % (e.filename, e.strerror))
        else:
            dez = deezer.Login("mun87081@cndps.com", "asd123a@",
                               "6afe8dd1218df2ae7927210aeca25ef17bc46920072ea72ddf16225eeabf79637d84b43e37f0e2f0c0a6a280d60d5516223e7c4f3270f6a32e8062e4832fb2e6f9c66b8c2f4072f9845061dd3b0ce45e9d5c981b4c8537be3fbf9fd609b14e56")
            track = dez.download(track['deezer_id'], track)
            if (os.path.exists(track['url_128'])):
                url = track['url_128']
                if track['url_320'] != None:
                    url = track['url_320']
                track['url_local'] = localdir + "/track/" + uuid.uuid4().hex + ".mp3"
                shutil.copyfile(url, track['url_local'])
                track['error_code'] = 0
                track['status'] = 1
                try:
                    requests.put("http://54.39.49.17:8030/api/tracks/{}/".format(track['id']),
                                 data=json.dumps(track), headers=headers)
                except:
                    requests.put("http://54.39.49.17:8030/api/tracks/{}/".format(track['id']),
                                 data=json.dumps(track), headers=headers)
                try:
                    os.remove(track['url_128'])
                    if (os.path.exists(track['url_320'])):
                        os.remove(track['url_320'])
                    if (os.path.exists(track['url_flac'])):
                        os.remove(track['url_flac'])
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))
        print(json.dumps(track))





