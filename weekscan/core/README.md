Vendored, byte-identical copies of the IFI 2.0 indicator code (ifi/pine.py, ifi/indicators.py, ifi/states.py at the
Oct 18 freeze), the same files the Eye Lab vendors. The weekly scan imports these, never ifi/, research/ or eyelab/.
VENDOR.sha256 pins them; the tests fail if a byte changes.
