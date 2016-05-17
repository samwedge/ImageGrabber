# ImageGrabber
Website image grabber

Python script to grab images from a website at set intervals.
It can be used to collect images from an online webcam so that you can put them together into a timelapse video, or simply to keep a local record.

The code has a section labelled “USER SETTINGS”. In this section, you can define a list of websites under the “paths” variable. Each of these links will be checked by the code and the images downloaded. The “periodic” variable can be “True” or “False”. If True, the code will run every “t” seconds. Note that this doesn’t strictly download the images every t seconds because I have done this a lazy way. It is every t seconds + the time taken to download and process the images. To get around this, you can set “periodic” to False (which will instruct the code to run once only) and use another tool (such as cron) to run the code periodically.

When the code first runs, it will create a directory called “IMAGES”. In this directory, it will create a separate directory for each website in the “paths” list. Each time it downloads an image, it will perform a check to see if that image has already been downloaded. If so, it will discard the latest download. If not, then it will add it to the directory.
