from django.shortcuts import render
from django.shortcuts import redirect
import cv2
import numpy as np
from django.http import StreamingHttpResponse
import threading
from django.views.decorators import gzip
from django.http import HttpResponse
import base64
from . import Applying_perspective
from . import Per_blur
from . import convert
import mimetypes

frame =[[]]
points=[]
done=[[]]
imagelist=[]
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    def get_capture(self):
        ret,frame=self.video.read()
        return frame
    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


cam = VideoCamera()


def gen(camera):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def stream(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass
def html_render(request):
    global frame
    global points
    global done
    frame=[]
    points=[]
    done=[[]]
    return render (request,"index.html")

def capture(request):
    global frame
    frame=cam.get_capture()
    h,w,c=frame.shape
    ret, frame_buff = cv2.imencode('.png', frame) #could be png, update html as well
    frame_b64 = base64.b64encode(frame_buff)

    frame2=str(frame_b64)
    frame1=frame2[2:len(frame2)-1]
    # Note this was fixed to be one dict with the context variables
    return render(request, 'result.html', {'img': frame1, 'h':h ,'w':w})
def points(request):
    global points
    points=request.POST['myData']
    return redirect('display_points')
def display_points(request):
    global points
    img=Applying_perspective.applyper(frame,points)
    ret, frame_buff = cv2.imencode('.png', img) #could be png, update html as well
    frame_b64 = base64.b64encode(frame_buff)

    frame2=str(frame_b64)
    frame1=frame2[2:len(frame2)-1]
    return render(request,'test.html',{'img':frame1})

def display_last(request):
    global frame
    global points
    global done
    done=Per_blur.per_blur(frame,points)
    ret, frame_buff = cv2.imencode('.png', done) #could be png, update html as well
    frame_b64 = base64.b64encode(frame_buff)

    frame2=str(frame_b64)
    frame1=frame2[2:len(frame2)-1]
    global imagelist
    imagelist.append(done)

    return render(request,'final.html',{'img':frame1})
def download(request):
    global done
    global imagelist
    convert.convert(imagelist)
    fl_path = '/home/nehal/Camscanner_web_app/my.pdf'
    filename = 'my.pdf'

    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
