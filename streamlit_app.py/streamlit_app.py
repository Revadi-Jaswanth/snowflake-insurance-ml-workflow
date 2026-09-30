import streamlit as st
from snowflake.snowpark.context import get_active_session

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Insurance Cost Predictor",
    page_icon="💰",
    layout="centered"
)

# ---------------------------------------------------------
# Snowflake Session
# ---------------------------------------------------------

session = get_active_session()

# Explicitly set Snowflake context
session.sql("USE WAREHOUSE ML_PIPELINE_WH").collect()
session.sql("USE DATABASE INSURANCE_ML").collect()
session.sql("USE SCHEMA ML_PIPE").collect()

# ---------------------------------------------------------
# Application Header
# ---------------------------------------------------------

st.title("💰 Insurance Cost Predictor")

st.write(
    "Predict medical insurance charges using our "
    "XGBoost machine learning model registered in Snowflake."
)

st.divider()

# ---------------------------------------------------------
# User Inputs
# ---------------------------------------------------------

st.subheader("Customer Information")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30,
        step=1
    )

    sex = st.selectbox(
        "Sex",
        ["male", "female"]
    )

    bmi = st.number_input(
        "BMI",
        min_value=10.0,
        max_value=60.0,
        value=25.0,
        step=0.1
    )

with col2:
    children = st.number_input(
        "Number of Children",
        min_value=0,
        max_value=10,
        value=0,
        step=1
    )

    smoker = st.selectbox(
        "Smoker",
        ["no", "yes"]
    )

    region = st.selectbox(
        "Region",
        [
            "southwest",
            "southeast",
            "northwest",
            "northeast"
        ]
    )

st.divider()

# ---------------------------------------------------------
# Prediction
# ---------------------------------------------------------

if st.button(
    "🔮 Predict Insurance Charges",
    width="stretch"
):

    with st.spinner("Generating prediction..."):

        try:

            query = f"""
            SELECT
                (
                    MODEL(
                        INSURANCE_ML.ML_PIPE.INSURANCE_CHARGES_MODEL,
                        V2
                    )!predict(
                        {int(age)},
                        '{sex}',
                        {float(bmi)},
                        {int(children)},
                        '{smoker}',
                        '{region}'
                    )
                )['output_feature_0']::FLOAT AS PREDICTED_CHARGES
            """

            result = session.sql(query).collect()

            prediction = float(
                result[0]["PREDICTED_CHARGES"]
            )

            st.success("Prediction generated successfully!")

            st.metric(
                label="Predicted Insurance Charges",
                value=f"${prediction:,.2f}"
            )

            st.info(
                "Model: INSURANCE_CHARGES_MODEL V2"
            )

        except Exception as e:

            st.error("Prediction failed.")
            st.code(str(e))