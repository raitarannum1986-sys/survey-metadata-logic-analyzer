from io import BytesIO
import pandas as pd


def generate_analysis_export(
    variables_df,
    logic_df,
    tags_df,
    profile_df
):
    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        variables_df.to_excel(
            writer,
            sheet_name="Variables",
            index=False
        )

        logic_df.to_excel(
            writer,
            sheet_name="Logic",
            index=False
        )

        tags_df.to_excel(
            writer,
            sheet_name="XML_Tags",
            index=False
        )

        profile_df.to_excel(
            writer,
            sheet_name="Survey_Profile",
            index=False
        )

    return output.getvalue()