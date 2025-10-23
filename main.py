from PIL import Image, ImageDraw, ImageFont
import requests

def stringify(start=0, stop=0,wordList=''):
    text = ' '.join(wordList[start:stop])
    charNum = len(text)
    maxChar = 80 #the maximum number of characters per line
    stopShift = 0 #the amount stop will be shifted at return
    while charNum >= maxChar:
        stopShift+=1
        text = ' '.join(wordList[start:stop-stopShift])
        charNum = len(text)
    return text, stop-stopShift

url = 'https://baconipsum.com/api/'
params = {'type': 'meat-and-filler',
          'format': 'text',
          'sentences': 100}

response = requests.get(url, params=params)

baconText = response.text
wordList = baconText.split()

font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu[wdth,wght]", 36)

im = Image.new('RGB',(1500,2250), 'white')

d = ImageDraw.Draw(im)


start, stop = 0, 15
xCoord = [100]
yCoord = [250]

for i in range(25):
    text, stop = stringify(start=start,stop=stop,wordList=wordList)
    d.text((xCoord[i],yCoord[i]), text=text, anchor='ls', fill='black', font=font)
    xCoord.append(100)
    yCoord.append(yCoord[i]+74)
    start = stop
    stop+=15
    i+=1
im.save("output/testImage.jpeg")
