"""
LavaVu python interface: viewer utils & wrapper

This module provides an interface to the LavaVu library allowing
loading of data, rendering of static images, animation and interactive visualisation

To create an instance of the LavaVu rendering engine, use the Viewer() class, e.g.

>>> import lavavu
>>> lv = lavavu.Viewer()

See the :any:`lavavu.Viewer` class documentation for more information.

"""

#NOTE: regarding sync of state between python and library
#- sync from python to lavavu is immediate,
#    property setting must always trigger a sync to lavavu
#- sync from lavavu to python is lazy, always need to call _get()
#    before using state data

__all__ = ['Viewer', 'Object', 'Properties', 'ColourMap', 'DrawData', 'Figure', 'Geometry', 'Image',
           'download', 'grid2d', 'grid3d', 'cubeHelix', 'loadCPT', 'matplotlib_colourmap', 'printH5', 'lerp', 'style', 'cellstyle', 'cellwidth',
           'version', 'settings', 'is_ipython', 'is_notebook', 'getname']

#Module settings
import os
#must be an object or won't be referenced from __init__.py import
#(enures values are passed on when set externally)
settings = {"default_args" : [], "echo_fails" : False, "quality_override" : None}
#Default arguments for viewer creation
_val = os.environ.get('LV_ARGS')
if _val:
  settings["default_args"] = _val.split()
#Dump base64 encoded images on test failure for debugging
_val = os.environ.get('LV_ECHO_FAIL')
if _val:
    settings["echo_fails"] = bool(_val)
#Quality override - ignore passed quality setting
_val = os.environ.get('LV_QUALITY')
if _val:
    settings["quality_override"] = int(_val)

import json
import math
import sys
import glob
import control
import numpy
import re
import copy
import base64
import threading
import time
import weakref

from vutils import is_ipython, is_notebook, getname

#import swig module
import LavaVuPython
version = LavaVuPython.version

TOL_DEFAULT = 0.0001 #Default error tolerance for image tests
TIMER_MAX_FPS = 200   #FPS for frame timer
TIMER_INC = 1.0 / TIMER_MAX_FPS #Timer increment in milliseconds

geomnames = ["labels", "points", "grid", "triangles", "vectors", "tracers", "lines", "shapes", "volumes", "screen"]
geomtypes = [LavaVuPython.lucLabelType,
             LavaVuPython.lucPointType,
             LavaVuPython.lucGridType,
             LavaVuPython.lucTriangleType,
             LavaVuPython.lucVectorType,
             LavaVuPython.lucTracerType,
             LavaVuPython.lucLineType,
             LavaVuPython.lucShapeType,
             LavaVuPython.lucVolumeType,
             LavaVuPython.lucScreenType]

datatypes = {"vertices":  LavaVuPython.lucVertexData,
             "normals":   LavaVuPython.lucNormalData,
             "vectors":   LavaVuPython.lucVectorData,
             "indices":   LavaVuPython.lucIndexData,
             "colours":   LavaVuPython.lucRGBAData,
             "texcoords": LavaVuPython.lucTexCoordData,
             "luminance": LavaVuPython.lucLuminanceData,
             "rgb":       LavaVuPython.lucRGBData,
             "values":    LavaVuPython.lucMaxDataType}

def _convert_keys(dictionary):
    if (sys.version_info > (3, 0)):
        #Not necessary in python3...
        return dictionary
    """Recursively converts dictionary keys
       and unicode values to utf-8 strings."""
    if isinstance(dictionary, list) or isinstance(dictionary, tuple):
        for i in range(len(dictionary)):
            dictionary[i] = _convert_keys(dictionary[i])
        return dictionary
    if not isinstance(dictionary, dict):
        if isinstance(dictionary, unicode):
            return dictionary.encode('utf-8')
        return dictionary
    return dict((k.encode('utf-8'), _convert_keys(v))
        for k, v in dictionary.items())

class _CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(CustomEncoder, self).default(obj)

def _convert_args(dictionary):
    """Convert a kwargs dict to a json string argument list
       Ensure all elements can be converted by using custom encoder
    """
    return str(json.dumps(dictionary, cls=_CustomEncoder))

def grid2d(corners=((0.,1.), (1.,0.)), dims=[2,2]):
    """
    Generate a 2d grid of vertices

    Parameters
    ----------
    corners : tuple or list
        top left and bottom right corner vertices (2d)
    dims : tuple or list
        dimensions of grid nodes, number of vertices to generate in each direction

    Returns
    -------
    vertices : array
        The 2d vertices of the generated grid
    """
    x = numpy.linspace(corners[0][0], corners[1][0], dims[0], dtype='float32')
    y = numpy.linspace(corners[0][1], corners[1][1], dims[1], dtype='float32')
    xx, yy = numpy.meshgrid(x, y)
    vertices = numpy.vstack((xx,yy)).reshape([2, -1]).transpose()
    return vertices.reshape(dims[1],dims[0],2)

def grid3d(corners=((0.,1.,0.), (1.,1.,0.), (0.,0.,0.), (1.,0.,0.)), dims=[2,2]):
    """
    Generate a 2d grid of vertices in 3d space

    Parameters
    ----------
    corners : tuple or list
        3 or 4 corner vertices (3d)
    dims : tuple or list
        dimensions of grid nodes, number of vertices to generate in each direction

    Returns
    -------
    vertices : array
        The 3d vertices of the generated 2d grid
    """
    if len(dims) < 2:
        print("Must provide 2d grid index dimensions")
        return None
    if len(corners) < 3:
        print("Must provide 3 or 4 corners of grid")
        return None
    if any([len(el) < 3 for el in corners]):
        print("Must provide 3d coordinates of grid corners")
        return None

    if len(corners) < 4:
        #Calculate 4th corner
        A = numpy.array(corners[0])
        B = numpy.array(corners[1])
        C = numpy.array(corners[2])
        AB = numpy.linalg.norm(A-B)
        AC = numpy.linalg.norm(A-C)
        BC = numpy.linalg.norm(B-C)
        MAX = max([AB, AC, BC])
        #Create new point opposite longest side of triangle
        if BC == MAX:
            D = B + C - A
            corners = numpy.array([A, B, C, D])
        elif AC == MAX:
            D = A + C - B
            corners = numpy.array([A, D, B, C])
        else:
            D = A + B - C
            corners = numpy.array([D, A, B, C])
    else:
        #Sort to ensure vertex order correct
        def vertex_compare(v0, v1):
            if v0[0] < v1[0]: return 1
            if v0[1] < v1[1]: return 1
            if v0[2] < v1[2]: return 1
            return -1
        import functools
        corners = sorted(list(corners), reverse=True, key=functools.cmp_to_key(vertex_compare))

    def lerp(coord0, coord1, samples):
        """Linear interpolation between two 3d points"""
        x = numpy.linspace(coord0[0], coord1[0], samples, dtype='float32')
        y = numpy.linspace(coord0[1], coord1[1], samples, dtype='float32')
        z = numpy.linspace(coord0[2], coord1[2], samples, dtype='float32')
        return numpy.vstack((x,y,z)).reshape([3, -1]).transpose()

    w = dims[0]
    h = dims[1]
    lines = numpy.zeros(shape=(h,w,3), dtype='float32')
    top = lerp(corners[0], corners[1], dims[0])
    bot = lerp(corners[2], corners[3], dims[0])
    lines[0,:] = top
    lines[h-1:] = bot
    for i in range(w):
        line = lerp(top[i], bot[i], h)
        for j in range(1,h-1):
            lines[j,i] = line[j]
    return lines

def cubeHelix(samples=16, start=0.5, rot=-0.9, sat=1.0, gamma=1., alpha=None):
    """
    Create CubeHelix spectrum colourmap with monotonically increasing/descreasing intensity

    Implemented from FORTRAN 77 code from D.A. Green, 2011, BASI, 39, 289.
    "A colour scheme for the display of astronomical intensity images"
    http://adsabs.harvard.edu/abs/2011arXiv1108.5083G

    Parameters
    ----------
    samples : int
        Number of colour samples to produce
    start : float
        Start colour [0,3] 1=red,2=green,3=blue
    rot : float
        Rotations through spectrum, negative to reverse direction
    sat : float
        Colour saturation grayscale to full [0,1], >1 to oversaturate
    gamma : float
        Gamma correction [0,1]
    alpha : list or tuple
        Alpha [min,max] for transparency ramp

    Returns
    -------
    list
        List of colours ready to be loaded by colourmap()
    """

    colours = []

    if not isinstance(alpha,list) and not isinstance(alpha,tuple):
        #Convert as boolean
        if alpha: alpha = [0,1]

    for i in range(0,samples+1):
        fract = i / float(samples)
        angle = 2.0 * math.pi * (start / 3.0 + 1.0 + rot * fract)
        amp = sat * fract * (1 - fract)
        fract = pow(fract, gamma)

        r = fract + amp * (-0.14861 * math.cos(angle) + 1.78277 * math.sin(angle))
        g = fract + amp * (-0.29227 * math.cos(angle) - 0.90649 * math.sin(angle))
        b = fract + amp * (+1.97294 * math.cos(angle))

        r = max(min(r, 1.0), 0.0)
        g = max(min(g, 1.0), 0.0)
        b = max(min(b, 1.0), 0.0)
        a = 1.0
        if alpha:
            a = alpha[0] + (alpha[1]-alpha[0]) * fract

        colours.append((fract, 'rgba(%d,%d,%d,%d)' % (r*0xff, g*0xff, b*0xff, a*0xff)))

    return colours

def matplotlib_colourmap(name, samples=16):
    """
    Import a colourmap from a matplotlib

    Parameters
    ----------
    name : str
        Name of the matplotlib colourmap preset to import
    samples : int
        Number of samples to take for LinearSegmentedColormap type

    Returns
    -------
    list
        List of colours ready to be loaded by colourmap()
    """
    try:
        import matplotlib.pyplot as plt
        cmap = plt.get_cmap(name)
        if hasattr(cmap, 'colors'):
            #Reduce length? many MPL maps have 256 samples,
            #unnecessary since we are already interpolating
            #Can disable this by setting samples=None
            data = cmap.colors
            if len(data) == 256 and samples is not None:
                subsample = int(256/samples)
                data = data[0::subsample]
            return data
        #Get colour samples when no list provided
        if samples == None: samples = 16
        colours = []
        for i in range(samples):
            pos = i/float(samples-1)
            colours.append(cmap(pos))
        return colours
    except (Exception) as e:
        #Assume single colour value, just return it
        return name
    return []

#Wrapper class for a set of properties
#handles property updating via internal dict
class Properties(dict):
    """
    The Properties class provides an interface to a collection of properties with a control factory,
    allowing controls to be created to manipulate their values interactively
    Properties can be passed in when created or set by using as a dictionary:

    Parameters
    ----------
    callback : function
        Optional function to call whenever a property in this
        collection is changed by an interactive control
        The function should take one argument,
        the collection of type lavavu.Properties() and will be called, with
        the new values whenever the control value is updated.
    **kwargs
        Set of initial properties to store in the collection

    Example
    -------

    Create a property set, load some test data

    >>> import lavavu
    >>> lv = lavavu.Viewer()
    >>> props = lv.Properties(floatprop=1.0)
    >>> props["boolprop"] = True
    >>> print(props)
    {'floatprop': 1.0, 'boolprop': True}

    Now create some controls to manipulate them

    >>> f = props.control.Range('floatprop', range=(0,1))
    >>> b = props.control.Checkbox('boolprop')

    """
    def __init__(self, parent, callback=None, **kwargs):
        self._parent = weakref.ref(parent)
        self.callback = callback
        super(Properties, self).__init__(**kwargs)

        #Need to store with id on parent to match when new data sent from client
        parent._collections[str(id(self))] = weakref.ref(self)

        self.control = control._ControlFactory(self)

    @property
    def parent(self):
        return self._parent()

#Wrapper class for drawing object
#handles property updating via internal dict
class Object(dict):
    """  
    The Object class provides an interface to a LavaVu drawing object
    Object instances are created internally in the Viewer class and can
    be retrieved from the object list

    New objects are also created using viewer methods
    
    Parameters
    ----------
    **kwargs
        Initial set of properties passed to the created object

    Example
    -------
        
    Create a viewer, load some test data, get objects
    
    >>> import lavavu
    >>> lv = lavavu.Viewer()
    >>> lv.test()
    >>> print(lv.objects)
    dict_keys(['particles', 'particles_colourbar', 'line-segments', 'Z-cross-section', 'Y-cross-section', 'X-cross-section'])

    Object properties can be passed in when created or set by using as a dictionary:

    >>> obj = lv.points(pointtype="sphere")
    >>> obj["pointsize"] = 5

    A list of available properties can be found here: https://mivp.github.io/LavaVu-Documentation/Property-Reference
    or by using the online help:

    >>> obj.help('opacity') # doctest: +SKIP

    """
    def __init__(self, parent, *args, **kwargs):
        self.dict = kwargs
        self._parent = weakref.ref(parent)
        self._current = 0
        self._geom = None
        if not "filters" in self.dict: self.dict["filters"] = []

        #Create a control factory
        self.control = control._ControlFactory(self)

        #Init prop dict for tab completion
        super(Object, self).__init__(**self.parent.properties)

    @property
    def parent(self):
        return self._parent()

    @property
    def name(self):
        """
        Get the object's name property

        Returns
        -------
        name: str
            The name of the object
        """
        return str(self.dict["name"])

    def _setprops(self, props):
        #Replace props with new data from app
        self.dict.clear()
        self.dict.update(props)

    def _set(self):
        #Send updated props (via ref in case name changed)
        self.parent._setupobject(self.ref, **self.dict)

    def __getitem__(self, key):
        self.parent._get() #Ensure in sync
        if key in self.dict:
            return self.dict[key]
        #Check for valid key
        if not key in self.parent.properties:
            raise KeyError(key + " : Invalid property name")
        #Default to the property lookup dict (default value is first element)
        #(allows default values to be returned from prop get)
        prop = super(Object, self).__getitem__(key)
        #Must always return a copy to prevent modifying the defaults!
        return copy.copy(prop["default"])

    def __setitem__(self, key, value):
        #Check for valid key
        if not key in self.parent.properties:
            raise KeyError(key + " : Invalid property name")
        if key == "colourmap":
            if isinstance(value, LavaVuPython.ColourMap) or isinstance(value, ColourMap):
                value = value.name #Use name instead of object when setting colourmap on object
            elif not self.parent.app.getColourMap(value):
                #Not found by passed id/name/ref, use the value to set map data
                cmap = self.colourmap(value)
                value = cmap.name

        self.parent.app.parseProperty(key + '=' + _convert_args(value), self.ref)
        self.parent._get() #Ensure in sync

    def __contains__(self, key):
        return key in self.dict

    def __repr__(self):
        return str(self.ref)

    def __str__(self):
        #Default string representation
        self.parent._get() #Ensure in sync
        return '{\n' + str('\n'.join(['  %s=%s' % (k,json.dumps(v)) for k,v in self.dict.items()])) + '\n}\n'

    #Interface for setting filters
    def include(self, *args, **kwargs):
        """
        Filter data by including a range of values
        shortcut for: filter(... , out=False)

        Parameters
        ----------
        label : str
            Data label to filter on
        values : number or list or tuple
            value range single value, list or tuple
            if a single value the filter applies to only this value: x == value
            if a list  e.g. [0,1] range is inclusive 0 <= x <= 1
            if a tuple e.g. (0,1) range is exclusive 0 < x < 1

        Returns
        -------
        int
            The filter id created
        """
        return self.filter(*args, out=False, **kwargs)

    def includemap(self, *args, **kwargs):
        """
        Filter data by including a range of mapped values
        shortcut for: filter(... , out=False, map=True)

        Parameters
        ----------
        label : str
            Data label to filter on
        values : number or list or tuple
            value range single value, list or tuple
            if a single value the filter applies to only this value: x == value
            if a list  e.g. [0,1] range is inclusive 0 <= x <= 1
            if a tuple e.g. (0,1) range is exclusive 0 < x < 1

        Returns
        -------
        int
            The filter id created
        """
        return self.filter(*args, out=False, map=True, **kwargs)

    def exclude(self, *args, **kwargs):
        """
        Filter data by excluding a range of values
        shortcut for: filter(... , out=True)

        Parameters
        ----------
        label : str
            Data label to filter on
        values : number or list or tuple
            value range single value, list or tuple
            if a single value the filter applies to only this value: x == value
            if a list  e.g. [0,1] range is inclusive 0 <= x <= 1
            if a tuple e.g. (0,1) range is exclusive 0 < x < 1

        Returns
        -------
        int
            The filter id created
        """
        return self.filter(*args, out=True, **kwargs)
            
    def excludemap(self, *args, **kwargs):
        """
        Filter data by excluding a range of mapped values
        shortcut for: filter(... , out=True, map=True)

        Parameters
        ----------
        label : str
            Data label to filter on
        values : number or list or tuple
            value range single value, list or tuple
            if a single value the filter applies to only this value: x == value
            if a list  e.g. [0,1] range is inclusive 0 <= x <= 1
            if a tuple e.g. (0,1) range is exclusive 0 < x < 1

        Returns
        -------
        int
            The filter id created
        """
        return self.filter(*args, out=True, map=True, **kwargs)

    def filter(self, label, values, out=False, map=False):
        """
        Filter data by including a range of values

        Parameters
        ----------
        label : str
            Data label to filter on
        values : number or list or tuple
            value range single value, list or tuple
            if a single value the filter applies to only this value: x == value
            if a list  e.g. [0,1] range is inclusive 0 <= x <= 1
            if a tuple e.g. (0,1) range is exclusive 0 < x < 1
        out : boolean
            Set this flag to filter out values instead of including them
        map : boolean
            Set this flag to filter by normalised values mapped to [0,1]
            instead of actual min/max of the data range

        Returns
        -------
        int
            The filter id created
        """
        #Pass a single value to include/exclude exact value
        #Pass a tuple for exclusive range (min < val < max)
        # list for inclusive range (min <= val <= max)
        self.parent._get() #Ensure have latest data
        filterlist = []
        if "filters" in self:
            filterlist = self["filters"]

        if isinstance(values, float) or isinstance(values, int):
            values = [values,values]
        newfilter = {"by" : label, "minimum" : values[0], "maximum" : values[1], "map" : map, "out" : out, "inclusive" : False}
        if isinstance(values, list) or values[0] == values[1]:
            newfilter["inclusive"] = True

        filterlist.append(newfilter)

        self.parent.app.parseProperty('filters=' + json.dumps(filterlist), self.ref)
        self.parent._get() #Ensure in sync
        return len(self["filters"])-1

    @property
    def datasets(self):
        """
        Retrieve available labelled data sets on this object

        Returns
        -------
        dict
            A dictionary containing the data objects available by label
        """
        #Return data sets dict converted from json string
        sets = json.loads(self.parent.app.getObjectDataLabels(self.ref))
        if sets is None or len(sets) == 0: return {}
        return _convert_keys(sets)

    def append(self):
        """
        Append a new data element to the object

        Object data is sometimes dependant on individual elements to
        determine where one part ends and another starts, e.g. line segments, grids

        This allows manually closing the active element so all new data is loaded into a new element
        """
        self.parent.app.appendToObject(self.ref)

    def triangles(self, data, split=0):
        """
        Load triangle data,

        This is the same as loading vertices into a triangle mesh object but allows
        decomposing the mesh into smaller triangles with the split option

        Parameters
        ----------
        split : int
            Split triangles this many times on loading
        """
        if split > 1:
            self.parent.app.loadTriangles(self.ref, data, self.name, split)
        else:
            self.vertices(data)

    def _convert(self, data, dtype=None):
        #Prepare a data set
        if not isinstance(data, numpy.ndarray):
            #Convert to numpy array first
            data = numpy.asarray(data)

        #Always convert float64 to float32
        if data.dtype == numpy.float64:
            data = data.astype(numpy.float32)

        #Transform to requested data type if provided
        if data.dtype == numpy.float32 and dtype == numpy.uint8:
            #Convert float[0,1] to uint8 * 255
            #TODO: test
            data *= 255.0
            data = data.astype(numpy.uint8)
        elif dtype != None and data.dtype != dtype:
            data = data.astype(dtype)

        #Masked array? Set fill value to NaN
        if numpy.ma.is_masked(data):
            if data.fill_value != numpy.nan:
                print("Warning: setting masked array fill to NaN, was: ", data.fill_value)
                numpy.ma.set_fill_value(data, numpy.nan)
            data = data.filled()

        return data

    def _loadScalar(self, data, geomdtype):
        #Passes a scalar dataset (float/uint8/uint32)
        data = self._convert(data)
        #Load as flattened 1d array
        #(ravel() returns view rather than copy if possible, flatten() always copies)
        if data.dtype == numpy.float32:
            self.parent.app.arrayFloat(self.ref, data.ravel(), geomdtype)
        elif data.dtype == numpy.uint32:
            self.parent.app.arrayUInt(self.ref, data.ravel(), geomdtype)
        elif data.dtype == numpy.uint8:
            self.parent.app.arrayUChar(self.ref, data.ravel(), geomdtype)


    def _checkDims(self, size):
        #User provided dims value
        if 'dims' in self.dict:
            D = self["dims"]
            #Dims match provided data?
            if isinstance(D, int):
                if D != size:
                    print("WARNING: provided 'dims' property doesn't match data size: ", D, size)
            elif len(D) == 1:
                if D[0] != size:
                    print("WARNING: provided 'dims' property doesn't match data size: ", D, size)
            elif len(D) == 2:
                if D[0]*D[1] != size:
                    print("WARNING: provided 'dims' property doesn't match data size: ", D, D[0]*D[1], size)
            elif len(D) == 3:
                if D[0]*D[1]*D[2] != size:
                    print("WARNING: provided 'dims' property doesn't match data size: ", D, D[0]*D[1]*D[2], size)

            #As data found, skip auto-calc of dims
            return True

        #No user data, calculate the dims if possible
        return False


    def _volumeDimsFromShape(self, data):
        #Volume? Use the shape as dims if not provided on value data load

        #If dims not set or don't match provided data?
        #3D shape required
        if not self._checkDims(data.size) and len(data.shape) > 2:
            #Need to flip for volume? (if in expected numpy order of Z,Y,X)
            self["dims"] = (data.shape[2], data.shape[1], data.shape[0])


    def _gridDimsFromShape(self, data):
        #Quads grid? Use the data.shape as dims if not provided on vertex data load

        #3D shape required [y, x, 3]
        #Dims set or already match provided data? skip
        if not self._checkDims(data.size/3) and len(data.shape) > 2:
            #Use matching shape dimensions, numpy [rows, cols] lavavu [width(cols), height(rows)]
            D = self["dims"]
            if data.shape[1] * data.shape[0] == data.size/3:
                D[0] = data.shape[1] #columns
                D[1] = data.shape[0] #rows
            elif data.shape[2] * data.shape[0] == data.size/3:
                D[0] = data.shape[2] #columns
                D[1] = data.shape[0] #rows
            elif data.shape[2] * data.shape[1] == data.size/3:
                D[0] = data.shape[2] #columns
                D[1] = data.shape[1] #rows
                D = (data.shape[2], data.shape[1], data.shape[0])

            self["dims"] = D

    def _tracerDimsFromShape(self, data):
        #Tracers? Use the size if not provided on vertex data load

        #Dims set or already match provided data?
        if not self._checkDims(data.size/3):
            #Dims = vertex count
            self["dims"] = (data.size/3, 1)

    def _loadVector(self, data, geomdtype, magnitude=None):
        """
        Accepts 2d or 3d data as a list of vertices [[x,y,z]...] or [[x,y]...]
         - If the last dimension is 2, a zero 3rd element is added to all vertices
        Also accepts 2d or 3d data as columns [[x...], [y...], [z...]]
         - In this case, there must be > 3 elements or cannot autodetect!
         - If the last dimenion is not 3 (or 2) and the first is 3 (or 2)
           the data will be re-arranged automatically
        """
        #Passes a vector dataset (float)
        data = self._convert(data, numpy.float32)

        #Detection of structure based on shape
        shape = data.shape
        if len(shape) >= 2:
            #Data provided as separate x,y,z columns? (Must be > 3 elements)
            if shape[-1] > 3 and shape[0] == 3:
                #Re-arrange to array of [x,y,z] triples
                data = numpy.vstack((data[0],data[1],data[2])).reshape([3, -1]).transpose()
            elif shape[-1] > 3 and shape[0] == 2:
                #Re-arrange to array of [x,y] pairs
                data = numpy.vstack((data[0],data[1])).reshape([2, -1]).transpose()

            #Now check for 2d vertices
            if data.shape[-1] == 2:
                #Interpret as 2d data... must add 3rd dimension
                data = numpy.insert(data, 2, values=0, axis=len(shape)-1)

            #Quads or tracers? Use the shape as dims if not provided
            #Quad/Triangle type?
            #if self["geometry"] == 'quads' or self["geometry"] == 'grid':
            if self["geometry"] in self.parent.renderers[LavaVuPython.lucGridType] or self["geometry"] in self.parent.renderers[LavaVuPython.lucTriangleType]:
                self._gridDimsFromShape(data)
            if self["geometry"] in self.parent.renderers[LavaVuPython.lucTracerType]:
            #elif self["geometry"] == 'tracers':
                self._tracerDimsFromShape(data)

        #Convenience option to load magnitude as a value array
        if magnitude is not None:
            axis = len(data.shape)-1
            mag = numpy.linalg.norm(data,axis=axis)
            if isinstance(magnitude, str):
                label = magnitude
            else:
                label = "magnitude"
            self.parent.app.arrayFloat(self.ref, mag.ravel(), label)

        #Load as flattened 1d array
        #(ravel() returns view rather than copy if possible, flatten() always copies)
        self.parent.app.arrayFloat(self.ref, data.ravel(), geomdtype)

    @property
    def data(self):
        """
        Return internal geometry data at current timestep
        Returns a Geometry() object that can be iterated through containing all data elements
        Elements contain vertex/normal/value etc. data as numpy arrays

        Returns
        -------
        Geometry
            An object holding the data elements retrieved

        Example
        -------
        >>> import lavavu
        >>> lv = lavavu.Viewer()
        >>> obj = lv.points(vertices=[[0,1], [1,0]])
        >>> for el in obj.data:
        ...     print(el)
        DrawData("points") ==> {'vertices': 6}
        """
        return Geometry(self)

    #Iterating an object iterates the internal geometry
    def __iter__(self):
        self._geom = self.data
        return self._geom.__iter__()

    def __next__(self): # Python 3
        return self.next()

    def next(self):
        if self._current > len(self._geom)-1:
            self._current = 0
            raise StopIteration
        else:
            self._current += 1
            return self._geom[self._current-1]

    def vertices(self, data):
        """
        Load 3d vertex data for object

        Parameters
        ----------
        data : list or array
            Pass a list or numpy float32 3d array of vertices
        """
        self._loadVector(data, LavaVuPython.lucVertexData)

    def normals(self, data):
        """
        Load 3d normal data for object

        Parameters
        ----------
        data : list or array
            Pass a list or numpy float32 3d array of normals
        """
        self._loadVector(data, LavaVuPython.lucNormalData)

    def vectors(self, data, magnitude=None):
        """
        Load 3d vector data for object

        Parameters
        ----------
        data : list or array
            Pass a list or numpy float32 3d array of vectors
        magnitude : str
            Pass a label to calculate the magnitude and save under provided name (for use in colouring etc)
        """
        self._loadVector(data, LavaVuPython.lucVectorData, magnitude)

    def values(self, data, label="default"):
        """
        Load value data for object

        Parameters
        ----------
        data : list or array
            Pass a list or numpy float32 array of values
        label : str
            Label for this data set
        """
        data = self._convert(data, numpy.float32)

        #Volume? Use the shape as dims if not provided
        if self["geometry"] == 'volume':
            self._volumeDimsFromShape(data)

        self.parent.app.arrayFloat(self.ref, data.ravel(), label)

    def colours(self, data):
        """
        Load colour data for object

        Parameters
        ----------
        data : str or list or array
            Pass a list or numpy uint32 array of colours
            if a string or list of strings is provided, colours are parsed as html colour string values
            if a numpy array is passed, colours are loaded as 4 byte ARGB unsigned integer values
        """
        if isinstance(data, numpy.ndarray):
            if data.dtype != numpy.uint32:
                return self.rgba(data)
            self._loadScalar(data, LavaVuPython.lucRGBAData)
            return
        #Convert to list of strings
        if isinstance(data, str):
            data = data.split()
        if len(data) < 1: return
        #Load as string array or unsigned int array
        if isinstance(data[0], list):
            #Convert to strings for json parsing first
            data = [str(i) for i in data]
        if isinstance(data[0], str):
            #Each element will be parsed as a colour string
            self.parent.app.loadColours(self.ref, data)
        else:
            #Plain list, assume unsigned colour data, either 4*uint8 or 1*uint32 per rgba colour
            data = numpy.asarray(data, dtype=numpy.uint32)
            self.colours(data)

    def indices(self, data, offset=0):
        """
        Load index data for object

        Parameters
        ----------
        data : list or array
            Pass a list or numpy uint32 array of indices
            indices are loaded as 32 bit unsigned integer values
        offset : int
            Specify an initial index offset, for 1-based indices pass offset=1
            Default is zero-based
        """

        #Accepts only uint32 indices
        data = self._convert(data, numpy.uint32)
        if offset > 0:
            #Convert indices to offset 0 before loading by subtracting offset
            data = numpy.subtract(data, offset)
        #Load indices
        self._loadScalar(data, LavaVuPython.lucIndexData)

    def rgb(self, data):
        """
        Load rgb data for object

        Parameters
        ----------
        data : list or array
            Pass a list or numpy uint8 array of rgb values
            values are loaded as 8 bit unsigned integer values
        """

        #Accepts only uint8 rgb triples
        data = self._convert(data, numpy.uint8)

        #Detection of split r,g,b arrays from shape
        #If data provided as separate r,g,b columns, re-arrange (Must be > 3 elements to detect correctly)
        shape = data.shape
        if len(shape) >= 2 and shape[-1] > 3 and shape[0] == 3:
            #Re-arrange to array of [r,g,b] triples
            data = numpy.vstack((data[0],data[1],data[2])).reshape([3, -1]).transpose()

        self._loadScalar(data, LavaVuPython.lucRGBData)

    def rgba(self, data):
        """
        Load rgba data for object

        Parameters
        ----------
        data : list or array
            Pass a list or numpy uint8 array of rgba values
            values are loaded as 8 bit unsigned integer values
        """

        #Accepts only uint8 rgba
        data = self._convert(data, numpy.uint8)

        #Detection of split r,g,b arrays from shape
        #If data provided as separate r,g,b,a columns, re-arrange (Must be > 4 elements to detect correctly)
        shape = data.shape
        if len(shape) >= 2 and shape[-1] > 4 and shape[0] == 4:
            #Re-arrange to array of [r,g,b,a] values
            data = numpy.vstack((data[0],data[1],data[2],data[3])).reshape([4, -1]).transpose()

        self._loadScalar(data, LavaVuPython.lucRGBAData)


    def luminance(self, data):
        """
        Load luminance data for object

        Parameters
        ----------
        data : list or array
            Pass a list or numpy uint8 array of luminance values
            values are loaded as 8 bit unsigned integers
        """

        #Accepts only uint8 luminance values
        data = self._convert(data, numpy.uint8)
        self._loadScalar(data, LavaVuPython.lucLuminanceData)

    def texture(self, data, width, height, channels=4, flip=True, mipmaps=True, bgr=False):
        """
        Load raw texture data for object

        Parameters
        ----------
        data : list or array
            Pass a list or numpy uint32 or uint8 array
            texture data is loaded as raw image data
        width : int
            image width in pixels
        height : int
            image height in pixels
        channels : int
            colour channels/depth in bytes (1=luminance, 3=RGB, 4=RGBA)
        flip : boolean
            flip the texture vertically after loading
            (default is enabled as usually required for OpenGL but can be disabled)
        mipmaps : boolean
            generate mipmaps (slow)
        bgr : boolean
            rgb data is in BGR/BGRA format instead of RGB/RGBA
        """
        if not isinstance(data, numpy.ndarray):
            data = self._convert(data, numpy.uint32)
        if data.dtype == numpy.uint32:
            self.parent.app.textureUInt(self.ref, data.ravel(), width, height, channels, flip, mipmaps, bgr)
        elif data.dtype == numpy.uint8:
            self.parent.app.textureUChar(self.ref, data.ravel(), width, height, channels, flip, mipmaps, bgr)

    def labels(self, data):
        """
        Load label data for object

        Parameters
        ----------
        data : list or str
            Pass a label or list of labels to be applied, one per vertex
        """
        if isinstance(data, str):
            data = [data]
        self.parent.app.loadLabels(self.ref, data)

    def colourmap(self, data=None, reverse=False, monochrome=False, **kwargs):
        """
        Load colour map data for object

        Parameters
        ----------
        data : list or str or ColourMap
            If not provided, just returns the colourmap
            (A default is created if none exists)
            Provided colourmap data can be
            - a string,
            - list of colour strings,
            - list of position,value tuples
            - a built in colourmap name
            - An existing ColourMap object
            Creates a colourmap named objectname_colourmap if object
            doesn't already have a colourmap
        reverse : boolean
            Reverse the order of the colours after loading
        monochrome : boolean
            Convert to greyscale

        Returns
        -------
        ColourMap(dict)
            The wrapper object of the colourmap loaded/created
        """
        cmap = None
        if data is None:
            cmid = self["colourmap"]
            if cmid:
                #Just return the existing map
                return ColourMap(cmid, self.parent)
            else:
                #Proceeed to create a new map with default data
                data = cubeHelix()
        elif isinstance(data, ColourMap):
            #Passed a colourmap object
            cmap = data
            self.ref.colourMap = data.ref
            data = None
        else:
            #Load colourmap on this object
            if self.ref.colourMap is None:
                self.ref.colourMap = self.parent.app.addColourMap(self.name + "_colourmap")
                self["colourmap"] = self.ref.colourMap.name
            cmap = ColourMap(self.ref.colourMap, self.parent)

        #Update with any passed args, colour data etc
        cmap.update(data, reverse, monochrome, **kwargs)
        return cmap

    def opacitymap(self, data=None, **kwargs):
        """
        Load opacity map data for object

        Parameters
        ----------
        data : list or str
            If not provided, just returns the opacity map
            (A default is created if none exists)
            Provided opacity map data can be
            - list of opacity values,
            - list of position,opacity tuples
            Creates an opacity map named objectname_opacitymap if object
            doesn't already have an opacity map

        Returns
        -------
        ColourMap(dict)
            The wrapper object of the opacity map loaded/created
        """
        colours = []
        if data is None:
            cmid = self["opacitymap"]
            if cmid:
                #Just return the existing map
                return ColourMap(cmid, self.parent)
            else:
                #Proceeed to create a new map with default data
                colours = ["black:0", "black"]
        #Create colour list using provided opacities
        elif isinstance(data, list) and len(data) > 1:
            if isinstance(data[0], list) or isinstance(data[0], tuple) and len(data[0]) > 1:
                #Contains positions
                for entry in data:
                    colours.append((entry[0], "black:" + str(entry[1])))
                #Ensure first and last positions of list data are always 0 and 1
                if colours[0][0]  != 0.0: colours[0]  = (0.0, colours[0][1])
                if colours[-1][0] != 1.0: colours[-1] = (1.0, colours[-1][1])
            else:
                #Opacity only
                for entry in data:
                    colours.append("black:" + str(entry))
        else:
            print("Only list data is supported for opacity maps, length of list must be at least 2")
            return None

        #Load opacity map on this object
        ret = None
        if self.ref.opacityMap is None:
            self.ref.opacityMap = self.parent.app.addColourMap(self.name + "_opacitymap")
            self["opacitymap"] = self.ref.opacityMap.name
        c = ColourMap(self.ref.opacityMap, self.parent)
        c.update(colours, **kwargs)
        opby = self["opacityby"]
        if len(str(opby)) == 0:
            self["opacityby"] = 0 #Use first field by default
        return c
        
    def reload(self):
        """
        Fully reload the object's data, recalculating all parameters such as colours
        that may be cached on the GPU, required after changing some properties
        so the changes are reflected in the visualisation
        """
        self.parent.app.reloadObject(self.ref)

    def select(self):
        """
        Set this object as the selected object
        """
        self.parent.app.aobject = self.ref
    
    def file(self, *args, **kwargs):
        """
        Load data from a file into this object

        Parameters
        ----------
        filename : str
            Name of the file to load
        """
        #Load file with this object selected (import)
        self.select()
        self.parent.file(*args, obj=self, **kwargs)
        self.parent.app.aobject = None

    def files(self, *args, **kwargs):
        """
        Load data from a series of files into this object (using wildcards or a list)

        Parameters
        ----------
        files : str
            Specification of the files to load
        """
        #Load file with this object selected (import)
        self.select()
        self.parent.files(*args, obj=self, **kwargs)
        self.parent.app.aobject = None

    def colourbar(self, **kwargs):
        """
        Create a new colourbar using this object's colourmap

        Returns
        -------
        colourbar : Object
            The colourbar object created
        """
        #Create a new colourbar for this object
        return self.parent.colourbar(self, **kwargs)

    def clear(self):
        """
        Clear all visualisation data from this object
        """
        self.parent.app.clearObject(self.ref)

    def cleardata(self, typename=""):
        """
        Clear specific visualisation data/values from this object

        Parameters
        ----------
        typename : str
            Optional filter naming type of data to be cleared,
            Either a built in type: (vertices/normals/vectors/indices/colours/texcoords/luminance/rgb/values)
            or a user defined data label
        """
        if typename in datatypes:
            #Found data type name
            dtype = datatypes[typename]
            self.parent.app.clearData(self.ref, dtype)
        else:
            #Assume values by label (or all values if blank)
            self.parent.app.clearValues(self.ref, typename)

    def update(self, filter=None, compress=True):
        """
        Write the objects's visualisation data back to the database

        Parameters
        ----------
        filter : str
            Optional filter to type of geometry to be updated, if omitted all will be written
            (eg: labels, points, grid, triangles, vectors, tracers, lines, shapes, volume)
        compress : boolean
            Use zlib compression when writing the geometry data
        """
        #Update object data at current timestep
        if filter is None:
            #Re-writes all data to db for this object
            self.parent.app.update(self.ref, compress)
        else:
            #Re-writes data to db for this object and geom type
            self.parent.app.update(self.ref, self.parent._getRendererType(filter), compress)

    def getcolourmap(self, string=True):
        """
        Return the colour map data from the object as a string or list
        Either return format can be used to create/modify a colourmap
        with colourmap()

        Parameters
        ----------
        string : boolean
            The default is to return the data as a string of colours separated by semi-colons
            To instead return a list of (position,[R,G,B,A]) tuples for easier automated processing in python,
            set this to False

        Returns
        -------
        mapdata : str/list
            The formatted colourmap data
        """
        cmid = self["colourmap"]
        return self.parent.getcolourmap(cmid, string)

    def isosurface(self, isovalues=None, name=None, convert=False, updatedb=False, compress=True, **kwargs):
        """
        Generate an isosurface from a volume data set using the marching cubes algorithm

        Parameters
        ----------
        isovalues : number,list
            Isovalues to create surfaces for, number or list
        name : str
            Name of the created object, automatically assigned if not provided
        convert : bool
            Setting this flag to True will replace the existing volume object with the
            newly created isosurface by deleting the volume data and loading the mesh
            data into the preexisting object
        updatedb : bool
            Setting this flag to True will write the newly created/modified data
            to the database when done
        compress : boolean
            Use zlib compression when writing the geometry data
        **kwargs :
            Initial set of properties passed to the created object

        Returns
        -------
        obj : Object
            The isosurface object created/converted
        """
        #Generate and return an isosurface object, 
        #pass properties as kwargs (eg: isovalues=[])
        if isovalues is not None:
            kwargs["isovalues"] = isovalues

        #Create surface, If requested, write the new data to the database
        objref = None
        if convert: objref = self.ref
        ref = self.parent.isosurface(objref, self.ref, _convert_args(kwargs), convert)

        #Get the created/updated object
        if ref == None:
            print("Error creating isosurface")
            return ref
        isobj = self.parent.Object(ref)

        #Re-write modified types to the database
        if updatedb:
            self.parent.app.update(isobj.ref, LavaVuPython.lucVolumeType, compress)
            self.parent.app.update(isobj.ref, LavaVuPython.lucTriangleType, compress)
        return isobj

    def help(self, cmd=""):
        """
        Get help on an object method or property

        Parameters
        ----------
        cmd : str
            Command to get help with, if ommitted displays general introductory help
            If cmd is a property or is preceded with '@' will display property help
        """
        self.parent.help(cmd, self)

    def boundingbox(self, allsteps=False):
        bb = self.parent.app.getBoundingBox(self.ref, allsteps)
        return [[bb[0], bb[1], bb[2]], [bb[3], bb[4], bb[5]]]

#Wrapper dict+list of objects
class _Objects(dict):
    """  
    The Objects class is used internally to manage and synchronise the drawing object list
    """
    def __init__(self, parent):
        self._parent = weakref.ref(parent)

    @property
    def parent(self):
        return self._parent()

    def _sync(self):
        #Sync the object list with the viewer
        self.list = []
        #Loop through retrieved object list
        for obj in self.parent.state["objects"]:
            #Exists in our own list?
            if obj["name"] in self:
                #Update object with new properties
                self[obj["name"]]._setprops(obj)
                self.list.append(self[obj["name"]])
            else:
                #Create a new object wrapper
                o = Object(self.parent, **obj)
                self[obj["name"]] = o
                self.list.append(o)
            #Flag sync
            self[obj["name"]].found = True
            #Save the object id and reference (use id # to get)
            _id = len(self.list)
            self.list[-1].id = _id
            self.list[-1].ref = self.parent.app.getObject(_id)
            
        #Delete any objects from stored dict that are no longer present
        for name in list(self):
            if not self[name].found:
                del self[name]
            else:
                self[name].found = False

    def __repr__(self):
        rep = '{\n'
        for key in self.keys():
            rep += '  "' + key + '": {},\n'
        rep += '}\n'
        return rep

    def __str__(self):
        return str(self.keys())

class _ColourComponents():
    """Class to allow modifying colour components directly as an array
    """
    def __init__(self, key, parent):
        self.parent = parent
        self.key = key
        self.list = self.parent.list[self.key][1]

    def __getitem__(self, key):
        self.list = self.parent.list[self.key][1]
        return self.list[key]

    def __setitem__(self, key, value):
        self.list = self.parent.list[self.key][1]
        self.list[key] = value
        self.parent[self.key] = self.list

    def __str__(self):
        return str(self.list)

class _ColourList():
    """Class to allow modifying colour list directly as an array
    """
    def __init__(self, parent):
        self.parent = parent
        self.list = self.parent.tolist()

    def __getitem__(self, key):
        self.parent._get() #Ensure in sync
        self.list = self.parent.tolist()
        return _ColourComponents(key, self)

    def __setitem__(self, key, value):
        self.list = self.parent.tolist()
        self.list[key] = (self.list[key][0], value)
        self.parent.update(self.list)

    def __delitem__(self, key):
        self.list = self.parent.tolist()
        del self.list[key]
        self.parent.update(self.list)

    def __iadd__(self, value):
        self.append(value)

    def __add__(self, value):
        self.append(value)

    def append(self, value, position=1.0):
        self.list = self.parent.tolist()
        if isinstance(value, tuple):
            self.list.append(value)
        else:
            self.list.append((position, value))
        self.parent.update(self.list)

    def __str__(self):
        return str([c[1] for c in self.list])

class _PositionList(_ColourList):
    """Class to allow modifying position list directly as an array
    """
    def __init__(self, parent):
        self.parent = parent
        self.list = self.parent.tolist()

    def __getitem__(self, key):
        self.parent._get() #Ensure in sync
        self.list = self.parent.tolist()
        return self.list[key][0]

    def __setitem__(self, key, value):
        self.list = self.parent.tolist()
        self.list[key] = (value, self.list[key][1])
        self.parent.update(self.list)

    def __str__(self):
        return str([c[0] for c in self.list])

#Wrapper class for colourmap
#handles property updating via internal dict
class ColourMap(dict):
    """
    The ColourMap class provides an interface to a LavaVu ColourMap
    ColourMap instances are created internally in the Viewer class and can
    be retrieved from the colourmaps list

    New colourmaps are also created using viewer methods

    Parameters
    ----------
    **kwargs
        Initial set of properties passed to the created colourmap

    """
    def __init__(self, ref, parent, *args, **kwargs):
        self._parent = weakref.ref(parent)
        if isinstance(ref, LavaVuPython.ColourMap):
            self.ref = ref
        else:
            self.ref = self.parent.app.getColourMap(ref)

        self.dict = kwargs
        self._get() #Sync

        #Init prop dict for tab completion
        super(ColourMap, self).__init__(**self.parent.properties)

    @property
    def parent(self):
        return self._parent()

    @property
    def name(self):
        """
        Get the colourmap name property

        Returns
        -------
        name : str
            The name of the colourmap
        """
        return self.ref.name

    @property
    def colours(self):
        """
        Returns the list of colours

        Returns
        -------
        colours : list
            A list of colours
         """
        self._get()
        return _ColourList(self)

    @colours.setter
    def colours(self, value):
        #Dummy setter to allow +/+= on colours list
        pass

    @property
    def positions(self):
        """
        Returns the list of colour positions

        Returns
        -------
        positions : list
            A list of colour positions [0,1]
         """
        self._get()
        return _PositionList(self)

    def _set(self):
        #Send updated props (via ref in case name changed)
        self.parent.app.setColourMap(self.ref, _convert_args(self.dict))

    def _get(self):
        self.parent._get() #Ensure in sync
        #Update prop dict
        for cm in self.parent.state["colourmaps"]:
            if cm["name"] == self.ref.name:
                #self.colours = cm["colours"]
                self.dict.update(cm)
                #self.dict.pop("colours", None)
                #print self.dict

    def __getitem__(self, key):
        self._get() #Ensure in sync
        if not key in self.parent.properties:
            raise ValueError(key + " : Invalid property name")
        if key in self.dict:
            return self.dict[key]
        #Default to the property lookup dict (default is first element)
        prop = super(ColourMap, self).__getitem__(key)
        #Must always return a copy to prevent modifying the defaults!
        return copy.copy(prop["default"])

    def __setitem__(self, key, value):
        if not key in self.parent.properties:
            raise ValueError(key + " : Invalid property name")
        #Set new value and send
        self.dict[key] = value
        self._set()

    def __contains__(self, key):
        return key in self.dict

    def tolist(self):
        """
        Get the colourmap data as a python list

        Returns
        -------
        list
            The colour and position data which can be used to re-create the colourmap
        """
        arr = []
        for c in self["colours"]:
            comp = re.findall(r"[\d\.]+", c["colour"])
            comp = [int(comp[0]), int(comp[1]), int(comp[2]), int(255*float(comp[3]))]
            arr.append((c["position"], comp))
        return arr

    def tohexstr(self):
        """
        Get the colourmap colour data as a string with hex rgb:a representation,
        NOTE: ignores position data

        Returns
        -------
        str
            The colour data which can be used to re-create the colourmap
        """
        def padhex2(i):
            s = hex(int(i))
            return s[2:].zfill(2)
        string = ""
        for c in self["colours"]:
            comp = re.findall(r"[\d\.]+", c["colour"])
            string += "#" + padhex2(comp[0]) + padhex2(comp[1]) + padhex2(comp[2])
            if float(comp[3]) < 1.0:
                string += ":" + str(comp[3])
            string += " "
        return string

    def __repr__(self):
        return self.__str__().replace(';', '\n')

    def __str__(self):
        #Default string representation
        cmstr = '"""'
        for c in self["colours"]:
            cmstr += "%6.4f=%s; " % (c["position"],c["colour"])
        cmstr += '"""\n'
        return cmstr

    def update(self, data=None, reverse=False, monochrome=False, **kwargs):
        """
        Update the colour map data

        Parameters
        ----------
        data : list,str
            Provided colourmap data can be
            - a string,
            - list of colour strings,
            - list of position,value tuples
            - or a built in colourmap name
        reverse : boolean
            Reverse the order of the colours after loading
        monochrome : boolean
            Convert to greyscale
        """
        if data is not None:
            if isinstance(data, str) and re.match('^[\w_]+$', data) is not None:
                #Single word of alphanumeric characters, if not a built-in map, try matplotlib
                if data not in self.parent.defaultcolourmaps():
                    newdata = matplotlib_colourmap(data)
                    if len(newdata) > 0:
                        data = newdata
            if not isinstance(data, str):
                data = json.dumps(data)

            #Load colourmap data
            self.parent.app.updateColourMap(self.ref, data, _convert_args(kwargs))

        if reverse:
            self.ref.flip()
        if monochrome:
            self.ref.monochrome()
        self._get() #Ensure in sync

class Figure(dict):
    """  
    The Figure class wraps a set of visualisation state data, providing a way
    of managing a collection of preset visualisations or "figures" of a single model

    - Figures represent a full set of visualisation settings,
      including visibility of chosen objects
    - A single model can contain many objects and multiple figures, all of which work
      on the same set of objects, but may not use them all (ie: some are hidden)
    - A figure object encapsulates the same data that can be stored on disk in a JSON file with
      Viewer.store(filename) and restored with Viewer.restore(filename)
    """
    def __init__(self, parent, name):
        self._parent = weakref.ref(parent)
        self.name = name
        #Init prop dict for tab completion
        super(Figure, self).__init__(**self.parent.properties)

    @property
    def parent(self):
        return self._parent()

    def __getitem__(self, key):
        if not key in self.parent.properties:
            raise ValueError(key + " : Invalid property name")
        #Activate this figure on viewer
        self.load()
        #Return key on viewer instance
        if key in self.parent:
            return self.parent[key]
        #Default to the property lookup dict (default is first element)
        prop = super(Figure, self).__getitem__(key)
        #Must always return a copy to prevent modifying the defaults!
        return copy.copy(prop["default"])

    def __setitem__(self, key, value):
        if not key in self.parent.properties:
            raise ValueError(key + " : Invalid property name")
        #Activate this figure on viewer
        self.load()
        #Set new value
        self.parent[key] = value
        #Save changes
        self.save()

    def __repr__(self):
        return '{"' + self.name + '"}'

    def __str__(self):
        return self.name

    def load(self):
        """
        Load this figure's state into the Viewer
        """
        #Activate this figure on viewer
        self.parent.figure(self.name)

    def save(self):
        """
        Save the Viewer state to this figure
        """
        #Save changes
        self.parent.savefigure(self.name)

    def show(self, *args, **kwargs):
        """
        Render this figure

        - Load the figure state into the Viewer,
        - Call Viewer.display(args, kwargs) to render
        """
        #Activate this figure on viewer
        self.load()
        #Render
        self.parent.display(*args, **kwargs)

    def image(self, *args, **kwargs):
        """
        Render this figure to an image file:

        - Load the figure state into the Viewer,
        - Call Viewer.image(args, kwargs) to render an image to file
        """
        #Activate this figure on viewer
        self.load()
        #Render
        return self.parent.image(*args, **kwargs)


class _LavaVuThreadSafe(LavaVuPython.LavaVu):
    def __init__(self, threaded=True, *args, **kwargs):
        self._threaded = threaded
        self._closing = False

        if threaded:
            # Create a condition variable to synchronize resource access
            self._cv = threading.Condition()

            # Create the command queue
            from collections import deque
            self._q = deque()

            #Safe call return value
            self._returned = None

        super(_LavaVuThreadSafe, self).__init__(*args, **kwargs)

    #def __getattr__(self, attr):
    #    #Lock?
    #    return self.app[attr]

    #def __setattr__(self, attr, value):
    #    #Lock?
    #    self.app[attr] = value

    ####################################

    """
    These functions must be called on the render thread only
    as they make OpenGL calls
    """
    def saferun(self, *args, **kwargs):
        return self._lavavu_call('run', True, *args, **kwargs)

    def close(self, *args, **kwargs):
        return self._lavavu_call('close', True, *args, **kwargs)

    def image(self, *args, **kwargs):
        return self._lavavu_call('image', True, *args, **kwargs)

    def imageJPEG(self, *args, **kwargs):
        return self._lavavu_call('imageJPEG', True, *args, **kwargs)

    def imagePNG(self, *args, **kwargs):
        return self._lavavu_call('imagePNG', True, *args, **kwargs)

    def video(self, *args, **kwargs):
        return self._lavavu_call('video', True, *args, **kwargs)

    def web(self, *args, **kwargs):
        return self._lavavu_call('web', True, *args, **kwargs)

    def isoSurface(self, *args, **kwargs):
        return self._lavavu_call('isoSurface', True, *args, **kwargs)

    #def safegetstate(self, *args, **kwargs):
    #    return self._lavavu_call('getState', True, *args, **kwargs)

    #def setState(self, *args, **kwargs):
    #    return self._lavavu_call('setState', True, *args, **kwargs)

    def commands(self, *args, **kwargs):
        #Parse commands and wait until they are processed
        return self._lavavu_call('parseCommands', True, *args, **kwargs)

    def qcommands(self, *args, **kwargs):
        #Queue commands for parsing and return immediately to continue processing
        self._lavavu_call('parseCommands', False, *args, **kwargs)

    def addTimeStep(self, *args, **kwargs):
        return self._lavavu_call('addTimeStep', True, *args, **kwargs)

    def imageDiff(self, *args, **kwargs):
        return self._lavavu_call('imageDiff', True, *args, **kwargs)

    def loadFile(self, *args, **kwargs):
        return self._lavavu_call('loadFile', True, *args, **kwargs)

    def updateColourMap(self, *args, **kwargs):
        return self._lavavu_call('updateColourMap', True, *args, **kwargs)

    def gl_version(self, *args, **kwargs):
        return self._lavavu_call('gl_version', True, *args, **kwargs)

    """
    #def loadColours(self, *args, **kwargs):
    #    #print("COLOURS")
    #    return self._lavavu_call('loadColours', True, *args, **kwargs)

    def arrayFloat(self, *args, **kwargs):
        return self._lavavu_call('arrayFloat', True, *args, **kwargs)
        #self._lavavu_call('arrayFloat', False, *args, **kwargs)

    def arrayUInt(self, *args, **kwargs):
        return self._lavavu_call('arrayUInt', True, *args, **kwargs)
        #self._lavavu_call('arrayUInt', False, *args, **kwargs)

    def arrayUChar(self, *args, **kwargs):
        return self._lavavu_call('arrayUChar', True, *args, **kwargs)
        #self._lavavu_call('arrayUChar', False, *args, **kwargs)

    def clearData(self, *args, **kwargs):
        return self._lavavu_call('clearData', True, *args, **kwargs)

    def clearValues(self, *args, **kwargs):
        return self._lavavu_call('clearValues', True, *args, **kwargs)
    """

    ####################################

    def display(self, *args, **kwargs):
        #Don't wait for return value
        self._openglviewer_call('display', False, *args, **kwargs)
        #return self._openglviewer_call('display', True, *args, **kwargs)

    #def events(self, *args, **kwargs):
    #    return self._openglviewer_call('events', True, *args, **kwargs)

    def show(self, *args, **kwargs):
        if not self.viewer.visible:
            self.viewer.visible = True
            #This is a bit weird/broken, it shows the window only if visible is true
            # and does not set the visible flag
            #TODO: make behaviour of viewer.show/hide consistent
            self._openglviewer_call('show', False, *args, **kwargs)

    def hide(self, *args, **kwargs):
        if self.viewer.visible:
            #Also a bit broken, needs fixing,
            #This is the opposite of show, clears visible flag
            # and hides window regardless of flag setting
            self._openglviewer_call('hide', False, *args, **kwargs)

    def events(self, *args, **kwargs):
        self.viewer.nodisplay = True #Handle rendering ourselves
        return self._openglviewer_call('events', True, *args, **kwargs)
        #self._openglviewer_call('events', False, *args, **kwargs)

        #self._openglviewer_call('execute', False, *args, **kwargs)
        #Note: no longer calls show() if not visible, need to do manually
        return not self.viewer.quitProgram

    def execute(self, *args, **kwargs):
        #self._openglviewer_call('execute', False, *args, **kwargs)
        return self._openglviewer_call('execute', True, *args, **kwargs)

    ####################################

    #Call LavaVu method from render thread
    def _lavavu_call(self, name, wait_return, *args, **kwargs):
        method = getattr(super(_LavaVuThreadSafe, self), name)
        return self._thread_call(method, wait_return, *args, **kwargs)

    #Call OpenGLViewer method from render thread
    def _openglviewer_call(self, name, wait_return, *args, **kwargs):
        return self._thread_call(getattr(self.viewer, name), wait_return, *args, **kwargs)

    def _thread_call(self, method, wait_return, *args, **kwargs):
        if not self._threaded:
            return method(*args, **kwargs)
        """
        This calls a method on the render thread
        All args are placed on the queue, along with the method

        if wait_return is True:
          Wait for the call to be executed with a condition variable lock
          Returns the saved return data from render thread after woken
        Otherwise:
          Return immediately
        """
        #Use the thread queue to pass input args
        self._q.append([method, wait_return, args, kwargs])
        #print("THREAD_CALL:",method.__name__,args,kwargs)
        if wait_return:
            #Wait until the call is completed in render thread
            with self._cv:
                self._cv.wait()
            #Return the saved result data
            return self._returned

    def _thread_run(self):
        """
        This function manages the render thread.
        Used to: handle events, get images
        All OpenGL calls must be made from here
        """
        #self._kwargs["usequeue"] = True #Switch on command queuing

        #Render event handling loop!
        while not self._closing:
            #Process interactive and timer events
            if self.viewer.events():
                self.viewer.execute()

            #Process commands that must be run on the render thread
            if len(self._q):
                #if not self.app.viewer.isopen or not self.app.amodel:
                #    print("NOT OPEN!")
                #    print('deferring : ' + self.app._q[0])
                method, wait_return, args, kwargs = self._q.popleft()
                #If set, must return result and notify waiting thread with condition variable
                if wait_return:
                    #print("CALLING:",method.__name__)
                    self._returned = method(*args, **kwargs)
                    #Notify waiting thread result is ready
                    with self._cv:
                        self._cv.notify()
                    #print("RETURNED:",type(self._returned))
                else:
                    method(*args, **kwargs)
                method = None

            time.sleep(TIMER_INC)

            #Detect window closed
            if self.viewer.quitProgram:
                if is_notebook():
                    #Just hide the window
                    self.viewer.hide()
                    self.viewer.quitProgram = False


class Viewer(dict):
    """  
    The Viewer class provides an interface to a LavaVu session
    
    Parameters
    ----------
    arglist : list
        list of additional init arguments to pass
    database : str
        initial database (or model) file to load
    figure : int
        initial figure id to display
    timestep : int
        initial timestep to display
    verbose : boolean
        verbose output to command line for debugging
    interactive : boolean
        begin in interactive mode, opens gui window and passes control to event loop immediately
    hidden : boolean
        begin hidden, for offscreen rendering or web browser control
    cache : boolean
        cache all model timesteps in loaded database, everything loaded into memory on startup
        (assumes enough memory is available)
    quality : int
        Render sampling quality, render 2^N times larger image and downsample output
        For anti-aliasing image rendering where GPU multisample anti-aliasing is not available
    writeimage : boolean
        Write images and quit, create images for all figures/timesteps in loaded database then exit
    resolution : list, tuple
        Window/image resolution in pixels [x,y]
    script : list
        List of script commands to run after initialising
    initscript : boolean
        Set to False to disable loading any "init.script" file found in current directory
    usequeue : boolean
        Set to True to add all commands to a background queue for processing rather than
        immediate execution
    **kwargs
        Remaining keyword args will be  passed to the created viewer
        and parsed into the initial set of global properties
            
    Example
    -------
        
    Create a viewer, setting the initial background colour to white
    
    >>> import lavavu
    >>> lv = lavavu.Viewer(background="white")

    Objects can be added by loading files:
    #>>> lavavu.download(source + 'Mandible.obj') # doctest: +ELLIPSIS

    >>> import lavavu
    >>> obj = lv.file('model.obj') # doctest: +SKIP

    Or creating empty objects and loading data:

    >>> obj = lv.points('mypoints')
    >>> obj.vertices([[0,0,0], [1,1,1]])

    Viewer commands can be called as methods on the viewer object:

    >>> lv.rotate('x', 45)

    Viewer properties can be set by using it like a dictionary:

    >>> lv["background"] = "grey50"

    A list of available commands and properties can be found in the docs

     - https://mivp.github.io/LavaVu-Documentation/Scripting-Commands-Reference
     - https://mivp.github.io/LavaVu-Documentation/Property-Reference

    or by using the online help:

    >>> lv.help('rotate') # doctest: +SKIP
    >>> lv.help('opacity') # doctest: +SKIP
    (...)

    """

    def __init__(self, binpath=None, havecontext=False, omegalib=False, port=8080, *args, **kwargs):
        """
        Create and init viewer instance

        Parameters
        ----------
        (see Viewer class docs for setup args)
        port : int
            Web server port, open server on specific port for control/interaction
            Viewer will be run in a separate thread, all rendering will be done in this thread
            When disabled (None) creates the viewer in the current(main) thread and disables the server
        binpath : str
            Override the executable path
        havecontext : boolean
            OpenGL context provided by user, set this if you have already setup the context
        omegalib : boolean
            For use in VR mode, disables some conflicting functionality
            and parsed into the initial set of global properties
        """
        self.resolution = (640,480)
        self._ctr = 0
        self.app = None
        self._objects = _Objects(self)
        self.state = {}
        self._managed = False
        self.server = None
        self._thread = None
        self._collections = {}

        #Launch in thread?
        #(Can disable by setting port=0)
        if port > 0:
            #Exit handler to clean up threads
            #(__del__ does not always seem to get called on termination)
            def exitfn(vref):
                #Check if the viewer reference is still valid
                viewer = vref()
                if viewer:
                    viewer._shutdown()
            import atexit
            atexit.register(exitfn, weakref.ref(self))

            self._cv = threading.Condition()
            #self.app = _LavaVuThreadSafe(binpath, havecontext, omegalib)
            def _thread_run(viewer, args, kwargs):
                """
                This function runs the render thread.
                Used to: create the viewer, handle events, get images
                All OpenGL calls must be made from here
                """
                #Create the viewer
                viewer._create(True, binpath, havecontext, omegalib, *args, **kwargs)

                #Sync with main thread here to ensure render thread has initialised before it continues
                with viewer._cv:
                    viewer._cv.notifyAll()

                #Handle events
                viewer.app._thread_run()

                #Closedown/delete must be called from thread to free OpenGL resources!
                viewer.app = None
                viewer = None
                import gc
                gc.collect()

            #Thread start
            self._thread = threading.Thread(target=_thread_run, args=[self, args, kwargs])
            #Due to python failing to call __del__ on exit, have to use daemon or thread never quits
            self._thread.daemon = True

            #Start the thread and wait for it to finish initialising
            with self._cv:
                self._thread.start()
                self._cv.wait()

            #Start the web server
            import server
            self.server = server.serve(self, port, ipv6=True) #ipv6 flag pass through?
        else:
            self._create(False, binpath, havecontext, omegalib, *args, **kwargs)

    def _create(self, threaded, binpath=None, havecontext=False, omegalib=False, *args, **kwargs):
        """
        Create and init the C++ viewer object
        """
        try:
            #Get the binary path if not provided
            if binpath is None:
                binpath = os.path.abspath(os.path.dirname(__file__))

            self.app = _LavaVuThreadSafe(threaded, binpath, havecontext, omegalib)

            #Get property dict
            self.properties = _convert_keys(json.loads(self.app.propertyList()))
            #Init prop dict for tab completion
            super(Viewer, self).__init__(**self.properties)

            self.setup(safe=False, *args, **kwargs)

            #Control setup, expect html files in same path as viewer binary
            control.htmlpath = self.htmlpath = os.path.join(self.app.binpath, "html")
            control.dictionary = self.app.propertyList()

            if not os.path.isdir(control.htmlpath):
                control.htmlpath = self.htmlpath = None
                print("Can't locate html dir, interactive view disabled")

            #Create a control factory
            self.control = control._ControlFactory(self)

            #List of inline WebGL viewers
            self.webglviews = []

            #Get available commands
            self._cmdcategories = self.app.commandList()
            self._cmds = {}
            self._allcmds = []
            for c in self._cmdcategories:
                self._cmds[c] = self.app.commandList(c)
                self._allcmds += self._cmds[c]

            #Create command methods
            selfdir = dir(self)  #Functions on Viewer
            for key in self._allcmds:
                #Check if a method exists already
                if key in selfdir:
                    existing = getattr(self, key, None)
                    if existing and callable(existing):
                        #Add the lavavu doc entry to the docstring
                        doc = ""
                        if existing.__doc__:
                            if "Wraps LavaVu" in existing.__doc__: continue #Already modified
                            doc += existing.__doc__ + '\n----\nWraps LavaVu script command of the same name:\n > **' + key + '**:\n'
                        doc += self.app.helpCommand(key, False)
                        #These should all be wrapper for the matching lavavu commands
                        #(Need to ensure we don't add methods that clash)
                        existing.__func__.__doc__ = doc
                else:
                    #Use a closure to define a new method that runs this command
                    def cmdmethod(name):
                        _target = weakref.ref(self) #Use a weak ref in the closure
                        def method(*args, **kwargs):
                            arglist = [name]
                            for a in args:
                                if isinstance(a, (tuple, list)):
                                    arglist += [str(b) for b in a]
                                else:
                                    arglist.append(str(a))
                            _target().commands(' '.join(arglist))
                        return method

                    #Create method that runs this command:
                    method = cmdmethod(key)

                    #Set docstring
                    method.__doc__ = self.app.helpCommand(key, False)
                    #Add the new method
                    self.__setattr__(key, method)

            #Add module functions to Viewer object
            mod = sys.modules[__name__]
            import inspect
            for name in dir(mod):
                element = getattr(mod, name)
                if callable(element) and name[0] != '_' and not inspect.isclass(element):
                    #Add the new method
                    self.__setattr__(name, element)

            #Add object by geom type shortcut methods
            #(allows calling add by geometry type, e.g. obj = lavavu.lines())
            self.renderers = self.properties["renderers"]["default"]
            for key in [item for sublist in self.renderers for item in sublist]:
                #Use a closure to define a new method to call addtype with this type
                def addmethod(name):
                    _target = weakref.ref(self) #Use a weak ref in the closure
                    def method(*args, **kwargs):
                        return _target()._addtype(name, *args, **kwargs)
                    return method
                method = addmethod(key)
                #Set docstring
                method.__doc__ = "Add a " + key + " visualisation object,\nany data loaded into the object will be plotted as " + key
                self.__setattr__(key, method)

            #Switch the default background to white if in a browser notebook
            if is_notebook() and not "background" in self:
                self["background"] = "white"

        except (RuntimeError) as e:
            print("LavaVu Init error: " + str(e))
            pass

    def _shutdown(self):
        #Wait for the render thread to exit
        if self.port and self._thread:
            #print("---SHUTDOWN-THREAD")
            self.app._closing = True
            self._thread.join()
            self._thread = None
        #Wait for server thread to exit
        if self.server:
            #print("---SHUTDOWN-SERVER")
            self.server._closing = True
            self.server.join()
            self.server = None

    def __del__(self):
        #print("---DELETING")
        if not self._managed:
            self._shutdown()

    def __enter__(self):
        #Using context manager
        self._managed = True

    def __exit__(self):
        #Using context manager
        if self._managed:
            self._shutdown()

    def _getRendererType(self, name):
        """
        Return the type index of a given renderer label
        """
        for i in range(len(self.renderers)):
            if name in self.renderers[i]:
                return geomtypes[i]

    def setup(self, safe=True, arglist=None, database=None, figure=None, timestep=None, 
         verbose=False, interactive=False, hidden=True, cache=False, quality=3,
         writeimage=False, resolution=None, script=None, initscript=False, usequeue=False, **kwargs):
        """
        Execute the viewer, initialising with provided arguments and
        entering event loop if requested

        Parameters: see __init__ docs

        """
        #Convert options to args
        args = settings["default_args"][:]
        if not initscript:
          args += ["-S"]
        if verbose:
          args += ["-v"]
        #Automation: scripted mode, no interaction
        if not interactive:
          args += ["-a"]
        #Hidden window
        if hidden:
          args += ["-h"]
        #Timestep cache
        if cache:
          args += ["-c1"]
        #Subsample anti-aliasing for image output
        if settings["quality_override"]:
            #Override provided setting with global setting
            quality = settings["quality_override"]
        args += ["-z" + str(quality)]
        #Timestep range
        if timestep != None:
            if isinstance(timestep, int):
                args += ["-" + str(timestep)]
            if isinstance(timestep, (tuple, list)) and len(timestep) > 1:
                args += ["-" + str(timestep[0]), "-" + str(timestep[1])]
        #Database file
        if database:
          args += [database]
        #Initial figure
        if figure != None:
          args += ["-f" + str(figure)]
        #Resolution
        if resolution != None and isinstance(resolution,tuple) or isinstance(resolution,list):
          #Output res
          #args += ["-x" + str(resolution[0]) + "," + str(resolution[1])]
          #Interactive res
          args += ["-r" + str(resolution[0]) + "," + str(resolution[1])]
          self.resolution = resolution
        #Save image and quit
        if writeimage:
          args += ["-I"]
        if script and isinstance(script,list):
          args += script
        if arglist:
            if isinstance(arglist, list):
                args += arglist
            else:
                args += [str(arglist)]
        self.queue = usequeue

        #Additional keyword args as property settings
        for key in kwargs:
            if isinstance(kwargs[key], str):
                args += [key + '="' + kwargs[key] + '"']
            else:
                args += [key + '=' + json.dumps(kwargs[key])]

        if verbose:
            print("ARGS:",args)

        try:
            #Need to call thread safe version if not in render thread
            if safe:
                self.app.saferun(args)
            else:
                self.app.run(args)
            #Load objects/state
            if database:
                self._get()
        except (RuntimeError) as e:
            print("LavaVu Run error: " + str(e))
            pass



    #dict methods
    def __getitem__(self, key):
        #Get view/global property
        self._get()
        view = self.state["views"][0]
        if key in view:
            return view[key]
        elif key in self.state:
            return self.state[key]
        elif key in self.state["properties"]:
            return self.state["properties"][key]
        elif key in self.properties:
            #Must always return a copy to prevent modifying the defaults!
            return copy.copy(self.properties[key]["default"]) #Default from prop list
        else:
            raise ValueError(key + " : Invalid property name")
        return None

    def __setitem__(self, key, item):
        #Set view/global property
        if not key in self.properties:
            raise ValueError(key + " : Invalid property name")
        self.app.parseProperty(key + '=' + json.dumps(item))
        self._get()

    def __contains__(self, key):
        return key in self.state or key in self.state["properties"] or key in self.state["views"][0]

    def __repr__(self):
        self._get()
        #return '{"' + self.state["properties"]["caption"] + '"}'
        return '{}'

    def __eq__(self, other):
        #Necessary because being forced to inherit from dict to support buggy IPython key completion
        #means we get dict equality, which we _really_ don't want
        #Two Viewer objects should never be equal unless they refer to the same object
        return id(self) == id(other)

    def __str__(self):
        #View/global props to string
        self._get()
        properties = self.state["properties"]
        properties.update(self.state["views"][0])
        return str('\n'.join(['    %s=%s' % (k,json.dumps(v)) for k,v in properties.items()]))

    @property
    def gl(self):
        """
        Return GL version string
        """
        return self.app.gl_version()

    @property
    def port(self):
        """
        HTTP server interface port

        Returns
        -------
        port : int
            Port the HTTP server is running on
            Will return 0 if server is not running
        """
        if self.server:
            return self.server.port
        else:
            return 0

    @property
    def objects(self):
        """
        Returns the active objects

        Returns
        -------
        objects : _Objects(dict)
            A dictionary wrapper containing the list of available visualisation objects
            Can be printed, iterated or accessed as a dictionary by object name
        """
        self._get()
        return self._objects

    @property
    def colourmaps(self):
        """
        Returns the list of active colourmaps

        Returns
        -------
        colourmaps : dict
            A dictionary containing the available colourmaps as ColourMap() wrapper objects
         """
        self._get()
        maps = {}
        for cm in self.state["colourmaps"]:
            maps[cm["name"]] = ColourMap(cm["name"], self)
        return maps

    @property
    def figures(self):
        """
        Retrieve the saved figures from loaded model
        Dict returned contains Figure objects which can be used to modify the figure

        Returns
        -------
        figures : dict
            A dictionary of all available figures by name
        """
        if not self.app.amodel:
            return {}
        figs = self.app.amodel.fignames
        figures = {}
        for fig in figs:
            figures[fig] = Figure(self, name=fig)
        return figures

    @property
    def steps(self):
        """
        Retrieve the time step data from loaded model

        Returns
        -------
        timesteps : list
            A list of all available time steps
        """
        return self.timesteps()

    def Figure(self, name, objects=None, **kwargs):
        """
        Create a figure

        Parameters
        ----------
        name : str
            Name of the figure
        objects : list
            List of objects or object names to include in the figure, others will be hidden

        Returns
        -------
        figure : Figure
            Figure object
        """
        #Show only objects in list
        if objects and isinstance(objects, list):
            #Hide all first
            for o in self._objects:
                self._objects[o]["visible"] = False
            #Show by name or Object
            for o in objects:
                if isinstance(o, str):
                    if o in self._objects:
                        o["visible"] = True
                else:
                    if o in self._objects.list:
                        o["visible"] = True

        #Create a new figure
        self.savefigure(name)
        #Sync list
        figs = self.figures
        #Get figure wrapper object
        fig = figs[name]
        #Additional keyword args = properties
        for key in kwargs:
            fig[key] = kwargs[key]
        #Return figure
        return fig

    @property
    def step(self):
        """    
        step : int
            Returns current timestep
        """
        return self['timestep']

    @step.setter
    def step(self, value):
        """    
        step : int
            Sets current timestep
        """
        self.timestep(value)

    def _get(self):
        #Import state from lavavu
        self.state = _convert_keys(json.loads(self.app.getState()))
        self._objects._sync()

    def _set(self):
        #Export state to lavavu
        #(include current object list state)
        #self.state["objects"] = [obj.dict for obj in self._objects.list]
        self.app.setState(json.dumps(self.state))

    def commands(self, cmds, queue=False):
        """
        Execute viewer commands
        https://mivp.github.io/LavaVu-Documentation/Scripting-Commands-Reference
        These commands can also be executed individually by calling them as methods of the viewer object

        Parameters
        ----------
        cmds : list or str
            Command(s) to execute
        """
        if not len(cmds): return
        #Split multiple entries
        if ';' in cmds:
           cmds = cmds.split(';')
        if isinstance(cmds, list):
            cmds = '\n'.join(cmds)

        #JSON state?
        if cmds[0] == '{':
            self.app.setState(cmds)
            #self.app.setState(str(cmds.decode('ascii')))
        elif queue or self.queue: #Thread safe queue requested
            self.app.queueCommands(cmds)
            #self.app.qcommands(cmds)
        else:
            self.app.commands(cmds)

    def help(self, cmd="", obj=None):
        """
        Get help on a command or property

        Parameters
        ----------
        cmd : str
            Command to get help with, if ommitted displays general introductory help
            If cmd is a property or is preceded with '@' will display property help
        """
        if obj is None: obj = self
        md = ""
        if not len(cmd):
            md += _docmd(obj.__doc__)
        elif cmd in dir(obj) and callable(getattr(obj, cmd)):
            md = '### ' + cmd + '  \n'
            md += _docmd(getattr(obj, cmd).__doc__)
        else:
            if cmd[0] != '@': cmd = '@' + cmd
            md = self.app.helpCommand(cmd)
        #Add docs search link
        if len(cmd):
            md += "\n[Search for '" + cmd + "' in documentation](https://mivp.github.io/LavaVu-Documentation/search.html?q=" + cmd + ")"
        _markdown(md)

    def __call__(self, cmds):
        """
        Run a LavaVu script

        Parameters
        ----------
        cmds : str
            String containing commands to run, separate commands with semi-colons"

        Example
        -------
        >>> import lavavu
        >>> lv = lavavu.Viewer()
        >>> lv.test()
        >>> lv('reset; translate -2')

        """
        self.commands(cmds)

    def _setupobject(self, ref=None, **kwargs):
        #Strip data keys from kwargs and put aside for loading
        datasets = {}
        cmapdata = None
        for key in list(kwargs):
            if key in ["vertices", "normals", "vectors", "colours", "indices", "values", "labels"]:
                datasets[key] = kwargs.pop(key, None)
            if key == "colourmap":
                cmapdata = kwargs.pop(key, None)

        #Call function to add/setup the object, all other args passed to properties dict
        if ref is None:
            ref = self.app.createObject(_convert_args(kwargs))
        else:
            self.app.setObject(ref, _convert_args(kwargs))

        #Get the created/updated object
        obj = self.Object(ref)

        #Read any property data sets (allows object creation and load with single prop dict)
        for key in datasets:
            #Get the load function matching the data set (eg: vertices() ) and call on data
            data = datasets[key]
            if data is None or len(data) < 1: continue
            func = getattr(obj, key)
            func(data)

        #Set the colourmap, so python colourmap setting features can be used
        if cmapdata is not None:
            obj.colourmap(cmapdata)

        #Return wrapper obj
        return obj

    def add(self, name=None, **kwargs):
        """
        Add a visualisation object

        Parameters
        ----------
        name : str
            Name to apply to the created object
            If an object of this name exists, it will be returned instead of created

        Returns
        -------
        obj : Object
            The object created
        """
        if isinstance(self._objects, _Objects) and name in self._objects:
            print("Object exists: " + name)
            return self._objects[name]

        #Put provided name in properties
        if name and len(name):
            kwargs["name"] = name

        #Adds a new object, all other args passed to properties dict
        return self._setupobject(ref=None, **kwargs)

    #Shortcut for adding specific geometry types
    def _addtype(self, typename, name=None, **kwargs):
        #Set name to typename if none provided
        if not name: 
            self._ctr += 1
            name = typename + str(self._ctr)
        kwargs["geometry"] = typename
        return self.add(name, **kwargs)

    def Object(self, identifier=None, **kwargs):
        """
        Get or create a visualisation object

        Parameters
        ----------
        identifier : str or int or Object, optional
            If a string, lookup an object by name
            If a number, lookup object by index
            If an object reference, lookup the Object by reference
            If omitted, return the last object in the list
            If no matching object found and string identifier provided, creates an empty object
        **kwargs
            Set of properties passed to the object

        Returns
        -------
        obj : Object
            The object located/created
        """
        #Return object by name/ref or last in list if none provided
        #Get state and update object list
        self._get()
        o = None
        if len(self._objects.list) == 0:
            print("WARNING: No objects exist!")
        #If name passed, find this object in updated list, if not just use the last
        elif isinstance(identifier, str):
            for obj in self._objects.list:
                if obj.name == identifier:
                    o = obj
                    break
            #Not found? Create
            if not o:
                return self.add(identifier, **kwargs)
        elif isinstance(identifier, int):
            #Lookup by index
            if len(self._objects.list) >= identifier:
                o = self._objects.list[identifier-1]
        elif isinstance(identifier, LavaVuPython.DrawingObject):
            #Lookup by swig wrapped object
            for obj in self._objects.list:
                #Can't compare swig wrapper objects directly,
                #so use the name
                if obj.name == identifier.name():
                    o = obj
                    break
        else:
            #Last resort: last object in list
            o = self._objects.list[-1]

        if o is not None:
            self.app.setObject(o.ref, _convert_args(kwargs))
            return o
        print("WARNING: Object not found and could not be created: ",identifier)
        return None

    def ColourMap(self, identifier=None, **kwargs):
        """
        Get or create a colourmap

        Parameters
        ----------
        identifier : str or int or Object, optional
            If a string, lookup an object by name
            If a number, lookup object by index
            If an object reference, lookup the Object by reference
            If omitted, return the last object in the list
            If no matching object found and string identifier provided, creates an empty object
        **kwargs
            Set of properties passed to the object

        Returns
        -------
        obj : Object
            The object located
        """

    def Properties(self, callback=None, **kwargs):
        """
        Create a property collection, essentially a dict() but with a
        control factory that allows creation of interactive controls to edit the properties

        Parameters
        ----------
        callback : function
            Optional function to call whenever a property in this
            collection is changed by an interactive control
            The function should take one argument,
            the collection of type lavavu.Properties() and will be called, with
            the new values whenever the control value is updated.
        **kwargs
            Set of initial properties to store in the collection

        Returns
        -------
        props : Properties
            The collection created
        """
        return Properties(self, callback, **kwargs)

    def file(self, filename, obj=None, **kwargs):
        """
        Load a database or model file

        Parameters
        ----------
        filename : str
            Name of the file to load
        obj : Object
            Vis object to load the file data into,
            if not provided a default will be created
        """

        #Load a new object from file
        self.app.loadFile(filename)

        #Get last object added if none provided
        if obj is None:
            obj = self.Object()
        if obj is None:
            if not "json" in filename and not "script" in filename:
                print("WARNING: No objects exist after file load: " + filename)
            return None

        #Setups up new object, all other args passed to properties dict
        return self._setupobject(obj.ref, **kwargs)
    
    def files(self, files, obj=None, **kwargs):
        """
        Load data from a series of files (using wildcards or a list)

        Parameters
        ----------
        files : str
            Specification of the files to load, either a list of full paths or a file spec string such as `*.gldb`
        obj : Object
            Vis object to load the data into, if not provided a default will be created
        """
        #Load list of files with glob
        filelist = []
        if isinstance(files, list) or isinstance(files, tuple):
            filelist = files
        elif isinstance(files, str):
            filelist = sorted(glob.glob(files))
        obj = None
        for infile in filelist:
            obj = self.file(infile, **kwargs)
        return obj

    def colourbar(self, obj=None, **kwargs):
        """
        Create a new colourbar

        Parameters
        ----------
        obj : Object, optional
            Vis object the colour bar applies to

        Returns
        -------
        colourbar : Object
            The colourbar object created
        """
        #Create a new colourbar
        if obj is None:
            ref = self.app.colourBar()
        else:
            ref = self.app.colourBar(obj.ref)
        if not ref: return
        #Update list
        self._get() #Ensure in sync
        #Setups up new object, all other args passed to properties dict
        return self._setupobject(ref, **kwargs)

    def defaultcolourmaps(self):
        """
        Get the list of default colour map names

        Returns
        -------
        colourmaps : list of str
            Names of all predefined colour maps
        """
        return list(LavaVuPython.ColourMap.getDefaultMapNames())

    def defaultcolourmap(self, name):
        """
        Get content of a default colour map

        Parameters
        ----------
        name : str
            Name of the built in colourmap to return

        Returns
        -------
        str
            Colourmap data formatted as a string
        """
        return LavaVuPython.ColourMap.getDefaultMap(name)

    def colourmap(self, data=None, name="", reverse=False, monochrome=False, **kwargs):
        """
        Load or create a colour map

        Parameters
        ----------
        name : str
            Name of the colourmap, if this colourmap name is found
            the data will replace the existing colourmap, otherwise
            a new colourmap will be created
        data : list or str
            Provided colourmap data can be
            - a string,
            - list of colour strings,
            - list of position,value tuples
            - or a built in colourmap name
            If none provided, a default colourmap will be loaded from lavavu.cubeHelix()
        reverse : boolean
            Reverse the order of the colours after loading
        monochrome : boolean
            Convert to greyscale

        Returns
        -------
        ColourMap(dict)
            The wrapper object of the colourmap loaded/created
        """
        c = ColourMap(self.app.addColourMap(name), self)
        if data is None:
            data = cubeHelix()
        c.update(data, reverse, monochrome, **kwargs)
        return c

    def getcolourmap(self, mapid, string=True):
        """
        Return colour map data as a string or list
        Either return format can be used to create/modify a colourmap
        with colourmap()

        Parameters
        ----------
        mapid : str or int
            Name or index of the colourmap to retrieve
        string : boolean
            The default is to return the data as a string of colours separated by semi-colons
            To instead return a list of (position,[R,G,B,A]) tuples for easier automated processing in python,
            set this to False

        Returns
        -------
        mapdata : str or list
            The formatted colourmap data
        """
        c = ColourMap(mapid, self)
        if string:
            return c.__str__()
        else:
            return c.tolist()

    def clear(self, objects=True, colourmaps=True):
        """
        Clears all data from the visualisation
        Including objects and colourmaps by default

        Parameters
        ----------
        objects : boolean
            including all objects, if set to False will clear the objects
            but not delete them
        colourmaps : boolean
            including all colourmaps

        """
        self.app.clearAll(objects, colourmaps)
        self._get() #Ensure in sync

    def store(self, filename="state.json"):
        """
        Store current visualisation state as a json file
        (Includes all properties, colourmaps and defined objects but not their geometry data)

        Parameters
        ----------
        filename : str
            Name of the file to save

        """
        with open(filename, "w") as state_file:
            state_file.write(self.app.getState())

    def restore(self, filename="state.json"):
        """
        Restore visualisation state from a json file
        (Includes all properties, colourmaps and defined objects but not their geometry data)

        Parameters
        ----------
        filename : str
            Name of the file to load

        """

        if os.path.exists(filename):
            with open(filename, "r") as state_file:
                self.app.setState(state_file.read())

    def timesteps(self):
        """
        Retrieve the time step data from loaded model

        Returns
        -------
        timesteps : list
            A list of all available time steps
        """
        return _convert_keys(json.loads(self.app.getTimeSteps()))

    def addstep(self, step=-1, **kwargs):
        """
        Add a new time step

        Parameters
        ----------
        step : int, optional
            Time step number, default is current + 1
        **kwargs
            Timestep specific properties passed to the created object
        """
        self.app.addTimeStep(step, _convert_args(kwargs))

    def render(self):
        """        
        Render a new frame, explicit display update
        """
        self.app.display()

    def init(self):
        """        
        Re-initialise the viewer window
        """
        if self.app.viewer.isopen: return
        self.app.viewer.open()
        self.app.viewer.init()

    def update(self, filter=None, compress=True):
        """
        Write visualisation data back to the database

        Parameters
        ----------
        filter : str
            Optional filter to type of geometry to be updated, if omitted all will be written
            (labels, points, grid, triangles, vectors, tracers, lines, shapes, volume)
        compress : boolean
            Use zlib compression when writing the geometry data
        """
        for obj in self._objects.list:
            #Update object data at current timestep
            if filter is None:
                #Re-writes all data to db for object
                self.app.update(obj.ref, compress)
            else:
                #Re-writes data to db for object and geom type
                self.app.update(obj.ref, self._getRendererType(filter), compress)

        #Update figure
        self.savefigure()

    def image(self, filename="", resolution=None, transparent=False, quality=95):
        """
        Save or get an image of current display

        Parameters
        ----------
        filename : str
            Name of the file to save (should be .jpg or .png),
            if not provided the image will be returned as a base64 encoded data url
        resolution : list or tuple
            Image resolution in pixels [x,y]
        transparent : boolean
            Creates a PNG image with a transparent background
        quality : int
            Quality for JPEG image compression, default 95%

        Returns
        -------
        image : str
            filename of saved image or encoded image as string data
        """
        if resolution is None:
            return self.app.image(filename, 0, 0, quality, transparent)
        return self.app.image(filename, resolution[0], resolution[1], quality, transparent)

    def frame(self, resolution=None, quality=90):
        """
        Get an image frame, returns current display as base64 encoded jpeg data url

        Parameters
        ----------
        resolution : list or tuple
            Image resolution in pixels [x,y]
        quality : int
            Quality for JPEG image compression, default 90%

        Returns
        -------
        image : str
            encoded image as string data
        """
        #Jpeg encoded frame data
        if not resolution: resolution = self.resolution
        return self.app.image("", resolution[0], resolution[1], quality)

    def jpeg(self, resolution=None, quality=90):
        """
        Get an image frame, returns current display as JPEG data in a bytearray

        Parameters
        ----------
        resolution : list or tuple
            Image resolution in pixels [x,y]
        quality : int
            Quality for JPEG image compression, default 90%

        Returns
        -------
        image : bytearray
            encoded image as byte array
        """
        #Jpeg encoded frame data
        if not resolution: resolution = self.resolution
        return bytearray(self.app.imageJPEG(resolution[0], resolution[1], quality))

    def png(self, resolution=None):
        """
        Get an image frame, returns current display as PNG data in a bytearray

        Parameters
        ----------
        resolution : list or tuple
            Image resolution in pixels [x,y]

        Returns
        -------
        image : bytearray
            encoded image as byte array
        """
        #PNG encoded frame data
        if not resolution: resolution = self.resolution
        return bytearray(self.app.imagePNG(resolution[0], resolution[1]))

    def display(self, resolution=(0,0), transparent=False):
        """        
        Show the current display as inline image within an ipython notebook.
        
        If IPython is installed, displays the result image content inline

        If IPython is not installed, will save the result with 
        a default filename in the current directory

        Parameters
        ----------
        resolution : list or tuple
            Image resolution in pixels [x,y]
        transparent : boolean
            Creates a PNG image with a transparent background
        """
        if is_notebook():
            from IPython.display import display,Image,HTML
            #Return inline image result
            img = self.app.image("", resolution[0], resolution[1], 0, transparent)
            display(HTML("<img src='%s'>" % img))
        else:
            #Not in IPython, call default image save routines (autogenerated filenames)
            self.app.image("*", resolution[0], resolution[1], 0, transparent)

    def webgl(self, filename="webgl.html", resolution=(640,480), inline=True, menu=True):
        """        
        Create a WebGL page with a 3D interactive view of the active model
        
        Result is saved with default filename "webgl.html" in the current directory

        If running from IPython, displays the result WebGL content inline in an IFrame

        Parameters
        ----------
        filename : str
            Filename to save generated HTML page, default : webgl.html
        resolution : list or tuple
            Display window resolution in pixels [x,y]
        inline : boolean
            Display inline when in an IPython notebook cell, on by default.
            Set to false to open a full page viewer in a tab or new window
        menu : boolean
            Include and interactive menu for controlling visualisation appearance, on by default

        Returns
        -------
        str or obj
            filename as string if inline=False, or the inline object otherwise
        """

        try:
            data = '<script id="data" type="application/json">\n' + self.app.web() + '\n</script>\n'
            shaderpath = os.path.join(self.app.binpath, "shaders")
            html = control._webglviewcode(shaderpath, menu) + data
            if inline:
                ID = str(len(self.webglviews))
                template = control.inlinehtml
                template = template.replace('---ID---', ID)
                template = template.replace('---MENU---', 'true' if menu else 'false')
                template = template.replace('---HIDDEN---', control.hiddenhtml)
                template = template.replace('---WIDTH---', str(resolution[0]))
                template = template.replace('---HEIGHT---', str(resolution[1]))
                html = template.replace('---SCRIPTS---', html)
                self.webglviews.append(ID)
            else:
                template = control.basehtml
                template = template.replace('---MENU---', 'true' if menu else 'false')
                template = template.replace('---HIDDEN---', control.hiddenhtml)
                html = template.replace('---SCRIPTS---', html)
                if not filename.lower().endswith('.html'):
                    filename += ".html"
                text_file = open(filename, "w")
                text_file.write(html)
                text_file.close()

            if is_notebook():
                if inline:
                    #from IPython.display import IFrame
                    #display(IFrame(filename, width=resolution[0], height=resolution[1]))
                    from IPython.display import display,HTML
                    return display(HTML(html))
                else:
                    import webbrowser
                    webbrowser.open(filename, new=1, autoraise=True) # open in a new window if possible
            return filename

        except (Exception) as e:
            print("WebGL output error: " + str(e))
            pass

    def exec_webgl(self, code, ID=None):
        """
        Runs code to act on the active (last) webgl viewer object

        The viewer will be available in the variable 'viewer' by inserting code before the
        provided JavaScript, allowing execution of viewer functions in the following script

        Parameters
        ----------
        code : str
            A JavaScript string to execute after getting the viewer object
        ID : int
            A specific webgl ID number, if multiple are active this allows specifying which
            to execute code with, the first being ID=0
        """
        if ID is None:
            #Get the last added viewer
            ID = len(self.webglviews)-1
            if ID < 0: return
        js = """
        var canvas = document.getElementById('canvas_---ID---');
        var viewer = canvas.viewer;
        """.replace('---ID---', str(ID))
        from IPython.display import display,HTML,Javascript
        display(Javascript(js + code))

    def video(self, filename="", fps=10, quality=1, resolution=(0,0)):
        """        
        Shows the generated video inline within an ipython notebook.
        
        If IPython is installed, displays the result video content inline

        If IPython is not installed, will save the result in the current directory


        Parameters
        ----------
        filename : str
            Name of the file to save, if not provided a default will be used
        fps : int
            Frames to output per second of video
        quality : int
            Encoding quality, 1=low(default), 2=medium, 3=high, higher quality reduces
            encoding artifacts at cost of larger file size
        resolution : list or tuple
            Video resolution in pixels [x,y]
        """

        try:
            fn = self.app.video(filename, fps, resolution[0], resolution[1], 0, 0, quality)
            self.player(fn)
        except (Exception) as e:
            print("Video output error: " + str(e))
            pass

    def player(self, filename):
        """
        Shows a video inline within an ipython notebook.

        If IPython is not running, just returns


        Parameters
        ----------
        filename : str
            Path and name of the file to play
        """

        try:
            if is_notebook():
                from IPython.display import display,HTML
                html = """
                <video src="{fn}" controls loop>
                Sorry, your browser doesn't support embedded videos, 
                </video><br>
                <a href="{fn}">Download Video</a> 
                """
                #Jupyterlab replaces ? with encoded char TODO: fix
                #Get a UUID based on host ID and current time
                #import uuid
                #uid = uuid.uuid1()
                #filename = filename + "?" + str(uid)
                display(HTML(html.format(fn=filename)))
        except (Exception) as e:
            print("Video output error: " + str(e))
            pass

    def rawimage(self, resolution=(640, 480), channels=3):
        """
        Return raw image data

        Parameters
        ----------
        resolution : tuple(int,int)
            Image width and height in pixels
        channels : int
            colour channels/depth in bytes (1=luminance, 3=RGB(default), 4=RGBA)

        Returns
        -------
        image : array
            Numpy array of the image data requested
        """
        img = Image(resolution, channels)
        self.app.imageBuffer(img.data)
        return img

    def testimages(self, imagelist=None, tolerance=TOL_DEFAULT, expectedPath='expected/', outputPath='./', clear=True):
        """
        Compare a list of images to expected images for testing

        Parameters
        ----------
        imagelist : list
            List of test images to compare with expected results
            If not provided, will process all jpg and png images in working directory
        tolerance : float
            Tolerance level of difference before a comparison fails, default 0.0001
        expectedPath : str
            Where to find the expected result images (should have the same filenames as output images)
        outputPath : str
            Where to find the output images
        clear : boolean
            If the test passes the output images will be deleted, set to False to disable deletion
        """
        results = []
        if not imagelist:
            #Default to all png images in expected dir
            cwd = os.getcwd()
            try:
                os.chdir(expectedPath)
            except:
                #No expected images yet, just get images in cwd
                #will be copied in to expected in testimage()
                pass
            imagelist = glob.glob("*.png")
            imagelist += glob.glob("*.jpg")
            imagelist.sort(key=os.path.getmtime)
            os.chdir(cwd)

        for f in sorted(imagelist):
            outfile = outputPath+f
            expfile = expectedPath+f
            results.append(self.testimage(expfile, outfile, tolerance))

        #Combined result
        overallResult = all(results)
        if not overallResult:
            raise RuntimeError("Image tests failed due to one or more image comparisons above tolerance level!")
        if clear:
            try:
                for f in imagelist:
                    os.remove(f)
            except:
                pass
        print("-------------\nTests Passed!\n-------------")

    def testimage(self, expfile, outfile, tolerance=TOL_DEFAULT):
        """
        Compare two images

        Parameters
        ----------
        expfile : str
            Expected result image
        outfile : str
            Test output image
        tolerance : float
            Tolerance level of difference before a comparison fails, default 0.0001

        Returns
        -------
        result : boolean
            True if test passes, difference <= tolerance
            False if test fails, difference > tolerance
        """
        if not os.path.exists(expfile):
            print("Test skipped, Reference image '%s' not found!" % expfile)
            print("No expected data, copying generated image to expected...")
            expectedPath = os.path.abspath(os.path.dirname(expfile))
            if not os.path.exists(expectedPath):
                os.makedirs(expectedPath)
            from shutil import copyfile
            if outfile:
                copyfile(outfile, expfile)
            else:
                self.app.image(expfile)
        if len(outfile) and not os.path.exists(outfile):
            raise RuntimeError("Generated image '%s' not found!" % outfile)

        diff = self.app.imageDiff(outfile, expfile)
        result = diff <= tolerance
        reset = '\033[0m'
        red = '\033[91m'
        green = '\033[92m'
        failed = red + 'FAIL' + reset
        passed = green + 'PASS' + reset
        if not result:
            print("%s: %s Image comp errors %f, not"\
                  " within tolerance %g of reference image."\
                % (failed, outfile, diff, tolerance))
            if settings["echo_fails"]:
                print("__________________________________________")
                if len(outfile):
                    print(outfile)
                    with open(outfile, mode='rb') as f:
                        data = f.read()
                        import base64
                        print("data:image/png;base64," + base64.b64encode(data).decode('ascii'))
                else:
                    print("Buffer:")
                    print(self.app.image(""))
                print("__________________________________________")
        else:
            print("%s: %s Image comp errors %f, within tolerance %f"\
                  " of ref image."\
                % (passed, outfile, diff, tolerance))
        return result

    def window(self):
        """
        Create and display an interactive viewer instance

        This shows an active viewer window to the visualisation
        that can be controlled with the mouse or html widgets

        """
        #TODO: support resolution set / full size of div, requires updating viewer frame size
        self.control.Window()
        self.control.show()

    def redisplay(self):
        """
        Update the display of any interactive viewer

        This is required after changing vis properties from python
        so the changes are reflected in the viewer

        """
        #Issue redisplay to active viewer
        self.control.redisplay()

    def camera(self, data=None):
        """
        Get/set the current camera viewpoint

        Displays and returns camera in python form that can be pasted and
        executed to restore the same camera view

        Parameters
        ----------
        data : dict
            Camera view to apply if any

        Returns
        -------
        result : dict
            Current camera view or previous if applying a new view
        """
        self._get()
        me = getname(self)
        if not me: me = "lv"
        #Also print in terminal for debugging
        self.commands("camera")
        #Get: export from first view
        vdat = {}
        if len(self.state["views"]) and self.state["views"][0]:
            def copyview(dst, src):
                for key in ["translate", "rotate", "xyzrotate", "aperture"]:
                    if key in src:
                        dst[key] = copy.copy(src[key])
                        #Round down arrays to max 3 decimal places
                        try:
                            for r in range(len(dst[key])):
                                dst[key][r] = round(dst[key][r], 3)
                        except:
                            #Not a list/array
                            pass

            copyview(vdat, self.state["views"][0])

            print(me + ".translation(" + str(vdat["translate"])[1:-1] + ")")
            print(me + ".rotation(" + str(vdat["xyzrotate"])[1:-1] + ")")

            #Set
            if data is not None:
                copyview(self.state["views"][0], data)
                self._set()

        #Return
        return vdat


    def getview(self):
        """
        Get current view settings

        Returns
        -------
        view : str
            json string containing saved view settings
        """
        self._get()
        return json.dumps(self.state["views"][0])

    def setview(self, view):
        """
        Set current view settings

        Parameters
        ----------
        view : str
            json string containing saved view settings
        """
        self.state["views"][0] = _convert_keys(json.loads(view))
        #self._set() #? sync

    def events(self):
        """
        Process input events
        allows running interactive event loop while animating from python
        e.g.

        >>> import lavavu
        >>> lv = lavavu.Viewer()
        >>> def event_loop():
        ...     while lv.events():
        ...         #...build next frame here...
        ...         lv.render()
        ... event_loop() # doctest: +SKIP

        Returns
        -------
        boolean :
            False if user quit program, True otherwise
        """
        if self.app.events():
            self.app.execute()
            #self.viewer.render()
        return not self.app.viewer.quitProgram

    def serve(self, *args, **kwargs):
        """
        Run a web server in python
        This uses server.py to launch a simple web server

        Parameters
        ----------
        port : int
            port to run on
        ipv6 : boolean
            use ipv6 if True, ipv4 if False
        retries : int
            Number of attempts to open a port, incrementing the port number each time
        """
        if self.server: return
        import server
        self.server = server.serve(self, *args, **kwargs)

    def browser(self, resolution=None, inline=True):
        """
        Open web server browser interface
        """
        if not self.server: self.serve()
        #Running outside IPython notebook? Join here to wait for quit
        #filename = 'http://localhost:' + str(self.server.port) + '/control.html'
        filename = 'http://localhost:' + str(self.server.port) + '/interactive.html'
        if not is_notebook():
            import webbrowser
            webbrowser.open(filename, new=1, autoraise=True) # open in a new window if possible
        elif inline:
            from IPython.display import IFrame
            if resolution is None: resolution = self.resolution
            display(IFrame(filename, width=resolution[0], height=resolution[1]))
        else:
            import webbrowser
            webbrowser.open(filename, new=1, autoraise=True) # open in a new window if possible

    def interactive(self):
        self.app.show() #Need to manually call show now
        if is_notebook():
            self.commands("interactive noloop")
        else:
            self.commands("interactive")

    #TODO: TEST, on mac and with/without threading
    def interact(self, resolution=None):
        """
        Opens an external interactive window
        Unless native=True is passed, will open an interactive web window
        for interactive control via web browser

        This starts an event handling loop which blocks python execution until the window is closed

        Parameters
        ----------
        resolution : tuple(int,int)
            Window width and height in pixels, if not provided will use the global default
        """
        try:
            #Start the server if not running
            if not self.server:
                self.serve()

            if is_notebook():
                if resolution is None: resolution = self.resolution
                from IPython.display import display,Javascript
                js = 'var win = window.open("http://localhost:{port}/interactive.html", "LavaVu", "toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=no,width={width},height={height}");'.format(port=self.server.port, width=resolution[0], height=resolution[1])
                display(Javascript(js))
                #Need a small delay to let the injected javascript popup run
                time.sleep(0.1)
            else:
                import webbrowser
                url = "http://localhost:{port}/interactive.html".format(port=self.server.port)
                #webbrowser.open(url, new=1, autoraise=True) # open in a new window if possible
                #OPEN CONTROL TOO/INSTEAD?
                #url = "http://localhost:{port}/control.html".format(port=self.server.port)
                webbrowser.open(url, new=1, autoraise=True) # open in a new window if possible
                #Handle events until quit - allow interaction without exiting when run from python script
                while not self.app.viewer.quitProgram:
                    time.sleep(TIMER_INC)

        except (Exception) as e:
            print("Interactive launch error: " + str(e))
            pass

    """
    Allows use as thread safe functions
    """
    def isosurface(self, dstref, srcref, properties, clearvol):
        return self.app.isoSurface(dstref, srcref, properties, clearvol)
    #def arrayFloat(self, ref, data, geomdtype):
    #    return self.app.arrayFloat(ref, data, geomdtype)
    #def arrayUInt(self, ref, data, geomdtype):
    #    return self.app.arrayUInt(ref, data, geomdtype)
    #def arrayUChar(self, ref, data, geomdtype):
    #    return self.app.arrayUChar(ref, data, geomdtype)

    def get_all_vertices(self, objectlist):
        """
        Extract all vertex data from a list of objects

        Returns
        -------
        pverts : array
            the vertices, numpy array
        bb_all : tuple
            the bounding box of the combined data
        """
        #Get vertices from a list of lavavu objects
        pverts = None
        bb_all = [[float('Inf'), float('Inf'), float('Inf')], [float('-Inf'), float('-Inf'), float('-Inf')]]
        for o in objectlist:
            #Concatenate all elements
            bb = self.objects[o].boundingbox(True)
            for i in range(3):
                if bb[0][i] < bb_all[0][i]: bb_all[0][i] = bb[0][i]
                if bb[1][i] > bb_all[1][i]: bb_all[1][i] = bb[1][i]

            for v in self.objects[o].data.vertices:
                v = v.reshape((-1,3))
                pverts = v if pverts is None else numpy.concatenate([pverts, v])
        return pverts, bb_all


#Wrapper for list of geomdata objects
class Geometry(list):
    """  
    The Geometry class provides an interface to a drawing object's internal data
    Geometry instances are created internally in the Object class with the data property

    Example
    -------
        
    Get all object data

    >>> import lavavu
    >>> lv = lavavu.Viewer()
    >>> obj = lv.triangles()
    >>> lv.addstep()
    >>> print(lv.steps)
    [0]
    >>> obj.vertices([[0,1], [1,1], [1,0]])
    >>> obj.append()
    >>> obj.vertices([[2,2], [2,3], [3,2]])
    >>> lv.addstep()
    >>> print(lv.steps)
    [0, 1]
    >>> obj.vertices([[0.5,1], [1.5,1], [1.5,0]])
    
    Get only triangle data

    >>> data = obj.data["triangles"]
    >>> print(data)
    [DrawData("triangles") ==> {'vertices': 9}]
    >>> print(data.vertices)
    [array([0.5, 1. , 0. , 1.5, 1. , 0. , 1.5, 0. , 0. ], dtype=float32)]

    Get data at specific timestep only
    (default is current step including fixed data)

    >>> data = obj.data["0"]
    >>> print(data)
    [DrawData("triangles") ==> {'vertices': 9}, DrawData("triangles") ==> {'vertices': 9}]
    >>> print(data.vertices)
    [array([0., 1., 0., 1., 1., 0., 1., 0., 0.], dtype=float32), array([2., 2., 0., 2., 3., 0., 3., 2., 0.], dtype=float32)]

    Loop through data elements

    >>> for el in data:
    ...     print(el)
    DrawData("triangles") ==> {'vertices': 9}
    DrawData("triangles") ==> {'vertices': 9}
    """

    def __init__(self, obj, timestep=-2, filter=None):
        self.obj = obj
        self.timestep = timestep
        #Get a list of geometry data objects for a given drawing object
        if self.timestep < -1:
            glist = self.obj.parent.app.getGeometry(self.obj.ref)
        else:
            glist = self.obj.parent.app.getGeometryAt(self.obj.ref, timestep)
        sets = self.obj.datasets
        for g in glist:
            #By default all elements are returned, even if object has multiple types 
            #Filter can be set to a type name to exclude other geometry types
            if filter is None or g.type == self.obj.parent._getRendererType(filter):
                g = DrawData(g, obj)
                self.append(g)
                #Add the value data set labels
                for s in sets:
                    g.available[s] = sets[s]["size"]

        #Allows getting data by data type or value labels using Descriptors
        #Data by type name
        for key in datatypes:
            typename = key
            if key == 'values':
                #Just use the first available value label as the default .values descriptor
                if len(sets) == 0: continue
                typename = list(sets.keys())[0]
            #Access by type name to get a view
            setattr(Geometry, key, _GeomDataListView(self.obj, self.timestep, typename))
            #Access by type name + _copy to get a copy
            setattr(Geometry, key + '_copy', _GeomDataListView(self.obj, self.timestep, typename, copy=True))

        #Data by label
        for key in sets:
            setattr(Geometry, key, _GeomDataListView(self.obj, self.timestep, key))

    def __getitem__(self, key):
        if isinstance(key, str):
            #Return data filtered by renderer type
            if key in geomnames:
                return Geometry(self.obj, timestep=self.timestep, filter=key)
            else:
                try:
                    #Or data by type/label
                    val = getattr(self, key)
                    return val
                except:
                    #Or data filtered by timestep if a string timestep number passed
                    ts = int(key)
                    return Geometry(self.obj, timestep=ts)

        return super(Geometry, self).__getitem__(key)

    def __str__(self):
        return '[' + ', '.join([str(i) for i in self]) + ']'

    def __call__(self):
        #For backwards compatibility with old Viewer.data() method (now a property)
        return self

class _GeomDataListView(object):
    """A descriptor that provides view/copy/set access to a DrawData list"""
    def __init__(self, obj, timestep, key, copy=False):
        self.obj = obj
        self.timestep = timestep
        self.key = key
        self.copy = copy

        #Set docstring
        if copy:
            self.__doc__ = "Get a copy of all " + key + " data from visualisation object"
        else:
            self.__doc__ = "Get a view of all " + key + " data from visualisation object"

    def __get__(self, instance, owner):
        # we get here when someone calls x.d, and d is a GeomDataListView instance
        # instance = x
        # owner = type(x)

        #Return a copy
        if self.copy:
            return [el.copy(self.key) for el in instance]
        #Return a view
        return [el.get(self.key) for el in instance]

    def __set__(self, instance, value):
        # we get here when someone calls x.d = val, and d is a GeomDataListView instance
        # instance = x
        # value = val
        if not isinstance(value, list) or len(value) != len(instance):
            raise ValueError("Must provide a list of value arrays for each entry, %d entries" % len(instance))
        #Set each DrawData entry to corrosponding value list entry
        v = 0
        for el in instance:
            #Convert to numpy
            data = self.obj._convert(value[v], numpy.float32)
            el.set(self.key, data.ravel())
            v += 1

#Wrapper class for GeomData geometry object
class DrawData(object):
    """  
    The DrawData class provides an interface to a single object data element
    DrawData instances are created internally from the Geometry class

    copy(), get() and set() methods provide access to the data types

    Example
    -------

    >>> import lavavu
    >>> lv = lavavu.Viewer()
    >>> obj = lv.points(vertices=[[0,1], [1,0]], colours="red blue")
    >>> obj.values([2, 3], "myvals")
        
    Get the data elements

    >>> print(obj.data)
    [DrawData("points") ==> {'vertices': 6, 'colours': 2, 'myvals': 2}]
    
    Get a copy of the colours (if any)

    >>> colours = obj.data.colours_copy

    Get a view of the vertex data

    >>> verts = obj.data.vertices

    WARNING: this reference may be deleted by other calls, 
    use _copy if you are not processing the data immediately 
    and relying on it continuing to exist later

    Get a some value data by label "myvals"
    >>> vals = obj.data.myvals
    >>> print(vals)
    [array([2., 3.], dtype=float32)]

    Load some new values for this data, provided list must match first dimension of existing data list

    >>> print(obj.data.myvals)
    [array([2., 3.], dtype=float32)]
    >>> obj.data.myvals = [[4,5]]
    >>> print(obj.data.myvals)
    [array([4., 5.], dtype=float32)]

    """
    def __init__(self, data, obj):
        self.data = data
        self._obj = obj
        self._parent = weakref.ref(obj.parent)
        self.available = {}
        #Get available data types
        for key in datatypes:
            dat = self.get(key)
            if len(dat) > 0:
                self.available[key] = len(dat)

        #Allows getting data by data type or value labels using Descriptors
        sets = obj.datasets
        #Data by type name
        for key in datatypes:
            typename = key
            if key == 'values':
                #Just use the first available value label as the default .values descriptor
                if len(sets) == 0: continue
                typename = list(sets.keys())[0]
            #Access by type name to get a view
            setattr(DrawData, key, self.get(typename))
            #Access by type name + _copy to get a copy
            setattr(DrawData, key + '_copy', self.copy(typename))

    @property
    def parent(self):
        return self._parent()

    @property
    def type(self):
        return geomnames[self.data.type]

    def get(self, typename):
        """
        Get a data element from geometry data

        Warning... other than for internal use, should always
        immediately make copies of the data
        there is no guarantee memory will not be released!

        Parameters
        ----------
        typename : str
            Type of data to be retrieved
            (vertices/normals/vectors/indices/colours/texcoords/luminance/rgb/values)

        Returns
        -------
        data : array
            Numpy array view of the data set requested
        """
        array = None
        if typename in datatypes and typename != 'values':
            if typename in ["luminance", "rgb"]:
                #Get uint8 data
                array = self.parent.app.geometryArrayViewUChar(self.data, datatypes[typename])
            elif typename in ["indices", "colours"]:
                #Get uint32 data
                array = self.parent.app.geometryArrayViewUInt(self.data, datatypes[typename])
            else:
                #Get float32 data
                array = self.parent.app.geometryArrayViewFloat(self.data, datatypes[typename])
        else:
            #Get float32 data
            array = self.parent.app.geometryArrayViewFloat(self.data, typename)
        
        return array

    def copy(self, typename):
        """
        Get a copy of a data element from geometry data

        This is a safe version of get() that copies the data
        before returning so can be assured it will remain valid

        Parameters
        ----------
        typename : str
            Type of data to be retrieved
            (vertices/normals/vectors/indices/colours/texcoords/luminance/rgb/values)

        Returns
        -------
        data : array
            Numpy array containing a copy of the data set requested
        """
        #Safer data access, makes a copy to ensure we still have access 
        #to the data no matter what viewer does with it
        return numpy.copy(self.get(typename))

    def set(self, typename, array):
        """
        Set a data element in geometry data

        Parameters
        ----------
        typename : str
            Type of data to set
            (vertices/normals/vectors/indices/colours/texcoords/luminance/rgb/values)
        array : array
            Numpy array holding the data to be written
        """
        if typename in datatypes and typename != 'values':
            if typename in ["luminance", "rgb"]:
                #Set uint8 data
                self.parent.app.geometryArrayUInt8(self.data, array.astype(numpy.uint8), datatypes[typename])
            elif typename in ["indices", "colours"]:
                #Set uint32 data
                self.parent.app.geometryArrayUInt32(self.data, array.astype(numpy.uint32), datatypes[typename])
            else:
                #Set float32 data
                self.parent.app.geometryArrayFloat(self.data, array.astype(numpy.float32), datatypes[typename])
        else:
            #Set float32 data
            self.parent.app.geometryArrayFloat(self.data, array.astype(numpy.float32), typename)

    def __repr__(self):
        renderlist = [geomnames[value] for value in geomtypes if value == self.data.type]
        return ' '.join(['DrawData("' + r + '")' for r in renderlist]) + ' ==> ' + str(self.available)

#Wrapper class for raw image data
class Image(object):
    """  
    The Image class provides an interface to a raw image

    Example
    -------
        
    >>> import lavavu
    >>> lv = lavavu.Viewer()
    >>> lv.test()
    >>> img = lv.rawimage() # doctest: +SKIP
    >>> img.save('out.png') # doctest: +SKIP
    
    TODO: expose image loading functions, custom blend equations

    """
    def __init__(self, resolution=(640, 480), channels=4, value=[255, 255, 255, 0]):
        if isinstance(value, int):
            value = [value, value, value, 255]
        if isinstance(value, float):
            value = [value*255, value*255, value*255, 255]
        while len(value) < channels:
            value.append(value[-1])
        fill = numpy.array(value[0:channels], dtype=numpy.uint8)
        self.data = numpy.tile(fill, (resolution[1], resolution[0], 1))

    def paste(self, source, resolution=(640,480), position=(0,0)):
        """
        Render another image to a specified position with this image

        Parameters
        ----------
        source : array or lavavu.Viewer
            Numpy array containing raw image data to paste or a Viewer instance to source the frame from
        resolution : tuple(int,int)
            Sub-image width and height in pixels, if not provided source must be a numpy array of the correct dimensions
        position : tuple(int,int)
            Sub-image x,y offset in pixels

        """
        if not isinstance(source, numpy.ndarray):
            source = source.rawimage(resolution, self.data.shape[2]).data

        resolution = (source.shape[1], source.shape[0])
        dest = (resolution[0] + position[0], resolution[1] + position[1])

        if self.data.shape[0] < dest[1] or self.data.shape[1] < dest[0]:
            raise ValueError("Base image too small for operation!" + str(self.data.shape) + " < " + str(dest))
        if self.data.shape[2] != source.shape[2]:
            raise ValueError("Base image and pasted image must have same bit depth!" + str(self.data.shape[2]) + " < " + str(source.shape[2]))
        
        self.data[position[1]:dest[1], position[0]:dest[0]] = source

    def blend(self, source, resolution=(640,480), position=(0,0)):
        """
        Render another image to a specified position with this image with alpha blending

        Parameters
        ----------
        source : array or lavavu.Viewer
            Numpy array containing raw image data to paste or a Viewer instance to source the frame from
        resolution : tuple(int,int)
            Sub-image width and height in pixels, if not provided source must be a numpy array of the correct dimensions
        position : tuple(int,int)
            Sub-image x,y offset in pixels

        """
        if not isinstance(source, numpy.ndarray):
            source = source.rawimage(resolution, self.data.shape[2]).data

        channels = self.data.shape[2]
        if channels < 4 and blend is not None:
            print("Require alpha channel to blend")
            return

        #Alpha blending, assumes not premultiplied alpha
        src = source.astype(numpy.float32)
        dst = self.data[position[1]:resolution[1] + position[1], position[0]:resolution[0] + position[0]].astype(numpy.float32)
        srcalpha = src[:, :, 3] / 255.0
        dstalpha = dst[:, :, 3] / 255.0
        outalpha = srcalpha + dstalpha * (1.0 - srcalpha)
        #Ignore divide by zero if outalpha is zero
        with numpy.errstate(divide='ignore',invalid='ignore'):
            for c in range(3):
                #Premultiplied blend:
                #dst[:, :, c] = src[:, :, c] + dst[:, :, c] * (1.0 - srcalpha)
                #Not premultiplied: premultiply, then blend
                src[:, :, c] *= srcalpha
                dst[:, :, c] *= dstalpha
                dst[:, :, c] = (src[:, :, c] + dst[:, :, c] * (1.0 - srcalpha)) / outalpha
        dst[:, :, 3] = outalpha * 255

        self.paste(dst, resolution, position)
        #self.data[position[1]:dest[0], position[0]:dest[1]] = dst

    def save(self, filename):
        """
        Save a raw image data to provided filename

        Parameters
        ----------
        filename : str
            Output filename (png/jpg supported, default is png if no extension)

        Returns
        -------
        path : str
            Path to the output image
        """
        return LavaVuPython.rawImageWrite(self.data, filename)

    def display(self):
        """        
        Show the image as inline image within an ipython notebook.
        """
        if is_notebook():
            from IPython.display import display,Image,HTML
            #Return inline image result
            img = self.save("")
            display(HTML("<img src='%s'>" % img))

def loadCPT(fn, positions=True):
    """
    Create a colourmap from a CPT colour table file

    Parameters
    ----------
    positions : boolean
        Set this to false to ignore any positional data and
        load only the colours from the file

    Returns
    -------
    colours : string
        Colour string ready to be loaded by colourmap()
    """
    result = ""
    values = []
    colours = []
    hexcolours = []
    hsv = False
    hinge = None

    def addColour(val, colour):
        if len(values) and val == values[-1]:
            if colour == colours[-1]:
                return #Skip duplicates
            val += 0.001 #Add a small increment
        values.append(val)
        if isinstance(colour, str):
            if '/' in colour:
                colour = colour.split('/')
            if '-' in colour:
                colour = colour.split('-')
        if isinstance(colour, list):
            if hsv:
                colour = [float(v) for v in colour]
                import colorsys
                colour = colorsys.hsv_to_rgb(colour[0]/360.0,colour[1],colour[2])
                colour = [int(v*255) for v in colour]
            else:
                colour = [int(v) for v in colour]

        if len(colours) == 0 or colour != colours[-1]:
            if isinstance(colour, str):
                hexcolours.append(colour)
            else:
                hexcolours.append("#%02x%02x%02x" % (colour[0],colour[1],colour[2]))

        colours.append(colour)

    with open(fn, "r") as cpt_file:
        for line in cpt_file:
            if "COLOR_MODEL" in line and 'hsv' in line.lower():
                hsv = True
                continue
            if "HINGE" in line:
                line = line.split('=')
                hinge = float(line[1])
                continue
            if line[0] == '#': continue
            if line[0] == 'B': continue
            if line[0] == 'F': continue
            if line[0] == 'N': continue
            line = line.split()
            #RGB/HSV space separated?
            if len(line) > 7:
                addColour(float(line[0]), [int(line[1]), int(line[2]), int(line[3])])
                addColour(float(line[4]), [int(line[5]), int(line[6]), int(line[7])])
            #Pass whole strings if / or - separated
            elif len(line) > 1:
                addColour(float(line[0]), line[1])
                if len(line) > 3:
                    addColour(float(line[2]), line[3])
            


    minval = min(values)
    maxval = max(values)
    vrange = maxval - minval
    #print "HINGE: ",hinge,"MIN",minval,"MAX",maxval
    
    if positions:
        for v in range(len(values)):
            #Centre hinge value
            if hinge is not None:
                if values[v] == hinge:
                    values[v] = 0.5
                elif values[v] < hinge:
                    values[v] = 0.5 * (values[v] - minval) / (hinge - minval)
                elif values[v] > hinge:
                    values[v] = 0.5 * (values[v] - hinge) / (maxval - hinge) + 0.5
            else:
                values[v] = (values[v] - minval) / vrange

            if isinstance(colours[v], str):
                result += "%.5f=%s; " % (values[v], colours[v])
            else:
                result += "%.5f=rgb(%d,%d,%d); " % (values[v], colours[v][0], colours[v][1], colours[v][2])
    else:
        for v in range(len(hexcolours)):
            #print "(%f)%s" % (values[v], hexcolours[v]),
            result += hexcolours[v] + " "

    return result

def printH5(h5):
    """
    Print info about HDF5 data set (requires h5py)

    Parameters
    ----------
    h5
        HDF5 Dataset loaded with h5py
    """
    print("------ ",h5.filename," ------")
    ks = h5.keys()
    for key in ks:
        print(h5[key])
    for item in h5.attrs.keys():
        print(item + ":", h5.attrs[item])

def download(url, filename=None, overwrite=False, quiet=False):
    """
    Download a file from an internet URL

    Parameters
    ----------
    url : str
        URL to request the file from
    filename : str
        Filename to save, default is to keep the same name in current directory
    overwrite : boolean
        Always overwrite file if it exists, default is to never overwrite

    Returns
    -------
    filename : str
        Actual filename written to local filesystem
    """
    #Python 3 moved urlretrieve to request submodule
    try:
        from urllib.request import urlretrieve
        from urllib.parse import urlparse
        from urllib.parse import quote
    except ImportError:
        from urllib import urlretrieve
        from urllib import quote
        from urlparse import urlparse

    if filename is None:
        filename = url[url.rfind("/")+1:]

    if overwrite or not os.path.exists(filename):
        #Encode url path
        o = urlparse(url)
        o = o._replace(path=quote(o.path))
        url = o.geturl()
        if not quiet: print("Downloading: " + filename)
        urlretrieve(url, filename)
    else:
        if not quiet: print(filename + " exists, skipped downloading.")

    return filename

def style(css):
    """
    Inject stylesheet
    """
    if not is_notebook():
        return
    from IPython.display import display,HTML
    display(HTML("<style>" + css + "</style>"))

def cellstyle(css):
    """
    Override the notebook cell styles
    """
    style("""
    div.container {{
        {css}
    }}
    """.format(css=css))

def cellwidth(width='99%'):
    """
    Override the notebook cell width
    """
    cellstyle("""
    width:{width} !important;
    margin-left:1%;
    margin-right:auto;
    """.format(width=width))

def _docmd(doc):
    """Convert a docstring to markdown"""
    if doc is None: return ''
    def codeblock(lines):
        return ['```python'] + ['    ' + l for l in lines] + ['```']
    md = []
    code = []
    indent = 0
    lastindent = 0
    for line in doc.split('\n'):
        indent = len(line)
        line = line.strip()
        indent -= len(line)
        if len(line) and len(md) and line[0] == '-' and line == len(md[-1].strip()) * '-':
            #Replace '-----' heading underline with '#### heading"
            md[-1] = "#### " + md[-1]
        elif line.startswith('>>> '):
            #Python code
            code += [line[4:]]
        else:
            #Add code block
            if len(code):
                md += codeblock(code)
                code = []
            elif len(md) and indent == lastindent + 4:
                #Indented block, preserve indent
                md += ['&nbsp;&nbsp;&nbsp;&nbsp;' + line + '  ']
                #Keep indenting at this level until indent level changes
                continue
            else:
                md += [line + '  '] #Preserve line breaks
        lastindent = indent
    if len(code):
        md += codeblock(code)
    return '\n'.join(md)

def _markdown(mdstr):
    """Display markdown in IPython if available,
    otherwise just print it"""
    if is_notebook():
        from IPython.display import display,Markdown
        display(Markdown(mdstr))
    else:
        #Not in IPython, just print
        print(mdstr)

def lerp(first, second, mu):
    """Linear Interpolation between values of two lists

    Parameters
    ----------
    first : tuple or list
        first list of values
    second : tuple or list
        second list of values
    mu : float
        Interpolation factor [0,1]

    Returns
    -------
    list
        A list of the interpolated values
    """
    #
    final = first[:]
    for i in range(len(first)):
        diff = second[i] - first[i]
        final[i] += diff * mu
    return final

if __name__ == '__main__':
    #Run doctests
    import doctest
    doctest.testmod()

