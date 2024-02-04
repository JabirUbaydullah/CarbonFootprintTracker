import streamlit as st
import uuid
import pandas as pd
import plost

row_store = list()


def remove_row(id):
    st.session_state["input_rows"].remove(str(id))


def add_row():
    id = uuid.uuid4()
    st.session_state["input_rows"].append(str(id))


def create_input_row(id):
    row = st.empty()
    ingredient_column, amount_column, unit_column, remove_row_column = row.columns(4)

    ingredient = ingredient_column.selectbox(
        "Choose Ingredients",
        st.session_state["carbon_footprint_data"].keys(),
        label_visibility="collapsed",
        key=f"ingredient-selectbox-{id}",
    )

    amount = amount_column.number_input(
        "Choose Amount",
        min_value=0,
        max_value=100000,
        label_visibility="collapsed",
        value=st.session_state["ingredient_serving_amounts"][ingredient],
        key=f"amount-number-input-{id}",
    )

    unit_list = ["g", "kg", "oz", "lbs", "mL", "L"]
    unit = unit_column.selectbox(
        "Choose Unit",
        unit_list,
        index = unit_list.index(st.session_state["ingredient_serving_units"][ingredient]),
        label_visibility="collapsed",
        key=f"unit-selectbox-{id}",
    )

    remove_row_column.button(
        ":grey[:heavy_multiplication_x:]",
        type="primary",
        key=f"remove-row-{id}",
        on_click=remove_row,
        args=[id],
    )

    return (ingredient, amount, unit)


def convert_units(amount, unit):
    if unit == "g" or unit == "mL":
        return amount / 1000
    elif unit == "lbs":
        return amount / 2.20462
    elif unit == "oz":
        return amount / 35.274
    else:
        return amount


def calculate_carbon_footprint():
    total_carbon_footprint = 0
    individual_carbon_footprints = list()
    for row in row_store:
        ingredient, amount, unit = row
        individual_carbon_value = (
            convert_units(amount, unit)
            * st.session_state["carbon_footprint_data"][ingredient]
        )
        individual_carbon_footprints.append((ingredient, individual_carbon_value))
        total_carbon_footprint += individual_carbon_value
    return round(total_carbon_footprint, 5), individual_carbon_footprints


def calculate_equivalent_driving_miles(carbon_footprint):
    # .1435371022 is the kg CO2e per mile of Toyota RAV4 2024
    return round(carbon_footprint / 0.1435371022, 5)


def main():
    st.title("Carbon Footprint Tracker")
    st.subheader("Instructions", divider="blue")

    description = "<p>This website allows the user to enter in specific amounts of ingredients that they are consuming and will show the total carbon footprint of all of the ingredients together.</p>"

    st.markdown(description, unsafe_allow_html=True)
    st.text(" ")

    if "input_rows" not in st.session_state:
        st.session_state["input_rows"] = list()

    if "carbon_footprint_data" not in st.session_state:
        df = pd.read_csv("food-carbon-footprint.csv")
        st.session_state["carbon_footprint_data"] = dict(
            zip(df["Ingredient"], df["kg CO2 produced per kg of product"])
        )
        st.session_state["ingredient_serving_amounts"] = dict(zip(df["Ingredient"], df["Serving Amount"]))
        st.session_state["ingredient_serving_units"] = dict(zip(df["Ingredient"], df["Serving Unit"]))

    for r in st.session_state["input_rows"]:
        row = create_input_row(r)
        row_store.append(row)

    st.button("Add Ingredient", on_click=add_row)

    st.text(" ")
    
    metric_row = st.empty()
    carbon_footprint_column, miles_column = metric_row.columns(2)
    
    carbon_footprint, carbon_footprint_list = calculate_carbon_footprint()
    chart_df = pd.DataFrame(
        carbon_footprint_list, columns=["Ingredient", "Carbon Footprint (kg CO₂e)"]
    )

    st.text(" ")
    st.text(" ")

    plost.donut_chart(
        data=chart_df, theta="Carbon Footprint (kg CO₂e)", color="Ingredient"
    )
    carbon_footprint_column.metric(
        label=":blue[Total Carbon Footprint]", value=f"{carbon_footprint} kg CO₂e"
    )
    miles_column.metric(
        label=":blue[Total Equivalent Miles Driven]",
        value=f"{calculate_equivalent_driving_miles(carbon_footprint)} miles",
        help="Based on kg CO2e per mile of Toyota RAV4 2024",
    )


if __name__ == "__main__":
    main()
