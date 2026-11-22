# ALIVE · Лицо по зонам

## Утверждённые принципы

- Лоб: тонкий нерегулярный микрорельеф и небольшие цветовые различия.
- Веки: тонкая кожа, деликатные складки по возрасту, влажный край нижнего века, отдельные ресницы.
- Нос и внутренние участки щек: мелкие нерегулярные поры; легкий блеск носа, немного красноты у ноздрей.
- Наружные щеки и виски: более тонкая фактура; щеки преимущественно матовые, едва заметный пушок в боковом свете.
- Под глазами: мягкий более прохладный оттенок; без нарочитой усталости и старения.
- Губы: тонкие вертикальные складки, мягкий неровный край, сдержанный естественный цвет.
- Брови и волосы: естественные направления роста, разная плотность и мелкие пряди.
- Глаза: различимая радужка, согласованные зрачки и блики от источников сцены, слегка кремовые белки.
- Веснушки и мелкие отметины сохраняют индивидуальность, не превращаются в равномерный шум.

Возраст, тон кожи и индивидуальные особенности задаются для конкретного героя. Не переносить мужскую щетину из промпта Федора на других персонажей. Не добавлять подросткам взрослые морщины или крупные поры ради «реализма».

## Переиспользуемый блок ALIVE

```text
Create a new photographic exposure. Prioritize character identity, believable anatomy and exchanged eyelines. Frame faces large enough to resolve natural detail. Resolve both faces within a coherent focus region; let the background fall out of focus. Use anatomically regional skin: finer forehead and temple microrelief, delicate eyelid skin, small irregular pores beside the nose and inner cheeks, mostly matte outer cheeks with subtle peach fuzz, restrained nasal sheen, fine vertical lip creases, growth-directed eyebrow hairs, believable irises and coherent catchlights. Preserve age and individual skin tone. Shape faces with motivated directional light, weak scene-derived bounce and controlled shadow-side fill; separate background planes with selective practical sources. Natural highlight rolloff and clean tonal transitions. No uniform pore pattern, grain overlay, wax skin, face-restoration smoothing, sharpening halos or equal microdetail across the frame.
```

## Федор · типаж 009

Входные изображения в порядке подачи. [Премиальный портрет 009](../images/fp01.png) и [контрольный анфас](../images/fp02.png). Первый задаёт черты и цвет. Второй помогает сверять пропорции анфаса.

```text
Reference 1 is the approved premium three-quarter portrait of the original fictional character Fedor Sheremetev, ALIVE type 009. Reference 2 is his straight frontal control. Keep the exact identity of image 1 and use image 2 for frontal geometry and feature placement. Preserve his late-teen appearance, eye spacing, muted olive gray-green irises, low naturally straight dark brows, exact observed nasal dorsum, tip and nostril shape, mouth width, natural lip contours, asymmetry, jaw, faint freckles and occasional short stubble. Ash-brown grown-out hair with subtly lighter strands. Reference 1 settles any ambiguity about color or features.

Forehead and temples: fine irregular microrelief with subtle shifts in skin tone; fine downy hairs near the temple. Eyelids: delicate skin, age-appropriate folds and a subtly moist lower lid margin, individual lashes. Under-eye: slightly cooler tone and soft real transition, preserve the original shallow shape. Eyes: olive gray-green radially textured irises, optically aligned pupils, translucent limbal color, natural lightly cream sclerae and soft coherent catchlights. Brows: individual growth-directed hairs with uneven density and minute gaps, exact original height and curve. Nose and inner cheeks: small irregular pores, soft localized sheen on bridge and tip, faint redness at nostril edge; keep the original bridge, tip and alar outline. Outer cheeks: largely matte with fine soft peach fuzz and small nonuniform color variation. Lips: fine shallow vertical lines, soft uneven outline, natural muted color, neutral closed mouth; preserve the precise Cupid's bow, relative lip volume and natural corners. Preserve the actual light freckles and the sparse growth direction of fine facial stubble.

Real live-action casting photography, neutral broad directional studio daylight from upper camera-left, weak neutral bounce, restrained shadow-side fill, clean very light warm beige studio background, photographic optics and believable sharpness, neutral accurate skin color and clean highlight rolloff. Keep the true local scale of each texture. Preserve age and ordinary asymmetry. Soft skin outside the focal region. Avoid repeated procedural pores, grit, synthetic cracks, beauty retouch, face-restoration smoothing, sharpening halos, harsh HDR, stylization, CGI, illustrations, text, watermarks and logos.
```

Блок использован для крупного портрета, макрокадров и листа ракурсов. [Макро правого глаза](../images/fp23.png) дополнительно опирается на [лист с обоими глазами](../images/fp18.png). Полные задания с кадрированием находятся в [пакете промптов Федора](../FEDOR_Prompt_Pack.md). Модель OpenAI Image API `gpt-image-2.5-sunburst`, качество `high`.
