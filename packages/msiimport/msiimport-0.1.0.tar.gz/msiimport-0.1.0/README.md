# msiimport

## Description

A convenience package for accessing mass spec image data stored as analyze75 formated files (.hdr, .img, .t2m).

If there is interest in further functionality, please create an issue to ask for features or filetype compatibility (imzML, ...).

No filetype writing is planned at this time.

## Installation

Install msiimport with:

`pip install msiimport`

## Example

```python
# Get a 2D ndarray of data near an m/z peak

from msiimport import analyze75 as ana

#...

data = ana(path_to_dot_hdr)
image = data.getImage(peakmz=303.23, tolerance=0.4)

```