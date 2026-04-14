import pandas as pd
from pathlib import Path

root = Path('db')

for tsv in root.glob('*.tsv'):
    print(tsv)
    df = pd.read_csv(tsv, sep='\t', na_values=R'\N')
    df.to_parquet(root / (tsv.stem + '.new.parquet'))
