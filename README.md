# Hurricane_Imagery_App

Contains files and documentation to run a Streamlit app for predicting windspeeds of tropical cyclones based on their satellite imagery.

## The underlying data set and sample images

Input images are IRWIN (infrared window) images near 11mcm from the GRIDSAT-B1 satellite.  You can find raw global satellite imagery at

https://www.ncei.noaa.gov/data/geostationary-ir-channel-brightness-temperature-gridsat-b1/access/

Some sample images in the correct format for processing are included in the folder sample_images.  These are images of more recent hurricanes (spanning the years 2017 - 2020) derived from the GRIDSAT-B1 data resized and centered by hand.

The ML model that predicts the windspeed uses data on centered images of tropical cyclones from the HURSAT-B1 dataset found here:

https://www.ncei.noaa.gov/data/hurricane-satellite-hursat-b1/archive/v06/

Raw compressed .tar.gz data for each storm as well as .csv files containing relevsat features for each image are stored at the AWS S3 bucket 'hurricane-imagery-bucket'.  Images were sampled stratified by estimated windspeed intensity in 5 classes : tropical storm, category 1, category 2, category 3, and category 4-5.
Each class contains approxiamtely 1,500 images for a total training size of 6,720 and testing size of 1,050.

## Details on the machine learning algorithm

The model chosen is a CNN using a stochastic gradient descent optimizer.  The resulting model has a RMSE of 10 knots, which is comparable to RMSEs of the existing Dvorak technique for estimating windspeeds based on satellite imagery.  Note that due to the relative lack of training examples in category 5, the model will tend to underestimate the intensity of very intense storms.
