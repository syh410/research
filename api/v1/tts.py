import uuid
import paddle
from pydub import AudioSegment
from flask import send_file, request, current_app
from paddlespeech.cli import TTSExecutor
from . import v1bp


tts_executor = TTSExecutor()
@v1bp.route('tts', methods=['POST'])
def tts():
    content = request.json
    text = content['text']
    if not text:
        return "Text not found", 400
    wav_file = tts_executor(
        text=text,
        output='/tmp/' + str(uuid.uuid4()) + '.wav',
        am='fastspeech2_csmsc',
        am_config=None,
        am_ckpt=None,
        am_stat=None,
        spk_id=0,
        phones_dict=None,
        tones_dict=None,
        speaker_dict=None,
        voc='pwgan_csmsc',
        voc_config=None,
        voc_ckpt=None,
        voc_stat=None,
        lang='zh',
        device=paddle.get_device())
    current_app.logger.info('Wave file has been generated: {}'.format(wav_file))

    def wav_to_mp3(wav_file):
        mp3_file = wav_file.replace(".wav", ".mp3")
        AudioSegment.from_wav(wav_file).export(mp3_file, format="mp3")
        current_app.logger.info('Mp3 file has been generated: {}'.format(mp3_file))
        return mp3_file
    
    mp3_file = wav_to_mp3(wav_file)
    return send_file(mp3_file)
