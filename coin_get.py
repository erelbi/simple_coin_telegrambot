import os
from pycoingecko import CoinGeckoAPI
from GoogleNews import GoogleNews
try:
    import httplib
except:
    import http.client as httplib
import telebot
from multiprocessing import Pool

googlenews = GoogleNews()
cg = CoinGeckoAPI()
googlenews.set_lang('en')
googlenews.set_period('1d')
bot = telebot.AsyncTeleBot("token:tokentokentokentoken")


class Coinews(object): 
    def __init__(self):
        print( 'connected!' if self.connect() else 'no internet!' )
        
    @bot.message_handler(commands=['start'])
    def start_bot(message):
	    bot.reply_to(message, "Selam ben kubi para bot!")
    
    @bot.message_handler(commands=['clear'])
    def clear(message):
	    os.system('cls' if os.name=='nt' else 'clear')
        
    @bot.message_handler(commands=['news'])
    def trend_new_get_all(message):  
        try:
            result = Coinews.trend_coin_list()
            for coins in list(result):
                for k in coins.values():
                    bot.reply_to(message,"{0} -----------> {1}".format(list(coins.keys())[0],k))
        except Exception as err:
            print(err)
            bot.reply_to(message,"bir hata ile karşılaşıldı")
              

    @bot.message_handler(func=lambda message: True)
    def coin_price(message): 
        try:
	        bot.reply_to(message,"{0} coninin Fiyatı {1} Türk Lirası".format(list(cg.get_price(ids=message.text, vs_currencies='try').keys())[0],cg.get_price(ids=message.text, vs_currencies='try')[message.text]["try"]))
        except:
            bot.reply_to(message,"{0} isminde bir coin bulunamadı".format(message.text))

        
   

    @classmethod
    def  trend_coin_list(cls):
        trend_coin = cg.get_search_trending()
        coin_list = []
        try:
            for coin_lists in trend_coin["coins"]:
                coin_list.append(coin_lists['item']['name'])
            return cls.news_google_find(coin_list)
        except Exception as err:
            print(err)

    @staticmethod
    def news_google_find(coin_list):
        print("news google find")
        pool = Pool()
        try:
            return pool.map(Coinews.map_googlenews,coin_list) 
        except Exception as err:
            print(err)
        finally:
            pool.close()
            pool.join()
           
    def connect(self):
        conn = httplib.HTTPConnection("www.coingecko.com", timeout=5)
        try:
            conn.request("HEAD", "/")
            conn.close()
            return True
        except:
            conn.close()
            return False
        

    @staticmethod    
    def map_googlenews(coin): 
        print("map_googlenews")
        dict_coin = {}
        try: 
            dict_coin[coin] = Coinews.google_news_result_parse(coin)
            return dict_coin
        except:
            return False

    @staticmethod
    def google_news_result_parse(coin_name):
        print("google_news_result_parse")
        googlenews.results(sort=True)
        try:
            googlenews.get_news("{0} {1}".format(coin_name,"coin"))
            news_title = googlenews.get_texts()
            news_link = googlenews.get_links()
            return {news_title[i]: news_link[i] for i in range(len(news_title))}   
        except:
            return False
        finally:
            googlenews.clear()
        

    
if __name__ == "__main__":
    Coinews()
    bot.polling()

    
    


