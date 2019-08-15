#!/usr/bin/env python3
# -*-coding:utf-8-*-
import os
from AI.BDAI.ocr import (BD_jsonTtext,BD_ocrAllIn1dir,BD_ocr1By1dir,BD_table_orc)
from AI.BDAI.tts import (BD_text2audio,BD_audio2text,BD_textTaudio,BD_audio2textAll)
from AI.BDAI.conpdf import picsTpdf
#from AI.BDAI.translate import BD_trans
################################
from AI.TSAI.asr import TS_asr_echo
#from AI.TSAI.ocr import ocr as TSocr
from AI.TSAI.ocr import (TS_ocr,TS_ocrTtext,TS_ocr_text_dir)
from AI.TSAI.transl import (TS_trans,TS_speechtranslate,TS_imagetranslate,TS_img_trans_text)
from AI.TSAI.tts import (TS_tts,TS_ttsTplay,TS_ttsList,TS_ttsFile)
from AI.TSAI.txtchart import (get_content,get_ocr)
##########################
#from AI.KDXF.genwav import GenAudio
#from AI.KDXF.XF import (KDXF_audio2str,KDXF_str2audio)
from AI.KDXF.webtts import (KDXF_tts,KDXF_ttsFile)
from AI.KDXF.iat import (KDXF_aitFpcm,KDXF_aitFall)
from AI.KDXF.ocr import (KDXF_ocr_general,KDXF_OcrTtext)
#from AI.KDXF.ocr_handwr import KDXF_ocr_handwrite
################################3
from AI.util.tpdf import (imgLongsplitimage2A4,imgsto1pdf,imgLongplitT1pdf,imgLongto1pdf,imgLongtoText)
from AI.util.textsplit import (BD_text_split,TS_text_split)
from AI.util.audiopy import (new_from_audio,audio_split_combine,audio_split,audios_to_one,audiosn_to_one)
from AI.trans.youdaodictvoice import (download_audio,download_audio_YX)

def Ocr_1By1dir(dirname,func=BD_jsonTtext):
    """
    将目录下的jpg等图片文件转为txt文本文件。
    -------------------------------------
    dirname:目录的名称
    func:BD_jsonTtext,KDXF_OcrTtext
         
    """
    for root,dirs,files in os.walk(dirname):
        for f in files:
            #print(os.path.splitext(f)[1])
            if os.path.splitext(f)[1] in ['.jpg','.png','.jpeg']:
                print(f)
                f=os.path.abspath(root+'/'+f)
                try:
                    #print(f)
                    op=os.path.splitext(f)[0]+'.txt'
                    if not os.path.exists(op):
                        d=func(f)
                        if len(d.strip())>0:
                            with open(op,'w',encoding='utf8') as ff:
                                ff.write(d)
                            #os.remove(f)
                            print('remove file %s ...'%f)
                    time.sleep(0.5)
                except Exception as e:
                    pass
    return
def Ocr_AllIn1dir(dirname,func):
    Al='output_allinone.txt'
    ff=open(Al,'a',encoding='utf8')
    for root,dirs,files in os.walk(dirname):
        for f in files:
            if os.path.splitext(f)[1] in ['.jpg','.png','.jpeg']:
                f=os.path.abspath(root+'/'+f)
                try:
                    d=func(f)
                    print(f)
                    if len(d.strip())>0:
                        ff.write(d+'\n\n')
                        ff.write('----- %s ----\n\n'%f)
                        ff.flush()                        
                        #os.remove(f)
                        print('remove file %s ...'%f)
                    time.sleep(0.5)
                except Exception as e:
                    pass
    ff.close()
    return    
