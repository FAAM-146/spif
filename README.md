# SPIF - Single Particle Image Format data standard

Some information here about the standard.


## Terms and Usage

  - ***vocal*:** The netCDF vocabulary management and standards compliance checking package.
  - **vocabulary:** Attribute, group, and variable naming rules of a standard.  
  - ***vocal* project:** Code repository containing vocabulary definitions, file structure, and compliance rules. See [Project Contents](#project-contents).  
  - **product definition:** Definition of the file contents that are compliant with the rules as specified by the *vocal* project. Minimal example may be included in project or a more complete file defined by user. Definition may have   
  - **product:** A netCDF file that is described by the product definition.


## *vocal* project contents

The *vocal* project contains a `standards` directory with version subdirectories. A `v1` version is created initially and shall be referred to in this documentation.

```
  └── standard
      └── v1
          ├── attributes
          ├── definitions
          └── models
```

  - ``attributes``: ``pydantic`` models describing mandatory and optional global, group, and variable attributes.

  - ``definitions``: Working copy of the  `yaml` file product definition. The definition is an extension of the standard and so may contain attributes that are not in the standard (if this is indeed allowed by the standard). However all attributes must satisfy all the rules of the standard. Product definitions are looked for by default in this directory but may also be located elsewhere. 

  - ``models``: ``pydantic`` rule validators for the netCDF dataset, groups, dimensions, and variables.

  - ``products``: Versioned definition `json` files are created and placed in a `products` directory with versioned structure, the `latest` subdirectory is created by default. The `products` directory can be placed in a repository dedicated to an organisation's unique requirements.


## Standard compliance checking
The easiest way to create reference SPIF files and check the compliance of existing files is to use *[vocal](https://github.com/FAAM-146/vocal)* and the SPIF *vocal project*.

### Workflow

* If not already done so install *vocal* using the instructions [here](https://github.com/FAAM-146/vocal).
* Clone the SPIF *vocal project*
* Create a versioned product definition from the working copy. In this example a minimal product is created using the included definition. The version of the definition can be specified, this is seperate from the version of the standard.

  $ vocal create_version <project_path> -v <defintion_version> -o <definition_path>
  
  So to create a version 0.1 product definition stored in `spif/products` based on the version 1 standard;

  $ vocal create_version standard/v1 -v 0.1 -o .
  $ ls products/latest/
  dataset_schema.json  spif_example.json
      
* Create a minimal reference SPIF file (data is random).

  $ vocal eg_data -p <project_path> -d <definition_filename> -o <output_filename>
  
  $ vocal eg_data -p standard/v1 -d products/latest/spif_example.json -o spif_example.nc
  

* Check the generated bare-bones file for compliance.

  $ vocal check <output_filename> -p <project_path> -d <definition_filename>



  $ vocal check spif_example.nc -p standard/v1
  --------------------------------------------------
  Checking spif_example.nc against standard... OK!
  --------------------------------------------------

  $ vocal check spif_example.nc -p standard/v1 -d products/latest/spif_example.json
  --------------------------------------------------
  Checking spif_example.nc against standard... OK!
  --------------------------------------------------
  Checking dimension array_dimensions is in definition... OK!
  etc
  etc
  etc
  Checking variable /instrument_1_group/core/overload exists in definition... OK!
  ==================================================
  66 checks.
  0 warnings.
  0 errors found.
  ==================================================

