import pandas as pd


def export_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8-sig")


def export_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)