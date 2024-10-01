import pandas as pd


def crawlCul(query, verbose=False):
    query = query.replace("\n", "").replace("\t", "").replace("\\", "")
    url = f"https://www.cellosaurus.org/search?query=" + query
    if verbose:
        print(f"Crawling URL: {url}")
    try:
        extracted_tables = pd.read_html(url)
        if len(extracted_tables) > 0:
            if verbose:
                print(f"Found {len(extracted_tables[0])} results for query: {query}")
            return list(extracted_tables[0][0]), list(extracted_tables[0][2]), list(extracted_tables[0][1])
        else:
            if verbose:
                print(f"No results found for query: {query}")
            return [], [], []
    except ValueError as e:
        if verbose:
            print(f"Error crawling {url}: {str(e)}")
        return [], [], []


def crawlEth(query, verbose=False):
    query = query.replace("\n", "").replace("\t", "").replace("\\", "")
    url = f"https://www.cellosaurus.org/" + query
    if verbose:
        print(f"Crawling URL for ethnicity: {url}")
    try:
        extracted_tables = pd.read_html(url)
        info = extracted_tables[0]
        name = info[info[0] == "Cell line name"][1].iloc[0] if not info[info[0] == "Cell line name"].empty else ""
        gender = info[info[0] == "Sex of cell"][1].iloc[0] if not info[info[0] == "Sex of cell"].empty else ""
        age = info[info[0] == "Age at sampling"][1].iloc[0] if not info[info[0] == "Age at sampling"].empty else ""
        category = info[info[0] == "Category"][1].iloc[0] if not info[info[0] == "Category"].empty else ""
        species = info[info[0] == "Species of origin"][1].iloc[0] if not info[info[0] == "Species of origin"].empty else ""
        
        ancestry_table = next((table for table in extracted_tables if list(table.columns) == ['Origin', '% genome']), pd.DataFrame({'A' : []}))
        
        if verbose:
            print(f"Found information for {name}: Gender: {gender}, Age: {age}, Category: {category}, Species: {species}")
        
        return name, gender, category, age, species, ancestry_table
    except Exception as e:
        if verbose:
            print(f"Error crawling {url}: {str(e)}")
        return "", "", "", "", "", pd.DataFrame({'A' : []})


# tables = crawl(f"https://www.cellosaurus.org/search?query=lung+cells")
# print(type(tables[0]))
# table = crawlEth("CVCL_0025")
# print(list(table[table[0] == "Sex of cell"][1])[0])
# print(type(tables))
# for table in tables:
#     print(list(table.columns))
