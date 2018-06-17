from expedia import parse

def scrape(departure_city,departure_airport_code,arrival_city,arrival_state,arrival_airport_code,month,day,year):
    scraped_data = parse(departure_city,departure_airport_code,arrival_city,arrival_state,arrival_airport_code,month,day,year)
    #print ("Writing data to output file")departure_ci
         
    arrival_city='_'.join(arrival_city.split())
    #print(type(arrival_city))
    #print(arrival_city)
    with open('data/%s-%s-%s-%s-%s-flight-results.json'%(month,day,year,departure_city,arrival_city),'w') as fp:
          json.dump(scraped_data,fp,indent = 4)
          
if __name__=="__main__":
   departure_city = ['Guangzhou','Hongkong','Beijing','Shanghai','Shenzhen']
   departure_airport_code= args.departure_airport['CAN','HKG','PEK','PVG','SZX']
   arrival_city=Austin
   arrival_state=TX
   arrival_airport_code=AUS
   
   dictionary = dict(zip(departure_city, departure_airport_code))
   
   for departure_city,departure_airport_code in dictionarg.items():
       for year in [2018,2019]:
         if year==2018:
              for month in range(7,13):
                   if(month==9 or month==11):
                      for day in range(31):
                           scrape(departure_city,departure_airport_code,arrival_city,arrival_state,arrival_airport_code,month,day,year)
                   else:
                      for day in range(32):
                           scrape(departure_city,departure_airport_code,arrival_city,arrival_state,arrival_airport_code,month,day,year)
         if year==2019:
              for month in range(13):
                   if(month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12):
                      for day in range(32):
                           scrape(departure_city,departure_airport_code,arrival_city,arrival_state,arrival_airport_code,month,day,year)
                           
                   elif (month==2):
                      for day in range(29):
                           scrape(departure_city,departure_airport_code,arrival_city,arrival_state,arrival_airport_code,month,day,year)
                           
                   else:    
                      for day in range(31):
                           scrape(departure_city,departure_airport_code,arrival_city,arrival_state,arrival_airport_code,month,day,year)
                            
                    
                      
                       
   
   
   
   
   
   
   
   
   
   
   
   
   
 
                       
                           
                           
