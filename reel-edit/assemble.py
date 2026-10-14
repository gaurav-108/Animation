import subprocess
T=0.5; CUTS=[0,2.95,7.07,10.83,14.75,18.60,22.60,27.07]
TR=['fade','fadeblack','fade','fade','fade','fade']   # dip to black into "raat afsana"
F1='fonts/Cormorant600.ttf'; F2='fonts/GreatVibes-Regular.ttf.ttf'
LY=[("Tu hai toh",0.15,"khaas hai",0.9,2.7),
    ("Tu hai toh",3.15,"khwabon jaise din",3.8,6.8),
    ("Tu hai toh",7.35,"raat afsana",7.9,10.6),
    ("Ke har lamha",11.0,"karun haske",12.5,14.5),
    ("Mere rab ka",14.95,"main shukrana",16.5,18.4),
    ("Tu hai humdum",18.8,"humdum hai jaana",19.8,22.4),
    ("Mere dil ka",22.8,"mere dil ka",24.6,26.5)]
def dt(text,font,size,color,y,S,E):
    a=f"if(lt(t\\,{S}+0.45)\\,(t-{S})/0.45\\,if(lt(t\\,{E}-0.4)\\,1\\,({E}-t)/0.4))"
    yy=f"{y}+14*(1-min(1\\,(t-{S})/0.7))"
    return (f"drawtext=fontfile={font}:text='{text}':fontsize={size}:fontcolor={color}:x=(w-text_w)/2:y={yy}"
            f":shadowcolor=black@0.55:shadowx=2:shadowy=3:borderw=1:bordercolor=black@0.15:alpha='{a}':enable='between(t\\,{S}\\,{E})'")
g=[]; prev='[0:v]'
for k in range(1,7):
    out=f'[x{k}]'; g.append(f"{prev}[{k}:v]xfade=transition={TR[k-1]}:duration={T}:offset={CUTS[k]-T/2:.3f}{out}"); prev=out
d=[]
for l1,s1,l2,s2,e in LY:
    d.append(dt(l1,F1,70,'white@0.96',1500,s1,e))
    d.append(dt(l2,F2,124,'0xF7DEA8',1578,s2,e))
g.append(f"color=black:s=1080x1920:r=60:d=27.07[blk];[blk][8:v]alphamerge,format=yuva420p,colorchannelmixer=aa=0.55[gr];{prev}[gr]overlay=0:0[ov]");prev="[ov]"
g.append(f"{prev}"+",".join(d)+",fade=t=in:st=0:d=0.35,fade=t=out:st=26.35:d=0.72,format=yuv420p[v]")
g.append("[7:a]atrim=0:27.07,afade=t=in:d=0.05,afade=t=out:st=26.3:d=0.77,aresample=48000[a]")
open('fc.txt','w').write(";\n".join(g))
cmd=["ffmpeg","-v","error","-y"]+sum([["-i",f"seg/s{k}.mp4"] for k in range(7)],[])+["-i","song.m4a","-loop","1","-framerate","60","-i","grad.png","-filter_complex_script","fc.txt","-map","[v]","-map","[a]","-r","60","-c:v","libx264","-preset","slow","-crf","14","-profile:v","high","-level","4.2","-pix_fmt","yuv420p","-movflags","+faststart","-c:a","aac","-b:a","256k","-t","27.07","final.mp4"]
subprocess.run(cmd,check=True)
