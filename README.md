# Radio Swiss Pico Ticker

A "ticker" to show the currently playing song in [Radio Swiss](https://www.radioswissjazz.ch/en) (I have the _Jazz_ URL hardcoded, but you should know how to fix it) to be used together (potentially) with the [Homebridge-CLIPlayer](https://github.com/rberenguel/homebridge-CLIPlayer).

It requires a Pico with a [Pimoroni Unicorn hat](https://shop.pimoroni.com/products/pico-unicorn-pack?variant=32369501306963) as well as the [custom micropython for using it](https://github.com/pimoroni/pimoroni-pico/releases/tag/v1.23.0-1).

The code is based on Pimoroni's examples for the Unicorn.

https://github.com/user-attachments/assets/c9a372ee-4ffd-40c7-88b8-46d0a2e179db

---

## Usage

- You will need to add a file called `ssids.py` with the networks you want to try (more than one in case you want to move it around):

```python
ssids = {
    "network name1": "network password",
    "network name2": "network password",
}
```

- To use, just copy all the Python files to your Pico and restart it.
- Optionally change the URL in `current_song` to any other Radio Swiss online radio, or tweak the whole function to fetch from any other web radio provider.
- All buttons can be used for something (re-display the current song, change color, change brightness…) play around.
