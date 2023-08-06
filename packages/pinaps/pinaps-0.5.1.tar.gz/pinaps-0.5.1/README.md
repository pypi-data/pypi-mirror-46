# PiNaps Supporting Library

This library provides comprehensive, high level control of the [Pi-Naps_v0.2](https://www.blino.io/maker) Raspberry Pi hat.

<center> ![Blino Logo](imgs/BlinoLogo_Simple.svg) </center>

## Quick Start

```console
pip install pinaps
pip install SC16IS750

sudo raspi-config
```
> - _Select __interfacing options__ from menu._
> - _Select __serial__ from menu._
> - _Select __no__ to shell use over serial_.
> - _Select __yes__ to enabling serial port hardware_.

```console
sudo raspi-config
```
> - _Select __interfacing options__ from menu._

> - _Select __I2C__ from menu._

> - _Select __yes__ to enable ARM I2C interface._

Clone our examples repository somewhere appropriate:

```console
git clone https://Blino_Tech@bitbucket.org/blino-dev/pinaps.git
```

Run an example script - don't forget to plug your electrodes in!

```console
cd pi-naps_examples/

python meditate.py
```


## Additional Notes

### Pip Installing

If you're having trouble using pip install. Try using "python -m pip install --index-url https://pypi.org/simple/ example_pkg"
Where the url is the project url and the example_pkg is the package you wish to install.

### Python Library Path

You might be having a lot of trouble finding where to install the libraries manually. On raspbian it should look something like this:
"usr/local/lib/python2.7/dist-packages"

### Contacting Blino

If you'd like to get in contact with us about the PiNaps Library, especially any bugs you come across - Contact Harri at harri.renney@blino.co.uk