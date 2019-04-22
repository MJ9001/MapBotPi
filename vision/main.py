import sensor, image, time, ujson, pyb

thresholds = [(30, 100, 30, 80, -10, 46),
              (30, 100, -21, -3, -56, -14),
              (30, 100, -23, 22, 27, 61),
              (30, 100, -58, -23, -3, 47)]

red_led     = pyb.LED(1)
green_led   = pyb.LED(2)
blue_led    = pyb.LED(3)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_brightness(0)
sensor.set_saturation(0)
sensor.set_contrast(0)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

port = pyb.USB_VCP()

angleOfConcern = 35.4
clock = time.clock()
printStatus = True

blob_color_lookup = {
    1 << 0  :   "RED",
    1 << 1  :   "BLUE",
    1 << 2  :   "YELLOW",
    1 << 3  :   "GREEN"
}
leds = (red_led, blue_led, green_led)
led_lookup = {
    "RED"       :   (red_led,),
    "BLUE"      :   (blue_led,),
    "GREEN"     :   (green_led,),
    "YELLOW"    :   (red_led, green_led)
}

def detectAllColours(img):
    pole = None
    blobs = img.find_blobs(thresholds, pixels_threshold=300, area_threshold=300, roi=[0, 66, 321, 175])
    for blob in blobs:
        y = blob.rect()[2]
        if pole is None or y < pole.rect()[2]:
            pole = blob

    img.draw_rectangle(pole.rect())
    img.draw_cross(pole.cx(), pole.cy())
    x, y, width, height = pole.rect()
    dist = 3529.5 / height
    distX = centerX - pole.cx()
    aa_divisor = 1 if distX > 0 else 2
    actual_angle = (distX / (img.width() / aa_divisor)) * angleOfConcern
    
    color = blob_color_lookup.get(pole.code())
    params = {
        "color"     :   color,
        "angle"     :   actual_angle,
        "distance"  :   dist
    }
    for led in leds:
        led.off()
    for led in led_lookup.get(color):
        led.on()

    return params

while(True):
    #led.off()
    clock.tick()
    img = sensor.snapshot()
    centerX = int(img.width()/2)
    centerPoint = int(img.width()/2),int(img.height()/2)
    #img.draw_rectangle(int(320/2),int(240/2),5,5)
    pole = detectAllColours(img)
    port.write(ujson.dumps(pole))
