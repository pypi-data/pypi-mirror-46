import pandas as pd
import numpy as np

#functions to write:

#graph missing data percentages in columns

#future:
# clean columns
def graph_missing_data(df):
    '''
    Function takes in a df and graphs the missing data per column
    as a percentage. It doens't show columns with no missing data.

    INPUT:
        - DF
    OUTPUT:
        - DF of the percentage per column.
    '''
    missing_data = {}
    for i in df.columns[1:]:
        if df[i].isnull().sum() > 0:
            missing_percent = round((df[i].isnull().sum()/df.shape[0])*100,1)
            #print (f'{missing_percent}% of column {i} is null.')
            missing_data[i]=missing_percent
    missing_percentages = pd.DataFrame.from_dict(missing_data, orient='index')
    return missing_percentages

# def main():
#     """Read the Real Python article feed"""
#     # Read URL of the Real Python feed from config file
#     cfg = ConfigParser()
#     cfg.read_string(resources.read_text("reader", "config.txt"))
#     url = cfg.get("feed", "url")
#
#     # If an article ID is given, show the article
#     if len(sys.argv) > 1:
#         article = feed.get_article(url, sys.argv[1])
#         viewer.show(article)
#
#     # If no ID is given, show a list of all articles
#     else:
#         site = feed.get_site(url)
#         titles = feed.get_titles(url)
#         viewer.show_list(site, titles)
#
# if __name__ == "__main__":
#     main()
