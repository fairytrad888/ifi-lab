# Examples: how your eye-level signals get here

You can show a signal three ways; all end up as rows in `<RULE_ID>.csv`:

1. **Annotated screenshot.** Mark the bar where you'd act (and, if you like, where you'd be wrong). Claude reads the chart, writes the rule draft, and adds the row.
2. **Symbol + date list.** "XLE 2026-09-15 yes, XLK 2026-08-04 no". Near-misses (looks close but isn't) are the most useful rows.
3. **Verbal.** Describe what you look for; Claude drafts the rule and shows you blind charts of what it picks, and your yes/no on those becomes `<RULE_ID>_review.csv` (columns `chart_id,agree`).

Symbols outside the pools are fetched into a separate examples store. Any example symbol that belongs to pool A or B is excluded from grading that rule, because your eye has already seen it.
