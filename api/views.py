from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from rest_framework.response import Response
from rest_framework.views import APIView
from selenium.webdriver.chrome.options import Options
# Create your views here.

class CoinMarketCap(APIView):

    list1 = []

    def get(self,request):
        return Response({'enter payload'})
    
    def scrape(self, coins):
        list2 = []
        # print(coins['coins'])
        for coin in coins['coins']:
            
            # print(coin)

            options = Options()
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            driver = webdriver.Chrome(options=options)
            driver.get(f'https://coinmarketcap.com/currencies/{coin}/')

            driver.maximize_window() # For maximizing window
            driver.implicitly_wait(20)


            all_numbers = driver.find_elements(By.CSS_SELECTOR,".sc-d1ede7e3-0.hPHvUM.base-text")
            number_list = [numbers.text for numbers in all_numbers]
            # print(number_list)
            market_cap_list = number_list[0].split('\n')
            # print(market_cap[0])
            volume = number_list[1].split('\n')

            ranks = driver.find_elements(By.CSS_SELECTOR,".text.slider-value.rank-value")
            rank_list = [rank.text for rank in ranks]

            
            price = driver.find_element(By.CSS_SELECTOR,".sc-d1ede7e3-0.fsQm.base-text").text
           
            text = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[1]/div[1]/span").text
            
            
            
            officialinks = []
            socialmedialinks = []
            contracts = ""
            contracts_address = ""

            if text == 'Contracts':
                contracts = driver.find_element(By.XPATH,"//*[@id='__next']/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[1]/div[2]/div/div[1]").text.split(":")[0]
                contracts_address = driver.find_element(By.CSS_SELECTOR,".sc-d1ede7e3-0.sc-7f0f401-0.sc-96368265-0.bwRagp.gQoblf.eBvtSa.flexStart > a").get_attribute('href').split("/")[4]
                # print(contracts)
                # print(contracts_address)


                social_media = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[3]/div[2]/div")
                social_media_links = social_media.find_elements(By.CSS_SELECTOR,".sc-d1ede7e3-0.sc-7f0f401-0.gRSwoF.gQoblf > a")

                official_links = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[2]/div[2]/div")
                links = official_links.find_elements(By.CSS_SELECTOR,".sc-d1ede7e3-0.sc-7f0f401-0.gRSwoF.gQoblf > a")

                
                for link in links:
                    officialinks.append({"name":link.text,"link":link.get_attribute('href')})

                

                for link in social_media_links:
                    socialmedialinks.append({"name":link.text,"link":link.get_attribute('href')})

            else:
                social_media = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[2]/div[2]/div")
                social_media_links = social_media.find_elements(By.CSS_SELECTOR,".sc-d1ede7e3-0.sc-7f0f401-0.gRSwoF.gQoblf > a")


                official_links = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[1]/div[2]/div")
                links = official_links.find_elements(By.CSS_SELECTOR,".sc-d1ede7e3-0.sc-7f0f401-0.gRSwoF.gQoblf > a")


                
                for link in links:
                    officialinks.append({"name":link.text,"link":link.get_attribute('href')})

                

                for link in social_media_links:
                    socialmedialinks.append({"name":link.text,"link":link.get_attribute('href')})


            driver.quit()
            


            json_data = {"coin":coin,"output":{"price":price,"price_change":market_cap_list[0],"market_cap":market_cap_list[1],"market_cap_rank":rank_list[0][1:],
                                               "volume":volume[1],"volume_rank":rank_list[1][1:],"volume_change":number_list[2],"circulating_supply":number_list[3],
                                               "total_supply":number_list[4],"diluted_market_cap":number_list[6],"Contracts":[{"name":contracts,"address":contracts_address}],"official_links":officialinks,"socials":socialmedialinks}}
            
            list2.append(json_data)

        return list2
    

    # def create_json(self,price, number_list,rank_list,contracts,contracts_address,officialinks,socialmedialinks):


    #     json_data = {"coin":coin,"output":{"price":price,"price_change":price_change,"market_cap":market_cap,"market_cap_rank":market_cap_rank,
    #                                            "volume":volume,"volume_rank":volume_rank,"volume_change":volume_change,"circulating_supply":circulating_supply,
    #                                            "total_supply":total_supply,"diluted_market_cap":diluted_market_cap,"Contracts":[{"name":contracts,"address":contracts_address}],"official_links":officialinks,"socials":socialmedialinks}}
    
    def post(self,request):
        
        coins = json.loads(request.body)
        
        # list1 = []

        # for coin in coins['coins']:

            # print(coin)

            # options = Options()
            # options.add_argument('--disable-blink-features=AutomationControlled')
            
            # driver = webdriver.Chrome(options=options)
            # driver.get(f'https://coinmarketcap.com/currencies/{coin}/')

            # driver.maximize_window() # For maximizing window
            # driver.implicitly_wait(20)


            # # Print the list of titles
            # # duko = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/section/div/div[2]/div/div/p").text[0:5]
            # price = driver.find_element(By.CSS_SELECTOR,".sc-d1ede7e3-0.fsQm.base-text").text
            # price_change = driver.find_element(By.XPATH,"//*[@id='section-coin-overview']/div[2]/div/div/p").text[0:6]
            # market_cap = driver.find_element(By.CSS_SELECTOR,".sc-d1ede7e3-0.hPHvUM.base-text").text[7:]
            # market_cap_rank = driver.find_element(By.CSS_SELECTOR,".text.slider-value.rank-value").text[1:]
            # volume = driver.find_element(By.XPATH,"//*[@id='section-coin-stats']/div/dl/div[2]/div[1]/dd").text[8:]
            # volume_rank = driver.find_element(By.XPATH,"//*[@id='section-coin-stats']/div/dl/div[2]/div[2]/div/span").text[1:]
            # volume_change = driver.find_element(By.XPATH,"//*[@id='section-coin-stats']/div/dl/div[3]/div/dd").text
            # circulating_supply = driver.find_element(By.XPATH,"//*[@id='section-coin-stats']/div/dl/div[4]/div/dd").text[:14]
            # total_supply = driver.find_element(By.XPATH,"//*[@id='section-coin-stats']/div/dl/div[5]/div/dd").text[:14]
            # diluted_market_cap = driver.find_element(By.XPATH,"//*[@id='section-coin-stats']/div/dl/div[7]/div/dd").text
           
            # text = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[1]/div[1]/span").text
            
            
            
            # officialinks = []
            # socialmedialinks = []
            # contracts = ""
            # contracts_address = ""

            # if text == 'Contracts':
            #     contracts = driver.find_element(By.XPATH,"//*[@id='__next']/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[1]/div[2]/div/div[1]").text.split(":")[0]
            #     contracts_address = driver.find_element(By.CSS_SELECTOR,".sc-d1ede7e3-0.sc-7f0f401-0.sc-96368265-0.bwRagp.gQoblf.eBvtSa.flexStart > a").get_attribute('href').split("/")[4]
            #     # print(contracts)
            #     # print(contracts_address)


            #     social_media = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[3]/div[2]/div")
            #     social_media_links = social_media.find_elements(By.CSS_SELECTOR,".sc-d1ede7e3-0.sc-7f0f401-0.gRSwoF.gQoblf > a")

            #     official_links = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[2]/div[2]/div")
            #     links = official_links.find_elements(By.CSS_SELECTOR,".sc-d1ede7e3-0.sc-7f0f401-0.gRSwoF.gQoblf > a")

                
            #     for link in links:
            #         officialinks.append({"name":link.text,"link":link.get_attribute('href')})

                

            #     for link in social_media_links:
            #         socialmedialinks.append({"name":link.text,"link":link.get_attribute('href')})

            # else:
            #     social_media = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[2]/div[2]/div")
            #     social_media_links = social_media.find_elements(By.CSS_SELECTOR,".sc-d1ede7e3-0.sc-7f0f401-0.gRSwoF.gQoblf > a")


            #     official_links = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[1]/div[2]/div")
            #     links = official_links.find_elements(By.CSS_SELECTOR,".sc-d1ede7e3-0.sc-7f0f401-0.gRSwoF.gQoblf > a")


                
            #     for link in links:
            #         officialinks.append({"name":link.text,"link":link.get_attribute('href')})

                

            #     for link in social_media_links:
            #         socialmedialinks.append({"name":link.text,"link":link.get_attribute('href')})


            # driver.quit()
            


            # json_data = {"coin":coin,"output":{"price":price,"price_change":price_change,"market_cap":market_cap,"market_cap_rank":market_cap_rank,
            #                                    "volume":volume,"volume_rank":volume_rank,"volume_change":volume_change,"circulating_supply":circulating_supply,
            #                                    "total_supply":total_supply,"Contracts":[{"name":contracts,"address":contracts_address}],"official_links":officialinks,"socials":socialmedialinks}}
            
        data = self.scrape(coins=coins)

            # print(data)

            # self.list1.append(data)
            # print(list1)

            # print(price)
            # print(price_change)
            # print(market_cap)
            # print(market_cap_rank)
            # print(volume)
            # print(volume_rank)
            # print(volume_change)
            # print(circulating_supply)
            # print(total_supply)
            # print(diluted_market_cap)

            

            # for link in social_media_links:
            #     print(link.get_attribute('href'))
            # print(official_links)
            # print(contracts +":"+contracts_address)
            # Close the webdriver
            
        return Response({'tasks':data})
        


