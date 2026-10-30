# Emily Forestier
# A Problem with Presidents Project

# Library Usage:
# - DateTime library to handle real dates instead of just strings
# - NumPy library for numerical operations
# - Pandas library for data manipulation and analysis

from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Raw string to handle the backslashes in the file path
president_path = r"C:\Users\fores\Downloads\a_problem_with_presidents\U.S. Presidents Birth and Death Information - Sheet1.csv"


def analyze(path):

    frame = pd.read_csv(path)

    # Converts times into datetime objects 
    # If date is invalud, it will be converted to NaT (Not a Time)
    frame["bday"] = pd.to_datetime(frame["BIRTH DATE"], errors="coerce")
    frame["dod"] = pd.to_datetime(frame["DEATH DATE"], errors="coerce")

    today = pd.Timestamp(datetime.today().date())
    # Fills the missing values in the column in the date of death (presidents still alive) with todays date
    frame["find_dod"] = frame["dod"].fillna(today)

    # Calculates the birth year, days lived, years lived, and months lived for each president
    frame["year_of_birth"] = frame["bday"].dt.year
    frame["lived_days"] = (frame["find_dod"] - frame["bday"]).dt.days
    frame["lived_years"] = frame["lived_days"] / 365.25
    # Calculation: Gets difference of years and multiplies by 12, then adds on leftover months by subtracting birth from death month
    frame["lived_months"] = (
        (frame["find_dod"].dt.year - frame["bday"].dt.year) * 12
        + (frame["find_dod"].dt.month - frame["bday"].dt.month)
    )

    # Creates a new table of the 10 longest lived presidents with their birth year, years lived, and days lived (longest lived at the top)
    longest_lived = frame.sort_values(by="lived_days", ascending=False).head(10)[
        ["PRESIDENT", "year_of_birth", "lived_years", "lived_days"]
    ]

    print(longest_lived, "\n")

    shortest_lived = frame.sort_values(by="lived_days", ascending=True).head(10)[
        ["PRESIDENT", "year_of_birth", "lived_years", "lived_days"]
    ]

    print(shortest_lived, "\n")

    # Creates new table of days lived of presidents who already died (NaT values dropped)
    days_lived_cleaned = frame["lived_days"].dropna()

    stats = {
        "Mean": days_lived_cleaned.mean(),
        "Median": days_lived_cleaned.median(),
        "Min": days_lived_cleaned.min(),
        "Max": days_lived_cleaned.max(),
        "Standard Deviation": days_lived_cleaned.std(),
    }

    # Creates vertical table of statistic and values from the stats dictionary (each type of stat under "Statistic" and the corresponding value under "Value")
    stats_frame = pd.DataFrame(list(stats.items()), columns=["Statistic", "Value"])
    print(stats_frame)

    plt.figure(figsize=(10, 6))

    sns.histplot(days_lived_cleaned, kde=True, bins=12, color="teal")

    plt.title(
        "Distribution of Lifespans (Days Lived) Among Deceased U.S. Presidents",
        fontsize=14,
        pad=15,
    )
    plt.xlabel("Total Days Lived", fontsize=12)
    plt.ylabel("Frequency (Number of Presidents)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.savefig(
        "president_lifespan_distribution.png", dpi=300, bbox_inches="tight"
    )

    plt.show()

def main():
    analyze(president_path)

if __name__ == "__main__":
    main()
