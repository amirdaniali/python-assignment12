## Amir Daniali
## Code the Dream
## Week 12
## Advanced Data Visualtions


import sqlite3
import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation


BASEDIR = pathlib.Path(__file__).parent.parent
print(BASEDIR)


def task2(db_path: pathlib.Path | str) -> None:
    """
    Task 2: A Line Plot with Pandas

        Create a file called cumulative.py. The boss wants to see how money is rolling in. You use SQL to access ../db/lesson.db again. You create a DataFrame with the order_id and the total_price for each order. This requires joining several tables, GROUP BY, SUM, etc.
        Add a "cumulative" column to the DataFrame. This is an interesting use of apply():

        def cumulative(row):
           totals_above = df['total_price'][0:row.name+1]
           return totals_above.sum()

        df['cumulative'] = df.apply(cumulative, axis=1)

        Because axis=1, apply() calls the cumulative function once per row. Do you see why this gives cumulative revenue? One can instead use cumsum() for the cumulative sum:

        df['cumulative'] = df['total_price'].cumsum()

        Use Pandas plotting to create a line plot of cumulative revenue vs. order_id.
        Show the Plot.


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

        if not (BASEDIR / "assignment12/cumulative_plot.gif").is_file():
            print("Animated plot not found in disk. Saving it now. Please be patient.")
            ani.save(BASEDIR / "assignment12/cumulative_plot.gif")

        plt.show()


if __name__ == "__main__":
    task2(BASEDIR / "db/lesson.db")
