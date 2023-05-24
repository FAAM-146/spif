# SPIF
Single Particle Image Format data standard

## Names of stuff

  - ***vocal*:** The netCDF standards compliance checking package (all lower case?)  
  - ***vocal* project:** code repository that contains vocabulary definitions of netCDF standard  
  - **standard vocabulary:** The defined file structure and component criteria of a standard. Stored as JSON?  
  - **product definition:** The defined file structure and component criteria of a netCDF file that follows the standard vocabulary and so satisfies the standard. Stored as yaml?  
 
  

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

