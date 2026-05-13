# Bone And Face Structure Layer / 骨相与面部锚点层

Use when the character will appear in portraits, close-ups, character sheets, beauty/fashion frames, live-action style images, recurring AI-video segments, or when face drift is likely.

Core principle: bone structure is an identity anchor, not a beauty template. It should preserve who the character is while allowing expression, age, fatigue, damage, makeup, lighting, and style to change.

## Output Fields

```text
Bone structure / 骨相锚点:
Face envelope / 脸型包络:
Eye structure / 眼部结构:
Nose / lips anchor:
Skin / texture anchor:
Hairline / hair mass:
Neck / hand secondary anchors:
Facial performance range:
Facial forbidden drift:
```

## Anatomy-To-Prompt Map

| Layer | What to define | Good anchors |
| --- | --- | --- |
| Cranial shape / 颅顶 | skull height, crown roundness, head-to-face ratio | high rounded crown, low flat crown, narrow skull, broad skull |
| Face envelope / 脸型包络 | overall face shape and jaw path | soft oval, square jaw, long narrow face, round childlike face, tapered chin |
| Cheek / jaw / 颧颌 | cheekbone height, fullness, jaw tension | high cheekbones, softly full cheeks, firm angular jaw, rounded jawline |
| Brow / eye / 眉眼 | brow weight, eye shape, eye corner, lower-eye form | straight brows, peach-blossom eyes, deep-set eyes, lifted outer corners, full lower-eye softness |
| Nose / lips | bridge, tip, nostril read, lip volume, cupid's bow, mouth corner | refined straight bridge, upturned tip, full cupid's bow, thin compressed lips |
| Skin / texture | age, translucency, pores, undertone, finish | translucent warm skin, matte weathered skin, freckled texture, rough sunburned surface |
| Hairline / hair mass | hairline shape, volume, parting, sideburn/temple behavior | widow's peak, clean hairline, heavy hair mass framing face, loose temple strands |
| Secondary anchors | neck, collarbone, hands, nails, scars, moles | long neck, visible collarbone, slender fingers, scar across brow, mole under eye |

## Prompt Compression

Keep the production prompt compact. Pick 3-5 face anchors, then list forbidden drift.

```text
Face anchors: [cranial/face envelope], [cheek/jaw], [eye structure], [nose/lips], [hairline/hair mass].
Secondary anchors: [neck/hand/mark if important].
Avoid: [wrong face shape], [wrong eye style], [wrong age/makeup], [plastic skin], [ethnicity/style drift if relevant].
```

## Example: Soft Eastern Portrait Anchor

```text
Bone structure: high rounded cranial crown, hair volume wrapping the face, soft oval face envelope, gentle curved jawline, slightly full cheekbones.
Eye structure: peach-blossom eyes, subtly lifted outer corners, full lower-eye softness, direct relaxed gaze.
Nose / lips: refined nose bridge, slightly upturned nose tip, full cupid's bow, soft moist lips, faint smile tension.
Skin / texture: translucent warm skin, soft pink undertone, fine natural texture, luminous but not plastic.
Hair / secondary anchors: black loose hair with slight waves, stray temple strands, slender neck, visible collarbone, long refined fingers.
Facial forbidden drift: avoid sharp V-line face, oversized anime eyes, heavy contour makeup, Westernized high-contrast bone structure, waxy plastic skin.
```

## Variation Rules

- Do not reuse one attractive face for every role. Give each important character a different face envelope, cheek/jaw logic, eye structure, and hair mass.
- Match bone structure to narrative function: status, labor, training, illness, age, temperament, class, and world rules should leave visible traces.
- Separate permanent identity from temporary state: makeup, sweat, tears, dust, bruises, lighting, expression, and fatigue may change.
- Avoid piling all beauty terms into one face. Too many glamour anchors create generic model-beauty drift.
- For groups, contrast at least two of: face envelope, eye geometry, jaw path, hairline, skin texture, posture.
