import streamlit as st
import time
from datetime import datetime as dt
import netCDF4 as nc
import selenium
from selenium import webdriver
from matplotlib.backends.backend_agg import RendererAgg

import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import os
from git import Repo
import subprocess

from git import Repo

import tensorflow as tf

def bash_string(string):
  return subprocess.run(string, shell = True, capture_output = True)

def convert_coordinates(NS_index, EW_index, to_degrees):
    # conversion between true latitude/longitude and the indices here:
    # latitude: (0, -70), (2000, 70)
    # longitude: (0, -180), (5143, 180)

    # performs the linear conversion between indices of the GRIDSAT image and standard latitude/longitude degrees
    # to_degrees determines which direction the covnersion is carried out
    # GRIDSAT INDICES must be integers, so these functions need not be exact inverses due to rounding

    if to_degrees:
        latitude = 140 / 2000 * NS_index - 70
        longitude = 360 / 5143 * EW_index - 180
        return (latitude, longitude)

    if not (to_degrees):
        lat_index = int((NS_index + 70) * (2000 / 140))
        lon_index = int((EW_index + 180) * (5143 / 360))
        return (lat_index, lon_index)

def plot_cyclone(image_df):

    fig = plt.figure(edgecolor='black')
    g1 = sns.heatmap(image_df, cbar=False, cmap="YlGnBu")
    g1.set(yticklabels=[])
    g1.set(xticklabels=[])
    g1.tick_params(left=False, bottom=False)
    st.pyplot(fig)

def predict_windspeed(norm_image):

    model = tf.keras.models.load_model('hurricane_imagery_model.h5', compile=True)
    prediction = model.predict([norm_image])
    st.write('')
    prediction_physical = int(prediction[0][0] * MAX_WIND)
    st.header('Estimated Windspeed is ' + str(prediction_physical) + ' knots.')
    return prediction_physical

def display_restart_button():

    restart = st.button("Predict Another Cyclone")
    if restart is not None:
        st.caching.clear_cache()
        lat = False
        lon = False
        datetime = False

def create_user_log(datetime, lat, lon, prediction_physical):

    request_datetime = dt.now()
    user_log_data = {'storm_datetime' : datetime,
                     'storm_lat' : lat,
                     'storm_long' : lon,
                     'predicted_windspeed' : prediction_physical}
    user_log_df = pd.DataFrame(user_log_data, index = [request_datetime])
    file_name = "/app/hurricane_imagery_app/UserLog" + str(request_datetime) + ".csv"
    user_log_df.to_csv(file_name)
    st.write(bash_string('pwd'))
    st.write(bash_string('ls'))

    repo = Repo('Hurricane_Imagery_App')
    repo.index.add([file_name])
    repo.index.commit('Adding User Log at ' + str(request_datetime))
    origin = repo.remote('origin')
    origin.push()

#     try:
#       bash_string('cp /app/hurricane_imagery_app/' + file_name + ' 

      

MAX_PIXEL = 350
MAX_WIND = 180

st.title('🌀 Tropical Cyclone Image Predictor 🌀')
st.header('Input an Infrared Satellite Image of a Tropical Cyclone to Estimate its Windspeed')

st.write(' ')

lat = False
lon = False
datetime = False

st.write("Enter the spacetime coordinates of a tropical cyclone you would like to analyze.")
st.write(
    "See [here](https://www.ssd.noaa.gov/PS/TROP/tdpositions.html) for a list of historical locations of tropical cyclones.",
    unsafe_allow_html=True)

datetime = st.text_input("Enter Datetime (Format YYYY.MM.DD.HH, (YYYY 1980-2021) (HH 24HR Multiple of 3) :",
                         key='datetime_field',
                         value = "")
lat = st.text_input("Enter Latitude of Cyclone Center (Enter South Latitudes as Negative):",
                    key='lat_field',
                    value = "")
lon = st.text_input("Enter Longitude of Cyclone Center (Enter East Longitudes as Negative):",
                    key='lon_field',
                    value = "")

if datetime and lat and lon:

    st.write("Connecting to GRADSAT-B1 ... ")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    wd = webdriver.Chrome('chromedriver',
                          chrome_options=chrome_options)

    wd.get('https://www.ncei.noaa.gov/data/geostationary-ir-channel-brightness-temperature-gridsat-b1/access/')
    year_string = datetime[0: 4]
    year_link = wd.find_element_by_link_text(year_string + '/')
    year_link.click()

    nc_file_link = wd.find_element_by_link_text("GRIDSAT-B1." + datetime + ".v02r01.nc")
    nc_file_link.click()
    st.write("Downloading Storm Data ... ")
    time.sleep(7)

    nc_file_name = nc_file_link.text
    dataset = nc.Dataset(nc_file_name)
    dataset.set_auto_mask(False)

    df_irwin = pd.DataFrame(dataset['irwin_2'][0])
    del (dataset)

    lat_center, lon_center = convert_coordinates(float(lat),
                                                 float(lon),
                                                 to_degrees=False)
    margin = 150

    centered_df = df_irwin.iloc[lat_center - margin: lat_center + margin + 1,
                  lon_center - margin: lon_center + margin + 1]
    centered_df.index = np.arange(0, 301, 1)
    centered_df.columns = np.arange(0, 301, 1)

    print("Predicting Windspeed ... ")

    norm_df = centered_df / MAX_PIXEL
    norm_image = np.array(norm_df)
    del (norm_df)
    norm_image.resize(1, 301, 301, 1)

    prediction_physical = predict_windspeed(norm_image)
    plot_cyclone(centered_df)
    create_user_log(datetime, lat, lon, prediction_physical)

    display_restart_button()

with st.expander("Predict by Manual Image Upload"):
    uploaded_file = st.file_uploader('Upload a 1 x 301 X 301 x 1 centered HURSAT IRWIN image (2D Numpy array) in CSV format.')

    if uploaded_file is not None:

        uploaded_df = pd.read_csv(uploaded_file, index_col=0)

        norm_df = uploaded_df / MAX_PIXEL
        norm_image = np.array(norm_df)
        norm_image.resize(1, 301, 301, 1)

        prediction_physical = predict_windspeed(norm_image)
        plot_cyclone(uploaded_df)
        display_restart_button()
