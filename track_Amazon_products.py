
import os  
import urllib2
import urllib
import pandas 
import csv
import time
from time import sleep
def try_amazon(url,wait):
     if wait == 8:
         print "Try Amazon one more time",wait
     sleep(wait)

     try: 
         f = urllib.urlopen(url)
         page = f.read()
         f.close()
#  print page
         startlink = page.find('To discuss automated access to Amazon data')
         if startlink != -1: 
             if wait >= 8:
                 return -1  # amazon finally failed
             else:
                 return try_amazon(url,wait+2)
         else:
             return page
     except:
         return ""
    
    

def get_page(url):#This function is just to return the webpage contents; the source of the webpage when a url is given.
 try:
#  print url
  f = urllib.urlopen(url)
  page = f.read()
  f.close()
#  print page
  startlink = page.find('To discuss automated access to Amazon data')
  if startlink != -1: # this means amazon won't return the page
 #try one more time
      return try_amazon(url, 2)
               
  else:
      return page
 except: 
  return ""



'''
def get_page(url):
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)          
        page = response.read()
#        req.close()
        
        startlink = page.find('To discuss automated access to Amazon data')
        if startlink != -1: # this means amazon won't return the page
            return -1
        else:
            return page
    except: 
        return ""
'''
def get_price(page):
#    print page
    prime = True
    start_link = page.find('priceblock_ourprice')
 #   print start_link 
    if start_link == -1: 
        prime = False  # this indicates the product is not prime
        start_link = page.find('priceblock_saleprice')
        if start_link == -1:
 
            start_link = page.find('price3P')
            if start_link == -1:  #This indicates product is out of stock:
                prime = "OUT"
                return "OUT",prime
        
    # now look for $ sign
    start_price = page.find('$', start_link)
    end_price = page.find('<', start_price + 2)#was +1
    price = page[start_price + 1:end_price]
    
    try:
        price = float(price)
        
        return price,prime
    except: 
        return 1000.00,prime
 #   print start_quote,end_quote
 #   print ur
    return price,prime
 
def get_sales_rank(page):
#    print page

    start_link = page.find('Sellers Rank:')
    if start_link == -1:
        return 'no rank'
    
    start_rank = page.find('#',start_link)
    
    end_rank = page.find(' ', start_rank)  #was +1
    rank = page[start_rank + 1:end_rank]
    #need to strip the , out
    if end_rank - start_rank > 10:
         return "no rank"
    return rank

def get_review_count(page):
#    print page

    start_link = page.find('CustomerReviewText')
    if start_link == -1:
        return 0
    start_count = page.find('>',start_link)
    
    end_count = page.find(' ', start_count)  #was +1
    count = page[start_count + 1:end_count]
    if end_count - start_count > 10:
       count = 0
    
    return count
    
def get_left_in_stock(page):
#    print page

    start_link = page.find('left in stock')
    if start_link == -1:
        return "In Stock"
    start_count = page.find('Only',start_link-20)
    
    start = page.find(' ', start_count) 
    end = page.find(' ', start+1)#was +1
    count = page[start + 1:end]
    if end - start > 10:
       count = "In Stock"
    
    return count
    
def get_shipping(page):
#    print page

    start_link = page.find('shipping')
    if start_link == -1:
        return "Free Shipping?"
    start_count = page.find('$',start_link)
    if (start_count-start_link > 400) or start_count == -1:
        count = "Free Shipping"
        return count
    end_count = page.find(' ', start_count)  #was +1
    count = page[start_count + 1:end_count]
    if end_count - start_count > 10:
       count = "Free ????"
    
    return count

def send_email(list):
    import smtplib

    you = "judee@glutenfreeyouandme.com"
    me = "adejaco12@gmail.com"


    msg = "\nSome of your products or your competitors have some interesting news online\n\n" 
    for product in list:
        if product['price change']== "Yes":
            msg = msg + str(product['title']) + " from " + str(product['brand']) + \
            " has a price change from " + str(product['old price']) + " to " + str(product['price']) + "\n\n" 
        if product['rank change']== "Yes":
            msg = msg + str(product['title']) + " from " + str(product['brand']) + \
            " has a rank of " + str(product['rank']) + " its 7 day average if " + str(product['7 day ma rank']) \
            + " and its 30 ma rank is " + str(product['30 day ma rank'])+ "\n\n"
        if product['new_review']== "Yes":
            msg = msg + str(product['title']) + " from " + str(product['brand']) + \
            " has a new review number " + str(product['review_cnt']) + "\n\n" 
        if float(product['stock_left']) < 4:
            msg = msg + str(product['title']) + " from " + str(product['brand']) + \
            " is running out of stock with this many left  " + str(product['stock_left']) + "\n" 
        msg = msg + "\n"
        
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()

    server.login("adejaco12@gmail.com", "bday2015")
    problems = server.sendmail(me,you, msg)
    sendtome = server.sendmail(me,me, msg)
    server.quit()
    print problems
    print sendtome   
    return

def send_email_GFYM(list):
    import smtplib

    you = "adejaco12@gmail.com"
    me = "adejaco12@gmail.com"

    msg = "\nSome of your GFYM products have some interesting news online\n\n" 
    for product in list:
        
        if product['new_review']== "Yes":
            msg = msg + str(product['title'])  + \
            " has a new review number " + str(product['review_cnt']) + "\n\n" 
        if float(product['stock_left']) < 4:
            msg = msg + str(product['title']) +  \
            " is running out of stock with this many left  " + str(product['stock_left']) + "\n\n" 
        msg = msg + "\n"
        
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()

    server.login("adejaco12@gmail.com", "bday2015")
    problems = server.sendmail(me,you, msg)
    server.quit()
    print problems
       
    return
# main program
# read in CSV files  
time_of_day = time.strftime("%H:%M:%S") 
date = time.strftime("%m/%d/%Y")
print date+" "+time_of_day

# open up the stock tracking file and read it into a list of dictionaries to modify
productlist = []
with open('tracking_products.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for header in reader:
        product_fieldnames = header
        break
csvfile.close()   
with open('tracking_products.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     for product in reader:
#         print(stock)
         productlist.append(product)
 
csvfile.close()    

# stocklist now contains tracking stocks
# loop through the list and get the latest quote
#update the max value, max date and % of top as needed     



email_GFYM = False
email_list_GFYM = [] 
email = False
email_list = []  
 
# make sure tracking_product_new got moved correctly last time
 
try:
    
    os.rename("tracking_products_new.csv", "tracking_products_keep"+ date[3:5] + ".csv")
    print " tracking did not finish correctly last time"
except: 
    print ""
 
 

with open('tracking_products_new.csv', 'ab') as csvfile:
     
     writer = csv.DictWriter(csvfile, fieldnames = product_fieldnames)
     writer.writeheader()
     for product in productlist: 
         url = "http://www.amazon.com/dp/" + product['ASIN']       # get detailed page for the competitors product 


# get fields we are interested in from competitors
         page = get_page(url)
         if page == "":
             print product['brand'] + "_"+ product['title']+" page doesn't exit"
             time_of_day = time.strftime("%H:%M:%S") 
             date = time.strftime("%m/%d/%Y")
             print time_of_day, date
             writer.writerow(product)
             continue
         if page == -1:
             print product['brand'] + "_"+ product['title']+" amazon denied access "
             time_of_day = time.strftime("%H:%M:%S") 
             date = time.strftime("%m/%d/%Y")
             print time_of_day, date
             writer.writerow(product)
             continue
        
         price,prime = get_price(page)
         if price == "OUT":
             price = product['price']
         rank = get_sales_rank(page)
         seller_review_count = get_review_count(page)
         stock_left = get_left_in_stock(page)
         if prime == False:
             shipping = get_shipping(page)
         elif prime == "OUT":
             shipping = "OUT"
             stock_left = "OUT"
         else:
             shipping = "PRIME"
         time_of_day = time.strftime("%H:%M:%S") 
         date = time.strftime("%m/%d/%Y")

# Update sales rank
         product['rank'] = rank
         day30 = .03333/2
         day7 = .1429/2
         product['30 day ma rank']=(1-day30)*float(product['30 day ma rank'].replace(',',''))+(day30)*float(rank.replace(',',''))

         product['7 day ma rank']=(1-day7)*float(product['7 day ma rank'].replace(',',''))+(day7)*float(rank.replace(',',''))
         # is there a price change
         product['price change'] = "No"
         if float(price) != float(product['price']):
             product['price change'] = "Yes"
             product['old price'] = product['price']
         
         product['price'] = price
         # is there a rank change
         rank_deviation_30 = .20*float(product['30 day ma rank'])
         rank_deviation_ma = .10*float(product['30 day ma rank'])
         if abs(float(rank.replace(',',''))-float(product['30 day ma rank'])) > rank_deviation_30:
             product['rank change'] = "Yes"
         else:
             product['rank change'] = "No"
             
         if abs(float(product['7 day ma rank'])-float(product['30 day ma rank'])) > rank_deviation_ma:
             product['rank change'] = "Yes"
      
        
         
         #is there a new review
        
         if float(product['review_cnt']) != float(seller_review_count):
             product['new_review'] = "Yes"
         else:
             product['new_review'] = "No"
         product['review_cnt'] = seller_review_count  # update review count    
         #has shipping gone non-prime
         product['shipping'] = shipping         
         
         #is the stock left getting low
         product['stock_left'] = stock_left  #
         try: 
             stock_left = float(product['stock_left'])
        
         except:
             if product['stock_left'] == "In Stock":
                 stock_left = 100
             else:
                 stock_left = 0
             product['stock_left'] = stock_left
         
      
   #is there a new review or is stock getting low for a GFYM product
         stock_low_level = 10
         if (product['new_review']== "Yes" and product['brand'] == "Gluten Free You and Me") or \
                    (stock_left < stock_low_level and product['brand'] == "Gluten Free You and Me") :
            email_list_GFYM.append(product)
            email_GFYM = True
          
         
           #now check all products for interesting changes       
         if product['new_review']=="Yes" or product['rank change'] == "Yes" or product['price change'] == "Yes" \
             or stock_left < stock_low_level:
            email_list.append(product)
            email = True
          
        #update time of update
         product ['date of update'] = time.strftime("%m/%d/%Y")
         product ['time of update'] = time.strftime("%H:%M:%S") 

      
          
         writer.writerow(product)
    
# now rename the new file 
os.remove('tracking_products.csv')
os.rename("tracking_products_new.csv", "tracking_products.csv")

# send emails
#if email_GFYM == True:
#    send_email_GFYM(email_list_GFYM)
if email == True:
    send_email(email_list)

    


   
print "Sucessfully completed"                                               

print "that's it"                                               
