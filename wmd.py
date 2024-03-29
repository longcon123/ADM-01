import pysrt
from pydub import AudioSegment
import time
from vinorm import TTSnorm

class WMD():
    def __init__(self, frame_rate='22050', channel='1'):
        self.frame_rate = frame_rate
        self.channel = channel
        self.time_to_ms = lambda x: (x.hours*3600 + x.minutes * 60 + x.seconds) * 1000 + x.milliseconds
        
    def write_meta_data(self, spk_id, audio_name, sub_name):
        self.sound = AudioSegment.from_file(audio_name)
        self.subs = pysrt.open(sub_name, encoding='utf-8')
        audio_cnt = 0
        audio_part_name = audio_name.split('/')[-1].split('.')[0]
        csv_output = '{}/{}.csv'.format(spk_id, spk_id)
        with open(csv_output, 'w') as fd:
            for sub in self.subs:
                # Get start time, end time in miliseconds
                start_ms = self.time_to_ms(sub.start)
                end_ms = self.time_to_ms(sub.end)   
                # Audio extracted file name
                audio_cnt +=1
                audio_save_name = '{}_{}_{:05d}.wav'.format(spk_id,audio_part_name,audio_cnt)
                audio_save_path = '{}/wav/{}'.format(spk_id, audio_save_name)
                text = str(sub.text)
                norm_text = TTSnorm(text)
                ## TODO: Remove english text and aduio: if english(text) == True:
                # Extract file
                extract = self.sound[start_ms:end_ms]
                # Saving converted audio
                extract.export(audio_save_path,format="wav", parameters=['-ar', self.frame_rate, '-ac', self.channel, '-ab', '64'])
                # Write to csv file
                fd.write('{}_{}|{}\n'.format(spk_id, audio_save_name, norm_text))


# if __name__ == '__main__':
#     audio_name = 'audio1.mp3'
#     sub_name = 'audio1.srt'
#     audio_outdir = 'audio'
#     csv_output = 'output.csv'


#     frame_rate = '22050'
#     mono_channel = '1'
#     song = AudioSegment.from_file(audio_name)
#     subs = pysrt.open(sub_name, encoding='utf-8')
#     time_to_ms = lambda x: (x.hours*3600 + x.minutes * 60 + x.seconds) * 1000 + x.milliseconds
#     audio_cnt = 0
#     # Extract data 
#     with open(csv_output, 'w') as fd:
#         for sub in subs:
#             # Get start time, end time in miliseconds
#             start_ms = time_to_ms(sub.start)
#             end_ms = time_to_ms(sub.end)   
#             # Audio extracted file name
#             audio_cnt +=1
#             audio_extract_name = '{}.wav'.format('speaker01_audio{:06d}'.format(audio_cnt))
#             text = str(sub.text)
#             # Extract file
#             extract = song[start_ms:end_ms]
#             # Saving converted audio
#             extract.export(audio_extract_name,format="wav", parameters=['-ar', frame_rate, '-ac', mono_channel, '-ab', '64'])
#             # Write to csv file
#             fd.write('{}|{}\n'.format(audio_extract_name, text))
