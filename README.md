# Hurricane_Imagery_App

Contains files and documentation to run an app for predicting windspeeds of tropical cyclones based on their satellite imagery.  The app is powered and hosted by Streamlit [here](https://share.streamlit.io/natetotz/hurricane_imagery_app/main).  This model performs comparably to existing Dvorak-type techniques while only requiring a single centered infrared image.

## The underlying data set and sample images

Input images are IRWIN (infrared window) images near 11µm from [GRIDSAT-B1 satellite data](https://www.ncdc.noaa.gov/gridsat/gridsat-index.php?name=gridsat-intro), in the form of 301 x 301 CSV files.  The user can either opt to input the time, longitude, and latitude of a storm center, or upload a properly formatted image file manually.  An extensive list of centers of historical storms can be found [here](https://www.ssd.noaa.gov/PS/TROP/tdpositions.html).  Raw global satellite imagery is available [here](https://www.ncei.noaa.gov/data/geostationary-ir-channel-brightness-temperature-gridsat-b1/access/).  Some sample images in the correct format for processing are included in the folder sample_images.  These are images of more recent hurricanes (spanning the years 2017 - 2020) derived from the GRIDSAT-B1 data resized and centered by hand.

The ML model uses data on centered images of tropical cyclones from the HURSAT-B1 dataset found [here](https://www.ncei.noaa.gov/data/hurricane-satellite-hursat-b1/archive/v06/).  Raw compressed .tar.gz data for each storm as well as CSV files containing relevant features for each time slice of each storm are stored at the AWS S3 bucket 'hurricane-imagery-bucket'.  When unzipped, the data is stored in netCDF4 format.  Documentation for these files can be found [here](https://www.ncdc.noaa.gov/hursat/doc/HURSAT-Documentation-v6-b1.pdf).

Images were sampled from storms in the years (1978 - 2015) and stratified by estimated windspeed intensity in 5 classes: 

+ Tropical Storm
+ Category 1
+ Category 2
+ Category 3
+ Category 4-5

Categories 4 and 5 were merged due to a relative lack of Category 5 images.  Each class contains 1,554 images for a total training size of 6,720 and testing size of 1,050.

The full stratified data set used for training and validating the model is stored [on Google Drive here](https://drive.google.com/drive/folders/1sw9jvZgN-knslx3rACmnA6oQELqjHvCB?usp=sharing).  Each file is a 301 x 302 CSV file.  Taken together, columns 0 through 300 yield the 301 x 301 image array of the storm.  Column 301 consists entirely of entries containing the actual windspeed of the storm in knots.  Each file name contains metadata for the storm following the same convention as the above netCDF4 file names.

## Details on the machine learning algorithm

The model chosen is a regression CNN using a stochastic gradient descent optimizer.  Details of the model and its training are in the Hurricane_ML.py script.

The resulting model has a RMSE of 10 knots, which is comparable to the RMSEs of the existing Dvorak techniques for estimating windspeeds based on satellite imagery.  For an in-depth analysis of Dvorak techniques and their errors, consult [*An Evaluation of Dvorak Technique–Based Tropical Cyclone Intensity Estimates, J. Knaff et. al. (2010)*](https://journals.ametsoc.org/view/journals/wefo/25/5/2010waf2222375_1.xml).

Note that due to the relative lack of training examples in category 5, the model will tend to underestimate the intensity of very intense storms.  The algorithm also assumes input images are centered on the circulation of the tropical cyclone.  Therefore storms with ill-defined eyes or unclear circulation patterns will be difficult to properly center and therefore accurately analyze; this is particularly true of weak storms.

If the user opts to input the spacetime location of a tropical cyclone, the app creates a user log containg the request datetime, location and predicted windspeed of the tropical cyclone.  These logs can be used to further evaluate the performance of the ML model.  The logs are CSVC files of the form 'UserLog*.csv' and are stored in this Github repo.
