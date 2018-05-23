import picamera
import pygame
import time
import os
import PIL.Image
import cups
import RPi.GPIO as GPIO

from threading import Thread
from pygame.locals import *
from time import sleep
from PIL import Image, ImageDraw


# initialise global variables
Numeral = ""  # Numeral is the number display
Message = ""  # Message is a fullscreen message
BackgroundColor = ""
CountDownPhoto = ""
CountPhotoOnCart = ""
SmallMessage = ""  # SmallMessage is a lower banner message
TotalImageCount = 0  # Counter for Display and to monitor paper usage
PhotosPerCart = 30  # Selphy takes 16 sheets per tray
imagecounter = 0
imagefolder = 'Photos'
templatePath = os.path.join('Photos', 'Template', "template.png") #Path of template image
ImageShowed = False
Printing = False
BUTTON_PIN = 25
#IMAGE_WIDTH = 558
#IMAGE_HEIGHT = 374
IMAGE_WIDTH = 550
IMAGE_HEIGHT = 360


# Load the background template
bgimage = PIL.Image.open(templatePath)

#Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialise pygame
pygame.init()  # Initialise pygame
pygame.mouse.set_visible(False) #hide the mouse cursor
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w,infoObject.current_h), pygame.FULLSCREEN)  # Full screen 
background = pygame.Surface(screen.get_size())  # Create the background object
background = background.convert()  # Convert it to a background

screenPicture = pygame.display.set_mode((infoObject.current_w,infoObject.current_h), pygame.FULLSCREEN)  # Full screen
backgroundPicture = pygame.Surface(screenPicture.get_size())  # Create the background object
backgroundPicture = background.convert()  # Convert it to a background

transform_x = infoObject.current_w # how wide to scale the jpg when replaying
transfrom_y = infoObject.current_h # how high to scale the jpg when replaying

camera = picamera.PiCamera()
# Initialise the camera object
camera.resolution = (infoObject.current_w, infoObject.current_h)
camera.rotation              = 0
camera.hflip                 = True
camera.vflip                 = False
camera.brightness            = 50
camera.preview_alpha = 120
camera.preview_fullscreen = True
#camera.framerate             = 24
#camera.sharpness             = 0
#camera.contrast              = 8
#camera.saturation            = 0
#camera.ISO                   = 0
#camera.video_stabilization   = False
#camera.exposure_compensation = 0
#camera.exposure_mode         = 'auto'
#camera.meter_mode            = 'average'
#camera.awb_mode              = 'auto'
#camera.image_effect          = 'none'
#camera.color_effects         = None
#camera.crop                  = (0.0, 0.0, 1.0, 1.0)


# A function to handle keyboard/mouse/device input events
def input(events):
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()

			
# set variables to properly display the image on screen at right ratio
def set_demensions(img_w, img_h):
	# Note this only works when in booting in desktop mode. 
	# When running in terminal, the size is not correct (it displays small). Why?

    # connect to global vars
    global transform_y, transform_x, offset_y, offset_x

    # based on output screen resolution, calculate how to display
    ratio_h = (infoObject.current_w * img_h) / img_w 

    if (ratio_h < infoObject.current_h):
        #Use horizontal black bars
        #print "horizontal black bars"
        transform_y = ratio_h
        transform_x = infoObject.current_w
        offset_y = (infoObject.current_h - ratio_h) / 2
        offset_x = 0
    elif (ratio_h > infoObject.current_h):
        #Use vertical black bars
        #print "vertical black bars"
        transform_x = (infoObject.current_h * img_w) / img_h
        transform_y = infoObject.current_h
        offset_x = (infoObject.current_w - transform_x) / 2
        offset_y = 0
    else:
        #No need for black bars as photo ratio equals screen ratio
        #print "no black bars"
        transform_x = infoObject.current_w
        transform_y = infoObject.current_h
        offset_y = offset_x = 0

def InitFolder():
    global imagefolder
    global Message
 
    Message = 'Folder Check...'
    UpdateDisplay()
    Message = ''

	#check image folder existing, create if not exists
    
	if not os.path.isdir(imagefolder):	
		os.makedirs(imagefolder)	
		
	imagefolder2 = os.path.join(imagefolder, 'images')
	if not os.path.isdir(imagefolder2):
		os.makedirs(imagefolder2)
		
def DisplayText(fontSize, textToDisplay):
    global Numeral
    global Message
    global screen
    global background
    global pygame
    global ImageShowed
    global screenPicture
    global backgroundPicture
    global CountDownPhoto

    if (BackgroundColor != ""):
            #print(BackgroundColor)
            background.fill(pygame.Color("black"))
    if (textToDisplay != ""):
            #print(displaytext)
            font = pygame.font.Font(None, fontSize)
            text = font.render(textToDisplay, 1, (227, 157, 200))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery
            if(ImageShowed):
                    backgroundPicture.blit(text, textpos)
            else:
                    background.blit(text, textpos)
				
def UpdateDisplay():
    # init global variables from main thread
    global Numeral
    global Message
    global screen
    global background
    global pygame
    global ImageShowed
    global screenPicture
    global backgroundPicture
    global CountDownPhoto
   
    background.fill(pygame.Color("white"))  # White background
    #DisplayText(100, Message)
    #DisplayText(800, Numeral)
    #DisplayText(500, CountDownPhoto)

    if (BackgroundColor != ""):
            #print(BackgroundColor)
            background.fill(pygame.Color("black"))
    if (Message != ""):
            #print(displaytext)
            font = pygame.font.Font(None, 100)
            text = font.render(Message, 1, (227, 157, 200))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery
            if(ImageShowed):
                    backgroundPicture.blit(text, textpos)
            else:
                    background.blit(text, textpos)

    if (Numeral != ""):
            #print(displaytext)
            font = pygame.font.Font(None, 800)
            text = font.render(Numeral, 1, (227, 157, 200))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery
            if(ImageShowed):
                    backgroundPicture.blit(text, textpos)
            else:
                    background.blit(text, textpos)

    if (CountDownPhoto != ""):
            #print(displaytext)
            font = pygame.font.Font(None, 500)
            text = font.render(CountDownPhoto, 1, (227, 157, 200))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery
            if(ImageShowed):
                    backgroundPicture.blit(text, textpos)
            else:
                    background.blit(text, textpos)
    
    if(ImageShowed == True):
    	screenPicture.blit(backgroundPicture, (0, 0))   	
    else:
    	screen.blit(background, (0, 0))
   
    pygame.display.flip()
    return


def ShowPicture(file, delay):
    global pygame
    global screenPicture
    global backgroundPicture
    global ImageShowed
    backgroundPicture.fill((0, 0, 0))
    img = pygame.image.load(file)
    img = pygame.transform.scale(img, screenPicture.get_size())  # Make the image full screen
    #backgroundPicture.set_alpha(200)
    backgroundPicture.blit(img, (0,0))
    screen.blit(backgroundPicture, (0, 0))
    pygame.display.flip()  # update the display
    ImageShowed = True
    time.sleep(delay)
	
# display one image on screen
def show_image(image_path):	
	screen.fill(pygame.Color("white")) # clear the screen	
	img = pygame.image.load(image_path) # load the image
	img = img.convert()	
	set_demensions(img.get_width(), img.get_height()) # set pixel dimensions based on image	
	x = (infoObject.current_w / 2) - (img.get_width() / 2)
	y = (infoObject.current_h / 2) - (img.get_height() / 2)
	screen.blit(img,(x,y))
	pygame.display.flip()

def CapturePicture():
        global imagecounter
        global imagefolder
        global Numeral
        global Message
        global screen
        global background
        global screenPicture
        global backgroundPicture
        global pygame
        global ImageShowed
        global CountDownPhoto
	global BackgroundColor	
	
	BackgroundColor = ""
	Numeral = ""
        Message = ""
	UpdateDisplay()
	time.sleep(1)
	CountDownPhoto = ""
	UpdateDisplay()
	background.fill(pygame.Color("black"))
	screen.blit(background, (0, 0))
	pygame.display.flip()
	camera.start_preview()
	BackgroundColor = "black"

	for x in range(3, -1, -1):
                if x == 0:                        
                        Numeral = ""
                        Message = "PRENEZ LA POSE"
                else:                        
                        Numeral = str(x)
                        Message = ""                
                UpdateDisplay()
                time.sleep(1)

        BackgroundColor = ""
        Numeral = ""
        Message = ""
        UpdateDisplay()
        imagecounter = imagecounter + 1
        ts = time.time()
        filename = os.path.join(imagefolder, 'images', str(imagecounter)+"_"+str(ts) + '.jpg')
        camera.capture(filename, resize=(IMAGE_WIDTH, IMAGE_HEIGHT))
        camera.stop_preview()
        ShowPicture(filename, 2)
        ImageShowed = False
        return filename
    
	
def TakePictures():
        global imagecounter
        global imagefolder
        global Numeral
        global Message
        global screen
        global background
        global pygame
        global ImageShowed
        global CountDownPhoto
	global BackgroundColor
	global Printing
	global PhotosPerCart
	global TotalImageCount

        input(pygame.event.get())
        CountDownPhoto = "1/3"        
        filename1 = CapturePicture()

        CountDownPhoto = "2/3"
        filename2 = CapturePicture()

        CountDownPhoto = "3/3"
        filename3 = CapturePicture()

        CountDownPhoto = ""
        Message = "Attendez svp..."
        UpdateDisplay()

        image1 = PIL.Image.open(filename1)
        image2 = PIL.Image.open(filename2)
        image3 = PIL.Image.open(filename3)   
        TotalImageCount = TotalImageCount + 1
	
        bgimage.paste(image1, (625, 30))
        bgimage.paste(image2, (625, 410))
        bgimage.paste(image3, (55, 410))
        # Create the final filename
        ts = time.time()
        Final_Image_Name = os.path.join(imagefolder, "Final_" + str(TotalImageCount)+"_"+str(ts) + ".jpg")
        # Save it to the usb drive
        bgimage.save(Final_Image_Name)
        # Save a temp file, its faster to print from the pi than usb
        bgimage.save('/home/pi/Desktop/tempprint.jpg')
        ShowPicture('/home/pi/Desktop/tempprint.jpg',3)
        bgimage2 = bgimage.rotate(90)
        bgimage2.save('/home/pi/Desktop/tempprint.jpg')
        ImageShowed = False
        Message = "Appuyez sur le bouton pour imprimer"
        UpdateDisplay()
        time.sleep(1)
        Message = ""
        UpdateDisplay()
        Printing = False
        WaitForPrintingEvent()
        Numeral = ""
	Message = ""
	print(Printing)
        if Printing:
                if (TotalImageCount <= PhotosPerCart):
                        if os.path.isfile('/home/pi/Desktop/tempprint.jpg'):
                                # Open a connection to cups
                                conn = cups.Connection()
                                # get a list of printers
                                printers = conn.getPrinters()
                                # select printer 0
                                printer_name = printers.keys()[0]
                                Message = "Impression en cours..."
                                UpdateDisplay()
                                time.sleep(1)
                                # print the buffer file
                                printqueuelength = len(conn.getJobs())
                                if printqueuelength > 1:
                                        ShowPicture('/home/pi/Desktop/tempprint.jpg',3)
                                        conn.enablePrinter(printer_name)
                                        Message = "Impression impossible"                
                                        UpdateDisplay()
                                        time.sleep(1)
                                else:
                                        conn.printFile(printer_name, '/home/pi/Desktop/tempprint.jpg', "PhotoBooth", {})
                                        time.sleep(40)            
                else:
                        Message = "Nous vous enverrons vos photos"
                        Numeral = ""
                        UpdateDisplay()
                        time.sleep(1)
                
        Message = ""
        Numeral = ""
        ImageShowed = False
        UpdateDisplay()
        time.sleep(1)

def MyCallback(channel):
    global Printing
    GPIO.remove_event_detect(BUTTON_PIN)
    Printing=True
	
def WaitForPrintingEvent():
    global BackgroundColor
    global Numeral
    global Message
    global Printing
    global pygame
    countDown = 5
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING)
    GPIO.add_event_callback(BUTTON_PIN, MyCallback)
    
    while Printing == False and countDown > 0:
        if(Printing == True):
            return
        for event in pygame.event.get():			
            if event.type == pygame.KEYDOWN:				
                if event.key == pygame.K_DOWN:
                    GPIO.remove_event_detect(BUTTON_PIN)
                    Printing = True
                    return        
        BackgroundColor = ""
        Numeral = str(countDown)
        Message = ""
        UpdateDisplay()        
        countDown = countDown - 1
        time.sleep(1)

    GPIO.remove_event_detect(BUTTON_PIN)
        
	
def WaitForEvent():
    global pygame
    NotEvent = True
    while NotEvent:
            input_state = GPIO.input(BUTTON_PIN)
            if input_state == False:
                    NotEvent = False			
                    return
            for event in pygame.event.get():			
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                        if event.key == pygame.K_DOWN:
                            NotEvent = False
                            return
            time.sleep(0.2)

def main(threadName, *args):
	InitFolder()
    while True:
            show_image('images/start_camera.jpg')
            WaitForEvent()
            time.sleep(0.2)
            TakePictures()
    GPIO.cleanup()


# launch the main thread
Thread(target=main, args=('Main', 1)).start()
