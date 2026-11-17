# Таис · MD-пакет для агентов

## Статус и входные данные

Лицо: tais053, утверждённый типаж А / tais-type-053, MAT-R005 v2, Лена и Игорь. Новые листы — пример фотореалистической сдачи, не автоматическое принятие M2/M3. Анимационная часть отложена по прямому указанию пользователя.

Основной источник лица: https://esannikov.github.io/Alive/World/characters/tais/#tais053 . Для сохранения лица используйте исходный портрет, не общий план. Рабочий мастер тела и раннего костюма — TAIS-TP01.

Численный рост ≈154 см — предложение. Книжное соотношение: Таис едва до плеча Федору, с. 19. Не добавлять новые шрамы на лицо, украшения, номера и нашивки без источника или отдельного решения.

## Единый блок генерации

```text
Use case: identity-preserving character production reference. This is Tais, a fictional girl nearly seventeen years old, from ALIVE. Image 1 is the ONLY approved face identity reference tais053. Match her broad cheekbones, compact natural jaw, straight full brows, slightly almond honey-brown eyes, irregular light freckles concentrated over bridge of nose and inner cheeks, naturally full unpainted lips, ash-dark-brown hair. Preserve the same youthful face and proportions, never age her up or turn her into a generic beauty model. All depictions fully clothed and nonsexual. Anatomically plausible petite lean agile build, ordinary teen proportions. Editorial photographic studio reference quality, clean focal detail and anatomically regional skin: fine forehead microrelief, fine eyelid creases appropriate to age, irregular small pores near nose, matte outer cheeks with subtle peach fuzz, restrained nasal sheen, fine natural lip lines, growth-directed eyebrow hairs, coherent catchlights. No uniform pore noise, no grain overlay, no wax skin, no beauty smoothing, no oversharpening. Background for EVERY panel is seamless calm pale warm beige #eee6d9, no scenery, no paper texture, no vignette or dark gradient. Soft neutral directional key from upper left with enough fill to read every detail; subtle form shadows, restrained contact shadows. Premium readable art-department character sheets, generous spacing, clean composition. No added facial scars, tattoos, piercings, jewellery, insignia or numbers on costume. No sexualized posing. No decorative text, no pseudo-glyphs.
```

## Костюмы

- TC01: серая короткая рабочая куртка с капюшоном, бриджи ниже колен с широкими манжетами, чёрными шнурками и крупными боковыми карманами; чёрно-белая бандана, две косы, потёртые ботинки. С. 43–44. Точные швы и конструкция обуви — предложение.
- TC02: тёмно-синяя пайта с глубокими карманами, тёплая футболка, обтрёпанные длинные штаны. Причина замены: куртка не высохла. С. 52.
- TC03: старая джинсовая рубашка из каюты вместо испорченной пайты. С. 377.
- TC04: новые трикотажные спортивные штаны с кулиской и полосатый верх с длинными рукавами, распущенные волосы. С. 458.

## Промпты по листам

Это рабочие рецепты для повторения и дальнейшей правки. Они нормализованы по отобранным результатам; не заявляются полным дословным журналом всех исходных запросов. Подключайте общий блок выше и соответствующие референсы.

### TAIS-TP01 · Паспорт образа

Утверждённая основа лица — tais053. Полная фигура и костюм TC01 разработаны для примера; их утверждение отдельно.

Входные референсы: tais053.

```text
One complete front-facing full-body studio portrait. Match approved tais053 face. Petite nearly-seventeen-year-old, neutral credible proportions, roughly seven heads tall, both feet and hands visible. Use costume TC01. No portrait inset.
```

Оригинал: images/tp01.png

### TAIS-TP21 · Рост и пропорции

154 см — рабочая оценка, а не число из романа.

Программная компоновка: светло-бежевый фон, исходные изображения без ретуши, читаемые подписи из manifest.json. Для карты событий использовать TC01–TC04; для роста — TAIS-TP01 и явную пометку оценки; для знаков — TAIS-TP17 без добавленных эмблем.

Оригинал: images/tp21.png

### TAIS-TP02 · Передние ракурсы

Фронт, профиль и передние три четверти. Единый ранний костюм TC01.

Входные референсы: tais053 + TAIS-TP01.

```text
Three full-body views, same height and foot baseline: front, left profile, front three-quarter. Match TP01 body and costume. Neutral long-lens perspective, no backpack, no crop.
```

Оригинал: images/tp02.png

### TAIS-TP03 · Задние ракурсы

Спина, противоположный профиль и задние три четверти. Это визуальный лист, не ортографическая 3D-проверка.

Входные референсы: tais053 + TAIS-TP01.

```text
Three full-body views: back, opposite profile, rear three-quarter. Same TC01 seam construction and proportions as TP01 and TP02.
```

Оригинал: images/tp03.png

### TAIS-TP04 · Голова в ракурсах

Одна личность в шести ракурсах; бандана и две косы.

Входные референсы: tais053.

```text
Six large head portraits in a 3x2 grid: front, left three-quarter, left profile, right three-quarter, right profile, back. Same bandana, braids, neutral expression.
```

Оригинал: images/tp04.png

### TAIS-TP05 · Макроплан глаза

Светло-карий, медовый оттенок. Рисунок радужки — разработка образа, не буквальный рисунок из текста.

Входные референсы: tais053.

```text
Large eye macro and small identity portrait. Honey-brown iris, real radial fibres, coherent pupil and reflections, delicate age-appropriate eyelid skin. No invented green or blue eyes.
```

Оригинал: images/tp05.png

### TAIS-TP06 · Фактура лица по зонам

Лоб; область глаза; нос; внешняя щека; губы; линия волос. Возрастная фактура без равномерного шума.

Входные референсы: tais053.

```text
One frontal identity portrait plus six macro regions: forehead, eyelid, nose and inner cheek, outer cheek, lips, eyebrow/hairline. Different real regional skin, not repeated noise.
```

Оригинал: images/tp06.png

### TAIS-TP07 · Левая и правая кисти

Ладонные и тыльные поверхности. Форма кистей предложена для персонажа; постоянные шрамы не выдуманы.

Входные референсы: tais053.

```text
Paired left and right palms and dorsal hand views on beige, wrist continuing into charcoal cuff. Five anatomically coherent digits, natural nails, youthful lean hands, no invented scars or rings. Verify handedness visually rather than trusting panel order.
```

Оригинал: images/tp07.png

### TAIS-TP08 · Стопа и обувь

Фронт, бок, задняя часть, подошва и компактный ориентир стопы. Потёртые ботинки описаны на с. 44; конструкция предложена.

Входные референсы: tais053 + TAIS-TP01.

```text
Same worn black boots from TP01: front pair, side, rear pair, sole. A small neutral side view of foot and ankle for anatomy. No excessive individual-toe detail.
```

Оригинал: images/tp08.png

### TAIS-TP09 · Конструкция причёски

Косы, пробор, узел банданы и собранные волосы.

Входные референсы: tais053.

```text
Hairstyle construction in six views: braids and bandana front, side and back, visible parting, knot detail, hair gathered beneath bandana. Preserve roots and hair volume.
```

Оригинал: images/tp09.png

### TAIS-TP10 · Состояния волос

Косы; сухие распущенные; мокрые; убранные под бандану. Во всех видах закрытая повседневная одежда.

Входные референсы: tais053.

```text
Four clothed chest-up states: dry braids, loose dry hair, loose damp hair, hair gathered beneath bandana. Same charcoal opaque crew-neck shirt, no bathing scene.
```

Оригинал: images/tp10.png

### TAIS-TP11 · Мимика: внимание и доверие

Слева направо, сверху вниз: базовое состояние; сосредоточенность; любопытство; скепсис; тихая улыбка; смех.

Входные референсы: tais053.

```text
Six consistent face portraits: guarded baseline, focused listening, curiosity, skepticism, quiet smile, natural laughter. Preserve face through muscular changes.
```

Оригинал: images/tp11.png

### TAIS-TP12 · Мимика: напряжение и уязвимость

Раздражение; сдержанный гнев; испуг; боль; печаль; облегчение. Разница интенсивности не меняет типаж.

Входные референсы: tais053.

```text
Six consistent face portraits: irritation, controlled anger, alarm, restrained pain with no injury shown, grief, relief. Subtle age-appropriate expressions, no face warping.
```

Оригинал: images/tp12.png

### TAIS-TP13 · Повседневная пластика

Стойка, сидение, шаг и приседание. Четыре отдельные позы.

Входные референсы: tais053 + TAIS-TP01.

```text
Four whole-body poses in TC01: alert standing, seated on a simple stool with both feet grounded, walking, balanced crouch. Coherent joints and support.
```

Оригинал: images/tp13.png

### TAIS-TP14 · Активная пластика

Старт бега, торможение, низкое перемещение и вытянутая рука. Четыре отдельные позы.

Входные референсы: tais053 + TAIS-TP01.

```text
Four whole-body action studies in TC01: sprint start, braking, low cautious movement, upward reach. Exactly two connected arms and two connected legs, whole hands and boots in frame.
```

Оригинал: images/tp14.png

### TAIS-TP15 · Костюмы TC01 и TC02

Верхний ряд: ранний комплект спереди и сзади. Нижний: тёмно-синяя пайта и длинные штаны.

Входные референсы: tais053 + TAIS-TP01.

```text
Four full-body views in 2x2: TC01 front/back above, TC02 front/back below. TC01 grey jacket/cargo breeches, TC02 navy hoodie/long dark trousers. Same person and boot construction.
```

Оригинал: images/tp15.png

### TAIS-TP16 · Костюмы TC03 и TC04

Верх: найденная джинсовая рубашка. Низ: новые спортивные штаны и полосатый верх.

Входные референсы: tais053 + TAIS-TP01.

```text
Four full-body views in 2x2: TC03 front/back above, TC04 front/back below. TC03 faded denim shirt/dark long trousers; TC04 new striped long-sleeve shirt/grey drawcord track trousers, loose slightly damp hair.
```

Оригинал: images/tp16.png

### TAIS-TP17 · Крой и крупные детали

Куртка спереди/сзади, бриджи, манжета и карман. Конструкция служит примером детализации.

Входные референсы: tais053 + TAIS-TP01.

```text
Photographic garment flatlay: exact TC01 jacket front/back, breeches, cuff/drawcord macro, pocket/zipper macro. Match TP01 seams. No insignia.
```

Оригинал: images/tp17.png

### TAIS-TP18 · Ранние личные вещи

Рюкзак и бандана. Два состояния каждого предмета; силуэт ладони даёт условный масштаб. Размеры предложены.

Входные референсы: предыдущий принятый лист предмета; лицо не требуется.

```text
Backpack front/back and matching bandana unfolded/folded. Beige flatlay, approximate hand-scale silhouette. Backpack about 42cm high, bandana about 50cm square; dimensions are design proposals.
```

Оригинал: images/tp18.png

### TAIS-TP23 · Магнитная доска — конструктив

Дека около 80 × 24 см; телескопический руль около 90 см над декой. Эти размеры предложены для примера, не взяты из романа. Слева рабочее, справа сложенное состояние; колёс нет.

Входные референсы: предыдущий принятый лист предмета; лицо не требуется.

```text
Magnetic board with NO wheels. Horizontal deck about 80x24cm, vertical telescopic steering column about 90cm above deck, handle width about 38cm. Deployed three-quarter SIDE view and folded top view. Folded stem telescopes and grips tuck inside deck outline. Preserve dark material and muted pink button. Proposed dimensions, not source measurements.
```

Оригинал: images/tp23.png

### TAIS-TP19 · Позднее снаряжение

Лазерный меч: выключенный вид, деталь рукояти, включённый вид. Концепт реквизита; не утверждённая инженерная конструкция.

Входные референсы: предыдущий принятый лист предмета; лицо не требуется.

```text
Same fictional laser sword: inactive hilt, enlarged detail, complete activated view with blade about four times hilt length. No internal construction details. Beige prop-reference photography.
```

Оригинал: images/tp19.png

### TAIS-TP22 · Маркировка костюма

На раннем костюме не добавлены неподтверждённые номер, погоны или эмблема.

Программная компоновка: светло-бежевый фон, исходные изображения без ретуши, читаемые подписи из manifest.json. Для карты событий использовать TC01–TC04; для роста — TAIS-TP01 и явную пометку оценки; для знаков — TAIS-TP17 без добавленных эмблем.

Оригинал: images/tp22.png

### TAIS-TP20 · Карта изменений

Четыре комплекта связаны с событиями; повреждение пайты, перевязка и заживление описаны отдельно.

Программная компоновка: светло-бежевый фон, исходные изображения без ретуши, читаемые подписи из manifest.json. Для карты событий использовать TC01–TC04; для роста — TAIS-TP01 и явную пометку оценки; для знаков — TAIS-TP17 без добавленных эмблем.

Оригинал: images/tp20.png

## Проверка перед публикацией

- Лицо не заменено на tais059 или новый типаж; возраст остаётся подростковым.
- Стороны тела, кисти, пальцы и суставы проверены по изображению; подписи не исправляют ошибочную анатомию.
- Все головы, кисти и обувь входят в кадр; единый костюм сохраняет крой и детали.
- У магнитной доски нет колёс; рабочий руль достаточной высоты, сложенное состояние конструктивно объяснимо.
- Повреждение плеча не получает выдуманную каноническую сторону. С. 317–319 и 417 показывают лечение/заживление; сторона требует отдельного решения.
- Фон спокойный светло-бежевый, без шумной текстуры, драматических бликов и окружения.
- Проверять каждую область кожи в исходном масштабе. При восковом лице — новая экспозиция с исходным портретом.
- Новая публикация не означает утверждение нового листа.
