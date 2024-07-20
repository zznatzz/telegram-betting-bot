import requests
import datetime
import CommonUtility, Utility
import Results
import pandas as pd
import mysql.connector
import os
import sys

# API and Telegram tokens
ALPHA_VANTAGE_API_KEY = 'FT1EGCJ8PJCVXB4H'
ODDS_API_KEY = '4ed5a6c5691e30531b4c610cdeee9d8e'
TELEGRAM_API_TOKEN = '7154482517:AAHtAskMUIPQBs_LiFJheEeXo0raWtDsqrI'

# Directory path
DIRECTORY_PATH = '~/telegram-betting-bot/'

DB_USER = CommonUtility.getParameterFromFile('DATABASE_USER')
DB_PORT = CommonUtility.getParameterFromFile('DATABASE_PORT')
DB_PWD = CommonUtility.getParameterFromFile('DATABASE_PWD')
DB_SCHEMA = CommonUtility.getParameterFromFile('DATABASE_SCHEMA')
ENV = CommonUtility.getParameterFromFile('ENV')
LEAGUES_LIST_PATH = os.path.dirname(os.getcwd())
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

mydb = mysql.connector.connect(user=DB_USER, password=DB_PWD, host='127.0.0.1', auth_plugin='mysql_native_password')
mycursor = mydb.cursor()

mycursor.execute("INSERT INTO {}.metodo_results \
                  SELECT b.home_team,\
                         b.away_team,\
                         b.home_odd,\
                         b.draw_odd,\
                         b.away_odd,\
                         a.match_date,\
                         b.home_goals,\
                         b.away_goals,\
                         a.competition_cod,\
                         a.match_cod,\
                         a.last_lost_odd,\
                         a.last_lost_home,\
                         a.last_competition_cod,\
                         a.last_diff_goals,\
                         a.tip,\
                         a.competition_cod=a.last_competition_cod,\
                         b.home_goals>b.away_goals,\
                         b.home_goals=b.away_goals,\
                         b.home_goals<b.away_goals,\
                         (b.home_goals+b.away_goals)>=3 \
                  FROM {}.next_metodo a JOIN {}.latest_results b \
                  ON a.match_cod=b.match_cod".format(DB_SCHEMA, DB_SCHEMA, DB_SCHEMA))

mydb.commit()

# Uncomment and update these sections if needed

# mycursor.execute("WITH view AS (SELECT SUM(CASE WHEN home_goals=away_goals THEN draw_odd-1 ELSE -1 END) AS profitto,\
#                                        COUNT(*) AS num_tot_partite,\
#                                        SUM(CASE WHEN home_goals=away_goals THEN 1 ELSE 0 END) AS num_pareggi,\
#                                        SUM(draw_odd) AS draw_sum_odds \
#                                 FROM {}.metodo_results \
#                                 WHERE flag=1) \
#                   SELECT ROUND((profitto/num_tot_partite)*100, 0) AS yield,\
#                          profitto,\
#                          num_tot_partite,\
#                          num_pareggi,\
#                          draw_sum_odds/num_tot_partite AS avg_odd \
#                   FROM view;".format(DB_SCHEMA))
#
# df_report = pd.DataFrame(mycursor.fetchall(), columns=["yield", "profitto", "num_tot_partite", "num_pareggi", "avg_odd"])
#
# Utility.telegram_bot_sendtext("\U0001F4CA Xbot Report Balance \n \
# \n \
# Stake on single match is 1 \n \
# \n \
# \U0001F4B0 Profit/Loss: {} \n \
# \n \
# \U0001F4C8 Yield: {}% \n \
# \n \
# \U0001F4A5 Total Picks: {} \n \
# \n \
# \U0001F522 Average Odd: {} \n \
# ".format(round(df_report.values[0][1], 2), df_report.values[0][0], df_report.values[0][2], round(df_report.values[0][4], 2)))
#
# mycursor.execute("WITH view AS (SELECT SUM(CASE WHEN home_goals=away_goals THEN draw_odd-1 ELSE -1 END) AS profitto,\
#                                        COUNT(*) AS num_tot_partite,\
#                                        SUM(CASE WHEN home_goals=away_goals THEN 1 ELSE 0 END) AS num_pareggi,\
#                                        SUM(draw_odd) AS draw_sum_odds \
#                                 FROM {}.metodo_results \
#                                 WHERE flag=1) \
#                   SELECT ROUND((profitto/num_tot_partite)*100, 0) AS yield,\
#                          profitto,\
#                          num_tot_partite,\
#                          num_pareggi,\
#                          draw_sum_odds/num_tot_partite AS avg_odd \
#                   FROM view;".format(DB_SCHEMA))
#
# df_report = pd.DataFrame(mycursor.fetchall(), columns=["yield", "profitto", "num_tot_partite", "num_pareggi", "avg_odd"])
#
# mycursor.execute("WITH data AS (SELECT match_date AS day,\
#                                        match_cod,\
#                                        CASE WHEN home_goals=away_goals THEN draw_odd-1 ELSE -1 END AS single_profit \
#                                 FROM db_metodo_prod.metodo_results \
#                                 GROUP BY match_cod) \
#                    SELECT day,\
#                           SUM(single_profit) OVER (ORDER BY day) AS cumulative_profit \
#                    FROM data;")
#
# df_report = pd.DataFrame(mycursor.fetchall(), columns=["Data", "Cumulative_Profit"])
#
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# sns.set_style("whitegrid")
#
# # Color palette
# blue, = sns.color_palette("muted", 1)
#
# # Create data
# x = list(range(len(df_report)))
# y = df_report['Cumulative_Profit']
#
# # Make the plot
# fig, ax = plt.subplots()
# ax.plot(x, y, color=blue, lw=3)
# ax.fill_between(x, 0, y, alpha=.3)
# ax.set(xlim=(0, len(x)+1), ylim=(-5, None), xticks=x)
# ax.set_xlabel('#Pick')
# ax.set_ylabel('Cumulative_Profit')
# fig.savefig(os.path.join(DIRECTORY_PATH, 'report_image.jpg'))
#
# Utility.telegram_bot_sendphoto(os.path.join(DIRECTORY_PATH, 'report_image.jpg'))
