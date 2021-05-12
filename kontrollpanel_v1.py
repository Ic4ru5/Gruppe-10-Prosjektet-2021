import pygame
import datetime as dt
from time import sleep
import requests
import json

# User specific ids
user_id = 4


# RGB colors for icons
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
yellow_dark = (255,200,0)
yellow_light = (255,255,200)
grey = (50,50,50)
light_blue = (100,100,255)
green = (0,255,0)
blue = (0,0,255)


# lists of the months of the year, and the days of each month
# used for the bookings
months = ["January", "February", "March", "April", "May",
    "June", "July", "August", "September", "October", "November", "December"]
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


# The rooms of the menu
rooms = ["living", "kitchen", "bathroom", "sleep 1", "sleep 2", "sleep 3", "sleep 4", "sleep 5", "RPI-room"]

# The keys and tokens for all the acording ids
kontrollkey = ["158", "8932", "458", "1776"]
personalkey = ["13254", "8056", "11150", "29471"]
token = ["eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0ODk2In0.uDXPvOeCqQhEr7HlqYoolhRaVh-QzcCaBQIcgRCHHE4", 
            "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MDgwIn0.JqLFfCKkjyl_3-LKr2_UIPsu53JuyOw_oiZZ5JX8_n0",
            "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MTkxIn0.67_wTOsrUBgKMcvhMVi7AS-yFOsJWRrtQzDs9fEu4zM",
            "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MjE1In0.pLf4zCRh8J0ZA1MBsp7hIYGJGqSbc93B4e_KAjUNivk"]


# The CoT signals
class Signal:
    # initiation of a signal
    def __init__(self, key, token):
        self.key = key
        self.token = token
        
    # getting the value of the signal
    def get(self):
        response = requests.get('https://circusofthings.com/ReadValue', 
                        params = {'Key':self.key, 'Token':self.token})
        response = json.loads(response.content)
        return response["Value"]
    
    # writing a value to the signal
    def write(self, value):
        data ={'Key': self.key, 'Value': value, 'Token': self.token}
        requests.put('https://circusofthings.com/WriteValue',
                        data = json.dumps(data),
                        headers={'Content-Type':'application/json'})



booking_signal = Signal(kontrollkey[user_id-1], token[user_id-1])           # the bookingsignal of current user
personal_signal = Signal(personalkey[user_id-1], token[user_id-1])          # the personal signal of current user

# the presonal signals of all the users
pers1 = Signal(personalkey[0],token[user_id-1])
pers2 = Signal(personalkey[1],token[user_id-1])
pers3 = Signal(personalkey[2],token[2])
pers4 = Signal(personalkey[3],token[user_id-1])
#pers5 = Signal(personalkey[4],token[4])                if we had a fifth person







def main_layout(screen):
    # getting the dimensions of the display
    w,h = screen.get_width(), screen.get_height()
    pygame.draw.rect(screen, black, (0,0,w,h))

    font = pygame.font.Font('freesansbold.ttf', 10)
    
    # ------------ the rooms ---------------
    # sleep 1
    pygame.draw.rect(screen, white, (3*w/320,49*h/160,5*w/32,37*h/120),2)
    text_sleep1 = font.render('sleep 1', True, red)
    screen.blit(text_sleep1, (w/64,151*h/480)) 

    # sleep 2
    pygame.draw.rect(screen, white, (21*w/128,9*h/16,5*w/32,37*h/120),2)
    text_sleep2 = font.render('sleep 2', True, red)
    screen.blit(text_sleep2, (109*w/640,137*h/240)) 

    # sleep 3
    pygame.draw.rect(screen, white, (41*w/128,9*h/16,5*w/32,37*h/120),2)
    text_sleep3 = font.render('sleep 3', True, red)
    screen.blit(text_sleep3, (209*w/640,137*h/240)) 

    # sleep 4
    pygame.draw.rect(screen, white, (87*w/128,9*h/16,5*w/32,37*h/120),2)
    text_sleep4 = font.render('sleep 4', True, red)
    screen.blit(text_sleep4, (439*w/640,137*h/240)) 

    # sleep 5
    pygame.draw.rect(screen, white, (107*w/128,9*h/16,5*w/32,37*h/120),2)
    text_sleep5 = font.render('sleep 5', True, red)
    screen.blit(text_sleep5, (549*w/640,137*h/240)) 

    # rpi room
    pygame.draw.rect(screen, white, (21*w/128,13*h/80,9*w/32,31*h/120),2)
    text_rpi_room = font.render('rpi room', True, red)
    screen.blit(text_rpi_room, (109*w/640,41*h/240)) 

    # bathroom
    pygame.draw.rect(screen, white, (107*w/128,13*h/60,5*w/32,49*h/240),2)
    text_bathroom = font.render('bathroom', True, red)
    screen.blit(text_bathroom, (539*w/640,9*h/40)) 

    # kitchen / Tv area
    pygame.draw.line(screen,white, (57*w/128,11*h/48), (107*w/128,11*h/48),2)  # rpi - batroom
    pygame.draw.line(screen,white, (317*w/320,101*h/240), (317*w/320,9*h/16),2)  # bathroom - sleep 5
    pygame.draw.line(screen,white, (61*w/128,5*h/6), (87*w/128,5*h/6),2)  # sleep 4 - sleep 3
    text_kitchen = font.render('kitchen', True, red)
    screen.blit(text_kitchen, (289*w/640,19*h/80)) 
    text_tv_area = font.render('tv_area', True, red)
    screen.blit(text_tv_area, (309*w/640,16*h/9)) 

    # entrance
    pygame.draw.line(screen,white, (87*w/128,3*h/160), (87*w/128,19*h/48),2)    # kitchen / left entrance
    pygame.draw.line(screen,white, (87*w/128,3*h/160), (55*w/64,3*h/160),2)      # top entrance
    pygame.draw.line(screen,white, (55*w/64,3*h/160), (55*w/64,13*h/60),2)    # right entrance
    text_entrance = font.render('entrance', True, red)
    screen.blit(text_entrance, (439*w/640,13*h/480)) 

    
    # the button for viewing signals
    pygame.draw.rect(screen, white, (0,7*h/8,w/8,h/8),0)
    text_signals = font.render('view signals', True, black)
    screen.blit(text_signals, (0,9*h/10)) 


    # drawing the current position of people with stickfigures
    greenstickman = pygame.image.load("Pics/greenstick2.png").convert_alpha()
    bluestickman = pygame.image.load("Pics/bluestick1.png").convert_alpha()
    yellowstickman = pygame.image.load("Pics/yellowstick.png").convert_alpha()
    redstickman = pygame.image.load("Pics/redstick.png").convert_alpha()

    #checking where each person is
    sigpers1 = str(pers1.get())
    sigpers2 = str(pers2.get())
    sigpers3 = str(pers3.get())
    sigpers4 = str(pers4.get())

    # drawing the colors to show wich figure is wich    
    pygame.draw.rect(screen, green, (0,0,w/50,h/50))
    text_greenname = font.render('sleep 1', True, white)
    screen.blit(text_greenname, (w/50,0)) 

    pygame.draw.rect(screen, yellow_dark, (0,2*h/50,w/50,h/50))
    text_yellowname = font.render('sleep 2', True, white)
    screen.blit(text_yellowname, (w/50,2*h/50)) 

    pygame.draw.rect(screen, blue, (0,4*h/50,w/50,h/50))
    text_bluename = font.render('sleep 3', True, white)
    screen.blit(text_bluename, (w/50,4*h/50)) 

    pygame.draw.rect(screen, red, (0,6*h/50,w/50,h/50))
    text_redname = font.render('sleep 4', True, white)
    screen.blit(text_redname, (w/50,6*h/50)) 

    # first person
    if int(sigpers1[1]) == 0: 
        screen.blit(greenstickman, (23*w/30, h/10))

    elif int(sigpers1[1]) == 1: 
        screen.blit(greenstickman, (15*w/30, 6*h/10))
    
    elif int(sigpers1[1]) == 2: 
        screen.blit(greenstickman, (17*w/30, 3*h/10))
    
    elif int(sigpers1[1]) == 3: 
        screen.blit(greenstickman, (27*w/30, 3*h/10))
    
    elif int(sigpers1[1]) == 4:
        screen.blit(greenstickman, (2*w/30, 4*h/10))
    


    if int(sigpers2[1]) == 0:
        screen.blit(yellowstickman, (20*w/30, h/10))
    
    elif int(sigpers2[1]) == 1:
        screen.blit(yellowstickman, (16*w/30, 6*h/10))
    
    elif int(sigpers2[1]) == 2:
        screen.blit(yellowstickman, (14*w/30, 3*h/10))
    
    elif int(sigpers2[1]) == 3:
        screen.blit(yellowstickman, (26*w/30, 3*h/10))
    
    elif int(sigpers2[1]) == 4:
        screen.blit(yellowstickman, (6*w/30, 7*h/10))
    
    
    if int(sigpers3[1]) == 0:
        screen.blit(bluestickman, (22*w/30, h/10))

    elif int(sigpers3[1]) == 1:
        screen.blit(bluestickman, (17*w/30, 6*h/10))
    
    elif int(sigpers3[1]) == 2:
        screen.blit(bluestickman, (15*w/30, 3*h/10))
    
    elif int(sigpers3[1]) == 3:
        screen.blit(bluestickman, (25*w/30, 3*h/10))
        
    elif int(sigpers3[1]) == 4:
        screen.blit(bluestickman, (11*w/30, 7*h/10))
    
    
    if int(sigpers4[1]) == 0:
        screen.blit(redstickman, (21*w/30, h/10))

    elif int(sigpers4[1]) == 1:
        screen.blit(redstickman, (18*w/30, 6*h/10))
    
    elif int(sigpers4[1]) == 2:
        screen.blit(redstickman, (16*w/30, 3*h/10))
    
    elif int(sigpers4[1]) == 3:
        screen.blit(redstickman, (28*w/30, 3*h/10))
    
    elif int(sigpers4[1]) == 4:
        screen.blit(redstickman, (21*w/30, 7*h/10))
    
    
    pygame.display.flip()


def layout_click(screen):
    w,h = screen.get_width(), screen.get_height()

    mousepos = pygame.mouse.get_pos()
    # check for mouseclick in sleep 1
    if mousepos[0] > 3*w/320 and mousepos[0] < 53*w/320 and mousepos[1] > 49*h/160 and mousepos[1] < 59*h/96:
        if pygame.mouse.get_pressed()[0]:
            return "sleep 1"
    
    # check for mouseclick in sleep 2
    elif mousepos[0] > 21*w/128 and mousepos[0] < 41*w/128 and mousepos[1] > 9*h/16 and mousepos[1] < 419*h/480:
        if pygame.mouse.get_pressed()[0]:
            return "sleep 2"
    
    # check for mouseclick in sleep 3
    elif mousepos[0] > 41*w/128 and mousepos[0] < 61*w/128 and mousepos[1] > 9*h/16 and mousepos[1] < 419*h/480:
        if pygame.mouse.get_pressed()[0]:
            return "sleep 3"

    # check for mouseclick in sleep 4
    elif mousepos[0] > 87*w/128 and mousepos[0] < 107*w/128 and mousepos[1] > 9*h/16 and mousepos[1] < 419*h/480:
        if pygame.mouse.get_pressed()[0]:
            return "sleep 4"
    
    # check for mouseclick in sleep 5
    elif mousepos[0] > 107*w/128 and mousepos[0] < 127*w/128 and mousepos[1] > 9*h/16 and mousepos[1] < 419*h/480:
        if pygame.mouse.get_pressed()[0]:
            return "sleep 5"

    # check for bathroom
    elif mousepos[0] > 107*w/128 and mousepos[0] < 127*w/128 and mousepos[1] > 13*h/60 and mousepos[1] < 19*h/48:
        if pygame.mouse.get_pressed()[0]:
            return "bathroom"
    
    # checking for kitchen
    elif mousepos[0] > 57*w/128 and mousepos[0] < 87*w/128 and mousepos[1] > 11*h/48 and mousepos[1] < 19*h/48:
        if pygame.mouse.get_pressed()[0]:
            return "kitchen"
    
    # checking for living room
    elif mousepos[0] > 21*w/128 and mousepos[0] < 127*w/128 and mousepos[1] > 11*h/48 and mousepos[1] < 5*h/6:
        if pygame.mouse.get_pressed()[0]:
            return "living"
    
    # checking for signals button
    elif mousepos[0] > 0 and mousepos[0] < w/8 and mousepos[1] > 7*h/8 and mousepos[1] < h:
        if pygame.mouse.get_pressed()[0]:
            return "signals"


def menu(screen, s_temp, r_temp = "0", room = 0):
    font = pygame.font.Font('freesansbold.ttf', 15)
    w,h = screen.get_width(), screen.get_height()

    # blacking out the background
    # then giving the menu a red outline
    pygame.draw.rect(screen, black, (w/3,h/5,w/3,8*h/15))                                            # the background
    pygame.draw.rect(screen, red, (w/3,h/5,w/3,8*h/15),1)                                            # the outline


    # button 1 (prefered stove temp, if in kitchen)
    pygame.draw.rect(screen, white, (131*w/384,101*h/480,61*w/192,7*h/60))
    text_temperature = font.render('Room temperature', True, black)
    screen.blit(text_temperature, (131*w/384,101*h/480))

    text_r_temp = font.render(r_temp, True, black)                                                      # the current selected temp
    screen.blit(text_r_temp, (131*w/384,121*h/480))
    

    # button 2  (room booking)
    pygame.draw.rect(screen, white, (131*w/384,163*h/480,61*w/192,7*h/60))
    text_fulllight = font.render('Book room', True, black)
    screen.blit(text_fulllight, (131*w/384,163*h/480))


    # button 3 (cancell all bookings)
    pygame.draw.rect(screen, white, (131*w/384,15*h/32,61*w/192,7*h/60))
    text_cancel = font.render('Cancel all', True, black)
    screen.blit(text_cancel, (131*w/384,15*h/32))


    # button 4 (prefered stove temp, if in kitchen)
    pygame.draw.rect(screen, white, (131*w/384,287*h/480,61*w/192,7*h/60))
    if room == 1:
        text_temperature = font.render('Guests', True, black)
    else:
        text_temperature = font.render('Stove Temperature', True, black)
    screen.blit(text_temperature, (131*w/384,287*h/480))

    text_s_temp = font.render(s_temp, True, black)                                                      # the current selected temp
    screen.blit(text_s_temp, (131*w/384,19*h/30))


    pygame.display.flip()


def menu_clicking(screen):
    w,h = screen.get_width(), screen.get_height()
    
    mousepos = pygame.mouse.get_pos()
    # checking for button press on the room temp button
    if mousepos[0] > 131*w/384 and mousepos[0] < 253*w/384 and mousepos[1] > 101*h/480 and mousepos[1] < 157*h/480:
        if pygame.mouse.get_pressed()[0]:
            return "room temp"
    
    # checking for button press on the booking button
    elif mousepos[0] > 131*w/384 and mousepos[0] < 253*w/384 and mousepos[1] > 163*h/480 and mousepos[1] < 73*h/160:
        if pygame.mouse.get_pressed()[0]:
            return "booking"

    # checking for button press on the cancel all bookings button
    elif mousepos[0] >131*w/384 and mousepos[0] < 253*w/384 and mousepos[1] > 15*h/32 and mousepos[1] < 281*h/480:
        if pygame.mouse.get_pressed()[0]:
            return "cancel"
    
    # checking for button press on the stove temperatuer button
    elif mousepos[0] > 131*w/384 and mousepos[0] < 253*w/384 and mousepos[1] > 287*h/480 and mousepos[1] < 343*h/480:
        if pygame.mouse.get_pressed()[0]:
            return "stove temp"


def booking(screen, month_select = None):
    w,h = screen.get_width(), screen.get_height()
    font = pygame.font.Font('freesansbold.ttf', 20)

    # blacking out the screen
    screen.fill(black)

    day_height = 43*h/240                           # the height between each layer of dates
    day_width = w/7                                 # the width between each layer of dates


    # finding the current date
    current_date = dt.datetime.now()                # the current time
    current_date = current_date.strftime("%d,%B")   # showing only the day and month
    current_date = current_date.split(",",)         # splitting the output into a list


    # telling the current/selected month
    if month_select == None:                                    # if there is no given month to show, use the current month
        d_index = months.index(current_date[1])                 # the index of the month in the lists of months
        text_month = font.render(current_date[1], True, white)  # making the menu tell the current month
    else:
        d_index = months.index(month_select)
        text_month = font.render(month_select, True, white)     # making the menu tell the selected month

    screen.blit(text_month, (0,0))                              # making the month apear in the corner


    left_days = days[d_index] - (7*4)               # the days not covered in the matrix

    # The date icons
    for i in range(4):                              # the rows in the matrix
        for j in range(7):                          # the coloumns of the matrix
            date = str(i*7+1+j)                     # the date of the day currently being made
            if int(date) == int(current_date[0]) and month_select == current_date[1]:     # highlighting todays date
                pygame.draw.rect(screen, light_blue, (day_width*j, day_height*i+50, day_width-5, day_height-5))
        
            else:
                pygame.draw.rect(screen, white, (day_width*j, day_height*i+50, day_width-5, day_height-5))

            text_date = font.render(date, True, black)          # making the menu tell the according date
            screen.blit(text_date, (day_width*j, day_height*i+50))

    for i in range(left_days):                                  # the last days not covered in the matrix
        date = str(days[d_index]-left_days+i+1)                 # the dates of the days not covered
        if date == current_date[0] and month_select == current_date[1]:         # highlighting todays date
            pygame.draw.rect(screen, light_blue, (day_width*i, day_height*4+50, day_width-5, day_height-5))
        
        else:
            pygame.draw.rect(screen, white, (day_width*i, day_height*4+50, day_width-5, day_height-5))

        text_date = font.render(date, True, black)              # making the menu tell the according date
        screen.blit(text_date, (day_width*i, day_height*4+50))
        
    
    # the icons for changing month   
    pygame.draw.rect(screen, white, (27*w/64, h/96, w/16, 40))    # button for going back a month 
    text_back = font.render("<", True, black)              
    screen.blit(text_back, (27*w/64, h/96))
    
    pygame.draw.rect(screen, white, (33*w/64, h/96, w/16, 40))    # button for going forward a month
    text_back = font.render(">", True, black)              
    screen.blit(text_back, (9*w/16, h/96))



    pygame.display.flip()


def booking_click(screen, days_month):
    w,h = screen.get_width(), screen.get_height()
    
    day_height = 43*h/240                           # the height between each layer of dates
    day_width = w/7                                 # the width between each layer of dates

    mousepos = pygame.mouse.get_pos()

    # checking for clicks on the back or forward buttons
    if mousepos[0] > 27*w/64 and mousepos[0] < 31*w/64 and mousepos[1] > h/96 and mousepos[1] < 3*h/32:
        if pygame.mouse.get_pressed()[0]:
            return "back"

    elif mousepos[0] > 33*w/64 and mousepos[0] < 37*w/64 and mousepos[1] > h/96 and mousepos[1] < 3*h/32:
        if pygame.mouse.get_pressed()[0]:
            return "forward"
    
    # checking for clicks on any of the dates
    else:
        for i in range(4):
            for j in range(7):
                if mousepos[0] > day_width*j and mousepos[0] < day_width*j+day_width-5 and mousepos[1] > day_height*i+50 and mousepos[1] < day_height*i+45+day_height:
                    if pygame.mouse.get_pressed()[0]:
                        return i*7+1+j
        
        for i in range(int(days_month)-7*4):
            if mousepos[0] > day_width*i and mousepos[0] < day_width*i+day_width-5 and mousepos[1] > day_height*4+50 and mousepos[1] < day_height*4+50+day_height-5:
                if pygame.mouse.get_pressed()[0]:
                    return 7*4+i+1


def time_book(screen):
    # !!!!!!! heavy inspiration taken from https://stackoverflow.com/questions/46252905/on-screen-typing-in-pygame/46253506
    # !!!!!!! by user wizofe
    w,h = screen.get_width(), screen.get_height()
    font = pygame.font.Font('freesansbold.ttf', 30)

    time = ""
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.unicode.isalpha():           # making the function not take any alphabetic characters
                    None

                elif evt.unicode:
                    time += evt.unicode

                elif evt.key == pygame.K_BACKSPACE:
                    if len(time) == 3:
                        time = time[:-2]            # removes first . 
                    
                    elif len(time) == 6:
                        time = time[:-2]            # removes - 

                    elif len(time) == 9:
                        time = time[:-2]            # removes last .
                    
                    elif time == "booking lasting too long":
                        time = ""
                    
                    else:
                        time = time[:-1]

                elif evt.key == pygame.K_RETURN:    # if keypress is enter then save the starttime and the time booked for, in minutes
                    time = time[:2] + time[3:5] + str((int(time[6:8])-int(time[:2]))*60+(int(time[9:11])-int(time[3:5])))
                     
                    
                    if len(time) > 6:
                        print("LONG")
                        time = "booking lasting too long"
                        

                    else:
                        
                        if len(time) < 6:
                            for _ in range(6-len(time)):
                                time = time[:4] + "0" + time[4:]    # making sure there are enough zeroes between the
                        
                        
                        return time                                 # start time and the minutes

            elif evt.type == pygame.QUIT:                           # cancel by x-ing out
                return

            if len(time) == 2:
                time += "."
            
            elif len(time) == 5:
                time += "-"

            elif len(time) == 8:
                time += "."

        # blacking out the screen
        screen.fill(black)

        correct = font.render("please write in fomrat xx.xx-xx.xx", True, white)         # text to render
        
        block = font.render(time, True, red)        # text to render
        rect = block.get_rect()                     # center of the text
        rect.center = screen.get_rect().center      # center of the screen
        screen.blit(block, rect)                    # render input text 
        screen.blit(correct, (w/10, 0))             # render correct text
        pygame.display.flip()


def temp_menu(screen, max_temp):
    w,h = screen.get_width(), screen.get_height()
    font = pygame.font.Font('freesansbold.ttf', 30)

    temp = ""
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.unicode.isalpha():           # making the function not take any alphabetic characters
                    None

                elif evt.unicode:
                    temp = temp[:len(temp)-1:]
                    temp += evt.unicode 
                    temp += "°"

                    

                elif evt.key == pygame.K_BACKSPACE:
                    if temp == "temp to high":
                        temp = ""
                    
                    else:
                        temp = temp[:-2]
                        temp += "°"

                elif evt.key == pygame.K_RETURN:    # if keypress is enter then save the starttime and the time booked for, in minutes
                    if len(temp) > max_temp:
                        print("LONG")
                        temp = "temp to high"
                        
                    else:
                        if len(temp) < max_temp:
                            for _ in range(max_temp-len(temp)):
                                temp = "0" + temp    # making sure there are enough zeroes between the
                        return temp                                 # start time and the minutes

            elif evt.type == pygame.QUIT:           # cancel by x-ing out
                return

            

        # blacking out the screen
        screen.fill(black)

        correct = font.render("please write the desired number", True, white)         # text to render
        
        block = font.render(temp, True, red)        # text to render
        rect = block.get_rect()                     # center of the text
        rect.center = screen.get_rect().center      # center of the screen
        screen.blit(block, rect)                    # render input text 
        screen.blit(correct, (w/10, 0))             # render correct text
        pygame.display.flip()


def guests(screen, guests):
    w,h = screen.get_width(), screen.get_height()
    font = pygame.font.Font('freesansbold.ttf', 30)

    guests = ""
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.unicode.isalpha():               # making the function not take any alphabetic characters
                    None

                elif evt.unicode:
                    #guests = guests[:len(guests)-1:]
                    guests += evt.unicode 
                    #guests += "°"

                    
                
                elif evt.key == pygame.K_BACKSPACE:
                    guests = guests[:-1]                    

                elif evt.key == pygame.K_RETURN:        # if keypress is enter then save the starttime and the time booked for, in minutes
                        if len(guests) < 3:
                            for _ in range(3-len(guests)):
                                guests = "0" + guests   # making sure there are enough zeroes between the
                        return guests                   # start time and the minutes
                        

        # blacking out the screen
        screen.fill(black)

        correct = font.render("please the temp in xxx", True, white)         # text to render
        
        block = font.render(guests, True, red)        # text to render
        rect = block.get_rect()                     # center of the text
        rect.center = screen.get_rect().center      # center of the screen
        screen.blit(block, rect)                    # render input text 
        screen.blit(correct, (w/10, 0))             # render correct text
        pygame.display.flip()


def reqans(screen, message, fromw = "book", sign = None):
    font = pygame.font.Font('freesansbold.ttf', 35)
    w,h = screen.get_width(), screen.get_height()

    block = font.render("idk yet", True, white)                     # text to render
    print(message)
    if message == 3:
        if fromw == "book":
            block = font.render("Successfully booked", True, white)     # text to render

        elif fromw == "cancelling":
            block = font.render("Successfully cancelled", True, white)     # text to render
    
    elif message == 4:
        block = font.render("Busy time", True, red)                 # text to render
        if sign != None:
            next_a = font.render("next available time:", True, red)                 # text to render (next available time)
            next_b = font.render(f"{str(sign)[5:7]}.{str(sign)[7:9]}", True, red)   # text to render (next available time)
            screen.blit(next_a, (0,3*h/5))                                                # render next available time
            screen.blit(next_b, (0,4*h/5))                                                # render next available time

    elif message == 5:
        block = font.render("Unknown error", True, red)             # text to render
    
    elif message == 6:
        block = font.render("Successfully canceled", True, white)             # text to render
    
    else:
        block = font.render("ERROR OCOURED", True, red)             # text to render

    pygame.draw.rect(screen, black, (w/32,2.5*(h/6),9*w/10,h/6))
    pygame.draw.rect(screen, red, (w/32,2.5*(h/6),9*w/10,h/6),1)

    rect = block.get_rect()                                         # center of the text
    rect.center = screen.get_rect().center                          # center of the screen
    screen.blit(block, rect)                                        # render input text 

    pygame.display.flip()

    pygame.time.wait(4000)


def signalscreen(screen):
    w,h = screen.get_width(), screen.get_height()
    screen.fill(black)
    font = pygame.font.Font('freesansbold.ttf', 15)

    book = str(booking_signal.get())
    pers = str(personal_signal.get())

    text_date = font.render(f"bookingdate: {book[1:3]}.{book[3:5]}", True, white)
    screen.blit(text_date, (0,0)) 
    
    text_time = font.render(f"bookingtime: {book[5:7]}:{book[7:9]} for {book[9:11]} minutes", True, white)
    screen.blit(text_time, (0,h/10)) 

    text_room = font.render(f"bookingroom: {book[11]}", True, white)
    screen.blit(text_room, (0,2*h/10)) 

    text_temp = font.render(f"stove temperature/guests (if room is over 3): {book[12:15]}", True, white)
    screen.blit(text_temp, (0,3*h/10)) 

    text_status = font.render(f"Status of the signal: {book[15]}", True, white)
    screen.blit(text_status, (0,4*h/10)) 

    text_persroom = font.render(f"The room of the signal owner: {pers[1]}", True, white)
    screen.blit(text_persroom, (0,5*h/10)) 

    text_perstemp = font.render(f"The prefered temp of the user: {pers[2:4]}", True, white)
    screen.blit(text_perstemp, (0,6*h/10)) 

    text_persguests = font.render(f"The current amount of guests: {pers[4]}", True, white)
    screen.blit(text_persguests, (0,7*h/10)) 



    pygame.display.flip()

    for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                return "quit"




def main():
    
    # starting pygame 
    pygame.init()
    stove_temp = "000°"
    room_temp = str(personal_signal.get())[2:4] + "°"
    currentguests = "0"
    
    # set screensize
    screen = pygame.display.set_mode((1550,900))
    pygame.display.set_caption("Konsoll")     # making window say "kontrollpanel"
    
    main_layout(screen)                                     # showing the main screen
    
    running = True 

    while running:
        try:
            # getting the current date
            current_date = dt.datetime.now()                        # the current time
            current_date = current_date.strftime("%d,%B")           # showing only the day and month
            current_date = current_date.split(",")                  # splitting the output into a list
            month_select = months[months.index(current_date[1])]    # the index of the month in the lists and the according month
            

            # getting the mouse output from the main screen
            Mouse_in = layout_click(screen)
            if Mouse_in != None:
                print(Mouse_in)
                

            # variable to give the user some time before the next click registers
            first = 1


            # mouseclick found on signals button
            while Mouse_in == "signals":
                if signalscreen(screen) == "quit":
                    Mouse_in = None
                    main_layout(screen)


            # mouseclick found in users personal room
            while Mouse_in == "sleep " + str(user_id):
                menu_click = menu_clicking(screen)              # click checking in the menu
                if menu_click != None:
                    if first == 1:                              # if first run, make a delay
                        first = 0
                        menu_click = None
                        menu(screen, currentguests, room_temp, 1)                            # showing the menu screen
                        pygame.time.wait(400)
        

                    print(menu_click)

                # cancel all orders
                while menu_click == "cancel":
                    signal_value = int(str(user_id) + "042820000140002")
                    print(signal_value)
                    booking_signal.write(signal_value)

                    success = booking_signal.get()                          # checking the signal in CoT
                    while success != signal_value:                          # checking if the signal at CoT is the one sent
                        success = booking_signal.get()
                        print(success)
                        
                    
                    for i in range(20000):                                  # checking for 20 sek if the signal at CoT has been processed
                        pygame.time.wait(1)
                        success = int(booking_signal.get())
                        print(i, success)
                        if str(success)[len(str(success))-1] != "2":        # checking if signal has been changed
                            print("SUCCESSSS")
                            break
                    
                    reqans(screen, int(str(success)[len(str(success))-1]), "cancelling")  # sending the recieved signal to the function 
                                                                            # giving output to the user
                    menu_click = None
                    main_layout(screen)
                    menu(screen, currentguests, room_temp, 1)

                
                if menu_click == "stove temp":
                    currentguests = guests(screen, currentguests)
                    main_layout(screen)
                    menu(screen, currentguests, room_temp, 1)
                    print(currentguests)
                
                if menu_click == "room temp":
                    room_temp = str(temp_menu(screen, 3))                       # asking for new room temp value
                    main_layout(screen) 
                    menu(screen, currentguests, room_temp, 1)
                    currentsig = str(personal_signal.get())                             # checking the signal in CoT
                    signal_value = currentsig[:2] + room_temp[:2] + currentsig[4]       # making the new signal 
                    personal_signal.write(signal_value)                                 # writing the new signal
                    
                    


                # click found on the booking button
                while menu_click == "booking":
                    booking(screen, month_select)                   # showing the booking menu
                    bookklikk = booking_click(screen, days[months.index(month_select)])

                    # a skip of the first run to not taking an output immediatly
                    if first == 0:
                        pygame.time.wait(200)
                        first = 1
                    
                    else:
                        if bookklikk == "back":
                            month_select = months[months.index(month_select)-1]         # selecting the previous month 
                            pygame.time.wait(200)                                       # pausing a bit to prevent skipping alot
                            print(month_select)
                        
                        elif bookklikk == "forward":
                            if month_select == months[11]:
                                month_select = months[0]
                            else:
                                month_select = months[months.index(month_select)+1]     # selecting the next month
                            pygame.time.wait(200)                                       # pausing a bit to prevent skipping alot
                            print(month_select)
                        
                        elif bookklikk != None:
                            print(bookklikk)
                            pygame.time.wait(200)

                        while type(bookklikk) is int:                                   # if there was a keypress on a date
                            bookingsignallist = ["4",          
                                str(bookklikk).zfill(2), str(months.index(current_date[1])+1).zfill(2),        # making a list of things to put in the signal
                                str(time_book(screen))]
                            print(bookingsignallist)
                            print(bookingsignallist[3])
                            if bookingsignallist[3] == "None":                          # if the menu is X-ed out, it will return None
                                bookklikk = str(bookklikk)
                            
                            else:
                                    # the signal put in correct order 
                                signal_value = int(str(user_id) + str(bookingsignallist[2]) + bookingsignallist[1] + str(bookingsignallist[3]) + str(bookingsignallist[0]) + currentguests.zfill(3) + "1")

                                booking_signal.write(signal_value)                      # sending signal to CoT
                                print(signal_value)
                                pygame.time.wait(50)
                                
                                success = booking_signal.get()                          # checking the signal in CoT
                                while success != signal_value:                          # checking if the signal at CoT is the one sent
                                    success = booking_signal.get()
                                    
                                
                                for i in range(20000):                                  # checking for 20 sek if the signal at CoT has been processed
                                    pygame.time.wait(1)
                                    success = int(booking_signal.get())
                                    print(i, success)
                                    if str(success)[len(str(success))-1] != "1":        # checking if signal has been changed
                                        bookklikk = str(bookklikk)
                                        break
                                
                                reqans(screen, int(str(success)[len(str(success))-1]))  # sending the recieved signal to the function 
                                                                                        # giving output to the user
                                
                                

                            
                            


                    for event in pygame.event.get():
                    # only do something if the event is of type QUIT
                        if event.type == pygame.QUIT:
                            menu_click = None
                            main_layout(screen)
                            menu(screen, currentguests, room_temp, 1)
                        
                        
                    

                
                for event in pygame.event.get():
                    # only do something if the event is of type QUIT
                    if event.type == pygame.QUIT:
                        Mouse_in = None
                        main_layout(screen)


            # mouseclick found in livingroom
            while Mouse_in == "living":
                
                menu_click = menu_clicking(screen)              # click checking in the menu
                if menu_click != None:
                    if first == 1:                              # if first run, make a delay
                        first = 0
                        menu_click = None
                        menu(screen, stove_temp, room_temp)                            # showing the menu screen
                        pygame.time.wait(400)

                    print(menu_click)

                # cancel all orders
                while menu_click == "cancel":
                    signal_value = int(str(user_id) + "042820000110002")
                    print(signal_value)
                    booking_signal.write(signal_value)

                    success = booking_signal.get()                          # checking the signal in CoT
                    while success != signal_value:                          # checking if the signal at CoT is the one sent
                        success = booking_signal.get()
                        print(success)
                    
                    for i in range(20000):                                  # checking for 20 sek if the signal at CoT has been processed
                        pygame.time.wait(1)
                        success = int(booking_signal.get())
                        print(i, success)
                        if str(success)[len(str(success))-1] != "2":        # checking if signal has been changed
                            break
                    
                    reqans(screen, int(str(success)[len(str(success))-1]), "cancelling")  # sending the recieved signal to the function 
                                                                            # giving output to the user
                    menu_click = None
                    main_layout(screen)
                    menu(screen, stove_temp, room_temp)

                
                if menu_click == "stove temp":
                    stove_temp = temp_menu(screen, 4)
                    main_layout(screen)
                    menu(screen, stove_temp, room_temp)
                    print(stove_temp)
                
                if menu_click == "room temp":
                    room_temp = str(temp_menu(screen, 3))                       # asking for new room temp value
                    main_layout(screen) 
                    menu(screen, currentguests, room_temp)
                    currentsig = str(personal_signal.get())                             # checking the signal in CoT
                    signal_value = currentsig[:2] + room_temp[:2] + currentsig[4]       # making the new signal 
                    personal_signal.write(signal_value)                                 # writing the new signal


                # click found on the booking button
                while menu_click == "booking":
                    booking(screen, month_select)                   # showing the booking menu
                    bookklikk = booking_click(screen, days[months.index(month_select)])

                    # a skip of the first run to not taking an output immediatly
                    if first == 0:
                        #print("RAN")
                        pygame.time.wait(400)
                        first = 1
                    
                    else:
                        if bookklikk == "back":
                            month_select = months[months.index(month_select)-1]         # selecting the previous month 
                            pygame.time.wait(200)                                       # pausing a bit to prevent skipping alot
                            print(month_select)
                        
                        elif bookklikk == "forward":
                            if month_select == months[11]:
                                month_select = months[0]
                            else:
                                month_select = months[months.index(month_select)+1]     # selecting the next month
                            pygame.time.wait(200)                                       # pausing a bit to prevent skipping alot
                            print(month_select)
                        
                        elif bookklikk != None:
                            print(bookklikk)
                            pygame.time.wait(200)

                        while type(bookklikk) is int:                                   # if there was a keypress on a date
                            bookingsignallist = [str(rooms.index(Mouse_in)+1),          
                                str(bookklikk).zfill(2), str(months.index(current_date[1])+1).zfill(2),        # making a list of things to put in the signal
                                str(time_book(screen))]
                            print(bookingsignallist)
                            print(bookingsignallist[3])
                            if bookingsignallist[3] == "None":                          # if the menu is X-ed out, it will return None
                                bookklikk = str(bookklikk)
                            
                            else:
                                    # the signal put in correct order 
                                signal_value = int(str(user_id) + str(bookingsignallist[2]) + bookingsignallist[1] + str(bookingsignallist[3]) + str(bookingsignallist[0]) + stove_temp[:len(stove_temp)-1] + "1")

                                booking_signal.write(signal_value)                      # sending signal to CoT
                                print(signal_value)
                                pygame.time.wait(50)
                                
                                success = booking_signal.get()                          # checking the signal in CoT
                                '''
                                while success != signal_value:                          # checking if the signal at CoT is the one sent
                                    success = booking_signal.get()
                                    print("runn")
                                '''
                                for i in range(20000):                                  # checking for 20 sek if the signal at CoT has been processed
                                    pygame.time.wait(1)
                                    success = int(booking_signal.get())
                                    print(i, success)
                                    if str(success)[len(str(success))-1] != "1":        # checking if signal has been changed
                                        bookklikk = str(bookklikk)
                                        break
                                
                                reqans(screen, int(str(success)[len(str(success))-1]), "book", success)     # sending the recieved signal to the function 
                                                                                                            # giving output to the user
                                
                                

                            
                            


                    for event in pygame.event.get():
                    # only do something if the event is of type QUIT
                        if event.type == pygame.QUIT:
                            menu_click = None
                            main_layout(screen)
                            menu(screen, stove_temp, room_temp)
                        
                        
                    

                
                for event in pygame.event.get():
                    # only do something if the event is of type QUIT
                    if event.type == pygame.QUIT:
                        Mouse_in = None
                        main_layout(screen)
            

            # mouseclick found in bathroom
            while Mouse_in == "bathroom":
                
                menu_click = menu_clicking(screen)              # click checking in the menu
                if menu_click != None:
                    if first == 1:                              # if first run, make a delay
                        first = 0
                        menu_click = None
                        menu(screen, stove_temp, room_temp)                            # showing the menu screen
                        pygame.time.wait(400)

                    print(menu_click)

                # cancel all orders
                while menu_click == "cancel":
                    signal_value = int(str(user_id) + "042820000130002")
                    print(signal_value)
                    booking_signal.write(signal_value)

                    success = booking_signal.get()                          # checking the signal in CoT
                    while success != signal_value:                          # checking if the signal at CoT is the one sent
                        success = booking_signal.get()
                        print(success)
                    
                    for i in range(20000):                                  # checking for 20 sek if the signal at CoT has been processed
                        pygame.time.wait(1)
                        success = int(booking_signal.get())
                        print(i, success)
                        if str(success)[len(str(success))-1] != "2":        # checking if signal has been changed
                            break
                    
                    reqans(screen, int(str(success)[len(str(success))-1]), "cancelling")  # sending the recieved signal to the function 
                                                                            # giving output to the user
                    menu_click = None
                    main_layout(screen)
                    menu(screen, stove_temp, room_temp)

                
                if menu_click == "stove temp":
                    stove_temp = temp_menu(screen, 4)
                    main_layout(screen)
                    menu(screen, stove_temp, room_temp)
                    print(stove_temp)
                
                if menu_click == "room temp":
                    room_temp = str(temp_menu(screen, 3))                       # asking for new room temp value
                    main_layout(screen) 
                    menu(screen, currentguests, room_temp)
                    currentsig = str(personal_signal.get())                             # checking the signal in CoT
                    signal_value = currentsig[:2] + room_temp[:2] + currentsig[4]       # making the new signal 
                    personal_signal.write(signal_value)                                 # writing the new signal


                # click found on the booking button
                while menu_click == "booking":
                    booking(screen, month_select)                   # showing the booking menu
                    bookklikk = booking_click(screen, days[months.index(month_select)])

                    # a skip of the first run to not taking an output immediatly
                    if first == 0:
                        pygame.time.wait(400)
                        first = 1
                    
                    else:
                        if bookklikk == "back":
                            month_select = months[months.index(month_select)-1]         # selecting the previous month 
                            pygame.time.wait(200)                                       # pausing a bit to prevent skipping alot
                            print(month_select)
                        
                        elif bookklikk == "forward":
                            if month_select == months[11]:
                                month_select = months[0]
                            else:
                                month_select = months[months.index(month_select)+1]     # selecting the next month
                            pygame.time.wait(200)                                       # pausing a bit to prevent skipping alot
                            print(month_select)
                        
                        elif bookklikk != None:
                            print(bookklikk)
                            pygame.time.wait(200)

                        while type(bookklikk) is int:                                   # if there was a keypress on a date
                            bookingsignallist = [str(rooms.index(Mouse_in)+1),          
                                str(bookklikk).zfill(2), str(months.index(current_date[1])+1).zfill(2),        # making a list of things to put in the signal
                                str(time_book(screen))]
                            print(bookingsignallist)
                            print(bookingsignallist[3])
                            if bookingsignallist[3] == "None":                          # if the menu is X-ed out, it will return None
                                bookklikk = str(bookklikk)
                            
                            else:
                                    # the signal put in correct order 
                                signal_value = int(str(user_id) + str(bookingsignallist[2]) + bookingsignallist[1] + str(bookingsignallist[3]) + str(bookingsignallist[0]) + stove_temp[:len(stove_temp)-1] + "1")

                                booking_signal.write(signal_value)                      # sending signal to CoT
                                print(signal_value)
                                pygame.time.wait(50)
                                
                                success = booking_signal.get()                          # checking the signal in CoT
                                while success != signal_value:                          # checking if the signal at CoT is the one sent
                                    success = booking_signal.get()
                                
                                for i in range(20000):                                  # checking for 20 sek if the signal at CoT has been processed
                                    pygame.time.wait(1)
                                    success = int(booking_signal.get())
                                    print(i, success)
                                    if str(success)[len(str(success))-1] != "1":        # checking if signal has been changed
                                        bookklikk = str(bookklikk)
                                        break
                                
                                reqans(screen, int(str(success)[len(str(success))-1]), "book", success)  # sending the recieved signal to the function 
                                                                                        # giving output to the user
                                
                                

                            
                            


                    for event in pygame.event.get():
                    # only do something if the event is of type QUIT
                        if event.type == pygame.QUIT:
                            menu_click = None
                            main_layout(screen)
                            menu(screen, stove_temp, room_temp)
                        
                        
                    

                
                for event in pygame.event.get():
                    # only do something if the event is of type QUIT
                    if event.type == pygame.QUIT:
                        Mouse_in = None
                        main_layout(screen)
            

            # mouseclick found in kitchen
            while Mouse_in == "kitchen":
                
                menu_click = menu_clicking(screen)              # click checking in the menu
                if menu_click != None:
                    if first == 1:                              # if first run, make a delay
                        first = 0
                        menu_click = None
                        menu(screen, stove_temp, room_temp)                            # showing the menu screen
                        pygame.time.wait(400)

                    print(menu_click)

                # cancel all orders
                while menu_click == "cancel":
                    signal_value = int(str(user_id) + "042820000120002")
                    print(signal_value)
                    booking_signal.write(signal_value)

                    success = booking_signal.get()                          # checking the signal in CoT
                    while success != signal_value:                          # checking if the signal at CoT is the one sent
                        success = booking_signal.get()
                        print(success)
                    
                    for i in range(20000):                                  # checking for 20 sek if the signal at CoT has been processed
                        pygame.time.wait(1)
                        success = int(booking_signal.get())
                        print(i, success)
                        if str(success)[len(str(success))-1] != "2":        # checking if signal has been changed
                            break
                    
                    reqans(screen, int(str(success)[len(str(success))-1]), "cancelling")  # sending the recieved signal to the function 
                                                                            # giving output to the user
                    menu_click = None
                    main_layout(screen)
                    menu(screen, stove_temp, room_temp)

                
                if menu_click == "stove temp":
                    stove_temp = temp_menu(screen, 4)
                    main_layout(screen)
                    menu(screen, stove_temp, room_temp)
                    print(stove_temp)
                
                if menu_click == "room temp":
                    room_temp = str(temp_menu(screen, 3))                       # asking for new room temp value
                    main_layout(screen) 
                    menu(screen, currentguests, room_temp)
                    currentsig = str(personal_signal.get())                             # checking the signal in CoT
                    signal_value = currentsig[:2] + room_temp[:2] + currentsig[4]       # making the new signal 
                    personal_signal.write(signal_value)                                 # writing the new signal


                # click found on the booking button
                while menu_click == "booking":
                    booking(screen, month_select)                   # showing the booking menu
                    bookklikk = booking_click(screen, days[months.index(month_select)])

                    # a skip of the first run to not taking an output immediatly
                    if first == 0:
                        pygame.time.wait(400)
                        first = 1
                    
                    else:
                        if bookklikk == "back":
                            month_select = months[months.index(month_select)-1]         # selecting the previous month 
                            pygame.time.wait(200)                                       # pausing a bit to prevent skipping alot
                            print(month_select)
                        
                        elif bookklikk == "forward":
                            if month_select == months[11]:
                                month_select = months[0]
                            else:
                                month_select = months[months.index(month_select)+1]     # selecting the next month
                            pygame.time.wait(200)                                       # pausing a bit to prevent skipping alot
                            print(month_select)
                        
                        elif bookklikk != None:
                            print(bookklikk)
                            pygame.time.wait(200)

                        while type(bookklikk) is int:                                   # if there was a keypress on a date
                            bookingsignallist = [str(rooms.index(Mouse_in)+1),          
                                str(bookklikk).zfill(2), str(months.index(current_date[1])+1).zfill(2),        # making a list of things to put in the signal
                                str(time_book(screen))]
                            print(bookingsignallist)
                            print(bookingsignallist[3])
                            if bookingsignallist[3] == "None":                          # if the menu is X-ed out, it will return None
                                bookklikk = str(bookklikk)
                            
                            else:
                                    # the signal put in correct order 
                                signal_value = int(str(user_id) + str(bookingsignallist[2]) + bookingsignallist[1] + str(bookingsignallist[3]) + str(bookingsignallist[0]) + stove_temp[:len(stove_temp)-1] + "1")

                                booking_signal.write(signal_value)                      # sending signal to CoT
                                print(signal_value)
                                pygame.time.wait(50)
                                
                                success = booking_signal.get()                          # checking the signal in CoT
                                
                                for i in range(20000):                                  # checking for 20 sek if the signal at CoT has been processed
                                    pygame.time.wait(1)
                                    success = int(booking_signal.get())
                                    print(i, success)
                                    if str(success)[len(str(success))-1] != "1":        # checking if signal has been changed
                                        bookklikk = str(bookklikk)
                                        break
                                
                                reqans(screen, int(str(success)[len(str(success))-1]), "book", success)  # sending the recieved signal to the function 
                                                                                        # giving output to the user
                                
                                

                            
                            


                    for event in pygame.event.get():
                    # only do something if the event is of type QUIT
                        if event.type == pygame.QUIT:
                            menu_click = None
                            main_layout(screen)
                            menu(screen, stove_temp, room_temp)
                        
                        
                    

                
                for event in pygame.event.get():
                    # only do something if the event is of type QUIT
                    if event.type == pygame.QUIT:
                        Mouse_in = None
                        main_layout(screen)
            
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

        except:
            print("an error occoured\nrebooting system")
            main_layout(screen)                                     # showing the main screen



# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()