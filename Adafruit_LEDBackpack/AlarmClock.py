#!/usr/bin/python

import time
import pygame

class AlarmClock(object):
    COLOR_TRANSPARENT=0
    COLOR_GREEN=1
    COLOR_RED=2
    COLOR_YELLOW=3
    current_color=1
    bg_color=0
    alarm_time='06:30'
    org_alarm_time='06:30'
    alarm_text='ALARM!!'
    snooze_time=1
    org_snooze_time=0
    snooze_count=0
    debug=False
    flash=True
    sound='/home/pi/alarm.mp3'

    def __init__(self, debug=False):
        self.debug=debug
        self.alarm_time=self.get_time()
        #copy over originals
        self.org_alarm_time=self.alarm_time
        self.org_snooze_time=self.snooze_time
        
        pygame.mixer.init()
        pygame.mixer.music.load(self.sound)
        #Debug Set Alarm for 2 minutes from now
        if(self.debug):
            self.set_snooze()

    def set_alarm(self, time=False):
        " Set alarm time in Hours : Minutes (12:59) "
        if(time):
            self.alarm_time=time
        else:
            self.alarm_time=self.get_time()
        self.org_alarm_time=self.alarm_time

    def set_snooze_time(self, mins=10):
        " Set Snooze time, format in minutes "
        self.snooze_time=mins
        self.org_snooze_time=self.snooze_time

    def set_snooze(self):
        " Set snooze "
        if(self.debug):
            print("Setting snooze")
        ++self.snooze_count
        # Increment Alarm Time
        hrs = int(time.strftime('%I'))
        mins = int(time.strftime('%M')) + self.snooze_time
        if(mins > 59):
            r = mins % 60
            hrs += (mins - r) / 60
            mins = r
            if(hrs > 12):
                hrs = hrs - 12
        if(hrs < 10):
            hrs = "0" + str(hrs)
        if(mins < 10):
            mins = "0" + str(mins)
        #Set alarm time
        self.alarm_time="%s:%s"%(hrs, mins)
        if(self.debug):
            print("New Alarm Time %s" % self.alarm_time)
        if(self.snooze_time > 3):
            --self.snooze_time
        #Stop Sound
        self.tigger_sound(False)

    def stop_alarm(self):
        " Stop Alarm and reset object "
        if(self.debug):
            print("Stopping alarm")
        self.snooze_count=0
        self.alarm_time=self.org_alarm_time
        self.snooze_time=self.org_snooze_time
        self.tigger_sound(False)
    
    def tigger_sound(self, on):
        " Trigger Sound "
        if(on):
            if(pygame.mixer.music.get_busy()):
                return
            if(self.debug):
                print("Playing sound")
            # Play sound up to 25 times
            pygame.mixer.music.play(25)
        else:
            if(self.debug):
                print("Pausing sound")
            # Pause sound
            pygame.mixer.music.pause()

    def get_time(self):
        " Get Time "
        return time.strftime("%I:%M")
    
    def get_dsp_time(self):
        " GetDisplay Time "
        return time.strftime("%I:%M%p")[:-1]

    def is_am(self):
        " Returns true if it is AM "
        return time.strftime("%p") == 'AM'

    def check_alarm(self):
        " Check to see if the alarm should be triggered "
        return self.get_time() == self.alarm_time

    def display_msg(self):
        " Get the Current Display MSG"
        self.set_colors()
        if(self.check_alarm()):
            self.tigger_sound(True)
            return self.alarm_text
        else:
            return self.get_dsp_time()

    def set_colors(self):
        " Get the Current Colors "
        #Set the default BG to transparent
        self.bg_color=self.COLOR_TRANSPARENT
        if(self.is_am()):
            self.current_color=self.COLOR_GREEN
        else:
            self.current_color=self.COLOR_YELLOW
        #Check if alarm triggered
        if(self.check_alarm()):
            if(self.flash):
                self.current_color=self.COLOR_TRANSPARENT
                self.bg_color=self.COLOR_RED
                self.flash=False
            else:
                self.current_color=self.COLOR_RED
                self.bg_color=self.COLOR_TRANSPARENT
                self.flash=True

    def get_color(self):
        " Get the Current Color "
        return self.current_color

    def get_bg(self):
        " Get the Current BG "
        return self.bg_color
