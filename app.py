import streamlit as st
import os
from main import run_pipeline

st.title("AI CAD Generator")

product = st.selectbox(
    "Select Product",
    ["plate","bracket","flange","motor_mount","gear_plate","assembly","u_channel","cabinet","control_box","enclosure","machine_frame"]
)

uploaded_file = st.file_uploader("Upload Excel File")

if uploaded_file:

    with open("input.xlsx","wb") as f:
        f.write(uploaded_file.read())

    st.success("Excel uploaded successfully")

    if st.button("Generate CAD Model"):

        with st.spinner("Generating CAD Model..."):

            result = run_pipeline(product,"input.xlsx")

        if result is None or result["status"]=="error":

            st.error("Error during generation")

        else:

            st.success("CAD Model Generated Successfully")

            st.write("Generated File:",result["cad_file"])

            if os.path.exists(result["cad_file"]):

                with open(result["cad_file"],"rb") as f:

                    st.download_button(
                        "Download CAD File",
                        f,
                        file_name=os.path.basename(result["cad_file"])
                    )

            else:

                st.error("CAD file not found in outputs folder")