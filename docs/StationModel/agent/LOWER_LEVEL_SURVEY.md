# I рівень МОАГ · звірка з романом і маршрут B1–B4

24 листопада 2026 року. У [переглядачі станції](https://esannikov.github.io/Alive/StationModel/station-3d.html) відкрийте «Навігатор» → «I» → «Пройти I рівень · B1–B4». Стрілки під карткою ведуть від технічної палуби через трюм, бази й Холодний Ангар до нижнього машинного відсіку. Пошук у навігаторі відкриває окрему кімнату.

Номери сторінок відповідають [PDF роману](https://github.com/esannikov/Alive/blob/main/Sources/ALIVE.pdf). Позначення палуб, кути, радіуси та більшість маршрутів обслуговування належать моделі. Опис і походження сцен зібрані в [довіднику нижнього рівня](https://github.com/esannikov/Alive/blob/main/Bible/Environments/Lower_Level.md).

## Сюжетні місця

| Місце | Сторінки | Де подивитися і що там видно |
|---|---|---|
| Відкритий технічний низ, труби й шахти | 15–21, 53, 214 | `huntTunnel`, `huntShaft`, `ventFoot`. У шести вентиляційних станціях B1 бічний вхід виводить на драбину з проміжними майданчиками. Кількість і крок конструкцій задано для моделі. |
| Спільний підхід до двох баз | 18, 21, 218, 262 | `sharedDoor`, `basePipe`, `darkPlan`. Від розвилки можна йти до порога Темної або в трубу до Овальної. |
| Темна база й спальні | 21–30, 133–137, 189, 238, 314 | `darkoval`, `youngRoom`, `farRoom`, `springBed`. Загальна кімната, галерея, спальні, місце Таїс і Федора. |
| Душова, бойлер і сушіння | 23–25, 235–238, 276 | `darkWash`, `baseServices`. Душова та її технічний бік мають окремі ракурси. |
| Овальні, постачання та пізня зустріч | 99–100, 308, 497–501 | `ovalbase` і `ovalSupplyHead` показують базу та змодельований канал подачі. `familyRefuge` веде в колишню каюту за подвійними дверима до Інни, Діни, Рити й Сені. На с. 498 дитина лежить поперек зсунутих ліжок, на с. 499–500 Інна готує частування. Точна адреса каюти та механізм добування харчів лишаються авторськими рішеннями макета. |
| База Диких | 205–208 | `wildTunnelEye`, `wildRoomEye`, `wildTableFood`. Теплотраса, вузький вхід, поворот і кімната Жеки. |
| Сміттєвий цех і деталі | 98, 102–104, 278 | `trashSalvage`, `sorting`, `furnaceRear`, `ashService`. Біля восьми приймачів видно відводи зі стрічки. У картці цеху можна перейти до дошки Федора, преса оборотної тари, ділянки органіки та заднього виходу за піччю. Обладнання відбору й пакування реконструйовано. [Чотири ракурси](recycling-floor.jpg). |
| Повернення з Лоном | 227–229 | `lonLanding`. Кабіна відкривається в коридор. На майданчику Емма й Коля, на вантажному візку ящики та пакунок сухого молока й картоплі. Кнопка в картці зсуває обидві стулки. Кут і конструкція шахти взяті з інженерного плану моделі. |
| Спуск до сміттєвого цеху | 471–472 | `wasteStairs`. За відчиненими дверима видно сходи, що виходять до сортувального цеху. Розміщення й довжину нижньої секції обрано за висотою палуб. Люк за піччю на с. 278–279 і далі має окремий ракурс `furnaceRear`. |
| Прямий транспортний коридор | 214–217 | `straightcorrEye`. Коридор зі слідами руху й прихованим доступом. |
| Квадратний колодязь і ворота | 63–66, 350–353, 472 | `squarewellClose`. Видно колодязь, ворота і їхні сюжетні стани. Від холодного боку воріт пішим маршрутом можна дійти через розвилку з Вовиком і відкриту каюту до вантажного входу Ангару 2. |
| Ангар, місток і лабораторія | 354–359, 515–520, 532 | `hangarCartRoute`, `hangarCatwalk`, `dispatchRoom`, `proflabInterior`, `labLetters`. Візок, підйом, пультова, укриття і знахідки Професора. |
| Комори, стіна імен і покинуті каюти | 264–265, 309, 351–353 | `stores`, `memorial`, `lostCabin`. На стіні ім’я Іллі показане як можливий стан після обіцянки Колі. У холодних каютах з обох галерей видно голі рами ліжок, залишені меблі й погаслі планшети. |

## Як працює ця частина корабля

- **B1.** На нижньому ярусі вентиляційних станцій прорізи й площадки показують, де людина залишає палубу та переходить на наступний проліт.
- **B2.** Візок, мішок і ящик біля роликового стола взяті з бібліотеки. Огороджена верхня станція має барабан на опорах. Проріз у палубі збігається з шахтою камбуза на B3.
- **B3.** У двох галереях холодного півкільця відкрито 38 покинутих кают. При трьох ангарних вестибюлях облаштовано три вмивальні й три кімнати вахти. Центральний прохід у кожній сполучає обидві галереї. Обладнання повторюється інстансами. Для пізнього укриття є окремий дверний проріз.
- **B4.** Гарячі й холодні ємності стоять на сідлових опорах. У торцях є ревізійні кришки. Біля вузла теплообміну на 36° можна простежити обидва контури від апарата до сусідніх ємностей.

## Два піші маршрути B3

- У картці **«Три проходи за воротами колодязя»** відкрийте **«Пройти від воріт до Ангару 2»**. Сім зупинок ведуть від воріт через місце Вовика та відкриту каюту до ангарного вестибюля й вантажного входу. По дорозі можна призупинитися й роздивитися розвилку, написи та бічні виходи. Довжина в моделі 821 м. Роман фіксує розгалуження, каюти й ангар, але не задає кути поворотів, довжину шляху та призначення кожної гілки.
- У картці **«Пізнє укриття Овальних»** відкрийте **«Пройти до укриття Овальних»**. Від переходу між галереями шлях іде вздовж кают, через подвійні двері до порога сімейної кімнати. Чотири зупинки, 195 м за планом моделі. Опора на с. 497–501.

## Обхід та обслуговування

| Палуба | Що з’єднано | Де подивитися |
|---|---|---|
| B1 | Під шістьма радіальними фермами з палуби можна піднятися сімома маршами до галереї. На верхньому проході видно підвіси та кронштейни. | «Сходова вежа під фермою» |
| B2 | Спільна труба огинає два почергові ряди баластних цистерн. Від кожної із 18 ємностей є фланцевий відвід, засувка і доступ до маховика з майданчика. | «Пост баластного колектора» |
| B3 | У 14 службових відсіках з боку кільцевої галереї прорізано проходи до робочих місць. Англійські вказівники ведуть через просвіти в поручнях до дверей. Є підходи до інструментальної, гідравлічного верстака, гаража, архіву й кімнат трьох ангарних змін. | Наприклад, знайдіть «гідравл» або «гараж» у навігаторі. |
| B4 | Замкнений обхід перетинає труби перед теплообмінником на 36°. Бічні гілки виводять до драбин і кришок 20 ємностей. Вісім рядів накопичувачів мають спільний кабельний канал і доступ до кожної із 24 секцій. | «Майданчик ревізії ємності» та «Галерея накопичувачів» |

Географію двох сімейних баз та Ангару 2 звірено за окремими епізодами. Роман не містить суцільного плану палуб B1–B4. Точну ліфтову вісь, підключення цеху до B2, траси труб та робочі відстані обрано для інтерактивної станції.

## Покажчик ракурсів

Покажчик локального переглядача містить 121 зупинку. Нижче їх наведено в порядку екскурсії.

### B1 · Комунікації

- [Гідровузол озера, труби, ферми й вентиляція B1](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=utility)
- [Сходова вежа під фермою](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=trussStairs)
- [Сервісний вхід у вентиляційну шахту](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=ventFoot)
- [Сервісна касета](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=filterBench)

### B2 · Трюми

- [Контейнерні трюми й баластні резервуари B2](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=cargo)
- [Пост баластного колектора](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=ballastValve)
- [Верхня станція кошика Овальних](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=ovalSupplyHead)
- [Пост приймання](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=receiving)

### B3 · Бази дітей

- [Сектор баз · оточення B3](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=basesDistrict)
- [Темна база · план усіх кімнат](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=darkPlan)
- [Спальня молодших](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=youngRoom)
- [Дальня спальня](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=farRoom)
- [Спільні двері та розвилка](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=sharedDoor)
- [Темна база · спільна кімната](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=darkoval)
- [Таїс · Темна база](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=taisFigure)
- [Спальня · з висоти очей](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bedroomEye)
- [Спальня Таїс і Федора](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=springBed)
- [Спальня · підйом від спільної кімнати](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=sleepLanding)
- [Вода та повітря · сервісна шафа](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=baseServices)
- [Душова та бойлер](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=darkWash)
- [Спальні Темної бази](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=darkBunks)
- [Комори зі стелажами](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=stores)
- [Стіна пам’яті](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=memorial)
- [Круглий лаз](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=basePipe)
- [Овальна база · загальний вигляд](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=ovalbase)
- [Чотири ліжка та тумбочки](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=ovalBeds)
- [Стіл Овальних](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=ovalTea)
- [Овальна · шахта B2 і запасний хід](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=ovalAccess)

### B3 · Мисливський хід

Від Темної бази скоби відкритого стояка ведуть у вентканал Кільця 2. За знятим фланцем є настил. Із нього три сходинки спускаються на дах вантажної кліті, а збоку починається драбина до рівня II. Розташування ходів та оснастки відповідає варіанту Б інтерактивної моделі.

- [Вхід у стояк](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=huntTunnel)
- [Усередині вентиляційної дуги](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=huntDuctEye)
- [Вихід крізь фланець](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=huntFlangeEye)
- [Дно шахти 1](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=huntShaft)
- [З даху кліті](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=huntRoofEye)
- [З майданчика вгору](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=huntLadderEye)
- [Увесь хід на B3](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=huntPlan)

### B3 · Коридори й відсіки

- [Радіально-кільцевий план Нижнього рівня B3](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=refugee)
- [Дикі · тепловий вузол](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=wildHeat)
- [Дикі · від кільця до порога](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=wildTunnel)
- [Ввід із кіля в сервісну камеру](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=reactorVault)
- [Сміттєсортувальний цех і Променева піч](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=trash)
- [Конвеєр іграшок і деталей, магнітна дошка й трубки](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=trashSalvage)
- [Променева піч, щупальця-клешні й прохід за цехом](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=furnaceRear)
- [Прямий транспортний коридор із написом](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=straightcorr)
- [Емма в Прямому коридорі перед написом «ОНИ ЗДЕСЬ»](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=straightcorrEye)
- [База Диких · підхід і навколишні відсіки B3](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=wildbase)
- [До Диких · на рівні очей](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=wildTunnelEye)
- [Вузький підхід до Диких і бічний коридор](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=wildApproach)
- [База Диких · Жека за столом](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=wildRoomEye)
- [Дикі · вечеря на столі](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=wildTableFood)
- [База Диких · залізний стіл, Жека й чотири лежанки](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=wildInterior)
- [Квадратний колодязь і Високовольтні ворота](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=squarewell)
- [Ворота Гончих Псів, замок і труба спуску](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=squarewellClose)
- [Колосальні дугові Холодні ангари стаї й лабораторія](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=hangars)
- [Холодний ангар 2 · від візка до містка](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=hangarCatwalk)
- [Від містка до пультової](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=proflab)
- [Лабораторія й укриття Професора усередині](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=proflabInterior)
- [Пультова ручного керування шлюзами Ангару 2](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=dispatchRoom)
- [Інструментальна комора](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayToolCrib)
- [Кабельна траншея](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayCableTrench)
- [Акумуляторна резервного живлення](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayBackupPower)
- [Гідравлічна насосна](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayHydraulicBench)
- [Пост діагностики Донів](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayDonService)
- [Пневматична ресиверна](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayAirPlant)
- [Гараж візків · Ангар 2](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayGarage)
- [Холодний архів Професора](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayArchive)
- [Вимірювальна галерея · вихід Овальної](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayOvalGallery)
- [Роздягальня · Ангар 1](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayCrewOne)
- [Роздягальня · Ангар 2](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayCrewTwo)
- [Роздягальня · Ангар 3](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayCrewThree)
- [Приймання вторсировини](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayScrap)
- [Зворотна вода · за душовою](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bayGreywater)
- [Знахідки в залізному ящику](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=recoveryParts)
- [Оборотна тара · вихід із преса](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=recoveryPack)
- [Органіка · розвантаження барабана](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=recoveryBio)
- [Відчинені двері до сміттєвого цеху](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=wasteStairs)
- [Ліфт Лона · повернення з другого рівня](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=lonLanding)
- [Три проходи за воротами колодязя](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=coldFork)
- [Покинуті каюти за воротами](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=lostCabin)
- [Пізнє укриття Овальних · у гостях із Колею](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=familyRefuge)
- [Вмивальня зміни біля Ангару 2](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=shiftWash)
- [Кімната вахти біля Ангару 2](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=shiftWatch)
- [Верстак ремонту Донів](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=repairBench)
- [Майданчик водяних насосів](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=waterService)
- [Сортувальний пост](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=sorting)
- [Стіл Диких](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=wildMess)

### B3 · Технічні кільця

- [Водяний контур біля дитячих баз](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=plantWater)
- [Очищення повітря](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=plantAir)
- [Галерея розподільних щитів](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=plantPower)
- [Холодильна машина Ангару 2](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=plantCold)

### B3 · Траси й зовнішнє кільце

- [R4 · План майстерень](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=r4WorkshopPlan)
- [D1 · Розбирання Дона](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=r4Strip)
- [М1 · Токарна дільниця](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=r4Lathe)
- [Овальна · оболонка та вихід](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=ovalService)
- [Бази між двома трасами](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=baseRingAccess)
- [W1–W2 · Басейни й аерація](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=outerBasins)
- [E1–E2 · Електричні зали](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=outerPower)
- [T1–T2 · Цистерни й баласт](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=outerReserve)
- [H2 · Радіальний тунель до ангару](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=radialRoads)

### B3 · Холодний ангар 2

- [Чотири вантажні доки](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=freightHull)
- [Вантажний док D01](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=freightDock1)
- [Вантажний док D02](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=freightDock2)
- [Вантажний док D03](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=freightDock3)
- [Вантажний док D04](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=freightDock4)
- [Сервісні люки палуби](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=deckService)
- [Док палубної платформи](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=shuttleDock)
- [Порожні прольоти](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=emptyFrames)
- [Резерв під фермами](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=aftReserve)
- [Ярусні двори · проїзд Y2](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=tierYards)
- [Контейнерний двір](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=handlingCrane)
- [Ремонтний пост](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=handlingShop)
- [Весь Холодний ангар 2](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=hangarWhole)
- [З містка · пост передавання 01](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=hangarDispatchLanes)
- [Розвилка · контейнерна смуга 02](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=hangarCartRoute)
- [Лігво Зграї за контейнерами](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=hangarPackDen)
- [Під фермами Ангару 2](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=hangarRoof)
- [Уздовж дугового містка](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=hangarGalleryWalk)
- [Вантажна галерея Ангару 2](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=hangarFreightView)
- [За другими дверима · житлова кімната](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=labShelter)
- [Знахідка Колі · планшет біля приладів](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=labLetters)

### B4 · Кіль

- [Інженерна палуба B4 та вентральний корпус](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=underside)
- [Осьове ядро · колектори й котушки](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=reactorAxis)
- [Ядро · сервісний теплообмінник](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=reactorService)
- [Галерея накопичувачів](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=bankGallery)
- [Майданчик ревізії ємності](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=vesselLanding)
- [Вузол теплового контуру](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=heatService)
- [Приймання золи](https://esannikov.github.io/Alive/StationModel/station-3d.html#view=ashService)

### B4 · Від реактора до радіатора

Сім зупинок на висоті очей ведуть від зовнішнього обходу реактора вздовж силової шини до розподільного залу, через теплообмінний відсік до вводу в кіль. Восьмий ракурс показує той самий радіатор із космосу. У навігаторі відкрийте «I · Нижній рівень» → «B4 · Від реактора до радіатора». Стрілка «Наступна точка групи» послідовно перемикає зупинки.

У сухому залі дві рами UT-05 з’єднані шинами, дві лінії заходять у перебірку накопичувачів на 128°, допоміжне відгалуження проходить до приводів насосів. За перегородкою стоять дві паралельні пари UT-08 і UT-03. Лінії від реактора приходять до задніх плит теплообмінників. Окремий контур переносить тепло до радіатора на 150° та повертає охолоджений теплоносій через насоси. На обшивці видно поле з 32 плит. Це просторове рішення для інтерактивної моделі.
