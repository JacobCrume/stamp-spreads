# INFO123 — Deliverable build plan

**Due:** 16 October 2026, 5:00 pm, via Learn.
**Who builds it:** this project, in this workspace. No Gemini, Mistral, ChatGPT, Figma, Suno, or other AI product is part of the build.
**Product:** Stamp, a line of peel-and-press spread portions for toast. Each portion sits on a release film like a sticker. You peel one off and press it onto hot toast; the heat softens it into a layer. No knife, no open jar.

The brief’s chat-by-chat workflow is not the plan. The plan is the sequence that produces the files and URLs Learn marks.

---

## What we are shipping

| Deliverable | File or URL | Pass condition |
| --- | --- | --- |
| Business plan | `business-plan/Stamp-business-plan.pdf` | One PDF, 1,500–2,500 words excluding images. Contains the market figures, logo, pack shot, social ad, process diagram, and ERD, each beside the paragraph that uses it. Covers product, market, competitors, marketing, operations, and information systems. |
| Jingle | `audio/stamp-jingle.mp3` | Plays, 15–60 seconds, names Stamp and the toast-sticker idea. |
| Website | Vercel production URL | Loads with no login. Landing page for Stamp. |
| Chatbot | `{site}/chat` | Same deployment. Answers product questions from the locked spec. No login. |
| Video | `.mp4` you record from the slide deck we build | Talking-head, 2–3 minutes, hard stop 3:29. Pitch finishes by 1:00. |
| Chat-session form | Learn form | Still a graded item. We submit the link to this project’s sessions. It is not a separate production stage. |

Missing the video scores 0/25. Missing the chat-session form scores an E. The PDF, jingle, site, and chatbot are the other four core items.

---

## Product spec we will build against

Locked now, so the logo, pack, site, bot, jingle, and PDF describe the same thing.

| Item | Decision |
| --- | --- |
| Brand and product name | **Stamp** |
| Format | A thin, single-serve disc of spread on a food-safe release film, nested in a printed card sheet. Peel, press onto hot toast, done. |
| Category in the dataset | Spreads |
| Launch line | Four flavours, locked with you: Salted Butter, Raspberry, Yeast extract, Peanut. |
| Packs | An 8-stamp sheet of one flavour (10 g each, 80 g), and a mixed sheet with two of each. $5.00 a sheet. |
| Buyer | Someone who eats toast away from a full kitchen: a flat, an office, a hall, a school bag. They want flavour without a knife or a jar. |
| Position | Pantry-stable for 12 months. $5.00 a sheet is $6.25 per 100 g, above about 90% of branded spread SKUs. |
| Allergen we will state | Peanut contains peanuts. Salted Butter is dairy. Yeast extract contains gluten from barley. Full list is in `brand/product-spec.md`. |
| Claims we will make | Peel-and-press, one portion, even cover, four flavours, no knife. |
| Claims we will not make | Health treatment, organic, gluten-free, low-sugar, or “better for you,” unless a finished recipe actually supports that sentence. No fake certification marks on the pack. |

Raw dataset baseline the market section starts from (revenue column, as published, in thousands of NZD):

| Year | Spreads revenue (thousands NZD) | Spreads units (thousands) |
| --- | --- | --- |
| 2022 | 274,859 | 32,758 |
| 2023 | 305,274 | 36,273 |
| 2024 | 315,577 | 37,946 |
| 2025 | 341,356 | 40,213 |

That is about 24% revenue growth from 2022 to 2025. Premium tier revenue inside spreads rose faster than value (about 29% vs about 8%). The sheet has 41 spread brands and 154 spread product names. None of those names describe a portion, sachet, pod, or peel-and-press format. Stage 1 cleans the known bad price cells before any chart is final, then these totals are recomputed and only the recomputed figures go in the PDF.

Nearest jar brands already in the file, for the competitor section: Fix & Fogg, Pic's, Nutella, Vegemite, Bega, Sanitarium, Pams, and the honey brands (Airborne, Egmont, Manuka Doctor). Live shelf prices are collected in Stage 5 from retailer or brand pages.

---

## Repository layout

```text
INFO123 Project/
  PLAN.md
  nz_breakfast_sales_2022_2025.xlsx
  data/                 cleaned table, figure script, PNGs
  brand/                logo, pack, ad, prompts, palette
  audio/                lyrics, render script, mp3
  diagrams/             process and ERD source plus PNG
  business-plan/        copy, build script, PDF
  website/              SvelteKit app
  presentation/         pitch deck and timing sheet
```

One product file, `brand/product-spec.md`, is the source for the PDF, the site copy, the chatbot answers, and the jingle hook. Later stages read it. They do not invent a second version of the product.

---

## Stage 1 — Product lock and market figures

**Produces:** the spec every later asset quotes, and the charts that go in the PDF.

1. Write `brand/product-spec.md`: format, four flavours, both pack types, use steps, buyer, claims list, allergen list, home recipe per flavour, and an industrial version (deposit onto release film, cut, nest in a sheet, flow-wrap). Industrial constraints: target cost per stamp, ambient or chilled shelf life, and the claim ban from the table above.
2. Clean `nz_breakfast_sales_2022_2025.xlsx` with a Python script into `data/spreads-clean.csv`.
   - A row is name + brand + weight + quarter. Same name with two weights is two SKUs.
   - Replace unit prices above $40 when units and revenue imply a normal shelf price (`revenue ÷ units`). Log each replacement.
   - Impute a missing revenue or units only when the surviving price makes the identity `price × units ≈ revenue` hold.
   - Parse weight into grams and pack count.
3. Recompute spreads revenue and units by year, by price tier, and by brand. Build three PNG figures in `data/figures/`:
   - Quarterly spreads revenue, 2022-Q1 through 2025-Q4, with the other three categories as context.
   - 2022 vs 2025 spreads revenue by price tier.
   - Price per 100 g for branded spreads, with the Stamp sheet price marked once it is chosen.
4. Set the sheet price and the mixed-sheet price from that per-100 g band. Record both in the product spec.

**Done when:** the spec has recipes, prices, and claims; the three PNGs exist; every number on them matches the cleaned CSV.

## Stage 2 — Logo, pack, and social ad

**Produces:** the three images the PDF and the site share.

Visual system, fixed before generation:

- Wordmark: STAMP, all capitals. A custom drawing in the Toundra construction (heavy stems, round feet, semicircular arches). No symbol.
- One colour pair on every flavour: light purple `#E24BFF` and dark purple `#3B0764`. Dark on light, the same relationship as Toundra's forest green on lime. Flavour is type, not a second colour.
- Manrope is the text face only. It is not the wordmark.
- Pack: flat front. Forest field, purple STAMP, flavour name, and the line “Peel. Press. Toast.”
- Ad: 4:5, purple field, STAMP, and the same line.

Generation order: logo first, then pack and ad using the logo as the reference image so the mark matches. Save the final files as `brand/logo.png`, `brand/pack.png`, and `brand/ad.png`. Keep the earlier frames in `brand/explorations/` so the finals are the ones the other stages use.

**Done when:** the three finals show the same name, the same four flavours, and no certification badges we do not hold.

## Stage 3 — Jingle

**Produces:** `audio/stamp-jingle.mp3`.

Built locally. No music-generation service.

1. Write a 20–40 second lyric in `audio/lyrics.txt`. The hook says “Stamp” and the action peel / press / toast. One flavour can be named. Tone matches the pack: short, bright, not a wellness ad.
2. Render a melody and a simple drum bed in Python (numpy) and mix a vocal with a local speech engine (`espeak-ng` or `festival`). Export with ffmpeg.
3. Measure the file with `ffprobe`. Trim or rewrite until the duration is inside 15–60 seconds and the product name is intelligible.

**Done when:** the mp3 plays on its own, the duration check passes, and the lyric file matches the recording.

## Stage 4 — Process diagram and ERD

**Produces:** the two figures the PDF still needs, plus the facts printed next to them.

1. Pick one real New Zealand company that can deposit or portion-pack a spread. Record the trading name, the page the contact details came from, the location, and why the process fits a film-and-sheet format. Save this in `diagrams/manufacturer.md`.
2. Critical process: **sheet making and release** — order in, batch deposit onto film, cut, nest, check, pack, dispatch. That is the process whose failure means a customer gets no breakfast. Draw it as a Mermaid flowchart with one failure path (failed weight check or film that will not release). Export `diagrams/process.png`. Write two bottlenecks and the operational response under the figure notes.
3. Business-level entities: Product (flavour), Sheet (the sellable pack), Customer, Order, Order line, Batch, Manufacturer, Campaign. Five KPIs, each with a formula and the entity it comes from:
   - repeat purchase rate
   - stamps per order
   - on-time dispatch rate
   - batch rejection rate
   - gross margin per sheet after manufacturer cost
4. Mermaid `erDiagram` to `diagrams/erd.png`. Short note on two questions this model can answer (which flavour is reordered, which batch failed release) and one it cannot (a medical effect).

**Done when:** both PNGs render cleanly, the manufacturer contact is copied from a page we opened, and the KPI list matches the ERD entities.

## Stage 5 — Business plan PDF

**Produces:** `business-plan/Stamp-business-plan.pdf`.

A Python build script (`business-plan/build_pdf.py`, reportlab) lays the document out. Copy lives in `business-plan/copy.md` so the word count is checkable before export. Images are placed by the script from the paths above, not pasted by hand into a chat export.

| Section | Words | Content |
| --- | --- | --- |
| Cover | — | STAMP wordmark, logo, your name, date |
| Executive summary | 180–220 | Format, buyer, the spreads growth result, the jar-vs-stamp difference |
| Product | 300–400 | Four flavours, both recipes in brief, pack, price, how to use |
| Market | 300–400 | Cleaned figures and what they justify. Units labelled as NZD, not “thousands” left ambiguous. |
| Competitors | 250–350 | Three jar competitors with a sourced price, pack size, and the format difference |
| Customer and brand | 150–200 | Buyer, logo, pack shot, the line of ad copy |
| Marketing | 250–350 | Channel (Instagram and short video), the ad, where the jingle runs, two or three real NZ podcasts whose pages we opened |
| Operations | 200–280 | Manufacturer, the sheet-making process, the diagram, two bottlenecks |
| Information | 200–280 | Five KPIs, the ERD, two decisions the data supports |
| First 90 days | 80–120 | Assumptions labelled as assumptions |

Word count is the prose only. The script fails the build if the count falls outside 1,500–2,500. After export, render the PDF pages to images and read them: spelling of STAMP, figure legibility, no empty boxes, captions that state a conclusion.

**Done when:** the PDF builds in one command, the word-count check passes, and all six image types are visible in the rendered pages.

## Stage 6 — Website (SvelteKit)

**Produces:** a SvelteKit app in `website/` that we can deploy.

| Choice | Spec |
| --- | --- |
| Framework | SvelteKit, TypeScript |
| Adapter | `@sveltejs/adapter-vercel` |
| Styling | Project CSS. Palette and type from Stage 2. No component library. |
| Rendering | Marketing routes prerendered. |
| Assets | Logo, pack, and ad copied into `website/static/` from `brand/`. |
| Copy | Pulled from `brand/product-spec.md`. The site does not add claims the spec forbids. |

Routes:

| Path | Page |
| --- | --- |
| `/` | Landing. What a Stamp is, the peel-press-toast sequence, the four flavours, the sheet price, one market sentence, the pack image. |
| `/flavours` | One block per flavour: name, taste, allergen, which sheet it is on. |
| `/chat` | Built in Stage 7. Linked in the header from the start so the nav does not change after deploy. |

No cart and no payment. The call to action is the product explanation and the support chat. A fake checkout is out of scope.

**Done when:** `npm run build` succeeds, `/` and `/flavours` show the real pack and the locked prices, and a logged-out browser can read both.

## Stage 7 — Support chatbot

**Produces:** `/chat` on the same app. The public chatbot URL is the site URL plus `/chat`.

The bot is ours. It does not call another model at runtime.

- Knowledge is a typed module, `website/src/lib/knowledge.ts`, authored from the product spec: what a Stamp is, how to apply it, the four flavours, allergens, prices, pack contents, where it will be sold (direct, at launch), and a crushed-sheet complaint reply.
- Matching is intentional and small: normalise the question, score it against those topics, return the authored answer. A question that does not match gets a short reply listing what the bot can answer.
- Hard refusals, also authored: medical advice, and any “is it organic / gluten-free / low-sugar?” question, which is answered with the claim ban.
- The page looks like a support chat: a transcript, a text field, Stamp’s voice in short sentences.

Test list, saved as a run we can repeat:

1. What is a Stamp?
2. How do I use it?
3. What flavours are there?
4. Does the Peanut stamp contain nuts?
5. Is it gluten-free?
6. How much is a sheet?
7. Where can I buy it?
8. My sheet arrived crushed.
9. Will this help my stomach?
10. How does it compare with a jar of peanut butter?

**Done when:** those ten questions return the spec’s answers, questions 5 and 9 stay inside the claim ban, and the page is reachable at `/chat`.

## Stage 8 — Deploy on Vercel

**Produces:** a production URL with no login.

1. Vercel project, root directory `website`, framework SvelteKit, adapter already set.
2. Production deploy from this project.
3. Open the production origin and `/chat` in a private window. Confirm images load, prices match the PDF, and one chat question is answered.
4. Write both URLs into `business-plan/urls.txt` and into the executive summary if the PDF is rebuilt after deploy. Rebuild the PDF if the summary names the URL.

**Done when:** the private-window check passes on the production host, not on `localhost`.

You will need to be logged in to Vercel for the deploy. The app itself does not ask a visitor to log in.

## Stage 9 — Video package

**Produces:** a slide deck you record. The recording has to be you.

We build `presentation/Stamp-pitch.pptx` and `presentation/timing.md`.

| Time | Slides | Content we prepare |
| --- | --- | --- |
| 0:00–0:10 | Title | Stamp, your name. Does not count toward the two pitch slides. |
| 0:10–0:30 | Pitch 1 | The sticker format and the four flavours. |
| 0:30–1:00 | Pitch 2 | The spreads growth number from Stage 1, and the difference versus a jar. |
| 1:00–2:50 | 2–4 reflection slides | Slide shells and the two questions only. |

Pitch speaker notes are written to those times. You record with PowerPoint’s Record Slide Show, or any webcam-plus-slides recording, and export `.mp4`. Target length 2:30–2:50. Stop before 3:29.

The reflection answers stay in your voice: a specific moment from this build, and one critique of using AI to create the business. We leave those slides unwritten so the reflection you submit is yours.

**Done when:** the deck exists, the pitch notes fit in 60 seconds when read aloud, and you have an `.mp4` under 3:29 with your face and the slides in frame.

## Stage 10 — Submission pack

On the morning of 16 October:

- Upload the PDF, the mp3, and the mp4 as files.
- Submit the Vercel URL and the `/chat` URL on the Learn form.
- Submit this project’s session link on the chat-session form.
- Open the production site once more in a private window before you send it.

---

## Stage order

```text
1 Product spec + cleaned data + market figures
        │
        ├── 2 Logo, pack, ad
        ├── 3 Jingle
        └── 4 Manufacturer, process PNG, ERD PNG
                 │
                 ▼
            5 Business plan PDF
                 │
                 ▼
            6 SvelteKit site ── 7 /chat bot ── 8 Vercel
                                                   │
                                                   ▼
                                            9 Slides and your recording
                                                   │
                                                   ▼
                                            10 Submit
```

Stages 2, 3, and 4 can run as soon as Stage 1 has locked the name, the flavours, and the claims. The PDF waits until their files exist. The site waits until the logo and pack exist. The bot waits until the spec’s prices and allergens are final. Deploy is the last software step. The video is last because the pitch numbers have to match the PDF.

## What you do, and what this build does

| You | This build |
| --- | --- |
| Vercel login when we deploy | The SvelteKit app, the bot, the deploy setup |
| Record and export the talking-head video | The deck, the pitch notes, the timing |
| Speak the reflection in your own words | The reflection slide shells and the two questions |
| Click submit on Learn | The PDF, mp3, site, and chat URL |
