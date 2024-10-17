# Exploratory data analysis: conclusions and observations

After the detailed exploration of data, one can make the following conclusion as to the basic data analysis:

1. Data with which we are to be working with represent (*i*) information about different actions of users with items, (*ii*) data about categories of recommended items and groups of categories (parent categories), as well as (*iii*) properties of items.
2. Not all categories can be a part of a larger group: it was found that some categories (25 categories, to be exact) do not have parent categories and thus do not have any further classification. 
3. Different user actions encompass usual events: viewing of items, adding to cart and the transaction itself. The highest share of such actions relates to items views as it so happens in reality. The other shares refer to adding to cart and transaction but, however, not all adding to cart actions result in the transactions taking place.
4. Properties of items represent two datasets with a diverse information about different features and their values. A problem with data format has been found which could have appeared during web-scrapping of data.
