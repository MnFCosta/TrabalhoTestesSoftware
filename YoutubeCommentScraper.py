from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


#codigo para automatizar scraping de comentário do youtube usando selenium 

options = webdriver.ChromeOptions()
#options.add_argument("--window-size=1980,1020")
options.add_argument("--log-level=3")
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
login_url = 'https://www.youtube.com/'

print('Passo 1: Acessar o Youtube')
try:
    driver.get(login_url)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.save_screenshot('tela01.png')
    time.sleep(2)
except:
    driver.quit()
    print('Erro ao acessar o Youtube')
    quit()


print('Passo 2: Busca pelo video na barra de pesquisa do youtube ')
try:
    action = ActionChains(driver)
    search_box = driver.find_element(By.XPATH, "//input[@id='search']")
    #Simular o mouse passando no menu Departamentos
    #menu = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="search"]')))
    #action.move_to_element(menu).perform()

    action.move_to_element(search_box).click()

    # Digita o que voce colocar no campo de busca
    action.send_keys("Não chora china veia")

    # Pressiona Enter para realizar a busca
    action.send_keys(Keys.ENTER)

    # Executa as ações criadas
    action.perform()

    video = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer")))
    action.move_to_element(video).perform()

    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a/yt-image/img"))).click()
   
    driver.save_screenshot('tela02.png')
    time.sleep(2)
except:
    driver.quit()
    print('Erro ao acessar o menu...')
    quit()

print('Passo 3: Capturar comentários do vídeo')
try:
    wait = WebDriverWait(driver,10)
    with open('comentários_do_video.csv','w') as arquivo:
        for item in range(3): #by increasing the highest range you can get more content
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(3)

        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
            arquivo.write('Comentário: ' + comment.text+'\n\n')

    driver.save_screenshot('tela03.png')

except:
    driver.quit()
    print('Erro ao salvar os comentários :(')
    quit()

print('Passo 4: Retorna a página inicial do youtube')
try:
    
    wait = WebDriverWait(driver,10)
    botaoguia = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="logo-icon"]')))
    action.move_to_element(botaoguia)

    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="logo-icon"]'))).click()
    action.perform()
    time.sleep(5)
    driver.save_screenshot('tela04.png')
    

except:
    driver.quit()
    print('Erro ao retornar a pagina inicial')
    quit()

print('Scraping realizado com sucesso!')
driver.quit()