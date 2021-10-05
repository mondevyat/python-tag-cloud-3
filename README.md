# Обработка естественного языка с использованием Python / NLP with Python

### Парсер, ***реализованный в прошлой лабораторной работе***, проходится по статьям тематики ***"блокчейн"*** и скачивает их при помощи библиотек Selenium и Webdriver (функция parser())
![parser_1](https://i.ibb.co/LPC88VH/image.png)
###
### ***...***
![parser_2](https://i.ibb.co/frjtzP7/image.png)
### Затем функция pdf_reader() считывает весь текст из скаченных статей при помощи библиотеки tika и формирует их в файл AllText.txt
![pdf_reader](https://i.ibb.co/PMq5gWp/image.png)
### После чего в функции extract_keywords() создаётся словарь из ***ключевых терминов***, связанных с тематикой скаченных статей, и каждое их вхождение записывается в файл Keywords.txt при помощи ***Yargy-парсера***
![extract_keywords](https://i.ibb.co/cvTcb17/image.png)
### Следующим делом при помощи библиотек worldcloud и matplotlib функция keywords_tag_cloud() создаёт ***облако тегов*** из текста файла Keywords.txt и сохраняет его в виде изображения под названием "keywords_tag_cloud.png"
![keywords_tag_cloud](https://i.ibb.co/874X88S/keywords-tag-cloud.png)
### Далее отрабатывает функция extract_names() и при помощи библиотеки ***Natasha*** нормализует, леммитизирует и получает фамилии из файла AllText.txt, записывая самые встречающиеся в файл TopSurnames.txt
![extract_names](https://i.ibb.co/80D48kg/image.png)
### Завершает работу программы функция surnames_tag_cloud(), которая аналогично keywords_tag_cloud(), создаёт облако тегов ***ключевых персонажей***, публикующих материалы и выступающих на конференциях
![key_names_tag_cloud](https://i.ibb.co/8j0G7Mz/key-name-tag-cloud.png)
