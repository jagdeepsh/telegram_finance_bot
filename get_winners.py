import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict
import asyncio

async def get_winners() -> List[Dict]:

    winners = []

    try:
        global driver
        driver = webdriver.Chrome()
        driver.get('https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'td'))
            )

        tr = driver.find_elements(By.TAG_NAME, 'tr')

        for index, elem in enumerate(tr[2:], start=2):
            # Ticker logic
            ticker: str = elem.get_attribute('data-rowkey')
            if ticker is not None:
                if 'NASDAQ:' in ticker:
                    ticker = ticker.replace('NASDAQ:','')
                elif 'AMEX:' in ticker:
                    ticker = ticker.replace('AMEX:','')
                else:
                    ticker = ticker.replace('NYSE:','')
            td = elem.find_elements(By.TAG_NAME, 'td')
            
            
            change: str = td[1].text
            price: str = td[2].text
            volume: str = td[3].text.replace('\u202f', '')
            relative_volume: str = td[4].text
            market_cap: str = td[5].text.replace('\u202f', '')
            p_e_ratio: str = td[6].text
            EPS_dil_TTM: str = td[7].text
            EPS_dil_growth_TTM_YoY: str = td[8].text
            dividend_yield: str = td[9].text
            sector: str = td[10].text
            analyst_rating: str = td[11].text

            stock = {
                        'ticker':ticker,
                        'change':change,
                        'price':price,
                        'volume':volume,
                        'relative_volume':relative_volume,
                        'market_cap':market_cap,
                        'p_e_ratio':p_e_ratio,
                        'EPS_dil_TTM':EPS_dil_TTM,
                        'EPS_dil_growth_TTM_YoY':EPS_dil_growth_TTM_YoY,
                        'dividend_yield':dividend_yield,
                        'sector':sector,
                        'analyst_rating':analyst_rating
                    }
            winners.append(stock)

    except selenium.common.exceptions.NoSuchElementException:
        print("Element not found")
    except Exception as e:
        print(e)
    finally:
        if 'driver' in locals():
            driver.quit()
    return winners
        
async def main():
    winners_data = await get_winners()
    print(winners_data)

if __name__ == "__main__":
    asyncio.run(main())
