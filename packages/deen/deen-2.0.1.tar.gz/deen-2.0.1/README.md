# deen

<img src="https://i.imgur.com/HKdQpc3.png" width="90%">

An application that allows to apply encoding, compression and hashing to generic input data. It is meant to be a handy tool for quick encoding/decoding tasks for data to be used in other applications. It aims to be a lightweight alternative to other tools that might take a long time to startup and should not have too many dependencies. It includes a GUI for easy interaction and integration in common workflows as well as a CLI that might be usefule for automation tasks.

## Installation

```bash
pip3 install deen
```

Further information is available in the [wiki](https://github.com/takeshixx/deen/wiki).

### Packages

There is a [deen-git](https://aur.archlinux.org/packages/deen-git) package available in the Arch User Repository (AUR).

## Usage

See the [wiki](https://github.com/takeshixx/deen/wiki) for basic and more advanced usage examples.

### Bash Completion

Bash completion can be enabled by adding the following line to your `~/.bash_profile` or `.bashrc`:

    source ~/path/to/deen-completion.sh

### ZSH Completion

ZSH completion can be enabled by adding the following line to your `~/.zshrc`:

    autoload bashcompinit && bashcompinit && source ~/path/to/deen-completion.sh
