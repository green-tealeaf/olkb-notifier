# olkb-notifier
Simple py3status module for notifying order position in the olkb.com queue.

## Usage
If you're using i3status with py3status already:

1. Place the `olkb.py` module in your py3status module directory.
2. Replace `<insert order number here>` on line 11 with your order number.
3. Add `order += "olkb"` into your `.i3status.conf`
4. Restart i3 or just i3status.

## Notes
The module creates a file called .olkb.cache into a hardcoded location at `$HOME/.i3/py3status/.olkb.cache` to store the last-seen order position. You can change that manually if required.
