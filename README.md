# LuxHelper

Lux helper is a program target to help adjust Lux data information, such as correct mising points, from solar geolocators in a easier way, by the use of standard image editors.

Typically, solar geolocators produce Lux data with missing, dim and noise samples. That, that require manual adjusts, specially during sunrise and sunset itensity areas. This periods are utilized by analisys tools to estimate the position of the geolocators and their carries: birds.

The missing points of geolocator data is typically adjusted by reseachers using R and TwGeo package, on a sample basis, in a demanding task, onto a not intuitive fronted build onto R.

This program address this adjustment, allowing the use of of-the-self image editors, such as Gimp.

The program has 2 main functions:

* Converts lux data to bitmaps
    Converts a lux file into a Bitmap to be adjusted on a image editor, such as Gimp. Each colunm on the Bitmap represents a entire day of samples. Each line pixel represents individual samples taken during the day. This function produces a file called **input lux filename.bmp**

* Converts bitmap to lux data
    Take a previous created Bitmap adjusted by the user and converts back to a Lux file with header and dates for each sample. Requires also the original Lux file to gather headers and dates. Produces a new lux file called **input bmp.lux**

The program was write in Python 3 and should run out of the box on any terminal, on Windows and Linux, without major issues.

## Installing

Clone or download the current repository on your machine.

You need Python 3 to execute the program. Tests were made with Python 3.8.10 on Ubuntu 20.04 Linux machine, however should work with both with Windows and Linux containing Python 3.

No special libraries are required to execute.

Suggest installing vanilal Python from https://www.python.org/downloads/

Possible Bitmap editors to be used are:
* MS Paint (simple but effective)
* Gimp (powerfull and free).
* **Avoid using Inkspace, since it is a vectorial editor.**

For terminal, suggest using git-bash on Windows https://git-scm.com/downloads.

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

The command will generate a BMP file on the same folder called `Chestnut_BV753.lux.bmp` for the required `Chestnut_BV753.lux` lux file. Then you can open the image on any editor and proceed the adjustments on sunrise and sunset.

> NOTE:
> Since Lux data usually varies from 0 to 100.000 Lux, and bitmaps only support values from 0 to 255 (8 bits), we do the follow processing on each entry:
> 
> We normalize all the entries, apply a exponential adjustment and scale them between 0 to 255 to be
>  possible to use with BMP file. The exponential adjustment allows low bright values to
> be more visible, but change little the high bright values.
> After external processing is done on the editor, the scprit will scales back the values to original ranges.
>

Only use values between back and white while editing the image. On Gimp you can easily adjust the image contrast to enhance dim points, draw lines and use tools like Erode and Dilate to adjust the final image. Don't forget to save the changes after finish **over the original Bitmap**.

> ATTENTION: Do not change the image WIDTH or HEIGHT.

--------

### Convert LUX to BMP:

Example command:

`python3 luxHelper.py bmp2lux --bmpFile Chestnut_BV753.lux.bmp --refLuxFile Chestnut_BV753.lux`

The command will convert the Bitmap defined on bmpFile parameter `Chestnut_BV753.lux.bmp` to a LUX file on the current folder called `Chestnut_BV753.lux.bmp.lux`. Now you can grab this file and import it inside R and proceed normally with your data analisys.

If the original dimensions of the image were changed during the process, the *bmp2lux* will detect and stop without producing any artifacts.
