# Hound
A FireCloud database extension

## Purpose

This repository contains the source code for the Hound database extension system.
This system aims to provide a low-latency system for logging changes to a FireCloud
workspace.

This allows for attribute provenance to be reconstructed by querying the database
history, and for external tools to log changes as well.

## Minimum Viable Product
1) Hound should be able to retain a log of when an entity/workspace attribute was changed, and why
2) Hound should be able to respond to provenance queries by checking above log entries
3) Hound should support logging arbitrary data (such as "a lapdog submission was run", etc)
4) Hound should be external to lapdog/dalmatain

## Usage
1) Users with hound-enabled software automatically generate logs as they continue
to do their work
2) Hound can recreate attribute value histories from logs to produce provenance

## Format

Hound logs data in a bucket folder. Entries are organized based on the list below.
`snowflake` refers to an auto-generated ID from Hound's snowflake implementation.
Snowflakes are almost guaranteed to be unique (see below)

* hound/: Root folder for hound data in bucket
  * (samples|pairs|participants|sets)/: Folder for entity-metadata change logs
    * (entity-id)/: Folder for entity data
      * (attribute)/: Folder for attribute data on each entity
        * (snowflake): Serial numbered files containing **update objects**
  * workspace/: Folder for workspace-level metadata
    * (attribute)/: Folder for attribute data on the workspace
      * (snowflake): Serial numbered files containing **update objects**
  * logs/: Folder for event-logs
    * (job|upload|meta|other)/: Folder for specific event entries
      * (snowflake): Files containing **log entries**

### Snowflake spec
Encode 22-byte snowflake into 44 byte (hex encoded) object name
* 64-bit (8 byte) unix timestamp (8 byte floating-point number)
* 64-bit (8 byte) machine id (based on nodename) Only 6 bytes used
* 16-bit (2 byte) random client id (generated during init of Snowflake object)
* 16-bit (2 byte) sequence identifier (starts at 0 per client, increments from there)
* 8-bit (1 byte) Zero field (reserved)
* 8-bit (1 byte) checksum field (sum of remaining fields)

#### Uniqueness

Snowflakes are structured to almost guarantee uniqueness. If two clients from the
same machine (or from machines with identical MAC addresses) create a snowflake
at **exactly** the same time (within their system clocks' precisions) **AND** the
clients have generated the same number of snowflakes so far (clients have the same
  sequence id), there is a 1/65536 chance that the snowflakes will collide (based on
  client id).
