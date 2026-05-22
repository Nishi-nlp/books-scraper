import pandas as pd


def export_to_csv(data, filename="data/books.csv"):
    df = pd.DataFrame(data)

    df.to_csv(filename, index=False)