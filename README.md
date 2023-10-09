# goit_python_web_hw_08
GoIT, Python WEB, Homework number 08. NoSQL. MongoDB.


### Перша частина
#### Вихідні дані

У нас є json файл з авторами та їх властивостями: дата та місце народження, короткий опис біографії.
Також ми маємо наступний json файл із цитатами від цих авторів.

#### Порядок виконання

  Створіть хмарну базу даних Atlas MongoDB
  За допомогою ODM Mongoengine створіть моделі для зберігання даних із цих файлів у колекціях authors та quotes.
  Під час зберігання цитат (quotes), поле автора в документі повинно бути не рядковим значенням, а [Reference fields](http://docs.mongoengine.org/guide/defining-documents.html?highlight=ReferenceField#reference -fields) полем, де зберігається ObjectID з колекції authors.
  - Напишіть скрипти для завантаження json файлів у хмарну базу даних.
  - Реалізуйте скрипт для пошуку цитат за тегом, за ім'ям автора або набором тегів. Скрипт виконується в нескінченному циклі і за допомогою звичайного оператора input приймає команди у наступному форматі команда: значення. Приклад:

    - name: Steve Martin — знайти та повернути список всіх цитат автора Steve Martin;
    - tag:life — знайти та повернути список цитат для тега life;
    - tags:life,live — знайти та повернути список цитат, де є теги life або live (примітка: без пробілів між тегами life, live);
    - exit — завершити виконання скрипту;

    Виведення результатів пошуку лише у форматі utf-8;

#### Додаткове завдання

Подумайте та реалізуйте для команд name:Steve Martin та tag:life можливість скороченого запису значень для пошуку, як name:st та tag:li відповідно;
Виконайте кешування результату виконання команд name: та tag: за допомогою Redis, щоб при повторному запиті результат пошуку брався не з MongoDB бази даних, а з кешу;

##### Підказка

    Для команд name:st та tag:li використовуйте регулярні вирази в String queries


### Друга частина

Напишіть два скрипти: consumer.py та producer.py. Використовуючи RabbitMQ, організуйте за допомогою черг імітацію розсилки email контактам.

Використовуючи ODM Mongoengine, створіть модель для контакту. Модель обов'язково повинна включати поля: повне ім'я, email та логічне поле, яке має значення False за замовчуванням. Воно означає, що повідомлення контакту не надіслано і має стати True, коли буде відправлено. Інші поля для інформаційного навантаження можете придумати самі.

Під час запуску скрипта producer.py він генерує певну кількість фейкових контактів та записує їх у базу даних. Потім поміщає у чергу RabbitMQ повідомлення, яке містить ObjectID створеного контакту, і так для всіх згенерованих контактів.

Скрипт consumer.py отримує з черги RabbitMQ повідомлення, обробляє його та імітує функцією-заглушкою надсилання повідомлення по email. Після надсилання повідомлення необхідно логічне поле для контакту встановити в True. Скрипт працює постійно в очікуванні повідомлень з RabbitMQ.

Заглушка може імітувати поведінку існуючого коду (наприклад, процедури на віддаленому комп'ютері) або бути тимчасовою заміною ще не створеного коду. Наприклад, замість функції, що виконує складні обчислення, можна тимчасово (доки не буде написана сама функція) поставити заглушку, що завжди повертає 1, і налагоджувати інші функції, що залежать від неї.

#### Додаткове завдання
Введіть у моделі додаткове поле телефонний номер. Також додайте поле, що відповідає за кращий спосіб надсилання повідомлень — SMS по телефону або email. Нехай producer.py відправляє у різні черги контакти для SMS та email. Створіть два скрипти consumer_sms.py та consumer_email.py, кожен з яких отримує свої контакти та обробляє їх.


### RESULT

#### SEED
```
src/main.py"
connect_db - ok
added authors id: 652425416f6a5cc787f5fbe0 (Albert Einstein)
added authors id: 652425416f6a5cc787f5fbe1 (Steve Martin)
added quotes id: 652425416f6a5cc787f5fbe2
added quote of quote.author Albert Einstein, author id [652425416f6a5cc787f5fbe0] = (Albert Einstein) 
added quotes id: 652425416f6a5cc787f5fbe3
added quote of quote.author Albert Einstein, author id [652425416f6a5cc787f5fbe0] = (Albert Einstein) 
added quotes id: 652425416f6a5cc787f5fbe4
added quote of quote.author Albert Einstein, author id [652425416f6a5cc787f5fbe0] = (Albert Einstein) 
added quotes id: 652425416f6a5cc787f5fbe5
added quote of quote.author Steve Martin, author id [652425416f6a5cc787f5fbe1] = (Steve Martin) 
```

#### SEARCH
```
/src/main.py"
connect_db - ok
added authors id: 652427d2a11bdaf84635efa9 (Albert Einstein)
added authors id: 652427d2a11bdaf84635efaa (Steve Martin)
added quotes id: 652427d2a11bdaf84635efab
added quote of quote.author Albert Einstein, author id [652427d2a11bdaf84635efa9] = (Albert Einstein) 
added quotes id: 652427d2a11bdaf84635efac
added quote of quote.author Albert Einstein, author id [652427d2a11bdaf84635efa9] = (Albert Einstein) 
added quotes id: 652427d2a11bdaf84635efad
added quote of quote.author Albert Einstein, author id [652427d2a11bdaf84635efa9] = (Albert Einstein) 
added quotes id: 652427d3a11bdaf84635efae
added quote of quote.author Steve Martin, author id [652427d2a11bdaf84635efaa] = (Steve Martin) 
>>>help
List of commands: ('name', 'tag', 'help', 'exit'),  please to use ':' as argument separator
>>>name bert
command 'name bert' - unknown, can use 'help' for list of commands
>>>name:bert 
command 'name' - args: bert
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“The world as we have created it is a process of our thinking. It '
          'cannot be changed without changing our thinking.”',
 'tags': ['change', 'deep-thoughts', 'thinking', 'world']}
[ 2 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“There are only two ways to live your life. One is as though '
          'nothing is a miracle. The other is as though everything is a '
          'miracle.”',
 'tags': ['inspirational', 'life', 'live', 'miracle', 'miracles']}
[ 3 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“Try not to become a man of success. Rather become a man of value.”',
 'tags': ['adulthood', 'success', 'value']}
>>>name: mart
command 'name' - args: mart 
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Steve Martin',
 'quote': '“A day without sunshine is like, you know, night.”',
 'tags': ['humor', 'obvious', 'simile']}
>>>tag: liv
command 'tag' - args: liv 
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“There are only two ways to live your life. One is as though '
          'nothing is a miracle. The other is as though everything is a '
          'miracle.”',
 'tags': ['inspirational', 'life', 'live', 'miracle', 'miracles']}
>>>tag: succ
command 'tag' - args: succ
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“Try not to become a man of success. Rather become a man of value.”',
 'tags': ['adulthood', 'success', 'value']}
>>>tag:     
for command 'tag' arguments is empty
>>>tag: ""
command 'tag' - args: ""
Not Found
>>>tag: xxxxx
command 'tag' - args: xxxxx
Not Found
>>>name: wwwwww
command 'name' - args: wwwwww
Not Found
>>>exit
command 'exit'
```

#### MULTIPLE not full TAGS
```
>>>tag:li,suc 
command 'tag' - args: li,suc 
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“There are only two ways to live your life. One is as though '
          'nothing is a miracle. The other is as though everything is a '
          'miracle.”',
 'tags': ['inspirational', 'life', 'live', 'miracle', 'miracles']}
[ 2 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“Try not to become a man of success. Rather become a man of value.”',
 'tags': ['adulthood', 'success', 'value']}
Time execution: -0.03691690001869574
```


#### UTF-8
>>>tag: live,марія                                                                                                          
command 'tag' - args: live,марія 
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“There are only two ways to live your life. One is as though '
          'nothing is a miracle. The other is as though everything is a '
          'miracle.”',
 'tags': ['inspirational', 'life', 'live', 'miracle', 'miracles']}
[ 2 ] ----------------------------------------------------------------------------------------------------
{'author': 'Steve Martin',
 'quote': '“A day without sunshine is like, you know, night.”',
 'tags': ['humor', 'obvious', 'simile', 'марія']}
Time execution: 0.019614700024249032
>>>

#### REDIS CACHE

```
command 'name' - args: albert
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“The world as we have created it is a process of our thinking. It '
          'cannot be changed without changing our thinking.”',
 'tags': ['change', 'deep-thoughts', 'thinking', 'world']}
[ 2 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“There are only two ways to live your life. One is as though '
          'nothing is a miracle. The other is as though everything is a '
          'miracle.”',
 'tags': ['inspirational', 'life', 'live', 'miracle', 'miracles']}
[ 3 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“Try not to become a man of success. Rather become a man of value.”',
 'tags': ['adulthood', 'success', 'value']}
Time execution: 0.02808839999488555
>>>name: albert
command 'name' - args: albert
[ 1 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“The world as we have created it is a process of our thinking. It '
          'cannot be changed without changing our thinking.”',
 'tags': ['change', 'deep-thoughts', 'thinking', 'world']}
[ 2 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“There are only two ways to live your life. One is as though '
          'nothing is a miracle. The other is as though everything is a '
          'miracle.”',
 'tags': ['inspirational', 'life', 'live', 'miracle', 'miracles']}
[ 3 ] ----------------------------------------------------------------------------------------------------
{'author': 'Albert Einstein',
 'quote': '“Try not to become a man of success. Rather become a man of value.”',
 'tags': ['adulthood', 'success', 'value']}
Time execution: 0.009065599966561422
>>>

```

