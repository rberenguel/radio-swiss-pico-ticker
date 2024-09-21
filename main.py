import gc
import network
import random
import time
import urequests


from picographics import PicoGraphics, DISPLAY_UNICORN_PACK, PEN_P8
from picounicorn import PicoUnicorn
from ssids import ssids



class SwissJazzTicker:
    def __init__(self):
        self.debug = False
        self.active = True
        self._value = 30
        self._sleep = 7
        self.hue()
        self.startup()
        self.set_color()
        self.t = self.unicorn.get_width()
        self.BLACK = self.graphics.create_pen_hsv(0.0, 0.0, 0.0)
        self.graphics.set_font("bitmap8")
        self.playing_now = self.current_song()
        self.wrap = -self.graphics.measure_text(self.playing_now, scale=0)
        self.cycles = 0
        self.showing = 1

    def startup(self):
        """Starts all the hardware and connects to the relevant network"""
        self.graphics = PicoGraphics(DISPLAY_UNICORN_PACK, pen_type=PEN_P8)
        self.unicorn = PicoUnicorn()
        # Starting up wifi
        self.unicorn.set_pixel(0, 0, 50, 0, 0)
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        self.unicorn.set_pixel(0, 1, 50, 50, 0)
        # Just in case the WiFi needs to warm up or something
        time.sleep(1)
        scanned = wlan.scan()
        ssids_here = list(map(lambda x: x[0].decode(), scanned))

        connected = False
        for ssid in ssids.keys():
            if ssid in ssids_here:
                wlan.connect(ssid, ssids[ssid])
                connected = True
                print(f"Connected to {ssid}")
                self.unicorn.set_pixel(0, 2, 0, 50, 0)
        if not connected:
            # Show an error message on screen
            current_song = lambda: f"No known network found: {ssids_here}"
            self.hue = lambda x: 0.5
     
    def loop(self):
        """Eval loop that keeps showing the text and offers some controls"""
        while True:
            if self.unicorn.is_pressed(self.unicorn.BUTTON_X):
                self.active = not self.active
                self.graphics.set_pen(self.BLACK)
                self.graphics.clear()
                self.unicorn.update(self.graphics)
                if self.active:
                    self.unicorn.set_pixel(0, 0, 30, 30, 30)
                    # TODO all this initialization is done in like 3 places now
                    self.playing_now = self.current_song()
                    self.wrap = -self.graphics.measure_text(self.playing_now, scale=0)
                    self.t = self.unicorn.get_width()
                    self.showing = 1
                    self.cycles = 0
                time.sleep(0.3) # debounce
            if self.active:
                self.unicorn.set_pixel(0, 0, 30, 30, 30)
                if self.unicorn.is_pressed(self.unicorn.BUTTON_A):
                    # TODO all this initialization is done in like 3 places now
                    self.playing_now = self.current_song()
                    self.wrap = -self.graphics.measure_text(self.playing_now, scale=0)
                    self.t = self.unicorn.get_width()
                    self.showing = 1
                    self.cycles = 0
                if self.unicorn.is_pressed(self.unicorn.BUTTON_B):
                    self.value_up()
                    self.set_color()
                if self.unicorn.is_pressed(self.unicorn.BUTTON_Y):
                    self.sleep()
                self.cycles +=1
                if self.showing == 1:
                    self.graphics.set_pen(self.BLACK)
                    self.graphics.clear()
                    self.graphics.set_pen(self.color)
                    self.graphics.text(self.playing_now, self.t, 0, scale=1)
                    self.unicorn.update(self.graphics)
                    self.t -= 1
                time.sleep(self._sleep/100.0)
                if self.cycles >= max(int(5/self._sleep), -self.wrap + self.unicorn.get_width()): # 5 seconds or whatever time it takes to scroll
                    print("resetting showing")
                    self.showing = (self.showing + 1 ) % 4;
                    self.cycles = 0
                    new_song = self.current_song()
                    if new_song != self.playing_now:
                        self.showing = 1
                        self.playing_now = new_song
                        self.wrap = -self.graphics.measure_text(self.playing_now, scale=0)
                        self.t = self.unicorn.get_width()
                        self.hue()
                        self.set_color()
                        gc.collect()
        
     
    def set_color(self):
        """Fix the color given the HSV in self. To avoid creating too many color objects"""
        try:
            self.color = self.graphics.create_pen_hsv(self._hue, 0.8, self._value/100.0)
        except Exception as e:
            print("Failed to generate color, values:")
            print(f"{self.hue}, 0.8, {self._value/100.0}")
            
    def current_song(self):
        try:
            r = urequests.get("https://api.radioswissjazz.ch/api/v1/rsj/en/current", timeout=1)
            title = r.json()['channel']['playingnow']['current']['metadata']['title']
            artist = r.json()['channel']['playingnow']['current']['metadata']['artist']
            return f"{title} - {artist}".replace("g", "9") # g-s don't look good
        except Exception as e: 
            if self.debug:
                return str(e)
            return ""

    def value_up(self):
        """Increment the value (brightness) of the color"""
        self._value += 10
        if self._value > 101:
            self._value = 10
    
    def hue(self):
        """Set a random hue"""
        self._hue = float(random.randint(0, 30))/30.0

    def sleep(self):
        """Cycle the speed"""
        
        self._sleep += 1
        if self._sleep > 20:
            self._sleep = 5

sjt = SwissJazzTicker()

sjt.loop()


