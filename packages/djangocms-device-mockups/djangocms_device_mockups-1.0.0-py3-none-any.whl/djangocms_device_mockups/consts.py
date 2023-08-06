# Get table from here -
# https://github.com/pixelsign/html5-device-mockups
# check for missing from here:
# https://github.com/pixelsign/html5-device-mockups/blob/master/src/scss/devices.scss

DEVICE_MOCKUPS = [
        ('Chromebook', 'Chromebook', 'portrait', 'black'),
        ('Galaxy S3', 'galaxyS3', 'portrait, landscape', 'black, white'),
        ('Galaxy S5', 'galaxyS5', 'portrait, landscape', 'black, white, gold'),
        ('Galaxy Tab 4', 'galaxyTab4', 'portrait', 'black, white'),
        ('HTC One M8', 'HtcOneM8', 'portrait, landscape', 'black'),
        ('Huawei P8', 'HuaweiP8', 'portrait, landscape', 'gold'),
        ('iMac', 'iMac', 'portrait', 'black'),
        ('iPad', 'iPad', 'portrait, landscape', 'black, white'),
        ('iPad Air 2', 'iPadAir2', 'portrait, landscape', 'black, white, gold'),
        ('iPad Pro', 'iPadPro', 'portrait, landscape', 'black, white, gold'),
        ('iPhone 6', 'iPhone6', 'portrait, landscape', 'black, white, gold'),
        ('iPhone 6 Plus', 'iPhone6Plus', 'portrait, landscape', 'black, white, gold'),
        ('iPhone SE', 'iPhoneSE', 'portrait, landscape', 'black, white, gold, pink'),
        ('iPhone 5', 'iPhone5', 'portrait, landscape', 'black, white'),
        ('iPhone 6 Hand', 'iPhone6Hand', 'portrait', 'black, white'),
        ('iPhone 7 Hand', 'iPhone7Hand', 'portrait', 'black'),
        ('iPhone 7 Hand 2', 'iPhone7Hand_2', 'portrait', 'black'),
        ('iPhone 7', 'iPhone7', 'portrait, landscape', 'black, white, gold, pink, red'),
        ('iPhone X', 'iPhoneX', 'portrait, landscape', 'black'),
        ('Lumia 930', 'Lumia930', 'portrait, landscape', 'black, white'),
        ('Macbook', 'Macbook', 'portrait', 'black, white, gold'),
        ('Macbook 2015', 'Macbook2015', 'portrait', 'black, white, gold'),
        ('Macbook Pro', 'MacbookPro', 'portrait', 'black'),
        ('Pixel', 'Pixel', 'portrait', 'black, white'),
        ('Samsung TV', 'SamsungTV', 'portrait', 'black'),
        ('Surface Pro 3', 'SurfacePro3', 'landscape', 'black'),
        ('Surface Studio', 'SurfaceStudio', 'portrait', 'black'),
        ('Surface', 'Surface', 'portrait', 'black'),
]

DEVICE_CHOICES = [(d[1], d[0]) for d in DEVICE_MOCKUPS]

ORIENTATION_CHOICES =  [('portrait', 'Portrait'),
                        ('landscape', 'Landscape')]

COLOURS = 'black, white, gold, pink, red'
COLOUR_CHOICES = [(c, c) for c in COLOURS.split(', ')]

DEVICE_DICT = {d[1]: {'orientation': d[2].split(', '), 'colour': d[3].split(', ')} for d in DEVICE_MOCKUPS}