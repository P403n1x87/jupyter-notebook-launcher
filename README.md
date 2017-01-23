## Synopsis

Jupyter Notebook Launcher is a Jupyter Notebook Launcher and Indicator for Ubuntu. The installation will also create a MIME type for jupyter notebooks that can be opened directly from the file manager.


## Requirements

- Ubuntu (>= 16.10)
- jupyter-notebook
- python3
- python3-gi
- gir1.2-gtk-3.0
- gir1.2-appindicator3-0.1
- gir1.2-glib-2.0


## Installation

There are two ways of installing this software. Make sure that all dependencies are satisfied:

~~~
sudo apt install jupyter-notebook, jupyter-notebook, python3-gi, gir1.2-gtk-3.0, gir1.2-appindicator3-0.1, gir1.2-glib-2.0
~~~

### The Nest of Heliopolis PPA

Add _The Nest of Heliopolis_ Ubuntu PPA to your Software Sources with

~~~
sudo apt-add-repository ppa:phoenix1987/ppa
~~~

and then install with

~~~
sudo apt update
sudo apt install jupyter-notebook-launcher
~~~

### Pip

Clone this branch in any folder you like and then run the `setup.py` script with

~~~
sudo -H pip install jupyter-notebook-launcher
~~~


## License

GPLv3.
