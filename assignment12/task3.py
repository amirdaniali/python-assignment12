## Amir Daniali
## Code the Dream
## Week 12
## Advanced Data Visualtions


from datetime import date
import sqlite3
import pathlib
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.data as pldata
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation


BASEDIR = pathlib.Path(__file__).parent.parent
print(BASEDIR)


def task3(db_path: pathlib.Path | str) -> None:
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
    results = None

    try:

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        my_query = """
            SELECT o.order_id, SUM(p.price*li.quantity) AS revenue, o.date
            FROM orders o
            JOIN line_items li
                ON li.order_id = o.order_id
            JOIN products p
                ON p.product_id = li.product_id
            GROUP BY o.order_id;
"""
        #  I'm getting Order Dates too. Because I think it makes more sense to show a plot
        # with dates than to make the x-axis be about order ids.

        cursor.execute(my_query)
        results = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()

    if results:
        df = pd.DataFrame(results, columns=["order_id", "total_price", "date"])
        df["cumulative"] = df["total_price"].cumsum()
        df["date"] = pd.to_datetime(df["date"])

        #
        df.plot(
            x="date",
            xlabel="",
            y="cumulative",
            kind="line",
            color="purple",
            title="Cumulative Revenue",
        )

        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.YearLocator(base=5))  # every 5 years
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

        plt.gcf().autofmt_xdate(rotation=45)

        plt.grid(True, linestyle="--", alpha=0.5)

        ax.set_xlim(pd.Timestamp("1970-01-01"), pd.Timestamp("2025-09-09"))

        plt.show()

        #  What the excerise wanted.
        df.plot(
            x="order_id",
            xlabel="",
            y="cumulative",
            kind="line",
            color="green",
            title="Cumulative Revenue",
        )
        plt.show()

        # Animated Plot as a bonus
        # I love how amazing it is to create visualisations with python.
        fig, ax = plt.subplots()
        (line,) = ax.plot([], [], color="gold")
        ax.set_title("Cumulative Revenue (With Animation!!!!)")
        ax.set_xlabel("Year")
        ax.set_ylabel("Cumulative Revenue")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.xaxis.set_major_locator(mdates.YearLocator(base=5))
        plt.xticks(rotation=45)

        # Initialization function
        def init():
            ax.set_xlim(df["date"].min(), df["date"].max())
            ax.set_ylim(0, df["cumulative"].max() * 1.05)
            line.set_data([], [])
            return (line,)

        # Animation function
        def update(frame):
            x = df["date"][:frame]
            y = df["cumulative"][:frame]
            line.set_data(x, y)
            return (line,)

        # Create animation
        ani = animation.FuncAnimation(
            fig,
            update,
            frames=len(df),
            init_func=init,
            blit=True,
            interval=20,
            repeat=False,
        )
        ani.save(BASEDIR / "assignment12/cumulative_plot.gif")

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    task3(BASEDIR / "db/lesson.db")
