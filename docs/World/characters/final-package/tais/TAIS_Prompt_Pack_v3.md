# Таис · пакет промптов v3.0

## Референсы

- Типаж А · [tais053](https://esannikov.github.io/Alive/World/characters/tais/#tais053).
- [Согласованный портрет v3](images/v3/face-master.png) закрепляет лицо, мягкий рельеф под носом, глаза, веснушки и пропорции.
- [Мастер базового костюма TC01](images/v3/tp01.png) закрепляет силуэт, крой и цвет. Красная хлопковая бандана с мелкой сакурой, тёмно-синий анорак с асимметричным воротником, карманом на левой груди, усилением на правом рукаве. Свободные серо-бежевые карго, тёмные запылённые туфли.
- [Контроль света и цвета](images/v3/tp-control.png) задаёт мягкое нейтральное освещение на очень светлом бежевом фоне.
- [Модельный лист фигуры](images/v3/tp24.png) для сверки посадки одежды и пропорций. Рабочий рост около 154 см, в романе Таис едва до плеча Федору (с. 19).
- [Манифест](manifest.json) содержит коды, ревизии и исходные страницы.

## Премиальный блок

```text
Premium photoreal live-action character reference, natural soft directional high-CRI studio daylight, soft bounced shadows, neutral skin tones, realistic regional skin texture with fine pores and subtle freckles, sharp eyes and individual strands of hair, material-specific woven fibers, coherent seams and folds, restrained local contrast, natural photographic depth, clean very light warm beige seamless background. Worn garments show ordinary patina at contact points with physically plausible folds and stitching, with no synthetic surface pattern, crackle, embossed skin, grain clumps, beauty retouch or excessive sharpening.
```

Для кадров базовой серии сначала загрузите портрет, затем мастер TC01. Для листов рук, аксессуаров и сюжетного гардероба добавьте соответствующие исходные листы v2. При смене костюма сохраняйте лицо, возраст, рост и пластику. Ниже сохранены текстовые запросы на английском и русские подписи для издательской сборки.

## Листы и запросы

### TAIS-TP01 · Паспорт образа

Типаж А (tais053) в согласованном костюме TC01, редакция 2. Тёмно-синий анорак, длинные брюки карго и приглушённо-красная бандана с сакурой.


```text
Premium photoreal live-action character reference, natural soft directional high-CRI studio daylight, soft bounced shadows, neutral skin tones, realistic regional skin texture with fine pores and subtle freckles, sharp eyes and individual strands of hair, material-specific woven fibers, coherent seams and folds, restrained local contrast, natural photographic depth, clean very light warm beige seamless background. Worn garments show ordinary patina at contact points with physically plausible folds and stitching, with no synthetic surface pattern, crackle, embossed skin, grain clumps, beauty retouch or excessive sharpening.

Create exactly one full-length vertical 2:3 approved costume photograph of fictional ALIVE character Tais. IMAGE 1 (the approved premium portrait v3) locks her identity: same facial proportions, amber-brown eyes, freckles, small beauty mark, brows, nose, lips, barely defined soft philtrum, restrained direct expression, dark brown braids and flyaway side fringe, age and build. Transfer the identity precisely with the same naturally young facial proportions and no beauty changes. IMAGE 2 (full-length costume reference) locks her exact outfit, stance, arrangement, fit and proportions. Copy the dark slate-navy canvas hooded half-zip anorak cut, high asymmetric collar with snap and taupe inner facing, zipper length, single rectangular taupe buttoned flap pocket on her left chest (viewer right), low kangaroo pocket, darker seam construction, slate blue reinforcement on her right forearm (viewer left), original snap cuffs, roomy but wearable silhouette, matching original baggy greige cargo trousers with side patch pockets and natural leg folds, and exactly the same low heavy dark brown shoes with visible traces of dry dust and wear across toes and sole edges. Preserve silhouette and original color blocking. Retain her brief natural three-quarter shoulders and both hands relaxed, weight grounded, eyes toward camera, both braids arranged as in source. The only design update is the bandana: preserve its exact placement, knot, tail, folds and scale. Use a muted dusty brick red or soft madder wine red cotton (around #8f4548 in neutral light), low satin-free sheen. Add a legible small Japanese sakura textile motif: sparse ivory and faded blush five-petaled blossoms with subtly notched tips, a few fine stems and buds, articulated as repeat-printed cloth that follows the folds. Delicate scale with room for the red field. No lettering, ornament or costume accents elsewhere. Photograph her standing head-to-toe against the light warm beige reference sweep, with visible floor under both shoes, comfortable headroom and a soft grounded contact shadow. Camera at lower chest height, natural 55–70mm full-body perspective, both shoes completely in frame, no elongation. No captions or branding.
```

[Лист PNG](images/v3/tp01.png)

### TAIS-TP21 · Рост и пропорции

154 см — рабочая оценка для сопоставления кадров. В романе Таис едва до плеча Федору.

Поставить TAIS-TP01 на общий фон. Добавить ориентир ≈154 см с пометкой «Рабочая оценка роста».

[Лист PNG](images/v3/tp21.png)

### TAIS-TP24 · Модельный лист фигуры


```text
Premium ALIVE live-action model documentation. True photographic material and natural detail in skin, hair and woven cloth, soft directional neutral daylight, restrained contrast, light warm beige seamless studio background, consistent shadow and scale, mild honest wear rather than embossed textures, no text, grids, borders, logos or typography. Input portrait locks the same approved Tais face with original proportions and softened philtrum; the full-body input locks build, exact clothing, dusty boots, restrained brick-red sakura bandana, and styling whenever worn.

A neutral technical costume-fitting sheet of the same slim short fictional character Tais to check overall proportions and clothing fit. Horizontal 3:2, three equally sized full-body orthographic reference views of the same person: straight front, strict left side, straight back. Grounded relaxed neutral pose with hands at sides, no exaggerated proportions. Wear an entirely opaque modest dark slate athletic base-layer set consisting of a close-fitting plain high-neck sleeveless tank top, long enough to fully cover torso and tucked in, and plain close-fitting above-knee bike-length base-layer shorts, plus simple dark socks. No skin exposure beyond arms and lower legs. The purpose is technical modeling and garment fit. Calm factual photographic rendering, equal scale, same floor line, do not stylize figure, no anatomical grids or text, no measuring tools. Preserve original face, two braids and muted sakura bandana to identify Tais.

Final wardrobe refinement on the generated base sheet:
Strict local wardrobe edit of the existing technical costume-fitting model sheet, all three equal-scale full-body front / side / back views. Make the existing dark charcoal opaque bike-length shorts into simple shorter training shorts, with a clearly shorter straight hem in the upper half of each thigh, approximately halfway between the original hem and the inseam junction. A practical short athletic cut with secure complete coverage and flat opaque stretch fabric, never a brief shape. Use precisely the same dark fabric, waist position and plain waistband. Alter only the lower hems of the six short legs and reveal the previously covered strips of thigh in an anatomically continuous way. Keep the front, left profile, and back neutral stance, full length and equal floor line, natural body shape and calibrated limb proportions, camera, original facial identity and expression, arms and hands, same high-neck sleeveless base-layer top, braids, red Japanese floral bandana, socks, matte light beige background and studio lighting. Flat technical wardrobe photography, no posing change, no emphasis or close-up, no captions.

Final reference match and short athletic cut:
Strict localized edit of image 1, a technical neutral character turnaround sheet with three whole-body equally scaled views and studio reference clothing. Image 2 is the original identity-master portrait of the SAME fictional Tais, her precise face. Priority is restore facial identity and optical clarity: transfer the exact approved face from image 2 to the frontal face of the left figure, matching her sober straight gaze, original eyelids and eye spacing, amber-brown eye color, eyebrows, freckles, cheek marking, nose width, soft natural philtrum, lip outline and corners, chin and cheekbones. Keep the same head angle and preserve her specific facial silhouette and nose in profile. The rear head stays rear. Preserve the dusty red sakura bandana and braids of image 1. Second local change: adjust the hem of the existing matte charcoal training shorts just slightly upward by about 1 cm on each leg in all three views, maintain a normal short athletic fit, fully opaque secure coverage, waist and flat seam shape. Keep the plain charcoal high-neck training top. Keep scale, standing posture and arm positions, hands, socks, background, lighting, fully visible feet, character age and physical proportions exactly in place. Simple reference photos and no stylization. No extra closeup, no emphasis, no layout changes, no labels.

Final sequential reference edits:
Extremely localized documentation photo edit. Use the exact provided accepted 3-view technical model sheet as the source. ONLY replace the dark ankle socks in all three panels with naturally bare feet in exactly the same neutral grounded position on the floor, correct anatomy consistent with the front, left profile and rear viewing angles, neutral studio lighting and unobtrusive contact shadows. Do not reframe or zoom. Preserve exact already approved face and hair, facial expression, muted sakura bandana, silhouette and body proportions, fitted matte high-neck top, exact already approved short charcoal athletic shorts including their hems and fit, hand position, leg alignment, headroom, same beige backdrop and same three-figure layout. Pixel-faithful unchanged composition outside the sock areas. Natural photographic detail. No captions.

Only edit the hair and headwear of the three figures in this exact neutral technical full-body turnaround photograph. Remove the red bandana completely in all three figures and undo both braids. Reveal Tais's original natural brown hairline and side part. Dark ash-brown medium-long unstyled loose hair with subtle waves, dry, falling naturally to upper shoulder blades in back, slightly longer in back, her familiar loose side fringe. Front view: keep both eyebrows, eyes, cheeks and outline of her exact face clearly visible; most hair can sit behind her shoulders with a few strands forward. Left profile: place hair naturally behind the visible ear and around the back of the shoulder, keep the exact nose, brows, lip and chin silhouette. Rear view: show the same length and hair color, loose at upper shoulder blades, no ties or cloth. Preserve exact approved faces in front and side and all other details, same three full-body views at same scale and spacing, neutral posture, exact matte high-neck top, exact approved short charcoal sports shorts and their leg hems, same bare feet with no socks, beige backdrop and existing lighting. Adjust only hair/headwear in all three panels. Preserve eyes and freckling. Do not crop or change the camera. No captions.
```

[Лист PNG](images/v3/tp24.png)

### TAIS-TP02 · Передние ракурсы

Фронт, профиль и передние три четверти. Карман на левой груди Таис и усиление на её правом рукаве задают асимметрию костюма.


```text
Premium ALIVE live-action model documentation. True photographic material and natural detail in skin, hair and woven cloth, soft directional neutral daylight, restrained contrast, light warm beige seamless studio background, consistent shadow and scale, mild honest wear rather than embossed textures, no text, grids, borders, logos or typography. Input portrait locks the same approved Tais face with original proportions and softened philtrum; the full-body input locks build, exact clothing, dusty boots, restrained brick-red sakura bandana, and styling whenever worn.

Wide 3:2 model sheet, precisely three full-length views FRONT, strict side profile, frontal 3/4. Feet on same horizontal floor line, equal scale, no overlap. Anatomically plausible and the exact same person and costume in all views, relaxed neutral arms. Port and starboard asymmetry matters: her left chest (right to viewer in front) carries the one taupe buttoned flap pocket, her right forearm (left to viewer in front) the blue reinforcement; long baggy greige cargo trousers, dusty dark shoes.
```

[Лист PNG](images/v3/tp02.png)

### TAIS-TP03 · Задние ракурсы

Задние три четверти с обеих сторон и вид со спины. Швы спинки и положение узла — рабочие детали для моделирования.


```text
Premium ALIVE live-action model documentation. True photographic material and natural detail in skin, hair and woven cloth, soft directional neutral daylight, restrained contrast, light warm beige seamless studio background, consistent shadow and scale, mild honest wear rather than embossed textures, no text, grids, borders, logos or typography. Input portrait locks the same approved Tais face with original proportions and softened philtrum; the full-body input locks build, exact clothing, dusty boots, restrained brick-red sakura bandana, and styling whenever worn.

Wide 3:2 model sheet, exactly three full-length views REAR THREE QUARTER, straight BACK, opposite REAR THREE QUARTER. Same floor line and scale, distinct poses at rear angle, head always turned with torso. Preserve original design with fabric hood folded against shoulders, neatly finished back panel, loose long cargo legs, red floral headscarf knot and short tails tied behind. Back seams and knot are plausible design studies.
```

[Лист PNG](images/v3/tp03.png)

### TAIS-TP04 · Голова в ракурсах

Шесть ракурсов типажа А. Сверяйте пропорции лица, косы и посадку банданы по утверждённому портрету.


```text
Premium ALIVE live-action model documentation. True photographic material and natural detail in skin, hair and woven cloth, soft directional neutral daylight, restrained contrast, light warm beige seamless studio background, consistent shadow and scale, mild honest wear rather than embossed textures, no text, grids, borders, logos or typography. Input portrait locks the same approved Tais face with original proportions and softened philtrum; the full-body input locks build, exact clothing, dusty boots, restrained brick-red sakura bandana, and styling whenever worn.

Wide 3:2 sheet exactly six chest-up photos in 2 rows of 3 at a fixed scale. Front neutral, left three-quarter, left exact profile; right three-quarter, right exact profile, rear head. Identical approved Tais face, two loose brown braids, muted brick-red cotton wrap with tiny ivory sakura. Same original high-collar navy anorak at bottom of each frame. Every image has breathing room and full bandana.
```

[Лист PNG](images/v3/tp04.png)

### TAIS-TP05 · Макроплан глаза

Медово-карий глаз. Фрагмент контрольного портрета, увеличенный для сравнения радужки, век и брови.

Увеличенный фрагмент радужки и полного контрольного портрета.

[Лист PNG](images/v3/tp05.png)

### TAIS-TP06 · Фактура лица по зонам

Крупные фрагменты одного контрольного портрета. Рельеф под носом оставлен мягким и неглубоким.

Шесть кропов из контрольного портрета, собранных с общим видом лица и подписями.

[Лист PNG](images/v3/tp06.png)

### TAIS-TP07 · Левая и правая кисти

Сверху — правая и левая ладони. Снизу — тыльная сторона левой и правой кисти. Стороны определены относительно Таис.


```text
Premium ALIVE live-action model documentation. True photographic materials and natural regional details, gentle neutral light, restrained contrast, light warm beige seamless studio background, consistent scale, real fabric wear, no artificial textures, no captions or logos.

Source-preserving edit of first landscape photographic hand board, exact positions, distinct sides, all four hands each with five correct fingers: top left right palm, top right left palm, bottom left dorsal left, bottom right dorsal right. Match only the navy canvas snap cuffs of second costume reference where wrists are visible. Preserve anatomy, natural skin and nails, no jewelry.
```

[Лист PNG](images/v3/tp07.png)

### TAIS-TP08 · Обувь и пыль

Низкая тёмно-коричневая обувь с потёртостями и сухой пылью. В кадре сохранён широкий низ серо-бежевых брюк.


```text
Premium ALIVE live-action model documentation. True photographic material and natural detail in skin, hair and woven cloth, soft directional neutral daylight, restrained contrast, light warm beige seamless studio background, consistent shadow and scale, mild honest wear rather than embossed textures, no text, grids, borders, logos or typography. Input portrait locks the same approved Tais face with original proportions and softened philtrum; the full-body input locks build, exact clothing, dusty boots, restrained brick-red sakura bandana, and styling whenever worn.

Wide landscape horizontal two side-by-side tightly framed equipment reference photos of the exact scuffed low dark brown utility shoes from the full body reference. Boots on feet with only the cropped hems of the identical loose greige cargo trousers visible, no view of other body parts. Left photo side and front three quarter view of both boots on ground. Right photo sharp side profile of one boot to read outsole, eyelets, toe seam and dry powder dirt. Same sole profile and upturned toe as the input.
```

[Лист PNG](images/v3/tp08.png)

### TAIS-TP09 · Конструкция причёски

Две косы, естественная линия волос, завязанный сзади платок из красной ткани с мелкой сакурой.


```text
Premium ALIVE live-action model documentation. True photographic material and natural detail in skin, hair and woven cloth, soft directional neutral daylight, restrained contrast, light warm beige seamless studio background, consistent shadow and scale, mild honest wear rather than embossed textures, no text, grids, borders, logos or typography. Input portrait locks the same approved Tais face with original proportions and softened philtrum; the full-body input locks build, exact clothing, dusty boots, restrained brick-red sakura bandana, and styling whenever worn.

Wide 3:2 plate exactly three waist-up photographic rear views. First left rear 3/4 shows the braid base at nape, second straight rear shows the dusty red bandana knot and two short sakura-printed cloth tails and asymmetric drape, third right rear 3/4 sees where twin braids fall along the shoulder. Same dark brown hair, field of tiny ivory five-petalled blossoms on matte red cloth, exact slate navy anorak. Real knots and hair anatomy, easy to read.
```

[Лист PNG](images/v3/tp09.png)

### TAIS-TP10 · Состояния волос

Косы в бандане, сухие распущенные, влажные распущенные, собранные под банданой. Силуэт анорака служит общей опорой.


```text
Premium ALIVE live-action model documentation. True photographic material and natural detail in skin, hair and woven cloth, soft directional neutral daylight, restrained contrast, light warm beige seamless studio background, consistent shadow and scale, mild honest wear rather than embossed textures, no text, grids, borders, logos or typography. Input portrait locks the same approved Tais face with original proportions and softened philtrum; the full-body input locks build, exact clothing, dusty boots, restrained brick-red sakura bandana, and styling whenever worn.

Wide visual character-continuity plate, precisely four head-and-shoulder views across one row at a fixed scale, approved identical face, in the same closed high collar anorak. Show (left to right) twin braids with dusty red sakura bandana, dry loose hair natural shoulder length without bandana, damp loose hair brushed back without bandana, two braids gathered with bandana and short tails. Non-glamorous studio lighting, nothing other than hair configuration varies.
```

[Лист PNG](images/v3/tp10.png)

### TAIS-TP11 · Мимика: внимание и доверие

Шесть выражений: нейтральное, сосредоточенность, любопытство, скепсис, улыбка и смех.


```text
Premium ALIVE live-action model documentation. True photographic material and natural detail in skin, hair and woven cloth, soft directional neutral daylight, restrained contrast, light warm beige seamless studio background, consistent shadow and scale, mild honest wear rather than embossed textures, no text, grids, borders, logos or typography. Input portrait locks the same approved Tais face with original proportions and softened philtrum; the full-body input locks build, exact clothing, dusty boots, restrained brick-red sakura bandana, and styling whenever worn.

Landscape 3:2 controlled two by three expression reference contact sheet, exactly six very consistent shoulder portraits of the same approved Tais. No change to any facial identity or outfit. Order left to right: neutral focused; quietly concentrating; curious; skeptical with restrained lifted brow; private faint smile; unguarded short natural laugh. Same slate anorak collar, brick red sakura bandana and twin braids. Consistent high-CRI studio background.
```

[Лист PNG](images/v3/tp11.png)

### TAIS-TP12 · Мимика: напряжение и уязвимость

Шесть выражений: раздражение, гнев, испуг, дискомфорт, печаль и облегчение.


```text
Premium ALIVE live-action model documentation. True photographic material and natural detail in skin, hair and woven cloth, soft directional neutral daylight, restrained contrast, light warm beige seamless studio background, consistent shadow and scale, mild honest wear rather than embossed textures, no text, grids, borders, logos or typography. Input portrait locks the same approved Tais face with original proportions and softened philtrum; the full-body input locks build, exact clothing, dusty boots, restrained brick-red sakura bandana, and styling whenever worn.

Landscape 3:2 controlled two by three expression reference contact sheet exactly six consistent shoulder portraits of same approved Tais. Order left to right: irritation; contained anger with tight jaw; quick genuine alarm; discomfort shown by transient brow tension; quiet sadness; relief as shoulders ease. Visibly distinct expressions, no tears or injury, lock face identity, slate anorak collar and brick red sakura bandana.
```

[Лист PNG](images/v3/tp12.png)

### TAIS-TP13 · Повседневная пластика

Четыре состояния в базовом костюме: стойка, сидя, поворот на оклик и шаг.


```text
Premium ALIVE live-action model documentation. True photographic material and natural detail in skin, hair and woven cloth, soft directional neutral daylight, restrained contrast, light warm beige seamless studio background, consistent shadow and scale, mild honest wear rather than embossed textures, no text, grids, borders, logos or typography. Input portrait locks the same approved Tais face with original proportions and softened philtrum; the full-body input locks build, exact clothing, dusty boots, restrained brick-red sakura bandana, and styling whenever worn.

Wide 3:2 four photo costume poses on same beige sweep in a single row, four full-body same Tais, entirely separate equally scaled silhouettes. Standing settled with body weight to one side, sitting on simple low cube, turning head and torso after a call, relaxed walking stride. Exact anorak, headscarf, cargo pants and dusty boots. No items in hands. Natural, observant, understated movement.
```

[Лист PNG](images/v3/tp13.png)

### TAIS-TP14 · Активная пластика

Четыре состояния в базовом костюме: бег, присед, движение рукой вверх и шаг на опору.


```text
Premium ALIVE live-action model documentation. True photographic material and natural detail in skin, hair and woven cloth, soft directional neutral daylight, restrained contrast, light warm beige seamless studio background, consistent shadow and scale, mild honest wear rather than embossed textures, no text, grids, borders, logos or typography. Input portrait locks the same approved Tais face with original proportions and softened philtrum; the full-body input locks build, exact clothing, dusty boots, restrained brick-red sakura bandana, and styling whenever worn.

Wide 3:2 four photo movement studies on the same light beige sweep in a single row, four distinct full-body exactly same Tais. A brief sprint with clear foot placement, a stable deep crouch, reaching high with one hand, stepping up onto a very low neutral platform. Believable natural balance and human body proportions, exact anorak shirt, headscarf, cargo pants and dusty boots, no added objects, no weapon.
```

[Лист PNG](images/v3/tp14.png)

### TAIS-TP15 · Костюмы TC01 и TC02

Слева — базовый анорак и карго, справа — тёмно-синяя пайта и тёмные длинные брюки для отдельного эпизода.


```text
Premium ALIVE live-action model documentation. True photographic materials and natural regional details, gentle neutral light, restrained contrast, light warm beige seamless studio background, consistent scale, real fabric wear, no artificial textures, no captions or logos.

Landscape studio wardrobe comparison, exactly four full-length views in one row, at equal scale. First and second are front and back of the exact approved TC01 anorak-and-cargos outfit of second input including brick-red tiny sakura bandana and dusty dark brown shoes. One taupe left chest flap pocket. Third and fourth show front and back of TC02 from BOTTOM ROW of third input: dark blue full-zip hoodie over charcoal T-shirt, long dark trousers, plain dark footwear, two braids, no bandana. Exact same Tais as first input, naturally young body, clean feet and head margins.
```

[Лист PNG](images/v3/tp15.png)

### TAIS-TP16 · Костюмы TC03 и TC04

Слева — найденная джинсовая рубашка. Справа — полосатый верх, спортивные брюки и распущенные волосы.


```text
Premium ALIVE live-action model documentation. True photographic materials and natural regional details, gentle neutral light, restrained contrast, light warm beige seamless studio background, consistent scale, real fabric wear, no artificial textures, no captions or logos.

Landscape studio wardrobe sheet, exactly four full-length views in one row at equal scale and floor line. Copy alternative outfits from THIRD INPUT. First two are front/back of TC03 worn plain denim shirt, dark trousers and shoes, dark braids and muted brick red sakura bandana from second input. Last two are front/back of TC04, narrow muted navy and cream striped long sleeve top, relaxed gray drawstring athletic trousers, dark shoes and dry loose hair. Exact same Tais as portrait input, naturally young body, clean feet and head margins.
```

[Лист PNG](images/v3/tp16.png)

### TAIS-TP17 · Крой и крупные детали

Крупные планы воротника со смещённой застёжкой, накладного кармана, усиления на правом рукаве и манжеты.


```text
Premium ALIVE live-action model documentation. True photographic material and natural detail in skin, hair and woven cloth, soft directional neutral daylight, restrained contrast, light warm beige seamless studio background, consistent shadow and scale, mild honest wear rather than embossed textures, no text, grids, borders, logos or typography. Input portrait locks the same approved Tais face with original proportions and softened philtrum; the full-body input locks build, exact clothing, dusty boots, restrained brick-red sakura bandana, and styling whenever worn.

Landscape garment construction photographic board of the exact dark slate navy anorak and greige cargos shown in the approved full figure. Overhead on very light beige textile backdrop. The assembled garment and trousers at left, right side several optical close-ups of its asymmetric high snap collar, exact single taupe flap pocket and dark snap, dusty slate-blue forearm fabric repair, and cuffs with hardware. Preserve existing pocket and color block construction; no extra military attachments or labelling.
```

[Лист PNG](images/v3/tp17.png)

### TAIS-TP18 · Рюкзак и бандана

Графитовый рюкзак и матовая красная хлопковая бандана. На развороте видны мелкие цветы сакуры и тонкая кайма.


```text
Premium ALIVE live-action model documentation. True photographic materials and natural regional details, gentle neutral light, restrained contrast, light warm beige seamless studio background, consistent scale, real fabric wear, no artificial textures, no captions or logos.

Edit first image as product photography. Preserve the two views of the graphite soft worn backpack on left. In right half, replace black bandana with red cotton matching second ref, full square flat lay above and folded below. Small sparse ivory and faded blush five-petaled sakura with notched petals and tiny buds, refined quiet Japanese textile spacing, subtle border and real cloth grain. No character or lettering.
```

[Лист PNG](images/v3/tp18.png)

### TAIS-TP23 · Магнитная доска — конструктив

Слева рабочий вид доски для сверки силуэта. Справа эскиз складывания. Согласование стойки и ручек требуется до моделирования.

Использован существующий лист магнитной доски из v2.

[Лист PNG](images/tp23.png)

### TAIS-TP19 · Лазерный меч · выключен и активен

Верх: луч убран в рукоять. Низ: рабочая полная длина. Ледяной оттенок, полупрозрачные световые слои и корпус из старой бронзы — предложение адаптации.

Использован существующий лист реквизита из v2.

[Лист PNG](images/tp19-v2.png)

### TAIS-TP22 · Маркировка костюма

Базовый анорак без номера, форменных нашивок и эмблем. Цветочный рисунок относится к бандане.

Использовать TP17 и подписать, что на анораке отсутствуют форменные нашивки, номер и эмблемы.

[Лист PNG](images/v3/tp22.png)

### TAIS-TP20 · Карта изменений

Последовательность костюмов TC01–TC04 для визуальной непрерывности. Сторона ранения плеча остаётся открытым решением.

Свести TP15 и TP16 в один лист, привязать TC01–TC04 к страницам романа. Отдельно отметить перевязку и заживление без выбора стороны.

[Лист PNG](images/v3/tp20.png)

## Контрольный портрет

```text
Conservative film-photography rebackground and wardrobe edit of image 1, exact Tais face and light natural skin detail, using image 2 for the current wardrobe only. Freeze facial geometry, expression, skin color, freckles, mole, eyes and texture. Do not synthesize extra texture. Preserve the small naturally shallow philtrum between her nose and lip, slightly feathering its shadow. Retain two simple brown braids and flyaways. Change only the bandana and upper garment to match image 2 (soft matte muted brick red cloth with small ivory and faded pink sakura flowers; navy canvas anorak with asymmetric stand collar and taupe facing). Light warm beige studio seamless background, soft clean daylight on face and fabric, very little color grading. Optical sharpness in eyes, focused hair strands and real fabric stitching without added grit. Real teen skin with soft transitions and fine random original pores. Absolutely no etched lines, thumbnail ridges, microcracks, embossed texture, orange-peel or pattern artifact on the skin. Full head and top of shoulders with natural studio headroom; vertical 2:3, no graphics.
```
