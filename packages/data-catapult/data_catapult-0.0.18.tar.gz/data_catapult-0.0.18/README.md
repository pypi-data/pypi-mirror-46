# Catapult bulk data import library

### Example usage:
```
db = driver.MonetDBDriver(conn)
db.to_sql(df, "my_schema_name", "my_table_name")
```

### Clickhouse specific examples

To make columns Nullable users must explicitly list them in the nullable_list
parameter for to_sql, otherwise columns will be assumed to be non-nullable
for performance reasons.

Note that imports for floating point types to columns
that are non-nullable with null values, those null values will be imported as NaNs,
which may interfere with the summations of columns (as 1 + NaN = NaN).

```
from data_catapult.database import clickhouse as driver
df = pd.read_csv("mycsv.csv")
db = driver.ClickhouseDriver(host="myhost.com", database="mydb")
db.to_sql(df, "my_table", pk=["pk1", "pk2"], nullable_list=['nullcol1', 'nullcol2'])
```