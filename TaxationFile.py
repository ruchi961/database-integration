#EAI Practical
#Developing API - Python side - Taxation module
from flask import Flask
from flask import request,jsonify
import mysql.connector
import requests
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="EAIapplication"
)



app=Flask(__name__)


print(mydb)
@app.route("/Taxation",methods=['POST'])
def Taxation():
        global mydb
        data = request.get_json()
        print(data)
        products_list=""
        Invoice_Total=0
        for i in data["Products"]:
                products_list = products_list+i['Product']+","
                Invoice_Total = Invoice_Total + int(i['Cost'])
        Tax_value=18
        print(products_list,Tax_value,Invoice_Total)
        
        Tax_amount = (Invoice_Total*Tax_value)/100
        Total_amount = Tax_amount+Invoice_Total
        print(Total_amount)
        
        mycursor = mydb.cursor()
        sql = "INSERT INTO Invoice (ProductsPurchased,TotalPrice,Tax,TaxAmount, Location,TotalPriceTax) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (products_list, Invoice_Total,Tax_value,Tax_amount,data['Location'],Total_amount)
        mycursor.execute(sql, val)
        cus_id =  mycursor.lastrowid
        mydb.commit()
        mycursor.close()
        url = 'http://localhost:8080/taxCh'
        myobj = {'ProductsPurchased':products_list,
                 'TotalPrice':Invoice_Total,'Tax':Tax_value,
                 'TaxAmount':Tax_amount,
                 'Location':data['Location'],'TotalPriceTax': Total_amount,'CustomerID':cus_id}
        print(myobj)

        x = requests.post(url, json = myobj)
        print(x.text)
        
        status="success"
        return jsonify(status,200)

app.run()
