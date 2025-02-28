import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from pathlib import Path
import datetime
import time

from parser.NBA.check import check_stat, id_check, stage_check, total_check
from parser.NBA.save import handicap_result_table, moneyline_result_table, player_tables, team_stat_pts_tables, team_stat_tables, team_table_espn, match_table, total_result_table, update_time
from parser.NBA.redact import date_redact_full_month, time_redact


class ParsingNBA(object):
    def __init__(self, first_date, second_date):
        driver_path = Path("parser/drivers/chromedriver.exe").resolve()
        self.service  = Service(driver_path)
        options = webdriver.ChromeOptions()
        # options.add_extension("parser/drivers/adblock.crx")
        self.driver = webdriver.Chrome(service = self.service, options=options)
        self.driver.maximize_window()
        self.first_date = first_date
        self.second_date = second_date


    def date_cycle(self):

        start_date = datetime.datetime.strptime(self.first_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(self.second_date, '%Y-%m-%d')

        while (start_date <= end_date):
            date = start_date.strftime('%Y%m%d')

            self.url = f"https://www.espn.com/nba/schedule/_/date/{date}"

            self.date_match = start_date.strftime('%Y-%m-%d')

            self.get_matches_link()

            start_date += datetime.timedelta(days=1)

        update_time()

        self.driver.close()
        self.driver.quit()

        return 'Данные NBA cобраны'

            
    # Сбор всех матчех и проверка их наличия

    def get_matches_link(self):
        self.driver.get(self.url)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.Table__TBODY"))
            )
            logging.info(f"Загружена страница: {self.url}")
        except Exception as e:
            logging.warning(f"Ошибка загрузки страницы: {self.url}: {e}")
            return 0

        soup = BeautifulSoup(self.driver.page_source,'lxml')

        no_games = soup.find_all("section", class_="EmptyTable")


        if len(no_games) != 0:
            no_games_date = no_games[0].find("div").get_text()

            no_games_date = no_games_date.split()

            date_check = datetime.datetime.strptime(self.date_match, '%Y-%m-%d')
            day = date_check.strftime('%#d') + ','
            year = date_check.strftime('%Y')

            if day in no_games_date and year in no_games_date:
                return False


        items_tbody = soup.find("tbody", class_="Table__TBODY")

        if items_tbody == None:
            return 0


        items_td = items_tbody.find_all("td", class_="teams__col Table__TD")

        matches = list()

        for td in items_td:
            if len(td) > 0 and td.find("a").get_text() != 'Postponed' and td.find("a").get_text() != 'Canceled':
                matches.append(td.find("a").get("href"))

        
        for match in matches:
            try:
                self.open_matches_link(f"https://www.espn.com{match}")
            except Exception as e:
                logging.error(f"Ошибка при обработке матча {match}: {e}")


    def open_matches_link(self, link):
        
        self.driver.get(link)

        try:
            logging.info(f"Открываем матч: {link}")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.GameInfo__Meta span'))
            )
        except Exception as e:
            logging.error(f"Ошибка загрузки страницы матча {link}: {e}")
            return

        split_game_num = link.split('/')
        self.game_num = split_game_num[-2]

        # Дата матча
        date_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.GameInfo__Meta span')

        dates = [date.get_attribute("textContent") for date in date_selenium]

        dates = dates[0].split(', ')


        match_date = date_redact_full_month(dates[1] + ' ' + dates[2])

        match_time = time_redact(dates[0])

        # Команды
        teams_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.Gamestrip__TeamContainer div.Gamestrip__Info div.Gamestrip__InfoWrapper div.ScoreCell__Truncate h2'))
        )

        teams = [team.get_attribute('textContent') for team in teams_selenium]

        data_teams = team_table_espn(teams[0], teams[1])

        self.teams_id = [data_teams[0], data_teams[1]]

        teams = [data_teams[2], data_teams[3]]

        # Создаем уникальный ID
        teams = [team.lower().replace(" ", "_") for team in teams]

        self.match_id = "_".join(teams)


        self.match_id += f"_{match_date.replace('-', '_')}_%"

        self.match_id = id_check(self.match_id, match_time)

        # Получение данных через HTML и запись в список
        totals_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.Gamestrip__Table div.flex div.Table__ScrollerWrapper div.Table__Scroller table.Table tbody.Table__TBODY tr.Table__TR td.Table__TD') # Собирает результаты команд
        stages_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="ScoreCell__GameNote di"]') # Собираем данные об этапе

        totals = [total.get_attribute('textContent') for total in totals_selenium]
        stages = [stage.get_attribute('textContent') for stage in stages_selenium]


        if int(totals[int(len(totals)/2)-1]) > int(totals[-1]):
            resul_team1 = 'win'
            resul_team2 = 'lose'
        else:
            resul_team2 = 'win'
            resul_team1 = 'lose'
        

        stage = stage_check(stages)

        if stage == 0:
            return 0
        
        total = total_check(totals)


        if not self.open_box_score():
            return 0

        
        if not match_table(self.match_id, self.teams_id, '', self.date_match, stage):

            moneyline_result_table(self.match_id, self.teams_id, total[0])

            total_result_table(self.match_id, total[0])

            handicap_result_table(self.match_id, self.teams_id, total[0])

            team_stat_pts_tables(self.match_id, self.teams_id, total)
            team_stat_tables(self.match_id, self.teams_id, resul_team1, resul_team2, self.stats[0], self.stats[1])
            
            player_tables(self.match_id, self.teams_id[0], self.stats[2], self.stats[4])
            player_tables(self.match_id, self.teams_id[1], self.stats[3], self.stats[5])


    def open_box_score(self):
        
        self.driver.get(f'https://www.espn.com/nba/boxscore/_/gameId/{self.game_num}')


        playerStat_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="Boxscore Boxscore__ResponsiveWrapper"] div.Wrapper div.Boxscore div.ResponsiveTable div.flex div.Table__ScrollerWrapper div.Table__Scroller table.Table tbody.Table__TBODY tr.Table__TR td.Table__TD') # Собираем стартер команд

        player_stats = [playerStat.get_attribute('textContent') for playerStat in playerStat_selenium]


        if len(player_stats) == 0:
            return False

        time.sleep(2)

        player_link_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="Boxscore Boxscore__ResponsiveWrapper"] div.Wrapper div.Boxscore div.ResponsiveTable div.flex table.Table tbody.Table__TBODY tr[class="Table__TR Table__TR--sm Table__even"] td.Table__TD div.flex a.AnchorLink')) # Собираем игроков команд
        )
        
        player_name_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="Boxscore Boxscore__ResponsiveWrapper"] div.Wrapper div.Boxscore div.ResponsiveTable div.flex table.Table tbody.Table__TBODY tr[class="Table__TR Table__TR--sm Table__even"] td.Table__TD div.flex a.AnchorLink span.Boxscore__AthleteName--long') # Собираем стартер команд

        player_names = [player_link.get_attribute('textContent') for player_link in player_name_selenium]


        player_links = [player_link.get_attribute('href') for player_link in player_link_selenium]


        player_IDs = list()

        for link in player_links:
            IDs = link.split('/')
            player_IDs.append(IDs[7])

        self.stats = check_stat(player_names, player_stats, player_IDs)

        return True


