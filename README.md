# Hurricane_Imagery_App

Contains files and documentation to run an app for predicting windspeeds of tropical cyclones based on their satellite imagery.  The app is powered and hosted by Streamlit at the URL

https://share.streamlit.io/natetotz/hurricane_imagery_app/main

This model performs comparably to existing Dvorak-type techniques while only requiring a single centered infrared image.

## The underlying data set and sample images

Input images are IRWIN (infrared window) images near 11µm from the GRIDSAT-B1 satellite.  Raw global satellite imagery is available at

https://www.ncei.noaa.gov/data/geostationary-ir-channel-brightness-temperature-gridsat-b1/access/

Some sample images in the correct format for processing are included in the folder sample_images.  These are images of more recent hurricanes (spanning the years 2017 - 2020) derived from the GRIDSAT-B1 data resized and centered by hand.

The ML model uses data on centered images of tropical cyclones from the HURSAT-B1 dataset found here:

https://www.ncei.noaa.gov/data/hurricane-satellite-hursat-b1/archive/v06/

Raw compressed .tar.gz data for each storm as well as .csv files containing relevant features for each image are stored at the AWS S3 bucket 'hurricane-imagery-bucket'.  When unzipped, the data is stored in netCDF4 format.  Documentation for these files can be found at

https://www.ncdc.noaa.gov/hursat/doc/HURSAT-Documentation-v6-b1.pdf

Images were sampled from storms in the years (1978 - 2015) and stratified by estimated windspeed intensity in 5 classes : tropical storm, category 1, category 2, category 3, and category 4-5.  Each class contains 1,554 images for a total training size of 6,720 and testing size of 1,050.

## Details on the machine learning algorithm

The model chosen is a regression CNN using a stochastic gradient descent optimizer.  

The resulting model has a RMSE of 10 knots, which is comparable to RMSEs of the existing Dvorak technique for estimating windspeeds based on satellite imagery.  For an in-depth analysis of Dvorak techniques and their errors, consult *An Evaluation of Dvorak Technique–Based Tropical Cyclone Intensity Estimates, J. Knaff et. al. (2010)*, available online at

https://journals.ametsoc.org/view/journals/wefo/25/5/2010waf2222375_1.xml

Note that due to the relative lack of training examples in category 5, the model will tend to underestimate the intensity of very intense storms.  The algorithm also assumes input images are centered on the circulation of the tropical cyclone.  Therefore storms with ill-defined eyes or unclear circulation patterns will be difficult to properly center and therefore accurately analyze; this is particularly true of weak storms.
