# notion-sync

```
pip install notion-sync
```

![](https://www.travis-ci.org/Adjective-Object/notion-md-sync.svg?branch=master) ![](https://img.shields.io/badge/straight-passing-brightgreen.svg)

A tool to sync a notion collection to markdown files

## Setting up Notion

- Create a collection table view
- Add columns for
  - Publish Date (type date)
  - Status (type select, with Published as an option)
  - Tags (type multi_select)

## Setting up you syncing directory

- copy `config-example.json` to `config.json`
- set token_v2 to the value of your token_v2 token on a logged-in session of notion
- set sync_root to the url of a collection view page (the database-as-rows page)

In the same directory as your config file, run:

```
notion_sync
```
