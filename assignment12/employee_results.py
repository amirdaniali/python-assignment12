## Amir Daniali
## Code the Dream
## Week 12
## Advanced Data Visualtions

import sqlite3
import pathlib
import pandas as pd
import matplotlib.pyplot as plt

BASEDIR = pathlib.Path(__file__).parent.parent
print(BASEDIR)


def task1(db_path: pathlib.Path | str) -> None:
    """
    Create a file called employee_results.py.
    Load a DataFrame called employee_results using SQL. Copy the db/lesson.db database from your python_homework folder to your python-assignment12 folder. Copy the db folder and the lesson.db file within it. This can be done using the cp -r command. In your assignment12 folder, connect to ../db/lesson.db. You use SQL to join the employees table with the orders table with the line_items table with the products table. You then group by employee_id, and you SELECT the last_name and revenue, where revenue is the sum of price * quantity. Ok, that's a lot of SQL to mess with, so here is the statement you need:

    SELECT last_name, SUM(price * quantity) AS revenue FROM employees e JOIN orders o ON e.employee_id = o.employee_id JOIN line_items l ON o.order_id = l.order_id JOIN products p ON l.product_id = p.product_id GROUP BY e.employee_id;

    Use the Pandas plotting functionality to create a bar chart where the x axis is the employee last name and the y axis is the revenue.
    Give appropriate titles, labels, and colors.
    Show the plot.

    """
    results = None

    try:

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        suggested_query = """
            SELECT last_name, SUM(price * quantity) AS revenue
            FROM employees e 
            JOIN orders o ON e.employee_id = o.employee_id 
            JOIN line_items l ON o.order_id = l.order_id 
            JOIN products p ON l.product_id = p.product_id 
            GROUP BY e.employee_id;
        """

        # I never shy away from getting some SQL practice.
        my_query = """
            SELECT e.last_name, SUM(p.price*li.quantity) AS revenue
            FROM employees e
            JOIN orders o
                ON e.employee_id = o.employee_id 
            JOIN line_items li
                ON li.order_id = o.order_id
            JOIN products p
                ON p.product_id = li.product_id
            GROUP BY e.employee_id;
"""

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
        df = pd.DataFrame(results, columns=["last_name", "revenue"])
        df.plot(
            x="last_name",
            y="revenue",
            kind="bar",
            color="purple",
            title="Revenue of each employee",
        )

        plt.show()


if __name__ == "__main__":
    task1(BASEDIR / "db/lesson.db")
