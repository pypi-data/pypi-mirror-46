## Is Git Repo Clean

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Intro](#intro)
    - [What is it?](#what-is-it)
    - [Why create it?](#why-create-it)
- [Install](#install)
- [Usage](#usage)
    - [programmatic](#programmatic)
    - [cli](#cli)
- [Api](#api)
    - [`check` async (dir=os.getcwd()) => bool](#check-async-dirosgetcwd--bool)
    - [`checkSync` (dir=os.getcwd()) => bool](#checksync-dirosgetcwd--bool)
    - [`version`](#version)
- [Test](#test)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

<br>

### Intro

#### What is it?

A simple function that tests whether your git repo is clean.

by *clean* I mean it has:
- no untracked files
- no staged changes
- no unstaged changes

Installing this also exposes a cli command `is-git-repo-clean`


#### Why create it?

I wanted to write a build script that would exit early if the git repo
wasn't clean

<br>

### Install

```sh
$ pip install is_git_repo_clean
```

<br>

### Usage

#### programmatic

```python
import is_git_repo_clean


async def isCleanAsync(pathToGitRepo = None):
  # async by default
   return await is_git_repo_clean.check(pathToGitRepo)


def isCleanSync(pathToGitRepo = None):
  # sync available
  return is_git_repo_clean.checkSync(pathToGitRepo)
```

#### cli

```sh
$ is-git-repo-clean --help

Usage
  is-git-repo-clean [--dir <path>] [--silent]
  is-git-repo-clean --help
  is-git-repo-clean --version

Options
  dir:      path to the git repo to test.  Defaults to `os.getcwd()`
  silent:   disables output
  help:     print this
  version:  prints the version of this tool

Returns
  <exit code>: <output>

  0: yes
  1: no
  2: <invalid arg message>
  3: dir is not a git repository
  4: unexpected error occurred <error>
```

<br>

### Api

`is_git_repo_clean` exports the following


#### `check` async (dir=os.getcwd()) => bool
 - an asynchronous function that returns whether the git repo is clean


#### `checkSync` (dir=os.getcwd()) => bool
 - a synchronous function that returns whether the git repo is clean


#### `version`

<br>

### Test

```sh
hub clone olsonpm/py_is-git-repo-clean
cd py_is-git-repo-clean
python runTests.py
```
