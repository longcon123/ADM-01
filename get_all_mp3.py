import os
import pytube
import pandas
import time
from pathlib import Path
from pydub import AudioSegment
from glob import glob
from wmd import WMD
from wsrt import WSRT
# import whisper
# from whisper.utils import WriteSRT

df = pandas.read_csv('speaker.csv')

spk_id = df['Id']
spk_gender = df['Gender']
spk_region = df['Region']
spk_use_music = df['Music']
spk_audio = df['Audio']

def get_all_mp3(spk_id, spk_audio):
    index_spk = 0
    for spk in spk_id:
        if not os.path.exists(spk):
            os.makedirs(spk)
            os.makedirs(spk+"/mp3")
            os.makedirs(spk+"/wav")
            os.makedirs(spk+"/data")
        count_mp3 = 0
        mp3s = spk_audio[index_spk].split("\n")
        n_mp3 = len(mp3s)
        print(spk, n_mp3)
        for link in mp3s:
            #print(link)
            ok = False
            while not ok:
                try:
                    time.sleep(3)
                    data = pytube.YouTube(link)
                    audio = data.streams.get_audio_only()
                    audio.download(filename=spk+'/mp3/audio{:02d}.mp3'.format(count_mp3))
                    ok = True
                except:
                    print("Error Dowload Audio, TRYING AGAIN!!!")
            print("Spk{} file{} ok".format(spk,count_mp3))
            count_mp3 += 1
        index_spk += 1
        break

def concat_mp3s(spk_ids):
    for spk_id in spk_ids:
        spk_mp3_path = '{}/mp3'.format(spk_id)
        all_mp3 = glob('{}/*.mp3'.format(spk_mp3_path))
        print("Combining {}".format(spk_id))
        if len(all_mp3) > 1:
            playlist_mp3 = [AudioSegment.from_file(mp3_file) for mp3_file in all_mp3]
            combined = AudioSegment.empty()
            for mp3 in playlist_mp3:
                combined+=mp3
            combined.export(spk_id+'/data/all.mp3', format="mp3")
        print("Combine Done {}".format(spk_id)) 

def get_srt(spk_ids):
    write_srt = WSRT()
    for spk_id in spk_ids:
        spk_mp3_path = '{}/mp3'.format(spk_id)
        mp3s = sorted(glob('{}/*.mp3'.format(spk_mp3_path)))
        for mp3 in mp3s:
            print(mp3)
            write_srt.save_srt_from_mp3(mp3=mp3)
            print("Oke{}".format(mp3))

def get_meta_data(spk_ids):
    for spk_id in spk_ids:
        spk_mp3_path = '{}/mp3'.format(spk_id)
        mp3 = glob('{}/*.mp3'.format(spk_mp3_path))[0]
        srt = glob('{}/*.srt'.format(spk_mp3_path))[0]
        meta_dt = WMD(mp3, srt)
        meta_dt.write_meta_data(spk_id)


start_time = time.time()
#get_all_mp3(spk_id) ## TEST OK
#concat_mp3s('Speaker01') ## TEST OK
#get_srt('Speaker01') ## TEST OK
#get_meta_data(spk_id) ## TEST Ok
print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    print("==> STEP1 START!!!")
    print("... STEP1 Running...")
    get_all_mp3(spk_id=spk_id, spk_audio=spk_audio)
    print("!!!--> STEP1: GET ALL MP3 Audio DONE <--!!!")
    print("==> STEP2 START!!!")
    print("... STEP2 Running...")
    #concat_mp3s(spk_ids=spk_id)
    #print("!!!--> STEP2: COMBINED ALL MP3 DONE <--!!!")
    print("==> STEP3 START!!!")
    print("... STEP3 Running...")
    get_srt(spk_ids=spk_id)
    print("!!!--> STEP3: GET SRT ALL SPK DONE <--!!!")
    #print("==> STEP4 START!!!")
    #print("... STEP4 Running...")
    #get_meta_data(spk_ids=spk_id)
    #print("!!!--> STEP4: WRITE META DATA ALL SPK DONE <--!!!")


# video = 'https://www.youtube.com/watch?v=yZrvuX2rrNk'
# data = pytube.YouTube(video)
# # Convert to audio file
# audio = data.streams.get_audio_only()
# audio.download(filename='audio2.mp3')
