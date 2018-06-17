import json
import requests
from lxml import html
from collections import OrderedDict
import argparse

def parse(departure_city,departure_airport_code,arrival_city,arrival_state,arrival_airport_code,month,day,year):
        for i in range(5):
                try:
                        url="https://www.expedia.com/Flights-Search?trip=oneway&leg1=from%3A{0}%2C%20China%20({1})%2Cto%3A{2}%2C%20({3})%20({4})%2Cdeparture%3A{5}%2F{6}%2F{7}TANYT&passengers=adults%3A1%2Cchildren%3A0%2Cseniors%3A0%2Cinfantinlap%3AY&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com".format(departure_city,departure_airport_code,arrival_city,arrival_state,arrival_airport_code,month,day,year)



                        #headers = {'User-Agent': 'mozzilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
                       
                        response = requests.get(url,verify=False)
                        parser = html.fromstring(response.text)
                        #print(parser)
                        json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")
                        raw_json =json.loads(json_data_xpath[0] if json_data_xpath else '')
                        flight_data = json.loads(raw_json["content"])

                        flight_info  = OrderedDict()
                        lists=[]
                        #price_list=[]
                        #print(flight_data['legs']['AA7101coach2018-12-21T11:00+08:00CAN2018-12-21T14:15+08:00PEK0AA262coach2018-12-21T17:25+08:00PEK2018-12-21T16:50-06:00DFW0AA2636coach2018-12-21T19:05-06:00DFW2018-12-21T20:08-06:00AUS0'])
                        #print(flight_data['legs'].keys().length())
                        #print(flight_data['legs'].keys())
                        #print(len(list(flight_data['legs'].keys())))
                                         
                        for i in flight_data['legs'].keys():
                        
                                
                                exact_price = flight_data['legs'][i].get('price',{}).get('exactPrice','')
                                                                
                               
                                departure_location_city = flight_data['legs'][i].get('departureLocation',{}).get('airportCity','')
                                departure_location_airport_code = flight_data['legs'][i].get('departureLocation',{}).get('airportCode','')

                                
                                arrival_location_airport_code = flight_data['legs'][i].get('arrivalLocation',{}).get('airportCode','')
                                arrival_location_city = flight_data['legs'][i].get('arrivalLocation',{}).get('airportCity','')
                                airline_name = flight_data['legs'][i].get('carrierSummary',{}).get('airlineName','')
                                no_of_stops = flight_data['legs'][i].get("stops","")
                                
                               
                                flight_duration = flight_data['legs'][i].get('duration',{})
                                flight_hour = flight_duration.get('hours','')
                                flight_minutes = flight_duration.get('minutes','')
                                #flight_days = flight_duration.get('numOfDays','') # can be deleted
                                
                                
                                if no_of_stops==0:
                                        stop = "Nonstop"
                                else:
                                        stop = str(no_of_stops)+' Stop'


                              
                                total_flight_duration = " {0} hours {1} minutes".format(flight_hour,flight_minutes)
                                departure = departure_location_airport_code+", "+departure_location_city
                                arrival = arrival_location_airport_code+", "+arrival_location_city
                                carrier = flight_data['legs'][i].get('timeline',[])[0].get('carrier',{})
                               
                                if not airline_name:
                                        airline_name = carrier.get('operatedBy','')

                                timings = []
                                for timeline in  flight_data['legs'][i].get('timeline',{}):
                                        if 'departureAirport' in timeline.keys():
                                                departure_airport = timeline['departureAirport'].get('longName','')
                                                departure_time = timeline['departureTime'].get('time','')
                                                arrival_airport = timeline.get('arrivalAirport',{}).get('longName','')
                                                arrival_time = timeline.get('arrivalTime',{}).get('time','')
                                                flight_timing = {
                                                                                        'departure_airport':departure_airport,
                                                                                        'departure_time':departure_time,
                                                                                        'arrival_airport':arrival_airport,
                                                                                        'arrival_time':arrival_time
                                                }
                                                timings.append(flight_timing)

                                flight_info={'stops':stop,
                                        'ticket price':int(exact_price),
                                        'departure':departure,
                                        'arrival':arrival,
                                        'flight duration':total_flight_duration,
                                        'airline':airline_name,
                                       
                                        'timings':timings,
                                       
                                }
                                lists.append(flight_info)
                        sortedlist = sorted(lists, key=lambda k: k['ticket price'],reverse=False)
                        #print(price_list)
                        return sortedlist

                except ValueError:
                        print ("Rerying...")
                        
                return {"error":"failed to process the page",}
                
if __name__=="__main__":
         argparser = argparse.ArgumentParser()
         argparser.add_argument('--departure_city',help = 'Departure city name')
         argparser.add_argument('--departure_airport',help = 'Departure airport code')
         argparser.add_argument('--arrival_city',type=str,help='Arrival cit)y name')
         argparser.add_argument('--arrival_state',help='Arrival state name')
         argparser.add_argument('--arrival_airport',help='Arrival airport code')
         
         argparser.add_argument('--month',help = 'MM')
         argparser.add_argument('--day',help = 'DD')
         argparser.add_argument('--year',help = 'YYYY')
        
         args = argparser.parse_args()
         departure_city = args.departure_city
         departure_airport_code= args.departure_airport
         arrival_city=args.arrival_city
         arrival_state=args.arrival_state
         arrival_airport_code=args.arrival_airport
         month = args.month
         day=args.day
         year=args.year
           
         #print(arrival_city)
         print ("Fetching flight details")
         scraped_data = parse(departure_city,departure_airport_code,arrival_city,arrival_state,arrival_airport_code,month,day,year)
         print ("Writing data to output file")
         
         arrival_city='_'.join(arrival_city.split())
         print(type(arrival_city))
         print(arrival_city)
         with open('data/%s-%s-flight-results.json'%(departure_city,arrival_city),'w') as fp:
                 json.dump(scraped_data,fp,indent = 4)
                                
