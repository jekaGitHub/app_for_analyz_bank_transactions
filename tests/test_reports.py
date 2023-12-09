import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category(df_list):
    df_1 = pd.DataFrame(df_list)
    results = spending_by_category(df_1, "Супермаркет", "07.12.2023").to_dict(orient="records")
    assert [item["Категория"] for item in results] == ["Супермаркет", "Супермаркет"]
