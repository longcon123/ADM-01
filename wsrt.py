from pathlib import Path
import whisper
from whisper.utils import WriteSRT

class WSRT():
    def __init__(self, modelSize='large', language='vi'):
        self.model = whisper.load_model(modelSize)
        self.language = language
    
    def save_srt_from_mp3(self, mp3):
        result = self.model.transcribe(mp3, language=self.language)
        p = Path(mp3)
        writer = WriteSRT(p.parent)
        writer(result, mp3)   

# modelSize = "large"

# if __name__ == "__main__":
#     mp3 = "/content/audio1.mp3"
#     model = whisper.load_model('large')
#     print("Transcribing: "+mp3+" ...")
#     result = model.transcribe(mp3, language='vi')
    
#     print(result["text"])
    
#     print("Saving: "+mp3+".srt ...")
#     p = Path(mp3)
#     writer = WriteSRT(p.parent)
#     writer(result, mp3)