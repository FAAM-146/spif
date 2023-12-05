# SPIF - Single Particle Image Format data standard

**Check that this is not too similar to paper text**

The SPIF file uses the [NetCDF4 format](https://www.unidata.ucar.edu/software/netcdf/). NetCDF4 is a structured binary file format capable of containing large datasets and has automatic compression utilities. NetCDF4 is widely supported on a variety of platforms and environments.

In a similar fashion to the [CF (Climate and Forecast) Conventions](http://cfconventions.org/), the SPIF conventions define a minimum structure, in terms of groups, variables, and attributes, for compliance. Any additional data contained within the file is optional but should not conflict with the standards. In this documentation any suggested but optional data for inclusion are given in *italics*. Due to the focussed type of data, SPIF conventions are more demanding of variable and attribute names than the CF conventions are. SPIF follows the CF [scoping guidelines](http://cfconventions.org/Data/cf-conventions/cf-conventions-1.8/cf-conventions.html#groups) in that dimensions are visible to all child groups.


## Terms and Usage

  - ***vocal*:** The netCDF vocabulary management and standards compliance checking package.
  - **vocabulary:** Attribute, group, and variable naming rules of a standard.  
  - ***vocal* project:** Code repository containing vocabulary definitions, file structure, and compliance rules. See [Project Contents](#project-contents).  
  - **product definition:** Definition of the contents of a netCDF file that are compliant with the rules as specified by the *vocal* project. A minimal example is included in the project or users may create more complex definitions for specific uses.  
  - **product:** A netCDF file that is described by the product definition.


## *vocal* Project Contents

The *vocal* project contains a `standards` directory with version subdirectories. Thus different versions of a standard can be within a project. A `v1` version is created initially and shall be referred to in this documentation.

```shell
  .
  ├── standard
  │   └── v1
  │       ├── attributes
  │       ├── definitions
  │       └── models
  └── example

```

  - `standard/v1/attributes`: `pydantic` models describing mandatory and optional global, group, and variable attributes.

  - `standard/v1/definitions`: Working copy of the product definition stored as a `yaml` file. The definition is an extension of the standard and so may contain attributes that are not in the standard (if this is indeed allowed by the standard). However all attributes must satisfy the rules of the standard. Product definitions are looked for by default in this directory but may also be located elsewhere if the path is explicitly given. 

  - `standard/v1/models`: `pydantic` rule validators for the netCDF dataset, groups, dimensions, and variables.

  - `products`: Versioned definition `json` files are created and placed in a `products` directory with versioned structure, the `latest` subdirectory is created by default. The `products` directory can be placed in a repository dedicated to an organisation's unique requirements.

  - `example`: Directory in this repository with some example raw and SPIF format data for illustration and use by user.


## Standard Compliance

The *vocal* package and SPIF *vocal* project allow arbitrary netCDF files to be checked against the SPIF standard to ensure compliance. With compliance the appropriate file metadata can be included within the root of the file;

```
Conventions: SPIF-1.0
```

### Example workflow

The easiest way to illustrate the compliance checking is to use *vocal* to create a reference SPIF file and then check its compliance.

* If not already done so install *vocal* using the instructions [here](https://github.com/FAAM-146/vocal).
* Clone the SPIF *vocal project*, ie this repository.
* Create a versioned product definition from the working copy. In this example a minimal product is created using the included definition. The version of the definition can be specified, this is seperate from the version of the standard.

```shell
  $ vocal create_version <project_path> -v <defintion_version> -o <definition_path>
```

  So to create a version 0.1 product definition stored in `spif/products` based on the version 1 standard;

```shell
  $ vocal create_version standard/v1 -v 0.1 -o .
  $ ls products/latest/
  dataset_schema.json  spif_example.json
```

* Create a minimal reference SPIF file (data is random).
```shell
  $ vocal eg_data -p <project_path> -d <definition_filename> -o <output_filename>
```

```shell
  $ vocal eg_data -p standard/v1 -d products/latest/spif_example.json -o spif_example.nc
```  

* Check the generated bare-bones file for compliance.
```shell
  $ vocal check <output_filename> -p <project_path> -d <definition_filename>
```

```shell
  $ vocal check spif_example.nc -p standard/v1
  
  Checking spif_example.nc against v1 standard... OK!
  

  $ vocal check spif_example.nc -p standard/v1 -d products/latest/spif_example.json
  
  Checking spif_example.nc against standard... OK!

  Checking spif_example.nc against spif_example.json specification... OK!
  
  ✔ Checking attribute /.author exists
  :
  :
  :
  ✔ Checking variable /instrument_1_group/core/overload exists in definition

  ==================================================
  ✔ 67 checks.
  ! 0 warnings.
  ✗ 0 errors found.
  ==================================================

```

### Creating an in-house format definition for SPIF files

A common usage will be testing a netCDF file against two 'standards' at the same time. For example, an organisation may have an in-house file structure for their SPIF files which includes specific attributes and variables. These files include metadata and data that is optional under the SPIF standard but mandatory in the in-house definition. In-house standard definitions are created with a yaml file and these are described in the _vocal_ [README](https://github.com/FAAM-146/vocal#specifying-data-products).

The standard SPIF [definition file](https://github.com/FAAM-146/spif/blob/main/standard/v1/definitions/spif_example.yaml) may produce a [netCDF file] which looks like;


```shell

netcdf std_spif_example {
  // global attributes:
      :Conventions = "SPIF-0.1" ;

  group: instrument_1 {
    dimensions:
      array_dimensions = 2 ;
      pixel_colors = 3 ;
    variables:
      float color_value(pixel_colors) ;
      int array_size(array_dimensions) ;
      int image_size(array_dimensions) ;
      float resolution(array_dimensions) ;
      float wavelength ;
      float pathlength ;
   group: core {
      dimensions:
        image_num = UNLIMITED ;
        pixel = UNLIMITED ;
      variables:
        uint64 timestamp(image_num) ;
          timestamp:standard_name = "time" ;
          timestamp:units = "seconds since 1970-01-01 00:00:00 +0000" ;
        ubyte image(pixel) ;
        ubyte startpixel(image_num) ;
        ubyte width(image_num) ;
        ubyte height(image_num) ;
        byte overload(image_num) ;
      } // group core
    } // group instrument_1_group
}
```

An in-house standard definition such as that used by [FAAM](faam_data/definitions/core-cloud-phy_faam_YYYYmmdd_v001_rN_xNNN_cip15-1.yaml) for a DMT CIP15 may produce a [netCDF file], the head of which looks like;


```shell

netcdf faam_spif_example {
  // global attributes:
      :Conventions = "CF-1.9 ACDD-1.3 SPIF-0.1" ;
      :acknowledgement = "Airborne data was obtained using the BAe-146-301 Atmospheric Research Aircraft [ARA] flown by Airtask Ltd and managed by FAAM Airborne Laboratory, jointly operated by UKRI and the University of Leeds" ;
      :creator_address = "Building 146, Cranfield University, College Road, Cranfield, Bedford. MK43 0AL. UK." ;
      :creator_email = "creator@faam.ac.uk" ;
      :creator_institution = "FAAM Airborne Laboratory" ;
      :creator_name = "A. N. Other" ;
      :creator_type = "person" ;
      :date = "1970-01-01" ;
      :date_created = "1970-01-01 06:00:00+00:00" ;
      :flight_date = "1970-01-01" ;
      :flight_number = "a001" ;
      :
      :etc


```

In order to test the compliance of this file to both the SPIF standard (version 0.1) and the FAAM definition (which complies with the SPIF structure rules) the product and definition can be different.

```shell
  $ vocal check faam_spif_example.nc -p standard/v1 -d path_to/faam-data/faam_data
```

This will check against the latest version of the in-house definition by default.

```shell
  $ vocal check faam_spif_example.nc -p standard/v1 -d path_to/faam-data/faam_data
```
