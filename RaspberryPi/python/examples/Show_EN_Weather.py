#!/usr/bin/python

#This program is provided for educational purposes only and should 
# not be used for any commercial purpose. If there is any infringement,
# please contact me to delete.

# EZ Updated to work with 7 inch B (black/red/white) device and added Debugging info

import os
import urllib
import sys
import logging

logging.basicConfig(level=logging.WARNING) # DEBUG or INFO or WARNING (default) or ERROR

path = os.path.realpath(os.path.dirname(sys.argv[0]))

picdir = path + '/../pic'
libdir = path + '/../lib'
logging.debug ('libdir: %s' % libdir)
if os.path.exists(libdir):
    sys.path.append(libdir)

from Weather import Get_EN_Weather
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
from PIL import Image

logging.debug ('%d argument(s): %s' % (len(sys.argv)-1, sys.argv))

if(len(sys.argv) > 2 and sys.argv[2] == 'debug'):
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug('Debugging ON')

if(len(sys.argv) > 1 and sys.argv[1] == '12'):
    import epd12in48
    logging.info ('epd12in48')
    Color_Type   = 1
    Inage_WIDTH  = epd12in48.EPD_WIDTH
    Inage_HEIGHT = epd12in48.EPD_HEIGHT
    epd = epd12in48.EPD()
    
elif(len(sys.argv) > 1 and (sys.argv[1] == 'B' or sys.argv[1] == 'b')):
    from waveshare_epd import epd12in48b
    logging.info("Display type: epd12in48b")
    Color_Type   = 2
    Inage_WIDTH  = epd12in48b.EPD_WIDTH
    Inage_HEIGHT = epd12in48b.EPD_HEIGHT
    epd = epd12in48b.EPD()

elif(len(sys.argv) > 1 and (sys.argv[1] == '7B' or sys.argv[1] == '7b')):
    import epd7in5b_V2
    logging.info("Display type: epd7in5b_V2")
    Color_Type   = 2
    Inage_WIDTH  = epd7in5b_V2.EPD_WIDTH
    Inage_HEIGHT = epd7in5b_V2.EPD_HEIGHT
    epd = epd7in5b_V2.EPD()

else:
    print('If you are using epd_12in48   please run: python %s 12'  % sys.argv[0])
    print('If you are using epd_12in48B  please run: python %s 12b' % sys.argv[0])
    print('If you are using epd_7in5b_V2 please run: python %s  7b' % sys.argv[0])
    print('And if you want to see mode debugging info, add debug to the end: python %s  7b debug' % sys.argv[0])
    sys.exit(0)

logging.debug("Display Width = %i, Height = %i", Inage_WIDTH, Inage_HEIGHT)
##################################################
Blackimage = Image.new("1", (Inage_WIDTH, Inage_HEIGHT), 255)
Otherimage = Image.new("1", (Inage_WIDTH, Inage_HEIGHT), 255)
# Create drawing context
Black = ImageDraw.Draw(Blackimage)
Other = ImageDraw.Draw(Otherimage)
if(Color_Type == 1):
    Painting = Black
    Painting_image = Blackimage
else:
    Painting = Other
    Painting_image = Otherimage
##################################################
logging.debug ("Ready drawing")

def Display_Init():
    logging.debug("e-paper init...")
    epd.init()
#    logging.debug("clearing...")
#    epd.clear()

def Display():
    if(Color_Type == 1):
        epd.display(Blackimage)
    else:
        epd.display(epd.getbuffer(Blackimage), epd.getbuffer(Otherimage))
    time.sleep(2)

def Display_END():
    logging.debug("goto sleep...")
    epd.sleep()
##################################################

font20 = ImageFont.truetype(picdir+"/Font.ttc",  10)
font25 = ImageFont.truetype(picdir+"/Font.ttc",  12)
font30 = ImageFont.truetype(picdir+"/Font.ttc",  15)
font35 = ImageFont.truetype(picdir+"/Font.ttc",  17)
font40 = ImageFont.truetype(picdir+"/Font.ttc",  20)
font45 = ImageFont.truetype(picdir+"/Font.ttc",  20)
font50 = ImageFont.truetype(picdir+"/Font.ttc",  25)
font55 = ImageFont.truetype(picdir+"/Font.ttc",  25)
font60 = ImageFont.truetype(picdir+"/Font.ttc",  30)
font70 = ImageFont.truetype(picdir+"/Font.ttc",  35)
font80 = ImageFont.truetype(picdir+"/Font.ttc",  40)
font110 = ImageFont.truetype(picdir+"/Font.ttc", 55)

# 6 horizontal columns, 3 vertical rows
W_Proportion = int(Inage_WIDTH/6)
H_Proportion = int(Inage_HEIGHT/3)

logging.info("Getting Weather")
Weather = Get_EN_Weather.Weather()

logging.info("Extracting Weather data")
Week = Weather.Extract_Week()
Date = Weather.Extract_Date()
Wea  = Weather.Extract_Wea()
TemHigh  = Weather.Extract_TemHigh()
TemLow  = Weather.Extract_TemLow()
TemHourly  = Weather.Extract_TemHourly()
TimeHourly  = Weather.Extract_TimeHourly()
Tem  = Weather.Extract_Tem()
OtherData  = Weather.Extract_OtherData()
City  = Weather.Extract_City()
RealTimeWeather  = Weather.Extract_RealTimeWeather()
Weather.Extract_Map()

logging.info("Drawing")
Display_Init()
#############################################################
Now = time.localtime()
Now = time.strftime("%H:%M", Now)
Now = "Updated " + Now
logging.debug("Draw update time %s", Now)
Black.text((Inage_WIDTH-5-font25.getsize(Now)[0],1), Now, font = font25, fill = 0)

logging.debug("City: %s", City)
Black.text((10,1), City, font = font80, fill = 0)

logging.debug("Temp: %s", Tem)
logging.debug(" Width in pixels with 110 (actually 55) font: %d", font110.getsize(Tem)[0]*len(Tem))
#Painting.text((110-len(Tem)*55,H_Proportion/4),Tem, font = font110, fill = 0)
Painting.text((80-font110.getsize(Tem)[0],H_Proportion/4),Tem, font = font110, fill = 0)
Black.text((80,H_Proportion/4),u'\N{DEGREE SIGN}C', font = font50, fill = 0)

logging.debug("RealTimeWeather: %s", RealTimeWeather)
Black.text((W_Proportion,H_Proportion/4), RealTimeWeather, font = font50, fill = 0)

logging.debug("Otherdata 0,1: %s, %s", OtherData[0], OtherData[1])
Black.text((W_Proportion,H_Proportion/6*3), OtherData[0], font = font30, fill = 0)
Black.text((W_Proportion,H_Proportion/6*4), OtherData[1], font = font30, fill = 0)

logging.debug("Otherdata 2,3: %s, %s", OtherData[2], OtherData[3])
Black.text((int(W_Proportion*2.5),H_Proportion/6*3), OtherData[2], font = font30, fill = 0)
Black.text((int(W_Proportion*2.5),H_Proportion/6*4), OtherData[3], font = font30, fill = 0)

logging.debug("Otherdata 4,5: %s, %s", OtherData[4], OtherData[5])
Black.text((int(W_Proportion*4),H_Proportion/6*3), OtherData[4], font = font30, fill = 0)
Black.text((int(W_Proportion*4),H_Proportion/6*4), OtherData[5], font = font30, fill = 0)

######## DOTTED LINE #####################################################
for i in range(0, Inage_WIDTH, 10):
    logging.debug("Ellipse %i,%i to %i,%i", i-2, H_Proportion/6*5-2, i+2, H_Proportion/6*5+2)
    Black.ellipse([i-2, H_Proportion/6*5-2, i+2, H_Proportion/6*5+2], fill = 0)

######## 6 vertical columns with date text images and min max temp ######################################
for i in range(0, 6):
    if (i != 0):
        logging.debug("Line: %i,%i to %i,%i", W_Proportion*i,H_Proportion,W_Proportion*i,H_Proportion*2)
        Black.line([(W_Proportion*i,H_Proportion),(W_Proportion*i,H_Proportion*1.75)], fill = 0,width = 3)
    Black.text((W_Proportion*i+30,H_Proportion +  0), Week[i]+' '+Date[i], font = font25, fill = 0)    
    Black.text((W_Proportion*i+30,H_Proportion + 20), Wea[i], font = font25, fill = 0)

    PNG = Image.open(str(i) +".png")	
    Painting_image.paste(PNG, (W_Proportion*i+ 10, H_Proportion + 40)) 
    
    Black.text((W_Proportion*i+85,H_Proportion + 60), TemHigh[i]+u'\N{DEGREE SIGN}C', font = font45, fill = 0)
    Black.text((W_Proportion*i+85,H_Proportion + 80), TemLow[i]+u'\N{DEGREE SIGN}C', font = font45, fill = 0)

######### Graph #########################################

temp = [None]*24
for i in range(0, 24):
    temp[i]  = int(TemHourly[i])

temp.sort()
if(temp[len(temp)-1] < 0): tem_max = int( temp[len(temp)-1]   /3.0)*3 # Note: int casting removes decimals, does not round...
else:                      tem_max = int((temp[len(temp)-1]+2)/3.0)*3
if(temp[0] < 0): tem_min = int((temp[0]-2)/3.0)*3
else:            tem_min = int( temp[0]   /3.0)*3
logging.debug("temp(len -1) %f, normalized max %i", temp[len(temp)-1], tem_max)
logging.debug("temp(     0) %f, normalized min %i", temp[0], tem_min)
tem_H_Proportion = int(H_Proportion/(tem_max - tem_min))
tem_W_Proportion = int((Inage_WIDTH-50)/24)
logging.debug("tem Height proportion %i", tem_H_Proportion)
logging.debug("tem Width  proportion %i", tem_W_Proportion)

# X Axis
if(tem_min<=0 and tem_max>=0):
  # Draw zero line
  logging.debug("Line: %i,%i to %i,%i", 50,Inage_HEIGHT-(30-tem_min*tem_H_Proportion),Inage_WIDTH-50,Inage_HEIGHT-(30-tem_min*tem_H_Proportion))
  Black.line([(50,Inage_HEIGHT-(30-tem_min*tem_H_Proportion)),(Inage_WIDTH-50,Inage_HEIGHT-(30-tem_min*tem_H_Proportion))],  fill = 0,width = 3)
else:
  # dotted x axis
  for x in range(50,Inage_WIDTH-50,4):
    Black.line([(x,Inage_HEIGHT-30),(x+2,Inage_HEIGHT-30)],  fill = 0,width = 1)
#  else: # one of them is zero
#   # solid x axis
#    Black.line([(50,Inage_HEIGHT-30),(Inage_WIDTH-50,Inage_HEIGHT-30)],  fill = 0,width = 3)

# Y axis
Black.line([(50,Inage_HEIGHT-30),(50,Inage_HEIGHT-30-H_Proportion)], fill = 0,width = 3)
# Arrows
#Black.line([(Inage_WIDTH-50-5,Inage_HEIGHT-30-5),(Inage_WIDTH-50,Inage_HEIGHT-30)], fill = 0,width = 3)
#Black.line([(Inage_WIDTH-50-5,Inage_HEIGHT-30+5),(Inage_WIDTH-50,Inage_HEIGHT-30)], fill = 0,width = 3)
#Black.line([(50-5,Inage_HEIGHT-H_Proportion+20+5),(50,Inage_HEIGHT-H_Proportion+20)], fill = 0,width = 3)
#Black.line([(50+5,Inage_HEIGHT-H_Proportion+20+5),(50,Inage_HEIGHT-H_Proportion+20)], fill = 0,width = 3)

# Hourly graph & temp & x axis text
for i in range(0,24, 1):
    logging.debug("i = %i, TimeHourly = %s, TemHourly = %s" % (i, TimeHourly[i], TemHourly[i]))
    arc_dax = 4
    y1 = Inage_HEIGHT-30-int((int(TemHourly[i])-tem_min)*tem_H_Proportion)
    if(i!=23):
        y2 = Inage_HEIGHT-30-int((int(TemHourly[i+1])-tem_min)*tem_H_Proportion)
        logging.debug("Line: %i,%i to %i,%i", 50+tem_W_Proportion*i,y1,50+tem_W_Proportion*(i+1),y2)
        Painting.line([(50+tem_W_Proportion*i,y1),(50+tem_W_Proportion*(i+1),y2)], fill = 0,width = 3)
    else:
        Painting.text((50+tem_W_Proportion*i,y1-30), TemHourly[i]+u'\N{DEGREE SIGN}C', font = font20, fill = 0)
        logging.debug("Ellipse %i,%i to %i,%i", 50+tem_W_Proportion*i-arc_dax, y1-arc_dax, 50+tem_W_Proportion*i+arc_dax, y1+arc_dax)
        Black.ellipse([50+tem_W_Proportion*i-arc_dax, y1-arc_dax, 50+tem_W_Proportion*i+arc_dax, y1+arc_dax], fill = 0)
        if(tem_min<0 and tem_max>0):
          # At zero line
          Black.text((50+tem_W_Proportion*i, Inage_HEIGHT-(27-tem_min*tem_H_Proportion)), TimeHourly[i], font = font25, fill = 0)
        else:
          # At x axis
          Black.text((50+tem_W_Proportion*i, Inage_HEIGHT-27), TimeHourly[i], font = font25, fill = 0)
        
    if((i%3) == 0):
        Painting.text((50+tem_W_Proportion*i,y1-30), TemHourly[i]+u'\N{DEGREE SIGN}C', font = font20, fill = 0)
        logging.debug("Ellipse %i,%i to %i,%i", 50+tem_W_Proportion*i-arc_dax, y1-arc_dax, 50+tem_W_Proportion*i+arc_dax, y1+arc_dax)
        Black.ellipse([50+tem_W_Proportion*i-arc_dax, y1-arc_dax, 50+tem_W_Proportion*i+arc_dax, y1+arc_dax], fill = 0)
        if(tem_min<0 and tem_max>0):
          # At zero line
          Black.text((50+tem_W_Proportion*i, Inage_HEIGHT-(27-tem_min*tem_H_Proportion)), TimeHourly[i], font = font25, fill = 0)
        else:
          # At x axis
          Black.text((50+tem_W_Proportion*i, Inage_HEIGHT-27), TimeHourly[i], font = font25, fill = 0)

#Y axis
Black.text((10,Inage_HEIGHT-30-H_Proportion*0/4), str(tem_min+int((tem_max - tem_min)*0/4)), font = font30, fill = 0)
Black.text((10,Inage_HEIGHT-30-H_Proportion*1/4), str(tem_min+int((tem_max - tem_min)*1/4)), font = font30, fill = 0)
Black.text((10,Inage_HEIGHT-30-H_Proportion*2/4), str(tem_min+int((tem_max - tem_min)*2/4)), font = font30, fill = 0)
Black.text((10,Inage_HEIGHT-30-H_Proportion*3/4), str(tem_min+int((tem_max - tem_min)*3/4)), font = font30, fill = 0)
Black.text((10,Inage_HEIGHT-30-H_Proportion*4/4), str(tem_min+int((tem_max - tem_min)*4/4)), font = font30, fill = 0)
#############################################################  
logging.debug("Display:")
Display()
logging.debug("Display END:")
Display_END()
logging.debug("Save:")
#Colorimage = Image.new("P", (Inage_WIDTH, Inage_HEIGHT), 255)
# putpalette() input is a sequence of [r, g, b, r, g, b, ...]
#Colorimage.putpalette([0, 0, 0, 102, 102, 102, 176, 176, 176, 255, 255, 255])


logging.info("Done.")