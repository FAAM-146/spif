.. title:: SPIF Definition

***********************************
SPIF Extensions and Optional Extras
***********************************

Within the mandatory groups of a SPIF file additional and optional attributes and/or variables may be included. In addtion to this, a SPIF file may be extended with optional groups; these groups may contain auxillary or higher level data products or data that does not belong within the ``core`` group but may be useful to the user of the image data. This page describes these optional groups and the parameters that may be contained within them. There are not regulated names and structures for these extended groups but following some of the guidelines here may improve the ease-of-use for other users. Some example optional parameters are given :doc:`here <spif_optional_params>`.

All of the optional groups described sit within the :ref:`instrument <spif-instrument_channel>` group.


.. _spif-aux:

Auxillary Data Group
--------------------

.. note:: The ``aux`` group is an optional SPIF feature.

The instrument ``aux`` group contains auxiliary data relevant to a given instrument. This data may be included to maintain integrity of the original dataset, making SPIF a suitable format for long term archiving. This group has its own ``time`` coordinate; this accommodates time series data that may be transmitted in parallel to the two dimensional image data. The ``aux`` group is optional and may include useful data such as;

    * Housekeeping data
    * Buffer time stamps
    * Image counters
    * Data acquisition timing words
    * Temperature
    * Altitude
    * Air speed


.. _tas:

Auxillary Air Speed Data
^^^^^^^^^^^^^^^^^^^^^^^^

The speed at which particles travel through the probe sample volume is an important parameter for further processing. It allows;

    * conversion of an OAPs slice into a physical resolution and so particle sizes to be calculated,
    * the calculation of sample volume and so higher-order microphysical parameters like particle number concentration, liquid water content, etc.

The true airspeed (TAS) of an OAP may set the rate at which the 1-dimensional array is read. The probe will have an internal TAS which may be set as a constant, read from an on-board pitot tube, or read from a secondary source via the aircraft data system. This internal TAS may be different from the actual air speed, for example if the set TAS does not match the actual air speed or a pitot tube freezes up. This situation will result in distorted images. Post-flight corrections may be required to the internal TAS to comensate for this.

.. TODO::
    :class: warning

    Two options exist here, firstly a **TAS\_corrected** variable that may not be present if no correction applicable. Or a **TAS\_correction** variable that is alway present but which has a default of 1.

If TAS is included then it should have the following form;

    | *float* **TAS\_original** (time)
    |  **TAS\_original**:long_name = "True Air Speed (TAS) as applied by the probe at time of data acquisition" ;
    |  **TAS\_original**:units = "m/s" ;
    |  **TAS\_original**:ancillary_variables = instrument/aux/TAS\_correction ;

    | *float* **TAS\_correction** (time)
    |  **TAS\_correction**:long_name = "Correction factor for True Air Speed (TAS) at the probe. Actual TAS is TAS\_original * TAS\_correction. Default is 1." ;
    |  **TAS\_correction**:units = "dimensionless" ;
    |  **TAS\_correction**:_Fillvalue = 1 ;
    |  **TAS\_correction**:ancillary_variables = instrument/aux/TAS\_original ;

or

    | *float* **TAS\_corrected** (time)
    |  **TAS\_corrected**:long_name = "Corrected true air speed (TAS) at the probe." ;
    |  **TAS\_corrected**:units = "m/s" ;
    |  **TAS\_corrected**:ancillary_variables = instrument/aux/TAS\_original ;


.. _spif-level-0:

Level-0 Processed Data Group
----------------------------

.. note:: The ``level-0`` group is an optional SPIF feature.

Following extraction of image data from the raw binary file, images can be analyzed for information about the particle/s they contain. At the most basic level, parameters of interest describe geometric and physical measurements of the identified particles. Thus, the level 0 data contains basic information about identified particles such as;

    * `Diameters`_ (more discussion on this below)
    * Area
    * Perimeter
    * Bounding box within image
    * Orientation
    * Right edge pixel count
    * Left edge pixel count
    * Center-in (boolean)
    * All-in (boolean)

Note that the level 0 particles are sized using number of pixels---conversion to a physical size takes place in level 1.

Each of the parameters discussed above applies to individual particles. For most imaging probes there can be multiple particles in a single image. Given this *n*-to-one relationship, the level 0 particle data will require use of a new dimension corresponding to the number of particles detected, which is likely to be different than the number of images captured. The ``particles`` dimension thus covers all parameters described in this section. With the additional dimension, there is a need for supplemental parameters which describe the relationship of detected particles to their original image, both in terms of a reference to the additional image, as well as a more exact temporal location, based on the particle’s location in the image frame.

A list of possible level 0 variables are given on :doc:`this page <spif_optional_params>`. As an example variables in the ``level-0`` group may have the following form;

**Dimensions:**

    | particle_num

**Variables:**

    | *int* **image\_index** (particle_num)
    |  **image\_index**:long\_name = "Reference to image\_num index of image containing current particle" ;
    |  **image\_index**:ancillary_variables = instrument/core/image\_num ;

    | *float* **N\_p** (particle_num)
    |  **N\_p**:long_name = "Max diameter of particle in the photodiode-array dimension" ;
    |  **N\_p**:units = "pixels" ;
    |  **N\_p**:references =  ;


.. _spif-level-1:

Level-1 Processed Data Group
----------------------------

.. note:: The ``level-1`` group is an optional SPIF feature.


Whereas level 0 data presents particle information as simply properties of an image, level 1 contains particle properties linked to physical, real-world quantities. In level 1, there are two primary categories of data:

    #. Particle properties scaled to physical dimensions (μm, etc.) using the resolution of the instrument,
    #. Parameters classifying particles into habits or other categories.

As discussed in `tas`_, when generating scaled particle properties, care must be taken to correct for improper scaling in the image time direction due to inconsistencies between the probe sampling rate and the speed of the aircraft. These inconsistencies can happen for various reasons the most common include; exceeding TAS limits of the probe, having incorrect or constant airspeed inputs supplied to the probe, or problems with local pitot measurements due to icing or other blockages.

As the ``level-1`` group is a sub-group of ``level-0``, the ``level-1`` group inherits the ``particle_num`` dimension. A ``PAS`` (or probe air speed) variable gives the correct true air speed at the probe for each particle derived from the TAS variables in the ``aux`` group.

.. TODO::
    :class: warning

    The ``PAS`` variable is just an idea to distinguish from ``TAS\_corrected``. Is this a sensible thing to have PAS/TAS for each particle (derived from timeseries)?

A list of possible level 1 variables are given on :doc:`this page <spif_optional_params>` and may include for example;

**Variables:**

    | *int* **PAS** (particle_num)
    |  **PAS**:long\_name = "Probe Air Speed (PAS) derived from the True Air Speed (TAS) variables in the auxilary data group" ;
    |  **PAS**:units = "m/s" ;

    | *float* **D\_p** (particle_num)
    |  **D\_p**:long_name = "Max diameter of particle in the photodiode-array dimension" ;
    |  **D\_p**:units = "um" ;
    |  **D\_p**:equivalent_name = "D_y, L5" ;
    |  **D\_p**:references =  ;


.. _Diameters:

Diameter definitions
--------------------

    Interpretation of particle diameter presents a challenge, as there are currently several definitions of particle diameter in use by the community, and a standard definition likely isn’t reasonable, since different diameters are useful depending on the measurement scenario. Thus, to make SPIF useful to the broader community, it may include a wide set of diameters in use by the community. An additional consideration for the inclusion of various particle diameters is how these diameters are named. Throughout the literature, varying names have been given to essentially identical diameters. In the diameter definitions here, an attempt will be made to standardize the names, while referencing other names used for a given diameter definition.


    =================   =================       ================================
    Pixel Diameter      Physical diameter       Definition
    =================   =================       ================================
    :math:`N_p`         :math:`D_p`             Maximum diameter in the
                                                photodiode-array dimension.
                                                Equivalent to :math:`N_y`/:math:`D_y` [1]_, [2]_ and :math:`L_5` [3]_.
    :math:`N_t`         :math:`D_t`             Maximum diameter in the time
                                                dimension. Equivalent to :math:`N_x`/:math:`D_x` [1]_, [2]_ and :math:`L_1` [3]_.
    :math:`N_{eq}`      :math:`D_{eq}`          Diameter of circle with area
                                                equivalent to particle area.
    :math:`N_s`         :math:`D_s`             Diameter of minimum enclosing
                                                circle. Equivalent to :math:`N_{max}`/:math:`D_{max}` [4]_.
    :math:`N_h`         :math:`D_h`             Hypotenuse of triangle formed by
                                                :math:`N_p` and :math:`N_t`.
    :math:`N_m`         :math:`D_m`             Mean of :math:`N_p` and
                                                :math:`N_t`.
    |Nsc|               |Dsc|                   Diameter in slice with maximum
                                                number of shaded pixels. Equivalent to :math:`L_2` [3]_.
    |Nsd|               |Dsd|                   Diameter in slice with greatest
                                                pixel separation. Equivalent to :math:`L_4` [3]_.
    |Nre|               |Dre|                   Reconstructed circle diameter
                                                for center-in particles.
    |Nho|               |Dho|                   Max hole diameter as defined in
                                                [5]_.

    =================   =================       ================================

.. Substitutions that don't fit into rst table

.. |Nsc| replace:: :math:`N_{\scriptsize\mbox{slice_count}}`
.. |Dsc| replace:: :math:`D_{\scriptsize\mbox{slice_count}}`
.. |Nsd| replace:: :math:`N_{\scriptsize\mbox{slice_diff}}`
.. |Dsd| replace:: :math:`D_{\scriptsize\mbox{slice_diff}}`
.. |Nre| replace:: :math:`N_{\scriptsize\mbox{reconst}}`
.. |Dre| replace:: :math:`D_{\scriptsize\mbox{reconst}}`
.. |Nho| replace:: :math:`N_{\scriptsize\mbox{hole}}`
.. |Dho| replace:: :math:`D_{\scriptsize\mbox{hole}}`



.. _spif-level-2:

Level-2 Processed Data Group
----------------------------

.. note:: The ``level-2`` group is an optional SPIF feature.


Level 2 processed data is derived from level-1 data and may include aggregated properties such as;

    * Concentration timeseries
    * Size distributions
    * Liquid water content timeseries


.. rubric:: References

.. [1] Korolev, A., Isaac, G.A. and Hallett, J. "Ice particle habits in stratiform clouds", Q.J.R. Meteorol. Soc., 126, 2873-2902, doi: `10.1002/qj.49712656913 <https://doi.org/10.1002/qj.49712656913>`_, 2000.
.. [2] Leroy, D., E. Fontaine, A. Schwarzenboeck, and J. W. Strapp. "Ice Crystal Sizes in High Ice Water Content Clouds. Part I: On the Computation of Median Mass Diameter from In Situ Measurements", J. Atmos. Oceanic Technol., 33, 11, 2461-2476, doi: `10.1175/JTECH-D-15-0151.1 <https://doi.org/10.1175/JTECH-D-15-0151.1>`_, 2016.
.. [3] Lawson, R. P. "Effects of ice particles shattering on the 2D-S probe", Atmos. Meas. Tech., 4, 1361-1381, doi: `10.5194/amt-4-1361-2011 <https://doi.org/10.5194/amt-4-1361-2011>`_, 2011.
.. [4] Heymsfield, A. J., Schmitt, C. and Bansemer, A. "Ice Cloud Particle Size Distributions and Pressure-Dependent Terminal Velocities from In Situ Observations at Temperatures from 0° to -86°C", J. Atmos. Oceanic Technol., 70, 4123-4154, doi: `10.1175/JAS-D-12-0124.1 <https://doi.org/10.1175/JAS-D-12-0124.1>`_, 2013.
.. [5] Korolev, A. V. "Reconstruction of the sizes of spherical particles from their shadow images Part I: Theoretical considerations", J. Atmos. Oceanic Technol., 24, 376-389, doi: `10.1175/JTECH1980.1 <https://doi.org/10.1175/JTECH1980.1>`_, 2007.