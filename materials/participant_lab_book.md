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

## Lab 3: Chain-of-thought (CoT): Multi-step Debugging (20 minutes)

Ask the model to reason step by step before giving the final answer. Reduces errors on logic, math, multi-step planning, and debugging.

**Task.** You are a developer whose site just crashed. You have a 50-line error log. If you ask an AI "what is the problem?", it often jumps to the first superficial warning it sees and gives a wrong solution, wasting hours. Write a prompt using the Chain-of-thought technique to force the AI to logically dissect the logs step-by-step before providing a final solution. Do not include the actual log; just write the prompt instructions.

**Submit.** Only your prompt. The AI evaluator returns scores, evidence, and improvement advice.

**After feedback.** Read the scores, evidence, and suggestions. Revise your prompt and retry when below 70.

**AI rubric (task-specific weights):**

- Prevent jumping to answer (30 points): Explicitly requests the model to not provide the final answer or solution immediately.
- Log analysis step (20 points): Instructs the model to first find and list the critical or fatal errors.
- Deduction step (20 points): Instructs the model to deduce the root cause from the found errors before giving a final single actionable solution.
- CoT Keywords (30 points): Uses explicit phrases like "Think step by step" or "Show your reasoning steps".

## Lab 4: Structured output: Relational JSON Shape (20 minutes)

Use visual structural shapes in your prompt to enforce strict output formats. Define foreign keys explicitly in the JSON shape.

**Task.** You have a transcript of a business meeting: "Ali, prepare the financial report by tomorrow. Sara, set up a meeting with the marketing team." Your project management backend requires a relational JSON structure where the "users" array and "tasks" array are separate, and tasks are linked to users via a foreign key ID. Write a prompt that extracts this information. You must explicitly draw the JSON shape in your prompt to show how to link the IDs (e.g., userId in users must match assignedTo in tasks). Do not provide the actual transcript, just the instructions.

**Submit.** Only your prompt. The AI evaluator returns scores, evidence, and improvement advice.

**After feedback.** Read the scores, evidence, and suggestions. Revise your prompt and retry when below 70.

**AI rubric (task-specific weights):**

- Visual JSON Skeleton (25 points): Provides an explicit visual template of the JSON containing the arrays "users" and "tasks".
- Strict Key Definition (25 points): The drawn template explicitly dictates the keys inside the objects (e.g. userId, name, taskDescription, deadline, assignedTo).
- Linking logic (30 points): Clearly defines the relationship between the user ID and the task assignedTo field (e.g., via inline comments in the template).
- Output restriction (20 points): Explicitly forbids any conversational text before or after the JSON.

## Lab 5: Tone control (Pure Negative Constraints) (15 minutes)

Simulate conversation (Iterative Refinement Flow) to fix model habits. If it outputs a bad tone, refine it iteratively instead of writing one perfect prompt.

**Task.** You are the editor of a neutral corporate newsletter. You want the AI to summarize a sensitive news story (e.g., a stock drop or a competitive event). The problem is the AI loves dramatic words ("disaster", "shocking") and sometimes inserts personal bias. Write a prompt to summarize the news using at least 3 negative constraints (must nots) to ensure the text is completely neutral, unbiased, and free of exaggerated words. Do not provide the actual news text, just the instructions.

**Submit.** Only your prompt. The AI evaluator returns scores, evidence, and improvement advice.

**After feedback.** Read the scores, evidence, and suggestions. Revise your prompt and retry when below 70.

**AI rubric (task-specific weights):**

- Assertiveness (25 points): Uses strong, unambiguous prohibitive language (e.g., "absolutely do not", "never").
- Bans emotional language (25 points): Explicitly forbids the use of dramatic, emotional, or exaggerated adjectives.
- Bans personal bias (25 points): Explicitly forbids personal opinions, analysis, or direct quotes.
- Format restriction (25 points): Specifies a negative format constraint (e.g., "do not use bullet points").

## Lab 6: Interview-style prompting (15 minutes)

System Architecture Design (for Devs). Complex designs (like a ride-hailing DB schema) depend on volume, real-time needs, and budget. Instead of a direct prompt, have the AI interview you as an architect.

**Task.** You want a highly personalized cover letter for a "Product Manager" role. A direct prompt yields generic robotic text. You want the AI to act as a "Career Coach" and interview you about your real past experiences. Write a prompt that instructs the AI to read a job description [job description text], interview you one question at a time to extract exactly 3 matching accomplishments, and then write the final cover letter once it has enough data. Submit only the prompt instructions.

**Submit.** Only your prompt. The AI evaluator returns scores, evidence, and improvement advice.

**After feedback.** Read the scores, evidence, and suggestions. Revise your prompt and retry when below 70.

**AI rubric (task-specific weights):**

- External Reference Context (30 points): Instructs the AI to base its questions on analyzing the provided job description.
- Single Question Rule (30 points): Explicitly limits the AI to asking exactly one question at a time and waiting for a reply.
- Stopping Condition Definition (20 points): Clearly defines when the interview should end (e.g., after collecting 3 matching accomplishments).
- Final Action Trigger (20 points): Instructs the AI to state a completion phrase (e.g., "I have enough data") and then output the final cover letter.

## Lab 7: Roles, chaining, and self-evaluation (20 minutes)

Code Self-Critique (for Developers). If the AI writes a script, it might miss edge cases. Force it to take a QA Role, evaluate its own code against a specific metric (e.g. Error Handling), and rewrite it.

**Task.** You are a logistics AI startup founder writing a short pitch email to an investor. An AI will normally use annoying exaggerated words and a begging tone. You must design a Prompt Chain. You cannot use a one-shot prompt. In one of the stages, force the AI to evaluate and critique its own text (Self-evaluation) to ensure all promotional words and begging tone are removed. Submit the prompts you would type in each stage (you must specify what you say in the first stage, how you force the model to confess its flaws in the second, and how you wrap it up in the final stage).

**Submit.** Only your prompt. The AI evaluator returns scores, evidence, and improvement advice.

**After feedback.** Read the scores, evidence, and suggestions. Revise your prompt and retry when below 70.

**AI rubric (task-specific weights):**

- Chain Separation (30 points): The participant clearly separates the workflow into 3 sequential prompts and does not combine them into one single request.
- Evaluation Metric Creation (20 points): The critique stage invents a specific evaluation metric or method (e.g., scoring from 1-10).
- Flaw Identification Mechanism (20 points): The critique stage forces the model to explicitly list out the specific flaws or banned words used.
- Chain Connection (30 points): The final rewrite prompt explicitly commands the AI to use the results/flaws from its own critique.

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
