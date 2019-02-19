#!/usr/bin/env python3
# -*-coding:utf-8-*-

from AI.BDAI.ocr import (BD_jsonTtext,BD_ocrAllIn1dir,BD_ocr1By1dir,BD_table_orc)
from AI.BDAI.tts import (BD_text2audio,BD_audio2text,BD_textTaudio,BD_audio2textAll)
#from AI.BDAI.translate import BD_trans
################################
from AI.TSAI.asr import TS_asr_echo
#from AI.TSAI.ocr import ocr as TSocr
from AI.TSAI.ocr import (TS_ocr,TS_ocr_text,TS_ocr_text_dir)
from AI.TSAI.transl import (TS_trans,TS_speechtranslate,TS_imagetranslate,TS_img_trans_text)
from AI.TSAI.tts import (TS_tts,TS_ttsTplay,TS_ttsList,TS_ttsFile)
from AI.TSAI.txtchart import (get_content,get_ocr)
##########################
#from AI.KDXF.genwav import GenAudio
#from AI.KDXF.XF import (KDXF_audio2str,KDXF_str2audio)
from AI.KDXF.webtts import (KDXF_tts,KDXF_ttsFile)
from AI.KDXF.iat import (KDXF_aitFpcm,KDXF_aitFall)
from AI.KDXF.ocr import KDXF_ocr_general
#from AI.KDXF.ocr_handwr import KDXF_ocr_handwrite
################################3
from AI.util.tpdf import (splitimage2A4,imgtopdf,imgsTpdf,imgtopdf_signal)
from AI.util.textsplit import (BD_text_split,TS_text_split)
from AI.util.audiopy import (new_from_audio,audio_split_combine,audio_split,audios_to_one)
