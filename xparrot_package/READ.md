# xParrot Interactive CLI App

---

Note that this `fish` function no longer works. :(

```fish
function xp
    set -g -x AIRTABLE_API_KEY 'insert_your_key_to_api_here'
    xparrot $argv -k $AIRTABLE_API_KEY
end
```
