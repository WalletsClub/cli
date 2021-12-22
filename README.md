# WalletsNet CLI

The WalletsNet CLI helps you connect to WalletsNet.

**With the CLI, you can:**

- Trigger webhook events or resend events for easy testing
- Tail your API request logs in real-time
- Build your first credit transfer transaction easy.

![demo](https://walletsclub.oss-cn-beijing.aliyuncs.com/Github/Snipaste_2021-12-22_11-40-15.png)

## Installation

WalletsNet CLI is available for macOS, Windows, and Linux for distros like Ubuntu, Debian, RedHat and CentOS.

```sh
git clone git@github.com:WalletsClub/cli.git
cd cli
pip3 install -r requirements.txt
pip3 install --editable .
```

## Usage

Installing the CLI provides access to the `walletsnet` command.

```sh-session
walletsnet [command]

# Run `help` for detailed information about CLI commands
walletsnet help
```

## Commands

The WalletsNet CLI supports a broad range of commands. Below is some of the most used ones:
- listen
  - Communicate with WalletsNet on your local machine, do not use it in production deployment
- examples
  - A list of available samples that can be created and bootstrapped by the CLI
- trigger
  - Trigger example instructions to conduct local testing.
- open
  - Open WalletsNet page
- status
  - Return WalletsNet system status and service availability.
- help
  - Help guide


## Documentation

Learn how to build your first credit transfer transaction, see the [Manual](https://static.walletsclub.com/walletsnet/documentation/blog/Get-start-your-first-credit-transfer.html)

## Feedback

Got feedback for us? Please don't hesitate to tell us on [feedback](https://github.com/WalletsClub/cli/issues/new).


## License
Copyright (c) WalletsNet. All rights reserved.

Licensed under the [Apache License 2.0 license](blob/master/LICENSE).
