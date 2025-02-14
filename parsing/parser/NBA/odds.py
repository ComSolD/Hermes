from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from parser.NBA.redact import date_redact, total_odds_redact
from parser.NBA.save import match_table, odds_moneyline_table, odds_total_table, team_table


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
        self.driver.get(f"https://www.oddsportal.com/basketball/usa/nba-{self.first_year}-{self.second_year}/results/")

        time.sleep(5)

        # Переключаемся по страницам
        pagination_links = self.driver.find_elements(By.CSS_SELECTOR, 'a.pagination-link[data-number]')

        max_page_number = max(int(link.get_attribute("data-number")) for link in pagination_links)

        for page in range(max_page_number, 0, -1):
            last_page_link = self.driver.find_element(By.CSS_SELECTOR, f'a.pagination-link[data-number="{page}"]')

            self.driver.execute_script("arguments[0].click();", last_page_link)

            time.sleep(5)

            # Находим все матчи на странице
            matches_selenium = self.driver.find_elements(By.XPATH, f'//a[starts-with(@href, "/basketball/usa/nba-{self.first_year}-{self.second_year}/") and not(@href="/basketball/usa/nba-{self.first_year}-{self.second_year}/") and not(@href="/basketball/usa/nba-{self.first_year}-{self.second_year}/standings/")]')

            matches = list()

            for match in matches_selenium:
                matches.append(match.get_attribute('href'))

            matches.reverse()

            # Открываем каждый матч
            for url in matches:
                self.open_matches_link(url)

                break

            break


        # Закрываем браузер
        self.driver.quit()


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

        self.match_id = "_".join(teams)

        self.match_id += f"_{self.first_year}_{self.second_year}_{match_date.replace('-', '_')}_{dates[2].replace(':', '_')}"


        if match_table(self.match_id, teams_id, f'{self.first_year}/{self.second_year}', match_date, ''):

            return 0

        self.moneyline_for_periods(self.driver, self.moneyline)

        div_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//div[contains(text(), "Over/Under")]'))
        )
        self.driver.execute_script("arguments[0].click();", div_element)

        time.sleep(1)

        self.total_for_periods(self.driver, self.total)

    

    # Функции для работы с ставками
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
                    div_element = WebDriverWait(driver, 10).until(
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
                    div_element = WebDriverWait(driver, 10).until(
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

