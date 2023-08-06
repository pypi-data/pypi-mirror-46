# ALS.Milo (version 0.15)

Overview
---
_**Milo**_ is a suite of Python modules used to read, process, and analyze 
data that was collected on the **Scattering Chamber** located at 
**Beamline 4.0.2** (_a.k.a. **BL402**_) of the **Advanced Light Source** 
(Berkeley, CA USA).

It is distributed under the _namespace package_, _**ALS**_. 

Installation
---
### Install from PyPI
**_ALS.Milo_** can be installed from PyPI using `pip`.
The following example shows how.
```bash
>> sudo pip install ALS.Milo
```
### Install from local repository (download)
**_ALS.Milo_** can be installed from a local copy of the project repository 
using `pip`. The following example shows how.
```bash
>> cd ALS.Milo-0.15.0/  # Local directory of project repository
>> sudo pip install .
```

Background information
---
Data from the BL402 Scattering Chamber is stored in two types of files:
* **FITS files**: Each image captured by the CCD (_a.k.a._ the camera) is 
stored in a separate file using the _FITS_ format. _More details below._
https://fits.gsfc.nasa.gov/fits_documentation.html
* **Scan summary files**: When a scan sequence is run to collect data, a text 
file is created to summarize the parameters of the scan and the data collected.

   Every _scan summary file_ contains a header that describes the scan and the 
types of data recorded, followed by data rows -- one row per data point. An 
_Instrument Scan_ provides an _image filename_ in each data row that can be 
used to access the CCD images recorded during the scan.

Usage
---
`class CcdImageFromFITS` encapsulates the operations of loading CCD data 
from a FITS file (including header information), accessing that data, and 
converting CCD screen coordinates (pixels) into reciprocal space coordinates.

If _**ALS.Milo**_ suite is not properly installed, or if it is installed in a 
directory that is not in the _system path_, the following commands can be used 
to access the `CcdImageFromFITS` class in the `qimage` module.
```python
import sys
sys.path.append("C:/Experiments/Padraic/Python402/Milo/") # Substitute appropriate path here
from als.milo.qimage import CcdImageFromFITS
```

To read a FITS file use the constructor:  
`CcdImageFromFITS(`*`filename`*`)` ,  
where _filename_ is a reachable (relative or absolute) file path to the FITS 
file.

The two-dimensional array of data can be accessed through the instance member, 
`data`.
```python
ccd_image = CcdImageFromFITS("NiFe_8044-00024.fits")
ccd_image.data  # 2D array with shape (num_rows, num_columns)
```

Reciprocal space coordinates are calculated for each pixel using the member 
function, `qvalues_df()`. The return value is a PANDAS dataframe (_df_) where 
each row corresponds to a single pixel. The columns `["Qx", "Qy", "Qz"]` are 
the diffractometer coordinates of the reciprocal space vector in units of 
nm<sup>-1</sup> (_Q_ = 2&pi; / _d_). Intensity of each pixel is in column, 
`"Counts"`.
```
ccd_image = CcdImageFromFITS("NiFe_8044-00024.fits")
q_ccd_df = ccd_image.qvalues_df()
q_ccd_df["Qx", "Qy", "Qz", "Counts"]    # CCD data in reciprocal space
```

Copyright Notice
---
ALS.Milo: BL402 RSXD Data Analysis, Copyright (c) 2014-2019, The Regents of 
the University of California, through Lawrence Berkeley National Laboratory 
(subject to receipt of any required approvals from the U.S. Dept. of Energy). 
All rights reserved.

If you have questions about your rights to use or distribute this software, 
please contact Berkeley Lab's Intellectual Property Office at IPO@lbl.gov.

NOTICE. This Software was developed under funding from the U.S. Department of 
Energy and the U.S. Government consequently retains certain rights. As such, 
the U.S. Government has been granted for itself and others acting on its 
behalf a paid-up, nonexclusive, irrevocable, worldwide license in the 
Software to reproduce, distribute copies to the public, prepare derivative 
works, and perform publicly and display publicly, and to permit other to do 
so. 