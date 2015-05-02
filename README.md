# Wodify
Exports all athlete weight-lifting information from wodify.com and provides an interface for comparing athletes against each other.

## Exporting
Data is exporting using Selenium. The client traverses the site using administrative credentials and individually exports each athletes data. The data is then merged and saved to a database. Once the data is stored in the database a simple interface is provided for comparing athletes each other.

## Roadmap
1. Currently Selenium uses the Chrome browser to export information. In the future I'd like to use a headless browser. This would allow the browser to run soley on a command line interface.
2. Profile page for every athlete.
3. Logic that can takes sets of data and compare which athletes rank closest to each other.
4. An API so that others can easily query the data and display it as they see fit on an interface of their choosing.