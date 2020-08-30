from PIL import Image
import cv2

def convert(opencv_imglist):
    i=1
    imagelist=[]
    dst = cv2.cvtColor(opencv_imglist[0], cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(dst)
    im1 = im_pil.convert('RGB')
    while i<len(opencv_imglist):
        print("hey")
        dst1 = cv2.cvtColor(opencv_imglist[i], cv2.COLOR_BGR2RGB)
        im_pil1 = Image.fromarray(dst1)
        im11 = im_pil1.convert('RGB')
        imagelist.append(im11)
        i=i+1
    name="my.pdf"
    im1.save(name,"PDF",save_all=True, append_images=imagelist)
