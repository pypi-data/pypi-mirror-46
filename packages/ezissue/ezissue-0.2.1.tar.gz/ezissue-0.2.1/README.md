<p align="center">
  <!-- <img src="https://raw.githubusercontent.com/andre-filho/commit-helper/master/assets/200-200.png" style="align: center"> -->
  <h1 align="center">EZIssue</h3>
</p>

<p align="center">
  <!-- <a href="https://travis-ci.org/andre-filho/commit-helper">
    <img src="https://travis-ci.org/andre-filho/commit-helper.svg?branch=master" alt="Build Status">
  </a>
  <a href="https://codeclimate.com/github/andre-filho/commit-helper/maintainability">
    <img src="https://api.codeclimate.com/v1/badges/0ef7545d395120222d77/maintainability" alt="Maintainability">
  </a>
  <a href="https://codebeat.co/projects/github-com-andre-filho-commit-helper-master"><img alt="codebeat badge" src="https://codebeat.co/badges/7621c6dc-7143-4efa-af3e-45508210d276" /></a>
  <a href="https://www.codacy.com/app/andre-filho/commit-helper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andre-filho/commit-helper&amp;utm_campaign=Badge_Grade">
    <img src="https://api.codacy.com/project/badge/Grade/595af9a088cf44e19ec2679a8c2617f6" alt="Codacy Badge">
  </a>
  <a href="https://codeclimate.com/github/andre-filho/commit-helper/test_coverage"><img src="https://api.codeclimate.com/v1/badges/0ef7545d395120222d77/test_coverage" /></a>
  <a class="badge-align" href="https://www.codacy.com/app/andre-filho/commit-helper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andre-filho/commit-helper&amp;utm_campaign=Badge_Coverage">
    <img src="https://api.codacy.com/project/badge/Coverage/595af9a088cf44e19ec2679a8c2617f6"/>
  </a> -->
</p>

## What does it do?
The **ezissue cli** is an application with command line interface which it's main objective is to help you
in the issue creation process in your projects.

It takes a file with a markdown table with your issues, formats them and send them to your repo's API.
Therefore you will no longer spend hours creating issues manually.

## Why should I use this?
If you find that the issue creation process is painfull and it breaks your *full-loko* mood while developing something, this is for you.

But if you want to spend hours creating issues on Github or Gitlab and find it fun (I sincerely doubt it), who am I to tell you what to do!

## Usage and configuration

This program has a CLI that you can take advantage of. Running `ezissue --help`
will show you the usage and options for the CLI.

```bash
$ ezissue --help

  Usage: ezissue [OPTIONS] FILENAME [github|gitlab]

  Options:
    --subid TEXT
    --numerate BOOLEAN
    --prefix [US|TS||BUG]
    --help                 Show this message and exit.
```

The issue output format is the following:

```markdown
 <!-- issue-table.md -->
 | issue title | brief description | condition a;condition b;condition c |
```

```markdown
  <!--title-->
  <PREFIX><SUBID><NUMBER> issue title
  <!--body-->
  **Issue description:**
  brief description

  - [ ] condition a
  - [ ] condition b
  - [ ] condition c
```

## Updating your current version

If you already have one of our `pip` releases installed in your machine and want to update to the latest version, use the command:

```bash
$ pip3 install --upgrade ezissue
```
