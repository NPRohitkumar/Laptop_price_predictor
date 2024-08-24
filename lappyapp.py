import streamlit as st
html_temp='''
<h1 style="color: yellow;text-align: center;">Laptop Price Predictor</h1>
<div style="background-color: cornflowerblue; color: white; width: 550px; margin: 0 auto;border-radius: 10px; text-align: center; height:130px;">
    <p style="font-weight: bolder">This app is designed to predict the laptop price based on various components.</p>
    <p style="font-weight: bolder">Once the configuration details of the laptop is entered</p>
    <p style="font-weight: bolder">please click on PREDICT to get the estimated price of the laptop.</p>
</div>'''
st.markdown(html_temp,unsafe_allow_html=True)

import numpy as np
import pickle as pkl 
pipe=pkl.load(open('pipe.pkl','rb'))
df=pkl.load(open('df.pkl','rb'))

company=st.selectbox("Brand",df['Company'].unique(),index=4)
Laptop_type=st.selectbox("Laptop_Type",df['TypeName'].unique(),index=1)
cpu=st.selectbox("Processor",df['Cpu'].unique())
ram=st.selectbox('RAM(in GB)',[2,4,6,8,12,16,24,32,64,128],index=3)
gpu=st.selectbox('Graphics Card',df['Gpu'].unique(),index=2)
os=st.selectbox('OS',df['OpSys'].unique(),index=2)
weight=st.number_input('Weight of the laptop(in kg)',0.6,4.7,2.2,0.1)
ips=st.selectbox('IPS Display',['No','Yes'])
touchscreen=st.selectbox('Touchscreen',['No','Yes'])
screen_size=st.number_input("Size of the screen(in Inches)",min_value=10.0,max_value=18.5,value=15.0,step=0.1)
resolution=st.selectbox("Screen Resolution",['1920x1080', '1366x768', '3840x2160', '3200x1800', '2560x1440',
       '1600x900', '2560x1600', '2304x1440', '2256x1504', '1920x1200',
       '1440x900', '2880x1800', '2400x1600', '2160x1440', '2736x1824'])

if st.button("PREDICT PRICE"):
  ppi=None
  if touchscreen == 'Yes':
    touchscreen = 1
  else:
    touchscreen = 0
  if ips == 'Yes':
    ips = 1
  else:
    ips = 0
  X_res=int(resolution.split('x')[0])
  Y_res=int(resolution.split('x')[1])
  ppi=((X_res*2)+(Y_res*2))*0.5/screen_size
  query=np.array([[company,Laptop_type,cpu,ram,gpu,os,weight,ips,touchscreen,ppi]])
  op=np.exp(pipe.predict(query))
  st.subheader("The predicted price of the laptop for the above mentioned configuration is:")
  st.subheader("Rs."+str(round(op[0])))
