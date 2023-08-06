import nibabel as nib
import numpy as np
import os

class analyze75():
    """Convenience class for opening and accesing a massspec images formatted with analyze75 (.hdr,.img,.t2m)"""

    def __init__(self, path_to_hdr_file):
        """Load the analyze75 dataset

        Parameters
        ----------
        path_to_hdr_file : str
            Path to .hdr file with .img and .t2m files in the same directory
        
        """

        self.hdrpath = path_to_hdr_file
        self.folder, hdrname = os.path.split(path_to_hdr_file)
        self.filename, _ = os.path.splitext(hdrname)
        
        self.t2mpath = os.path.join(self.folder, (self.filename + ".t2m"))
        self.load()
    
    def load(self):
        """Internal loading function"""
        self.nibdata = nib.analyze.load(self.hdrpath)
        
        # Find number of scanlines
        scanlines = self.nibdata.shape[0]
        
        # Read t2mdata
        self.t2marray = None
        with open(self.t2mpath, "rb") as f:
            self.t2marray = np.fromfile(f, dtype='f', count=scanlines)
    
    def getPeakdata(self, peakmz, tol=1e-08):
        """Returns 3 dimension array of data in the m/z range [peakmz-tol, peakmz+tol].

        Parameters
        ----------
        peakmz : float
            Mass to charge ratio peak to center around.
        tol : float, optional
            Tolerance value to define the data window. Default 1e-08

        Returns
        -------
        ndarray(Ni, Nj, Nk)
            Data array of the selected m/z range.

        """

        datamask = np.ma.masked_values(self.t2marray, peakmz, atol=tol, copy=False).mask
        d = self.nibdata.get_data().squeeze()
        return d[datamask, :, :]
    
    def getImage(self, peakmz, tol=1e-08, aggregatefunc=np.sum):
        """Get a 2D image by applying aggregatefunc to the m/z range [peakmz-tol, peakmz+tol] in the data. 

        Parameters
        ----------
        peakmz : float
            Mass to charge ratio peak to center around.
        tol : float, optional
            Tolerance value to define the data window. Default 1e-08
        aggregatefunc : function (Ni,) -> float, optional
            This function should accept 1-D arrays. It is applied to 1-D slices of the data. Defaults to np.sum.
        Returns
        ------
        ndarray(Nj, Nk)
            Array where the multiple planes of data have been combined by aggregatefunc.

        """

        rawdata = self.getPeakdata(peakmz, tol)
        return np.apply_along_axis(aggregatefunc, 0, rawdata)