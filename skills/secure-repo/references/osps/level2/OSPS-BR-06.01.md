# OSPS-BR-06.01

- **Control:** OSPS-BR-06, Include Signatures and Hashes With Release (Build and Release)
- **Level:** 2+
- **Exact text:** [OSPS Baseline v2026.08.28](https://baseline.openssf.org/versions/2026-08-28#osps-br-0601), the authority

> Summarised in this skill's own words.

- **Requires:** each official release is signed, or listed with each asset's
  cryptographic hash in a signed manifest.
- **Meet it:** sign at build time (for example OpenPGP or Sigstore signatures, or build
  provenance attestations), and publish hashes in a signed manifest. Choosing the
  mechanism is a tool decision for the human.
- **Verify:** verify a recent release's signatures or manifest yourself, following the
  project's own instructions.
