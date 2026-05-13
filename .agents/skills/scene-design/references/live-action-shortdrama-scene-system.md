# Live-Action Short Drama Scene System

Use this reference when designing scenes for English-language / overseas live-action vertical short dramas, especially when scenes must support recurring episodes, character blocking, power pressure, and AI video continuity.

## Goal

A short-drama scene is not a pretty background. It is a pressure container that lets the audience read who has power, who is trapped, what object matters, where the reveal will happen, and what changed after the beat.

Design scenes as:

```text
world rule + power layout + actor lane + narrative object + light cue + continuity state
```

## 1. Short Drama Scene Gate

Every scene packet should answer:

- Who controls entry, exit, seat, desk, bed, window, podium, or threshold?
- Who is blocked, exposed, cornered, elevated, watched, or forced to cross the room?
- What object can be handed, signed, revealed, denied, broken, or hidden?
- What can be read in the first 3 seconds in a 9:16 frame?
- What visible state must the next shot inherit?

Reject beautiful empty spaces. If the space cannot stage humiliation, rescue, betrayal, reveal, intimacy, threat, or reversal, it is not ready for short-drama production.

## 2. Power Space Architecture

For Western short dramas, power is often institutional. Give each location a power mechanism, not just luxury decor.

| Power domain | Scene type | Fixed anchors | Action lever |
| --- | --- | --- | --- |
| Corporate / CEO | executive office, boardroom | glass wall, long table, city window, chair hierarchy, nameplate | firing, vote, takeover, contract reveal |
| Inheritance / trust | family office, probate law office | trust binder shelves, sealed envelope, heavy desk, filing cabinet | signature, will reading, asset freeze |
| Legal / civic | courthouse hallway, DA press corridor, law office | county seal, microphone line, case folders, bench seating | subpoena, public charge, plea deal |
| Medical / insurance | hospital corridor, patient room, claims office | bed rail, monitors, cold lights, badge desk, red stamp | surgery delay, denial, diagnosis reveal |
| Education / class | admissions office, scholarship hallway, donor gala | trophy wall, crest, admissions files, donor board | admission, scholarship threat, public shame |
| Suburban / HOA | clean street, front lawn, clubhouse | mailbox, white fence, violation sign, trimmed lawn | fine, vote, eviction pressure |
| Church / charity | fellowship hall, charity office, sanctuary side room | bulletin board, donation table, cross, pledge cards | reputation exposure, grant denial |
| Gala / wedding | ballroom, stair landing, service corridor | chandeliers, champagne table, stage, side door | identity reveal, public rejection, secret recording |

## 3. Genre Scene Pack Builder

Build 5-8 recurring locations per project before writing episode prompts. Keep the scene set small enough for continuity.

### Genre Packs

| Genre | Core scenes |
| --- | --- |
| CEO revenge romance | executive office, boardroom, penthouse bedroom, gala hall, service corridor, parking garage, lawyer office, hospital room |
| Mafia forbidden love | nightclub back room, family dining room, warehouse office, church aisle, parking lot, safehouse bedroom, police interview room |
| Werewolf / Alpha romance | alpha office, medical lab, pack council room, moonlit forest edge, penthouse bedroom, gala / mating ceremony hall |
| Medical romance | hospital corridor, patient room, nurses station, operating prep room, boardroom, insurance claims office, rooftop break area |
| Legal thriller romance | law office, courthouse hallway, DA press corridor, interrogation room, family estate office, parking garage |
| Boarding school / scholarship revenge | admissions office, scholarship hallway, dorm room, donor gala, courtyard, headmaster office |
| Small-town scandal | diner, church charity hall, HOA street, sheriff office, zoning board room, clinic, parking lot |
| Royal / vampire / court fantasy | throne side hall, royal bedroom, council chamber, chapel, garden corridor, servant passage |

### Cast-To-Scene Rule

Every core character should have one scene they control and one scene where they lose control. If a scene belongs to nobody, it will not generate drama.

## 4. Vertical Blocking Lane

9:16 vertical short drama needs a readable lane system. Do not design only wide horizontal rooms.

### Layer Stack

| Layer | Purpose |
| --- | --- |
| Foreground pressure object | Door frame, desk edge, hospital rail, file stack, champagne tray, microphone stand. |
| Center actor lane | The vertical path where the main actor can enter, stop, turn, cross, or be blocked. |
| Background power anchor | City window, crest, board table, trophy wall, cross, county seal, bed monitor. |
| Threshold axis | Door, elevator, hallway, stair, curtain, or side entrance controlling arrival and exit. |
| Handoff zone | Desk corner, bed rail, podium, side table, folder tray, clipboard surface. |

### Blocking Prompts

Use these phrases when a scene must work in vertical video:

```text
vertical 9:16 blocking, central actor lane clear, foreground desk edge frames the lower third, door axis visible behind the actor, background power anchor stays readable
```

```text
two-character confrontation lane, dominant character near the desk and light source, trapped character near the doorway, document handoff zone between them
```

## 5. Scene State Ladder

A recurring location needs state changes. The same room should not reset clean after a major beat.

| State | Use | Visible rule |
| --- | --- | --- |
| `S0_normal_order` | Establish location before conflict. | Clean, functional, socially normal. |
| `S1_pressure_setup` | Tension begins. | Door half-open, folder on table, hard light, blocked path. |
| `S2_humiliation` | Public shame or coercion. | Actor trapped near edge, witnesses visible, object held by oppressor. |
| `S3_reveal` | Evidence or identity turns the scene. | Screen/file/envelope moves to center, light hits proof object. |
| `S4_aftermath` | Consequence remains. | Empty chair, spilled drink, scattered pages, dimmer light, changed door state. |
| `S5_power_reversal` | The formerly weak character controls space. | New center position, cleaner light, object ownership changed. |

### Scene State Record

```text
@Scene base identity =
S0_normal_order =
S1_pressure_setup =
S2_humiliation =
S3_reveal =
S4_aftermath =
S5_power_reversal =
Protected anchors =
Allowed changes =
Forbidden drift =
```

## 6. Scene Video Readiness Gate

A scene reference still is not automatically video-ready. Test core locations with 5-10 second motion auditions.

### Motion Tests

- Actor enters through the main door and stops in the center lane.
- Actor crosses from doorway to desk / bed / podium.
- One character blocks another at a threshold.
- A folder, envelope, phone, badge, ring, or clipboard moves through the handoff zone.
- Camera pushes in; background anchor remains stable.
- Two characters confront each other; power positions remain readable.
- The next shot inherits door state, object position, lighting, and surface traces.

### Labels

| Label | Meaning |
| --- | --- |
| `scene_video_ready` | Layout, light, anchors, and actor lane survive simple motion. |
| `needs_layout_lock` | Door, desk, bed, window, or table drifts. |
| `needs_light_lock` | Light direction or color changes too much. |
| `needs_prop_lock` | Narrative object disappears, mutates, or moves to the wrong zone. |
| `image_only` | Useful as mood / reference, not stable enough for video. |
| `reroll_scene` | Still image lacks action lane or story pressure. |

### Readiness Record

```text
scene_id =
base_scene_image =
motion_test =
layout_stability =
light_stability =
prop_stability =
actor_lane_read =
continuity_state =
readiness_label =
repair_instruction =
```

## 7. MJ Scene Reference Prompt Skeleton

Use this for scene stills:

```text
vertical live-action production design reference for an English-language US UK European short drama,
[scene type] designed for 9:16 actor blocking,
[power domain and narrative task],
[layout: entrance, center lane, power seat/desk/bed/podium, handoff zone],
[fixed anchors],
[narrative props / traces],
[light source and direction],
[color and material logic],
realistic streaming drama set, practical shootable space, no people, no text overlays,
clear floor path for actors, foreground / midground / background depth,
not a luxury hotel lobby unless specified
--ar 9:16 --v 8.1 --style raw --s 60 --q 1
```

## 8. Common Failure Ledger

| Failure | Cause | Repair |
| --- | --- | --- |
| Luxury-hotel drift | Overusing luxury, marble, chandelier, cinematic | Name exact power function: boardroom, claims office, admissions office; add work surfaces and institutional props. |
| Empty pretty room | Atmosphere without actor lane | Add entrance, threshold, center lane, handoff zone, and conflict position. |
| Horizontal-room drift | Wide architecture not vertical blocking | Specify 9:16 actor blocking, central lane, foreground pressure object, background anchor. |
| Door/window drift | Base layout not locked | Record door axis, window wall, desk orientation, and protected anchors. |
| Prop disappears | Prop treated as decoration | Make it a narrative object with owner, surface, and action. |
| Light resets | No scene state ledger | Track S0-S5 state, light source, door/window status, and traces. |
| Scene feels American-in-name only | No institutional details | Add county seal, HOA notice, trophy wall, admissions file, insurance stamp, hospital badge desk, zoning map. |

## Suggested Experiment Plan

Do not run 100 scenes first. Run eight core scene experiments:

1. CEO executive office
2. boardroom
3. luxury penthouse bedroom
4. hospital corridor / patient room
5. probate law office
6. private school admissions office
7. gala hall
8. suburban HOA street / church charity hall

For each: one MJ still, one vertical blocking still, one 5-10 second motion test, then label `scene_video_ready` or a repair tag.
