# Обработка естественного языка с использованием Python / NLP with Python

## Парсер, ***реализованный в прошлой лабораторной работе(bold italic)***, проходится по статьям тематики ***"блокчейн"(bold italic)*** и скачивает их при помощи библиотек Selenium и Webdriver (функция parser())
![parser_1](https://ibb.co/yR8XXH7)
# ...
![parser_2](https://ibb.co/vL0m6K8)
## Затем функция pdf_reader() считывает весь текст из скаченных статей при помощи библиотеки tika и формирует их в файл AllText.txt
![pdf_reader](https://ibb.co/YXHthd9)
## После чего в функции extract_keywords() создаётся словарь из ***ключевых терминов(bold italic)***, связанных с тематикой скаченных статей, и каждое их вхождение записывается в файл Keywords.txt при помощи ***Yargy-парсера(bold italic)***
![extract_keywords](https://ibb.co/GJPvs0b)
## Следующим делом при помощи библиотек worldcloud и matplotlib функция keywords_tag_cloud() создаёт ***облако тегов(bold italic)*** из текста файла Keywords.txt и сохраняет его в виде изображения под названием "keywords_tag_cloud.png"
![keywords_tag_cloud](https://ibb.co/RD47HHV)
## Далее отрабатывает функция extract_names() и при помощи библиотеки ***Natasha(bold italic)*** нормализует, леммитизирует и получает фамилии из файла AllText.txt, записывая самые встречающиеся в файл TopSurnames.txt
![extract_names](https://ibb.co/YXHthd9https://ibb.co/BtVKsk2)
## Завершает работу программы функция surnames_tag_cloud(), которая аналогично keywords_tag_cloud(), создаёт облако тегов ***ключевых персонажей(bold italic)***, публикующих материалы и выступающих на конференциях
![key_names_tag_cloud](https://ibb.co/xMDw7hm)
