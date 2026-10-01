# BOM notes

Costs are indicative estimates for a single prototype, in USD, updated for TRL 3 (CTW-CAL-001 section J). Every line is priced and carries a supplier or supplier type. Only the e-paper display price was checked against the maker's own listing (September 2026); the TwinKit gateway price comes from TwinKit's TRL 3 BOM. Suppliers are not yet selected.

- **Pilot kiosk parts** (items 1 to 12, 14, 15, 20 and 21): $778.00. The value-engineering target (`budget_usd`) is $750, a hypothetical control target and not a limit (set when Amish accepted the recommendations on 2026-09-25, CTW-DDR-002 N1), and under CTW-DDR-001 D1 it covers the kiosk only. The parts added on 2026-10-01 to make the kiosk buildable (CTW-DDR-003: display carrier, fixings, the head's converter, LED driver and terminal block) take the estimated cost $28.00 over the target; savings worth trying are in CTW-DEC-001.
- **Cabinet sun shield** (item 19, outdoor sites only, CTW-DDR-002 N4): $30.00. The outdoor kiosk is $808.00, $58.00 over the value-engineering target; it is reported, not counted under R16, because the pilot is on a sheltered site.
- **TwinKit gateway** (item 13): $290.00, costed in the TwinKit repo. A city that already runs TwinKit only needs the kiosk.
- **Kiosk with gateway**: $1,068.00, reported under R17.
- Screws, rivet nuts, tapes and gaskets are now their own line (21); line 15 keeps the conduit, cables, grommets and earth bonds.
- Items 16 to 18 are software and documents with no parts cost. Hosting for the public open data files is not included.
- The 60 W supply (item 12) covers the 26.7 W peak, and 40.2 W with the street heater studied in CTW-CAL-001; the panel heater is not in the BOM, because it is fitted only where the partner city has frost (CTW-DDR-002 N4) and that city is not yet chosen.
- Not included: concrete footing, anchor design, mains connection by an electrician, permits and installation labor.
