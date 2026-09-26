---
doc_id: CTW-PRB-001
title: CityTwin problem statement
project: CityTwin
doc_type: Problem statement
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (problem, users, context, constraints, prior work, open questions)
---

# CityTwin problem statement

City data sits in separate vendor dashboards, and residents rarely see the data collected on their streets. Where street sensing has been proposed without clear rules on who holds the data and what leaves the device, it has lost public trust.

## The problem

A city that installs counters, air and noise sensors, flood gauges and curb sensors usually buys each from a different vendor, with a different dashboard, data format and contract. The data stays in those silos, so a planner cannot put pedestrian counts next to air quality or flooding on one map, and a resident walking past a sensor cannot see what it measures, who is responsible for it, or the data it has collected.

Trust is the second problem. In a 2019 survey, 66 % of U.S. adults said the potential risks of government data collection about them outweigh the benefits, and 84 % said they have very little or no control over the data government collects about them ([Pew Research Center, 2019](https://www.pewresearch.org/internet/2019/11/15/americans-and-privacy-concerned-confused-and-feeling-lack-of-control-over-their-personal-information/)). In Toronto, Ontario's former privacy commissioner Ann Cavoukian resigned from the Sidewalk Labs project because de-identification at the source of collection could not be guaranteed for all participants ([CBC News](https://www.cbc.ca/news/canada/toronto/ann-cavoukian-sidewalk-data-privacy-1.4872223)); the project was later withdrawn on May 7, 2020, with Sidewalk Labs citing economic uncertainty ([Sidewalk Labs](https://medium.com/sidewalk-talk/why-were-no-longer-pursuing-the-quayside-project-and-what-s-next-for-sidewalk-labs-9a61de3fee3a)).

The lab's smart city set (CurbCount, CrossSafe, PotholeLog, DockHub, LoadZone, HeatMap Node, FloodGauge, AirStreet and NoiseMap) already follows one privacy rule: counts or levels only, with no images or audio leaving the device. What is missing is the layer that brings their data together, applies the same rules to what is published, shows it to residents in the street, and exports it as open data.

## Prior work

- **Open sensor platforms.** Barcelona's [Sentilo](https://www.sentilo.io/) is an open-source sensor and actuator platform built so a city can avoid technological silos. [Civil IoT Taiwan](https://ci.taiwan.gov.tw/) publishes air quality, water, earthquake and disaster sensor data as open data. Both are city- or nation-scale platforms, not a kit a small city or neighborhood group can run.
- **Open standards for sensor data.** The [OGC SensorThings API](https://www.ogc.org/standards/sensorthings/) is an open, geospatial standard for IoT observations and metadata.
- **Transparency in public space.** [Digital Trust for Places and Routines (DTPR)](https://dtpr.io/), stewarded by Helpful Places, is an open communication standard with icons for signage that explain what a sensor in public space does.
- **Community sensing.** [AirQo](https://airqo.net/), a Makerere University project, runs more than 400 low-cost air quality sensors in 14 African countries and publishes the data to the public.
- **Lab dependencies.** CityTwin runs on the TwinKit gateway (LoRaWAN concentrator, MQTT broker, time-series database) and reads the nine smart city nodes listed above.

None of these combines a small open gateway, one privacy rule set across many node types, a public street kiosk and an open data export in one design that a small team can build and audit.

## Users and context

Table 1. Users and needs.

| User | Need | Context |
| --- | --- | --- |
| Resident or passer-by | See what is measured on their street, by whom, and the current values, without an app | At the kiosk on a sidewalk, square or transit stop; on a phone through the QR code |
| City planner or engineer | One map of counts, curb use, air, noise, heat and flooding to compare before and after a street change | Office, on the city network |
| Data protection officer | Evidence that published data holds no personal data and follows retention rules | Privacy impact assessment and audit |
| Community group or school | Open files to analyze, and a kiosk to host at a library or community center | Local projects and teaching |
| Researcher or journalist | Documented, reusable open data under an open license | Download or API |
| Maintenance crew | Node health and alerts (battery, last seen, flood alerts) | Depot or field |

**Operating environment (kiosk).** Outdoors on a sidewalk or plaza, in rain, sun and dust, from about -20 °C to +45 °C air temperature depending on the city, with exposure to vandalism. Mains power from a street lighting circuit or an adjacent building. Indoor variants (library, city hall lobby) are simpler.

**Reference neighborhood (proposed, for sizing).** 46 LoRaWAN nodes: 8 CurbCount, 4 CrossSafe, 12 LoadZone pucks, 6 HeatMap Node, 4 FloodGauge, 6 AirStreet and 6 NoiseMap, plus PotholeLog on 3 buses and one DockHub. This is within the roughly 50 nodes that TwinKit is sized for.

## Constraints

- Garage-buildable prototype, about $600 USD (`project.yaml`). The first estimate is above this; see the precis and review note.
- Privacy by design: only counts and levels are taken in, stored or published; no images, audio or personal identifiers.
- Open software (MIT), open hardware (CERN-OHL-S-2.0) and open data under an open license (license awaiting Amish).
- Runs offline on one TwinKit gateway; no dependency on a vendor cloud.
- Mains work by a qualified electrician; street furniture installed only with the asset owner's permission.

## Out of scope

- Any camera, microphone, face or plate recognition, or tracking of individuals.
- Control of city systems (traffic signals, street lights). CityTwin shows and exports data; it does not actuate.
- Emergency alerting. FloodGauge alerts appear on the map, but CityTwin is not a public warning system.
- Large touch-screen advertising kiosks.

## Open questions

- Which city or neighborhood partner hosts the first kiosk? Proposed, awaiting Amish.
- Open data license (CC BY 4.0, CC0 or ODbL)? Proposed, awaiting Amish.
- Small-count threshold and raw data retention period for published people counts? Proposed, awaiting Amish.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
