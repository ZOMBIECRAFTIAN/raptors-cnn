# Plan B for Friday - if something fails

A short, calm protocol for the four most common Friday failures.

---

## Before you leave the house

Check that each of these is true. Tick them off out loud.

- [ ] Laptop is charged.
- [ ] Laptop charger and HDMI/USB-C adapter are in the bag.
- [ ] USB stick has `Portfolio_Presentation_EN.pptx` saved.
- [ ] USB stick also has a **PDF copy** of the deck (export from PowerPoint: File -> Export -> PDF).
- [ ] All three GitHub repos are pushed and accessible.
- [ ] All four `.md` documents (Project_Overview, Speaker_Notes, Cheat_Sheet, QA_Anticipated_Questions) are printed in landscape A4.
- [ ] Phone is charged and has the elevator pitch (`Elevator_Pitch_EN.md`) downloaded as a PDF for offline reading.
- [ ] Water bottle.
- [ ] You ate breakfast.
- [ ] You arrived 20 minutes early.

---

## Failure mode 1 - Projector does not work

**Symptoms:** HDMI / USB-C adapter does not connect, image flickers, resolution wrong.

**Action:**
1. Ask the host to call IT. While they do, turn your laptop screen toward the professor.
2. Open the deck and **enter slideshow mode** anyway. Even on a 13" screen, two people can follow.
3. Speak more slowly to compensate for the smaller visual.
4. Do not let this throw you. Smile and say:

> "I'll show you on the laptop while we wait for the projector - it actually works for two people."

---

## Failure mode 2 - No internet on the laptop

**Symptoms:** Wi-Fi disconnected, captive portal, slow.

**Action:**
1. **The deck works offline** - it has no embedded online resources.
2. The Flask GUI demo will not work (it needs no internet, but the model needs to be present). If you brought the trained model, demo locally. If not, skip the live demo and say:

> "I'll show you the GUI on a screencast - I have it saved on the USB stick."

3. The GitHub repos can be opened from your phone if the laptop has no internet.

**Pre-Friday prep:** Save screenshots of the GUI in action to the USB stick:
- `gui_upload.png` (drag-drop)
- `gui_top3.png` (with confidence bars)
- `gui_gradcam.png` (the heatmap)
- `gui_factsheet.png` (Merlin-style species sheet)

---

## Failure mode 3 - The Flask demo crashes

**Symptoms:** App throws an error on prediction, the model fails to load, port already in use.

**Action:**
1. Do not panic. The professor cares about the **idea**, not the demo.
2. Say:

> "Looks like the local environment has a hiccup - let me show you the architecture instead. I have a video of the demo if you'd like to see it."

3. Have a 30-second video of the GUI working, saved to your USB stick. Show that.
4. Move on to the next slide. **Do not** debug live.

**Pre-Friday prep:** Record a 60-second screen capture of the Flask app working. Save as `demo_flask.mp4` on the USB.

---

## Failure mode 4 - You blank during the presentation

**Symptoms:** You lose your place in the script, your mind goes empty.

**Action:**
1. **Pause.** Three seconds of silence reads as confidence, not panic.
2. Look at the slide title. The title is your topic.
3. Use this universal recovery line:

> "Let me ground us in why this matters."

   Then say *one* of the three things you know cold:
   - **"This project closes two gaps - epistemic and accessibility."**
   - **"Three numbers tell the story: ..."**
   - **"The way an expert ornithologist would describe this is ..."**

4. Then look back at your printed `Cheat_Sheet_EN.md` for the relevant section.

---

## Failure mode 5 - A question you cannot answer

**Symptoms:** You don't know.

**Action:** Use one of the five recovery phrases:

1. *"That is a great question. I haven't measured that directly, but my intuition is X - I'll verify and follow up."*
2. *"You're right - that is a documented limitation."*
3. *"Honestly, I don't know yet - that experiment is in the roadmap."*
4. *"Let me think about that for a moment."*  (3 seconds of silence is fine)
5. *"Could you help me make sure I understood the question correctly?"*

Never guess wrong. Recovery is always better.

---

## Failure mode 6 - The professor disagrees with your approach

**Symptoms:** "I don't think silhouette-first is the right call." or "Why bother with sign language?"

**Action:**
1. Do not defend immediately.
2. **Listen carefully** - the professor is telling you what they value.
3. Acknowledge the point: *"That's a fair critique. May I share why I chose it?"*
4. Give your evidence: the augmentation ablation plan, the operational match with expert descriptions, the Grad-CAM audit. The Deaf community engagement and WFD manifesto for sign language.
5. End with: *"That said, I'd love to hear how you would approach it differently - that's why I'm here."*

This turns disagreement into collaboration. It is the most powerful move in the meeting.

---

## After the meeting (within 24 hours)

- [ ] Write down every question they asked, in a Google Doc.
- [ ] Mark the ones you didn't answer well.
- [ ] Send a thank-you email referencing one specific thing they said.
- [ ] In the email, attach the GitHub links and the elevator-pitch one-pager.
- [ ] If they asked you to follow up on something, do it within 48 hours.

**Email template:**

> Subject: Thank you for today's conversation - Brian Fernandez Baez
>
> Dear Professor [Name],
>
> Thank you for taking the time today to review my portfolio. I particularly appreciated your point about [specific topic they raised].
>
> As mentioned, the three projects are at:
> - Australia: https://github.com/ZOMBIECRAFTIAN/raptor-australia
> - Mexico: https://github.com/ZOMBIECRAFTIAN/raptors-cnn
> - Bioacoustics: [private link]
>
> Attached is a one-page overview for your reference. I would be very interested in continuing the conversation about [whatever direction they pointed at].
>
> With thanks,
> Brian Fernandez Baez

---

## The single most important piece of advice

**You have built three real projects. The work speaks for itself.** Your job on Friday is not to convince the professor that you are brilliant - it is to **show them what you have actually built** and **listen to where they want to take it next**.

Be calm. Be honest. Be specific. You will do well.
