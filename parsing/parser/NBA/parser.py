from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import datetime
import time

from parser.NBA.check import check_stat, match_bet_check, stage_check, total_check
from parser.NBA.save import handicap_result_table, moneyline_result_table, player_tables, team_stat_pts_tables, team_stat_tables, team_table, bet_predict_tables, match_table, total_result_table, update_time
from parser.NBA.redact import bet_predict_redact, date_redact_full_month, time_redact


class ParsingNBA(object):
    def __init__(self, first_date, second_date):
        self.service  = Service(executable_path="parser/drivers/chromedriver.exe")
        options = webdriver.ChromeOptions()
        # options.add_extension("parser/drivers/adblock.crx")
        self.driver = webdriver.Chrome(service = self.service, options=options)
        self.driver.maximize_window()
        self.first_date = first_date
        self.second_date = second_date


    def date_cycle(self):
        date_now = datetime.datetime.today()
        date_now = date_now.strftime('%Y-%m-%d')

        start_date = datetime.datetime.strptime(self.first_date, '%Y-%m-%d')
        start_date = start_date.strftime('%Y-%m-%d')
 
        end_date = datetime.datetime.strptime(self.second_date, '%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')

        while (start_date <= end_date):
            date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            date = date.strftime('%Y%m%d')

            self.url = f"https://www.espn.com/nba/schedule/_/date/{date}"
            self.date_match = start_date

            self.get_matches_link()

            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            start_date += datetime.timedelta(days=1)
            start_date = start_date.strftime('%Y-%m-%d')

        update_time()

        self.driver.close()
        self.driver.quit()

        return 'Данные NBA cобраны'

            
    # Сбор всех матчех и проверка их наличия

    def get_matches_link(self):
        self.driver.get(self.url)

        time.sleep(5)

        soup = BeautifulSoup(self.work_with_HTML(),'lxml')


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
                self.open_matches_link("https://www.espn.com" + match)
            except:
                pass

            break


    def open_matches_link(self, link):
        
        self.driver.get(link)

        time.sleep(2)

        split_game_num = link.split('/')
        self.game_num = split_game_num[-2]

        # Дата матча
        date_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.GameInfo__Meta span')

        dates = list()

        for date in date_selenium:
            dates.append(date.get_attribute("textContent"))

        dates = dates[0].split(', ')


        match_date = date_redact_full_month(dates[1] + ' ' + dates[2])

        match_time = time_redact(dates[0])

        # Команды
        teams_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.Gamestrip__TeamContainer div.Gamestrip__Info div.Gamestrip__InfoWrapper div.ScoreCell__Truncate h2'))
        )

        teams = list() # Инициируем массив для записи команд

        for team in teams_selenium: # Записываем команды в наш массив
            teams.append(team.get_attribute('textContent'))

        self.teams_id = team_table(teams[0], teams[1])

        # Создаем уникальный ID
        teams = [team.lower().replace(" ", "_") for team in teams]

        self.match_id = "_".join(teams)

        self.match_id += f"_{match_date.replace('-', '_')}_{match_time.replace(':', '_')}"

        # Получение данных через HTML и запись в список
        totals_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.Gamestrip__Table div.flex div.Table__ScrollerWrapper div.Table__Scroller table.Table tbody.Table__TBODY tr.Table__TR td.Table__TD') # Собирает результаты команд
        stages_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="ScoreCell__GameNote di"]') # Собираем данные об этапе

        totals = list() # Инициируем массив для результата матча
        stages = list() # Инициируем массив для этапа


        for total in totals_selenium: # Записываем итоговый результат
            totals.append(total.get_attribute('textContent'))

        for stage in stages_selenium: # Записываем итоговый результат
            stages.append(stage.get_attribute('textContent'))


        if int(totals[int(len(totals)/2)-1]) > int(totals[-1]):
            resul_team1 = 'Win'
            resul_team2 = 'Lose'
        else:
            resul_team2 = 'Win'
            resul_team1 = 'Lose'


        short_names_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.Kiog a.mLASH') # Собирает название команд
        
        short_names = list() # Инициируем массив для записи команд

        for short_name in short_names_selenium: # Записываем команды в наш массив
            short_names.append(short_name.get_attribute('textContent'))


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

        player_stats = list()

        for playerStat in playerStat_selenium: # Записываем стартер команд
            player_stats.append(playerStat.get_attribute('textContent'))


        if len(player_stats) == 0:
            return False

        time.sleep(2)

        player_link_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="Boxscore Boxscore__ResponsiveWrapper"] div.Wrapper div.Boxscore div.ResponsiveTable div.flex table.Table tbody.Table__TBODY tr[class="Table__TR Table__TR--sm Table__even"] td.Table__TD div.flex a.AnchorLink')) # Собираем игроков команд
        )
        

        player_names = list()
        player_links = list()

        for player_link in player_link_selenium: # Записываем стартер команд
            player_names.append(player_link.get_attribute('textContent'))

        for player_link in player_link_selenium: # Записываем стартер команд
            player_links.append(player_link.get_attribute('href'))

        player_IDs = list()
        new_player_name = list()

        for link in player_links:
            IDs = link.split('/')
            player_IDs.append(IDs[7])
            if len(IDs) == 9:
                name = IDs[8].split('-')
                full_name = ''
                for i in range(0, len(name)):
                    full_name += name[i].upper()
                    if i < len(name)-1:
                        full_name += ' '
                new_player_name.append(full_name)

        if len(new_player_name) == len(player_names):
            player_names = new_player_name

        self.stats = check_stat(player_names, player_stats, player_IDs)

        return True


    # Вспомогательные функции


    def work_with_HTML(self):

        hide_HTML = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'main#fittPageContainer')) # Ищем ссылку на скрытый html
        )

        for html in hide_HTML: # Вытаскиваем html код из селениума
            other_HTML = html.get_attribute('outerHTML')

        with open("parser/HTML/sourse_page.html", "w") as file: # Записываем html
            try:
                file.write(other_HTML)
            except UnicodeEncodeError:
                self.driver.refresh() # Если страница не загрузилась полностью, вылаезт ошибка

                time.sleep(10)

                hide_HTML = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'main#fittPageContainer')) # Ищем ссылку на скрытый html
                )

                for html in hide_HTML: # Вытаскиваем html код из селениума
                    other_HTML = html.get_attribute('outerHTML')

                with open("parser/HTML/sourse_page.html", "w") as file:
                    file.write(other_HTML)


        with open("parser/HTML/sourse_page.html") as file: # Считываем html
            src = file.read()

        return src
