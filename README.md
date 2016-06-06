# USA names

This code allows you to look at historical patterns in U.S. names.  Maybe you're trying to find a baby name.

Two main features:

  1. For a given name or set of names, look at the popularity over time.
  2. For a given name, get a list of names with similar historical trends.

## Usage
First run the download script, `download_data.sh`.
Then explore baby names interactively, like
```
import names
x = names.Names()
x.viz('zelda')
x.viz('zelda jim noah')
x.similar_names('zelda', show=1)
x.viz_similar('zelda')
```

## Data
Data comes from the U.S. Social Security Administration, described at https://www.ssa.gov/oact/babynames/limits.html.  Download with `download_data.sh`.  ~20 MB unzipped.

## Examples
Name similarity is based only on the L1 distance between (log) popularity curves, but it's able to pick up on a surprising amount of information.

**Zelda** and other names from the early 20th century:
<img src="https://github.com/rkeisler/babynames/blob/master/figs/ex1.png" width="1000px"/>

**Traci** and other 1970s girl names ending in "i":
<img src="https://github.com/rkeisler/babynames/blob/master/figs/ex2.png" width="1000px"/>

**Geronimo** and other uncommon Spanish names:
<img src="https://github.com/rkeisler/babynames/blob/master/figs/ex3.png" width="1000px"/>

**Noah** is surging:
<img src="https://github.com/rkeisler/babynames/blob/master/figs/ex4.png" width="1000px"/>
