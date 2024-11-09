from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook





# inicia o navegador
browser = webdriver.Firefox()
#browser = webdriver.Chrome()
browser.get("https://www.linkedin.com/")

# logar-se no site e digitar a palavra chave
print("vamos começar a buscar suas vagas")
search = input("digite sua busca: ")
input("Faça login e volte aqui para pressionar ENTER")

# gerar a lista de vagas no site conforme a palavra chave
browser.get("https://www.linkedin.com/jobs/")
sleep(5)
input_jobs_search = browser.find_element(By.XPATH, "//header//input")
sleep(5)
input_jobs_search.send_keys(search)
sleep(5)
input_jobs_search.send_keys(Keys.ENTER)
sleep(5)

#pega a lista de resultados
ul_element = browser.find_element(By.CSS_SELECTOR, "main div.jobs-search-results-list")
sleep(5)


def scroll_list(pixels):
    browser.execute_script(f"arguments[0].scrollTop += {pixels};", ul_element)
    sleep(2)

links = []
for _ in range(25):
    scroll_list(200)
    links = browser.find_elements(By.XPATH, "//main//div/div//ul//li//a[@data-control-id]")
    print(len(links))
    if len(links) >= 25:
        print(f'chegamos ao numero esperado de {len(links)}')
        break


# prepara a lista para ser gravada numa planilha
spreadsheet = Workbook()

sheet = spreadsheet.active

sheet['A1'] = "NOME DA VAGA"
sheet['B1'] = "LINK DA VAGA"
next_line = sheet.max_row + 1

for link in links:
    text = link.text
    url_link = link.get_attribute("href")

    sheet[f'A{next_line}'] = text
    sheet[f'B{next_line}'] = url_link

    next_line += 1

# salva a lista numa planilha com o nome da palavra chave
spreadsheet.save("vagas_links-"+search+".xlsx")
print("planilha criada")

print("Encerrando busca")

#fecha o browse
browser.quit()

