import subprocess, numpy as np
for c in [1,2,3,4,5,6,7]:
    raw=subprocess.run(f"ffmpeg -v error -i stab/c{c}.mp4 -vf fps=4,scale=180:320 -f rawvideo -pix_fmt rgb24 -",shell=True,capture_output=True).stdout
    a=np.frombuffer(raw,np.uint8).reshape(-1,3).astype(float)/255
    lo=np.percentile(a,0.3,axis=0); hi=np.percentile(a,99.7,axis=0)
    print(c,"lo",np.round(lo,3),"hi",np.round(hi,3))
