
# SPIF - Single Particle Image Format

This repository contains the definition documentation for the Single Particle Image Format (SPIF) standard. SPIF is a file vocabulary for the [FAIR](https://doi.org/10.1038/sdata.2016.18) storage of image data where there is a requirement for auxiliary data and/or metadata to be kept in the same file as the image data. 

There are two parts to this repository;

1. The documentation source files that describe the standard.

   > The compiled documentation is hosted [here](https://www.faam.ac.uk/sphinx/spif).

1. The *vocal* project files that are used to manage and validate SPIF-compliant netCDF files.

   > This is described [below](#the-vocal-spif-project).


## The Single Particle Image Format

The Single Particle Image Format (SPIF) was developed for the archival storage of in situ atmospheric particle image data from imaging probes (see [Baumgardner et al. 2017](https://doi.org/10.1175/AMSMONOGRAPHS-D-16-0011.1) for example) such as the [2DC](https://doi.org/10.1175/1520-0426(1997)014%3C1224:ACFOAP%3E2.0.CO;2) and [CPI](http://www.specinc.com/cloud-particle-imager). The data from these probes has traditionally been stored in specialised binary formats; once decoded the raw data can be stored in SPIF files, improving access and usability of the data. The format is flexible enough to hold other sources of image data as well.

The SPIF file standard uses the [NetCDF4 format](https://www.unidata.ucar.edu/software/netcdf/). NetCDF4 is a structured binary file format capable of containing large datasets and has automatic compression utilities. The format is widely supported on a variety of platforms and environments.

In a similar fashion to the [CF (Climate and Forecast) Conventions](http://cfconventions.org/), the SPIF convention defines a minimum vocabulary, in terms of groups, variables, and attributes, for compliance. Any additional data contained within the file is optional but should not conflict with the requirements of the standard. Due to the focussed type of data, SPIF conventions are more demanding of variable and attribute names than the CF conventions are. SPIF follows the CF [scoping guidelines](http://cfconventions.org/Data/cf-conventions/cf-conventions-1.8/cf-conventions.html#groups) in that dimensions are visible to all child groups.


> **Details of the SPIF data standard and vocabulary descriptions are given [here](https://www.faam.ac.uk/sphinx/spif).**


## The *vocal* SPIF project

*[Vocal](https://github.com/FAAM-146/vocal)* is a tool for managing netCDF data product standards and associated data product specifications. This [repository](https://github.com/FAAM-146/spif) contains the *vocal* project for the SPIF data standard. This is not the only way to construct files that follow the standard but it gives an easy way to check files for compliance with the standard.

Below are described the project and how it may be used.


### Terms and Usage

  - ***vocal*:** The netCDF vocabulary management and standards compliance checking package.
  - **vocabulary:** Attribute, group, and variable naming rules of a standard.
  - ***vocal* project:** Code repository containing vocabulary definitions, file structure, and compliance rules. See [Project Contents](#vocal-project-contents).
  - **product definition:** Definition of the contents of a netCDF file that are compliant with the rules as specified by the *vocal* project. A minimal example is included in the project or users may create more complex definitions for specific use cases.
  - **product:** A netCDF file that is described by the product definition.


### *vocal* Project Contents

The *vocal* project contains a `standards` directory with version subdirectories. Thus different versions of a standard can be within a project. A `v1` version is created initially and shall be referred to in this documentation.

```shell
  .
  ├── spif
  │   ├── standard
  │   │   ├── conventions.yaml
  │   │   └── v1
  │   │       ├── attributes
  │   │       ├── definitions
  │   │       └── models
  │   └── docs
  │
  └── products
      ├── v1
      └── latest
```

  - `standard/conventions.yaml`: Contains netCDF global attribute `Convention` string that *vocal* searchs for to determine appropriate validators.

  - `standard/v1/attributes`: `pydantic` models describing mandatory and optional global, group, and variable attributes.

  - `standard/v1/definitions`: Working copy of the product definition stored as a `yaml` file. The definition is an extension of the standard and so may contain attributes that are not in the standard (if this is allowed) however all attributes must satisfy the rules of the standard. Product definitions are looked for by default in this directory but may also be located elsewhere if the path is explicitly given. Any number of definitions can be stored here.

  - `standard/v1/models`: `pydantic` rule validators for the netCDF dataset, groups, dimensions, and variables.

  - `docs`: Source documentation of the SPIF standard. The compiled documentation is hosted [here](https://www.faam.ac.uk/sphinx/spif).

  - `products`: Versioned definition `json` files are created and placed in a `products` directory with versioned structure, the `latest` subdirectory is created by default. The `products` directory can be created in an arbitrary path, including a repository dedicated to an organisation's unique requirements.


### Standard Compliance

The *vocal* package and SPIF *vocal* project allow arbitrary netCDF files to be checked against the SPIF standard to ensure compliance. With compliance the appropriate file metadata can be included within the root of the file, for example;

```
Conventions: SPIF-1.0
```

#### Example workflow

The easiest way to illustrate the compliance checking is to use *vocal* to create a reference SPIF file and then check its compliance.

* If not already done so, install *vocal* using the instructions [here](https://github.com/FAAM-146/vocal) and activate the environment.
* Clone the SPIF *vocal* project, ie this [repository](https://github.com/FAAM-146/spif).
* Create a versioned product definition from the working copy. Included in this repository are two example definition files; `standard/v1/definitions/spif_example.yaml` which can be used to check for minimal compliance, and `standard/v1/definitions/spif_extended_example.yaml` which is a more realistic example with optional attributes and variables. The example below will create a minimal SPIF product.

  ```shell
    $ vocal release <project_path> -v <defintion_version> -o <definition_path>
  ```

  So to create a version 1.1 product definition stored in `./products` based on the version 1 standard;

  ```shell
    (vocal) ~/spif$ vocal release standard/v1 -v 1.1 -o .
    (vocal) ~/spif$ ls products/latest/
    dataset_schema.json  spif_example.json
  ```

* Create a minimal reference SPIF file (data is random).

  ```shell
    $ vocal build -p <project_path> -d <definition_filename> -o <output_filename>
  ```

  ```shell
    (vocal) ~/spif$ vocal build -p standard/v1 -d products/latest/spif_example.json -o spif_example.nc
  ```

* Check the generated bare-bones file for compliance.

  ```shell
    $ vocal check <output_filename> -p <project_path> -d <definition_filename>
  ```

  This can be done purely against the standard or the standard and the product definition as well.

  ```shell
    (vocal) ~/spif$ vocal check spif_example.nc -p standard/v1
    
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

#### Creating an in-house product definition for SPIF files

A common usage will be testing a netCDF file against both the SPIF standard and organisational requirements at the same time. For example, an organisation may have an in-house vocabulary for their image data files. These files include metadata and data that is optional under the SPIF standard but mandatory in the in-house definition. In-house definitions are created with a yaml file and these are described in the *vocal* [README](https://github.com/FAAM-146/vocal#specifying-data-products). Note that the in-house definition will usually be stored elsewhere and so be (version) controlled by the organisation in question and not as part of the SPIF project repository. The included [extended example definition](standard/v0/definitions/spif_extended_example.yaml) could be used as a template for an in-house definition.

The standard SPIF [definition file](standard/v0/definitions/spif_example.yaml) may produce a netCDF file which looks like;


```ncl

netcdf spif_example {
  // global attributes:
      :Conventions = "SPIF-1.0" ;
      :imager_groups = "imager_1" ;

  group: imager_1 {
      :instrument_name = "imager_1" ;
      :instrument_long_name = "imager_1 with a more descriptive name" ;
      :group_type = "imager"
    dimensions:
      array_dimensions = 1 ;
      pixel_colors = 4 ;
    variables:
      float color_level(pixel_colors) ;
      int array_size(array_dimensions) ;
      int image_size(array_dimensions) ;
      float resolution(array_dimensions) ;
      float wavelength ;
      float pathlength ;
    group: core {
        :group_type = "core" ;
      dimensions:
        image_num = UNLIMITED ;
        pixel = UNLIMITED ;
      variables:
        uint64 timestamp(image_num) ;
          timestamp:standard_name = "time" ;
          timestamp:units = "nanoseconds since 2024-01-01 00:00:00 +0000" ;
        ubyte image(pixel) ;
        ubyte startpixel(image_num) ;
        ubyte width(image_num) ;
        ubyte height(image_num) ;
        byte overload(image_num) ;
      } // group core
    } // group imager_1
  }
```

The extended example definition may produce a netCDF file, the head of which looks like;

```ncl

netcdf spif_extended_example {
  // global attributes:
      :Conventions = "CF-1.9 ACDD-1.3 SPIF-1.0" ;
      :imager_groups = "OAP100" ;
      :title = "Raw image data from the OAP100" ;
      :creator_address = "A Building, Campus District, Town, Country." ;
      :creator_email = "info@arbitrary.org" ;
      :creator_institution = "Abitrary Research Organisation" ;
      :creator_name = "ARO" ;
      :creator_type = "institution" ;
      :instrument = "OAP100" ;
      :project = "ACC - Arbitrary Cloud Campaign" ;
      :platform = "Good Airplane v3" ;
      :platform_type = "aircraft" '
      :deployment_mode = "air" ;
      :date_created = "1970-01-01 06:00:00+00:00" ;
      :flight_date = "1970-01-01" ;
      :flight_number = "a001" ;
      :
      :etc
  }

```

In order to test the compliance of a netCDF file to both the SPIF standard (version 1.0) and the ARO in-house definition (which complies with the SPIF structure rules) one can run;

```shell
  (vocal) ~/spif$ vocal check faam_spif_example.nc -p standard/v1 -d path_to/aro/products
```

This will check against the latest version of the in-house definition by default.

If creating an in-house definition is not sufficient, for example if additional validators are required, then *[vocal](https://github.com/FAAM-146/vocal)* can be forked and and modified. To check that the in-house project has not diverged too far from the SPIF standard it is also possible to check a netCDF file against two different standards at the same time, for example;

```shell
  (vocal) ~/spif$ vocal check aro_example.nc -p standard/v1 path_to/aro/standard/v2
```

