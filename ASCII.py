import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pickle
from argparse import ArgumentParser
import math
import tqdm as tqdm

parser = ArgumentParser()

parser.add_argument(
    "--image_path",
    default="SPARC_ext.jpg",
    type=str,
    help="Path of the image to be converted",
)
parser.add_argument(
    "--bright_path",
    default="sort_bright.pickle",
    type=str,
    help="Path of pickle file storing 'sort_bright'",
)
parser.add_argument(
    "--output_name",
    default="SPARC_result",
    type=str,
    help="Path of the image to be converted",
)
parser.add_argument(
    "--output_mode",
    choices=['text','image'],
    default='image',
    type=str,
    help="Output mode",
)
parser.add_argument(
    "--theme_color",
    nargs="+",
    default=[255,255,255],
    type=int,
    help="Theme color. Enter 2 71 254 for blue",
)
parser.add_argument(
    "--output_size",
    nargs="+",
    default=[180,120],
    type=int,
    help="Output width and height",
)
parser.add_argument(
    "--threshold",
    default=0.85,
    type=float,
    help="Threshold for theme color",
)

args = parser.parse_args()

# Set constants
with open(args.bright_path, 'rb') as f:
    sort_bright = pickle.load(f)
NC=63

# Configure size
w=args.output_size[0]
h=args.output_size[1]


# SPARC blue
IMG=Image.open(args.image_path)
wo=IMG.size[0]
ho=IMG.size[1]
w_cen=wo//2
h_cen=ho//2
if (w_cen/w<h_cen/h):
  w_half=w_cen
  h_half=(int)(w_cen/w*h)
else:
  h_half=h_cen
  w_half=(int)(h_cen/h*w)
IMG=IMG.crop((w_cen-w_half,h_cen-h_half,w_cen+w_half,h_cen+h_half))

# Inner product of color # (0x02,0x47,0xfe) for SPARC blue
tar_color=tuple(args.theme_color)
R1=tar_color[0]*tar_color[0]+tar_color[1]*tar_color[1]+tar_color[2]*tar_color[2]
def inner_product(t_color):
  R2=t_color[0]*t_color[0]+t_color[1]*t_color[1]+t_color[2]*t_color[2]
  if R2==0: 
    return 0
  return (tar_color[0]*t_color[0]+tar_color[1]*t_color[1]+tar_color[2]*t_color[2])/math.sqrt(R1)/math.sqrt(R2)

# Confifure output size
if(args.output_mode=='text'):
  h=(int)(h/2.2) # [840,240]
IMG=IMG.resize((w,h))
nIMG=np.array(IMG)

# Generating ascii art
x=[]
y=[]
char=[]
c=[]
for i in range(h):
  for j in range(w):
    x.append(j)
    y.append(h-1-i)
    bright=(nIMG[i][j][0]/256+nIMG[i][j][1]/256+nIMG[i][j][2]/256)/3
    if inner_product((int(nIMG[i][j][0]),int(nIMG[i][j][1]),int(nIMG[i][j][2])))>args.threshold:
      c.append((bright*tar_color[0]/256,bright*tar_color[1]/256,bright*tar_color[2]/256))
    else:
      c.append((0,0,0))
    c_temp=0
    for k in range(NC):
      if bright<=sort_bright[k][0]:
        c_temp=k
        break
    if bright<=sort_bright[NC-1][0]:
      char.append(sort_bright[c_temp][1])
    else:
      char.append(' ')

if args.output_mode=='image':
  plt.figure(figsize=((int)(32/h*w),32))
  for i in tqdm.tqdm(range(h*w)):
    if char[i]!=' ':
      plt.text(x[i]/w,y[i]/h,char[i],color=c[i],fontsize=12)
  plt.savefig(args.output_name)

else:
  with open(args.output_name+".txt", "w") as file:
    for i in tqdm.tqdm(range(h*w)):
      file.write(char[i])
      if(i%w==w-1):
        file.write('\n')

