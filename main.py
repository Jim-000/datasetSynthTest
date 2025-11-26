from PIL import Image, ImageDraw, ImageFont
import requests
import random

headerLocations = {
    "pageNumberHeader": {
        "X": 1125,
        "Y": 50
    },
    "runningHeader": {
        "X": 250,
        "Y": 50
    }
}

font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu[wdth,wght]", 36)

def stringify(start=0, stop=0,paraNum=0,indent=False,wordList=[]):
    print("len wordList ", len(wordList))
    print("paraNum ",paraNum)
    paragraph = wordList[paraNum]
    paraList = paragraph.split(" ")
    
    if stop > len(paraList): #spaghetti
        text = ' '.join(paraList[start:len(paraList)])
        text = text + "\n"
        stop = 0
        paraNum+=1
    else:
        text = ' '.join(paraList[start:stop])
    charNum = len(text)
    maxChar = 80 #the arbitrary max number of characters per line
    stopShift = 0 #the amount stop will be shifted at return
    while charNum >= maxChar:
        stopShift+=1
        text = ' '.join(paraList[start:stop-stopShift])
        charNum = len(text)
    if indent == True:
        text = "    " + text
    return text, stop-stopShift, paraNum #spaghetti code, yippee!

def elementFill(d=ImageDraw):
    l = headerLocations
    pageNumber = random.randint(1,1000)
    global font
    d.text((l["pageNumberHeader"]["X"],l["pageNumberHeader"]["Y"]), text=pageNumber, anchor='ls', fill='black',font=font)


url = 'https://baconipsum.com/api/'
params = {'type': 'meat-and-filler',
          'format': 'text',
          'paras': 100}

response = requests.get(url, params=params)

baconText = response.text

wordList = baconText.split("\n\n")

font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu[wdth,wght]", 36)
pages = 1

while pages < 2: #Another arbitrary int. This one gives number of pages to be created.
    im = Image.new('RGB',(1500,2250), 'white')

    d = ImageDraw.Draw(im)


    xCoord = [100]
    yCoord = [250]
    lines = 25
    currLine = 0
    indent = True
    paraNum, start, stop = 0, 0, 15
    elementFill(d)
    while lines > 0: #more loopy than froot loops?
        lastParaNum = paraNum #spaghetti?
        text, start, paraNum = stringify(start=start,stop=stop,paraNum=paraNum,indent=indent,wordList=wordList)
        if paraNum != lastParaNum: #more spaghetti
            indent = True
        else:
            indent = False
        d.text((xCoord[currLine],yCoord[currLine]), text=text, anchor='ls', fill='black', font=font)
        xCoord.append(100)
        yCoord.append(yCoord[currLine]+74)
        stop+=15
        lines-=1
        currLine+=1

    im.save(f"projects/datasetSynthTest/output/testImage{pages}.jpeg")
    pages+=1

#Extra: experimenting with concatation to make full spread
def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

im1 = Image.open('projects/datasetSynthTest/output/testImage.jpeg')
im2 = Image.open('projects/datasetSynthTest/output/testImage1.jpeg')
get_concat_h(im1, im2).save('projects/datasetSynthTest/output/testImageConcate.jpeg')
