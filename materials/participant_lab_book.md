# Participant lab book

Use your own workspace. Submit your prompt and answer the three-option concept question. The AI evaluator scores four weighted criteria totaling 100; at least 70/100 plus a correct concept answer unlocks the next lab. You may retry.

## Lab 1: Set the scene: Python hiring on LinkedIn (20 minutes)

Define role, audience, tone, and format explicitly so the model does not have to guess.

**Task.** Your company urgently needs to hire a Python developer. Write a prompt that produces an engaging LinkedIn recruiting post attracting talented, suitable candidates. Explicitly specify role, audience, tone, and format. Define a relevant professional role, a precise candidate audience, an appropriate accessible tone, and a clear paragraph structure. The format must explicitly request an example or analogy to make the work understandable. Do not write the post itself. Role: 20 points; audience: 20; tone: 20; format: 40. Without an explicit example/analogy request, format is capped at 20/40. Scores below 70 fail; the concept answer must also be correct.

**Submit.** Only your prompt. The AI evaluator returns scores, evidence, and improvement advice.

**After feedback.** Read the scores, evidence, and suggestions. Revise your prompt and retry when below 70.

**AI rubric (task-specific weights):**

- Role (20): explicitly assigns a relevant role, such as a hiring manager, Python team lead, or technical recruiter.
- Audience (20): precisely identifies the Python candidates being addressed, including relevant experience or interests; the audience must fit recruiting.
- Tone (20): explicitly requests an engaging, professional, welcoming, accessible tone and avoids unexplained jargon.
- Format (40): specifies a clear structure or paragraph plan (20 points) AND explicitly requests a relevant example or analogy (20 points). Without that request, award at most 20/40; naming the word format alone earns no credit.

## Lab 2: Few-shot examples: Content Moderation & PII (20 minutes)

Show consistent input/output examples to teach a pattern, specifically for handling edge cases like PII and safety.

**Task.** Your company is an online pharmacy. You need an AI to summarize long user reviews into a single short sentence. However, there are two legal edge cases: 1. Users sometimes include PII like phone numbers or national IDs. 2. Users ask for medical advice (e.g., "Does this interact with aspirin?"). If published, the company faces fines.

Write a few-shot prompt that summarizes safe reviews into one sentence, but uses at least two edge-case examples to teach the model to return ONLY the tag [FLAG_PII] if personal info is present, and ONLY the tag [FLAG_MEDICAL] if medical advice is requested, without generating any summary. Do not write the final reviews, just the instructions and examples.

**Submit.** Only your prompt. The AI evaluator returns scores, evidence, and improvement advice.

**After feedback.** Read the scores, evidence, and suggestions. Revise your prompt and retry when below 70.

**AI rubric (task-specific weights):**

- PII Example (20 points): The prompt must include a distinct example demonstrating the PII rule (e.g., phone number or national ID).
- Medical Example (20 points): The prompt must include a distinct example demonstrating the medical advice rule.
- Processing Prevention (40 points): In the edge-case examples, the model must be shown returning ONLY the fallback tag ([FLAG_PII] or [FLAG_MEDICAL]) without any accompanying summary or processing of the sensitive text.
- Instruction Clarity (20 points): The initial instructions clearly explain the rules for both safe reviews and edge cases, and align perfectly with the behavior demonstrated in the examples.

## Lab 3: Decomposition and verification (20 minutes)

Break a problem into checkable intermediate results. Request a concise calculation summary and verify it with Python; verbose reasoning is not proof.

**Task.** Write a prompt for buying 3 pens at $2 each and 2 notebooks at $5 each with a 10% discount. Request numeric JSON fields subtotal, discount, and total. Specify the calculation stages and an independent verification step. Do not assume tax or extra fees. Submit instructions, not the numerical answer.

**Submit.** Only your prompt. The AI evaluator returns scores, evidence, and improvement advice.

**After feedback.** Read the scores, evidence, and suggestions. Revise your prompt and retry when below 70.

**AI rubric (task-specific weights):**

- Includes accurate prices, quantities, and discount rate.
- Clearly specifies subtotal, discount, and total calculation stages.
- Defines a numeric JSON contract with the three exact keys.
- Requests independent verification and forbids extra cost assumptions.

## Lab 4: Structured output and grounding (20 minutes)

A requested JSON shape still needs parsing, schema checks, and factual validation. Missing information should remain unknown.

**Task.** Write a prompt to convert these facts to JSON: OurApp costs $12/month with email support; TeamFlow costs $18/month with chat support; SoloDesk has an unknown price and community support. Require a products array in that order, with name, price_usd, and support. Use null for the unknown price and only the supplied facts. Submit the prompt, not the resulting JSON.

**Submit.** Only your prompt. The AI evaluator returns scores, evidence, and improvement advice.

**After feedback.** Read the scores, evidence, and suggestions. Revise your prompt and retry when below 70.

**AI rubric (task-specific weights):**

- Includes all facts about the three products without contradictions.
- Defines products, name, price_usd, support, and their data types.
- Requires null for unknown prices and forbids invented facts.
- Specifies JSON only, product order, and output validation.

## Lab 5: Constraints and iterative refinement (15 minutes)

Turn a vague critique into a concrete revision request. Compare the new result against the original requirements.

**Task.** Write a revision prompt and include this original draft: “Welcome! Smart scheduling is revolutionary. It fixes every meeting problem. Buy now!” Require exactly two factual sentences, at most 50 words, mentioning Google Calendar. Ban Welcome, revolutionary, and Buy now. Identify the original defects and specify how to check the revision. Submit only the revision instructions.

**Submit.** Only your prompt. The AI evaluator returns scores, evidence, and improvement advice.

**After feedback.** Read the scores, evidence, and suggestions. Revise your prompt and retry when below 70.

**AI rubric (task-specific weights):**

- Includes the original draft and identifies concrete defects.
- Explicitly requires exactly two sentences and at most 50 words.
- Requires Google Calendar and excludes all three prohibited phrases.
- Requests factual language, removal of unsupported claims, and a revision check.

## Lab 6: Interview-style prompting (15 minutes)

Ask targeted questions to resolve uncertainty before drafting. State a stopping condition so the interview can finish.

**Task.** Write an interview prompt for an article about async standups. Resolve audience, tone, and product mentions. Ask one question at a time and wait for each answer. Define when to stop interviewing, confirm the brief, and start drafting. Do not run the interview or invent user answers.

**Submit.** Only your prompt. The AI evaluator returns scores, evidence, and improvement advice.

**After feedback.** Read the scores, evidence, and suggestions. Revise your prompt and retry when below 70.

**AI rubric (task-specific weights):**

- Covers the article goal and missing audience, tone, and product policy.
- Explicitly asks one question at a time and waits for an answer.
- Defines a stopping condition and confirmation of the collected brief.
- Drafting begins only after context is complete; user answers are not invented.

## Lab 7: Roles, chaining, and self-evaluation (20 minutes)

Persistent instructions define behavior; user messages define the current task. Split a workflow into stages with explicit handoffs and verify critiques.

**Task.** Write a prompt or message sequence for an outline → draft → critique → revision workflow for a beginner Python KeyError guide. Separate persistent rules from the user task. Require three outline headings and at most 100 words each for draft and revision. Request JSON with outline, draft, critique, and revision. Define stage handoffs and accuracy checks. Do not execute the workflow.

**Submit.** Only your prompt. The AI evaluator returns scores, evidence, and improvement advice.

**After feedback.** Read the scores, evidence, and suggestions. Revise your prompt and retry when below 70.

**AI rubric (task-specific weights):**

- Separates persistent rules from the user request and requires technical accuracy.
- Defines all four stages and how each output feeds the next.
- Specifies the JSON contract, three headings, and both 100-word limits.
- Critiques accuracy and clarity and requires the revision to address that critique.

## Lab 8: Capstone: evidence over impressions (20 minutes)

Evaluate on multiple cases, retain failures, and save prompt versions. Temperature behavior depends on the model; lower values do not guarantee truth or identical output.

**Task.** Write a reusable classifier prompt for Auth, Export, Upload, or Other. Include at least two examples, an ambiguity policy, and instructions to treat input as data. Include tests: A Google sign-in fails; B CSV contains only 100 rows; C uploading a PDF crashes; D please add dark mode. Request JSON with A/B/C/D. Specify how to compare baseline and revised prompts on fixed tests and one new edge case. You do not need to run the experiment.

**Submit.** Only your prompt. The AI evaluator returns scores, evidence, and improvement advice.

**After feedback.** Read the scores, evidence, and suggestions. Revise your prompt and retry when below 70.

**AI rubric (task-specific weights):**

- Defines labels, at least two consistent examples, and an ambiguity policy.
- Includes all four test inputs and the A/B/C/D JSON contract.
- Treats input as data and disallows instructions within it from changing the task.
- Plans a baseline/revision comparison on fixed tests and a meaningful new edge case.
