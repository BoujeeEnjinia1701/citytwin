# CityTwin

**Area:** Smart Cities · **Status:** Concept · **Prototype budget:** about $600 USD · **Difficulty:** 3 of 5

A city dashboard built on TwinKit that brings the smart city nodes together on a map and in a public kiosk, with open data export and privacy rules built in.

## Concept rationale

One open, public view of street data builds trust and lets residents and planners use the same evidence.

## Burning platform

Smart city projects have lost public trust where data was closed or used without consent.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. It ties the smart city set together on TwinKit.

## Problem

City data sits in separate vendor dashboards, and residents rarely see the data collected on their streets.

## Concept

A city dashboard built on TwinKit that brings the smart city nodes together on a map and in a public kiosk, with open data export and privacy rules built in.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- TwinKit gateway and software
- Map dashboard
- Public kiosk enclosure with screen
- Open data export
- Data governance templates

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Privacy by design: no images, audio recordings or personal identifiers leave the device; only aggregate counts or levels are stored. Check local data protection law before any deployment. Mains wiring must be done or checked by a qualified electrician and follow local electrical code.

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Smart cities set.
