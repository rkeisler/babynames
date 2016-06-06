# baby names - A DATA-DRIVEN APPROACH 

This code allows you to look at historical patterns in U.S. names.

Two main features:
1) For a given name or set of names, look at the popularity over time.
2) For a given name, get a list of names with similar historical trends.

## Usage
First run the download script, `download_data.sh`.
Then explore baby names interactively.
```
import names
import names
x = names.Names()
x.viz('zelda')
x.viz('zelda jim noah')
x.similar_names('zelda', show=1)
x.viz_similar('zelda')
```

## Data
Data comes from the U.S. Social Security Administration, described at https://www.ssa.gov/oact/babynames/limits.html.  Download with `download_data.sh`.  ~20 MB unzipped.

