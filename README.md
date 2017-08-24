# theia
`theia` is a 3D Gaussian optics simulation program and library, with support for various optical components, non-sequential tracing, and general astigmatism. It was developed by the Optics Group of the Virgo collaboration at EGO in Cascina, Italy.

`theia` is written in Python2.7, in order to offer full modularity, portability and the object-oriented programming style to users.

In its executable form, `theia` allows for readily written text-based input of the optical setup and clear output of the physical data on the propagation of Gaussian beams through the optical setup, also in text form. When used in its library form, `theia` exploits the scripting possibilities of Python and can be used as a powerful tool for tasks such as optical bench design and optimization, stray light hunting, component alignment, etc.

## Installing
##### Requirements
Building `theia` and its documentation requires a small number of Python and latex packages which are listed in the REQUIREMENTS file.

##### Programs - Documentation
Once in the project root directory, issue the following to install `theia` locally (this will install the `theia` to `~/.local/bin` and this directory **must** be in your `PATH` to use `theia`):

- installation and documentation compilation: `make install`;
- only installation in the local environment: `make build-theia`;
- only documentation: `make build-doc`.

You can then move the pdf documents found in `doc/` and the tutorial files found in `tutos/` to wherever you feel is best and get rid of the project directory if you like.

For a system-wide installation, issue the following with root privileges:
`python setup.py install` (this will nonetheless not compile documentation).

##### Uninstalling
To remove a local `theia` installation from your system, `cd` to the `theia` root repository wherever it is (or download a new one) and issue:
`make clear`

To remove a system wide installation is generally a system-specific procedure but the Python2.7 libraries are generally kept in `/usr/local/lib/python2.7/*-packages`

## Usage
##### `theia` program
In general:
`theia [options] FNAME`

`theia` takes a `.tia` formatted input text file for the optical setup configuration and has a number of options concerning the output of information to the console and the writing of the output text file.

For the format of the input file, see the`userguide.pdf` and `quickref.pdf` files in `doc/` and for details on the command line options, you can also see the output of `theia -h`.

##### `theia` library
As usual, you can use the
```python
from theia.running.simulation import Simulation
```
idiom from Python to use specific functions or modules from the `theia` library. Please refer to the `apiguide.pdf` file for more details on the API.

## Documentation
To learn on `theia`, you will find (after installation) in `doc/`:

- `userguide.pdf` as a global guide to the operation of `theia` on the command line and an introduction to the `theia` library;
- `quickref.pdf` for an at-a-glance reference on the `.tia` format;
- `apiguide.pdf` for a detailed guide to the `theia` library.

For an easy online documentation, surf to `http://theia.hopto.org/docs/html/index.html`.

Don't forget that once you've installed `theia` you can call `pydoc [IMPORT PATH TO A THEIA MODULE OR PACKAGE]` from the command line for a quick query.

## Licensing
In the effort of taking down walls in the way of physics and computation, `theia` is free software and is released under the GNU General Public License, version 3+. So please feel free (as in freedom) to copy, take home, modify, teach, learn, and redistribute `theia`.

See the LICENSE file it the project root directory for more details.

## Contributing
The Theia Project is also an open source project, so please feel inventive and contact `raphael.duque@polytechnique.edu` for suggestions, comments, access to the git repository and bug reporting.

## Acknowledgements
This work owes a great deal to many people in and out of the gravitational interferometry community. We would like to thank G. Hemming, H. Yamamoto, and G. Duque among others.
