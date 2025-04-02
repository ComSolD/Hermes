from datetime import datetime
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pathlib import Path
import time
import traceback

from parser.NBA.redact import date_redact, handicap_odds_redact, total_odds_redact
from parser.NBA.save import match_table, odds_handicap_table, odds_moneyline_table, odds_total_table, team_table


class OddsNBA(object):
    def __init__(self, first_year, second_year):
        driver_path = Path("parser/drivers/chromedriver.exe").resolve()

        self.service  = Service(driver_path)

        options = webdriver.ChromeOptions()
        # options.add_extension("parser/drivers/adblock.crx")
        self.driver = webdriver.Chrome(service = self.service, options=options)
        self.driver.maximize_window()

        self.first_year = first_year
        self.second_year = second_year

        self.enough_date = datetime.strptime(self.second_year, "%Y-%m-%d").strftime("%d-%m-%Y")

        self.season = f"{int(self.second_year[:4])-1}/{self.second_year[:4]}"


    def get_matches_link(self):

        base_url = "https://www.oddsportal.com/basketball/usa/nba"

    
        if self.first_year == "now" or self.first_year == "now forward":
            url = f"{base_url}/results/"
        elif self.first_year == "get":
            url = base_url
        else:
            self.second_year = self.second_year.split("-")[0]
            url = f"{base_url}-{self.first_year}-{self.second_year}/results/"

        self.driver.get(url)
        
        time.sleep(5)

        try:
            if self.first_year == "get":
                self.process_matches_on_page()
            else:
                self.paginate_and_process_matches(url)
        except Exception as e:
            logging.error(f"Ошибка: {e}\n{traceback.format_exc()}")

        self.driver.quit()


    def process_matches_on_page(self):
        """Обрабатывает матчи на текущей странице."""
        matches_selenium = self.get_match_links()
        match_urls = [match.get_attribute('href') for match in matches_selenium]

        for url in match_urls:
            if self.open_matches_link(url) == 'enough':
                return


    def paginate_and_process_matches(self, main_url):
        """Перебирает страницы с результатами матчей и обрабатывает их."""
        pagination_links = self.driver.find_elements(By.CSS_SELECTOR, 'a.pagination-link[data-number]')
        if not pagination_links:
            return
        
        dropdown_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'group')]/button[contains(@class, 'flex')]"))
        )
        dropdown_button.click()


        # Шаг 2: Подождать пока откроется dropdown и выбрать нужный элемент
        dropdown_item = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Decimal Odds')]")))
        dropdown_item.click()

        max_page = max(int(link.get_attribute("data-number")) for link in pagination_links)

        pages = range(max_page, 0, -1) if self.first_year != "now forward" else range(1, max_page + 1)

        for page in pages:
            try:
                self.driver.get(main_url + f"#/page/{page}/")
                self.driver.refresh()

                time.sleep(2)

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(2)

                self.driver.execute_script("window.scrollTo(0, 0);")

                time.sleep(1)

                match_urls = [match.get_attribute('href') for match in self.get_match_links()]

                if self.first_year != "now forward":
                    match_urls.reverse()  # Переворачиваем список, чтобы идти в хронологическом порядке

                for url in match_urls:
                    
                    if self.open_matches_link(url) == 'enough':
                        return

            except Exception as e:
                logging.error(f"Ошибка на странице {page}: {e}\n{traceback.format_exc()}")


    def get_match_links(self):
        """Возвращает список элементов ссылок на матчи."""
        base_xpath = f'//a[starts-with(@href, "/basketball/usa/nba'
        
        if self.first_year == "now" or self.first_year == "get" or self.first_year == "now forward":
            xpath = base_xpath + '/") and not(@href="/basketball/usa/nba/") and not(contains(@href, "standings")) and not(contains(@href, "outrights")) and not(contains(@href, "results"))]'
        else:
            xpath = base_xpath + f'-{self.first_year}-{self.second_year}/") and not(@href="/basketball/usa/nba/") and not(@href="/basketball/usa/nba-{self.first_year}-{self.second_year}/") and not(contains(@href, "standings"))]'

        return self.driver.find_elements(By.XPATH, xpath)


    def open_matches_link(self, link):
        self.driver.get(link)

        time.sleep(2)

        try:
            # Дата матча
            date_selenium = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="game-time-item"] p'))
            )

            dates = list()

            for date in date_selenium:
                dates.append(date.get_attribute("textContent"))

            match_date = date_redact(dates)

            date = datetime.strptime(match_date, '%d-%m-%Y')

            if (self.first_year == 'get' and date >= datetime.strptime(self.enough_date, '%d-%m-%Y')) or (self.first_year == 'now forward' and date < datetime.strptime(self.enough_date, '%d-%m-%Y')):
                return 'enough'

            teams = list()

            # Первая команда
            team1_selenium = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="game-host"] p'))
            )

            for team in team1_selenium:
                team1 = team.get_attribute("textContent")
                teams.append(team.get_attribute("textContent"))

            # Вторая команда
            team2_selenium = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="game-guest"] p'))
            )

            for team in team2_selenium:
                team2 = team.get_attribute("textContent")
                teams.append(team.get_attribute("textContent"))

            
            teams_id = team_table(team2, team1)

            # Создаем персональный id для каждой команды
            teams = [team.lower().replace(" ", "_") for team in teams]

            teams.reverse()

            date = datetime.strptime(match_date, '%d-%m-%Y')

            self.match_id = "_".join(teams)

            self.match_id += f"_{match_date.replace('-', '_')}_{dates[2].replace(':', '_')}"

            if match_table(self.match_id, teams_id, self.season, match_date, '', ''):

                return 0

            try:
                self.process_odds_for_periods(self.driver, self.moneyline)
            except Exception as e:
                logging.error(f"Ошибка в данных по линии {self.match_id}: {e}\n{traceback.format_exc()}")

            try:
                div_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'//div[contains(text(), "Over/Under")]'))
                )
                self.driver.execute_script("arguments[0].click();", div_element)

                time.sleep(1)

                self.process_odds_for_periods(self.driver, self.total)
            except Exception as e:
                logging.error(f"Ошибка в данных по тоталу {self.match_id}: {e}\n{traceback.format_exc()}")

            try:
                div_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f'//div[contains(text(), "Asian Handicap")]'))
                )
                self.driver.execute_script("arguments[0].click();", div_element)

                time.sleep(1)

                self.process_odds_for_periods(self.driver, self.handicap)
            except Exception as e:
                logging.error(f"Ошибка в данных по форе {self.match_id}: {e}\n{traceback.format_exc()}")
            
        except Exception as e:
            logging.error(f"Ошибка обработки матча {link}: {e}\n{traceback.format_exc()}")

    

    # Функции для работы с ставками
    def process_odds_for_periods(self, driver, action_function):
        periods = {
            "full_time": "",  # Без клика, сразу вызываем функцию
            "1st_half": "1st Half",
            "2nd_half": "2nd Half",
            "1st_quarter": "1st Quarter",
            "2nd_quarter": "2nd Quarter",
            "3rd_quarter": "3rd Quarter",
            "4th_quarter": "4th Quarter",
        }

        try:
            action_function("full_time")
        except:
            self.driver.refresh()

            time.sleep(1)
            
            action_function("full_time") 

        for key, period_text in periods.items():
            if period_text:
                try:
                    div_element = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, f'//div[contains(text(), "{period_text}")]'))
                    )
                    driver.execute_script("arguments[0].click();", div_element)
                except:
                    continue
                
                try:
                    action_function(key)
                except:
                    self.driver.refresh()

                    time.sleep(1)
                    
                    action_function(key)
   

    def handicap(self, period):

        odds_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="min-md:px-[10px]"] div.relative div.flex div.flex p'))
        )

        odds = list()

        for odd in odds_selenium:
            odds.append(odd.get_attribute("textContent"))

        odds = handicap_odds_redact(odds)

        odds_handicap_table(self.match_id, odds, period)


    def total(self, period):

        odds_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="min-md:px-[10px]"] div.relative div.flex div.flex p'))
        )

        odds = list()

        for odd in odds_selenium:
            odds.append(odd.get_attribute("textContent"))

        odds = total_odds_redact(odds)

        odds_total_table(self.match_id, odds, period)

        
    def moneyline(self, period):

        odds_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@double-parameter]//p[@class="height-content"]'))
        )

        odds = list()

        for odd in odds_selenium:
            odds.append(odd.get_attribute("textContent"))


        team1_moneyline = odds[1]

        team2_moneyline = odds[0]

        if team1_moneyline and team2_moneyline:
        
            odds_moneyline_table(self.match_id, team1_moneyline, team2_moneyline, period)

