# A281428: factorial bounds and sharp onsets

Haobo Ma — ChronoAI Pte Ltd, Singapore  
Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore

License: CC BY 4.0 (`cc-by-4.0`). Revision 2, November 11, 2026.

## Results and attribution

Peter Bala's conjectures are in OEIS A281428, COMMENTS items 1–2,
with the displayed date March 3, 2026. They first entered the history on
February 16, 2026 (revision 32); item 2 was clarified on February 17
(revision 33), and the examples and displayed March date were added in
revision 37.
Lien-Hung Su (2026), Theorem 4.1, previously proved both conjectures.
This note gives an alternative proof of the first and extends its factorial
bounds and the analysis of the two accompanying examples:

- For `a(n)=(2n)! [x^(2n)] C(x)`, `C=cosh(integral_0^x C^4)`,
  `v_p(a(n)) >= v_p((2n)!)` for every prime `p>=5`.
- Every polynomial `F(S,C)` with integer coefficients has integral exponential
  coefficients `b_F(j)=j! [x^j] F(S,C)` with the same factorial valuation bound.
- Eventual divisibility for A281428 and A281427 occurs precisely for positive
  moduli coprime to 6. For A052502 it occurs precisely for moduli prime to 3.
- Modulo 385 the exact eventual-zero onset is 6.
- Modulo 27 the least eventual period is 18, with exact onset 2. This sharpens
  the onset 7 in the source observation and onset 3 supplied by Su's theorem.
- The source's January 22, 2026 operator formula requires the factor `n!`:
  `f_k(n,0)=n! [x^n] C(x)^k`, as previously noted by Su, Remark 4.2.
- The tentative `g`-operator identity in A281183, FORMULA, December 22,
  2025, follows by the substitution `z=tan(theta)` and operator conjugation.
  Its argument is a written proof in the note; the finite checks below
  cover the A281428 recurrences and companions.

These additional consequences are not presented as conjectures posed by the
companion entries, or as priority claims. The general period theorem and the
distinct exponent-4 cross-referenced sequences are credited to Su.

## Build

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Or use a standard LaTeX installation:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is included in `note.tex`; BibTeX is not required.
Packages: `fontenc`, `lmodern`, `amsmath`, `amssymb`, `amsthm`, `booktabs`,
`tabularx`, `geometry`, `xurl`, and `hyperref`.

## Exact coefficient and congruence checks

Python 3.10 or newer, standard library only:

```sh
python3 verify.py > regenerated-verification.json
cmp verification.json regenerated-verification.json
```

Two integer recurrences agree through index 256. The rational inverse-cubic
and square-root calculation covers indices 0–128. Independent rational products
check columns 1–8 through index 64 and the two companion identifications.
The modulo-27 certificate supplies the recurrence seed pairs, the obstruction
to onset 1, and the obstructions to proper-divisor periods. A polynomial
identity certificate verifies the differential equation used to derive the
second-order recurrence. Counts and precise finite ranges appear in
`verification.json`. Infinite conclusions have written proofs in `note.tex`
or the explicitly cited theorem of Su; finite agreement is not extrapolated.

## Scientific sources and Lean coverage

- Posing source: https://oeis.org/A281428, COMMENTS items 1–2 and EXAMPLE,
  Peter Bala, March 3, 2026. Companion identities: https://oeis.org/A281427
  and https://oeis.org/A052502.
- Lien-Hung Su, *Quadratic Derivations and Uniform Modular Periods for Six
  Inverse-Function Sequences*, v1, October 31, 2026, Theorem 4.1 and Remark 4.2,
  pp. 7–8; Corollary 3.3 and Proposition 3.4, pp. 5–6:
  https://doi.org/10.5281/zenodo.23835577.
- Ira M. Gessel, *Lagrange inversion*, JCTA 144 (2016), 212–249,
  https://doi.org/10.1016/j.jcta.2016.06.018;
  arXiv:1609.05988v1, Theorem 2.1.1, https://arxiv.org/abs/1609.05988v1.
- The declaration `D5.S1.Recurrence.Residue.BalaQuarticEGFEventualDivisibility.result`
  proves existence of the source series and eventual integer divisibility for
  every positive modulus coprime to six:
  https://github.com/the-omega-institute/trureturing/blob/b0f7c01b01511ea00428c1b6edad5dd2b372eaf8/D5/S1/Recurrence/Residue/BalaQuarticEGFEventualDivisibility.lean.
  The valuation inequalities, converse, polynomial observables, companion
  consequences, sharp 385/27 results and cross-referenced operator identity
  are written proofs in the note, not statements of this declaration.

The source archive contains `note.tex`, `README.md`, `verify.py`,
`verification.json`, `metadata.json`, and `SHA256SUMS`. Its mathematical
source and expected checker output are identical to the accompanying files.
From the extracted directory, `sha256sum -c SHA256SUMS` checks every
included source file before rebuilding.
