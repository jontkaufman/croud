# Diversity Matrix

Reference doc enumerating the dimensions across which the persona library should span. The persona generator skill consults this matrix at generation time:

- In **random** mode, it picks one value per dimension, biased toward dimension cells underrepresented in the current `_index.md`.
- In **fill-gaps** mode, it computes coverage per axis and prioritizes underrepresented cells.
- In **tag-spec** mode, it locks user-specified axes and randomizes the remainder.

The goal is to avoid clustering — no two personas should be near-duplicates, and the library as a whole should approximate the variance of real human web users.

---

**Demographic / structural**
- Age buckets: 13–17, 18–25, 26–34, 35–49, 50–64, 65–79, 80+
- Race / ethnicity: full spectrum, including mixed
- Geography: urban / suburban / rural × global regions
- Income: poverty, working, middle, upper-middle, wealthy
- Education: none / HS / trade / bachelor / advanced
- Profession: blue-collar, white-collar, creative, retired, student, unemployed, gig, founder, etc.
- Family/household structure: single / partnered / caregiver / kids-ages / multi-gen
- Immigrant/generation status: native / 1st-gen / 2nd-gen / international
- Sexual orientation / gender identity
- Religious observance: none / occasional / devout

**Technical / contextual**
- Tech literacy: novice / casual / power-user / professional
- Device primary: mobile (Android/iOS), desktop, tablet, low-end / high-end
- Internet quality: rural-slow / mobile-only / fiber / satellite
- Browsing context typical: in-bed / lunch-break / at-desk / on-toilet / waiting-room / commuting
- Time of day typical: early-morning / midday / evening / late-night
- Privacy posture: paranoid / cautious / indifferent

**Cognitive / behavioral**
- Reading style: skimmer / scanner / deep-reader / title-only / never-reads
- Reading literacy level: distinct from formal education
- Attention span: ADHD / focused / chronic-multitasker
- Patience: very-low / low / medium / high
- Disposition: trusting / skeptical / anxious / enthusiastic / indifferent
- Typical mood online: bored / rushed / leisurely / pissed-off / curious

**Physical / accessibility**
- Disability: vision / motor / cognitive / none
- Color vision: standard / deuteranopia / protanopia / tritanopia
- Motor/dexterity: standard / tremor / one-handed / accessibility-tools
- Language fluency: native / second-language / ESL-low

**Commercial / experiential**
- Buying style: research-heavy / impulsive / word-of-mouth / never-buys-online
- Risk tolerance: paranoid-CC / freely-buys / BNPL-user
- Brand sophistication: knows-every-brand / mid / brand-naive
- Domain expertise areas: list (drives jargon comprehension at review time)
- Past online traumas: scammed-before / identity-stolen / never-burned / bad-delivery
- Trust signals valued: reviews / press-logos / security-badges / founder-face / known-brand / referrals
- Currency / measurement defaults: USD/EUR/INR/etc; metric/imperial

**Aesthetic**
- Visual preference: minimalist / maximalist / nostalgic / corporate-polished / indie-handmade / brutalist / luxury
- Aesthetic suspicion threshold: when "polished" tips into "fake"
- UI pet peeves: popups / autoplay / sticky-chat / cookie-banners / paywalls / endless-scroll / mandatory-signup

**Cultural / contextual**
- Cultural/political bubble: terminally-online / mainstream / log-off / niche-community
