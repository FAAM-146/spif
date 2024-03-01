.. title:: SPIF Mandatory Parameters
.. note:: Auto-generated: |today|

~~~~
root
~~~~


 :comment: 

 :history: 

 :institution: 

 :references: 

 :source: 


/instrument
~~~~~~~~~~~


 :comment: 

 :institution: 

 :instrument\_channel: 

 :instrument\_firmware: 

 :instrument\_long\_name: 

 :instrument\_serial\_number: 

 :instrument\_software: 

 :manufacturer: 

 :platform: 

 :raw\_filenames: 

 :references: 

 | *boolean* **antishatter\_tips**
 |  **antishatter\_tips**:long\_name = "Use of antishatter-, or Korolev-tips on probe arms" ;


 | *float* **arm\_separation**
 |  **arm\_separation**:long\_name = "Physical distance between probe arms" ;
 |  **arm\_separation**:units = "millimeter" ;



/instrument/level0
~~~~~~~~~~~~~~~~~~


 :dimension: "particles" ;


 | *float* **F** (particles)
 |  **F**:long\_name = "Shape factor of particle" ;
 |  **F**:units = "dimensionless" ;
 |  **F**:references = "Holroyd 1986" ;


 | *float* **N\_eq** (particles)
 |  **N\_eq**:long\_name = "Diameter of circle with area equivalent to particle area" ;
 |  **N\_eq**:units = "pixels" ;
 |  **N\_eq**:equivalent\_name = "" ;
 |  **N\_eq**:references = "" ;


 | *float* **N\_h** (particles)
 |  **N\_h**:long\_name = "Hypotenuse of triangle formed by N\_p and N\_t" ;
 |  **N\_h**:units = "pixels" ;
 |  **N\_h**:equivalent\_name = "" ;
 |  **N\_h**:references = "" ;


 | *float* **N\_hole** (particles)
 |  **N\_hole**:long\_name = "Max hole diameter" ;
 |  **N\_hole**:units = "pixels" ;
 |  **N\_hole**:equivalent\_name = "" ;
 |  **N\_hole**:references = "" ;


 | *float* **N\_korolev** (particles)
 |  **N\_korolev**:long\_name = "Korolev-corrected diameter" ;
 |  **N\_korolev**:units = "pixels" ;
 |  **N\_korolev**:references = "Korolev, 2007." ;


 | *float* **N\_m** (particles)
 |  **N\_m**:long\_name = "Mean of N\_p and N\_t" ;
 |  **N\_m**:units = "pixels" ;
 |  **N\_m**:equivalent\_name = "" ;
 |  **N\_m**:references = "" ;


 | *int* **N\_p** (particles)
 |  **N\_p**:long\_name = "Max distance in the photodiode-array dimension" ;
 |  **N\_p**:units = "pixels" ;
 |  **N\_p**:equivalent\_name = "N\_y, L5" ;
 |  **N\_p**:references = "?" ;


 | *float* **N\_reconst** (particles)
 |  **N\_reconst**:long\_name = "Reconstructed circle diameter for center-in particle" ;
 |  **N\_reconst**:units = "pixels" ;
 |  **N\_reconst**:equivalent\_name = "" ;
 |  **N\_reconst**:references = "" ;


 | *int* **N\_s** (particles)
 |  **N\_s**:long\_name = "Diameter of minimum enclosing circle" ;
 |  **N\_s**:units = "pixels" ;
 |  **N\_s**:equivalent\_name = "N\_max" ;
 |  **N\_s**:references = "?" ;


 | *float* **N\_slice\_count** (particles)
 |  **N\_slice\_count**:long\_name = "Diameter of slice with maximum number of shaded pixels" ;
 |  **N\_slice\_count**:units = "pixels" ;
 |  **N\_slice\_count**:equivalent\_name = "L2" ;
 |  **N\_slice\_count**:references = "?" ;


 | *float* **N\_slice\_diff** (particles)
 |  **N\_slice\_diff**:long\_name = "Diameter of slice with greatest pixel separation" ;
 |  **N\_slice\_diff**:units = "pixels" ;
 |  **N\_slice\_diff**:equivalent\_name = "L4" ;
 |  **N\_slice\_diff**:references = "?" ;


 | *int* **N\_t** (particles)
 |  **N\_t**:long\_name = "Max distance in the time dimension" ;
 |  **N\_t**:units = "pixels" ;
 |  **N\_t**:equivalent\_name = "N\_x, L1" ;
 |  **N\_t**:references = "?" ;


 | *float* **S** (particles)
 |  **S**:long\_name = "Ratio of fully shaded slices to total slices" ;
 |  **S**:units = "dimensionless" ;
 |  **S**:references = "Holroyd 1986" ;


 | *boolean* **all\_in** (particles)
 |  **all\_in**:long\_name = "Flag indicating if particle is all-in" ;
 |  **all\_in**:units = "dimensionless" ;
 |  **all\_in**:references = "" ;


 | *float* **area** (particles)
 |  **area**:long\_name = "Number of shaded pixels" ;
 |  **area**:units = "pixels" ;
 |  **area**:equivalent\_name = "" ;
 |  **area**:references = "" ;


 | *float* **bbox** (particles, 4)
 |  **bbox**:long\_name = "Bounding box of particle. p0, t0, pN, tN pixel coordinates" ;
 |  **bbox**:units = "pixels" ;
 |  **bbox**:equivalent\_name = "" ;
 |  **bbox**:references = "" ;


 | *boolean* **center\_in** (particles)
 |  **center\_in**:long\_name = "Flag indicating if particle is center-in" ;
 |  **center\_in**:units = "dimensionless" ;
 |  **center\_in**:references = "" ;


 | *float* **ellipse\_angle** (particles)
 |  **ellipse\_angle**:long\_name = "Orientation of particle fit to ellipse" ;
 |  **ellipse\_angle**:units = "radians" ;
 |  **ellipse\_angle**:references = "" ;
 |  **ellipse\_angle**:comment = "Given in radians with range from -pi/2 to pi/2. Reference is parallel to photodiode array." ;


 | *float* **ellipse\_maj\_axis** (particles)
 |  **ellipse\_maj\_axis**:long\_name = "The length of the major axis of the ellipse fit to particle" ;
 |  **ellipse\_maj\_axis**:units = "pixels" ;
 |  **ellipse\_maj\_axis**:references = "" ;


 | *float* **ellipse\_min\_axis** (particles)
 |  **ellipse\_min\_axis**:long\_name = "The length of the minor axis of the ellipse fit to particle" ;
 |  **ellipse\_min\_axis**:units = "pixels" ;
 |  **ellipse\_min\_axis**:references = "" ;


 | *float* **fit\_angle** (particles)
 |  **fit\_angle**:long\_name = "Orientation of particle fit to line using least-squares technique" ;
 |  **fit\_angle**:units = "pixels" ;
 |  **fit\_angle**:references = "" ;
 |  **fit\_angle**:comment = "Given in radians with range from -pi/2 to pi/2. Reference is parallel to photodiode array." ;


 | *float* **fit\_maj\_axis** (particles)
 |  **fit\_maj\_axis**:long\_name = "The length of particle along the least-squares fit line orientation" ;
 |  **fit\_maj\_axis**:units = "pixels" ;
 |  **fit\_maj\_axis**:equivalent\_name = "" ;
 |  **fit\_maj\_axis**:references = "" ;


 | *float* **fit\_min\_axis** (particles)
 |  **fit\_min\_axis**:long\_name = "The length of particle perpendicular to the least-squares fit line orientation" ;
 |  **fit\_min\_axis**:units = "pixels" ;
 |  **fit\_min\_axis**:references = "" ;


 | *float* **fit\_r2** (particles)
 |  **fit\_r2**:long\_name = "R squared value from least-squares line fit" ;
 |  **fit\_r2**:units = "dimensionless" ;
 |  **fit\_r2**:references = "" ;


 | *float* **l\_edge\_count** (particles)
 |  **l\_edge\_count**:long\_name = "Number of shaded pixels along left (0th) photodiode boundary for current particle" ;
 |  **l\_edge\_count**:units = "pixels" ;
 |  **l\_edge\_count**:equivalent\_name = "" ;
 |  **l\_edge\_count**:references = "" ;


 | *float* **perimeter** (particles)
 |  **perimeter**:long\_name = "Number of pixels around perimeter of particle" ;
 |  **perimeter**:units = "pixels" ;
 |  **perimeter**:equivalent\_name = "" ;
 |  **perimeter**:references = "" ;


 | *float* **r\_edge\_count** (particles)
 |  **r\_edge\_count**:long\_name = "Number of shaded pixels along right (Nth) photodiode boundary for current particle" ;
 |  **r\_edge\_count**:units = "pixels" ;
 |  **r\_edge\_count**:equivalent\_name = "" ;
 |  **r\_edge\_count**:references = "" ;



/instrument/level1
~~~~~~~~~~~~~~~~~~


 :dimension: "particles" ;


 | *float* **D\_eq** (particles)
 |  **D\_eq**:long\_name = "Diameter of circle with area equivalent to particle area" ;
 |  **D\_eq**:units = "um" ;
 |  **D\_eq**:references = "" ;


 | *float* **D\_h** (particles)
 |  **D\_h**:long\_name = "Hypotenuse of triangle formed by D\_p and D\_t" ;
 |  **D\_h**:units = "um" ;
 |  **D\_h**:references = "" ;


 | *float* **D\_hole** (particles)
 |  **D\_hole**:long\_name = "Max hole diameter" ;
 |  **D\_hole**:units = "um" ;
 |  **D\_hole**:references = "" ;


 | *float* **D\_korolev** (particles)
 |  **D\_korolev**:long\_name = "Korolev-corrected diameter" ;
 |  **D\_korolev**:units = "um" ;
 |  **D\_korolev**:references = "Korolev, 2007." ;


 | *float* **D\_m** (particles)
 |  **D\_m**:long\_name = "Mean of D\_p and D\_t" ;
 |  **D\_m**:units = "um" ;
 |  **D\_m**:references = "" ;


 | *float* **D\_p** (particles)
 |  **D\_p**:long\_name = "Max distance in the photodiode-array dimension" ;
 |  **D\_p**:units = "um" ;
 |  **D\_p**:equivalent\_name = "D\_y, L5" ;
 |  **D\_p**:references = "?" ;


 | *float* **D\_reconst** (particles)
 |  **D\_reconst**:long\_name = "Reconstructed circle diameter for center-in particle" ;
 |  **D\_reconst**:units = "um" ;
 |  **D\_reconst**:references = "" ;


 | *float* **D\_s** (particles)
 |  **D\_s**:long\_name = "Diameter of minimum enclosing circle" ;
 |  **D\_s**:units = "um" ;
 |  **D\_s**:equivalent\_name = "D\_max" ;
 |  **D\_s**:references = "?" ;


 | *float* **D\_slice\_count** (particles)
 |  **D\_slice\_count**:long\_name = "Diameter of slice with maximum number of shaded pixels" ;
 |  **D\_slice\_count**:units = "um" ;
 |  **D\_slice\_count**:equivalent\_name = "L2" ;
 |  **D\_slice\_count**:references = "?" ;


 | *float* **D\_slice\_diff** (particles)
 |  **D\_slice\_diff**:long\_name = "Diameter of slice with greatest pixel separation" ;
 |  **D\_slice\_diff**:units = "um" ;
 |  **D\_slice\_diff**:equivalent\_name = "L4" ;
 |  **D\_slice\_diff**:references = "?" ;


 | *float* **D\_t** (particles)
 |  **D\_t**:long\_name = "Max distance in the time dimension" ;
 |  **D\_t**:units = "um" ;
 |  **D\_t**:equivalent\_name = "D\_x, L1" ;
 |  **D\_t**:references = "?" ;


 | *boolean* **all\_in** (particles)
 |  **all\_in**:long\_name = "Flag indicating if particle is all-in" ;
 |  **all\_in**:units = "dimensionless" ;
 |  **all\_in**:references = "" ;


 | *float* **area** (particles)
 |  **area**:long\_name = "Area of shaded pixels" ;
 |  **area**:units = "um^2" ;
 |  **area**:references = "" ;


 | *boolean* **center\_in** (particles)
 |  **center\_in**:long\_name = "Flag indicating if particle is center-in" ;
 |  **center\_in**:units = "dimensionless" ;
 |  **center\_in**:references = "" ;


 | *float* **ellipse\_angle** (particles)
 |  **ellipse\_angle**:long\_name = "Orientation of particle fit to ellipse" ;
 |  **ellipse\_angle**:units = "radians" ;
 |  **ellipse\_angle**:references = "" ;
 |  **ellipse\_angle**:comment = "Given in radians with range from -pi/2 to pi/2. Reference is parallel to photodiode array." ;


 | *float* **ellipse\_maj\_axis** (particles)
 |  **ellipse\_maj\_axis**:long\_name = "The length of the major axis of the ellipse fit to particle" ;
 |  **ellipse\_maj\_axis**:units = "um" ;
 |  **ellipse\_maj\_axis**:references = "" ;


 | *float* **ellipse\_min\_axis** (particles)
 |  **ellipse\_min\_axis**:long\_name = "The length of the minor axis of the ellipse fit to particle" ;
 |  **ellipse\_min\_axis**:units = "um" ;
 |  **ellipse\_min\_axis**:references = "" ;


 | *float* **habit** (particles)
 |  **habit**:long\_name = "Name of the habit classification technique" ;
 |  **habit**:key = "" ;
 |  **habit**:references = "" ;
