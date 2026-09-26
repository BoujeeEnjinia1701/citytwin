# CityTwin

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Smart Cities · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** $750 USD for the kiosk · **Difficulty:** 3 of 5

A city dashboard built on TwinKit that brings the smart city nodes together on a map and in a public kiosk, with open data export and privacy rules built in.

![CityTwin concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement CTW-DWG-001 (PDF)](cad/drawings/CTW-DWG-001.pdf) · [Calculations CTW-CAL-001](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

One open, public view of street data builds trust and lets residents and planners use the same evidence. CityTwin takes the counts and levels that the lab's smart city nodes already send, checks each record against a strict schema, applies the same privacy rules to everything it publishes, and shows the result on one map, in hourly open data files and on a kiosk in the street. The kiosk tells a passer-by what is measured nearby, who is responsible and how long data is kept, next to the current values.

It is open and garage-buildable because trust depends on being able to check the system. The software runs on one small TwinKit gateway that a city, a university or a neighborhood group can own outright, and the kiosk is a steel post, a folded aluminum head, a color e-paper screen and an electrical cabinet: parts a local fabricator and electrician can supply and inspect.

## Burning platform

Cities are growing and are adding sensors to manage that growth, but residents often do not trust how the data is used. About 55 % of the world's people live in urban areas, projected to reach 68 % by 2050 ([UN DESA, 2018](https://www.un.org/development/desa/en/news/population/2018-revision-of-world-urbanization-prospects.html)). In a 2019 survey, 66 % of U.S. adults said the risks of government data collection about them outweigh the benefits, and 84 % said they have very little or no control over it ([Pew Research Center](https://www.pewresearch.org/internet/2019/11/15/americans-and-privacy-concerned-confused-and-feeling-lack-of-control-over-their-personal-information/)).

Where the rules are unclear, projects stall. In Toronto, the former Ontario privacy commissioner resigned from the Sidewalk Labs project because de-identification at the point of collection could not be guaranteed ([CBC News](https://www.cbc.ca/news/canada/toronto/ann-cavoukian-sidewalk-data-privacy-1.4872223)), and the project was withdrawn in May 2020 ([Sidewalk Labs](https://medium.com/sidewalk-talk/why-were-no-longer-pursuing-the-quayside-project-and-what-s-next-for-sidewalk-labs-9a61de3fee3a)). Street data that is aggregated at the source, published openly and shown where it is collected is a practical answer.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Municipal government | One map of counts, curb use, air, noise, heat and flooding for planning, with a public kiosk and open data portal feed |
| Transport and road safety | Before and after evidence for street changes, combining CurbCount, CrossSafe, LoadZone and PotholeLog data |
| Environmental health | Neighborhood air, noise and heat maps for health departments and community groups |
| Water and drainage | FloodGauge levels next to rainfall and street data for drainage crews |
| Universities and schools | Open, documented street data and a kiosk for teaching and research |
| Business districts and transit hubs | Kiosks at plazas and stations that show local conditions and explain the sensors |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| European Union | High-value datasets, including earth observation and environment and mobility, must be published in machine-readable formats through APIs and bulk download under [Implementing Regulation (EU) 2023/138](https://eur-lex.europa.eu/eli/reg_impl/2023/138/oj/eng), applying from June 2024 |
| Canada | The Toronto Quayside project showed how data governance can decide a smart city project ([CBC News](https://www.cbc.ca/news/canada/toronto/ann-cavoukian-sidewalk-data-privacy-1.4872223)) |
| Taiwan | [Civil IoT Taiwan](https://ci.taiwan.gov.tw/) publishes air quality, water and disaster sensor data openly; CityTwin offers a small, open counterpart for a single city or district |
| Sub-Saharan Africa | [AirQo](https://airqo.net/) runs more than 400 low-cost air sensors in 14 African countries, showing demand for open community sensing where city budgets are small |
| India and Nigeria | With China, they account for 35 % of projected urban growth to 2050 ([UN DESA](https://www.un.org/development/desa/en/news/population/2018-revision-of-world-urbanization-prospects.html)); fast-growing cities need low-cost, open street data |
| Brazil | The general data protection law applies to public bodies as well as companies ([Lei 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)), which favors systems that publish only aggregates |

## What sparked the idea

The starting point was Amsterdam's sensor register. From December 2021 the city required companies, research institutions and government bodies to report sensors they place in public space, new or existing and mobile ones included, on a public online map that shows the type of sensor, its owner and whether it processes personal data, with June 1, 2022 as the deadline before the city could remove unregistered sensors at the owner's expense ([Cities Today](https://cities-today.com/amsterdam-introduces-mandatory-register-for-sensors/); [Sensorenregister Amsterdam](https://sensorenregister.amsterdam.nl/)). The register answers "who owns this and what does it collect?" on a website. CityTwin carries the same answer to the pavement: a notice plate with a QR code to the sensor register, the live counts and levels beside it, and open data files behind it, on hardware a city or neighborhood group can own.

## Problem

City data sits in separate vendor dashboards, and residents rarely see the data collected on their streets.

## Concept

A city dashboard built on TwinKit that brings the smart city nodes together on a map and in a public kiosk, with open data export and privacy rules built in.

CityTwin software on a TwinKit gateway receives counts and levels from the nine smart city node types, rejects anything outside each node's schema, stores the rest, suppresses small counts and movement traces, and publishes hourly CSV and GeoJSON files one way to a public host. The kiosk is a steel post with a 13.3 in color e-paper screen at about 1.46 m, three buttons at about 1.12 m, a data notice plate with a QR code, a lit sun hood, and a locked cabinet holding the mains protection, a 12 V supply and the gateway.

TRL 3 calculations ([CTW-CAL-001](docs/04-calcs/01-sizing.md)): a 46-node reference neighborhood sends 5,616 uplinks a day and loses 0.61 %, well within one gateway; data on the kiosk is at most 25.9 min old; kiosk and gateway draw 9.2 W from the mains with the hood light dimmed; the kiosk weighs about 60 kg with its outdoor sun shield and its post is stressed to 26.9 MPa in a 35 m/s gust with a 1.5 factor. A button's LED ring answers a press at once and the new layer follows in 19.8 s, within the 25 s target; the pilot kiosk costs $739.00 against the $750 budget; and a sheltered pilot site at 0 to 35 °C air leaves about 5 K of margin for the screen and the backup pack. Not met: backup time with an aged, cold pack (1.63 h against 2 h, until TwinKit fits a pack of at least 1.84 Ah) and the street climate range, so the pilot kiosk stands on a sheltered site and any outdoor site gets a cabinet sun shield and a shaded screen. Ingest of every node type is at risk until PotholeLog, DockHub and CrossSafe agree their interfaces. See the [requirements](docs/03-requirements.md) and the decision records [CTW-DDR-001](docs/decisions/0001-trl2-review-decisions.md) and [CTW-DDR-002](docs/decisions/0002-recommendations-accepted.md).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

1. Base plate and anchors
2. 100 mm square steel post, 1.75 m
3. Folded aluminum display head
4. Polycarbonate front window
5. 13.3 in color e-paper display (E Ink Spectra 6, 1600 x 1200 px)
6. Kiosk controller (Raspberry Pi Zero 2 W class, wired to the gateway)
7. Three stainless push buttons with LED rings
8. Data notice plate with QR code to the sensor register
9. Sun and rain hood with night light (dimmed to about 0.3 W)
10. Lockable services cabinet
11. Mains protection (30 mA RCBO and surge protector)
12. 12 V DIN power supply
13. TwinKit gateway with LiFePO4 backup, on its own DIN rail (costed in TwinKit)
14. LoRaWAN antenna on the post top (TwinKit BOM)
15. Conduit and cabling
16. Map dashboard, open data export and data governance templates (software and documents)
17. Cabinet sun shield for outdoor sites (BOM item 19)

The priced bill of materials is in [bom/bom.csv](bom/bom.csv): $739.00 for the pilot kiosk, $769.00 with the outdoor sun shield, $1,029.00 for the pilot kiosk with the TwinKit gateway.

## Safety

> Privacy by design: no images, audio recordings or personal identifiers leave the device; only aggregate counts or levels are stored. Check local data protection law before any deployment. Mains wiring must be done or checked by a qualified electrician and follow local electrical code.
>
> The kiosk is a roughly 60 kg steel post: install it only with the asset owner's permission, on a footing designed for local wind loads, with no sharp edges at head height. The TwinKit gateway contains a LiFePO4 backup pack: use a pack with a built-in BMS and fuse, and keep the cabinet out of direct sun or under its sun shield, because in sun it can run far above the pack's 45 °C charge limit. CityTwin is not a public warning system.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (CTW-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `CTW-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.
