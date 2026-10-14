import subprocess, sys, json
T=0.5  # dissolve length
# (stab clip, src start, speed, song window start, end, grade, glow)
G={
1:"curves=r='0/0 0.5/0.53 1/1':b='0/0.03 0.5/0.47 1/0.94',eq=contrast=1.08:saturation=1.15:gamma=0.97,colorbalance=rs=-0.03:bs=0.04:rh=0.05:bh=-0.05",
2:"curves=master='0/0 0.25/0.24 0.75/0.82 1/1',eq=contrast=1.06:saturation=1.2:gamma=1.08,colorbalance=rs=-0.04:bs=0.05:rh=0.04:gh=0.01:bh=-0.03",
3:"colorlevels=rimin=0.165:gimin=0.157:bimin=0.157:rimax=0.89:gimax=0.88:bimax=0.9,curves=master='0/0 0.25/0.2 0.5/0.5 0.75/0.81 1/1',eq=saturation=1.35:gamma=0.97,colorbalance=rs=-0.05:bs=0.08:rm=-0.03:bm=0.05:rh=-0.01:bh=0.04",
4:"colorlevels=rimin=0.03:gimin=0.01:bimin=0.01:rimax=0.86:gimax=0.85:bimax=0.88,curves=master='0/0 0.25/0.22 0.5/0.5 0.75/0.79 1/1',eq=saturation=1.1,colorbalance=rs=-0.02:bs=0.02:rh=0.03:gh=0.015:bh=-0.03",
5:"colorlevels=rimin=0.23:gimin=0.227:bimin=0.227:rimax=0.86:gimax=0.86:bimax=0.86,curves=master='0/0 0.25/0.17 0.5/0.5 0.75/0.83 1/1',eq=saturation=1.9:gamma=1.02,colorbalance=rs=0.02:bs=-0.03:rm=0.07:gm=0.02:bm=-0.08:rh=0.08:gh=0.04:bh=-0.08",
6:"eq=contrast=1.06:saturation=1.25:gamma=1.06,colorbalance=rs=-0.03:bs=0.04:rh=0.03:bh=-0.02",
7:"colorlevels=rimin=0.149:gimin=0.145:bimin=0.122:rimax=0.87:gimax=0.86:bimax=0.9,curves=master='0/0 0.25/0.2 0.5/0.5 0.75/0.81 1/1',eq=saturation=1.3:gamma=1.02,colorbalance=bs=0.03:rm=0.03:bm=-0.03:rh=0.04:bh=-0.03",
}
GLOW={1:.12,2:.06,3:.10,4:.15,5:.18,6:.06,7:.14}
SEG=[(1,1.4,0.7),(2,0.2,0.5),(3,0.9,0.5),(4,0.15,0.65),(5,0.0,0.65),(6,0.0,0.5),(7,0.3,0.75)]
CUTS=[0,2.95,7.07,10.83,14.75,18.60,22.60,27.07]
def dur(k):
    a=CUTS[k]-(T/2 if k>0 else 0); b=CUTS[k+1]+(T/2 if k<6 else 0); return b-a
def chain(c,ss,sp,D,interp=True):
    sd=D*sp+0.1
    f=f"trim=start={ss}:duration={sd:.3f},setpts=(PTS-STARTPTS)/{sp}"
    if interp and sp<0.99: f+=",minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1:scd=none"
    f+=f",fps=60,hqdn3d=1.2:1.2:3:3,{G[c]},scale=1080:1920:flags=lanczos,format=gbrp,split[a][b];[b]gblur=sigma=30[bb];[a][bb]blend=all_mode=screen:all_opacity={GLOW[c]},unsharp=5:5:0.55:5:5:0,vignette=angle=PI/8,trim=duration={D:.4f},setpts=PTS-STARTPTS,format=yuv420p"
    return f
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="still":   # graded vs raw preview frames
        for k,(c,ss,sp) in enumerate(SEG):
            t=ss+0.8
            subprocess.run(f"""ffmpeg -v error -y -ss {t} -i stab/c{c}.mp4 -filter_complex "[0]split[r][g];[g]{G[c]},scale=1080:1920,format=gbrp,split[a][b];[b]gblur=sigma=30[bb];[a][bb]blend=all_mode=screen:all_opacity={GLOW[c]},vignette=angle=PI/8,scale=270:480[gg];[r]scale=270:480,format=gbrp[rr];[rr][gg]hstack" -frames:v 1 prev{c}.png""",shell=True,check=True)
    elif mode=="seg":
        k=int(sys.argv[2]); c,ss,sp=SEG[k]; D=dur(k)
        subprocess.run(["ffmpeg","-v","error","-y","-i",f"stab/c{c}.mp4","-filter_complex",chain(c,ss,sp,D),"-an","-c:v","libx264","-preset","slow","-crf","8","-pix_fmt","yuv420p",f"seg/s{k}.mp4"],check=True)
        print("seg",k,"D",round(D,3))
