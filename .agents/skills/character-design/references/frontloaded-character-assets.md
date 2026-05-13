# Frontloaded Character Assets / 重在前期角色资产

Source distilled from `/Users/baimengke/Documents/【内门】重在前期角色设计_逐字稿.docx`.

Use this when a character, cast, or subject library must survive multi-reference image/video production. The point is not to make a pretty character. The point is to make a memorable, stable, performable asset that gives the model better reference material than prompt words alone can provide.

## Core Thesis

Multi-reference workflow is not the same as merely using a multi-reference model. In a real multi-reference workflow, the root of the output is the prepared asset: character, scene, preset, sound, and style references. A strong character reference is already a prompt.

Therefore:

- Do front work before video prompting.
- Design the cast before polishing one person.
- Make the character unforgettable, not only likable.
- Translate function, buff, posture, costume, color, and prop into visible reference material.
- Test the design in motion before trusting it.

## Six-Part Gate

### 1. Ensemble First / 群像先行

Never design an important character only as an isolated beautiful portrait. Start with a cast image or subject-library board.

Ask for:

- different ages, genders, heights, weights, body ratios
- different posture families: hunched, upright, open, closed, tense, loose
- different color zones and material zones
- roles that oppose, support, tempt, test, or mirror one another
- posture matching personality, not mannequin standing

The value of a character depends on difference from the rest of the cast, not on individual perfection.

Fail state: two characters share face type, hair, height, palette, costume category, and posture. If they merge in video, the design failed before prompting.

### 2. Archetype Mix / 原型混搭

Assign narrative functions before visual polish. A modern memorable role often mixes multiple functions:

- mentor + lover + killer
- outsider + detective + antihero
- mascot + guide + specialist
- hardbody + strategist
- trickster + emotional truth teller

The archetype mix decides what the character is allowed to do, what props belong to them, how they move, and what visual contradiction makes them memorable.

Convert the mix into visible language:

| Function signal | Visual translation |
| --- | --- |
| Mentor / guide | controlled gaze, measured posture, tool of instruction |
| Killer / danger | sharper silhouette, restricted movement, hard material |
| Lover / intimacy | softened line, proximity posture, warmer gesture |
| Detective / truth seeker | focused eyes, note/tool, scanning habit |
| Outsider | palette or costume separated from the world |
| Mascot / support | compact body, readable prop, helper behavior |

### 3. Posture Is Prompt / 姿态就是提示词

A static character card is not enough. Posture carries personality, history, and future motion. The model will infer voice, gait, action style, and acting from body shape, face, and posture.

Design at least these states for major characters:

- default posture: how the character stands when not performing
- pressure posture: what changes under threat
- relationship posture: how they lean toward or away from someone
- action posture: the body shape used in their specialty
- failure posture: how the flaw appears in the body
- arc posture: how they change after growth, injury, love, power, loss, or corruption

Avoid all reference images using the same front-facing mannequin pose. If posture does not express intention, the video prompt must work too hard.

### 4. Color Leaves A Residue / 色彩要留残像

Do not rely only on generic color psychology. Use color to make memory.

Useful strategies:

- extreme saturation: one color refuses to be ignored
- extreme contrast: black/white, warm/cold, red/green, soft/hard
- environmental isolation: one character color separates from the scene palette
- color arc: the same costume or prop changes meaning across the story

Example pattern: a yellow jacket can begin as protection, later become the last human trace around a machine-like body. The color anchor then becomes story, not decoration.

### 5. Costume And Prop Carry Story / 服化道承载叙事

Costume and prop must do more than signal genre.

Check whether they:

- change silhouette at video distance
- reveal identity, culture, rank, profession, faction, oath, wound, or obsession
- create action: grip, repair, strike, write, scan, hide, protect, betray
- carry the character arc
- separate the character from nearby roles
- survive as a 3-5 word prompt anchor

After designing costumes, run an ensemble costume test: put the cast together chatting, walking, fighting, or waiting. Check whether each person is still readable and whether the costume supports relationship and action.

### 6. Motion Audition / 动态试镜

Do not trust a still card until it has moved.

Minimum audition:

- one 10s or 15s clip with the character alone
- one multi-character clip with blocking
- one specialty action using their buff or toolchain
- one failure/reaction beat

Pass if:

- the character remains recognizable in motion
- posture and gait match the identity
- the buff produces visible action, objects, or authority
- face, costume, prop, and palette do not drift
- nearby characters do not merge
- the model's acting feels like the reference image, not a generic performer

If the audition fails, fix the asset before adding prompt adjectives.

## Frontloaded Output Block

Use this compact block before final prompt handoff:

```text
Frontloaded character asset gate:
- Ensemble contrast: [who this character differs from, and how]
- Archetype mix: [2-4 functions in tension]
- Identity buff: [world-recognized role + specialty + permissioned actions]
- Posture states: [default / pressure / relationship / action / failure]
- Color residue: [main memory color + contrast/isolation/arc]
- Costume-prop story: [silhouette + identity + action + arc]
- Motion audition: [solo / multi-character / specialty / failure result]
- Fix before prompting: [asset problems that must be solved first]
```

## Common Repairs

- Too pretty: add contradiction, function, posture, and a story-bearing prop.
- Too similar to another role: change one major axis: body, color, material, posture, or prop.
- Buff is invisible: add visual proof, hand habit, tool wear, marks, rank symbols, or carried objects.
- Video acting is generic: make posture states stronger and run another audition.
- Model loses identity: reduce moving characters, strengthen anchors, or redesign the reference asset.
