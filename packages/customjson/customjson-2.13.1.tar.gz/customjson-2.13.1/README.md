# customjson [![Build Status](https://travis-ci.com/ludeeus/customjson.svg?branch=master)](https://travis-ci.com/ludeeus/customjson)

This tool generates the "master" files that are used for the [`custom_updater`][custom_updater] and the [`custom_component_store`][custom_component_store]

For the [`custom_updater`][custom_updater] it generates and update these jsonfiles:

- [`custom-cards/information`][custom-cards/information]
- [`custom-components/information`][custom-components/information]

For the [`custom_component_store`][custom_component_store] it generates and updates [`ludeeus/data/custom-component-store/V1`][ludeeus/data/custom-component-store/V1]

## Install

**Require Python version 3.5.3+**

```bash
python3 -m pip install -U customjson
```

### Example

```bash
customjson --token aaabbbccc111222333 --mode component
```

#### CLI options

param | alias | description
-- | -- | --
`--token` | `-T` | An GitHub `access_token` with `repo` permissions.
`--push` | `-P` | Push a new `repos.json` file to the information repo.
`--mode` | `-M` | Must be `card` or `component`.
`--version` | `-V` | Print the installed version.

## Add more resources

### Components

The easiest way to add additional resources is to reuse the json file used by ['custom_updater'][custom_updater] if yo have that.

**Examples:**

https://github.com/ludeeus/customjson/blob/f0fd9643a3a5af63c5dc02cd228dfad99796fe3e/customjson/components/custom_updater.py#L7-L16

But there are other ways if you look in the `/customjson/components/` dir you can see different implementations that give more granular control.

### cards

look in the `/customjson/cards/` dir to see different implementations

***

[![BuyMeCoffee](https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667)](https://www.buymeacoffee.com/ludeeus)


[custom_updater]: https://github.com/custom-components/custom_updater
[custom_component_store]: https://github.com/ludeeus/custom-component-store
[custom-cards/information]: https://github.com/custom-cards/information/blob/master/repos.json
[custom-components/information]: https://github.com/custom-components/information/blob/master/repos.json
[ludeeus/data/custom-component-store/V1]: https://github.com/ludeeus/data/blob/master/custom-component-store/V1/data.json