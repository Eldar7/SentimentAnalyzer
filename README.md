[v0.1] Proof of concept
---

Анализ тональности текстов на основе DIALOGUE EVALUATION 2016,
Sentiment Analysis, SentiRuEval-2016
http://www.dialog-21.ru/en/evaluation/2016/sentiment/

***Что сделано:***
- Лемматизация и чистка текста
- RNN с обучающимся словарем
- Тренировка, распознавание, сохранение в *output.xml (валидация calc.js)

***Что можно сделать:***

- Интеграция с word2vec, предобученный словарь
- Доработка лемматриазции, профилактика опечаток в твитах
- Попробовать другие конфигурации сети
- Мерить F-measure, Repcall, Precision на этапе тренировки
- Добиться стабильности в показателях распознаваемости
- *[Интеграция с vk]

***Доделать:***
- Вынести глобальные константы в конфиг
- Output.xml привести в подобающий вид
- Избавиться от хардкода параметров, cmd интерфейс

Результаты запусков: [results.txt](results.txt)

---
## Change Log

### Added
- WHOLE **eval** directory from SentiRueval 2016 - плохая была идея... Надо качать https://drive.google.com/drive/u/0/folders/0BxlA8wH3PTUfTWZxUmFMVlNkVUE и разорхивировать в eval самим с заменой.
- **eval/run_eval.bat** to simplify evaluation execute 
