# rebotics scripts

Collection of scripts for rebotics

# Requirements
OpenCV installed locally. Otherwise it will not work.

Or docker installed locally. 

# Installation
If you don't use `pipsi`, you're missing out.
Here are [installation instructions](https://github.com/mitsuhiko/pipsi#readme).

`pipsi` can be installed with:

    $ sudo pip3 install pipsi

Then simply run to install all dependecies:

    $ pipsi install .


For docker:

    $ docker-compose build

That's it. And prepend docker run for every time you use want to use the following scripts.

For example:

    $ docker run -it -v ~/Downloads:/Downloads -v /tmp:/tmp retechlabs/rebotics-scripts rebotics extract_keyframes -o /Downloads/thumbnails /Downloads/VID_20171030_165205.mp4

This command will attach local `~/Downloads` folder inside the container and 
run keyframe extraction of the video to the thumbnails folder

## Create wheel
To easily distribute the script to the end user

    $ python setup.py bdist_wheel --universal

## Installation from wheel
Install from wheel distribution

    $ pip install rebotics_scripts-0.1.1-py2.py3-none-any.whl

# Usage

To use it:

    $ rebotics --help


# Extract keyframes
Extracting keyframes every second with defined threshold.

    $ rebotics extract_keyframes 

```
Usage: rebotics extract_keyframes [OPTIONS] [FILES]...

Options:
  -x INTEGER               x axis coordinate of top left corner. Default=0
  -y INTEGER               y axis coordinate of top left corner. Default=0
  -x1 INTEGER              width of bouding box. Default the bottom of the
                           image
  -y1 INTEGER              width of bouding box. Default the bottom of the
                           image
  -t, --threshold INTEGER  Threshold of keyframes extraction
  -o, --output PATH        Output path of the thumbnails. Default: .
  --help                   Show this message and exit.
```


# Using scrapped scripts:
create virtual environment using `venv` or `mkvirtualenv`

    $ virtualenv venv

Make sure that the installation is done for python 3.5+. 
Activate virtualenv environment
    
    $ source venv/bin/activate

Then hit installation of the dependencies
    
    $ pip install -r requirements.txt
    
# For tor installation
    
    $ sudo apt install tor
