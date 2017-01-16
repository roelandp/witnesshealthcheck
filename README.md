# witness health check
Barebones basic Python script to check basic witness health

This python3 script monitors basic vitality of system/tasks for (Steem/Golos) witnesses and uses Telegram to notify when problems arise.:
- Last updated price feed
- Time outs on public seednode

Add a telegram token + id and you get notifications as soon as either your `pricefeed_updatetreshold` is surpassed or your given seednode times out or has another error.

This script depends on
- Piston.steem library
- Telegram API

## usage:
1. Copy witnesshealthcheck.py over to a server with interwebs and Piston.steem
2. Fill out the `telegram_token` and `telegram_id` variables as well as your `witness` and `seed_node` info.
3. `chmod +x` witnesshealthcheck.py
4. Test the script for example with a very low value for `pricefeed_updatetreshold` (it should notify immediately if you put it to `0`)
5. Put the script inside a regular called (e.g. every 2/4 hours) cronjob.
