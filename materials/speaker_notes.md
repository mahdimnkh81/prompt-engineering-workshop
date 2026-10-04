# Speaker notes

## Slide 1 — Better prompts. Measurable results.

00:00–00:03. Welcome participants. Explain that success means usable, verified outputs. Ask everyone to choose one real task they want to improve.

## Slide 2 — One model. Two very different briefs.

00:03–00:07. Source p1. Ask which assumptions the vague request leaves open. Compare role, audience, output shape, and constraints; do not promise a universal improvement percentage.

## Slide 3 — Your route through the workshop

00:07–00:08. Display schedule. Labs include explanation, practice, review and retry time. Review submissions continuously during practice.

## Slide 4 — Open your own workspace

00:08–00:10. Confirm AvalAI is configured. Give each participant only their own credential row. Demonstrate Save draft, Submit, and Refresh feedback. Failed API requests do not assign a score or unlock a task.

## Slide 5 — Set the scene: Python hiring on LinkedIn

First 4 minutes of 00:10–00:30: explain the concept, then demonstrate the next slide. Source PDF pages 1–3. Ask a participant to name one likely failure mode.

## Slide 6 — Demonstration: explain an API invoice item

Use this API explanation as the demonstration. The participant exercise is the separate LinkedIn Python hiring scenario.

## Slide 7 — A pattern you can adapt

Demonstrate this example as part of the teaching allocation. Ask which details are reusable and which must change for a new task. Model outputs can vary; compare against requirements.

## Slide 8 — Your task

Practice for 10 minutes. Submit your prompt and the concept answer on your own page. The AI evaluator provides scores and feedback.

## Slide 9 — Check, discuss, improve

Reserve 6 minutes for feedback, retries, and a short discussion. Use the task-specific maximum points: Lab 1 uses 20/20/20/40; other labs use 25 each. Ask: Do large language models remember your previous conversations? Correct answer: No. The model's weights do not change between chats; it only "knows" what is inside the current context window. Apps that seem to remember you are re-inserting saved notes into the prompt.. Never use model self-confidence as proof of correctness.

## Slide 10 — Few-shot examples: Content Moderation & PII

First 4 minutes of 00:30–00:50: explain the concept, then demonstrate the next slide. Source PDF pages 3. Ask a participant to name one likely failure mode.

## Slide 11 — A pattern you can adapt

Demonstrate this example as part of the teaching allocation. Ask which details are reusable and which must change for a new task. Model outputs can vary; compare against requirements.

## Slide 12 — Your task

Practice for 10 minutes. Submit your prompt and the concept answer on your own page. The AI evaluator provides scores and feedback.

## Slide 13 — Check, discuss, improve

Reserve 6 minutes for feedback, retries, and a short discussion. Use the task-specific maximum points: Lab 1 uses 20/20/20/40; other labs use 25 each. Ask: Why does starting a prompt with "You are a Senior Cloud Solutions Architect..." usually produce a better technical answer than asking the same question with no role? Correct answer: Because the role is a statistical condition on next-token prediction: it pushes the model toward domain vocabulary, an expert's priorities, and implicit expectations like a professional tone, without spelling each one out. Never use model self-confidence as proof of correctness.

## Slide 14 — Chain-of-thought (CoT): Multi-step Debugging

First 4 minutes of 00:50–01:10: explain the concept, then demonstrate the next slide. Source PDF pages 3–4. Ask a participant to name one likely failure mode.

## Slide 15 — A pattern you can adapt

Demonstrate this example as part of the teaching allocation. Ask which details are reusable and which must change for a new task. Model outputs can vary; compare against requirements.

## Slide 16 — Your task

Practice for 10 minutes. Submit your prompt and the concept answer on your own page. The AI evaluator provides scores and feedback.

## Slide 17 — Check, discuss, improve

Reserve 6 minutes for feedback, retries, and a short discussion. Use the task-specific maximum points: Lab 1 uses 20/20/20/40; other labs use 25 each. Ask: Why does asking the model to reason step by step before answering improve the analysis of a long error log? Correct answer: Each reasoning token it writes becomes part of the context, so the final answer is conditioned on the listed errors and deductions instead of the first salient warning.. Never use model self-confidence as proof of correctness.

## Slide 18 — Structured output: Relational JSON Shape

First 4 minutes of 01:10–01:30: explain the concept, then demonstrate the next slide. Source PDF pages 4. Ask a participant to name one likely failure mode.

## Slide 19 — A pattern you can adapt

Demonstrate this example as part of the teaching allocation. Ask which details are reusable and which must change for a new task. Model outputs can vary; compare against requirements.

## Slide 20 — Your task

Practice for 10 minutes. Submit your prompt and the concept answer on your own page. The AI evaluator provides scores and feedback.

## Slide 21 — Check, discuss, improve

Reserve 6 minutes for feedback, retries, and a short discussion. Use the task-specific maximum points: Lab 1 uses 20/20/20/40; other labs use 25 each. Ask: Your prompt includes a JSON skeleton where tasks[].assignedTo must match users[].userId. What is the main remaining risk and the best mitigation? Correct answer: The model can still invent or mismatch IDs or add text around the JSON; forbid extra text and validate in code that the JSON parses and every assignedTo exists in users.. Never use model self-confidence as proof of correctness.

## Slide 22 — Break · 10 minutes

01:30–01:40. Preserve the break. Use the dashboard to identify participants needing help.

## Slide 23 — Tone control (Pure Negative Constraints)

First 3 minutes of 01:40–01:55: explain the concept, then demonstrate the next slide. Source PDF pages 5. Ask a participant to name one likely failure mode.

## Slide 24 — A pattern you can adapt

Demonstrate this example as part of the teaching allocation. Ask which details are reusable and which must change for a new task. Model outputs can vary; compare against requirements.

## Slide 25 — Your task

Practice for 7 minutes. Submit your prompt and the concept answer on your own page. The AI evaluator provides scores and feedback.

## Slide 26 — Check, discuss, improve

Reserve 5 minutes for feedback, retries, and a short discussion. Use the task-specific maximum points: Lab 1 uses 20/20/20/40; other labs use 25 each. Ask: Which statement about negative constraints ("Do not ...") is most accurate? Correct answer: They work best when specific (e.g., "do not use words like shocking or disaster") and paired with what to do instead, because vague bans leave the model guessing.. Never use model self-confidence as proof of correctness.

## Slide 27 — Interview-style prompting

First 3 minutes of 01:55–02:10: explain the concept, then demonstrate the next slide. Source PDF pages 5–6. Ask a participant to name one likely failure mode.

## Slide 28 — A pattern you can adapt

Demonstrate this example as part of the teaching allocation. Ask which details are reusable and which must change for a new task. Model outputs can vary; compare against requirements.

## Slide 29 — Your task

Practice for 7 minutes. Submit your prompt and the concept answer on your own page. The AI evaluator provides scores and feedback.

## Slide 30 — Check, discuss, improve

Reserve 5 minutes for feedback, retries, and a short discussion. Use the task-specific maximum points: Lab 1 uses 20/20/20/40; other labs use 25 each. Ask: In an interview-style prompt, what is the main purpose of an explicit stopping condition (e.g., "after 3 matching accomplishments, say I have enough data and write the letter")? Correct answer: Without it, the model either keeps asking indefinitely or decides on its own when to stop; the condition makes the switch to writing predictable and checkable.. Never use model self-confidence as proof of correctness.

## Slide 31 — Roles, chaining, and self-evaluation

First 4 minutes of 02:10–02:30: explain the concept, then demonstrate the next slide. Source PDF pages 6–7. Ask a participant to name one likely failure mode.

## Slide 32 — A pattern you can adapt

Demonstrate this example as part of the teaching allocation. Ask which details are reusable and which must change for a new task. Model outputs can vary; compare against requirements.

## Slide 33 — Your task

Practice for 10 minutes. Submit your prompt and the concept answer on your own page. The AI evaluator provides scores and feedback.

## Slide 34 — Check, discuss, improve

Reserve 6 minutes for feedback, retries, and a short discussion. Use the task-specific maximum points: Lab 1 uses 20/20/20/40; other labs use 25 each. Ask: Your team sends the same 40-page contract to the model many times a day, each time with a different question. Which prompt layout is best, and why? Correct answer: Contract first inside <documents> tags, question last: the instruction sits right before generation where attention is strongest, and the unchanged contract forms a static prefix that can be cached across requests. Never use model self-confidence as proof of correctness.

## Slide 35 — Capstone: evidence over impressions

First 4 minutes of 02:30–02:50: explain the concept, then demonstrate the next slide. Source PDF pages 7–9. Ask a participant to name one likely failure mode.

## Slide 36 — A pattern you can adapt

Demonstrate this example as part of the teaching allocation. Ask which details are reusable and which must change for a new task. Model outputs can vary; compare against requirements.

## Slide 37 — Your task

Practice for 10 minutes. Submit your prompt and the concept answer on your own page. The AI evaluator provides scores and feedback.

## Slide 38 — Check, discuss, improve

Reserve 6 minutes for feedback, retries, and a short discussion. Use the task-specific maximum points: Lab 1 uses 20/20/20/40; other labs use 25 each. Ask: You revised your classifier prompt and it now labels all 4 test inputs correctly (the baseline got 3/4). What is the strongest justified conclusion? Correct answer: The revision is promising; rerun both versions on the same fixed tests plus new unseen edge cases (e.g., an injection attempt) and keep the failures before claiming it is more reliable.. Never use model self-confidence as proof of correctness.

## Slide 39 — Common failures → useful repairs

02:50–02:53. Source pp7–8. Ask participants which failure they observed in their own attempts.

## Slide 40 — Transfer the technique to your work

02:53–02:56. Source p8. Invite two participants to show a before/after example. Model-generated citations and APIs need independent verification.

## Slide 41 — Keep a prompt journal

02:56–03:00. Source p9. Ask for one specific next action. Point to source PDF and provider-specific documentation; controls such as temperature differ between models.
