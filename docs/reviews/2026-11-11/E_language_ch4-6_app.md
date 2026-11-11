# Language audit: Chapters 4-6, Appendices A-G, generated tables

Scope: thesis/chapters/04_results.tex, 05_policy.tex, 06_conclusion.tex, appendix_a to appendix_g, and every generated table and figure note they include. I read every sentence of Chapters 4-6 and Appendix C. I read the other appendices for language and label consistency. I also skimmed Chapters 1-2 and parts of Chapter 3 for terms. I made no edits.

Line numbers are those of the files at HEAD 226a515. Quotes are exact source text and can be found with grep (LaTeX macros kept).

---

## Overall assessment

**Chapter 4.** This is the strongest chapter. Numbers carry one standard error and a table reference, and "detectable" is used as the house convention defines it. Several mechanical results are admitted where they arise: the 90+ denominator, stacking set by routing, platform count tied to capacity, and zero access meaning no BNPL. Two things weaken it. First, the central mechanism, an effect concentrated in households whose income does not cover food and rent, is reported as something the model found, although the rules largely decide it. Second, the answer section reports peer-influence results (volume and stacking rise, default does not) as findings, when the first part is true by construction. There is also some wording drift (91 vs 98 days) and some repetition across 4.1, 4.2, 4.4 and 4.7.

**Chapter 5.** It is clear and properly hedged on bureau visibility. It reports the multiple-comparison odds for the quintile results, which is good practice. Its main finding, that screening removes about as much default as BNPL adds, is close to an identity of the design, and the answer states it as a result. The rise in refusals under visibility is mechanical and is not called so. Two "so"/"because" clauses do not follow from what precedes them. The "no Rand amount" limitation is stated three times across Chapters 5 and 6.

**Chapter 6.** The voice is plain and short. Most of the RQ2 and RQ3 paragraphs repeat Chapter 4 and 5 sentences almost word for word and add nothing. Two RQ1 phrases claim more than the evidence supports ("of the right order" for about half the book; "tests stability" for a profile whose stationarity is partly built in). One RQ3 sentence is hard to parse.

**Appendix C.** It is careful and well indexed. The cap-definition paragraph is hard to follow, and its numbers look as if they contradict Table tab:cap. There are a few pronoun and connector slips, and two strength-of-claim slips: "not detectable" for differences below 0.25 points, and "do not differ from zero".

**Other appendices.** The language is mostly clean. The problems are terminology drift ("robustness arm" vs "sensitivity", "reseeded" vs "redrawn", "agents" vs "households", "streak rule" vs "earlier default rule"), two overclaims in the register ("flat", "pre-registered"), and several notation collisions in Appendix F.

AI tells are rare. I found no em dashes, no "However/Moreover/Notably/Importantly" openers, and none of the "crucial/landscape/robust/nuanced/leverage/underscore/highlight/delve" words. The tells I list below are mild: a few colon-reveal sentences, an announcing sentence, and "These findings identify".

---

## Glossary of terms as actually used (Chapters 4-6 and appendices)

| Concept | Term(s) used | Deviations / double uses |
|---|---|---|
| Outcome: household with an instalment past the threshold | **default** (arrears age >= 7 ticks) | Threshold worded four ways: "more than 90 days past due" (Ch1, Ch2), "91 or more days past due/behind" (04:23, 06:24, appC:110), "reached 98 days" (04:25), "the 90-day convention/construct" (Ch2 table, 06:41, appA:42). See C4-M3. |
| Default measures | **default during the run**; **default including the starting stock**; **default rate**; **population default** | tab_scenarios defines "Default rate" as "share of all households in default at the final tick", which is the same as "including the starting stock" only because default is permanent. That is fine, but give one definition. |
| Arrears level measure | **90+ share** (credit-active households > 90 days) | 04:37 introduces a second measure, "share of all households more than 90 days in arrears", under no name. Name it (e.g. "90+ share of all households"). |
| Food and rent not paid | **consumption distress** (Ch1, Ch2, appC:181, appF:74); **short of food and rent / short in a tick / ever short** (Ch4, Ch5, Ch6, tab_scenarios_distress); **food and rent left unpaid** (caption) | The defined term "consumption distress" never appears in Ch4-6. Either use it, or say once in Ch4 that "short of food and rent" is the consumption-distress measure. |
| Experimental arms | **baseline** (BNPL off); **benchmark** (BNPL on, no switch); **reference** / "reference settings" / "reference rules" (sensitivity reference arm); **control** (beta = 0, gamma = 0) | These are used consistently. "reference settings" (tab_effect) vs "reference rules" (appC:140) is minor. |
| Model lender of BNPL | **platform** | "provider" is used for real firms (good), but appA:63 says "\ac{BNPL} providers apply" for the model's platforms, and tab_bnpl_on_checks row "Owing two or more providers at once" has a model column about platforms. |
| Model unit | **household** | "agents" in appC:120, appC:184, appB spec:35 ("Agents treat current income as persistent"), appD (deliberate for resampled records), Ch3:394. "users" in 04:83, 04:248. "borrowers" only for CFPB (good). |
| Time step | **tick** | Consistent. "fortnight" is used only to justify the tick (good). |
| Peer channel | **peer influence** (beta, gamma); **peer adoption** (RQ2); **peer signal** (appG); **peer channel** (appC:70); **social channel** (appC:187) | "social channel" appears once. Use "peer channel". |
| Real reporting change | **reporting arrangements** | Consistent. |
| Model switch | **bureau visibility** / "visibility" | Consistent. |
| Regulation 23A on BNPL | **mandatory screening** / **screening** (switch) | "screen" is also the platforms' **light screen** (eligibility, order cap, limit). The two are close in wording. Ch5 is clear enough, but avoid bare "the screen". |
| Lender's test | **Regulation 23A test**; **gate** (appC, appG); **affordability test(s)** (appC:142); **affordability check** (FCA) | Acceptable. |
| Policy arms | **switch** (visibility, screening); **lever** (cooling-off, cap) | Ch2 table row 15 "Scenario switches" includes the window and the cap. appC fig caption "Every lever" includes the switches. appC:6 "the two levers of Section 5" is ambiguous (see AC-M1). |
| Platform cap | **cap on platforms owed**; **platform cap** (Ch2); **the cap** | Consistent. Code name `stacking_cap` only in the register (fine). |
| Owing >= 2 platforms | **stacking** / **owing two or more platforms** / **stacking depth** | Consistent. |
| Sensitivity runs | **sensitivity analysis / level sensitivity / effect sensitivity** (Ch3, Ch4) | **robustness arm** in the appendices (appB register:39, 61, 117, 119; appF:7, 94, 95, 101; appG:129, 130, 190). Pick one. |
| Activation | "newly randomised order each tick" (Ch2), "redrawn each tick" (Ch2 table, appB:119, appG:4) | "reseeded every tick" (appC:70) and "random, reseeded each tick" (tab_robustness_appendix) are technically wrong: the order is redrawn, the generator is not reseeded. |
| Earlier default rule | "the earlier default rule" (appC:25) | "streak rule" (appB register:65, 81; appF:73, 91, 97). Introduce "streak rule" once in appC:25. |
| Shortfall routes | **shortfall path** / **want-driven path** | Consistent. Table row "no \ac{BNPL} for shortfalls" vs prose "kept out of the shortfall path" / "Without shortfall \ac{BNPL}" (appC:126) is acceptable. |

---

## Chapter 4 (04_results.tex)

### HIGH

**C4-H1. tautology (by construction, partly admitted), HIGH.** 04:22-28, repeated at 04:252-253, 06:25-27 and appC:120.
Quote: "The effect runs through households that use \ac{BNPL} to bridge cash shortfalls" and "Most of these households are the 3.6\% whose surveyed"
- **What is wrong.** For the 3.6% group the result is largely fixed by the rules, but the text reports it as a mechanism the model found.
- **Which assumptions make it mechanical.** (a) Submodel 2: committed spending cannot be cut, so a household whose surveyed income is below food and rent is short in every tick. (b) Submodel 5: BNPL is used first on a shortfall. (c) Submodel 12: the platforms' screen does not test affordability, while the Regulation 23A lender refuses these households. (d) Default at seven ticks: their income cannot pay the three later instalments.
- **What follows.** Ch3:405-406 reports that 85% of the at-risk members default with BNPL against 47% without. Given (a)-(d), that gap is close to an accounting consequence.
- **What the text admits.** 04:29-30 admits that the lighter screen is why the lender's refusals fall. 06:26-27 admits "to whom the platforms' light screen lends where the Regulation 23A test would not". Neither says the outcome for this group is close to determined by the rules.
- **Rewrite (after 04:28).** "For this group the result follows largely from the rules. Their income does not cover food and rent, so they are short in every tick. The platforms lend to them where the Regulation 23A test would not, and their income cannot pay the later instalments. With \ac{BNPL}, 85\% of those who can default during the run do so, against 47\% without (Section~\ref{sec:data-validation})."
- **Rewrite (06:25-27).** "Most of it comes from the 3.6\% of households whose surveyed income does not cover their food and rent. The platforms lend to them where the Regulation 23A test would not, and the rules leave them little chance to repay."

### MED

**C4-M1. tautology (by construction, not admitted in the answer), MED.** 04:250-251 and 06:20-22.
Quote: "Peer influence under either adoption rule raises" (04:250); "although households borrow 2.4" (06:21)
- **What is wrong.** By Equation eq:peer and the threshold rule, beta and gamma raise the purchase probability, so higher volume is true by design.
- **Stacking.** Higher stacking follows from more frequent borrowing under random routing, which 04:89-97 admits.
- **The null on default.** 04:71-72 explains this correctly ("$\beta$ acts only on want-driven purchases"). Given that the shortfall path carries the effect and beta never touches it, the null is expected from the design.
- **Effect of the wording.** "although" in Ch6 presents an expected result as a surprise.
- **Rewrite (04:250-252).** "Peer influence raises volume and stacking, as it must, since it raises the purchase probability. It does not change the effect detectably ($+0.003 \pm 0.010$ points per 0.1 of $\beta$), because it acts only on want-driven purchases and the effect runs through the shortfall path."
- **Rewrite (Ch6).** "The effect does not change detectably with $\beta$ between 0 and 0.3 ($+0.003 \pm 0.010$ points per 0.1). Peer influence acts only on want-driven purchases, and the effect does not run through them."

**C4-M2. tautology (accounting identity reported as a sensitivity result), MED.** 04:187-189.
Quote: "The level of default is set mainly by the definition of default and the starting profile" and "households placed in default at the start are 6.36 of the 20.73 points"
- **What is wrong.** The second sentence shows only that the measure includes the starting stock by definition. No arm varies the starting profile.
- **Admission.** The 56-day half of the claim is a real sensitivity result, and 04:190-193 admits it is partly definitional. The starting-profile half is not admitted as definitional.
- **Rewrite.** "The level of default rests mainly on the definition of default. The households placed in default at the start make up 6.36 of the 20.73 points by construction. Defining default at 56 days in place of 98 raises it by $13.13 \pm 0.13$ points."

**C4-M3. terminology (threshold stated two ways in adjacent sentences), MED.** 04:23 and 04:25. The same wording recurs at 06:24 and appC:110.
Quote: "and then fall 91 or more days behind on it" and "\ac{BNPL} instalment reached 98 days"
- **What is wrong.** Default is seven ticks, or 98 days (Ch2:195). "91 or more" is true only at tick resolution, and a reader sees two thresholds for the same event two lines apart.
- **Rewrite.** "and then fall seven ticks (98 days) behind on it". Use the same wording in 06:24 and appC:110 ("when an instalment on any facility is seven ticks, or 98 days, past due").

**C4-M4. clarity / grammar (comparison misstated), MED.** 04:142-144.
Quote: "With $\gamma=0.3$ it" / "raises holding at full access by 14 to 34 points, against 10 at $\gamma=0$, and default by 0.89"
- **What is wrong.** The numbers are zero-to-full-access changes (Table tab:access), so the threshold rule itself does not "raise holding by 14 to 34 points". "it" also points back to "The threshold rule".
- **Rewrite.** "Under the threshold rule with $\gamma=0.3$, moving from zero to full access raises holding by 14 to 34 points, against 10 at $\gamma=0$, and default by 0.89 to 1.09 points, against 0.94 at $\gamma=0$."

**C4-M5. statistics-language / clarity (non sequitur and no test), MED.** 04:146-148.
Quote: "Volume under the threshold rule is 1.3 to 4.4 times the control's, so"
- **What is wrong.** A volume ratio cannot imply that the effect on default is unchanged. The claim also needs a contrast between each threshold arm's default change and the control's, and none is given (0.89 to 1.09 against 0.94, with no standard error).
- **Rewrite.** "Volume under the threshold rule is 1.3 to 4.4 times the control's. No threshold arm's change in default differs from the control's by more than two standard errors [give the largest difference $\pm$ SE]. Peer influence under either rule therefore raises \ac{BNPL} use without changing the effect on default detectably."

**C4-M6. statistics-language (claim without the test), MED.** 04:233-236. The same applies to 04:226.
Quote: "Purchase size does not move the effect detectably."
- **What is wrong.** "Detectably" needs the standard error of the difference between two effects, and only each effect's own standard error is given.
- **Rewrite.** "Halving or doubling $\kappa$, which halves or doubles volume, leaves the effect between 0.89 and 1.09 points at both values of $\beta$, within [x] points of the reference, less than two standard errors of the difference."
- **If that SE is not computed.** Say "leaves the effect between 0.89 and 1.09 points, against 0.98 and 1.07 in the reference" and drop "detectably".

**C4-M7. statistics-language (detectability of the remainder not stated), MED.** 04:253-254. The same omission is at appC:120.
Quote: "others it is $+0.11 \pm 0.07$ points at $\beta=0$ and $+0.18 \pm 0.08$ at $\beta=0.3$."
- **What is wrong.** Ch3:408-409 says the first is not detectable and the second is. The answer drops this, so a reader cannot tell whether BNPL affects the other 96.4% at all.
- **Rewrite.** "...among the others it is $+0.11 \pm 0.07$ points at $\beta=0$, not detectable, and $+0.18 \pm 0.08$ at $\beta=0.3$, which is."

**C4-M8. statistics-language ("detectably" applied to Sobol indices), MED.** 04:193-199.
Quote: "the variance decomposition, only the separation rate moves default detectably: its first-order" and "0.03 of zero, so none of them changes default detectably over its range"
- **What is wrong.** The house convention defines "detectable" for a difference beyond two standard errors. These are variance shares with bootstrap intervals and a noise correction, so using the word here stretches the convention.
- **Rewrite.** "Of the six parameters of the variance decomposition, only the separation rate accounts for a share of the variance of default distinguishable from zero: its first-order index is 0.84 ($\pm 0.15$, 95\% bootstrap interval)." End the paragraph with: "with noise removed, each of the five is within 0.03 of zero."

**C4-M9. clarity / tautology (unexplained and partly mechanical result), MED.** 04:174-176.
Quote: "Platform limits bind more often on poorer households: a limit reduces or refuses a fifth of" and "Raising the limit tenfold lowers population"
- **What is wrong (first sentence).** The limit is $\lambda$ times monthly income, so it is lower for poorer households by construction. The pattern is also not monotone (Q3 14.9%, Q4 16.0%).
- **What is wrong (second sentence).** It reports a detectable fall in default from a looser limit with no reason given. A reader expects more BNPL to mean more default, and the paragraph leaves the sign unexplained.
- **Rewrite.** "Limits are set as a multiple of income, so they bind more often on poorer households: a limit reduces or refuses 21\% of platform requests in Q1 and 20\% in Q2, against 13\% in Q5. Raising the limit tenfold lowers population default by $0.28 \pm 0.12$ points (Table~\ref{tab:robustness-appendix}), [one sentence on why, e.g. a larger agreement relieves more of a shortfall before the household reaches the lender]."

**C4-M10. grammar / clarity, MED.** 04:27.
Quote: "Most of these households are the 3.6\% whose surveyed"
- **What is wrong.** The new defaulters cannot "be" the 3.6%. They belong to it. "Most" is also vague when Ch3:406-407 gives about 0.9 of the 1.08 points.
- **Rewrite.** "About 0.9 of the 1.08 points come from the 3.6\% of households whose surveyed income does not cover their food and rent (Section~\ref{sec:data-validation})."

**C4-M11. statistics-language / overclaim, MED.** 04:86. The same claim is in tab_bnpl_on_checks:18.
Quote: "point in the two years, close to the \ac{CFPB}'s 32 to 33\% of borrowers in a"
- **What is wrong.** A two-year share of 28% sits below a one-year share of 32-33%. Over a matched window the model would be further below, so "close to" overstates the agreement. The figure note (04:117) admits the window difference, but the prose does not.
- **Rewrite.** "...and 28\% of ever-holders do so at some point in the two years, against the \ac{CFPB}'s 32 to 33\% of borrowers in one year~\citep{cfpb2025bnpl}."
- **Table.** Change "Close; different market" to "Below, over a longer window; different market".

**C4-M12. tautology (repetition across sections), MED.** The opening sentence of 4.3 is repeated in the answer and the conclusion.
Quote (04:83): "Owing several platforms at once is common among users"; (04:248): "Owing several platforms at once is common among users, at a rate set mostly by the assumed"; (06:18): "Owing several platforms at once is common, at a rate set by the routing"
- **What is wrong.** The same sentence appears three times. "common" is vague when 22% and 28% are available, and "mostly" (04) vs no qualifier (06) changes the strength of the claim.
- **Rewrite (04:83).** "With four platforms and no peer influence, 22\% of holders owe two or more platforms at the final tick..." Start with the number and drop the general sentence.
- **Rewrite (04:248).** "28\% of ever-holders owe two or more platforms at some tick, a share set by the assumed routing rule and by how often households borrow."
- **Ch6.** Shorten to a clause.

**C4-M13. tautology (reported four times), MED.** The beta-null on default is reported at 04:46-48 (20 seeds), at 04:63-70 (250 seeds), at 04:146-148 (threshold rule) and in the answer at 04:250-252.
Quote: "yet the effect on default does" (04:47)
- **What is wrong.** 4.1 anticipates 4.2 with a weaker estimate, and "yet" sets up a contrast that 4.2 then explains.
- **Rewrite.** Cut 04:46-48 to "At $\beta=0.3$ volume is 2.4 times that at $\beta=0$ (Section~\ref{sec:results-beta} reports the effect on default)." Keep the lending sentence.

**C4-M14. tautology (mechanical, admitted, but worded as a finding), MED.** 04:29-31.
Quote: "lighter than the Regulation 23A test, so the lender's refusals fall from 2{,}796 to 970 over the"
- **What is wrong.** The fall is mainly fewer applications reaching the lender, because BNPL is tried first (Submodel 5). The "so" is right, but the sentence credits the lighter screen. Applications should be the subject.
- **Rewrite.** "\ac{BNPL} is tried before the traditional lender (Submodel~5), and the platforms lend where the Regulation 23A test would not, so fewer requests reach the lender and its refusals fall from 2{,}796 to 970 over the run."

### LOW

**C4-L1. grammar, LOW.** 04:13.
Quote: "raises default during the run from 14.37\% (20.73\% including the starting stock) by"
- **What is wrong.** "raises ... from X ... by Y" with a parenthesis in between is hard to parse.
- **Rewrite.** "Without \ac{BNPL}, default during the run is 14.37\% (20.73\% including the starting stock). Enabling \ac{BNPL} raises it by $1.08 \pm 0.11$ points at $\beta=0$ and $1.12 \pm 0.11$ at $\beta=0.3$."

**C4-L2. clarity, LOW.** 04:14.
Quote: "Pooled by precision over four seed blocks"
- **What is wrong.** The reader is not told which blocks, and "by precision" is loose.
- **Rewrite.** "Weighted by inverse variance over four seed blocks (Tables~\ref{tab:baseline-arms}, \ref{tab:access} and~\ref{tab:effect} and the threshold control), whose estimates run from 0.94 to 1.08 points..."

**C4-L3. clarity / grammar, LOW.** 04:24.
Quote: "replicates the rise at $\beta=0$ is 1.07 points, of which 0.94 are households"
- **What is wrong.** Points are not households. "ten replicates" does not say which ten, beside the 20-replicate figure of 1.08 two lines earlier. The 0.94 here (by channel) is also easy to confuse with Ch3's "about 0.9" (by group).
- **Rewrite.** "On the first ten seeds of that block the rise at $\beta=0$ is 1.07 points. Of these, 0.94 points come from households whose oldest unpaid \ac{BNPL} instalment reached seven ticks, and 0.13 from traditional arrears."

**C4-L4. grammar, LOW.** 04:35.
Quote: "from 13.98\% to 12.46\% at $\beta=0$, because \ac{BNPL} holders join the denominator, so we use it"
- **What is wrong.** "because ... so" chains two connectors in one clause. The admission itself is good.
- **Rewrite.** "...falls with \ac{BNPL}, from 13.98\% to 12.46\% at $\beta=0$, because \ac{BNPL} holders join the denominator. We therefore use it for the level against the \ac{CCMR} and not for effects."

**C4-L5. grammar (unit missing; source shift), LOW.** 04:39.
Quote: "The share with no liquid savings rises by $0.17 \pm 0.04$."
- **What is wrong.** The unit is missing. The figure also comes from the 20-seed block, while the previous sentence uses 250 seeds.
- **Rewrite.** "On the seeds of Table~\ref{tab:baseline-arms}, the share with no liquid savings rises by $0.17 \pm 0.04$ points."

**C4-L6. clarity / number contradiction, LOW-MED.** tab_baseline_arms:18 vs Ch3:395.
Quote: "No liquid savings (\% of households) & 19.1 (0.2)" vs "and 45.2\% have no liquid savings"
- **What is wrong.** A reader meets 45.2% in Ch3 and 19.1% in Table 4.1 with no bridge. The first is at the start and the second is a post-burn-in average after households save.
- **Rewrite.** Add to the table note: "No liquid savings: post-burn-in average; 45.2\% have none at the start (Section~\ref{sec:population})."

**C4-L7. clarity, LOW.** 04:59-61 (47 words).
Quote: "The effect would count as non-linear only if a quadratic or a hinge at"
- **Rewrite.** "We fixed the reporting rule before the runs. The effect counts as non-linear only if a quadratic term, or a hinge at $\beta=0.1$, is more than two standard errors from zero and changes a conclusion at some value of $\beta$. Otherwise we report the effect at $\beta=0$ and a slope."

**C4-L8. AI-tell (colon reveal), LOW.** 04:68 and 04:71-72.
Quote: "Peer influence changes how much households borrow without" and "the shortfall path: $\beta$ acts only on want-driven purchases."
- **Note.** These are mild. "how much households borrow" should say BNPL, since traditional lending does not change.
- **Rewrite.** "From $\beta=0$ to $\beta=0.3$, \ac{BNPL} volume per eligible household rises from R862 to R2{,}014 a year, and the share of ever-holders who stack from 28\% to 70\%. The effect does not change detectably. This is expected, since $\beta$ acts only on want-driven purchases and the effect runs through the shortfall path."

**C4-L9. clarity, LOW.** 04:91-92.
Quote: "probability $3/4$, so a household that borrows often soon owes two platforms"
- **What is wrong.** 3/4 holds only when the household owes exactly one of four platforms.
- **Rewrite.** "...a household that owes one of the four platforms sends its next request first to another with probability $3/4$..."

**C4-L10. vague quantifier, LOW.** 04:96.
Quote: "seeds and with about the same volume"
- **Rewrite.** "...on the same seeds and with volume within 3\% (Table~\ref{tab:effect})."

**C4-L11. clarity, LOW.** 04:169-170.
Quote: "discretionary budgets, so the mean purchase rises from R108 in Q1 to R1{,}911 in Q5, and Q5,"
- **What is wrong.** Two "and"s, and "rise" is ambiguous (purchase or default).
- **Rewrite.** "Purchases are sized on discretionary budgets, so the mean purchase rises from R108 in Q1 to R1{,}911 in Q5. Q5 has the largest purchases and no detectable rise in default."

**C4-L12. clarity / wrong word, LOW.** 04:185.
Quote: "Every result belongs to the two-year horizon."
- **Rewrite.** "Every result holds for the two-year horizon only." Or move it to the opening of Section 4.

**C4-L13. grammar, LOW.** 04:189 and 04:193.
Quote: "households placed in default at the start are 6.36 of the 20.73 points"
- **What is wrong.** Households are not points.
- **Rewrite.** "...households placed in default at the start account for 6.36 of the 20.73 points". Apply the same fix at 04:193: "1.81 points come from households placed in default at the start".

**C4-L14. ambiguity, LOW.** 04:203-204.
Quote: "points while the" / "\ac{BNPL} share of a shortfall is capped."
- **What is wrong.** "while" reads as temporal or concessive.
- **Rewrite.** "...lowers default by $0.51 \pm 0.14$ and $0.39 \pm 0.15$ points, with the \ac{BNPL} share of a shortfall capped."

**C4-L15. clarity (pronoun / scope of range), LOW.** 04:226-228.
Quote: "The effect is detectable under every setting but one, at both values of $\beta$, and lies between" and "so such counts"
- **What is wrong.** The range excludes the one setting, and "such counts" has no clear referent.
- **Rewrite.** "The effect is detectable under every setting but one, at both values of $\beta$. Excluding that setting, it lies between 0.79 and 1.18 points. The settings share the block and often a no-\ac{BNPL} arm, so the number of detectable settings is not a count of independent replications."

**C4-L16. tautology (by construction, admitted in 4.4), LOW.** 04:254.
Quote: "Default rises with access, with no sign of a"
- **Note.** 04:125-127 says the access rows are the BNPL effect by another name, and the answer could say so.
- **Rewrite.** "Default rises with access, which is the \ac{BNPL} effect phased in, with no sign of a jump."

**C4-L17. repeated limitation, LOW.** The point that the shortfall-path assumptions are unmeasured is stated at 04:242-243 ("No study measures either for South Africa"), at 04:259-260 ("which is not measured for South Africa"), at Ch2:231 and at appC:126.
- **Fix.** Keep 04:242-243 and cut the clause at 04:259-260 to "The size of the effect depends most on whether households can borrow with \ac{BNPL} against a shortfall (Section~\ref{sec:results-effect})."

**C4-L18. number style, LOW.** 04:174 "a fifth" sits beside "13\%".
- **Fix.** Use 21% and 20% (see C4-M9).

**C4-L19. table/prose consistency, LOW.** tab_baseline_arms:28-29.
Quote: "Holders at the final tick (\%) & -- &" vs "Ever-holders, at any tick (\%) & 0.0 (0.0)"
- **What is wrong.** The same no-BNPL column shows a dash in one row and a zero in the next.
- **Fix.** Use "--" for both. The fig_stacking note says "Both shares are zero with one platform" while tab_stacking shows "--". Pick one convention.

**C4-L20. table label, LOW.** tab_effect:26.
Quote: "Routing and the shortfall path (Submodels 5, 7 and 13)"
- **What is wrong.** Submodel 7 (default) belongs to no row in this group.
- **Fix.** "(Submodels 5 and 13)".

**C4-L21. table note, LOW.** tab_access:7.
Quote: "given only where the change in default is detectable"
- **What is wrong.** Every row is detectable, so the clause does nothing.
- **Fix.** Delete it or say "every change is detectable".

**C4-L22. acronym consistency, LOW.** tab_robustness:25 "(IES-derived)" is plain text, while the body uses \ac{IES}.

---

## Chapter 5 (05_policy.tex)

### HIGH

**C5-H1. tautology (by construction, mechanism described but not called mechanical), HIGH.** 05:63-71, 05:102-103 and 06:31.
Quote: "and volume by about 3\%, so it lowers default by about as much as" (05:69); "Mandatory screening lowers default by 0.93 to 1.03 points, almost all in the poorest" (05:102); "lowers it by 0.93 to 1.03 points, about as much as \ac{BNPL} adds" (06:31)
- **What is wrong.** The offset is close to an identity of the design:
  - The BNPL effect is carried by households that the Regulation 23A test refuses (C4-H1).
  - Screening applies that same test to their BNPL requests.
  - A refused shortfall request passes in full to a lender that applies the test again (05:65-67), so those households return to their no-BNPL position.
  - "Default under screening ... is close to the 20.73\%" (05:70-72) is the expected outcome.
- **What the text admits.** 05:64-67 explains the route well but does not say the result follows from it. The answer and the conclusion present it as a policy finding.
- **The "so" at 05:69.** It does not follow from a small fall in holding.
- **Rewrite (after 05:68).** "This offset follows largely from the design. The households that carry the effect are those the Regulation 23A test refuses, and screening applies that test to their \ac{BNPL} requests. Screening lowers \ac{BNPL} holding by 0.3 points at $\beta=0$ and 0.7 at $\beta=0.3$, and volume by about 3\%. It therefore removes most of the effect while leaving 97\% of \ac{BNPL} volume in place."
- **Rewrite (answer, 05:102-103).** "Mandatory screening lowers default by 0.93 to 1.03 points, about as much as \ac{BNPL} adds, because it applies to \ac{BNPL} the test that the households carrying the effect fail."

### MED

**C5-M1. tautology (mechanical, not admitted), MED.** 05:37 and 05:99-100.
Quote: "Once the lender sees \ac{BNPL} instalments, it refuses about 13\% more applications and lends"
- **What is wrong.** Visibility only adds obligations to the residual-income test (Algorithm alg:gate), so refusals cannot fall. The size (13%) is a result, but the direction is fixed.
- **What the text admits.** 05:57-59 ("may favour") concerns default, not refusals.
- **Rewrite.** "Visibility can only add obligations to the test, so refusals rise. They rise by about 13\%, and lending falls by 12 to 15\%."

**C5-M2. tautology / statistics-language (understated admission), MED.** 05:57-61.
Quote: "The model's rules may favour this result." and "assesses surveyed rather than current income." and "so the result gives the direction of the"
- **What is wrong.** "this result" has no clear referent, since the paragraph follows the volume sentence. "may favour" understates an asymmetry the text itself spells out.
- **Surveyed income.** The text does not say in which direction surveyed income pushes the result.
- **"gives the direction".** This is stronger than the paragraph supports, since the rules "favour" that direction.
- **Rewrite.** "The model's rules push the visibility result upward. A refusal can put a household into arrears at once, whereas a granted loan is repaid over 25 months, partly after the run ends. The lender also assesses surveyed income, which [raises/lowers] [what]. The switches were not run under the other rules of Table~\ref{tab:effect} or over a longer horizon, so the rise in default holds only under the reference rules and is not a forecast."

**C5-M3. clarity (substantive caveat buried in a 44-word sentence), MED.** 05:38-40.
Quote: "and a quarter of it is on agreements opened in the same tick against the same shortfall, which a bureau"
- **What is wrong.** "it" is ambiguous, and the implication is unstated: a quarter of what the lender sees would not be visible under a real reporting lag, so the switch overstates visibility.
- **Rewrite.** "What the lender sees is mostly live instalments. Arrears and late fees are 9.9\% of the visible obligation at application. A quarter of the visible obligation is on agreements opened in the same tick against the same shortfall, and a bureau reporting with a lag would not show it. The switch therefore overstates what a lender would see."

**C5-M4. clarity (wrong causal link), MED.** 05:52-53.
Quote: "\ac{BNPL} volume falls by 1.3 to 1.5\%, because the switch acts on traditional lending and not on"
- **What is wrong.** The "because" explains why the fall is small, not why volume falls.
- **Rewrite.** "\ac{BNPL} volume falls by only 1.3 to 1.5\%, because the switch acts on traditional lending and not on \ac{BNPL} requests."

**C5-M5. statistics-language (difference in detectability read as a difference), MED.** 05:100-102. The same issue is at 05:19-20.
Quote: "the model refused households have nowhere else to borrow; with peer influence the rise is not"
- **What is wrong.** The answer implies that peer influence removes the visibility effect. 05:85-86 shows the two estimates do not differ detectably ($-0.09 \pm 0.08$).
- **Rewrite.** "...raises default by $0.20 \pm 0.07$ points without peer influence. With peer influence the rise, $0.10 \pm 0.06$, is not detectable, but it does not differ detectably from the rise without."

**C5-M6. tautology (limitation stated three times), MED.** 05:75-76, 05:105-106 and 06:32-33. It is also in the tab_scenarios_distress note.
Quote: "record only whether households are short of food and rent, with no Rand amount"; "unpaid, so neither result shows whether households end up better or worse off."; Ch6 "record how much goes unpaid, so the results do not show whether households are better off."
- **Fix.** Keep it once, at 05:75-76. In the answer write "...at $\beta=0.3$ only visibility does. Neither result shows whether households end up better off (Section~\ref{sec:scenarios})." Drop the clause from Ch6.

**C5-M7. vague quantifier, MED.** 05:63 and 05:102.
Quote: "Almost all of screening's fall in default is in Q1"
- **What is wrong.** A number is available, but the sentence mixes quintile points and population points. Q1's 4.68-point fall in a fifth of households is about 0.94 population points, against a total of 0.93.
- **Rewrite.** "Screening's fall in default is in Q1: $-4.68 \pm 0.10$ points at $\beta=0$ and $-4.70 \pm 0.10$ at $\beta=0.3$, about 0.94 points of population default, against a \ac{BNPL} effect in Q1 of about four points."

### LOW

**C5-L1. causal language, LOW.** 05:100-101 and 06:30.
Quote: "because in the model refused households have nowhere else to borrow"
- **What is wrong.** This is the mechanism by which the rules produce the rise, and no arm tests it (no fallback arm).
- **Rewrite.** "...since in the model a refused household has no other source of credit". This states the rule, not a tested cause.

**C5-L2. pronoun, LOW.** 05:67.
Quote: "Its refusals rise by 1{,}827"
- **Rewrite.** "The lender's refusals rise by 1{,}827, close to their level without \ac{BNPL}."

**C5-L3. completeness, LOW.** 05:85-86.
Quote: "($-0.09 \pm 0.08$ points for bureau visibility)"
- **What is wrong.** The sentence says "either switch" but gives only one contrast.
- **Fix.** Add the screening contrast and its standard error from results_numbers.json (I have not looked the value up).

**C5-L4. number consistency, LOW.** 05:93 "up to 41\%" vs appC:224 "40.5\%" and tab_cooloff "-40.5".
- **Fix.** Use 40.5% or "about 40%" in both places.

**C5-L5. vague quantifier, LOW.** 05:72 "slightly more households".
- **Fix.** The numbers follow, so "Screening leaves more households short of food and rent" is enough.

**C5-L6. grammar / ambiguity, LOW.** 05:46.
Quote: "the food and rent the loan would have paid first go unpaid"
- **Rewrite.** "and the food and rent that the loan would have paid go unpaid."

**C5-L7. table unit, MED.** tab_scenarios:20 and 32.
Quote: "\ac{BNPL} volume (R m) & 5.44 & $\boldsymbol{-1.3 \pm 0.6}$"
- **What is wrong.** The row unit says R m, but the changes are in per cent. The note explains it, but a reader scanning the table will read $-1.3$ R m.
- **Fix.** Use the row label "\ac{BNPL} volume (R m; change in \%)". Also change the note's "in per cent" to "in \%" to match the house style.

---

## Chapter 6 (06_conclusion.tex)

### MED

**C6-M1. tautology (near-verbatim repetition of the Ch4 and Ch5 answers), MED.**
Quote: 06:23-24 "to bridge cash shortfalls and then fall 91 or more days behind on it" (= 04:22-23); 06:30 "influence, because in the model refused households have nowhere else to borrow, and screening" (= 05:100-101); 06:31 "about as much as \ac{BNPL} adds" (= 05:103); 06:18 (= 04:248)
- **What is wrong.** The RQ2 and RQ3 paragraphs add no content beyond the two answer sections.
- **Fix.** Make each RQ paragraph two or three sentences that state the answer and its main condition. For example, RQ2: "Enabling \ac{BNPL} raises default by $1.03 \pm 0.06$ points. The rise comes almost entirely from \ac{BNPL} used against cash shortfalls by the 3.6\% of households whose income does not cover food and rent, and peer influence, routing and platform count do not change it detectably. How often households owe several platforms is set by the routing assumption."

**C6-M2. overclaim, MED.** 06:12-13.
Quote: "is of the right order for household debt"
- **What is wrong.** Ch3's table and appD:152 give total debt at 49% of the CCMR book ("About half"). "Of the right order" claims agreement the numbers do not show.
- **Rewrite.** "...and holds about half the household debt of the corresponding \ac{CCMR} book."

**C6-M3. tautology (overclaim on what is tested), MED.** 06:14-15.
Quote: "which tests stability and says nothing about how arrears arise"
- **What is wrong.** The run starts from the profile, the write-off rate is derived so that the 120+ stock is stationary, and two parameters are fitted to the bands. Part of the stability is built in, and only the final-tick 90+ share is untargeted. appC:114 calls it "a consistency check", which is the better wording.
- **Rewrite.** "The baseline keeps its calibrated arrears profile as a share while the credit-active book halves. Part of that stability is built into the calibration, and none of it shows how arrears arise."

**C6-M4. clarity (sentence must be read twice), MED.** 06:31-32.
Quote: "Visibility, and screening without" / "peer influence, leave slightly more households short of food and rent"
- **Rewrite.** "Visibility raises the share of households short of food and rent at both values of $\beta$, and screening raises it at $\beta=0$ only (Table~\ref{tab:scenarios-distress})."

**C6-M5. wrong word / overclaim, LOW-MED.** 06:21-22.
Quote: "although households borrow 2.4"
- **What is wrong.** Only BNPL volume is 2.4 times as large, and traditional lending does not change. The figure comes from the 20-seed block, while the slope beside it comes from 250 seeds (ratio 2.3).
- **Rewrite.** "...although \ac{BNPL} volume is more than twice as large at 0.3." Better still, see C4-M1.

### LOW

**C6-L1. AI-tell (announcing / overclaim), LOW.** 06:35.
Quote: "These findings identify where better data would most improve the analysis"
- **What is wrong.** The findings do not identify anything. The author does.
- **Rewrite.** "Better data would most improve four inputs: how much South African households borrow with \ac{BNPL} when short of cash and who they are, the size and frequency of \ac{BNPL} purchases, how households choose among providers, and where refused households borrow instead, including from informal lenders."

**C6-L2. AI-tell (announcing), LOW.** 06:41.
Quote: "The conclusions have further limits."
- **Fix.** Cut it and start with "Default follows the bureau's 90-day construct, but its level rests on...".

**C6-L3. topic sentence missing, LOW.** 06:48.
Quote: "A rule linking reported \ac{BNPL} behaviour to credit scores, pricing"
- **What is wrong.** The paragraph is a list of extensions with no lead.
- **Fix.** Add "Five extensions would test the results most directly." Ch2:159 also points readers to "the final paragraph" for the scoring extension, so the paragraph should be easy to find.

---

## Appendix C (appendix_c_supplementary.tex)

### MED

**AC-M1. clarity (ambiguous label), MED.** appC:6.
Quote: "the two levers of Section~\ref{sec:scenarios}"
- **What is wrong.** Section 5's main arms are the two switches. The appendix holds the two further levers.
- **Rewrite.** "the two further levers that Section~\ref{sec:scenarios} reports in summary".

**AC-M2. statistics-language (overstated), MED.** appC:134.
Quote: "Differences below about 0.25 points are not detectable" and "smaller effects cannot be distinguished from none"
- **What is wrong.** Ch3 says a true 0.26-point change is missed about half the time. Smaller true differences are often missed but sometimes detected.
- **Rewrite (heading).** "Differences below about 0.25 points are often missed".
- **Rewrite (sentence).** "A true difference of 0.26 points would be missed about half the time, and smaller ones more often."

**AC-M3. clarity / apparent number contradiction, MED.** appC:231-238.
Quote: "Counting agreements in place of platforms changes the cap's effect on default by at most" and "the cap as modelled changes default by $-0.02 \pm 0.10$ points"
- **What is wrong (numbers).** Table tab:cap gives the cap of two at $\beta=0.3$ as $-0.13 \pm 0.13$ points and $-13.5\%$ volume. The paragraph gives $-0.02 \pm 0.10$ and $13.9\%$ for what reads as the same arm. The reason (a paired no-cap arm on the cap seeds, against the unpaired benchmark) is stated in a clause, not up front.
- **What is wrong (order).** The topic sentence gives a bound with a standard error ("at most $0.24 \pm 0.12$"), which is an odd form. The three definitions are introduced after their first use.
- **Rewrite.** "A diagnostic compares three definitions of the cap on the cap arms' own seeds, each paired with an arm without a cap; its numbers therefore differ from Table~\ref{tab:cap}, which uses the benchmark of the cooling-off block. The definitions are the cap as modelled, a cap on agreements, and a cap on platforms that still allows further agreements on platforms already owed. At a cap of one the first two coincide. At a cap of two, at $\beta = 0.3$, ... The largest difference between the modelled and the agreement cap is $+0.24 \pm 0.12$ points, at a cap of three, two standard errors from zero."

**AC-M4. pronoun, MED.** appC:204-206.
Quote: "right cancels an agreement and does not block the next one. It does not"
- **What is wrong.** "It" reads as the right of withdrawal, not the window.
- **Rewrite.** "...although that right cancels an agreement and does not block the next one. The window does not block borrowing for a shortfall."

**AC-M5. statistics-language, MED.** appC:264.
Quote: "Their first-order indices do not differ from zero"
- **Rewrite.** "Their first-order indices are within their bootstrap intervals of zero."

**AC-M6. clarity (55-word colon sentence), MED.** appC:60-65.
Quote: "It also means the ceilings above"
- **Rewrite.** "The ceilings above are evaluated at per-capita quintile bounds, so they understate what the test permits a large household at the same bound. Across the population the applied ceiling runs from zero to 93.2\% of income, with a mean of 49.6\% in the bottom quintile."

### LOW

**AC-L1. grammar, LOW.** appC:38.
Quote: "An earlier version still fitted the separation rate"
- **What is wrong.** "still" reads as "continued to".
- **Rewrite.** "A still earlier version fitted the separation rate..."

**AC-L2. register, LOW.** appC:25.
Quote: "Until the final version"
- **Rewrite.** "Under an earlier rule, now replaced, a household defaulted after seven consecutive ticks..." Name it the "streak rule" here, since the register and Appendix F use that name.

**AC-L3. statistics-language (no standard error), LOW.** appC:31-32.
Quote: "raised default by 0.18 points"
- **What is wrong.** The other figures in the sentence carry a standard error.
- **Fix.** Add "$\pm$ SE".

**AC-L4. repetition, LOW.** appC:51-53. Two consecutive sentences start "Income is".
- **Rewrite.** "Income is survey take-home income, so statutory deductions are largely already out of it, and the model does not reduce it during a spell of unemployment."

**AC-L5. vague quantifier, LOW.** appC:55.
Quote: "which makes the test mildly more permissive"
- **Fix.** Give the size, or say "more permissive".

**AC-L6. terminology, LOW.** appC:70 and tab_robustness_appendix:14.
Quote: "Households act in random asynchronous order, reseeded every tick." and "random, reseeded each tick"
- **What is wrong.** The order is redrawn. Ch2, appB and appG use "redrawn".
- **Fix.** Use "redrawn every tick".

**AC-L7. statistics-language, LOW.** appC:75 and appA:75.
Quote: "default changes by $+0.17 \pm 0.11$" and "A fixed-order arm changes default by less than two standard errors"
- **Fix.** Use the house wording: "default does not change detectably ($+0.17 \pm 0.11$ points)".

**AC-L8. terminology, LOW.** appC:110.
Quote: "is 91 or more days past due, the bureau construct"
- **Note.** See C4-M3.

**AC-L9. overclaim, LOW.** appC:143-144.
Quote: "granted credit that a lender seeing its current income would refuse"
- **Fix.** "can be granted credit that..."

**AC-L10. agreement, LOW.** appC:187.
Quote: "No South African data exists"
- **Fix.** "No South African data exist on who influences whom."

**AC-L11. punctuation, LOW.** appC:270.
Quote: "activation-order and population-size checks and the single-tick shock; and"
- **Fix.** Replace "; and" with ", and".

**AC-L12. order, LOW.** appC:260.
Quote: "Replicate noise is still 14\% of the"
- **What is wrong.** "still" refers to the earlier 37% run, which is mentioned three sentences later.
- **Fix.** Drop "still" or move the earlier-run sentence first.

**AC-L13. consistency of evidence strength, LOW.** appC:291-292.
Quote: "that longer interest-free promotions" / "raise card balances"
- **What is wrong.** Ch1:122 has Hamill et al. "suggest that longer interest-free promotions could raise indebtedness".
- **Fix.** Use one strength in both places ("suggest ... could raise").

**AC-L14. terminology, LOW.** appC:120 "3.6\% of agents" and appC:184 "lowest-income agents".
- **Fix.** Elsewhere in the body the 3.6% are households. Use "households".

**AC-L15. typography, LOW.** tab_cooloff and tab_cap Vol. columns.
- **What is wrong.** Text-mode hyphens are used as minus signs ("-4.2", "-35.1").
- **Fix.** Use $-4.2$.

**AC-L16. ± meaning, LOW.** "±" means one standard error everywhere except 04:195, appC:263 and tab_sobol (95% bootstrap half-widths). Each use is labelled, so this is acceptable. Check that every Sobol "±" carries the label.

---

## Appendices A, B, D, E, F, G

### MED

**AB-M1. statistics-language (overclaim), MED.** appendix_b_register.tex:49.
Quote: "the \ac{BNPL} effect on default is flat over 0--0.30"
- **What is wrong.** The test supports "does not change detectably", with slope $+0.003 \pm 0.010$ per 0.1. Ch4 is careful not to say "flat".
- **Rewrite.** "the \ac{BNPL} effect on default does not change detectably over 0--0.30".

**AB-M2. terminology (overclaim), MED.** appendix_b_register.tex:49.
Quote: "the top of the pre-registered sweep"
- **What is wrong.** "Pre-registered" implies a public registration. Ch4:58 says only that the reporting rule was fixed before the runs.
- **Rewrite.** "the top of the sweep, whose reporting rule was fixed before the runs".

**AB-M3. terminology (robustness vs sensitivity), MED.** appB register:39, 61, 117, 119; appF:7, 94, 95, 101; appG:129, 130, 190.
Quote: "robustness arm" and "effect-robustness arm"
- **What is wrong.** Ch3's Table tab:experiments and Ch4 call these "level sensitivity" and "effect sensitivity" arms.
- **Fix.** Use "sensitivity arm" and "effect-sensitivity arm" throughout. The labels tab:robustness and sec:results-robustness need not change.

### LOW

- **AB-L1. register, LOW.** appB register:49 "$\beta = 0$ is the control and the headline". Replace "the headline" with "the reported reference".
- **AB-L2. terminology, LOW.** appB register:65 "Under the earlier streak rule". The name first appears here, while appC:25 uses "the earlier default rule". Define "streak rule" in appC:25.
- **AB-L3. terminology, LOW.** appB register:105 "at 2026 vintage" vs the note's "at 2026 prices" (appB register:19-20, appD:269). Use "at 2026 prices".
- **AB-L4. number style, LOW.** "0--0.30" / "0.30" (register) vs "0--0.3" (tab_sobol, Ch3 table, Ch4). "1.0" (appB spec:83, register:101) vs "1.00" (Ch2, tab_effect). Pick one per quantity.
- **AB-L5. terminology, LOW.** appB spec:35 "Agents treat current income as persistent." and :37 "Agents know their own balance sheets". Use "Households".
- **AA-L1. register, LOW.** appA:57 "badly over-permissive". Write "over-permissive at the bottom of the distribution". The example that follows makes the point.
- **AA-L2. terminology, LOW.** appA:63 "\ac{BNPL} providers apply is one of the conditions". In the model these are platforms, so use "the light screen the platforms apply".
- **AA-L3. wrong word, LOW.** appA:66 "Every household opens with no". Use "starts with no".
- **AA-L4. terminology, LOW.** appA:50-51 "single binary behavioural type". Elsewhere this is the "repayment archetype", so use "a binary repayment archetype".
- **AD-L1. agreement, LOW.** appD:21 "with the data-layer fields behind them, the survey field or fields it is built from". Use "...with the data-layer fields behind it, the survey field or fields each is built from".
- **AD-L2. misplaced clause, LOW.** appD:133-135 "none of which is discretionary in the ordinary sense," / "because \ac{NIDS} offers no finer split." Rewrite: "Because \ac{NIDS} offers no finer split, the label ``discretionary'' also covers transport, utilities and education, none of which is discretionary in the ordinary sense."
- **AD-L3. missing word, LOW.** appD:174 "its assumptions and its limits are Appendix~\ref{app:matching}". Use "are in Appendix".
- **AD-L4. unit missing, LOW.** appD:273 "(7.04, 6.08 and 4.36, against Stats". Use "(7.04, 6.08 and 4.36\%, against Stats SA's 6.9, 6.0 and 4.4\%)".
- **AD-L5. house style, LOW.** appD:250, appE:116, appE:137 and appE:145 write "percentage points" in prose, and tab_validation writes "0.4pp" with no space. Ch3:66 sets the convention as "points in the text and pp in tables". Use "points" in prose and "pp" with a consistent space in tables.
- **AE-L1. hyphenation, LOW.** appE:97 "nonlinear" vs 04:59 "non-linear". Use "non-linear".
- **AE-L2. wrong word, LOW.** appE:103 "gives why we did not use it". Use "explains why we did not use it".
- **AF-L1. notation collisions, LOW.** Each one is defined, but a reader of the pseudocode will trip over them:
  - $c(i)$ is the matching cell and $c_i(t)$ is consumption distress.
  - $d$ is a donor (appE:11, appF:178) and $d_i(t)$ is the default indicator.
  - $a$ is the drawn arrears age (appF:249) and $a_i(t)$ is liquid savings.
  - $h_b$ is a band's upper bound and $h_i(t)$ is hired jobseekers.
  - $s_b$ is a CCMR band share and $s_g$ is the peer share.
  - $p$ is province, platform, and the probability superscripts. appF:43 acknowledges the $q$/$p$ overlap only.
  - Fix: rename the local variables in Algorithm alg:seed (e.g. $x$ for the age and $\sigma_b$ for the band share), and use $j$ or $\delta$ for the donor.
- **AG-L1. pronoun, LOW.** appG:190-191 "so it spreads across platforms only when a limit binds". "it" is the arm, not the household. Use "...so a household spreads across platforms only when a limit binds".

---

## Cross-cutting: number style

- **Replicate counts.** Prose uses words ("twenty", "one hundred") but "250" in digits. Figure notes use "20 replicates" and "100 replicates", and tab_sobol uses "8 replicates" against Ch3's "eight per design point". Choose one rule, for example digits for counts given with a unit.
- **Thousands separators and rand amounts.** These are consistent (R1{,}911, 2{,}796).
- **Decimals for the same quantity.** Default uses two decimals everywhere (good). Holding is two decimals in tab_baseline_arms (9.93) and one in tab_beta and tab_distribution (9.9). Stacking is one decimal in tables and whole numbers in prose (acceptable).
- **Percent vs points.** I checked every "%", "points" and "pp" in Chapters 4-6, Appendix C and the generated tables. Rate changes are in points and relative changes are in per cent throughout. The exceptions are the tab_scenarios volume row (C5-L7), the unitless 04:39 (C4-L5) and appD:273 (AD-L4). The tab_scenarios note's "in per cent" is the only "per cent" in scope; use "%".
- **Spelling.** No US spellings found (behaviour, modelled, instalment, favour, programme, labour, and -ise are all British).
- **Capitalisation.** Section, Table, Figure, Appendix, Algorithm, Submodel and Pattern are capitalised consistently before a reference.
