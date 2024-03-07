from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options)
driver.get("https://www.whoscored.com/Regions/252/Tournaments/2/Seasons/9618/Stages/22076/PlayerStatistics/England-Premier-League-2023-2024")
# button = driver.find_element(By.CLASS_NAME, "css-1wc0q5e").click()
table = driver.find_element(By.ID, "top-player-stats-summary-grid")
text = table.text.split("\n")
cols = [i for i in text[1].split()]
players = text[3::4]
stats = text[5::4]
stats_split = []
for row in stats:
    stats_split.append([i for i in row.split()])

df = pd.DataFrame(stats_split, columns=cols)
df["Player"] = players
df = df[["Player"] + [col for col in df.columns if col != "Player"]]
print(df)
time.sleep(5)