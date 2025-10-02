## Amir Daniali
## Code the Dream
## Week 12
## Advanced Data Visualtions


import pathlib
import plotly.express as px
import plotly.data as pldata
import pandas as pd

BASEDIR = pathlib.Path(__file__).parent.parent


def task3(df: pd.DataFrame) -> None:
    """
    Task 3: Interactive Visualizations with Plotly

        Load the Plotly wind dataset, via the following:

        import plotly.express as px
        import plotly.data as pldata
        df = pldata.wind(return_type='pandas')

        Print the first and last 10 lines of the DataFrame.
        Clean the data. You need to convert the 'strength' column to a float. Use of str.replace() with regex is one way to do this, followed by type conversion.
        Create an interactive scatter plot of strength vs. frequency, with colors based on the direction.
        Save and load the HTML file, as wind.html. Verify that the plot works correctly.

    """
    print(df.head(10))
    print(df.tail(10))

    # if not (BASEDIR / "assignment12/wind.csv").is_file:
    #     df.to_csv(BASEDIR / "assignment12/wind.csv")

    df["strength_float"] = df["strength"].apply(parse_strength)

    fig = px.scatter(
        df,
        x="strength_float",
        y="frequency",
        labels={
            "frequency": "Frequency",
            "strength_float": "Strength (1 to  6+)",
            "direction": "Direction of Wind",
        },
        color="direction",
        title="Wind Data, Strength vs. Frequency",
        hover_data=["frequency"],
    )

    fig.write_html(BASEDIR / "assignment12/wind.html", auto_open=True)


def parse_strength(value) -> float | None:
    if "+" in value:
        return float(value.replace("+", "")) + 0.5
    elif "-" in value:
        parts = value.split("-")
        return (float(parts[0]) + float(parts[1])) / 2
    else:
        try:
            return float(value)
        except:
            return None


if __name__ == "__main__":

    df = pldata.wind(return_type="pandas")

    task3(df)
