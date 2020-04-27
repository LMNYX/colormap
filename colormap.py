from PIL import Image, ImageDraw, ImageFont
import argparse, os, re

parser = argparse.ArgumentParser(description="Proccesses file into colormap image.")
parser.add_argument('-f', '--from', dest="fromFile", type=str, help="Import from file")
parser.add_argument('-t', '--to', dest="toFile", type=str, help="Export to file")
args = parser.parse_args()
if(args.fromFile == None):
    print("Missing required arguments.")
    parser.print_help()
    os._exit(0)
if(args.toFile == None):
    print("toFile argument is missing saving to colormap.png")
    args.toFile = "colormap.png"

print("Starting colormap variable generation...")

print("-------------------------------------------------")

maxchr = 0
def Parse(text):
    global maxchr
    text = text.split('\n')
    v = []
    for line in text:
        res = re.findall(r'#(\w+) ([(](.*)[)])', line)
        for r in res:
            print("#{0} - {1}".format(r[0], r[2]))
            if(len(r[2]) > maxchr):
                maxchr = len(r[2])
            v.append([r[0], r[2]])
    return v

linenumber = 0
colormap = None

with open(args.fromFile, "r",encoding="utf-8") as f:
    fl = f.read()
    linenumber = len(fl.split('\n'))
    colormap = Parse(fl)

print("-------------------------------------------------")

print("Starting image generation...")
FontSaved = ImageFont.truetype('res/FreeMono.ttf', 21)
img = Image.new('RGB', (128+(13*maxchr),64+(19*len(colormap))), color='white')
draw = ImageDraw.Draw(img)
position = 1
for clr in colormap:
    print(str(clr))
    draw.rectangle([16,16+(19*position),32,32+(19*position)], fill="#"+clr[0], outline="black")
    draw.text((38,16+(19*position)-2), clr[1], font=FontSaved, fill="black")
    position += 1
del draw
img.save(args.toFile, "PNG")
print("-------------------------------------------------")
print("Saved to "+args.toFile)