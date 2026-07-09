*Could this be misused?*
- **Signals:** inputs from outside the trust boundary are validated and/or escaped
  (injection, XSS, path traversal); authn/authz checks on anything that reads or mutates
  data; no secrets in code; least privilege; caps on anything a caller controls (page
  size, batch size, rate).
- **Smells:** trusting caller input; missing authz on a mutating path; secrets in
  source; unbounded caller-controlled limits.