import json
import psycopg2


def connect():
    orgID = []
    orgName = []
    orgDict = []
    orgProducts = []
    productID = []
    productSupplier= []
    productName = []
    productDict = []
    ptgId = []
    ptgName = []
    ptgDict = []
# Connect to the PostgreSQL database server
    conn = None
    try:

        conn = psycopg2.connect(
            host="bimswarm.online",
            port="5432",
            database="swarmdb",
            user="swarmdb",
            password="swarmSecret")
# create a cursor
        cur = conn.cursor()
# Organizations Name and ID into Dictionary
        postgreSQL_select_Query = "select * from organisation"
        cur.execute(postgreSQL_select_Query)
        organizations = cur.fetchall()
        for row in organizations:
            orgID.append(row[0])
            orgName.append(row[5])
        for index,item in enumerate(orgID):
            org = {}
            org["Supplier"] = orgName[index]
            org["OrgId"] = orgID[index]
            org["products"] = []
            orgDict.append(org)
        postgreSQL_select_Query = "select * from product"
        cur.execute(postgreSQL_select_Query)
        products = cur.fetchall()
        for row in products:
            productID.append(row[0])
            productSupplier.append(row[2])
            productName.append(row[5])
        for index,item in enumerate(productID):
            product = {}
            product[productID[index]] = productName[index]
            product["OrgId"] = productSupplier[index]
            productDict.append(product)
        postgreSQL_select_Query = "select * from product_type_group"
        cur.execute(postgreSQL_select_Query)
        products = cur.fetchall()
        for row in products:
            ptgId.append(row[0])
            ptgName.append(row[2])
        for index,item in enumerate(ptgId):
            ptg={}
            ptg[ptgId[index]] = ptgName[index]
            ptgDict.append(ptg)
        for row in productDict:
            orgProducts={}
            for rows in orgDict:
                if row["OrgId"] == rows["OrgId"]:
                    orgProducts.update({list(row.keys())[0] : row[list(row.keys())[0]]})
                    rows["products"].append(orgProducts)
        with open('dataBase.json', 'w') as fout:
            json.dump(orgDict, fout)
        with open('ptg.json', 'w') as fout:
            json.dump(ptgDict, fout)
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == '__main__':
    connect()
