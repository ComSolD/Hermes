from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from parser.NBA.redact import date_redact, handicap_odds_redact, total_odds_redact
from parser.NBA.save import match_table, odds_handicap_table, odds_moneyline_table, odds_total_table, team_table


class OddsNBA(object):
    def __init__(self, first_year, second_year):
        self.service  = Service(executable_path="parser/drivers/chromedriver.exe")
        options = webdriver.ChromeOptions()
        # options.add_extension("parser/drivers/adblock.crx")
        self.driver = webdriver.Chrome(service = self.service, options=options)
        self.driver.maximize_window()
        self.first_year = first_year
        self.second_year = second_year



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
                self.paginate_and_process_matches()
        except:
            pass

        self.driver.quit()


    def process_matches_on_page(self):
        """Обрабатывает матчи на текущей странице."""
        matches_selenium = self.get_match_links()
        match_urls = [match.get_attribute('href') for match in matches_selenium]

        for url in match_urls:
            if self.open_matches_link(url) == 'enough':
                break


    def paginate_and_process_matches(self):
        """Перебирает страницы с результатами матчей и обрабатывает их."""
        pagination_links = self.driver.find_elements(By.CSS_SELECTOR, 'a.pagination-link[data-number]')
        if not pagination_links:
            return

        max_page_number = max(int(link.get_attribute("data-number")) for link in pagination_links)

        start, stop, step = (max_page_number, 0, -1) if self.first_year != "now forward" else (1, max_page_number + 1, 1)

        for page in range(start, stop, step):
            try:
                page_link = self.driver.find_element(By.CSS_SELECTOR, f'a.pagination-link[data-number="{page}"]')
                self.driver.execute_script("arguments[0].click();", page_link)

                time.sleep(5)

                match_urls = [match.get_attribute('href') for match in self.get_match_links()]

                if self.first_year != "now forward":
                    match_urls.reverse()  # Переворачиваем список, чтобы идти в хронологическом порядке

                for url in match_urls:
                    
                    if self.open_matches_link(url) == 'enough':
                        break
            except Exception as e:
                print(f"Ошибка на странице {page}: {e}")


    def get_match_links(self):
        """Возвращает список элементов ссылок на матчи."""
        base_xpath = f'//a[starts-with(@href, "/basketball/usa/nba'
        
        if self.first_year == "now" or self.first_year == "get" or self.first_year == "now forward":
            xpath = base_xpath + '/") and not(@href="/basketball/usa/nba/") and not(contains(@href, "standings")) and not(contains(@href, "outrights")) and not(contains(@href, "results"))]'
        else:
            xpath = base_xpath + f'-{self.first_year}-{self.second_year}/") and not(@href="/basketball/usa/nba/") and not(contains(@href, "standings"))]'

        return self.driver.find_elements(By.XPATH, xpath)


    def open_matches_link(self, link):
        self.driver.get(link)

        # Дата матча
        date_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="game-time-item"] p'))
        )

        dates = list()

        for date in date_selenium:
            dates.append(date.get_attribute("textContent"))

        match_date = date_redact(dates)

        date = datetime.strptime(match_date, '%d-%m-%Y')


        if self.first_year == 'get' or self.first_year == 'now forward':

            try:
                self.second_year = datetime.strptime(self.second_year, "%Y-%m-%d").strftime("%d-%m-%Y")
            except:
                pass

            if date == datetime.strptime(self.second_year, '%d-%m-%Y'):

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

        year = date.year

        if date.month >= 10:  # Сезон начинается осенью
            season = f"{year}/{int(str(year)) + 1}"

            first = year
            second = int(str(year)) + 1
        else:
            season = f"{year - 1}/{str(year)}"

            second = year
            first = int(str(year)) + 1

        self.match_id = "_".join(teams)

        self.match_id += f"_{first}_{second}_{match_date.replace('-', '_')}_{dates[2].replace(':', '_')}"

        if match_table(self.match_id, teams_id, season, match_date, ''):

            return 0

        self.moneyline_for_periods(self.driver, self.moneyline)

        div_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//div[contains(text(), "Over/Under")]'))
        )
        self.driver.execute_script("arguments[0].click();", div_element)

        time.sleep(1)

        self.total_for_periods(self.driver, self.total)

        div_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//div[contains(text(), "Asian Handicap")]'))
        )
        self.driver.execute_script("arguments[0].click();", div_element)

        time.sleep(1)

        self.handicap_for_periods(self.driver, self.handicap)

    

    # Функции для работы с ставками
    def handicap_for_periods(self, driver, action_function):
        periods = {
            "full_time": "",  # Без клика, сразу вызываем функцию
            "1st_half": "1st Half",
            "2nd_half": "2nd Half",
            "1st_quarter": "1st Quarter",
            "2nd_quarter": "2nd Quarter",
            "3rd_quarter": "3rd Quarter",
            "4th_quarter": "4th Quarter",
        }

        action_function("full_time")

        for key, period_text in periods.items():
            if period_text:
                try:
                    div_element = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, f'//div[contains(text(), "{period_text}")]'))
                    )
                    driver.execute_script("arguments[0].click();", div_element)
                except:
                    continue
                
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


    def total_for_periods(self, driver, action_function):
        periods = {
            "full_time": "",  # Без клика, сразу вызываем функцию
            "1st_half": "1st Half",
            "2nd_half": "2nd Half",
            "1st_quarter": "1st Quarter",
            "2nd_quarter": "2nd Quarter",
            "3rd_quarter": "3rd Quarter",
            "4th_quarter": "4th Quarter",
        }

        action_function("full_time")

        for key, period_text in periods.items():
            if period_text:
                try:
                    div_element = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, f'//div[contains(text(), "{period_text}")]'))
                    )
                    driver.execute_script("arguments[0].click();", div_element)
                except:
                    continue
                
                action_function(key)
   

    def total(self, period):

        odds_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="min-md:px-[10px]"] div.relative div.flex div.flex p'))
        )

        odds = list()

        for odd in odds_selenium:
            odds.append(odd.get_attribute("textContent"))

        odds = total_odds_redact(odds)

        odds_total_table(self.match_id, odds, period)


    def moneyline_for_periods(self, driver, action_function):
        periods = {
            "full_time": "",  # Без клика, сразу вызываем функцию
            "1st_half": "1st Half",
            "2nd_half": "2nd Half",
            "1st_quarter": "1st Quarter",
            "2nd_quarter": "2nd Quarter",
            "3rd_quarter": "3rd Quarter",
            "4th_quarter": "4th Quarter",
        }
        
        # Выполняем функцию сразу для полного времени
        action_function("full_time")
        
        for key, period_text in periods.items():
            if period_text:
                try:
                    div_element = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, f'//div[contains(text(), "{period_text}")]'))
                    )
                    driver.execute_script("arguments[0].click();", div_element)
                except:
                    continue
                
                action_function(key)
   
        
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

