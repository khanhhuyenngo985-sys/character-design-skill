# Short Drama Character Production System

Use this reference when a character asset library must become a playable short-drama cast system, not just a set of good-looking stills. It extends the live-action casting asset gate with four production modules: relationship matrix, genre cast pack, wardrobe state ladder, and video readiness gate.

## 1. Relationship Matrix

A short-drama character is only production-ready when their pressure lines are visible. Record relationships as actionable edges, not vague biographies.

### Edge Fields

| Field | Purpose |
| --- | --- |
| `source_character` | Who acts or holds pressure. |
| `target_character` | Who receives pressure. |
| `public_relation` | What society sees: boss, fiancee, mother-in-law, doctor, trustee. |
| `private_relation` | Hidden truth: ex-lover, secret heir, blackmailer, protector, betrayer. |
| `power_over` | What source can take, block, expose, approve, deny, or delay. |
| `protects` | Who or what source protects, if any. |
| `betrays` | Who source can betray and how. |
| `secret_about` | The secret object: pregnancy, inheritance, identity, medical record, affair, crime. |
| `romantic_pressure` | Desire, jealousy, debt, forbidden attraction, rejection, arranged bond. |
| `blocking_proof` | How the relationship appears in staging: distance, eyeline, document handoff, doorway block. |
| `scene_trigger` | What action activates the edge: vote, signature, gala reveal, custody hearing, boardroom meeting. |

### Edge Template

```text
@source -> @target:
public_relation =
private_relation =
power_over =
protects =
betrays =
secret_about =
romantic_pressure =
blocking_proof =
scene_trigger =
```

### Relationship QC

- Can the edge generate a 3-second hook?
- Can it create a humiliation, rescue, betrayal, reveal, or reversal scene?
- Is the power visible through prop, document, room access, touch, distance, or gaze?
- Does the relationship create a future episode button, not only backstory?

## 2. Genre Cast Pack Builder

Build 8-12 role packs for each short-drama genre. Do not start a project by browsing 120 faces; start by filling genre slots.

### Universal 10-Slot Pack

| Slot | Function |
| --- | --- |
| `lead_entry` | Audience-entry protagonist; unfairly treated but visually memorable. |
| `primary_desire` | Main love interest or desire object. |
| `shadow_rival` | Romantic, status, or inheritance rival. |
| `family_power` | Parent, matriarch, patriarch, trustee, executor, or family gatekeeper. |
| `institutional_gatekeeper` | Legal, medical, education, civic, church, or corporate authority. |
| `intimate_betrayer` | Friend, secretary, sibling, assistant, ex, or fake ally. |
| `professional_ally` | Doctor, lawyer, investigator, hacker, journalist, producer. |
| `community_witness` | Neighbor, diner owner, nurse, teacher, pastor, driver, receptionist. |
| `youth_or_elder_stake` | Child, teen, grandmother, elder patient, scholarship student. |
| `genre_hook_role` | Werewolf alpha, mafia heir, vampire, royal guard, celebrity, cult leader. |

### Genre-Specific Slot Bias

| Genre | Must-have slots |
| --- | --- |
| CEO revenge romance | hidden/undervalued heroine, cold CEO, fiancee rival, board investor, family trustee, secretary, lawyer, gossip witness. |
| Mafia forbidden love | mafia heir, protected heroine, rival fiancee, consigliere/lawyer, family matriarch, detective, nightclub/community witness. |
| Werewolf / Alpha romance | rejected mate, alpha, pack rival, healer/doctor, elder, human institutional threat, vulnerable child/heir. |
| Medical romance | nurse/surgeon heroine, doctor male lead, hospital board chair, insurance claims gatekeeper, malpractice witness, patient family. |
| Legal thriller romance | lawyer heroine, DA/judge antagonist, client, investigator, media witness, family secret holder. |
| Boarding school / scholarship revenge | scholarship lead, admissions director, donor parent, fake friend, rich rival, teacher ally, school-board power. |
| Small-town scandal | returning heroine, sheriff/detective, HOA president, church charity director, diner owner, ex, zoning board. |
| Royal / vampire / court fantasy | hidden royal/bride, prince/lord, bodyguard, court matriarch, priest/advisor, rival noble, servant witness. |

### Cast Pack Output

```text
Genre =
Premise promise =
Core hook =
Cast pack:
1. @role = function + asset_id / prompt_id + why this face works
...
Missing slots =
Reroll needs =
```

## 3. Wardrobe State Ladder

A recurring live-action short-drama role needs stateful wardrobe, not one fixed outfit. Record wardrobe as story progression.

### Standard Ladder

| State | Use | Visual rule |
| --- | --- | --- |
| `W0_public_mask` | Normal identity before pressure. | Controlled, socially legible, not too dramatic. |
| `W1_humiliation_workwear` | Low-status or exposed state. | Practical clothing, stains, tired texture, weaker posture. |
| `W2_pressure_damage` | After betrayal / injury / public shame. | Wrinkles, loosened collar, smudged makeup, missing prop, tense body. |
| `W3_reveal_event` | Gala, wedding, boardroom, court, press reveal. | Strong silhouette, one signature color, identity prop visible. |
| `W4_intimate_recovery` | Private healing / romance / confession. | Softer fabric, lower contrast, less armor, vulnerable posture. |
| `W5_final_power` | Revenge, restored status, victory, blackening. | Sharper tailoring, cleaner hair, upgraded material, controlled gaze. |

### Wardrobe Card

```text
@Character wardrobe ladder:
W0_public_mask =
W1_humiliation_workwear =
W2_pressure_damage =
W3_reveal_event =
W4_intimate_recovery =
W5_final_power =
Protected anchors across all states =
Forbidden wardrobe drift =
```

### Wardrobe QC

- Can the audience read the arc without dialogue?
- Does each state preserve the face, hair, body, and signature prop?
- Does the outfit remain shootable, not editorial?
- Is the reveal outfit different enough to produce a short-drama dopamine hit?

## 4. Video Readiness Gate

Approved stills are not automatically video-ready. Core characters need a motion audition before being trusted across episodes.

### Motion Audition Beats

Use 5-10 seconds, one action per test:

- Walk into a room and stop on a mark.
- Look down at a document, then look up with a controlled reaction.
- Hand over or receive a folder, envelope, badge, ring, phone, or glass.
- Turn from public smile to private threat.
- Cross a doorway to block another character.
- Sit, stand, or lean without losing body proportions.
- Hold eye contact while another character approaches.

### Readiness Labels

| Label | Meaning |
| --- | --- |
| `video_ready` | Face, body, costume, and prop survive simple motion. |
| `needs_face_lock` | Still is good, but motion changes face or age. |
| `needs_prop_lock` | Prop disappears, mutates, or changes hand. |
| `image_only` | Useful for casting board, not reliable for generated video. |
| `reroll_priority` | Still itself is weak enough to reroll before video. |

### Video Readiness Record

```text
asset_id =
test_prompt =
motion_result =
face_stability =
body_stability =
prop_stability =
wardrobe_stability =
readiness_label =
repair_instruction =
```

### Video QC

- Does the first frame still match the approved asset?
- Does the face age, ethnicity, or attractiveness tier drift?
- Do hands keep ownership of the document / prop?
- Is the costume state inherited from the still?
- Can the shot be cut into a 60-90 second vertical episode without confusing the audience?

## Suggested Production Order

```text
Character library
→ Genre cast pack
→ Relationship matrix
→ Wardrobe state ladder
→ Still reroll if needed
→ 5-10s motion audition
→ Video readiness label
→ Episode prompt package
```

Do not skip from still image directly to multi-episode video production for core characters. A still is a promise; the motion audition proves whether the promise can survive.
