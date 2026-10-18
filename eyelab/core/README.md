Vendored, byte-identical copies of the prior system's IFI 2.0 indicator code (ifi/pine.py, ifi/indicators.py,
ifi/states.py at the freeze). The Eye Lab imports these, never the prior packages, so neither system can change the
other. VENDOR.sha256 pins them; the tests fail if a byte changes.
