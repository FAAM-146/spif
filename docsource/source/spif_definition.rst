.. title:: SPIF Definition

********************
SPIF File Definition
********************

As described in :doc:`SPIF Structure <structure>`, in order to be SPIF-compliant, a file must have a prescribed structure and a set of included parameters. The exact list of mandatory parameters---parameters include netCDF groups, attributes, dimensions and variables---are given :doc:`here <spif_mandatory_params>` [#ParamGenerationFoot]_.

On this page, the mandatory SPIF groups are described in detail. Note that although the groups are mandatory, in the examples given not all of the attributes or variables of those groups may be.

Group/root attributes are defined as;

    :attribute_name: Short description of attribute value

Scalar variables, that is those without a dimension, are defined as;

    | *dtype* **variable_name**
    |  **variable_name**:attribute_1 = Short description of attribute 1 value ;
    |  **variable_name**:attribute_2 = Short description of attribute 2 value ;

Variables are defined as;

    | *dtype* **variable_name** (dimension)
    |  **variable_name**:attribute_1 = Short description of attribute 1 value ;
    |  **variable_name**:attribute_2 = Short description of attribute 2 value ;



.. _spif-root:

====================
SPIF Root Attributes
====================

Each SPIF file has a standardised set of attributes in the root. These attributes may include (``Conventions`` and ``title`` are mandatory);

    :Conventions: "SPIF-n.m"        (where n.m is the specification version)
    :title: Short description of dataset contents
    :institution: Where the data orginated
    :source: Name and version of software/hardware used to generate this dataset
    :history: Audit trail of file modifications
    :references: References of any documents describing the data and production of this dataset
    :comment: Any further information pertaining to this data

Any other attributes that apply to this dataset can be included in the root.


.. _spif-instrument_channel:

========================
Instrument Channel Group
========================

Although SPIF files will contain data from a single instrument, some instruments may have more than one independent instrument channels. Each of these instrument channels will have a separate group. The root of the **instrument channel group** contains attributes pertaining to that specific instrument/channel. It should also include any further information such as the probe software module that was used to create the file.

Instrument group attributes are currently not mandatory but may include;

    :instrument_name: Short name of instrument
    :instrument_long_name: Full descriptive name of instrument
    :instrument_channel: Instrument channel (if applicable)
    :instrument_serial_number: Serial number or instrument identifier
    :manufacturer: Manufacturer of instrument
    :instrument_firmware: Instrument firmware version
    :instrument_software: Name and version of data acquisition software interfacing with instrument
    :institution: Institution operating instrument
    :platform: Name or description of platform instrument is mounted on
    :raw_filenames: Raw data filename(s) used to generate the current instrument dataset
    :references: Link to web, paper, document reference describing instrument
    :comment: Any further notes about instrument, platform, location, orientation, etc;

Universal variables may also be included in the instrument group root. For example;

**Dimensions:**

    | pixel
    | bit

**Variables:**

    | *int* **value** (bit)
    |  **bit**:long_name = "Value of shadow level in image array" ;
    |  **bit**:ancillary\_variables = shadow;

    | *float* **shadow** (bit)
    |  **shadow**:long\_name = "Fractional obscuration of photodiode array for each bit value" ;

    | *float* **start\_time**
    |  **start\_time**:long\_name = "Reference datetime of image data" ;
    |  **start\_time**:units = "seconds since <reference datetime>" ;

    | *float* **resolution**
    |  **resolution**:long\_name = "Physical resolution of array pixels" ;
    |  **resolution**:units = "micrometer" ;
    |  **resolution**:ancillary_variables = instrument/resolution_err ;

    | *float* **resolution_err**
    |  **resolution_err**:long\_name = "Uncertainty of physical resolution of array pixels" ;
    |  **resolution_err**:units = "micrometer" ;

    | *float* **array\_rate**
    |  **array\_rate**:long\_name = "Maximum temporal clocking rate of the imaging array." ;
    |  **array\_rate**:units = "hertz" ;
    |  **array\_rate**:comment = "An OAP clocking rate may vary (eg with TAS) but will never be greater than array_rate. If 2d imaging probe then this defines maximum frame rate."

    | *int* **array\_size**
    |  **array\_size**:long\_name = "Number of pixels across the imaging array, may be 1d or 2d." ;

    | *int* **image\_size**
    |  **image\_size**:long\_name = "Number of pixels across an image, may be 1d or 2d. If fixed size then number of pixels, if variable size then _FillValue" ;
    |  **image\_size**:_FillValue = 0 ;

    | *float* **wavelength**
    |  **wavelength**:long\_name = "Operating wavelength of laser used for shadowing/imaging the particles" ;
    |  **wavelength**:units = "nanometer" ;

    | *float* **arm\_separation**
    |  **arm\_separation**:long_name = "Physical distance between probe arms" ;
    |  **arm\_separation**:units = "millimeter" ;

    | *boolean* **antishatter_tips**
    |  **antishatter\_tips**:long\_name = "Use of antishatter-, or Korolev-, tips on probe arms" ;


.. _spif-core:

Instrument Core Group
---------------------

The instrument ``core`` group isa sub-group of the ``instrument`` group and contains the raw image data. All image data has been extracted from the raw binary file and presented here in a more usable form, no filtering has been carried out so potentially corrupt images, repeated images, and noise are all included. Buffer headers are not included, these are contained within the ``raw`` group variable/s.

.. TODO::
    :class: warning

    The above paragraph stipulates that no image filtering is done. Are there any situations where this may *not* be the case?


The unlimited dimensions are ``image_num`` and ``pixel`` where ``max(image_num)`` is the number of images in the dataset and ``max(pixel)`` is the total number of pixels of data in the flattened image array.

.. Note::
    Each image may in fact contain multiple particles. As the ``core`` group is entirely raw data, there has been no processing to split out the multiple particles from a single image.

The arrival time of each image is given by ``timestamp``. The units are in nanoseconds from the reference ``start_time``, this is defined in the ``timestamp:units`` attribute using the `CF format <http://cfconventions.org/Data/cf-conventions/cf-conventions-1.8/cf-conventions.html#time-coordinate>`_. Note that different probes may not provide image times in exactly the same way and indeed, image arrival time may in some circumstances be difficult to precisely define. However, the ``timestamp`` variable will always give the image arrival time as accurately as possible, a description of how it was determined from the raw buffer data should be included in the ``timestamp:comment`` attribute. One may decide to add a ``timestamp_flag`` as an ancillary variable using the `CF flag format <http://cfconventions.org/Data/cf-conventions/cf-conventions-1.8/cf-conventions.html#flags>`_.

Variables in the ``core`` group include;

**Dimensions:**

    | image_num

**Variables:**

    | *int* **image** (pixel)
    |  **image**:long\_name = "Flattened 1d array of images" ;

    | *float* **timestamp** (image_num)
    |  **time**:standard_name = "time" ;
    |  **time**:timezone = "UTC" ;
    |  **time**:long_name = "image arrival time in nanoseconds from reference start time" ;
    |  **time**:units = "nanoseconds since <start_time>" ;
    |  **time**:ancillary_variables = instrument/start_time ;

    | *int* **startpixel** (image_num)
    |  **startpixel**:long\_name = "Array index of first image slice" ;

    | *int* **width** (image_num)
    |  **width**:long\_name = "Number of pixels across image" ;
    |  **width**:units = "pixels" ;

    | *int* **height** (image_num)
    |  **height**:long\_name = "Number of slices/lines in image" ;
    |  **height**:units = "lines" ;

    | *int* **overload** (image_num)
    |  **overload**:long\_name = "Data quality flag for each image" ;
    |  **overload**:flag_values = "0, 1" ;
    |  **overload**:flag_meanings, "good bad" ;


.. admonition:: A word on data types

    The above dtypes are given in the broadest terms as the definitions do not *require* a specific type of *integer* or *float*. However, significant savings in terms of file size and memory usage can be made by using the following dtypes (given in terms of `netCDF <http://unidata.github.io/netcdf4-python/#variables-in-a-netcdf-file>`_ and `numpy <https://numpy.org/doc/stable/reference/arrays.scalars.html>`_ dtypes);

       | **image**: 'u1' or np.uint8
       | **timestamp**: 'f4' or np.float32
       | **startpixel**: 'u8' or np.uint64
       | **width**: 'u4' or np.uint32
       | **height**: 'u4' or np.uint32
       | **flag**: 'u1' or np.uint8


.. _spif-raw:

Raw Data Group
--------------

The instrument ``raw`` group contains data variables of the raw buffer information in the binary file. This will include buffer headers, timing *ticks*, and other sundary data. In order to act as a fully fledged raw data format this group is required however, as the data is highly instrument dependent, the contents of this group are not described. This is not seen as a problem as only those very familiar with the raw data are likely going to work with the contents of this group. The variable dimension is ``buffer``.

.. TODO::
    :class: warning

    Does the raw data variable/s include the end-of-buffer demarcations?




.. rubric:: Footnotes

.. [#ParamGenerationFoot] The lists of mandatory and optional SPIF file parameters are automatically generated from a configuration files. These files are also used by the SPIF compliance-checker and so should be regarded as the authoritive source for a given SPIF version.
