# -*- coding: utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from yargy.pipelines import morph_pipeline
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from selenium import webdriver
from yargy import rule, Parser
from importlib import reload
from tika import parser
from time import sleep
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,
    
    Doc
)
import datetime
import csv
import os

CSV = 'articles.csv'
ARTICLES_URL = 'https://cyberleninka.ru/search?q=блокчейн&page=1'
TAG_CLOUD_URL = 'https://облакослов.рф/'
WORK_DIR = os.getcwd().replace('\\', '/')

def save_doc(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Автор(ы)', 'Год', 'Издательство', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['author'], item['year'], item['publisher'], item['link']])

def create_download_folder():
    now = datetime.datetime.now()
    os.chdir(WORK_DIR)
    folder_name = str(now).replace(':', '').replace('.', '').replace(' ', '').replace('-', '')
    os.mkdir(str(folder_name))
    path = WORK_DIR + '/' + folder_name + '/'
    return path

def execute_chrome(path, url):
    os.chdir(WORK_DIR)
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : str(path).replace('/', '\\')}
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(options=chromeOptions)
    driver.get(url)
    return driver

def parse(path, driver, page, articles, pagination, pages):
    pages_needed = int(input('Количество требуемых страниц (от 1 до ' + str(len(pages)) + '): '))
    while True:
        try:
            if (pages_needed >= 1 and pages_needed <= len(pages)):
                break
            else:
                pages_needed = int(input('Повторите ввод (от 1 до ' + str(len(pages)) + '): '))
        except ValueError:
            print('Введите число')

    for j in range(pages_needed):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'paginator')))

        filters = driver.find_elements_by_class_name('tag-list')
        filt = filters[1].find_elements_by_tag_name('span')
        for f in filt:
            if f.text == 'Компьютерные и информационные науки':
                f.click()
                break

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'paginator')))
        ul = driver.find_element_by_id('search-results')
        li = ul.find_elements_by_tag_name('li')

        pagination = driver.find_element_by_class_name('paginator')
        pages = pagination.find_elements_by_tag_name('li')

        print('\n\n\n+++++++++++++++\n'
             +'+             +\n'
             +'+ Страница №' + pages[page].text + ' +\n'
             +'+             +\n'
             +'+++++++++++++++\n\n\n')

        for i in range(len(li)):
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'paginator')))

            filters = driver.find_elements_by_class_name('tag-list')
            filt = filters[1].find_elements_by_tag_name('span')
            for f in filt:
                if f.text == 'Компьютерные и информационные науки':
                    f.click()
                    break

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'paginator')))
            ul = driver.find_element_by_id('search-results')
            li = ul.find_elements_by_tag_name('li')

            pagination = driver.find_element_by_class_name('paginator')
            pages = pagination.find_elements_by_tag_name('li')

            title = li[i].find_element_by_tag_name('a')
            authors = li[i].find_element_by_tag_name('span')
            year = li[i].find_element_by_class_name('span-block')
            publisher = year.find_element_by_tag_name('a')
            link = publisher.get_attribute('href')
            year = year.text[:4]

            articles.append(
                {
                    'title': title.text,
                    'author': authors.text,
                    'year': year,
                    'publisher': publisher.text,
                    'link': link
                }
            )

            print('\n= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =\n'
                 +'Название статьи  |  ' + title.text + '\n'
                 +'Автор(ы) статьи  |  ' + authors.text + '\n'
                 +'Год статьи       |  ' + year + '\n'
                 +'Издательство     |  ' + publisher.text + '\n'
                 +'Ссылка на статью |  ' + link + '\n'
                 +'= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =\n')

            print('\nОткрываю данную сатью...\n')
            title.click()

            print('\nСкачиваю статью...\n')
            download = driver.find_element_by_id('btn-download')

            download.click()

            print('\nВозвращаюсь назад...\n')
            driver.execute_script("window.history.go(-1)")

        page += 1

        if (page >= pages_needed):
            print('\n* Конец парсинга! Файл с названием \"' + CSV + '\" создан в локальной директории *\n\n')
            save_doc(articles, CSV)
            break
        else:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'paginator')))
            pagination = driver.find_element_by_class_name('paginator')
            pages = pagination.find_elements_by_tag_name('li')

            pages[page].find_element_by_tag_name('a').click()

    # Ждём загрузки всех файлов
    files = os.listdir(path)
    files = [os.path.join(path, file) for file in files]
    files = [file for file in files if os.path.isfile(file)]

    for file in files:
        if 'crdownload' in file:
            print('Ожидаю загрузки всех файлов...\n\n')
            sleep(10)
            break

def pdf_reader(path):
    print('Начинаю считывать текст из скачанных статей...\n')
    my_file = open('AllText.txt', 'w', encoding='utf-8')
    os.chdir(path)
    files = os.listdir(path)
    files_text = ''
    for i in files:
       files_text += (parser.from_file(i)['content'])
    my_file.write(files_text)
    my_file.close()
    print('\nЗакончил! Файл AllText.txt создан в рабочей директорииn\n\n')

def extract_keywords():
    os.chdir(WORK_DIR)
    
    file = open('AllText.txt', 'r', encoding='utf-8')

    KEYWORDS = morph_pipeline([
        'блокчейн', 
        'биткоин', 
        'криптовалюта', 
        'смарт', 
        'умный',
        'контракт',
        'цифровой',
        'ICO', 
        'транзакция',
        'экономика', 
        'технология', 
        'электронный',
        'правительство', 
        'информационный'
    ])

    text = file.read()
    RULE = rule(KEYWORDS)
    p = Parser(RULE)

    output_file = open('Keywords.txt', 'w', encoding='utf-8')
    keywords_list = []
    for match in p.findall(text):
        keywords_list.append([_.value for _ in match.tokens])

    keywords_list = sum(keywords_list, [])
    keywords_text = ''
    for keyword in keywords_list:
        keywords_text += keyword + ' '

    output_file.write(keywords_text)
    output_file.close()

def keywords_tag_cloud():
    file = open('Keywords.txt', 'r', encoding='utf-8')
    keywords_text = file.read()

    print('Считал содержимое файла Keywords.txt!\n\n')

    cloud = WordCloud(background_color='#30253c').generate(keywords_text)
    plt.imshow(cloud)
    plt.axis('off')
    plt.savefig('keywords_tag_cloud.png')

    print('Файл "keywords_tag_cloud.png", содержащий облако тегов, создан в рабочей директории!\n\n')

def extract_names():
    os.chdir(WORK_DIR)
    
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    ner_tagger = NewsNERTagger(emb)

    names_extractor = NamesExtractor(morph_vocab)

    
    file = open('AllText.txt', 'r', encoding='utf-8')
    text = file.read()
    print('Открыл файл AllText.txt\n\n')
    
    doc = Doc(text)
    print('Считал текст в Doc\n\n')
    print('Начинаю сегментацию...')
    doc.segment(segmenter)
    print('Закончил сегментацию!\n\n')
    print('Начинаю морфологический разбор...')
    doc.tag_morph(morph_tagger)
    print('Закончил морфологический разбор!\n\n') 
    print('Начинаю синтаксический разбор...')
    doc.parse_syntax(syntax_parser)
    print('Закончил синтаксический разбор!\n\n')
    print('Начинаю NER...')
    doc.tag_ner(ner_tagger)
    print('Закончил NER!\n\n')

    print('Нормализую...')
    for span in doc.spans:
        span.normalize(morph_vocab)
    print('Нормализовал!\n\n')

    print('Леммитизирую...')
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
    print('Леммитизировал!\n\n')

    print('Извлекаю имена и фамилии...')
    for span in doc.spans:
        if span.type == PER:
            span.extract_fact(names_extractor)
    print('Извлёк имена и фамилии!\n\n')

    names_dict = {_.normal: _.fact.as_dict for _ in doc.spans if _.fact}
    surnames_list = []
    for i in names_dict.keys():
        if 'last' in names_dict[i]:
            if len(names_dict[i]['last']) > 2:
                surnames_list.append(names_dict[i]['last'])

    output_file = open('AllSurnames.txt', 'w', encoding='utf-8')
    for surname in surnames_list:
            output_file.write(surname + '\n')
    print('Вывел все фамилии в отдельный файл AllSurnames.txt\n\n')

    main_surnames = []
    main_surnames_c = []
    for x in range(len(surnames_list)):
        c = 0
        for y in surnames_list:
            if y == surnames_list[x]:
                c += 1
        main_surnames.append(surnames_list[x])
        main_surnames_c.append(c)

    key_surnames_dict = dict(zip(main_surnames, main_surnames_c))
    key_surnames_dict = {k: key_surnames_dict[k] for k in sorted(key_surnames_dict, key=key_surnames_dict.get, reverse=True)}

    print('Формирую ключевые фамилии...\n\n')
    top_surnames_dict = {}
    for top in key_surnames_dict:
        if key_surnames_dict[top] > 1:
            top_surnames_dict[top] = key_surnames_dict[top]

    top_surnames_text = ''
    for k in top_surnames_dict:
        for v in range(top_surnames_dict[k]):
            top_surnames_text += k + ' '
    top_surnames_file = open('TopSurnames.txt', 'w', encoding='utf-8')
    top_surnames_file.write(top_surnames_text)
    
    print('Записал все ключевые фамилии в файл TopSurnames.txt!\n\n')

def surnames_tag_cloud():
    file = open('TopSurnames.txt', 'r', encoding='utf-8')
    surname_text = file.read()

    print('Считал содержимое файла TopSurnames.txt!\n\n')

    cloud = WordCloud(background_color='#30253c').generate(surname_text)
    plt.imshow(cloud)
    plt.axis('off')
    plt.savefig('key_name_tag_cloud.png')

    print('Файл "key_name_tag_cloud.png", содержащий облако тегов, создан в рабочей директории!\n\n')
    print('\n\n\n\nРабота программы окончена!\n\n\n\n')

def main():
    # Создаём папку, в которую будут загружаться статьи
    path = create_download_folder()
    # Запускаем Chrome с настроенной папкой для загрузки
    driver = execute_chrome(path, ARTICLES_URL)
    # Парсим страницу(ы) и качаем статьи в вышесозданную папку
    parse(path, driver, 0, [], driver.find_element_by_class_name('paginator'), driver.find_element_by_class_name('paginator').find_elements_by_tag_name('li'))
    # Считываем текст из скаченных файлов и объединям их в один
    pdf_reader(path)
    # Выделяем ключевые термины
    extract_keywords()
    # Создаём облаков тегов из терминов
    keywords_tag_cloud()
    # Выделяем ключевые фамилии
    extract_names()
    # Создаём облако тегов из фамилий
    surnames_tag_cloud()

if __name__ == "__main__":
	main()