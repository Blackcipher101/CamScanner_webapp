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
refpoints=[]
deb=0
class VideoCamera(object):

    def __init__(self):

        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        t1=threading.Thread(target=self.update, args=()).start()


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
    global cam
    global refpoints
    cam = VideoCamera()
    frame=[]
    points=[]
    done=[[]]
    refpoints=[]
    return render (request,"index.html")

def capture(request):
    global frame
    global deb
    if deb!=1:
        frame=cam.get_capture()
        cam.__del__()
    deb=0
    ret, frame_buff = cv2.imencode('.png', frame) #could be png, update html as well
    frame_b64 = base64.b64encode(frame_buff)

    frame2=str(frame_b64)
    frame1=frame2[2:len(frame2)-1]
    # Note this was fixed to be one dict with the context variables
    return render(request, 'result.html', {'img': frame1,})
def points(request):
    global points
    global refpoints
    points=request.POST['myData']
    refpoints=request.POST['refrence']
    print(len(points))
    return redirect('display_points')
def display_points(request):
    global points
    global refpoints
    img , pts =Applying_perspective.applyper(frame,points,refpoints)
    if len(pts)!=4:
        global deb
        deb=1
        return redirect('capture')
    ret, frame_buff = cv2.imencode('.png', img) #could be png, update html as well
    frame_b64 = base64.b64encode(frame_buff)

    frame2=str(frame_b64)
    frame1=frame2[2:len(frame2)-1]
    return render(request,'test.html',{'img':frame1})

def display_last(request):
    global frame
    global points
    global done
    global refpoints
    done=Per_blur.per_blur(frame,points,refpoints)
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
