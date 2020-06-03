# 2019-wid

Extracts of the [World Inequality Database](https://wid.world/).
## Data structure

Income data table are given per country.
The attributes present in the tables are:

* **year** the year for the data
* **low** the lower bound of the population quantile (from 0. to 1.)
* **high** the upper bound of the population quantile (from 0. to 1.)
* **width** the width of the quntile (high-low)
* **share** the share of the total income captured by this [low, high] quantile
* **cumul** the cumulative share of the quantiles, i.e. the share of [0., high]

# Steps to reproduce Social Taxation Graphs

- Start a web server in the current directory of each project. One way is to run python command:

```sh
python -m SimpleHTTPServer 8000
```
- Go to http://localhost:8000/whole_graph.html on your browser.

# What's in this directory!
### stacked_bar_chart
* [generate_social_taxation_data.py] - Python program that automates generation of data for a specific country for Social Taxation idea.
* [whole_graph.html] - HTML file containing D3 manipulations to show the final graph.
* [Rest of files]  - Data taken from original dataset given in the project + data generated by Python program above. To add a new country, its .tsv file from original dataset should be added to the directory *social_taxation_data*. 

### graph chart
* **data/** the data in [tsv](https://bl.ocks.org/mbostock/3305937).
	* **countries.tsv** country codes
	* **income/** income share per country
* **viz/stacked_bar_chart** sample visualisation
* **vendor/** vendorized d3 library

