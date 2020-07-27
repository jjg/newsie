# paperboy

How about a daily printed newspaper, govna?


## Description

Paperboy delivers a fresh hard-copy newspaper via your printer every morning based on the news sources you select.  Each article includes a summary and a QR code you can scan with your phone shoud you *want to know more*.


## Status

  * Generates a page of news from a list of RSS feeds
  * Can print the page directly to CUPS-configured printer
  * Emails the page to a configured destination
  * Block stories based on keywords

## TODO

  * Make the feed list dynamic (part of the config)
  * Add a tool to automate configuration
  * Fix encoding/unicode issues (ex:, the `'` in `it's` getting turned into weird characters).
  * ~~Blend stories so they don't appear grouped by source~~
  * ~~Only include stories from the last 24 hours (or some configured amount)~~
  * Grab more of the article if the RSS `summary` is too short
  * ~~Figure out why iOS won't parse the QR code links~~

