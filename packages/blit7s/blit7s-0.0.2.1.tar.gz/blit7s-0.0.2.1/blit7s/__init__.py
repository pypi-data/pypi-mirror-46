#blit7s: blit 7 segment
import pkg_resources as pkg
import os
import RPi.GPIO as GPIO
import time

def chart():
    import subprocess, sys
    cha=pkg.resource_filename("blit7s","chart.PNG")
    opener ="open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, cha])

##    except:
##        import subprocess, sys
##
##        opener ="open" if sys.platform == "darwin" else "xdg-open"
##        subprocess.call([opener, "Capture.PNG"])

        
def blitc(pin_list #list must have pins in the order: a-g, df
          ,str_character):

    GPIO.setup(pin_list,GPIO.OUT)
    fail=True
    if str_character == 1 or str_character== '1':
        GPIO.output(pin_list,[0,1,1,0,0,0,0,0])
        fail=False
        
    if str_character=='2'  or str_character== 2:
        GPIO.output(pin_list,[1,1,0,1,1,0,1,0])
        fail=False
    if str_character== '3' or str_character==3:
        GPIO.output(pin_list,[1,1,1,1,0,0,1,0])
        fail=False
    if str_character== '4' or str_character==4:
        GPIO.output(pin_list,[0,1,1,0,0,1,1,0])
        fail=False
    if str_character== '5' or str_character==5:
        GPIO.output(pin_list,[1,0,1,1,0,1,1,0])
        fail=False
    if str_character== '6' or str_character==6:
        GPIO.output(pin_list,[1,0,1,1,1,1,1,0])
        fail=False
    if str_character== '7' or str_character==7:
        GPIO.output(pin_list,[1,1,1,0,0,0,0,0])
        fail=False
    if str_character== '8' or str_character==8:
        GPIO.output(pin_list,[1,1,1,1,1,1,1,0])
        fail=False
    if str_character== '9' or str_character==9:
        GPIO.output(pin_list,[1,1,1,1,0,1,1,0])
        fail=False
    if str_character== '0' or str_character==0:
        GPIO.output(pin_list,[1,1,1,1,1,1,0,0])
        fail=False
    if str_character== 'decimal' or str_character=='period' or str_character=='.':
        GPIO.output(pin_list,[0,0,0,0,0,0,0,1])
        fail=False
    if str_character== 'a' or str_character=='A':
        GPIO.output(pin_list,[1,1,1,0,1,1,1,0])
        fail=False
    if str_character== 'b' or str_character=='B':
        GPIO.output(pin_list,[0,0,1,1,1,1,1,0])
        fail=False
    if str_character== 'c':
        GPIO.output(pin_list,[0,0,0,1,1,0,1,0])
        fail=False
    if str_character== 'C':
        GPIO.output(pin_list,[1,0,0,1,1,1,0,0])
        fail=False
    if str_character== 'd' or str_character=='D':
        GPIO.output(pin_list,[0,1,1,1,1,0,1,0])
        fail=False
    if str_character== 'E' or str_character=='e':
        GPIO.output(pin_list,[1,0,0,1,1,1,1,0])
        fail=False
    if str_character== 'F' or str_character=='f':
        GPIO.output(pin_list,[1,0,0,0,1,1,1,0])
        fail=False
    if str_character== 'G' or str_character=='g':
        GPIO.output(pin_list,[1,0,1,1,1,1,0,0])
        fail=False
    if str_character == 'h':
        GPIO.output(pin_list,[0,0,1,0,1,1,1,0])
        fail=False
    if str_character == 'H':
        GPIO.output(pin_list,[0,1,1,0,1,1,1,0])
        fail=False
    if str_character == "i" or str_character == 'I':
        GPIO.output(pin_list,[0,1,1,0,0,0,0,0])
        fail=False
    if str_character == "J" or str_character == 'j':
        GPIO.output(pin_list,[0,1,1,1,1,0,0,0])
        fail=False
    if str_character == "L" or str_character == "l":
        GPIO.output(pin_list,[0,0,0,1,1,1,0,0])
        fail=False
    if str_character == "O":
        GPIO.output(pin_list,[1,1,1,1,1,1,0,0])
        fail=False
    if str_character == "o":
        GPIO.output(pin_list,[0,0,1,1,1,0,1,0])
        fail=False
    if str_character == "P" or str_character =="p":
        GPIO.output(pin_list,[1,1,0,0,1,1,1,0])
        fail=False
    if str_character == 'r' or str_character =="R":
        GPIO.output(pin_list,[0,0,0,0,1,0,1,0])
        fail=False
    if str_character =="S" or str_character == 's':
        GPIO.output(pin_list,[1,0,1,1,0,1,1,0])
        fail=False

    if fail==True:
        GPIO.cleanup()
        error=(str_character, "is an invalid character and cannot be displayed with a 7 segment unit.")
        raise ValueError(error)

def sentence(pinlist #list must have pins in the order: a-g, dp
             ,string #string on what sentence you want to be 'blitted'
              ,pause_time #time each character will be displayed
             ):

    for x in string:
        blitc(pinlist,x)
        time.sleep(pause_time)
        GPIO.output(pinlist,[0,0,0,0,0,0,0,0])



def customchr(pin_list #list must have pins in the order: a-g, dp
              ,list_of_individual_segments #individual segments are a,b,c,d,e,f,g and dp
              ):

    if list_of_individual_segments is not type(list):
        error=(list_of_individual_segments, "is not a list. The individual segments must be in a list.")
        raise ValueError(error)

    else:
        for x in list_of_individual_segments:
            dplist=['DP','dp','Dp','dP']
            
            if x not in "aAbBcCdDEeFfGg" and x not in dplist:
                GPIO.cleanup()
                error=(x, "is an invalid individual sengment value.")
                raise ValueError(error)

            else:
                if x in "aA":
                    GPIO.output(pin_list,[1,0,0,0,0,0,0,0])

                if x in "bB":
                    GPIO.output(pin_list,[0,1,0,0,0,0,0,0])

                if x in "cC":
                    GPIO.output(pin_list,[0,0,1,0,0,0,0,0])

                if x in "dD":
                    GPIO.output(pin_list,[0,0,0,1,0,0,0,0])

                if x in "Ee":
                    GPIO.output(pin_list,[0,0,0,0,1,0,0,0])

                if x in "Ff":
                    GPIO.output(pin_list,[0,0,0,0,0,1,0,0])

                if x in "Gg":
                    GPIO.output(pin_list,[0,0,0,0,0,0,1,0])

                if x in dplist:
                    GPIO.output(pin_list,[0,0,0,0,0,0,0,1])
                    

               
    

    
