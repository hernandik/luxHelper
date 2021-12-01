# LuxHelper

Lux helper is a program target to help adjust Lux data from solar geolocators faster with the use of standard image editors.

Typical, solar geolocators produce Lux data with missing, dim and noise samples, that require manual adjusts, specially during sunrise and sunset. This periods are utilized by diverse analisys to estimage the position of the geolocators and their carries: birds.

This information is typically adjusted by reseachers using R and TwGeo package, on a sample basis, in a demandaing task, on a not to intuitive fronted build onto R.

This program address this adjustment, allowing the use of of-the-self image editors, such as Gimp.

The program has 2 main functions:

* Converts lux data to bitmaps
    Converts a lux file into a Bitmap to be adjusted on a image editor, such as Gimp. Each colunm on the Bitmap represents a entire day of samples. Each line pixel represents individual samples taken during the day. This function produces a file called **input lux filename.bmp**

* Converts bitmap to lux data
    Take a previous created Bitmap adjusted by the user and converts back to a Lux file with header and dates for each sample. Requires also the original Lux file to gather headers and dates. Produces a new lux file called **input bmp.lux**

The program was write in Python 3 and should run out of the box on any terminal, on Windows and Linux, without major issues.

## Installing

Clone or download the current repository on your machine.

You need Python 3 to execute the program. Tests were made with Python 3.8.10 on Ubuntu 20.04 Linux machine, however should work with any machine containing Python 3, like Windows ones.

No special libraries are required to execute. Out of box Python should work.

Suggest installing vanilal Python from https://www.python.org/downloads/

Possible Bitmap editors to be used are:
* MS Paint (simple but effective)
* Gimp (powerfull and free).

Suggest using git-bash on Windows as terminal https://git-scm.com/downloads.

> Avoid using Inkspace, since it is a vector editor and can change the image resolution easily.

## Using the tool

Open a terminal on a machine where Python is installed, over the folder where you download the script.

Execute python or python3 and assure that the python executable is found on the machine.
Run `python --version` to check that you have the correct major Python version.

Check that the luxHelper is running without issues by executing `python luxHelper.py`. That will present with help information about how to use the tool too.

If errors occur, that means that some library is missing on your Python environment.

--------

### Convert LUX to BMP:

Example command:

`python3 luxHelper.py lux2bmp --luxFile ../Downloads/Chestnut_BV753.lux`

The command will generate a BMP file on the current folder called **Chestnut_BV753.lux.bmp** containing the converted lux file. Then you can open the image on any editor and proceed he adjustments on sunrise and sunset.

> NOTE: 
> Since Lux data usually varies from 0 to 100.000 Lux, and bitmaps only support values from 0 to 255 (8 bits), we do the follow processing on each entry:
> 
> We normalize all the entries, apply a exponential adjustment and scale to 0 to 255 to be
>  possible to use with BMP file. The exponential adjustment allows low bright values to
> be more visible, and high bright values to do not change.
> After external processing is done on editor, the scprit scales back the values to original ranges.
>

Only use back, white and gray while editing the image. On Gimp you can easily adjust the image contrast to enhance dim points, draw lines and use tools libe Erode and Dilate to adjust the final image. Dont forget to save the changes after finish over the original Bitmap.

> ATTENTION: Do not change the image width or height.

--------

### Convert LUX to BMP:

Example command:

`python3 luxHelper.py bmp2lux --bmpFile Chestnut_BV753.lux.bmp --refLuxFile Chestnut_BV753.lux`

The command will convert the Bitmap defined on bmpFile to a LUX file on the current folder called **Chestnut_BV753.lux.bmp.lux**. Now you can grab this file and import it inside R and proceed normally with your data analisys.

If the original dimentions of the image were changed, the *bmp2lux* will detect and stop without producing any artifacts.

