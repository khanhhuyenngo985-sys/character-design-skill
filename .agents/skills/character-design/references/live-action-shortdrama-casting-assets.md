# Live-Action Short Drama Casting Asset Gate

Use this reference when designing MJ / image-model character assets for overseas short dramas, especially English-language US / UK / European live-action vertical dramas.

## Goal

The output is a casting and wardrobe-fitting asset, not a poster, concept painting, fashion editorial, or isolated beauty portrait. It must help production answer: who can play this role, what social power do they carry, what can they do on screen, and what anchors must remain stable in later AI video shots.

## Ensemble First

Before writing individual prompts, check the library or batch as a whole:

- Narrative functions: protagonists, love interests, rivals, family power, antagonists, professional allies, youth, community, genre hooks, relationship-conflict roles, institutional-power roles.
- Gender and age: include young adults, middle age, seniors, and children when the story world needs them.
- Western-market multicultural casting: White / European diaspora, Black / African diaspora, Latino / Hispanic, Mixed-race, South Asian diaspora, MENA / Arab diaspora, Indigenous / Pacific Islander, and Asian diaspora where appropriate.
- Attractiveness tier: leads may need cover-level beauty; supporting roles should stay ordinary, credible, and castable.
- Power architecture: for Western short drama, use institutions as power engines, not only billionaire-family hierarchy.

## Bone / Face Structure Layer

For live-action short-drama assets, add a light but explicit bone-structure layer. Do not use bone structure as a universal beauty formula; use it to stabilize identity, age, ethnicity read, and ensemble contrast.

Lock 3-5 visible traits per important role:

- Face envelope: oval, long narrow, square, heart-shaped, round, tapered, broad, compact.
- Cheek / jaw: high cheekbones, rounded cheeks, soft jaw, square jaw, narrow jaw, strong chin, gentle chin.
- Brow / eye structure: deep-set eyes, hooded eyes, wide-set eyes, almond eyes, heavy brow, soft brow.
- Nose / mouth: aquiline nose, straight bridge, broad nose, full lips, thin lips, soft mouth, stern mouth.
- Skin / age texture: freckles, fine lines, sun-browned skin, under-eye fatigue, natural pores, silver stubble.
- Secondary anchors: hairline, neck line, hand shape, mole, scar, glasses, beard shape.

For groups, vary at least two of face envelope, cheek/jaw logic, eye geometry, skin texture, hairline, or posture so cast members do not merge. When correcting ethnicity drift, strengthen bone and skin anchors instead of only repeating the ethnicity label.

Example:

```text
warm tan skin, rounded Latina cheekbones, dark steady eyes, compact oval face, straight dark hair in a side part, natural pores and light under-eye fatigue
```

## Power Architecture Layer

For overseas live-action drama, convert abstract power into visible institutional levers:

| Domain | Useful roles | Visible power levers |
| --- | --- | --- |
| Inheritance / wealth | family trustee, probate lawyer, executor | trust binder, will envelope, distribution schedule, certification |
| Legal / political | district attorney, judge, campaign aide | subpoena folder, plea deal papers, campaign pin, press note card |
| Medical / insurance | claims director, hospital board chair | denial stamp, pre-authorization badge, ethics report, board badge |
| Education / class | admissions director, donor parent, school-board member | admissions clipboard, scholarship file, donor check folder |
| Civic / suburban | HOA president, zoning board chair | violation notice, fine sheet, permit packet, zoning map tube |
| Church / charity | foundation director, charity board member | grant folder, donor pledge cards, church bulletin |

Each power role needs:

- Identity buff: who the world recognizes them as.
- Permissioned action: what this role can legally or socially do.
- Power limit: what the role cannot solve or where hypocrisy appears.
- Visible proof: object, badge, folder, signature tool, posture, or hand habit.

## Prompt Field Order For MJ

Use one compact English sentence with comma-separated fields and inline MJ parameters:

```text
full-length head-to-toe live-action actor casting photo for an English-language US UK European vertical short drama,
Western-market multicultural casting pool,
one single actor centered,
camera pulled back far enough to show shoes and floor,
plain TV casting-room photography,
realistic wardrobe fitting reference,
casting type: [region / ethnicity / class / profession],
[age + role identity + narrative action],
[body shape + bone/face structure + hair anchors],
[practical role-specific wardrobe],
[signature prop or visible power lever],
front view,
calm readable standing pose,
entire body inside frame with margin above the head and below the shoes,
feet fully visible on the floor,
clean neutral gray casting studio backdrop,
soft realistic studio light,
natural skin texture,
ordinary believable actor face,
real body proportions,
contemporary streaming drama realism,
attractive and powerful but not runway editorial
--ar 9:16 --v 8.1 --style raw --s 60-75 --q 1
```

## QC Gate

Approve only when most of these are true:

- Full body is visible, including shoes and floor.
- Face reads as Western-market live-action casting for the requested ethnicity / age.
- Bone / face anchors are specific enough to prevent generic beauty or ethnicity drift.
- Wardrobe is practical and shootable, not fantasy design or runway styling.
- Role can be read from silhouette, clothing, posture, and prop.
- Power lever is visible and story-relevant.
- Body proportions, hands, and feet are believable enough for a reference asset.
- The character feels like a real short-drama actor, not a luxury campaign model.

Reject or reroll when:

- Asian-face drift appears for a non-Asian Western role.
- The face becomes generic influencer beauty with no stable face envelope, cheek/jaw logic, or age texture.
- Body is cropped, shoes are missing, or the image becomes a portrait.
- The role becomes concept art, superhero, game character, or fashion editorial.
- Age, ethnicity, or gender misses the design target.
- Power prop is missing or unreadable.
- Hands, feet, or anatomy collapse.

## Batch Workflow

- Submit 8-10 prompts at a time; do not flood 100 roles in one pass.
- Download all variants and make a contact sheet before selecting.
- Usually keep two approved images per role for casting flexibility.
- Record prompt_id, role name, MJ job URL, selected image index, selection reason, issue notes, local path, batch, and status in a manifest.
- Keep internal prompt / QC / manifest files in the workspace; final human-facing delivery can be image-only when requested.
- For final delivery, use a single zip and Chinese filenames when the user asks for production handoff.

## Common Filename Pattern

```text
[编号]_[中文角色名]_[性别]_[成品序号].[ext]
```

Example:

```text
111_家族信托管理人_女_成品01.png
```
