import json
f = open('dataBase.json', 'r', encoding='utf-8')
data = json.load(f)
product = ""
bimSwarmDB = []
bimSwarmProductsDB = []
for i in range(len(data)):
    bimSwarmDB.append(str(data[i]['Supplier']))


def productsListing(df):
    df = df['Supplier']
    df = df.drop_duplicates()
    return df

def suppliersProductListing(df, supplier):
    df = df[df['Supplier'] == supplier]
    df = df['Product']
    df = df.drop_duplicates()
    return df

def product2Id(item):
    productID = ""
    for j in range(len(data)):
            for product in range(len(data[j]['products'])):
                for key, value in data[j]['products'][product].items():
                    if item == value:
                        productID = str(key)
                    else:
                        continue
    return productID


def supplier2Id(id):
    bim_swarm_products_db = []
    for j in range(len(data)):
        if id == data[j]['Supplier']:
            id = data[j]['OrgId']
            for product in range(len(data[j]['products'])):
                for key, value in data[j]['products'][product].items():
                    bim_swarm_products_db.append(value)
    return id, bim_swarm_products_db


def updateOrgDf(df, supplier):
    if supplier == "":
        return df
    return df[df['Supplier'] == supplier]

def updateProdDf(df, product):
    return df[df['Product'] == product]