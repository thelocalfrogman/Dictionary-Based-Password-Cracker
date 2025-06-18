
SET hash_count to 0

SET use_upper_input to INPUT "Check UPPERCASE versions? (y/n): " LOWERCASE
SET use_lower_input to INPUT "Check lowercase versions? (y/n): " LOWERCASE
SET use_title_input to INPUT "Check TitleCase versions? (y/n): " LOWERCASE

---
# Detect hash type based on character length
FUNCTION detect_hash_type 