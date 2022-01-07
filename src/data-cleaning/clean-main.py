# Import packages
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

# Import data
import_fp = Path("data/main/cornelia-raw.csv")
dataset = pd.read_csv(import_fp, encoding="utf-8", sep=";")

# Fix pseudo-NaN values
dataset.loc[:, "actor_first_name"] = (dataset.loc[:, "actor_first_name"]
                                      .replace(to_replace = ["[NN]",
                                                             "anonymous"],
                                               value = np.nan))

# Fix date columns format multiplicity
date_cols = ["date_day", "date_month", "date_year"]
for date_col in date_cols:
    notna_mask = dataset.loc[:, date_col].notna()
    dataset.loc[notna_mask, date_col] = (dataset
                                         .loc[notna_mask, date_col]
                                         .astype(int) # To drop right zeros
                                         .astype(str)
                                         .str.lstrip("0")) # To drop left zeros

# Fix 'source_entry' format multiplicity
alpha_mask = dataset.loc[:, "source_entry"].str[-1].str.isalpha()
dataset.loc[alpha_mask, "source_entry"] = (dataset
                                           .loc[alpha_mask, "source_entry"]
                                           .str[-1])
dataset.loc[~alpha_mask, "source_entry"] = ""
dataset.loc[:, "source_entry"] = ((dataset["date_day"].astype(str)
                                  + dataset["date_month"].astype(str)
                                  + dataset["date_year"].astype(str)
                                  + dataset["source_entry"])
                                  .str.replace("nannan", "0000"))

# Fix ENG/NL duality
replace_dict = {
    "role": {
        "apotheker": "pharmacist",
        "vergulder": "gilder",
        "glasschilder": "glass painter",
        "gelaesschryver": "glass painter",
        "goudslager": "goldsmith",
        "plaatslager": "plate craftsman"
    },
    "status": {
        "leermeester": "tutor",
        "meesterszoon": "master's son",
        "ouderman": "dean",
        "recognitie": "non-sworn in master",
        "cortosie": "non-sworn in master"
    }
}

dataset.loc[:, ["role", "status"]] = (dataset.loc[:, ["role", "status"]]
                                      .replace(to_replace=replace_dict))

# Enrich 'role' column
actor_role_year = dataset.loc[:, ["actor_first_name", "actor_surname",
                                  "date_year", "role"]]
actor_role_year["TEMP_fname"] = (actor_role_year["actor_first_name"]
                                 + " "
                                 + actor_role_year["actor_surname"])

print(actor_role_year)


# Export data
# export_fp = Path("data/cleaned/cornelia-cleaned.csv")
# dataset.to_csv(export_fp, format="utf-8", sep=";")


