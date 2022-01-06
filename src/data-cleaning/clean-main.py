# Import packages
from pathlib import Path

import numpy as np
import pandas as pd

# Import data
target = Path("data/main/cornelia-raw.csv")
dataset = pd.read_csv(target, encoding="utf-8", sep=";")

# Fix pseudoNaN values
dataset.loc[:, "actor_first_name"] = (dataset.loc[:, "actor_first_name"]
                                      .replace(to_replace = ["[NN]",
                                                             "anonymous"],
                                               value = np.nan))
# Fix 'source_entry' format multiplicity

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

