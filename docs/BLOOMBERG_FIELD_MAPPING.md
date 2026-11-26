# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

Source: data/sample/bloomberg_reference_sample.json
Reference: docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md
Live connectivity: not demonstrated

The sample is an instructor-approved fallback fixture
(is_live_bloomberg_output: false). It contains illustrative teaching
values and does not prove live Bloomberg connectivity.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | observation_date | Teaching wrapper key. String YYYY-MM-DD |
| ticker | application mapping | AAPL or SP500 (from canonical_ticker) |
| open | open_value | Teaching wrapper key |
| high | high_value | Teaching wrapper key |
| low | low_value | Teaching wrapper key |
| close | close_value | Teaching wrapper key |
| volume | volume_value | Teaching wrapper key |

teaching wrapper key != Bloomberg LIVE field mnemonic

## TD10 handoff

- Access mode: APPROVED_SAMPLE (is_live_bloomberg_output: false)
- Instrument identifier: AAPL US Equity (canonical ticker: AAPL)
- Benchmark identifier: SPX Index (canonical ticker: SP500)
- Date representation: string, format YYYY-MM-DD (key: observation_date)
- Input structure: top-level object with a "series" list; each series has
  role, canonical_ticker, provider_identifier and an "observations" list;
  each observation has observation_date, open_value, high_value,
  low_value, close_value, volume_value
- Missing fields: none. No null value was found in the sample
  (checked with grep). All six observation keys are present in both series.
- Special normalization notes:
  - The ticker is not in the observation rows. It must be taken from the
    series canonical_ticker (AAPL or SP500), never from provider_identifier.
  - SPX Index observations all show volume_value = 0 (21 of 21
    observations; an index has no traded volume of its own). This is a
    value in the fixture, not a missing field.
  - Wrapper keys are teaching keys, not Bloomberg field mnemonics.
- Expected canonical reference: data/sample/bloomberg_reference_expected.json
- Note: docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md was not available in the
  repository when this mapping was written; the mapping follows the
  schema_note of the sample file and the expected canonical file.