# SPIF
Single Particle Image Format data standard

## Terms and Usage

  - ***vocal*:** The netCDF vocabulary management and standards compliance checking package
  - **vocabulary:** Attribute, group, and variable naming rules of a standard.  
  - ***vocal* project:** code repository containing vocabulary definitions, file structure, and compliance rules. See [Project Contents](#project-contents).  
  - **product definition:** Definition of the file contents that are compliant with the rules as specified by the *vocal* project. Minimal example may be included in project or a more complete file defined by user. Definition may have attrs not in std (if allowed by the std) but must satisfy all rules of std  
  - **product:** A netCDF that is described by the product definition

## *vocal* project contents
  Describe what is in v1/dirs
   
   + Contained in py file defs in project

## Standard compliance checking
The easiest way to create reference SPIF files and check the compliance of existing files is to use *[Vocal](https://github.com/FAAM-146/vocal)* and the SPIF *Vocal project*.

### Workflow

* If not already done so install *vocal* using the instructions [here](https://github.com/FAAM-146/vocal).
* Clone the SPIF *vocal project definition*
* Create a *vocal project*

      vocal create_vocabs <how_to_specify_project> -v <version> -o <where_should_this_go>
  
  This creates the versioned project definition.
* Create a empty reference SPIF file

    vocal eg_data -p <project_name> -d <definition> -o <output_file>

* This is a bare-bones file.

