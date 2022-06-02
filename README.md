# FaustVision
Malleable computer vision tool allowing users to specify synths ascribed to different colors. The application detects objects within the frame, and depending on the color, plays the assigned instrument. Users specify the frequency range of each instrument. The x-coordinate position of the object affects frequency being played, while the y-coordinate affects amplitude.

## Installation
This application requires the installation of the `FAUST` [(Functional Audio Streaming)](https://faust.grame.fr/) and `Python` programming languages to path. Furthermore, `JACK` (Jack Audio Connection Kit) should be installed. This can be done in several ways depending on your operating system:
```
sudo apt-get/dnf install qjackctl
```
Be sure to also install the relevant Python packages by running
```
pip install -r requirements.txt
```

## Application Usage
This is a terminal based application, controlled by a shell script. Run the application by calling
```
sh main.sh ...
```
Note that when running the script, one can call up to four optional arguments `--red`, `--blue`, `--green`, `--yellow` with attached synths, written in FAUST. Example synths which can be used are provided in the `./examples` directory. You are also welcome to write and use your own synths written in FAUST (that's kind of the point!). Personalized FAUST `dsp` files can materialize to pretty much anything, so long as the process line is explicitly defined to take two arguments, frequency and amplitude (in that order) - they do not necessarily have to be used, but should be present.
```
...
...
...
process(freq, amp) = ...
```
After having supplied the color synths, you will be prompted to specify a frequency range for each defined color. Specify this range by writing the lower and upper bound seperated with a dash `-`. For example,
```
//> sh main.sh --green=./examples/sinosc.dsp --yellow=./examples/moog.dsp --blue=./examples/sinosc.dsp
* green instrument frequency range:0-400
* yellow instrument frequency range:100-500
* blue instrument frequency range: ...
```
Once you have specified a frequency range for each color, the application will load your webcam along with a JACK slider sound board visualizing the current frequency and amplitude of each instrument. Moving objects of the defined color will alter these variables in real time! To close the application, press the `q` key to close the webcam, and close the JACK slider sound board. 
