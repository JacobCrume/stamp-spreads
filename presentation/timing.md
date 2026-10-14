# Stamp Video Presentation — Timing & Script Sheet

**Course:** INFO123 Business AI Project  
**Deliverable:** 2–3 Minute Video Presentation (`.mp4` / `.mov` in Talking-Head format)  
**Strict Requirements:**  
- **Hard stop:** Must conclude before 3m29s (exceeding 3m29s forfeits excellence grades).
- **Pitch limit:** Part 1 (Investor Pitch) must be 1 minute maximum (strict).
- **Format:** Talking-head video (your face visible to camera alongside the slides).
- **AI restriction:** Part 2 (Personal Reflection) must be your own work in your own voice.

---

## Overall Timing Breakdown

| Section | Slide | Target Time | Cumulative | Content |
|---|---|---|---|---|
| **Intro** | Slide 1 (Title) | 0:00 – 0:08 | 0:08 | Title, name, brief opening |
| **Pitch 1** | Slide 2 (Product) | 0:08 – 0:34 | 0:34 | Problem, peel-and-press format, 4 launch flavours |
| **Pitch 2** | Slide 3 (Market) | 0:34 – 0:58 | 0:58 | $341M market growth, format void, unit economics ($5.00/sheet) |
| **Pitch Wrap** | Transition | 0:58 – 1:00 | 1:00 | Hard pitch cutoff at exactly 60 seconds |
| **Reflection 1** | Slide 4 (AI Lessons) | 1:00 – 1:55 | 1:55 | Prompting, context engineering, verification, pivotal moment |
| **Reflection 2** | Slide 5 (Ethics & Slop) | 1:55 – 2:45 | 2:45 | Combating AI slop, regulatory liability, knowledge worker ethics |
| **Wrap & Sign-off** | Slide 5 / Outro | 2:45 – 2:55 | 2:55 | Conclusion & final thank you (well clear of 3:29 limit) |

---

## Part 1: Investor Pitch Script (0:00 – 1:00)

*Read at a natural, energetic conversational pace (~130–140 words per minute). Word count for this pitch script is 132 words (approx. 52–56 seconds spoken).*

### Slide 1: Title (0:00 – 0:08)
> "Kia ora. I'm Jacob, and this is Stamp: a New Zealand breakfast spread innovation engineered for hot toast."

### Slide 2: Pitch 1 — Product Innovation & Launch Range (0:08 – 0:34)
> "Eating toast away from a full kitchen is broken. When you're in a student hall, flat, or office desk, nobody wants to lug a sticky 750-gram jar, track down a table knife, and wash it in an office sink.
> 
> Stamp reinvents the format with a thin, 10-gram disc of real spread on release film. You peel it off, press it onto hot toast, and residual heat softens it into an even spread in seconds. No knife, no open jar, no morning mess. 
> 
> We launch with four distinct flavours: Salted Butter, Raspberry, Yeast extract, and Peanut—pantry-stable for 12 months in an 8-stamp card sheet."

### Slide 3: Pitch 2 — Market Opportunity & Competitive Advantage (0:34 – 0:58)
> "Our analysis of New Zealand breakfast retail sales shows spreads revenue grew 24% to 341 million dollars, with the premium tier surging 29% to 113 million. Yet across 154 existing spread products, not one offers a single-serve portion format. 
> 
> Supermarket jars like Pic's or Fix & Fogg compete on bulk weight, but they are messy and stationary. At five dollars a sheet—just 63 cents a toast portion—Stamp captures premium convenience. With an assumed manufacturing cost of one-fifty, we retain a strong one-dollar-seventy-five gross margin per sheet. Stamp is ready to own portable breakfast."

*(Transition to reflection at 1:00)*

---

## Part 2: Personal Reflection Guidance (1:00 – 2:45)

*Per the assignment brief, this part MUST be in your own words without AI generation. Use the following structured cue points to guide your speaking.*

### Slide 4: Reflection Question 1 — Working with Generative AI (1:00 – 1:55)
*Target duration: ~55 seconds*

**Key prompts to address:**
1. **Prompting & Context Engineering:**
   - Mention how you structured distinct sessions rather than one massive unmanageable chat.
   - Explain how you used explicit negative constraints (e.g. banning health claims and certification badges) and role personas to get reliable results.
   - Highlight the hybrid chatbot architecture: powering customer support via OpenRouter (`openai/gpt-4o-mini`) with locked spec prompts and deterministic fallback to eliminate hallucinations.
2. **Fact-Checking & Independent Verification:**
   - Mention checking the raw breakfast sales data: spotting prices above $40 and verifying formulas (`price × units ≈ revenue`) rather than blindly trusting initial AI summaries.
   - Mention verifying real shelf prices independently on New World (e.g. Fix & Fogg $11.99, Pic's $7.79) to benchmark Stamp realistically.
3. **Pivotal Moment & What You'd Do Differently:**
   - Share a concrete example where an AI model gave an unrealistic answer (e.g., assuming chilled butter could sit ambiently without dairy-spread reformulations, or generating hallucinated organic claims) and how you corrected it.
   - State what you would do differently next time (e.g., establishing the locked specification earlier).

### Slide 5: Reflection Question 2 — Authenticity, AI Slop & Ethics (1:55 – 2:45)
*Target duration: ~50 seconds*

**Key prompts to address:**
1. **Combating 'AI Slop':**
   - Explain how you actively stripped out generic corporate jargon ("game-changer", "revolutionary breakfast journey") in favour of plain, punchy facts: "Peel. Press. Toast."
   - Contrast real physical packaging constraints (die-cut card, foil release liners) with typical AI fantasy mockups.
2. **Regulatory & Ethical Hazards:**
   - Emphasize the legal hazards of AI in food and beverage: hallucinated health benefits, false "gluten-free" claims (dangerous when Yeast extract contains barley gluten), and allergen responsibility (peanut allergy warnings).
   - How human steering was essential to enforce strict compliance with New Zealand Food Standards.
3. **The Role of the Future Knowledge Worker:**
   - Conclude with your takeaway: Generative AI accelerates drafting, but human judgment, taste, skepticism, and ultimate accountability can never be outsourced to a model.

---

## Recording & Export Instructions

1. **Software:** Open `presentation/Stamp-pitch.pptx` in Microsoft PowerPoint.
2. **Camera Setup:** Go to **Record** > **Record Slide Show** (or **From Beginning**).
   - Ensure your webcam is enabled in the bottom-right or corner of the screen so your talking head is clearly visible alongside the slides.
   - Check lighting (face well lit from the front, no heavy backlighting).
   - Test microphone audio levels.
3. **Execution:**
   - Start the recording and deliver the pitch following the timing marks.
   - Keep an eye on the running timer: Pitch concludes at ~0:58; Reflection concludes around 2:45.
   - Conclude and stop recording before **3:20** (safe buffer before the 3:29 penalty).
4. **Export:**
   - Click **File** > **Export** > **Create a Video** (or **Export As** > **Format: MP4**).
   - Select Full HD (1080p).
   - Save the exported file (e.g. `Jacob-Stamp-Presentation.mp4`).
5. **Verify:**
   - Open the `.mp4` file and watch it through: confirm video plays, audio is crisp and in sync, your face is visible, and duration is between 2:30 and 3:00.
