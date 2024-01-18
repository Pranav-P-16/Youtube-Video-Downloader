#https://www.youtube.com/watch?v=fY-eiJD4uUc
from pytube import YouTube
from threading import Thread
from PIL import Image
import requests,os,webbrowser
import urllib.request,random
import PySimpleGUI as sg
from pydub import AudioSegment
for i in os.listdir("Tmp/"):
    os.remove("Tmp/"+i)
def progress_Check(stream, chunk, remaining):
    global file_size,wn
    #Gets the percentage of the file that has been downloaded.
    percent = (100*(file_size-remaining))/file_size
    wn.write_event_value("Downloaded","Yes")
def err():
    sg.theme("Topanga")
    lyt=[[sg.Text("\t")]+[sg.Text("Task Failed Successfully !",font=("Pricedown",25))]+[sg.Text("\t")],
                 [sg.Button("OK",button_color=("black","red"))]]
    wnd=sg.Window("Error",lyt,element_justification="c",keep_on_top=True)
    event,values=wnd.read()
    wnd.close()
def warn():
    sg.theme("Topanga")
    lyt=[[sg.Text("\t")]+[sg.Text("Preferred resolution not available\nDownloading 720p instead",font=("Pricedown",25))]+[sg.Text("\t")],
                 [sg.Button("OK",button_color=("black","green2"))]]
    wnd=sg.Window("Error",lyt,element_justification="c",keep_on_top=True)
    event,values=wnd.read()
    wnd.close()
def success():
    sg.theme("Topanga")
    lyt=[[sg.Text("\t")]+[sg.Text("Downloaded Successfully !",font=("Pricedown",25))]+[sg.Text("\t")],
                 [sg.Button("OK",button_color=("black","red"))]]
    wnd=sg.Window("Success",lyt,element_justification="c",keep_on_top=True)
    event,values=wnd.read()
    wnd.close()
def download(m,wn,sel_resolution,url):
    global file_size,status_bar
    if m=="MP4":
        if sel_resolution!=1:
            try:
                k=yt.streams.filter(file_extension='mp4',res=str(sel_resolution)+"p",progressive="True").last()
                file_size=k.filesize
                status_bar.update("Downloading ... ~ "+str((file_size//1024)//1024)+" Mb")
                wn.find_element("bt2").Update(20)
                k.download("Output/")
                wn.write_event_value("Done","Happy")
            except:
                wn.write_event_value("Fail","Sad")
    elif m=="WAV":
        try:
            k=yt.streams.filter(file_extension="webm").last()
            file_size=k.filesize
            status_bar.update("Downloading ... ~ "+str((file_size//1024)//1024)+" Mb")
            k.download("Output/")
            wn.find_element("bt2").Update(20)
            yt.title=yt.title.replace("'","")
            yt.title=yt.title.replace('"',"")
            yt.title=yt.title.replace("|","")
            AudioSegment.from_file("Output/"+(yt.title).replace(".","")+".webm").export("Output/"+(yt.title).replace(".","")+".mp3", format="mp3")
            os.remove("Output/"+(yt.title).replace(".","")+".webm")
            wn.find_element("bt2").Update(75)
            AudioSegment.from_file("Output/"+(yt.title).replace(".","")+".mp3").export("Output/"+(yt.title).replace(".","")+".wav", format="wav")
            os.remove("Output/"+(yt.title).replace(".","")+".mp3")
            wn.write_event_value("Done","Happy")
        except:
            wn.write_event_value("Fail","Sad")
    elif m=="MP3":
        try:
            k=yt.streams.filter(file_extension="webm").last()
            file_size=k.filesize
            status_bar.update("Downloading ... ~ "+str((file_size//1024)//1024)+" Mb")
            wn.find_element("bt2").Update(20)
            k.download("Output/")
            yt.title=yt.title.replace("'","")
            yt.title=yt.title.replace('"',"")
            yt.title=yt.title.replace("|","")
            wn.find_element("bt2").Update(70)
            AudioSegment.from_file("Output/"+(yt.title).replace(".","")+".webm").export("Output/"+(yt.title).replace(".","")+".mp3", format="mp3")
            os.remove("Output/"+(yt.title).replace(".","")+".webm")
            wn.write_event_value("Done","Happy")
        except SyntaxError:
            wn.write_event_value("Fail","Sad")
def img_process_2(url):
    global stat,t,y
    stat=True
    t=random.randint(1,1000)
    y=random.randint(1,1000)
    urllib.request.urlretrieve(url,"Tmp/image"+str(t)+str(y)+".jpg")
    im1 = Image.open("Tmp/image"+str(t)+str(y)+".jpg")
    im1 = im1.resize((350,250))
    im1.save("Tmp/image"+str(t)+str(y)+".png")
    return "Tmp/image"+str(t)+str(y)+".png"
def main_convert(m,url,sel_resolution=1):
    global wn,status_bar
    pat=img_process_2(url)
    if len(yt.title) > 40 and len(yt.title)<80:
        ttle=yt.title[:40]
        ttle2=yt.title[40:80]
        ttle3=""
        se="1"
    elif len(yt.title)<=40:
        ttle=yt.title
        ttle2=""
        ttle3=""
        se="2"
    else:
        ttle=yt.title[:40]
        ttle2=yt.title[40:80]
        ttle3=yt.title[80:120]
        se="3"
    sg.theme("black")
    lt=[[sg.Text(ttle,font=("Pricedown",18))],[sg.pin(sg.Text("",key="txe",font=("Pricedown",18),visible=False))],
        [sg.pin(sg.Text("",key="txe2",font=("Pricedown",18),visible=False))],
        [sg.Image(pat)],
        [sg.Text("Number of Views : "+str(yt.views),font=("Pricedown",25))],
        [sg.Text("Rating : "+str(round(yt.rating,1)),font=("Pricedown",25))]+[sg.Image("Assets/rating.png")],
        [sg.pin(sg.Button("",image_filename="Assets/download.png",border_width=0,key="bt1",button_color=("black","black")))],
        [sg.ProgressBar(100,size=(32,20),bar_color=("green2","black"),key='bt2',orientation="h")],
        [sg.pin(sg.Button("",image_filename="Assets/downloaded.png",visible=False,key="bt3",border_width=0,button_color=("black","black")))]+
        [sg.pin(sg.Text("Download Finished",font=("Pricedown",25),key="tx1",visible=False))],
        [sg.StatusBar("", size=40, key='STATUS')]]
    wn=sg.Window("Youtube Video Downloader",lt).Finalize()
    status_bar=wn['STATUS']
    while True:
        if se=="1":
            try:
                wn.find_element("txe").Update(visible=True)
                wn.find_element("txe").Update(ttle2)
            except:
                pass
        elif se=="3":
            try:
                wn.find_element("txe").Update(visible=True)
                wn.find_element("txe2").Update(visible=True)
                wn.find_element("txe").Update(ttle2)
                wn.find_element("txe2").Update(ttle3)
            except:
                pass
        event,v=wn.read()
        if event==None:
            wn.close()
            break
        elif event=="bt3":
            webbrowser.open("Output/")
        elif event=="Done":
            status_bar.update("Downloaded...")
            wn.find_element("bt2").Update(100)
            wn.find_element("bt3").Update(visible=True)
            wn.find_element("tx1").Update(visible=True)
            success()
        elif event=="Downloaded":
            status_bar.Update("Converting...")
            wn.find_element("bt2").Update(50)
        elif event=="Fail":
            status_bar.update("Download Failed...")
            wn.find_element("bt2").Update(0)
            wn.find_element("bt1").Update(visible=True)
            err()
        elif event=="bt1":
            wn.find_element("bt2").Update(10)
            wn.find_element("bt1").Update(visible=False)
            Thread(target=download,args=(m,wn,sel_resolution,url), daemon=True).start()
            status_bar.update("Download Started...")
sg.theme("black")
lt=[[sg.Text("Youtube video downloader",font=("Pricedown",25))],
    [sg.Text("Enter URL ")]+[sg.Input(key="inp")],
    [sg.Text("Output Format ")]+[sg.Button("MP4",key="mp4button")]+[sg.Button("MP3",key="mp3button")]+[sg.Button("WAV",key="wavbutton")],
    [sg.pin(sg.Text("Output Quality ",key="txt2",visible=False))]+[sg.pin(sg.Button("360p",key="360pbutton",visible=False))]+[sg.pin(sg.Button("480p",key="480pbutton",disabled=True,visible=False))]+[sg.pin(sg.Button("720p",visible=False,key="720pbutton"))],
    [sg.Text("@",key="st_box0",font=("Pricedown",25),text_color="green2")]+[sg.Text("WELCOME",key="st_box",font=("Pricedown",25),text_color="yellow")],
    [sg.Button("Download")]]
window=sg.Window("Youtube Video Downloader",lt)
stat=False
sel_resolution=0
value_convert="e"
while True:
    e,v=window.read()
    try:
        link = v["inp"]
        yt = YouTube(link,on_progress_callback=progress_Check)
    except:
        link=""
    if e==None:
        window.close()
        break
    elif e=="Download":
        if value_convert=="MP3":
            window.find_element("st_box0").Update("")
            window.find_element("st_box").Update("")
            if stat==False:
                if link!="":
                    window.find_element("st_box").Update("MP3")
                    url=yt.thumbnail_url
                    window.find_element("st_box").Update("Loading...")
                    window.find_element("st_box0").Update("✔")
                    window.find_element("st_box0").Update(text_color="green2")
                    window.close()
                    main_convert("MP3",url)
                else:
                    window.find_element("st_box").Update("Broken URL")
                    window.find_element("st_box0").Update("!")
                    window.find_element("st_box0").Update(text_color="red")
                    window.find_element("inp").Update("")
        elif value_convert=="WAV":
            window.find_element("st_box0").Update("")
            window.find_element("st_box").Update("")
            if stat==False:
                if link!="":
                    window.find_element("st_box").Update("WAV")
                    url=yt.thumbnail_url
                    window.find_element("st_box").Update("Loading...")
                    window.find_element("st_box0").Update("✔")
                    window.find_element("st_box0").Update(text_color="green2")
                    window.close()
                    main_convert("WAV",url)
                else:
                    window.find_element("st_box").Update("Broken URL")
                    window.find_element("st_box0").Update("!")
                    window.find_element("st_box0").Update(text_color="red")
                    window.find_element("inp").Update("")
        elif value_convert=="MP4":
            window.find_element("st_box0").Update("")
            window.find_element("st_box").Update("")
            if sel_resolution!=0:
                if stat==False:
                    if link!="":
                        window.find_element("st_box").Update("MP4")
                        url=yt.thumbnail_url
                        window.find_element("st_box").Update("Loading...")
                        window.find_element("st_box0").Update("✔")
                        window.find_element("st_box0").Update(text_color="green2")
                        window.close()
                        main_convert("MP4",url,sel_resolution)
                    else:
                        window.find_element("st_box").Update("Broken URL")
                        window.find_element("st_box0").Update("!")
                        window.find_element("st_box0").Update(text_color="red")
                        window.find_element("inp").Update("")
            else:
                window.find_element("st_box").Update("Conversion Resolution Not Specified")
                window.find_element("st_box0").Update("!")
                window.find_element("st_box0").Update(text_color="orange")
        else:
            window.find_element("st_box").Update("Conversion Type Not Specified")
            window.find_element("st_box0").Update("!")
            window.find_element("st_box0").Update(text_color="orange")
    elif e=="mp3button":
        sel_resolution=0
        value_convert="MP3"
        window.find_element("360pbutton").Update(visible=False)
        window.find_element("480pbutton").Update(visible=False)
        window.find_element("720pbutton").Update(visible=False)
        window.find_element("txt2").Update(visible=False)
        window.find_element("st_box").Update("MP3 Type")
        window.find_element("st_box0").Update("✔")
        window.find_element("st_box0").Update(text_color="green2")
        window.find_element("mp3button").Update(button_color=("black","green2"))
        window.find_element("mp4button").Update(button_color=("black","white"))
        window.find_element("wavbutton").Update(button_color=("black","white"))
    elif e=="wavbutton":
        sel_resolution=0
        value_convert="WAV"
        window.find_element("360pbutton").Update(visible=False)
        window.find_element("480pbutton").Update(visible=False)
        window.find_element("720pbutton").Update(visible=False)
        window.find_element("txt2").Update(visible=False)
        window.find_element("st_box").Update("WAV Type")
        window.find_element("st_box0").Update("✔")
        window.find_element("st_box0").Update(text_color="green2")
        window.find_element("wavbutton").Update(button_color=("black","green2"))
        window.find_element("mp4button").Update(button_color=("black","white"))
        window.find_element("mp3button").Update(button_color=("black","white"))
    elif e=="mp4button":
        sel_resolution=0
        window.find_element("360pbutton").Update(visible=True,button_color=("black","white"))
        window.find_element("480pbutton").Update(visible=True,button_color=("black","white"))
        window.find_element("720pbutton").Update(visible=True,button_color=("black","white"))
        window.find_element("txt2").Update(visible=True)
        value_convert="MP4"
        window.find_element("st_box").Update("MP4 Type")
        window.find_element("st_box0").Update("✔")
        window.find_element("st_box0").Update(text_color="green2")
        window.find_element("mp4button").Update(button_color=("black","green2"))
        window.find_element("mp3button").Update(button_color=("black","white"))
        window.find_element("wavbutton").Update(button_color=("black","white"))
    elif e=="360pbutton":
        sel_resolution=360
        window.find_element("st_box0").Update("✔")
        window.find_element("st_box0").Update(text_color="green2")
        window.find_element("st_box").Update("MP4 Type 360p")
        window.find_element("360pbutton").Update(button_color=("black","green2"))
        window.find_element("480pbutton").Update(button_color=("black","white"))
        window.find_element("720pbutton").Update(button_color=("black","white"))
    elif e=="480pbutton":
        sel_resolution=480
        window.find_element("st_box0").Update("✔")
        window.find_element("st_box0").Update(text_color="green2")
        window.find_element("st_box").Update("MP4 Type 480p")
        window.find_element("480pbutton").Update(button_color=("black","green2"))
        window.find_element("360pbutton").Update(button_color=("black","white"))
        window.find_element("720pbutton").Update(button_color=("black","white"))
    elif e=="720pbutton":
        sel_resolution=720
        window.find_element("st_box0").Update("✔")
        window.find_element("st_box0").Update(text_color="green2")
        window.find_element("st_box").Update("MP4 Type 720p")
        window.find_element("720pbutton").Update(button_color=("black","green2"))
        window.find_element("360pbutton").Update(button_color=("black","white"))
        window.find_element("480pbutton").Update(button_color=("black","white"))


