.. title:: SPIF Mandatory Parameters
.. note:: Auto-generated: |today|

~~~~
root
~~~~


 :Conventions: "SPIF-0.86" ;
 

 :title: 


/instrument
~~~~~~~~~~~


 :instrument\_name: 

 :dimension: "bit" ;


 :dimension: "pixel" ;


 | *float* **array\_rate**
 |  **array\_rate**:long\_name = "Temporal clocking rate of imaging array" ;
 |  **array\_rate**:units = "hertz" ;


 | *int* **array\_size**
 |  **array\_size**:long\_name = "Number of pixels across the imaging array, may be 1d or 2d." ;
 |  **array\_size**:units = "dimensionless" ;


 | *int* **image\_size**
 |  **image\_size**:long\_name = "Number of pixels across an image, may be 1d or 2d. If fixed size then number of pixels, if variable size then \_FillValue" ;
 |  **image\_size**:units = "dimensionless" ;
 |  **image\_size**:\_fillvalue = "0" ;


 | *float* **resolution**
 |  **resolution**:long\_name = "Physical resolution of array pixels instrument" ;
 |  **resolution**:units = "um" ;


 | *float* **shadow** (bit)
 |  **shadow**:long\_name = "Fractional obscuration of photodiode array for each bit value" ;
 |  **shadow**:units = "dimensionless" ;


 | *float* **start\_time**
 |  **start\_time**:long\_name = "Reference datetime of image data" ;
 |  **start\_time**:units = "seconds since <reference datetime>" ;


 | *int* **value** (bit)
 |  **value**:long\_name = "Value of shadow level in image array" ;
 |  **value**:units = "dimensionless" ;


 | *float* **wavelength**
 |  **wavelength**:long\_name = "Operating wavelength of laser used for shadowing/imaging the particles" ;
 |  **wavelength**:units = "nm" ;



/instrument/core
~~~~~~~~~~~~~~~~


 :dimension: "image_num" ;


 | *int* **height** (image_num)
 |  **height**:long\_name = "Number of slices/lines in image" ;
 |  **height**:units = "dimensionless" ;


 | *int* **image** (pixel)
 |  **image**:long\_name = "Flattened 1d array of images" ;
 |  **image**:units = "dimensionless" ;


 | *int* **overload** (image_num)
 |  **overload**:long\_name = "Probe particle overload status" ;
 |  **overload**:flag\_values = "0, 1" ;
 |  **overload**:flag\_meanings = "normal overload" ;
 |  **overload**:units = "dimensionless" ;


 | *int* **startpixel** (image_num)
 |  **startpixel**:long\_name = "Array index of first image slice" ;
 |  **startpixel**:units = "dimensionless" ;


 | *float* **timestamp** (image_num)
 |  **timestamp**:long\_name = "Image arrival time in nanoseconds from reference start time" ;
 |  **timestamp**:units = "nanoseconds since <start\_time>" ;
 |  **timestamp**:ancillary\_variables = "instrument/start\_time" ;


 | *int* **width** (image_num)
 |  **width**:long\_name = "Number of pixels across image" ;
 |  **width**:units = "dimensionless" ;



/instrument/raw
~~~~~~~~~~~~~~~


 :dimension: "buffer" ;
