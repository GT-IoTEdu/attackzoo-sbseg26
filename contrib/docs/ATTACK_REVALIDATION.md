# attackzoo: Problems In The Attacks, Servers, And Scripts, With Measured Fixes

Report on the repository `GT-IoTEdu/attackzoo-sbseg26`, at commit `8613c66`. It has 51 items: 33 with a fix in a
commit, 4 victim proposals in optional commits, 2 optional diffs in the PR description, 4 reports with no fix and 8
notes with no fix. We measured the real effect of each attackzoo attack on the target; this text collects what did not
match what attackzoo itself promises, with the line of code that causes it, the test we ran and, when there is one, the
measured fix, before and after.

This report and the reproduction file enter the repository, in English, with the first commit of the pull request that
brings the fixes: `contrib/docs/ATTACK_REVALIDATION.md` and
[`contrib/docs/ATTACK_REVALIDATION_REPRODUCTION.md`](ATTACK_REVALIDATION_REPRODUCTION.md). In this text, "the PR",
"this PR" and "this commit" refer to that pull request and to its commits. An item whose commit is not accepted remains
valid as a report of the problem measured on `8613c66`.

## How To Read

Each item reads on its own, with the technical terms defined the first time they appear in it; when it cites another
item, it uses the ID. Each item with a commit is also in the message of the corresponding PR commit, in Portuguese (the
commit messages are in Portuguese, not translated), with two differences: in place of the general method section, the
message carries a short paragraph with the common method (and keeps in "How we tested" what that paragraph does not
cover), and the reproduction commands appear in full inside it. In the messages, the sections keep their Portuguese
names: Promessa (Promise), O que acontece (What happens), Causa (Cause), Como testamos (How we tested), Conserto or Sem
conserto testado (Fix or No fix tested), Antes e depois (Before and after), Como reproduzir (How to reproduce),
Ressalvas (Caveats) and Versões (Versions); in the reproduction part, Usa (Uses), Uma vez (Once), Em cada sessão (Each
session), Esperado (Expected) and Execução (Executed); and the marks are [medido], [lido] and [inferido] ([measured],
[read in code], [inferred]).

Each item follows the same template:

- title: `ID · attack or component: what happens`;
- short table: class, what goes into the PR (commit, optional commit, diff in the description, report only, note),
  files touched and which other item it depends on;
- **Promise**: what attackzoo says the attack does, quoted from `attack.yaml`, the README or the code, with the line;
- **What happens**: what we measured on the wire and on the target;
- **Cause**: the line of attackzoo code (or of the third party, with version) that explains the behavior;
- **How we tested**: what is specific to the item: images and trees, server, arguments, captures and counters, number
  of runs, machine load, what the independent reviewer recounted, what was done from the repository's own checklist,
  the deviations and what was not tested. What holds for all items is in "How We Tested (General Method)" and is not
  repeated in the item;
- **Fix** (or "No fix tested"): what the diff changes and what stays the same;
- **Before and after**: the same measurement under the same conditions, with only the image (or the file) swapped;
- **How to reproduce**: one line that points to the item's section in the reproduction file and to the parts of the
  common setup it uses (see "Reproduction file" below);
- **Caveats**: limits of what was measured;
- **Versions**: versions and commits of everything that went into the test.

Each claim carries a mark:

- **[measured]**: we ran it and counted (capture, log, system counter);
- **[read in code]**: we read it in the code, with file and line;
- **[inferred]**: deduced from what was measured or read, without direct measurement.

Classes:

- **(a) the code does something other than what it promises**: the attack says (in `attack.yaml`, in the README or in
  its own log) that it does something and, measured on the wire, it does not.
- **(b) inconsistency between parts of attackzoo**: each part works on its own, but two parts of the repository do not
  fit together (the attack and the server that attackzoo itself starts, the README and the code, the catalog and the
  campaign).
- **suggestion**: not a defect; it is a proposal (for example, a victim that does not exist in the scenario today).
- Qualifiers appear in parentheses: "latent" (only shows up under a condition that does not occur today), "secondary"
  (hidden by another defect of the same attack), "minor".

Short paths inside an item (`attack.yaml:5`, `entrypoint.sh:12`) are relative to the folder of the item's attack or
server; a bare `:N` is a line of the last file cited. Numbers use a decimal point. Counts of four or more digits appear
sometimes with a thousands comma (36,364) and sometimes without (3058), as they were recorded; in them, the comma is
never a decimal separator.

**Reproduction file.** The commands to redo the tests are in a separate file that accompanies this report,
[`contrib/docs/ATTACK_REVALIDATION_REPRODUCTION.md`](ATTACK_REVALIDATION_REPRODUCTION.md) ("attackzoo: How to
Reproduce the Report's Tests"). It starts with a common setup, in numbered parts (P1, P2, ...): the
code and the BEFORE (`8613c66`) and AFTER (the item's commit) trees, the isolated network of each item, the capture and
the count, the machine load and the images that several items use. Then comes one section per item, with the same ID,
which says which setup parts it uses, carries the commands, the expected result (the values of this report, with the
variation the item allows) and the run. All blocks were executed exactly as written, on the machine in "What Is Fixed";
the "Executed" line of each section says when, with what load and whether the result matched what was expected. The
differences between what ran and the text are declared in the file itself: the fetch in P1 (and, in the runs of
2026-11-17, also the clone) came from a local copy of the PR branch, which was not yet published; the P6 build ran with
two extra read-only commands; and the sections, except the one for MQTT-03, ran with an earlier form of P1, without the
`RAMO` variable, whose functions give the same commits. The PR commits do not come in a fresh clone: the setup brings
them from the PR branch with
`git fetch https://github.com/INARI18/attackzoo-sbseg26.git correcoes-ataques:correcoes-ataques` and finds each item's
commit by its ID, as the "Commits in the PR" section, after the Summary, shows. After the PR is accepted, the commits
are already in `main`: this step can be skipped, with `RAMO=main` in the setup (P1), and an item's commit is found with
`git log --grep='^<ID> ·' main`. If only some of the commits made it into `main`, the items left out stay on the PR
branch (the fetch above, with `RAMO` at its default).

## What Is Fixed

- **attackzoo**: commit `8613c660722c852bbeb10bfb180d58039f1c3426` (`main`). Checked with `git ls-remote` on 2026-11-16
  (04:13 and 19:04) and on 2026-11-17 (02:27), local time (UTC-3); each test battery checked again at the start and at
  the end, and `main` did not change. On 2026-11-18, the GitHub clones of the reproduction file runs had `main` at
  `8613c66` [measured]. The `docker/` folder is the same as in commit `d560abb` (`d560abb..8613c66` only adds
  `gerar_benigno_infra.py`).
- **Test period**: 2026-11-13 to 2026-11-18. On 2026-11-18 the measurements with mosquitto 2.1.4 for MQTT-01 and
  MQTT-03 ran, along with repetitions cited in ZEN-06, ZEN-08, COAP-01, NET-01 and CAMP-02 and runs of the reproduction
  file.
- **Docker**: 29.6.2, buildx 0.35.0.
- **Machine**: laptop with Ubuntu 24.04.4, 8 CPUs, 8 GB of RAM, Docker root on an HDD.
- **Third parties**: attackzoo clones several repositories and installs packages with no pinned version; each item
  gives the version that went into the test and the "Versions" appendix gathers them all. The ones that weigh most:
  Micro-XRCE-DDS-Client v3.0.2 and Micro-CDR v2.0.2 (the `master` of each on 2026-11-16); XRCE agent run v3.0.1 (`master`
  today is v3.0.2); Zenoh router `eclipse/zenoh:1.7.2`; mosquitto 2.1.2 (in the tables of the MQTT items, except where
  the item says otherwise) and 2.1.4 (the `eclipse-mosquitto:2` tag since 2026-11-17: in the 2026-11-18 measurements of
  MQTT-01 and MQTT-03 and in 2026-11-17 runs of the reproduction file, from MQTT-01 to MQTT-05); CoAPServer `744cc22`;
  DVWA 1.10 with Apache 2.4.25; yersinia 0.8.2; `ubuntu:24.04` resolved on 2026-11-16.

## How We Tested (General Method)

Each item has its own "How we tested", with only what is specific to it: images and trees, arguments, captures and
counters, number of runs, load, what the reviewer recounted, deviations and what was not tested. What holds for all
items is here and is not repeated in them; where an item does something differently, it says so.

**The 5 criteria.** A finding only made it into this report after passing:

1. **Promise quoted from attackzoo itself**: what `attack.yaml`, the README or the code say the attack does, with file
   and line. Without a promise, there is no defect, only a suggestion.
2. **New, complete reproduction**: the attack (or the build, or the script) from `8613c66`, built from scratch with the
   repository's own Dockerfile and run against attackzoo's own server; when the effect is a network one, with all
   traffic captured (see "Full-frame capture" below). Counts come from the capture, not from the attack log, because in
   several items the log says it sent what it did not send.
3. **Cause with a line of code**: the line of attackzoo, or of the third party with version and commit, that explains
   what the capture shows.
4. **Fix measured before and after under the same conditions**: same network, same IPs, same server, same arguments and
   variables; only the attack image changes (or the server's, or the script file). Items with no fix (reports and
   notes) do not have this criterion.
5. **Independent verification**: a second reviewer, who did not write the fix, recounted the captures with their own
   tools (their own tshark filters, protocol parsers they wrote, kernel counters), checked the lines cited in `8613c66`
   and in the third parties, and applied the diff to a clean checkout of `8613c66`. Where they disagreed with the first
   test, their number held, and it is the one in the text.

Where a criterion does not apply (an outdated README has no traffic; a note has no fix), the item says what was done
instead.

**Machine.** All tests ran on the machine in "What Is Fixed", with Linux kernel 7.0.0-38-generic, the same throughout
the period: the machine did not reboot between 2026-11-13 and 2026-11-18 [measured: last boot on 2026-11-07, read on
2026-11-19, with the same kernel].

**Images.** The images were built with the repository's own Dockerfile and the `docker/` context, as in
`docker/build-images.sh`, except where the item says otherwise (for example, images built earlier, with attack code
identical to that of `8613c66`). BEFORE is the image of the `8613c66` tree; AFTER, the same recipe with the item's
commit; when the item compares something else (for example, XRCE-02 against the image with XRCE-01), it says so. Where
the build clones or installs third parties with no pinned version, the item gives the versions that went in; in several
items, the attack file inside the image was checked against the tree (md5 or sha256), and the item says so.

**Isolated network.** Each test ran on its own Docker network, created with `docker network create --internal` (no
outbound access) and fixed IPs, with a new server container on each run. Except where the item says another plan, the
server or target is at `.10`, the attacker at `.20`, observers (subscriber, probe) from `.30` on and the legitimate
client at `.40`. No container gets `-p`: the target is the container's IP, as in the `docker run` in the attacks'
READMEs. The attack ran with `docker run`, with the arguments its README shows or that `attackzoo.py run` builds
(obtained by swapping the `docker` in `cmd_run` for a `print`), without `--rm` so the exit code and the log could be
read, and with the environment variables explicit, equal to the defaults in `attack.yaml`, except when the item says
otherwise. When the attack does not exit on its own within the item's window, it is stopped with `docker kill`
(SIGKILL), which has the same effect as the `docker rm -f` with which attackzoo ends the window. Differences from
attackzoo's own flow, common to all items (the item only mentions them when it does something differently):

- the network: in place of the `docker0` that `servers.sh` and `docker/build-images.sh` use, an isolated network, with
  fixed IPs and no `-p`;
- no `--rm`, to keep the exit code and the logs;
- the capture: full-frame and unfiltered on the bridge (below), in place of the per-attack filter the campaign uses;
- observers that attackzoo does not have (subscribers, probes, our own legitimate clients, general database log), which
  only observe; the item says which;
- the campaign path (`contrib/scripts/run_full_campaign.py`, with `--network host` and target `127.0.0.1`) was not
  exercised, except where the item says the opposite (the CAMP-* items ran the campaign script or its capture step;
  COAP-01 reproduced the campaign window);
- some third-party versions were pinned so the test would be repeatable: for example, XRCE agent v3.0.1, because
  building `master` (v3.0.2) with Fast-DDS risked exhausting the machine's memory; when this changes the result, the
  item says so;
- no internet on the test network, which matters in one case (the SpiderFoot in `web-wide-scanner` downloads a list at
  startup; item WEB-01 explains how we worked around it).

**Paths A and B.** Some items call "path A" the flow of `README.md:330-335` at the root: the attack against the server's
internal IP and internal port, with the `docker run` that `attackzoo.py run` builds (`modules/runners.py:147`). It is
what the tests ran, on the isolated network. "Path B" is the campaign's: `contrib/scripts/run_full_campaign.py` starts
the attack with `--network host` against `127.0.0.1` on the server's published port, going through docker-proxy, the
Docker process that forwards the port published with `-p` to the container, and ends the window with `docker rm -f`.

**Full-frame capture.** `tcpdump -s 0` on the bridge of the test network, running on the host, unfiltered: every
complete Ethernet frame, in all directions, from before the attack to after its end. In some items there was also a
capture inside a container's network namespace (the item says so). The kernel dropped 0 frames in all the captures
cited, except where the item gives another number. The count was done with tshark and, in several items, also with a
protocol parser we wrote; the second reviewer recounted with their own tools.

**Count.** With tshark display filters (the item cites the ones that matter) and, in some items, with raw BPF in
tcpdump; in the UDP filters, `!icmp` removes from the count the UDP header that travels inside ICMP port unreachable
messages. Kernel counters (`/proc/net/snmp` and the like in the target's network namespace), server logs and the
container's cgroup (CPU and memory) are used where the item says so.

**Runs.** One run per condition, except where the item says otherwise; BEFORE and AFTER with the same script and the
same arguments, with only the image (or the file) swapped.

**Machine load.** Part of the time other tests ran in parallel, on other networks; each item records the load (load
average from 0.15 to 13.8 in the items' measurements, depending on the item; from 0.08 to 14.9 in the runs of the
reproduction file). That is why the conclusions are counts (packets, messages, sessions, responses), not rates. Where an
item cites time or CPU, it gives the load and treats the number as an order of magnitude; where the load could explain
the result (for example, the STP floods of NET-02), the measurement was redone with the machine free of other tests,
which we call a quiet machine: 1-minute load average below 1.5 before each run and no other test running.

**Independent review.** In each item, the second reviewer of criterion 5 redid the counts without our scripts and
checked the lines cited; in the items with a fix, they applied the diff to a clean `git archive` of `8613c66`. Their
wording corrections are applied in the text. Each item's "How we tested" says what they recounted, with what, and where
they found something different.

**The repository's own checklist.** `contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132` and
`contrib/docs/SCRIPTS.md:212-216` ask, for an attack or server change: `attackzoo.py list --id`, a syntax check, an
image rebuild, a short run, MITRE if it changes and `check_attack_smoke.py`. The item only mentions the checklist when
it did something beyond what this paragraph says. In each item with a changed image, the rebuild and the short run are
the item's own measurements, with `docker run` and not with `attackzoo.py run`; no commit changes `mitre`;
`check_attack_smoke.py` was not run in any item. On the tree with the whole PR (commits, optional ones and the
description's diffs): `attackzoo.py list --json` loads 60 attacks in 7 categories, with no missing field; `bash -n` on
`servers.sh` and `docker/build-images.sh` and the parse of the changed `.py` files pass [measured]. On the final tree of
the PR (the 37 item commits), again on 2026-11-17 and, after the MQTT-03 commit was redone on 2026-11-18, on 2026-11-19:
`attackzoo.py list --json` loads 60 attacks in 7 categories, `bash -n` passes on all changed `.sh` files, the changed
`.py` files compile, no commit changes `mitre` and no changed file has CRLF [measured]. `check_attack_smoke.py` was not
run; two changes that it will flag are described in the items: the exit 143 of GEN-04 and the exit 1 of `xss-scanner`
when it finds XSS (WEB-06).

**What no item tested**, except where the item says so: `docker0` itself; path B; attackzoo's web interface and its
time watchdog; `attackzoo.py run` with real Docker (we ran the `docker run` it builds); `check_attack_smoke.py`; the
XRCE agent v3.0.2 in execution.

**Reproduction file.** The commands in the reproduction file follow these same practices: the common setup creates each
item's isolated network, makes the full-frame capture on the bridge with the drop count, counts with tshark and records
the machine load.

**PR assembly [measured, 2026-11-17 and 2026-11-18].** The series of the 37 item commits was assembled on `8613c66` from
the tested diffs and applies in full. Each commit has exactly the diff of its item (compared commit by commit). Where a
tested diff was split across commits or had a part left out of the PR (XRCE-01; MQTT-01 and MQTT-02; WEB-02 to WEB-06;
NET-04 and NET-05), the parts, added to what was left out, rebuild the original diff; CAMP-03 was redone on top of
CAMP-01 and CAMP-02, with the same lines swapped. On the final tree, with the `docker/` context as in `build-images.sh`
and with cache, the 36 images whose Dockerfile or copied files change with the PR build without error, and so do the 3
whose folder changes only in files the Dockerfile does not copy (`coap-server`, `smb-enumerating`,
`web-https-heartbleed`): 39 of 39. Of these, 30 came entirely from the tests' cache; the other 9 redid steps, among them
the 4 XRCE images that combine the attack fix with that of GEN-01, compiled again. On 2026-11-18 the series was redone
with the new MQTT-03 commit, which only changes the attack's `.py` in that commit and the following ones; each commit
again has exactly the diff of its item, the split parts rebuild the original diffs, and the `mqtt-qos-amplification`
image builds without error from the final tree, with the tree's `.py` inside it [measured].

## Notes For Reviewers

Effects of the commits beyond the fix, and choices of ours that the owner may prefer done another way. The detail, with
the measurements, is in each item.

Effects that will show up:

- **GEN-04**: `syn-flood` and `dos-http-slowloris` now exit on their own with code 143 at the end of `DURATION_S`, and
  `contrib/scripts/check_attack_smoke.py`, which treats any exit other than 0 as a failure, goes from PASS to FAIL on
  both [read in code; measured by the reviewer with the commands the smoke generates; the whole script was not run].
- **WEB-06**: when it finds XSS, the fixed `xss-scanner` exits with 1 (dalfox does this by design), and
  `check_attack_smoke.py` would count that as a failure [exit 1 measured; the smoke only read, not run].
- **WEB-02**: `http-server` now serves `/config/config.inc.php.bak` (200; upstream, 404), which DVWA's own setup
  creates on purpose (`MySQL.php:85-93`); we did not delete it. The file has the same variables as the `config.inc.php`
  in use, including the database password, which is the public default of the `vulnerables/web-dvwa` image [measured].
- **COAP-01**: without `--rm`, a stopped `coap-server` stays `Exited` and `./servers.sh start` does not recreate it;
  `./servers.sh restart` recovers it [measured].
- **SMB-01**: nmbd announces the server; on `docker0` this becomes new benign traffic, NBNS and BROWSER broadcasts
  [measured on the isolated network: 49 broadcasts in 900 s; inferred for `docker0`].
- **ZEN-01 to ZEN-06**: the six Zenoh attacks go from UDP to TCP, with an open session, which is what attackzoo's
  router listens on; their traffic in the pcaps changes shape [measured].
- **MQTT-01**: the broker gains the user `attacker`, and the authenticated flood costs more CPU in the broker: 1.03 s
  per 1000 CONNECTs in the item's test (0.78 to 1.70 s in twelve measurements of 2026-11-18), against 0.10 s for
  today's refusal, with mosquitto 2.1.2; with 2.1.4, which the `eclipse-mosquitto:2` tag gives since 2026-11-17, 13.28
  to 13.91 s [measured].
- **MQTT-03**: with mosquitto 2.1.4, the client whose `connect()` fails tries again: in 20 s, more TCP connections than
  clients (3058 to 4262 for 2000) and 1058 to 2334 `connect failed` log lines; against a target that refuses the
  connection, the attack keeps insisting until each client's deadline and ends on its own (at the defaults, in 22.5 s,
  with 36,364 SYNs and 36,364 log lines), instead of exiting in ~1 s [measured]. With a 2.1.2 broker up, nothing
  changes (2000 CONNECTs, 1016 CONNACKs, no new line).
- **CAMP-01**: the new filter of `cdp-table-flood` (`not ip and not ip6 and not arp`) is wider than the original: on
  `-i any` on a real host it keeps every frame that is not IPv4, IPv6 or ARP, from all interfaces [read in code;
  measured only on the isolated network, where the pcap was 100% CDP].
- **NET-04 and NET-05** (optional): the new victims start by default through `servers.sh` and
  `docker/build-images.sh`, including in the campaign, and become new hosts on `docker0` for the scanners [not
  measured]. The two commits also put DHCP and CDP in the servers' protocol list at the root `README.md:61` and take the
  count at `README.md:240` from 9 to 10 and to 11 servers [read in code].

Our choices:

- **MQTT-01**: the `attacker`/`attackerpass` credential reaches the attacks through the variables `MQTT_USER` and
  `MQTT_PASS`, which are not declared in `attack.yaml` (`contrib/docs/CATALOG_MAINTENANCE.md:72` prefers controls
  declared there). Alternatives measured in the item: use the `benign` user or turn on `allow_anonymous`.
- **MQTT-03**: in the new connection retry, 1 s between attempts and a 20 s deadline per client (the campaign window).
  Alternatives measured in the item: a longer connection deadline in paho and a semaphore of 100 clients until CONNACK.
- **WEB-01**: the `-m` list with 4 SpiderFoot modules defines what the attack now does. The port stays ignored
  (SpiderFoot 4.0 has no port option); the commit documents this in the port label, at `attack.yaml:27`, and in the
  `--target_port` line of the attack's `README.md:23`.
- **XRCE-03**: we kept the code's value (10 ms per step) and fixed the log text; the alternative is to change the value
  to 10 s per step.
- **ZEN-04, ZEN-05 and ZEN-09**: the keys `attackzoo/timestamp-mess` and `attackzoo/memory-exhaustion` are our choice
  (upstream had no key), and the ZEN-09 subscriber subscribes by default to `attackzoo/**`, which also receives the
  `memory-exhaustion` samples.
- **WEB-03 to WEB-06**: the login uses the fixed credential `admin`/`password`, the one DVWA's setup creates; with the
  password changed on the server, the login fails.
- **NET-04 and NET-05**: start the victims by default; the alternative is to leave them on demand, removing the lines
  from `servers.sh` and `build-images.sh`.
- **WEB-07**: no commit, with two options: remove `http-server` from the attack's `target_services` (recommended, not
  measured) or the optional diff that takes the attack to DVWA's `?page=`.
- **GEN-01**: the line `[ -x bin/$attack ] || ...` is redundant with `set -e`; it can go.
- **Versions**: as in the rest of the repository (see GEN-02), the NET-04 and NET-05 victims, the XRCE-11 client and the
  ZEN-09 subscriber use a base image by tag, and NET-04, NET-05 and the `curl` of WEB-06 install packages with no pinned
  version.

## Summary

In the same order as the items below: first those with a commit, by area and in the order of the PR commits; then the
optional commits, the description diffs, the reports and the notes.

| ID | Attack or component | Problem | Class | In this PR | Depends on |
|---|---|---|---|---|---|
| XRCE-01 | `xrce-dds-fragment-abuse` | no FRAGMENT goes out: the 4-slot stream (976 B usable) does not hold messages of 8 to 32 KB | a | commit | - |
| XRCE-02 | `xrce-dds-fragment-abuse` | the datawriter is created with empty XML; the agent refuses the creation (STATUS 0x80) and discards every write | a (secondary) | commit | XRCE-01 (effect) |
| XRCE-03 | `xrce-dds-time-desync` | the log calls nanoseconds microseconds and divides by 1e6 calling it seconds | b | commit | - |
| XRCE-04 | `xrce-dds-discovery-poison` | does not receive the XRCE discovery, answers in RTPS and loops on its own packet | a | commit | - |
| XRCE-05 | `xrce-dds-session-hijack` | the datawriter is created with empty XML and the 100 injections are discarded | a | commit | - |
| ZEN-01 | `zenoh-pico-keepalive-flood` | no KEEP_ALIVE reaches the router (UDP against a TCP-only router, another message's ID, no session) | a; transport also b | commit | - |
| ZEN-02 | `zenoh-pico-fragments-reassembly` | no fragment reaches the router's reassembly | a; transport also b | commit | - |
| ZEN-03 | `zenoh-pico-sequence-exhaustion` | no FRAME reaches the router; fixed, it consumes CPU but does not degrade ordering or reliability | a; transport also b | commit | - |
| ZEN-04 | `zenoh-pico-timestamp-mess` | no message reaches the router, and the timestamp goes in a format Zenoh does not have | a; transport also b | commit | - |
| ZEN-05 | `zenoh-pico-memory-exhaustion` | no byte reaches the router; fixed, the maximum-size batch does not make memory rise | a; transport also b | commit | - |
| ZEN-06 | `zenoh-pico-proto-fuzzer` | no fuzz case reaches the router and the crash detection never fires | a; transport also b | commit | - |
| ZEN-07 | `zenoh-pico-proto-fuzzer` | the "Malformed" strategy is drawn at random and printed, but has no generator (it sends random bytes) | a (minor) | commit | ZEN-06 (effect) |
| MQTT-01 | `mqtt-publisher-flood`, `mqtt-lwt-abuse`, `mqtt-qos-amplification`, `mqtt-broker` | the three attacks connect without credentials to a broker that refuses anonymous; only the refusal is exercised | b | commit | - |
| MQTT-02 | `mqtt-lwt-abuse` | `disconnect()` sends a graceful DISCONNECT, the broker discards the Will and the false alarm never goes out | a | commit | MQTT-01 (effect) |
| MQTT-03 | `mqtt-qos-amplification` | without paho's network loop, each client sends at most 20 QoS 2 PUBLISH and no PUBREL | a | commit | MQTT-01 (effect) |
| COAP-01 | `coap-server`, `coap-response-fuzz` | the server dies on the first datagram the parser rejects and nothing in attackzoo brings it back | b | commit | - |
| COAP-02 | `coap-token-collision` | the chosen Token never reaches the wire and each request uses a new socket: there is no collision | a | commit | - |
| WEB-01 | `web-wide-scanner` | SpiderFoot receives "IP PORT" as the target, treats it as a person's name and no packet reaches the server | a | commit | - |
| WEB-02 | `http-server` (DVWA) | the server starts with the DVWA database empty and every correct login goes to `setup.php` | b | commit | - |
| WEB-03 | `php-lfi-enumeration` | enumerates `?page=` on `login.php`, which does not read `page`; no file is included | a | commit | WEB-02 (effect) |
| WEB-04 | `web-post-bruteforce` | POSTs to `/` with no form, session or token; no password is evaluated | a | commit | WEB-02 (effect) |
| WEB-05 | `sql-injection` | runs sqlmap on `/` with no session and never reaches DVWA's injectable parameter | a | commit | WEB-02 (effect) |
| WEB-06 | `xss-scanner` | scans parameters DVWA does not have and never tests DVWA's reflected XSS | a | commit | WEB-02 (effect) |
| NET-01 | `arp-spoof` | ArpSpoof resolves the CIDR one address at a time (2 s per silent address) before forging the first reply | a | commit | - |
| NET-02 | `stp-conf-flood`, `stp-tcn-flood`, `cdp-table-flood`, `dhcp-starvation` | the background yersinia gets `/dev/null` as stdin and stops right away (0 to 1 frame per run) | a | commit | - |
| SMB-01 | `smb-server` | nmbd does not start, although the server declares NetBIOS and publishes 137/138 udp | a | commit | - |
| CAMP-01 | `run_full_campaign.py` (`cdp-table-flood`) | the `ether dst` capture filter does not compile on `-i any`: tcpdump dies and the campaign carries on "completed" | a | commit | - |
| CAMP-02 | `run_full_campaign.py` (`stp-conf-flood`, `stp-tcn-flood`) | the `stp` filter never matches a BPDU on `-i any` with tcpdump >= 4.99: 0 BPDUs in the pcap | a (only with tcpdump >= 4.99 on `-i any`) | commit | - |
| CAMP-03 | `run_full_campaign.py` (`ipv6-mld-flood`) | the `icmp6` filter drops all MLD, which carries a Hop-by-Hop header before the ICMPv6 | a | commit | CAMP-01, CAMP-02 (text) |
| CAMP-04 | `setup.sh` (NTLFlowLyzer) | the pinned NTLFlowLyzer (`86d0102`) does not import, and the campaign carries on "completed" without the flow CSV | a | commit | - |
| GEN-01 | the 7 `xrce-dds-*` (`install.sh`, `compile.sh`) | the build scripts exit with 0 when the compile or the clone fails | a (latent) | commit | - |
| GEN-03 | `web-https-heartbleed`, `smb-enumerating` | `target_services` points to the wrong server | b | commit | - |
| GEN-04 | `syn-flood`, `dos-http-slowloris` | ignore `DURATION_S`: BusyBox's `exec timeout` leaves python as PID 1, which discards SIGTERM | a | commit | - |
| NET-04 | `dhcp-starvation` (new server `dhcp-server`) | the scenario has no DHCP server to exhaust; victim proposal | b | optional commit | NET-02 (effect) |
| NET-05 | `cdp-table-flood` (new server `cdp-listener`) | nothing in the scenario listens for CDP; victim proposal | suggestion | optional commit | NET-02 (effect); NET-04 (text) |
| XRCE-11 | `xrce-dds-discovery-poison`, `xrce-dds-session-hijack` (new client `client-xrce-dds`) | no legitimate XRCE client in the scenario; victim proposal | suggestion | optional commit | XRCE-04, XRCE-05 (effect) |
| ZEN-09 | `zenoh-pico-timestamp-mess` (new server `zenoh-subscriber`) | with no subscriber, the timestamp's effect is not observable; subscriber proposal | suggestion | optional commit | ZEN-04 (effect) |
| ZEN-08 | `zenoh-pico-memory-exhaustion` | variant with mass declarations (DeclareSubscriber), which makes the router's memory grow | suggestion | optional diff in the description | ZEN-05 (text) |
| WEB-07 | `idor-path-traversal` | does the traversal in the URL path against an Apache that normalizes `/../`: no file is read | b | optional diff in the description | WEB-02 (effect) |
| WEB-08 | `idor-url-parameter` | fuzzes the `valid_name` parameter, which DVWA does not read | a | report only | - |
| NET-03 | `stp-tcn-flood` | the README still describes old defaults (`active_s` 5, `delay_ms` 500, "at most 5 seconds") | b | report only | - |
| CAMP-05 | campaign (NTLFlowLyzer) | on `-i any` NTLFlowLyzer creates 0 flows and the empty CSV counts as an extractor ok | b | report only | CAMP-04 (effect) |
| GEN-02 | Dockerfiles and build scripts | clones, pip and base images with no pin (suggestions) | suggestion | report only | - |
| XRCE-06 | `xrce-dds-fragment-abuse` | the script lasts ~77 s and the default window is 30 s | b (low impact) | note | - |
| XRCE-07 | `xrce-dds-time-desync` | no message is altered on the wire; the offset exists only in the attacker's own session | a, in part | note | - |
| XRCE-08 | `xrce-dds-discovery-poison` | no client in the scenario does XRCE discovery: the attack has nothing to poison | b | note | - |
| XRCE-09 | `xrce-dds-discovery-poison` | the fake agent answers RTPS to CREATE_CLIENT: the detour stops at the handshake and no session opens | a (latent) | note | XRCE-04 (effect) |
| XRCE-10 | `xrce-dds-session-hijack` | the 30 s window covers only 1 of the 7 keys the attack tries (43 s per key) | b | note | - |
| MQTT-04 | `mqtt-lwt-abuse` | always prints "LWT triggered", without checking anything | a | note | - |
| MQTT-05 | `mqtt-lwt-abuse` | `max_runtime_s: 10` against a loop of ~33 s; with the cutoff 17 of the 50 Wills go out | b | note | MQTT-01, MQTT-02 (effect) |
| COAP-03 | `coap-response-fuzz` | the "malformed options" phase sends a plain GET | a | note | - |

## Commits In The PR

In series order, on `8613c66`. The subjects are the commits' own, in Portuguese, as `git log` shows them. The first
commit adds this report and the reproduction file, in English, under `contrib/docs/`, and one link to each in the
documentation list of the `README.md`; it has no item ID and can be dropped without stopping the others from applying.
In the others, the first line of each commit's body is the item title, starting with the ID; that way,
`git log --format='%h %s' --grep='^ZEN-06 ·' 8613c66..correcoes-ataques` finds an item's commit. In a fresh clone of
attackzoo, this PR's commits arrive with
`git fetch https://github.com/INARI18/attackzoo-sbseg26.git correcoes-ataques:correcoes-ataques`, from the PR branch.
After the PR is accepted, the commits are already in `main`: this step can be skipped (in the reproduction file, with
`RAMO=main` in P1), and an item's commit is found with `git log --grep='^<ID> ·' main`. If only some of the commits made
it into `main`, the items left out stay on the PR branch (the fetch above, with `RAMO` at its default).

| n | ID | Commit subject |
|---|---|---|
| 1 | - | Relatório de revalidação dos ataques |
| 2 | XRCE-01 | Fragmentação no xrce-dds-fragment-abuse |
| 3 | XRCE-02 | Datawriter no xrce-dds-fragment-abuse |
| 4 | XRCE-03 | Correção do printf no xrce-dds-time-desync |
| 5 | XRCE-04 | Descoberta XRCE no xrce-dds-discovery-poison |
| 6 | XRCE-05 | Datawriter no xrce-dds-session-hijack |
| 7 | ZEN-01 | Sessão Zenoh no zenoh-pico-keepalive-flood |
| 8 | ZEN-02 | Sessão Zenoh no zenoh-pico-fragments-reassembly |
| 9 | ZEN-03 | Sessão Zenoh no zenoh-pico-sequence-exhaustion |
| 10 | ZEN-04 | Sessão Zenoh no zenoh-pico-timestamp-mess |
| 11 | ZEN-05 | Sessão Zenoh no zenoh-pico-memory-exhaustion |
| 12 | ZEN-06 | Sessão Zenoh no zenoh-pico-proto-fuzzer |
| 13 | ZEN-07 | Gerador Malformed no zenoh-pico-proto-fuzzer |
| 14 | MQTT-01 | Autenticação nos ataques MQTT |
| 15 | MQTT-02 | Fechamento sem DISCONNECT no mqtt-lwt-abuse |
| 16 | MQTT-03 | QoS 2 completo no mqtt-qos-amplification |
| 17 | COAP-01 | Reinício do coap-server em falha |
| 18 | COAP-02 | Correção do coap-token-collision |
| 19 | WEB-01 | Módulos do SpiderFoot no web-wide-scanner |
| 20 | WEB-02 | Banco do DVWA criado no build do http-server |
| 21 | WEB-03 | Login do DVWA no php-lfi-enumeration |
| 22 | WEB-04 | Login do DVWA no web-post-bruteforce |
| 23 | WEB-05 | Login do DVWA no sql-injection |
| 24 | WEB-06 | Login do DVWA no xss-scanner |
| 25 | NET-01 | Resolução ARP em lote no arp-spoof |
| 26 | NET-02 | Stdin do yersinia nos ataques de camada 2 |
| 27 | SMB-01 | nmbd no smb-server |
| 28 | CAMP-01 | Filtro de captura do cdp-table-flood |
| 29 | CAMP-02 | Filtro de captura dos ataques STP |
| 30 | CAMP-03 | Filtro de captura do ipv6-mld-flood |
| 31 | CAMP-04 | NTLFlowLyzer fixado em d99cd53 |
| 32 | GEN-01 | Falhas de build nos ataques XRCE-DDS |
| 33 | GEN-03 | target_services do smb-enumerating e do heartbleed |
| 34 | GEN-04 | Timeout sem exec no slowloris e no syn-flood |
| 35 | NET-04 | Vítima DHCP para o dhcp-starvation |
| 36 | NET-05 | Vítima CDP para o cdp-table-flood |
| 37 | XRCE-11 | Cliente benigno XRCE-DDS |
| 38 | ZEN-09 | Assinante Zenoh para o timestamp-mess |

## Dependency Map

Two kinds of dependency:

- **text**: a commit's diff has, in its context, lines that another commit creates or changes; without the other,
  `git apply` refuses the diff;
- **effect**: the commit applies on its own, but the measured effect only shows up with the other.

Text dependencies:

| Commit | Depends on | What happens without it |
|---|---|---|
| NET-05 (optional) | NET-04 (optional) | The lines of the two victims are neighbors in `servers.sh`, `docker/build-images.sh` and in the root `README.md` table, and NET-05 rewrites the protocol list and the server count that NET-04 changes in that `README.md`. Without NET-04, `git cherry-pick` of NET-05 conflicts in those 3 files, `git apply` refuses and `patch` fails on `README.md` and `servers.sh` [measured] |
| CAMP-03 | CAMP-01, CAMP-02 | The three lines are in the same dictionary (`AUTO_BPF_BY_ATTACK`) and CAMP-03's context includes the new lines of the other two. Without one of them (or without both), `git apply` refuses and `patch` applies with fuzz; `git cherry-pick` applies, by 3-way merge [measured] |
| ZEN-08 (description diff) | ZEN-05 | The diff only applies on top of ZEN-05 [measured] |

Same file, no text dependency: XRCE-02 was written on top of XRCE-01, ZEN-07 on ZEN-06, MQTT-02 on MQTT-01 and CAMP-02
on CAMP-01, but without the other, `git apply`, `git cherry-pick` and `patch` apply the same way; `patch` only shifts
the lines (-21, -121, -1 and -1) [measured, 2026-11-17, with each commit's `git format-patch` on the series without the
other]. XRCE-02, ZEN-07 and MQTT-02 depend on the other by effect (table below).

Effect dependencies (the first needs the second for the result measured in the item):

| Item | Needs | Why |
|---|---|---|
| XRCE-02 | XRCE-01 | Without XRCE-01 no FRAGMENT goes out and there is no write to deliver to the datawriter |
| XRCE-09 (note) | XRCE-04 | The handshake detour only exists with the discovery-poison fix |
| XRCE-11 (optional) | XRCE-04, XRCE-05 | The effect measured in discovery-poison uses the fixed attack; session-hijack's injections only reach DDS with the datawriter fix |
| ZEN-07 | ZEN-06 | Without ZEN-06 no fuzz case reaches the router's parser (it goes over UDP) |
| ZEN-09 (optional) | ZEN-04 | The subscriber only receives samples with timestamp-mess fixed (with the `8613c66` attack: 0 samples) |
| MQTT-02, MQTT-03 | MQTT-01 | Without the `attacker` user on the broker the connection is refused (CONNACK rc=5) and, with the refusal, the broker erases the Will |
| MQTT-05 (note) | MQTT-01, MQTT-02 | Without them no Will goes out, in any window |
| WEB-03, WEB-04, WEB-05, WEB-06, WEB-07 (description diff) | WEB-02 | Without the DVWA database created, every login goes to `setup.php` and none of the fixes reaches the vulnerable page |
| NET-04, NET-05 (optional) | NET-02 | With the `8613c66` yersinia, 0 DISCOVER and 0 CDP reach the victims |
| CAMP-05 (report) | CAMP-04 | The problem only shows up when NTLFlowLyzer imports |

Removal test [measured, 2026-11-17, and again on 2026-11-18 with the MQTT-03 commit redone, with the same result]: for
each of the 37 commits, the series was redone without it, with `git cherry-pick` of the other 36 on `8613c66`. Only one
removal stops another commit from applying: without NET-04, NET-05 fails. Any other commit can go without stopping the
others from applying; those that depend by effect keep applying, but without the effect described in the item. The 4
optional commits (victims) are at the end of the series. With the first commit in the series, on 2026-11-19 and on
2026-11-21 [measured], the same test on the 38 commits: without the first, all the others apply, and the other removals
give the same result.

## Commits: XRCE-DDS

### XRCE-01 · xrce-dds-fragment-abuse: No FRAGMENT Goes Out, Because The 4-slot Stream (976 B Usable) Does Not Hold Messages Of 8 To 32 KB

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/xrce-dds-fragment-abuse/attack_fragment_abuse.c` |
| Depends on | none |

**Promise.** `docker/attackers/xrce-dds-fragment-abuse/attack.yaml:5` and `README.md:3`: "Fragmented, incomplete, or
overlapping XRCE-DDS publications that stress reassembly, queues, and fragment handling on the agent." The code
announces each phase and says it sent: `attack_fragment_abuse.c:15` "[*] Sending incomplete fragments...", `:34` "[*]
Attempting overlapping fragment attack...", `:60` "[+] Overlapping fragments sent", `:65` "[*] Flooding with %d
fragmented messages...", `:87` "[+] Sent %d fragmented messages".

**What happens.** In XRCE-DDS (the DDS version for small devices: the client opens a session with an agent, which
publishes to DDS on its behalf), a message larger than the stream buffer (the session's send queue) only goes out split
into FRAGMENT submessages. The attack asks for 750 large messages (50 of 32,000 B, 200 of 16,000 B and 500 of 8,000 B)
and none goes out: the 750 calls to `uxr_prepare_output_stream` return 0, which is "invalid request" [measured]. The
whole run has 12 datagrams on the wire: from the attacker, the CREATE_CLIENT (the session-opening request), one datagram
with the 4 CREATE (participant, topic, publisher, datawriter) and 4 ACKNACK (receipt confirmations), 324 B of UDP
payload; from the agent, STATUS_AGENT, 4 STATUS and 1 ACKNACK; 0 FRAGMENT [measured]. Even so the attack prints
"Overlapping fragments sent" 20 times out of 20 and "Sent N fragmented messages" every 10 messages; only "Incomplete
fragments sent" stays at 0 of 50, because it is inside the `req_id` test [measured].

**Cause.** `attack_fragment_abuse.c:9-10` defines `STREAM_HISTORY 4` and `SMALL_BUFFER_SIZE 256 * STREAM_HISTORY`, and
`:128-130` creates the reliable output stream with those 1,024 B in 4 slots. `HUGE_MESSAGE_SIZE 32000` (`:11`) is
requested whole at `:19`, divided by 2 at `:39` and by 4 at `:70`, always with `uxr_prepare_output_stream`. In
Micro-XRCE-DDS-Client v3.0.2 (`6884d7bd`): `src/c/core/session/stream/output_reliable_stream.c:65-66` computes the
fragment block (252 B of the slot minus 8 B of headers = 244 B, with at most 4 free slots); `:101` only fragments if
`length <= available_block_size * remaining_blocks`, that is up to 976 B; messages of 8,008 to 32,008 B do not fit and
`:167` returns false; then `src/c/core/session/write_access.c:117,123` returns `UXR_INVALID_REQUEST_ID`, which is 0
(`include/uxr/client/core/session/session_info.h:45`). The attack tests the `req_id` (`:21`, `:43`, `:74`) only to skip
the write, without warning [read in code]. The condition at `:101` is the same in tags v2.4.3 (2024-03), v3.0.0, v3.0.1
and v3.0.2: with any Client since 2024 this attack does not fragment [read in code]. The 244 B block matches the wire
after the fix: the full FRAGMENT datagram is 252 B (4 + 4 + 244) [measured].

**How we tested.**
- Images: BEFORE = `docker build` of 2026-11-16 of the upstream `8613c66` tree, with the attack's own Dockerfile
  (`docker/` context, as in `docker/build-images.sh:127`). `install.sh` cloned the master of Micro-CDR (`99672492` =
  v2.0.2) and of the Client (`6884d7bd` = v3.0.2), checked inside the image; the image's `.c` has the upstream md5
  (`8e58cf5f`). AFTER = the same recipe with this commit: base, apt layers, third-party commits and
  `libmicroxrcedds_client.a` (md5 `a5977160`) the same; only the `.c` changes. Outside the commit, two diagnostic
  variants: upstream with 3 `fprintf(stderr)` that print the `req_id` (to count the 750 zeros) and upstream with only
  `STREAM_HISTORY 256`.
- Agent: `server-xrce-dds-agent` image of Micro-XRCE-DDS-Agent v3.0.1 (`155cfaaf`, with Fast-DDS v3.6.2 and Fast-CDR
  v2.2.8 pinned by commit), a new container per run, with `udp4 -p 8888` as in `servers.sh:116` and `-v6` (detailed
  log) in the runs that needed the log. attackzoo's `agent-source-install.sh` builds the Agent master, today v3.0.2
  (`a88c712b`), which we did not run. The refusal happens in the client before any byte goes out, so the agent version
  does not change BEFORE [read in code].
- Attack: the README's form (`docker run ... attack-xrce-dds-fragment-abuse:latest "<TARGET_IP>" "8888"`), with
  `-e DURATION_S=30` explicit (the default in `entrypoint.sh:5`). The attack ends through the entrypoint's own `timeout`
  (exit 124).
- Capture and count: count with tshark (FRAGMENT = first submessage with id `0x0d`, filter `udp.payload[4:1]==0d`;
  FLAG_LAST, the last-fragment mark, = bit `0x02` of the flags, `udp.payload[5:1] & 02`) and with an XRCE decoder of
  ours, which reads every submessage of every datagram and reassembles the messages by sequence number. From the agent:
  log with `-v6` and the UDP counters of `/proc/net/snmp`.
- Runs: BEFORE 3 (30 s with and without `-v6`, and 120 s), plus the 2 diagnostic ones; AFTER 5 (30 s with and without
  `-v6`, 30 s together with XRCE-02, 120 s, and one with `DURATION_S=20` and `docker kill` scheduled for 20 s, which did
  not get to act: the entrypoint's `timeout` exited first, exit 124). The 5 AFTER runs gave the same counts on the wire.
- Load: host load average between 2.2 and 4.5, with two other tests running on other bridges.
- Independent review: a second reviewer recounted the 10 captures with tshark and with an XRCE parser they wrote,
  checked the content of the reassembled messages, the lines cited in `8613c66` and in the Client from inside the image,
  and applied the tested patch (with the `setvbuf` line, see the deviation below) to a clean `git archive` of `8613c66`
  (`patch -p1` and `git apply --check`), arriving at the same file as the AFTER image.
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `attackzoo.py list --id`: not run,
  because the commit does not change `attack.yaml`.
- Declared deviation: the AFTER images we measured also had a `setvbuf(stdout, NULL, _IOLBF, 0)` line, which is not part
  of this commit. It only changes the stdout buffer, not the traffic; the commit without it was not built separately
  [inferred].
- Not tested: the campaign path (`--network host`, target `127.0.0.1` via docker-proxy, the Docker process that forwards
  the port published with `-p` to the container; the fix moves at the pace of the ACKNACKs, with 976 B in flight), the
  Agent v3.0.2 in execution and the stop by `docker rm -f` (exit 137).

**Fix.** Swaps `uxr_prepare_output_stream` for `uxr_prepare_output_stream_fragmented`, the Client's own API for a message
larger than the stream (`include/uxr/client/core/session/write_access.h:130`,
`src/c/core/session/write_access.c:148-313`), with a `flush_session` callback that runs
`uxr_run_session_until_confirm_delivery(session, 1000)` when the slots run out. The author's small stream
(`STREAM_HISTORY 4`) stays as it is. In phases 2 and 3 the code asked for 16,000 and 8,000 B but serialized only ~5.6 KB
and ~2.4 KB; in the fragmented API the last fragment only carries FLAG_LAST when the declared size is written
(`write_access.c:170-186`), so the same strings go into a zeroed local buffer of `size` bytes, written at once with
`ucdr_serialize_array_uint8_t` (Micro-CDR v2.0.2, `src/c/common.c:59-72,201-206`, which crosses the blocks through the
callback). The content stays the same as the original's, with the rest of the requested size zeroed [measured: 50 x
32,000 B all `0x46`; 200 x 16,000 B with 200 "OVERLAPPING_FRAGMENT_" and zero tail; 500 x 8,000 B with 100
"FLOOD_MESSAGE_" and zero tail]. Phases, counts, sizes, `usleep`, the `uxr_run_session_time(session, 10)` of phase 2, the
final wait, the key, `entrypoint.sh` and `attack.yaml` do not change. Alternative measured and discarded: only enlarging
the stream (`STREAM_HISTORY 256`) makes 208 of 750 messages go out (1 of 50, 200 of 200, 7 of 500; 13,627 FRAGMENT in
13,501 datagrams), because nothing runs the session in phases 1 and 3, and the tail of each message carries leftovers
from the buffer [measured].

**Before and after.** Same network, IPs, port, agent, `DURATION_S=30` and arguments; only the attack image changes.

| Measure | Before (`8613c66`) | After (with this commit) |
|---|---|---|
| `prepare` with a valid request | 0 of 750 | 750 of 750 (750 FLAG_LAST on the wire) |
| Datagrams attacker -> agent | 6 | 36,306 |
| FRAGMENT submessages | 0 | 36,300 (1 per datagram) |
| FRAGMENT with FLAG_LAST | 0 | 750 |
| Complete messages of 32,008 / 16,008 / 8,008 B | 0 / 0 / 0 | 50 / 200 / 500 |
| Retransmissions / sequence gaps | 0 / 0 | 0 / 0 |
| Agent ACKNACK | 1 | 36,301, none asking for a resend |
| UDP payload attacker -> agent | 324 B | 9,096,724 B |
| Container exit / duration | 124 / 31.2 s | 124 / 32.2 s and 32.0 s |
| Drops in the capture | 0 | 0 |

In AFTER, the messages go out in ~18.4 s, within the 30 s. In phase 1, in 50 of 50 messages the last 4 fragments go out
~100 ms later, in the next `prepare`: the agent is left with the reassembly incomplete during each `usleep(100000)`,
which is the "(NOT flushed)" of `:28` actually happening [measured]. The agent stays alive, with no restart, with 0 UDP
buffer errors (`RcvbufErrors` 0) [measured].

**How to reproduce.** In the reproduction file, section XRCE-01; uses P1, P2, P3, P6.

**Caveats.**
- Neither the original nor the fix does "overlapping": XRCE's FRAGMENT has no offset and the agent concatenates the
  pieces in sequence order until FLAG_LAST (Client `output_reliable_stream.c:139,152`, `write_access.c:182,189`; Agent
  `InputStream.hpp:380-387`) [read in code]. Measured: phase 2 is 200 distinct sequential messages, 0 repeated
  sequences.
- A message that never completes is expressible in this API: writing less than declared leaves the message without
  FLAG_LAST (`write_access.c:180-191`, `:267-268`) [read in code, not tested]. The fix follows what the code writes
  (phase 1 writes the 32,000 B declared); the incomplete message only exists for ~100 ms in each iteration of phase 1.
- If the callback fails (no ACKNACK in 1 s), serialization stops and the message is left without FLAG_LAST [read in
  code]; it did not happen in 5 runs.
- With the fix, the session and the messages reach the agent whole, but the datawriter is still refused (XRCE-02):
  without XRCE-02 nothing is published to DDS.
- In a run with a 20 s window, the 750 messages went out and phase 3 finished 18.7 s after the first datagram, with the
  machine loaded (load 3.4 to 4.0). It is 1 run: it does not count as a guarantee.
- The complete script still goes past the default 30 s (XRCE-06).
- Not tested: campaign path with `--network host`, Agent v3.0.2 in execution and stop by `docker rm -f`.

**Versions.**
- attackzoo `8613c66`.
- Micro-XRCE-DDS-Client v3.0.2 (`6884d7bd`) and Micro-CDR v2.0.2 (`99672492`): the master of each on 2026-11-16, which
  `install.sh` clones with no pin.
- Micro-XRCE-DDS-Agent run: v3.0.1 (`155cfaaf`) with Fast-DDS v3.6.2 (`39303846`) and Fast-CDR v2.2.8 (`1bc9c919`).
  Today's master is v3.0.2 (`a88c712b`), not run.
- Base `ubuntu:24.04` resolved on 2026-11-16, sha256 digest
  `73b999393d07f2bf65a40373778a44dc9a6d54ad7718d29247d8ff9413c4d6a8`.
- Ubuntu 24.04.4 host with Docker 29.6.2; capture and count with tcpdump 4.99.6 (libpcap 1.10.7) and tshark 4.6.9, in a
  tools container on the host network.

### XRCE-02 · xrce-dds-fragment-abuse: The Datawriter Is Created With Empty XML, The Agent Refuses The Creation (STATUS 0x80) And Discards Every Write

| | |
|---|---|
| Class | (a) the code does something other than what it promises (secondary) |
| In this PR | commit |
| Files | `docker/attackers/xrce-dds-fragment-abuse/attack_fragment_abuse.c` |
| Depends on | XRCE-01 (effect). The diff was written on top of XRCE-01, in the same file, but without it applies the same way, with an offset of -21 lines |

**Promise.** `docker/attackers/xrce-dds-fragment-abuse/attack.yaml:5` and `README.md:3`: "Fragmented, incomplete, or
overlapping XRCE-DDS publications that stress reassembly, queues, and fragment handling on the agent." The attack
creates a participant, topic, publisher and datawriter (`attack_fragment_abuse.c:135-149`) and writes to that datawriter
in every phase (`:19`, `:41`, `:72`).

**What happens.** In XRCE-DDS (the DDS version for small devices), the client asks the agent to create the DDS
entities; the datawriter is the entity that publishes to a topic. Here the agent answers STATUS 0x80 (error) to the
datawriter's CREATE in every run, including on the upstream image, and, in the runs with detailed log (`-v6`), logs
`[*** LOG ERROR #0001 ***] ... {argument not found}` [measured]. With XRCE-01 applied, the 750 messages reach the agent
whole, but the log shows 0 writes to DDS (`DataWriter.cpp | write`): nothing is published [measured]. The agent
reassembles the messages before looking for the datawriter (Agent `InputStream.hpp:368-401` concatenates until
FLAG_LAST), so the "stress reassembly" part happens with XRCE-01 alone; what is missing is the "publications" part
[read in code].

**Cause.** `attack_fragment_abuse.c:147`: `const char *datawriter_xml = "";`, passed to
`uxr_buffer_create_datawriter_xml` at `:148-149`. In Micro-XRCE-DDS-Agent v3.0.1 (`155cfaaf`),
`src/cpp/middleware/fastdds/FastDDSEntities.cpp:764-775`: with empty XML the `topic_name` is empty,
`find_local_topic("")` finds no topic and the creation fails (STATUS_ERR_DDS_ERROR, 0x80);
`src/cpp/processor/Processor.cpp:459-464`: WRITE_DATA (data submessage) to a nonexistent datawriter is discarded with no
reply [read in code]. In master (v3.0.2, `a88c712b`) the logic is the same at `FastDDSEntities.cpp:774-795` and
`Processor.cpp:460-467` [read in code]. The `{argument not found}` line is the Agent's own debug log coming out
truncated (`ProxyClient.cpp:526-530` in v3.0.1, `:534-538` in v3.0.2, pass 2 arguments to a 3-argument format; only
shows with `-v6`) [read in code]; it appears 1 time per refused datawriter and 0 times after the fix [measured].

**How we tested.**
- Images: three builds of 2026-11-16 with the attack's Dockerfile (`docker/` context): the upstream `8613c66`, the one
  with XRCE-01 and the one with XRCE-01 plus this commit. Same base, same apt layers, same Client v3.0.2 (`6884d7bd`),
  same Micro-CDR v2.0.2 (`99672492`) and the same `libmicroxrcedds_client.a`; only the `.c` changes.
- Agent: Micro-XRCE-DDS-Agent v3.0.1 (`155cfaaf`, Fast-DDS v3.6.2, Fast-CDR v2.2.8), a new container per run,
  `udp4 -p 8888 -v6` (`-v6` turns on the log that shows each write to DDS). attackzoo's `agent-source-install.sh` builds
  master, today v3.0.2, which we did not run.
- Attack in the README's form (`"<TARGET_IP>" "8888"`) with `-e DURATION_S=30` explicit.
- The datawriter's STATUS was read on the wire (submessage `000d00158000` = refusal, `000d00150000` = ok) with an XRCE
  decoder of ours; the writes, in the agent log.
- Runs: STATUS 0x80 showed up in the 9 runs without this commit (upstream, the 2 diagnostic variants and XRCE-01); with
  this commit, 1 run (30 s, with agent log), with the wire the same as in the 4 runs with XRCE-01 only.
- Load: load average 2.2 to 4.5 with other tests on other bridges.
- Independent review: a second reviewer recounted STATUS and writes with their own parser and in the raw agent log, and
  read the Agent v3.0.2 path (same logic, no execution).
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `attack.yaml` does not change.
- Declared deviation: the measured image also had the `setvbuf(stdout, NULL, _IOLBF, 0)` line, outside this PR; it only
  changes the stdout buffer [inferred].

**Fix.** One line: `datawriter_xml` stops being empty and now describes a data_writer with the same topic
(`HelloWorldTopic`) and the same type (`HelloWorld`) that the attack already creates at `:140`, `kind` `NO_KEY`, in a
single-line string like the other XML in the file (`:136`, `:140`). Below, broken only for reading:

```xml
<dds><data_writer><topic><kind>NO_KEY</kind>
<name>HelloWorldTopic</name><dataType>HelloWorld</dataType>
</topic></data_writer></dds>
```

Nothing else changes.

**Before and after.** Same conditions; BEFORE is the image with XRCE-01, because without it nothing reaches the
datawriter.

| Measure | Before (with XRCE-01) | After (XRCE-01 + this commit) |
|---|---|---|
| STATUS of the datawriter's CREATE | 0x80 (error) | 0x00 (ok) |
| Error lines in the agent log | 1 (`{argument not found}`) | 0 |
| Writes to DDS (agent log) | 0 | 750 (50 x 32,000 B, 200 x 16,000 B, 500 x 8,000 B) |
| FRAGMENT / FLAG_LAST / retransmissions | 36,300 / 750 / 0 | 36,300 / 750 / 0 |

The 750 writes also prove that the agent reassembles all 750 messages whole [measured].

**How to reproduce.** In the reproduction file, section XRCE-02; uses P1, P2, P6.

**Caveats.**
- It only has an effect with XRCE-01: without it no message reaches the datawriter.
- Measured with Agent v3.0.1; in v3.0.2, which attackzoo builds today, the refusal follows the same path by reading the
  code, with no execution.
- AFTER is 1 run; its wire repeated the counts of the 4 runs with XRCE-01 only.
- "Overlapping" stays out of XRCE's reach (see XRCE-01).
- Not tested: campaign path with `--network host`.

**Versions.**
- attackzoo `8613c66`; Micro-XRCE-DDS-Client v3.0.2 (`6884d7bd`); Micro-CDR v2.0.2 (`99672492`).
- Micro-XRCE-DDS-Agent run: v3.0.1 (`155cfaaf`) with Fast-DDS v3.6.2 (`39303846`) and Fast-CDR v2.2.8
  (`1bc9c919`); v3.0.2 (`a88c712b`) also read.
- Base `ubuntu:24.04` resolved on 2026-11-16, sha256 digest
  `73b999393d07f2bf65a40373778a44dc9a6d54ad7718d29247d8ff9413c4d6a8`; Docker 29.6.2; tcpdump 4.99.6; tshark 4.6.9.

### XRCE-03 · xrce-dds-time-desync: The Log Calls Nanoseconds Microseconds And Divides By 1e6 Calling It Seconds

| | |
|---|---|
| Class | (b) inconsistency between parts of attackzoo |
| In this PR | commit |
| Files | `docker/attackers/xrce-dds-time-desync/attack_time_desync.c` |
| Depends on | none |

**Promise.** The attack's own messages: `docker/attackers/xrce-dds-time-desync/attack_time_desync.c:31-32`
`"[*] Corrupted time offset to: %lld microseconds (%.2f seconds)\n"` with `malicious_offset / 1000000.0`, and `:62`
`"[Client %d] Desync iteration %d, offset: %lld us\n"`.

**What happens.** Each synchronization callback adds `10000000` to the session's `time_offset` (`:28-29`). For the
Micro-XRCE-DDS-Client that field is in nanoseconds, so each step is worth 10 ms, but the log says 10 s: the first line
is "Corrupted time offset to: 10000000 microseconds (10.00 seconds)" and the last of each child process is "1000000000
microseconds (1000.00 seconds)", when the real value is 1 s [measured]. A program of ours with the same callback, after
100 synchronizations (`time_offset` = 1e9), measures `uxr_epoch_millis - uxr_millis` = -1000 ms: for the library, 1e9 is
1 s [measured].

**Cause.** `:31` labels the value as microseconds, `:32` divides by `1000000.0` and calls it seconds, `:62` labels it
"us". In Client v3.0.2 (`6884d7bd`), `src/c/core/session/session.c:562` uses the field as nanoseconds
(`uxr_epoch_nanos = uxr_nanos() - session->time_offset`), and the default callback computes it in nanoseconds
(`:1191-1198`) [read in code].

**How we tested.**
- Images: BEFORE = `docker build` of 2026-11-16 of the upstream `8613c66` tree (`docker/` context; `install.sh` cloned
  Client `6884d7bd` = v3.0.2 and Micro-CDR `99672492` = v2.0.2); the binary has the same md5 (`239c91a4`) as an earlier
  build of ours with Client and Micro-CDR pinned to those same commits. AFTER = same recipe with this commit (binary
  `f73a7b97`); between the two binaries only the 2 format strings change.
- Agent: Micro-XRCE-DDS-Agent v3.0.1 (`155cfaaf`), `udp4 -p 8888 -v6`, a new one per case. The function that answers
  TIMESTAMP is the same in v3.0.2, which attackzoo builds today (`Processor.cpp:723-760` in v3.0.1, `:730-767` in
  v3.0.2, identical with `diff -w`) [read in code].
- IPs: agent `.10`, attacker `.20`, unit program `.40`. Attack in the README's form (`"<TARGET_IP>" "8888"`) with
  `-e DURATION_S=30`; it ends on its own, exit 0, in ~12.6 s, before the `timeout`.
- Count with tshark (TIMESTAMP = submessage `0x0e`, TIMESTAMP_REPLY = `0x0f`) and with a decoder of ours that reads the
  clock of each TIMESTAMP; `grep` on the attack log.
- Unit program: ours, with the same library and the same callback as the attack, 100 synchronizations.
- Runs: 1 with the BEFORE image and 1 with AFTER, with the same agent, network and arguments; plus 1 of the unit
  program.
- Load: load average 0.5 to 1.0, with no flood on the host.
- Independent review: a second reviewer recounted the 5 pcaps of the test, shared by XRCE-03 and XRCE-07 (BEFORE, AFTER,
  unit program, our client alone and during the attack), with tshark and their own parser, counted the lines of the
  logs, compared the binaries' strings and applied the patch with `git apply --check` to a clean `git archive` of
  `8613c66`.
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `attack.yaml` does not change.

**Fix.** Three `printf` lines: `:31` "microseconds" becomes "nanoseconds"; `:32` `/ 1000000.0` becomes
`/ 1000000000.0`; `:62` "us" becomes "ns". We chose to keep the value the code uses (10 ms per step) and fix the text;
the owner may prefer the opposite, changing the value to 10 s per step. Traffic and parameters do not change.

**Before and after.** Same agent, network, IPs and arguments; only the image changes.

| Measure | Before (`8613c66`) | After (with this commit) |
|---|---|---|
| Lines in the log / "Corrupted" lines | 2347 / 2000 | 2347 / 2000 |
| First "Corrupted" line | `10000000 microseconds (10.00 seconds)` | `10000000 nanoseconds (0.01 seconds)` |
| Largest value | `1000000000 microseconds (1000.00 seconds)` | `1000000000 nanoseconds (1.00 seconds)` |
| Iteration 90 | `offset: 910000000 us` | `offset: 910000000 ns` |
| CREATE_CLIENT / TIMESTAMP / DELETE / TIMESTAMP_REPLY | 20 / 2000 / 20 / 2000 | 20 / 2000 / 20 / 2000 |
| TIMESTAMP per second (per session / peak) | 9.95 / 200 | 9.95 / 200 |

**How to reproduce.** In the reproduction file, section XRCE-03; uses P1, P2, P3, P6.

**Caveats.**
- It only fixes the log text: the attack still alters nothing on the wire or outside its own session (XRCE-07).
- The fix assumes 10 ms per step is the intended value; it cannot be known from the code.
- Not tested: campaign path with `--network host` and Agent v3.0.2 in execution (the cause is local to the attacker)
  [inferred].

**Versions.**
- attackzoo `8613c66`; Micro-XRCE-DDS-Client v3.0.2 (`6884d7bd`); Micro-CDR v2.0.2 (`99672492`).
- Micro-XRCE-DDS-Agent run: v3.0.1 (`155cfaaf`); v3.0.2 (`a88c712b`) read.
- Base `ubuntu:24.04` resolved on 2026-11-16, sha256 digest
  `73b999393d07f2bf65a40373778a44dc9a6d54ad7718d29247d8ff9413c4d6a8`; Docker 29.6.2; tcpdump 4.99.6; tshark 4.6.9.

### XRCE-04 · xrce-dds-discovery-poison: Does Not Receive The XRCE Discovery, Answers In RTPS And Loops On Its Own Packet

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/xrce-dds-discovery-poison/attack_discovery_poison.c` |
| Depends on | none |

**Promise.** `docker/attackers/xrce-dds-discovery-poison/attack.yaml:5` and `README.md:3`: "Poisoning or manipulation of
XRCE-DDS agent discovery messages to induce incorrect association, redirection, or discovery degradation." The usage
printed by the binary itself (`attack_discovery_poison.c:319-321`): "1. Respond to discovery requests on port %d",
"2. Redirect clients to rogue agent at <ip>:<rogue_agent_port>", "3. Intercept all client communications". The
`target_ip` parameter is labeled "Advertised fake agent IP/FQDN" (`attack.yaml:23`).

**What happens.** In XRCE-DDS discovery (the DDS version for small devices), the client sends a GET_INFO to the
multicast group `239.255.0.2:7400` and accepts as an agent whoever answers with a valid XRCE INFO. The attack fails at
all three steps [measured]:
- It does not receive the GET_INFO: the request reaches the attack container's interface, but the kernel does not
  deliver it to the socket on 7400, because nothing in that netns (the container's network namespace) joined the group;
  the `Udp InDatagrams` counter stays at 0 and the client finds no agent.
- If a GET_INFO does arrive (unicast discovery pointed at the attacker), the reply is RTPS (DDS's wire protocol, another
  format), 64 B, and the XRCE Client refuses it: 3 of 3 replies, no agent found.
- Any datagram on 7400 triggers a loop that only stops when the process exits: a single 8 B datagram generated 277,424
  broadcasts in ~4 s (the attacker's loopback saw 277,423 copies addressed to itself), with a default route like the
  `docker0` one; with no default route, 1 reply and 0 broadcasts. The unicast GET_INFO itself also triggered the loop
  (465,169 broadcasts in 5.36 s).

**Cause.** The socket binds to `INADDR_ANY:7400` (`attack_discovery_poison.c:174-180`) and the file has no
`IP_ADD_MEMBERSHIP`; in Micro-XRCE-DDS-Client v3.0.2 (`6884d7b`), `src/c/profile/discovery/discovery.c:18-19,44-53,81`
sends the GET_INFO to `239.255.0.2:7400` [read in code]. The reply is built as RTPS at `:211-268`; the Client reads the
reply as XRCE and only accepts a complete INFO with activity type AGENT and XRCE version 1.0
(`discovery.c:163-167,197,204`) [read in code]. It is also not a valid SPDP DATA (readerId, writerId and writerSN are
missing before the locator) [read in code]. The loop: the same socket answers any datagram (`:193-198`), answers the
sender (`:271-272`; for its own packet the sender is its own IP:7400) and broadcasts to `255.255.255.255:7400`
(`:284-292`), which the kernel hands back to the same socket. That each reply generates two new requests is a reading of
the code; the mechanism was measured.

**How we tested.**
- Images: BEFORE = `docker build` of 2026-11-16 of the upstream `8613c66` tree (`docker/` context; Client `6884d7b` =
  v3.0.2, Micro-CDR `9967249` = v2.0.2). AFTER = same recipe with this commit; only the `.c` changes; build with no
  warnings.
- Discovery client: attackzoo has none (XRCE-08), so we used a program of ours with the same v3.0.2 library
  (`uxr_discovery_agents_default` for the default discovery, `uxr_discovery_agents` for the unicast one; if it finds an
  agent, it tries to open a session on it) and, in a later round, the client proposed in XRCE-11 (`discover` mode).
- Agent: Micro-XRCE-DDS-Agent v3.0.1 (`155cfaaf`), `udp4 -p 8888` without `-d` (as attackzoo starts it) or with
  `-d 7400` (control: the agent serves discovery). The attack does not talk to the agent. Also attackzoo's
  `client-super`, as it is in `8613c66`.
- Network: each container in a netns held by a container that only sleeps, and a helper with `NET_ADMIN` put
  `ip route add default dev eth0` in each netns, to imitate the default route of `docker0` (without it, broadcast and
  multicast give ENETUNREACH). The attack container got no capability.
- Attack: README form (`"<TARGET_IP>" "6666"`) with `TARGET_IP` = the IP of the attack's own container, as the label of
  `attack.yaml:23` asks; in the attackzoo scenario, `-e DURATION_S=60` and arguments `<agent IP> 8888`, our choice (the
  attack transmits nothing there, so the arguments do not change the result). Stopped by SIGTERM in place of
  `docker rm -f`, so stdout would reach the log.
- Capture also on the attacker's `eth0` and loopback when stated. Count with a pcap parser of ours and tshark filters;
  attack log (`Discovery request`, `Ignored`, `Intercepted`); `/proc/net/udp`, `/proc/net/igmp` and `/proc/net/snmp` of
  the attacker's netns.
- Scenarios, each with the BEFORE and the AFTER image: attackzoo scenario (agent without `-d`, `client-super xrce-dds`,
  60 s); the Client's default discovery; unicast discovery to the attacker; a single 8 B trigger with `nc -u` on 7400;
  agent with `-d` (3 attempts). The trigger with no default route, only with the BEFORE image. With the XRCE-11 client
  and the agent without `-d`: 1 run with the BEFORE image and 2 with AFTER.
- Load: load average 3.9 to 5.1 (3.1 to 6.0 in the runs with the XRCE-11 client), with other tests part of the time;
  the rates are indicative only.
- Independent review: a second reviewer recounted all pcaps and logs with their own parser and redid one measurement
  with the untouched upstream image (quiet host, load 0.45): the multicast GET_INFO reaches the attacker's `eth0` and
  the kernel does not deliver it (`Udp InDatagrams` 0 -> 0, `InMcastPkts` 0 -> 0); with another process in the same
  netns joining the group, the SAME upstream binary receives and answers RTPS, and the Client refuses. They also decoded
  the fix's INFO field by field against `discovery.c:151-188` and applied the patch to a clean `git archive` of
  `8613c66`.
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `attack.yaml` does not change.
- Not tested: the campaign path (`--network host`, `--target 127.0.0.1 --port 6666`).

**Fix.** On the 7400 socket: (1) `IP_ADD_MEMBERSHIP` on `239.255.0.2`, the default discovery group; (2) the reply
becomes a 44 B XRCE INFO in the layout the Agent itself uses (little endian, header copied from the request, type AGENT,
cookie "XRCE", version 1.0, eProsima vendor, 1 locator = `target_ip:target_port`); (3) it only answers GET_INFO (header
without client key and submessage `0x02`, with at least 12 B); the rest, including the INFO that comes back through the
loopback and the broadcast, is ignored and logged ("Ignored non-GET_INFO datagram"). The RTPS structures that were left
unused are removed. The broadcast to `255.255.255.255:7400` was kept, now with the INFO: it is harmless and useless,
because the clients listen on an ephemeral port. Arguments, `attack.yaml` and entrypoint do not change.

**Before and after.** Same network, routes, IPs, agent and arguments; only the attack image changes.

| Condition | Before (`8613c66`) | After (with this commit) |
|---|---|---|
| attackzoo scenario (agent without `-d`, `client-super`, 60 s) | 0 UDP datagrams from the attacker | 0 UDP datagrams (only 4 IGMP, joining and leaving the group) |
| Client's default discovery (our program) | GET_INFO reaches the interface, 0 at the socket; no agent found | 1 INFO of 44 B; the client finds the fake agent (`.20:6666`) |
| Unicast discovery to the attacker (our program) | 3 RTPS replies, refused | INFO accepted; the client sends 10 CREATE_CLIENT to the fake agent |
| XRCE-11 client in `discover`, agent without `-d` | 3 GET_INFO, 0 fake INFO, client exits with 1 | 3 fake INFO, 15 CREATE_CLIENT to the fake agent, 0 sessions, exits with 1 |
| 1 datagram of 8 B on 7400, with default route | 277,424 broadcasts in ~4 s, until the process exits | 0 replies, 0 broadcasts, 1 "Ignored" line in the log |
| Agent with `-d 7400` competing (3 attempts) | the client finds the real agent 3 of 3 | the client finds the fake agent 3 of 3 (race: the fake one arrived 17 to 222 us earlier) |

**How to reproduce.** In the reproduction file, section XRCE-04; uses P1, P2, P3, P6, P7.

**Caveats.**
- The commit fixes the discovery reception, the reply format and the loop. It does not make the attack reach the
  "incorrect association": the fake agent answers RTPS to CREATE_CLIENT and no session opens (XRCE-09).
- With `-d 7400` on the real agent it is a race: the attacker won by 17 to 222 us in the 3 attempts, it is not a
  guarantee.
- In the attackzoo scenario nothing triggers the attack, before or after (XRCE-08).
- The test used a discovery client of ours and the XRCE-11 client, because attackzoo has no client that does XRCE
  discovery.
- On the campaign path (`--network host`, `--target 127.0.0.1 --port 6666`), `target_ip` becomes the advertised locator:
  with the fix, the INFO would advertise `127.0.0.1:6666`, the client's own loopback [read in code and in a simulation of
  the campaign script, not tested]. On that path, joining the group with `INADDR_ANY` and the broadcast would go out
  through the host's default-route interface, the LAN [read in code].
- The loop's rates come from a loaded host (load 3.9 to 5.1); they serve only as an order of magnitude.

**Versions.**
- attackzoo `8613c66`; Micro-XRCE-DDS-Client v3.0.2 (`6884d7b`); Micro-CDR v2.0.2 (`9967249`).
- Micro-XRCE-DDS-Agent run: v3.0.1 (`155cfaaf`), which joins the group with `-d` in
  `DiscoveryServerLinux.cpp:86-89`; today's master is v3.0.2 (`a88c712b`).
- Base `ubuntu:24.04` resolved on 2026-11-16, sha256 digest
  `73b999393d07f2bf65a40373778a44dc9a6d54ad7718d29247d8ff9413c4d6a8`; Docker 29.6.2; tcpdump 4.99.6; tshark 4.6.9.

### XRCE-05 · xrce-dds-session-hijack: The Datawriter Is Created With Empty XML And The 100 Injections Are Discarded

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/xrce-dds-session-hijack/attack_session_hijack.c` |
| Depends on | none |

**Promise.** `docker/attackers/xrce-dds-session-hijack/attack.yaml:5`: "XRCE-DDS session hijacking or collision attempts
through manipulation of identifiers, keys, or session fields." `attack.yaml:18-19` maps to T1565 and T1565.002
(Transmitted Data Manipulation). The code creates a participant, topic, publisher and datawriter
(`attack_session_hijack.c:61-99`) and announces the injection: `:110` "[*] Injecting malicious messages...", `:124`
"[+] Injected message %d", for 100 messages "INJECTED_MESSAGE_%d: System Compromised" (`:112-131`).

**What happens.** In XRCE-DDS (the DDS version for small devices), the client asks the agent to create the DDS
entities; the datawriter is the one that publishes to a topic. The hijack itself works: with a legitimate client on key
`0xAAAABBBB`, the agent hands the key to the attacker ("session re-established"), erases the legitimate client's
entities, the legitimate client's next data does not arrive and it exits [measured]. But the injection does not happen:
the agent answers STATUS 0x80 (error) to the datawriter's CREATE, in 5 of 5 runs; the 100 WRITE_DATA (data submessages)
with "INJECTED_MESSAGE" go out on the wire and the agent discards them: 0 injected writes to DDS (in the 4 runs with
detailed log) and 0 injected messages at a subscriber of `HelloWorldTopic` (in the 3 with a subscriber) [measured].
Participant, topic and publisher are created (STATUS 0x00), and the agent announces the participant `HACKED_PARTICIPANT`
in DDS by SPDP (6 announcements at 100 ms, then 1 every 3 s; the count depends on the window) [measured].

**Cause.** `attack_session_hijack.c:97`: `const char* datawriter_xml = "";`, passed to `uxr_buffer_create_datawriter_xml`
at `:98-99`. In Micro-XRCE-DDS-Agent v3.0.2 (`a88c712b`), `src/cpp/middleware/fastdds/FastDDSEntities.cpp:774-795`: with
`xml.size() == 0` the `topic_name` is empty, `find_local_topic("")` finds no topic and the creation fails;
`src/cpp/client/ProxyClient.cpp:531-533` turns the failure into `STATUS_ERR_DDS_ERROR`, which is 0x80
(`include/uxr/agent/types/XRCETypes.hpp:6682`); `src/cpp/processor/Processor.cpp:460-467` discards WRITE_DATA to a
nonexistent datawriter, with no reply [read in code]. In the v3.0.1 we ran the path is the same
(`FastDDSEntities.cpp:764-775`, `Processor.cpp:459-464`) [read in code]. The official example the attack was copied from
has the XML (`examples/PublishHelloWorld/main.c:95-103` of Client v3.0.2) [read in code]. The hijack comes from
`Root.cpp:118-128` in v3.0.1 (`:145-157` in v3.0.2: same key and same session_id reuse the client),
`SessionManager.hpp:69-79` in v3.0.1 (`:72-82` in v3.0.2: the key moves to the new address) and `Processor.cpp:79-92` in
v3.0.1 (`:80-93` in v3.0.2: the key is resolved by the source address) [read in code].

**How we tested.**
- Images: BEFORE = `docker build` of 2026-11-16 of the upstream `8613c66` tree (`docker/` context; Client `6884d7bd` =
  v3.0.2, Micro-CDR `99672492`); the binary has the same md5 (`cb4a9548`) as an earlier build of ours with Client and
  Micro-CDR pinned to those same commits. AFTER = same recipe with this commit; same `libmicroxrcedds_client.a` (md5
  `a5977160`); only the `.c` and the binary change.
- Agent: Micro-XRCE-DDS-Agent v3.0.1 (`155cfaaf`, Fast-DDS v3.6.2), a new one per run, `udp4 -p 8888 -v6`, and the exact
  `udp4 -p 8888` of `docker/servers/xrce-dds-agent/server.yaml:15` in two runs. attackzoo's `agent-source-install.sh`
  builds master, today v3.0.2, which we did not run.
- Victims, assembled by us because attackzoo has no real XRCE client: the official examples `PublishHelloWorld` (key
  `0xAAAABBBB`) and `SubscribeHelloWorld` (key `0xCCCCDDDD`) of the same Client `6884d7bd`, compiled with the flags of
  the attack's `compile.sh`. Later, the client proposed in XRCE-11 as the victim.
- Attack in the README's form (`"<TARGET_IP>" "8888"`) with `-e DURATION_S=30`; it exits by `timeout` (exit 124). One
  BEFORE run with `DURATION_S=120`.
- Count with an XRCE decoder of ours and with tshark (`frame contains "INJECTED_MESSAGE"` coming from the agent; the
  datawriter's STATUS in the payload that contains `00:0d:00:15`), in the agent log (`datawriter created`,
  `DataWriter.cpp | write`) and in the subscriber log (`Received topic`).
- Runs: BEFORE 5 (attack only, with and without `-v6`; with subscriber; with subscriber and legitimate publisher; with
  subscriber and 120 s); AFTER 4 (the same, minus the 120 s one). With the XRCE-11 client as the victim, 3 runs with each
  image.
- Load: load average 0.2 to 1.4, no flood, in the main runs; 3.3 to 5.4 in the runs with the XRCE-11 client.
- Independent review: a second reviewer redid the counts with a pcap and XRCE parser of their own, without tshark or our
  scripts, and with the raw agent logs; checked the md5 of the binaries in the images, applied the patch to a clean `git
  archive` of `8613c66` and compared the XML with the example's, line by line.
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `attack.yaml` does not change.

**Fix.** `:97` receives the datawriter XML from the `PublishHelloWorld` example itself (topic `HelloWorldTopic`, type
`HelloWorld`, `NO_KEY`), in the file's concatenated-string style (`:62-68`, `:74-79`). Keys, window, number of messages,
keepalive and `attack.yaml` do not change.

**Before and after.** Same network, IPs, agent and victims; only the attack image changes.

| Run | Datawriter STATUS | Writes to DDS (agent log) | INJECTED at the subscriber |
|---|---|---|---|
| Attack only | 0x80 -> 0x00 | 0 -> 100 | no subscriber |
| Attack only, exact args of `server.yaml:15` | 0x80 -> 0x00 | no detailed log | no subscriber |
| Attack and subscriber | 0x80 -> 0x00 | 0 -> 100 | 0 -> 79 |
| Attack, subscriber and legitimate publisher | 0x80 -> 0x00 | 11 -> 111 (the 11 are the legitimate client's) | 0 -> 84 |
| XRCE-11 client as the victim (3 runs each) | 0x80 -> 0x00 | injected: 0 -> 100, 100, 100 | 0 -> 71, 74, 73 |

The hijack happened in both versions: in the run with a legitimate publisher and in the 6 runs with the XRCE-11 client
(3 of 3 in each version), 1.3 to 2.6 s after the attack container started [measured].

**How to reproduce.** In the reproduction file, section XRCE-05; uses P1, P2, P6.

**Caveats.**
- Measured with Agent v3.0.1 and Fast-DDS 3.6.2. In v3.0.2 with Fast-DDS 3.3.x, which attackzoo builds today, the
  refusal path is the same by reading the code (it does not go through Fast-DDS); AFTER on that agent was not measured
  (there is no ready image on Docker Hub and the build risked exhausting memory).
- Of the 100 writes, the subscriber received 79 and 84 (71 to 74 in the runs with the XRCE-11 client). The loss is inside
  the agent, between the subscriber's DDS reader and the XRCE stream, not on the wire; the cause was not investigated.
- The victims are our own setup. In the attackzoo flow there is no legitimate XRCE client, so there the "hijack" is just
  a new session (the log says "session established") [measured].
- The attack's CREATE_CLIENT declares MTU 508 on the wire (512 is the transport buffer), above the minimum of 13 that
  Agent v3.0.2 started to require [measured; read in code]; so v3.0.2's new validation would not refuse this session
  [inferred].
- The 30 s window covers only the first of the 7 keys; XRCE-10 suggests raising the duration.
- Not tested: campaign path with `--network host` and Agent v3.0.2 in execution.

**Versions.**
- attackzoo `8613c66`; Micro-XRCE-DDS-Client v3.0.2 (`6884d7bd`, also the source of the official examples used as the
  victim); Micro-CDR v2.0.2 (`99672492`).
- Micro-XRCE-DDS-Agent run: v3.0.1 (`155cfaaf`) with Fast-DDS v3.6.2 (`39303846`) and Fast-CDR v2.2.8
  (`1bc9c919`); v3.0.2 (`a88c712b`) read.
- Base `ubuntu:24.04` resolved on 2026-11-16, sha256 digest
  `73b999393d07f2bf65a40373778a44dc9a6d54ad7718d29247d8ff9413c4d6a8`; Docker 29.6.2; tcpdump 4.99.6; tshark 4.6.9.

## Commits: Zenoh

### ZEN-01 · zenoh-pico-keepalive-flood: No KEEP_ALIVE Reaches The Router (UDP Against A TCP-only Router, Another Message's ID, No Session)

| | |
|---|---|
| Class | (a) the code does something other than what it promises; the transport part (UDP against attackzoo's own TCP-only router) is also (b) |
| In this PR | commit |
| Files | `docker/attackers/zenoh-pico-keepalive-flood/attack_dos_keepalive_flood.c` |
| Depends on | none |

**Promise.**
- `docker/attackers/zenoh-pico-keepalive-flood/attack.yaml:5` (same in `README.md:3`): "Flood of Zenoh/Zenoh-Pico keepalive messages to consume processing and session-handling capacity."
- `attack_dos_keepalive_flood.c:2-3`: "Attack 1: DoS - KEEP_ALIVE Flood" / "Floods router with KEEP_ALIVE messages"; `attack.yaml:14-19` lists TA0040, T1498, T1498.001, T1499, T1499.002 (denial of service).
- Target: `attack.yaml:9-10` `target_services: - zenoh-router`. The `zenoh-router` server declares itself TCP-only: `docker/servers/zenoh-router/server.yaml:11-14` (`7447/tcp`, `7447:7447/tcp`), `README.md:16-17`; and says it serves this attack, `README.md:3`: "Serve as a Zenoh router for Zenoh-Pico attacks against fragmentation, keepalive, memory, fuzzing, sequence, and timestamp behavior."

**What happens.** The Zenoh router (the `zenohd` 1.7.2 process that the `zenoh-router` server starts) receives no KEEP_ALIVE (the "I am still alive" message of a Zenoh session) [measured]:
- In the attackzoo flow the attack sends 1,669,400 1-byte UDP datagrams (`02`) to port 7447 in ~7 s. The router kernel's `Udp NoPorts` counter (datagrams that reach a UDP port with no listener) rises by exactly 1,669,400 (100%); the router answers only 12 ICMP port unreachable (the kernel rate-limits) and nothing else; router CPU 0.1%; the router lists only the 2 sessions of our test client. Two other runs (2026-11-13 and 2026-11-16): 1,680,500 and 1,598,800 datagrams, `Udp NoPorts` = 100%, CPU 0.00%.
- Even with UDP port 7447 forcibly opened on the router (a diagnostic outside the attackzoo flow), every router reply is CLOSE INVALID (bytes `03 02`) and no session opens; the `02` byte alone gives "Decode error" in the log.
- Over TCP, a correct KEEP_ALIVE (`04`) as the first message, without opening a session: the router answers CLOSE INVALID in 0.35 ms and closes the connection; log: "Received invalid message instead of an InitSyn ... at io/zenoh-transport/src/unicast/establishment/accept.rs:177".

**Cause.**
- Transport [read in code]: `attack_dos_keepalive_flood.c:42` `socket(AF_INET, SOCK_DGRAM, 0)` and `:61` `sendto`. The router only listens on TCP: `docker/servers/zenoh-router/Dockerfile:1-2` (`FROM eclipse/zenoh:1.7.2`, `EXPOSE 7447`, no arguments); `servers.sh:119` publishes `-p 7447:7447`, which is TCP only. In Zenoh 1.7.2 `zenohd` starts as a router (`zenohd/src/main.rs:118-119`) and, without `-l`, listens only on `tcp/[::]:7447` (`commons/zenoh-config/src/defaults.rs:167-181`, line `:174`; `main.rs:180`). The `eclipse/zenoh:1.7.2` image runs `zenohd` with the container's arguments, here none (`eclipse-zenoh/ci`, `publish-crates-docker/Dockerfile:11-14`, read at commit `49a77d5`); the only UDP port it declares is 7446 for scouting (discovery by multicast).
- ID [read in code]: `:18` `#define Z_MSG_KEEP_ALIVE 0x02`. In Zenoh 1.7.2 the ID is the low 5 bits of the first byte (`commons/zenoh-protocol/src/common/mod.rs:23-28`) and `commons/zenoh-protocol/src/transport/mod.rs:54-61` defines OAM (operation and maintenance message) `0x00`, INIT `0x01`, OPEN `0x02`, CLOSE `0x03`, KEEP_ALIVE `0x04`, FRAME `0x05`, FRAGMENT `0x06`, JOIN `0x07`: `0x02` is OPEN. 1.0.0 is identical; 0.7.2-rc and 0.5.0-beta.9 also do not match (KEEP_ALIVE `0x08`).
- Session [read in code]: the attack sends the flood from the first packet (`:40`, `:59-63`). In 1.7.2 the first message of a connection has to be InitSyn (the INIT without the A flag, which opens the session), otherwise the router closes with `close::reason::INVALID` (`io/zenoh-transport/src/unicast/establishment/accept.rs:162-183`). Over TCP each batch (Zenoh's unit of sending) is preceded by 2 little-endian bytes with the size (`io/zenoh-transport/src/common/batch.rs:311-322`; reading in `io/zenoh-transport/src/unicast/link.rs:213-225`).

**How we tested.**
- Images: router `server-zenoh-router` built from attackzoo's `Dockerfile` at `8613c66` (zenohd v1.7.2-790faadb), running without arguments and with the image's own `RUST_LOG=info` (`debug` log only in the diagnostics and in the runs with the router paused in the middle of the flood). BEFORE attack built from `8613c66` (the `.c` inside the image has the same md5 as the source); AFTER, same recipe with this commit.
- Network: fixed IPs (our client `.30`); `--memory 1g --memory-swap 1g` on all containers.
- Attack: the `docker run` that `python3 attackzoo.py run iot_zenoh_pico_keepalive_flood --target <IP> --port 7447` generates (defaults filled in at `modules/attackzoo/commands.py:248-255`, command assembled at `modules/runners.py:147`): `-e DURATION_S=10 -e THREADS=4 <image> <router IP> 7447`. The attack stops through the `timeout --preserve-status -s INT` of `entrypoint.sh:7`.
- Count: in BEFORE, BPF and tshark filters (datagrams, first byte, ICMP) and the `/proc/net/snmp` delta read in the router's network namespace (`Udp NoPorts`, `Tcp PassiveOpens`). In AFTER, a parser of ours reassembles each TCP connection and walks the batches with the 2-byte prefix, as `zenohd` does, counting aligned KEEP_ALIVE (`01 00 04`) and any batch off the pattern. On the router side: cgroup CPU and memory every 0.25 s, the receive queue (`rx_queue`) from `/proc/net/tcp6` and the sessions the router itself lists in its admin space (`@/*/router`).
- Legitimate client: ours (Python, `eclipse-zenoh==1.7.2`), 2 sessions through the router, put and get every 0.5 s from 6 s before the attack. attackzoo has no Zenoh client that publishes or subscribes: `client-super` only opens and closes a TCP connection (`docker/clients/client-super/super-client.py:296-302`).
- Runs: BEFORE 3 (one in the same arrangement as AFTER, with a legitimate client); AFTER 2 with this commit.
- Load: up to 4 tests ran at the same time on the host (load 2 to 7.5).
- Forced scenarios (declared deviations, to test the send path and the stop path): router paused (`docker pause`) for 8 s in the middle of the flood, 4 runs; router paused at the end of the window; TCP listener that accepts and never answers; router paused and released 8 s after the start.
- Diagnostics (declared deviations): router with `-l udp/0.0.0.0:7447` and `debug` log; TCP probes with the right KEEP_ALIVE without opening a session.
- Independent review: at each stage, a reviewer who did not do the measurement recounted the pcaps with their own tools (their own pcap parser without tshark, or their own BPF and tshark filters in the UDP runs; never our scripts), redid the `/proc/net/snmp` and cgroup deltas, and checked the cited lines of attackzoo and Zenoh (tag 1.7.2 checked by `git ls-remote`). The numbers matched.
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `attack.yaml` does not change; `gcc -Wall -Wextra` with no warnings.
- Not tested: `THREADS` above 4; router with limited CPU; `connect()` against a target that drops SYN.

**Fix.** Only the `.c`; `attack.yaml`, `entrypoint.sh`, `README.md` and parameters (`target_ip`, `target_port`, `THREADS`, `DURATION_S`) do not change.
- TCP + `connect`; each thread opens a session: InitSyn (version `0x09`, role client, random 16-byte zid (node identifier)) → reads the InitAck cookie (the router's reply to the InitSyn) → OpenSyn (the message that completes the opening; lease of 10 s, the idle time after which the session drops; initial SN, the sequence number, 0; cookie) → waits for the OpenAck (the router's confirmation).
- Then, the same loop as upstream (`BURST_SIZE` 100, `usleep(1000)`), with each message = `01 00 04` (size 1 + KEEP_ALIVE `0x04`).
- `send_all` completes partial sends and retries on EAGAIN/EINTR while the attack runs: over TCP, a cut-off message misaligns the following batches and the router closes the session.
- Stop: `SO_SNDTIMEO` of 1 s after the handshake, `SO_RCVTIMEO` of 1 s before the `connect` and the burst loop checking `g_running`, so the SIGINT from the entrypoint's `timeout` ends the attack even with the router stopped reading or silent.
- It changes the transport from UDP to TCP, which is what the router declares; the attack's text does not mention UDP. Alternative tested and discarded: opening `udp/7447` on the router is not enough (CLOSE INVALID, the session is still required).
- Note [read in code, not measured]: `connect()` still has no deadline. Against a target that drops SYN (a filter), the thread stays in `connect` until the kernel's SYN retransmissions end (~127 s at the Linux default), and SIGINT goes to the main thread. Not reproducible without filtering SYN (a nonexistent target gives EHOSTUNREACH in ~3 s; a paused router completes the TCP handshake). Possible adjustment, not applied: put `SO_SNDTIMEO` before the `connect` (changes the behavior with slow SYN).

**Before and after.** Same router, same network arrangement, same arguments, same legitimate client and same measurement scripts; only the attack image changes. BEFORE is the run with a legitimate client; AFTER, the 2 runs of this commit, made later in the same arrangement.

| | BEFORE (8613c66) | AFTER (this commit, 2 runs) |
|---|---|---|
| on the wire | 1,669,400 1-byte UDP datagrams `02`, 0 TCP | 4 TCP connections: InitSyn, OpenSyn and KEEP_ALIVE |
| KEEP_ALIVE that reach `zenohd` | 0 (`Udp NoPorts` = 1,669,400, 100%) | 2,391,824 and 2,395,933 aligned, 0 batches off the pattern |
| router reply | 12 ICMP port unreachable, nothing else | InitAck, OpenAck and KEEP_ALIVE per session; 0 FIN/RST; 0 zero window |
| sessions the router lists during the flood | 2 (only the legitimate client) | 6 (2 from the client + 4 from the attack) |
| router CPU in the flood | 0.1% | 91.5% and 75.7% (~1 core) |
| legitimate client | 0 failures (median put 0.3 ms) | 0 failures in 60 of 60 probes per run |
| exit after the `timeout` SIGINT | router paused: 0.00 and 0.01 s (UDP does not block); router up: not measured | router up: 0.00 to 0.02 s; router paused or listener silent: 0.17 to 1.00 s, exit 0 |

Measured effect: router CPU (~1 core) and 4 busy sessions, which fulfills `attack.yaml:5`. Denial of service was not observed: with `THREADS=4` on an 8-CPU host the legitimate client had no failures. With the router paused for 8 s in the middle of the flood (4 runs, fix version with the same send loop), none of the 16 sessions dropped.

**How to reproduce.** In the reproduction file, section ZEN-01; uses P1, P2, P3, P4, P5.

**Caveats.**
- CPU only as an order of magnitude (other tests were running on the host).
- The "0 batches off the pattern" of AFTER (no decode error) comes from the pcap (all batches `01 00 04` to the end) and from the live sessions in the admin space, not from the log: with `RUST_LOG=info` the router would not log that error.
- The router acknowledges all bytes, except the last ones sent ~1 ms before the RST with which the attacker closes each connection.
- The misalignments that `send_all` avoids were only provoked with the router forced to stop reading for more than 1 s; in the normal flow they did not happen.
- Not tested: campaign path, `docker0`, larger `THREADS`, router with limited CPU, `connect()` against a target that drops SYN (see the note in the Fix).

**Versions.** Router: `eclipse/zenoh:1.7.2` (zenohd v1.7.2-790faadb; source read at tag 1.7.2, commit `790faad`); IDs also checked at tags 1.0.0 (`6231698`), 0.7.2-rc (`b9103c3`) and 0.5.0-beta.9 (`70d7b22`). Attack: `ubuntu:24.04` + `build-essential` (gcc 13.3.0), no pin, as upstream. Legitimate client: `eclipse-zenoh` 1.7.2 (Python). Docker 29.6.2.

### ZEN-02 · zenoh-pico-fragments-reassembly: No Fragment Reaches The Router's Reassembly

| | |
|---|---|
| Class | (a) the code does something other than what it promises; the transport part (UDP against the router, which is TCP-only in attackzoo itself) is also (b) |
| In this PR | commit |
| Files | `docker/attackers/zenoh-pico-fragments-reassembly/attack_fragment_bomb.c` |
| Depends on | none |

**Promise.**
- `docker/attackers/zenoh-pico-fragments-reassembly/attack.yaml:5` (same in `README.md:3`): "Flood of incomplete Zenoh/Zenoh-Pico fragments to stress router or peer buffers and reassembly logic."
- `attack_fragment_bomb.c:2-3`: "Attack 3: Fragment Bomb" / "Sends incomplete fragments to exhaust reassembly buffers"; `:133`: "Attack: Incomplete fragments (never complete)".
- Target: `attack.yaml:9-10` `target_services: - zenoh-router`, which declares itself TCP-only (`docker/servers/zenoh-router/server.yaml:11-14`, `README.md:16-17`).

**What happens.** No FRAGMENT (the Zenoh message that carries a piece of a large message, kept by the router until the last one arrives) reaches the reassembly [measured]:
- In the attackzoo flow: 176,050 UDP datagrams to port 7447, all with first byte `0x61`; the router's `Udp NoPorts` (datagrams to a UDP port with no listener) = 176,050 (100%); 15 ICMP port unreachable; 0 TCP; router CPU 0.00%; memory 1.15 MiB, flat. Our test client receives 100% before, during and after.
- With UDP port 7447 forcibly opened (diagnostic): `zenohd` reads `0x61` as InitAck (INIT with the A and S flags) in 7,223 of 15,272 datagrams and gives "Decode error" on the others; every router response is CLOSE INVALID (`03 02`) and no session opens.

**Cause.**
- Transport [read in code]: `attack_fragment_bomb.c:72` `socket(AF_INET, SOCK_DGRAM, 0)` and `:93` `sendto`; the router only listens on TCP (`docker/servers/zenoh-router/Dockerfile:1-2`; Zenoh 1.7.2 `commons/zenoh-config/src/defaults.rs:167-181`, router at `:174`; `servers.sh:119` publishes only TCP).
- ID [read in code]: `:17` `#define Z_MSG_FRAGMENT 0x01`, used at `:48`. In Zenoh 1.7.2 `0x01` is INIT and FRAGMENT is `0x06` (`commons/zenoh-protocol/src/transport/mod.rs:55,60`); the M (`0x40`, "more comes") and R (`0x20`, reliable) flags are right (`transport/fragment.rs:20-21`).
- Session [read in code]: the attack sends fragments from the first packet; the router closes the connection whose first message is not InitSyn (`io/zenoh-transport/src/unicast/establishment/accept.rs:162-183`; InitSyn and OpenSyn are the client messages that open the Zenoh session, and InitAck and OpenAck are the router's replies); over TCP each batch (Zenoh's unit of sending) is preceded by 2 bytes with its size (`io/zenoh-transport/src/common/batch.rs:311-322`).
- The reassembly the promise aims at [read in code]: `io/zenoh-transport/src/unicast/universal/rx.rs:180-192` stores each fragment and only delivers when one without the M flag arrives; `io/zenoh-transport/src/common/defragmentation.rs:66-91` only clears the buffer if the SN (sequence number) jumps or if it exceeds the capacity, which is `max_message_size` = 2^30 bytes (`commons/zenoh-config/src/defaults.rs:319`; `io/zenoh-transport/src/manager.rs:291,428`). With M always on and a consecutive SN, the buffer only grows, per channel (session and priority).

**How we tested.**
- Machine, images, network and capture as in ZEN-01: router `server-zenoh-router` built from `8613c66` (zenohd v1.7.2), no arguments, the image's `RUST_LOG=info`; `--memory 1g --memory-swap 1g` on router, attack and client.
- Attack: the `docker run` that `attackzoo.py run iot_zenoh_pico_fragments_reassembly --target <IP> --port 7447` generates: `-e DURATION_S=10 -e THREADS=4 <image> <router IP> 7447`; stopped by the `timeout --preserve-status -s INT` in `entrypoint.sh:7`. BEFORE = image from `8613c66`; AFTER = image with this commit (md5 of the `.c` inside the image = source).
- Count: in BEFORE, BPF and tshark filters and the router's `/proc/net/snmp` delta. In AFTER, a parser of ours reassembles the TCP connections, splits the batches by the 2-byte prefix and redoes the 1.7.2 reassembly path (SN and capacity check). Router memory and CPU from `docker stats` (~1 per second); out-of-memory (OOM) death from `docker inspect` (`OOMKilled=true`).
- Runs: BEFORE 1, plus 1 with a legitimate client; AFTER 2 (the first with an image that differs from this commit only in whitespace in `main()`), plus 1 with a legitimate client and 1 of 3 s with the router at `trace` log level (only the log level changes) to see each fragment decoded.
- Legitimate client: ours (Python, `eclipse-zenoh==1.7.2`), put at 50 Hz and get at 2 Hz through the router, from 8 s before the attack. attackzoo has no Zenoh client that publishes or subscribes (`super-client.py:296-302` only opens a TCP connection).
- Load: load ~5 (another test running); only the counts and the OOM support the conclusion.
- Stop (forced): with the router paused (`docker pause`) before the handshake, the threads give up in ~5 s and the process exits 0.00 s after the SIGINT; paused during the flood, it exits 1.07 s after the SIGINT.
- Independent review: a second reviewer recounted BEFORE with their own tshark filters and `/proc/net/snmp`, counted the AFTER FRAGMENTs with their own parser (without our scripts), checked the OOM in `docker inspect` and, in the client logs, the contrast between everything delivered in BEFORE and nothing delivered after the OOM (the exact split by phase, in the table, was not recounted by them). It matched; their caveat about the memory cap is below.
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `attack.yaml` does not change.
- Not tested: the router without a memory cap (as attackzoo starts it).

**Fix.** Only the `.c`, 3 hunks, `main()` untouched; `attack.yaml`, `entrypoint.sh` and parameters do not change. It is a large rewrite (~140 lines of TCP session opening), the same as in the other `zenoh-pico-*`, because reassembly only exists inside a session.
- TCP + `connect` + session opening: InitSyn (version `0x09`, client, random 16-byte zid (node identifier)) → from the InitAck it reads the cookie and the SN resolution (S flag) → OpenSyn (10 s lease, initial SN = thread base, cookie) → OpenAck.
- Each fragment: FRAGMENT header `0x06` | M `0x40` | R `0x20`, thread SN masked to the negotiated resolution, same sizes as upstream (512, 1024, 2048 bytes), SN advances by 1 (upstream already did `seq++`), per-thread base `thread_id * 1e6`. It never sends the final fragment: "incomplete fragments (never complete)".
- Batch with a 2-byte prefix; `send_all` completes partial sends; `SO_SNDTIMEO` of 1 s and `SO_RCVTIMEO` of 5 s before `connect`, so the `timeout`'s SIGINT can end a stuck thread.
- The SN mask table repeats `io/zenoh-transport/src/common/seq_num.rs:17-20` converted to `TransportSn = u32` (`commons/zenoh-protocol/src/transport/mod.rs:99`): `0x7F`, `0x3FFF`, `0x0FFFFFFF`, `0xFFFFFFFF`. The 64-bit entry is `(u64::MAX >> 1) as u32` and was never used: the router answered U32 in every measured session.
- The default router does not require first-fragment markers: all were accepted without them [measured].

**Before and after.** Same router (`--memory 1g`), network and arguments; only the attack image changes.

| | BEFORE (8613c66) | AFTER (this commit) |
|---|---|---|
| on the wire | 176,050 UDP datagrams (`0x61`), 0 TCP | 4 TCP connections: InitSyn, OpenSyn and 128,895 FRAGMENT |
| reaches the reassembly | nothing (`Udp NoPorts` = 176,050, 100%) | 128,895 (32,199 + 32,348 + 32,199 + 32,149); in the code replay, 0 dropped by SN or capacity |
| decoding at the router (`trace` log, 3 s) | n/a | 56,947 of 57,000 sent decoded as Fragment, 0 errors |
| router response | 15 ICMP port unreachable | InitAck, OpenAck and KEEP_ALIVE per session |
| router CPU | 0.00% | 79 → 98 → 108% |
| router memory | 1.15 MiB, stable | 1.15 → 122.8 → 423 → 724.5 MiB in ~4 s, then killed by OOM; 2nd run: peak 774.9 MiB, OOM |
| legitimate client | 100% delivered in the 3 phases | during: 382 of 544 put (162 lost), 15 of 22 get; after the OOM: 0 of 740 put, 0 of 29 get |

**How to reproduce.** In the reproduction file, section ZEN-02; uses P1, P2, P3, P4, P5.

**Caveats.**
- The measured OOM is under `--memory 1g`. attackzoo starts the router without a cap: what the code guarantees is that the reassembly buffer accumulates per channel up to the default of 2^30 bytes, at low cost to the attacker; without a cap, the limit becomes the host's memory [inferred, not measured].
- The AFTER "accepted in the reassembly" count for 10 s is a code replay over the pcap; the router's decoding was seen in the `trace` log only in the 3 s run.
- The legitimate client's loss numbers depend on the phase boundary (before, during, after the OOM) and only the delivered/not delivered contrast was checked by the reviewer; that is what matters.
- Not tested: router without a cap, campaign path, `docker0`.

**Versions.** Router: `eclipse/zenoh:1.7.2` (zenohd v1.7.2-790faadb; source read at tag 1.7.2, commit `790faad`). Attack: `ubuntu:24.04` + `build-essential` (no pin, as in upstream). Legitimate client: `eclipse-zenoh` 1.7.2 (Python). Docker 29.6.2.

### ZEN-03 · zenoh-pico-sequence-exhaustion: No FRAME Reaches The Router; Fixed, It Consumes CPU But Does Not Degrade Ordering Or Reliability

| | |
|---|---|
| Class | (a) the code does something other than what it promises; the transport part (UDP against the router, which is TCP-only in attackzoo itself) is also (b) |
| In this PR | commit |
| Files | `docker/attackers/zenoh-pico-sequence-exhaustion/attack_sequence_exhaustion.c` |
| Depends on | none |

**Promise.**
- `docker/attackers/zenoh-pico-sequence-exhaustion/attack.yaml:5` (same in `README.md:3`): "Exhaustion or intensive manipulation of Zenoh/Zenoh-Pico sequence numbers to degrade ordering, reliability, or session-state control."
- `attack_sequence_exhaustion.c:2-3`: "Attack 8: Sequence Number Exhaustion" / "Rapidly exhausts sequence number space to cause tracking issues"; `:120`: "Strategy: Jump sequence numbers by 10K-100K".
- Target: `attack.yaml:9-10` `target_services: - zenoh-router`, which declares itself TCP-only (`docker/servers/zenoh-router/server.yaml:11-14`).

**What happens.** No FRAME (the Zenoh message that carries data in a session, numbered by an SN, sequence number) reaches the router [measured]:
- In the attackzoo flow: 4,470,600 UDP datagrams to port 7447, all with first byte `0x20`; the router's `Udp NoPorts` = 4,470,600 (100%); 17 ICMP; router CPU 0.00%; log with only the startup lines. Another run (2026-11-13): 5,358,900 datagrams, 100% NoPorts; in a reproduction on 2026-11-17, 5,117,500, also 100% [measured].
- With UDP port 7447 forcibly opened (diagnostic): the router's 22,787 responses are all CLOSE INVALID (`03 02`); `zenohd` reads `0x20` as OAM; no session opens.
- With this commit the FRAMEs arrive and the router processes them, but the effect of `attack.yaml:5` ("degrade ordering, reliability") does not appear in Zenoh 1.7.2: the measured effect is router CPU, with no denial of service and no degradation of third parties (table below).

**Cause.**
- Transport [read in code]: `attack_sequence_exhaustion.c:50` `socket(AF_INET, SOCK_DGRAM, 0)` and `:81-82` `sendto`; the router only listens on TCP (`docker/servers/zenoh-router/Dockerfile:1-2`; Zenoh 1.7.2 `commons/zenoh-config/src/defaults.rs:167-181`, router at `:174`).
- ID [read in code]: `:17` `#define Z_MSG_FRAME 0x00`; in 1.7.2 the ID is the low 5 bits (`commons/zenoh-protocol/src/common/mod.rs:23-28`), `0x00` is OAM and FRAME is `0x05` (`commons/zenoh-protocol/src/transport/mod.rs:54,59`).
- Session [read in code]: without InitSyn/OpenSyn (the client messages that open the Zenoh session; the router replies with InitAck and OpenAck) the router closes the connection (`io/zenoh-transport/src/unicast/establishment/accept.rs:162-183`); over TCP each batch (Zenoh's unit of sending) is preceded by 2 bytes with its size (`io/zenoh-transport/src/common/batch.rs:311-322`).
- Two details that only appear after the transport is fixed, and explain the design of the fix [measured with variants of the fix]:
  - The payload byte `0x00` (`:78-79` "Minimal payload") brings the session down on the first FRAME: a FRAME's payload is a sequence of network messages (IDs `0x19` to `0x1f`, `commons/zenoh-protocol/src/network/mod.rs:40-46`); the reader returns the `0x00` (`commons/zenoh-codec/src/transport/frame.rs:228-239`), the router reads it as OAM without an identifier and gives "decoding error" (`io/zenoh-transport/src/unicast/universal/rx.rs:257-259`). Variant with the `0x00` put back: the 4 sessions drop on the first FRAME with that error.
  - An SN above the negotiated resolution brings the session down: `roll()` rejects an SN above the mask (`io/zenoh-transport/src/common/seq_num.rs:146-148`); with U32 resolution the mask is `0x0FFFFFFF` (`seq_num.rs:19`). The upstream base (`:64-65`, `thread_id * 1000000000`) already exceeds that on the first FRAME of threads 1 to 3; thread 0 exceeds it on FRAME 4,435. Variant without the mask: the 4 sessions drop with "The sequence number value must be smaller than the resolution at .../seq_num.rs:147".
- Why, once fixed, it does not degrade third parties [read in code]: the SN state is per session, priority and reliability; the router only compares with the last SN and accepts any forward jump of up to half the resolution (`rx.rs:216-235`, `seq_num.rs:145-155`); the 1.7.2 unicast transport has no retransmission queue (`io/zenoh-transport/src/unicast/universal/mod.rs:14-18`). Whoever jumps the SN only touches the state of their own session.

**How we tested.**
- Machine, images, network and capture as in ZEN-01: router `server-zenoh-router` from `8613c66` (zenohd v1.7.2), no arguments, `RUST_LOG=info`; `--memory 1g --memory-swap 1g`.
- Attack: the `docker run` that `attackzoo.py run iot_zenoh_pico_sequence_exhaustion --target <IP> --port 7447` generates: `-e DURATION_S=10 -e THREADS=4 <image> <IP> 7447`; stopped by the `timeout -s INT` in `entrypoint.sh:7`. BEFORE = image from `8613c66`; AFTER = image with this commit.
- Count: a parser of ours reassembles the connections, counts the batches and repeats the router's SN check (`roll()`, with the initial synchronization from `io/zenoh-transport/src/common/priority.rs:64-73` and the mask read from each connection's InitAck). On the router side: `/proc/net/snmp` delta, `docker stats`, and two runs with only the log level changed (`debug`, and `trace` of the receive module for 3 s) to see what `zenohd` decodes.
- Legitimate client: ours (Python, `eclipse-zenoh==1.7.2`), 2 sessions, put at 50 Hz and get at 2 Hz from 8 s before the attack; latency measured in the real flood window, taken from the pcap.
- Runs: BEFORE 1, plus 1 with a client; AFTER 1, plus 1 with a client, 1 `debug` and 1 `trace`; 2 diagnostic variants (with the `0x00` byte, without the mask).
- Load: load 4.9 to 8.1 (another Zenoh flood was running in another test).
- Stop (forced): router paused before the handshake, the threads give up in ~5 s and the process exits 0.00 s after the SIGINT; paused during the flood, it exits 0.81 s after.
- Independent review: a second reviewer redid the counts with their own parser (TCP reassembly, Zenoh batches, `roll()` replay), their own tshark fields and their own `grep` on the logs; redid the client latency in the real flood window. It matched; their corrections are applied here (the 100% acceptance in the 10 s AFTER is a code replay, not a reading of `zenohd`; the promised effect is not reached).
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `attack.yaml` does not change; `gcc -Wall -Wextra`: only the warning that already exists upstream ("unused parameter 'sig'").

**Fix.** Only the `.c`; `attack.yaml`, `entrypoint.sh`, `README.md`, `Dockerfile` and parameters do not change.
- TCP + `connect` + session opening (InitSyn → InitAck → OpenSyn → OpenAck), reading the SN resolution from the InitAck (S flag; without it, U32) and using the router's mask.
- OpenSyn with initial SN = `base & mask`: the router synchronizes at initial SN - 1 (`priority.rs:64-73`; with 0, at mask - 1), so the first FRAME is already accepted.
- FRAME `0x05` with the R flag (`0x25`), SN = `seq & mask`, no payload (the smallest FRAME that 1.7.2 accepts). The mask is a declared mapping choice: the SN wraps around the 2^28 space instead of exceeding it.
- Kept: jumps (`10000 + rand() % 100000`), per-thread base, loop (100 FRAME + `usleep(100)`), one FRAME per batch, as it was one per datagram.
- `send_all` completes partial sends; `SO_SNDTIMEO` 1 s and `SO_RCVTIMEO` 5 s before `connect`, so the SIGINT can end a stuck thread.
- The mask table repeats `seq_num.rs:17-20` converted to `TransportSn = u32` (`commons/zenoh-protocol/src/transport/mod.rs:99`): `0x7F`, `0x3FFF`, `0x0FFFFFFF`, `0xFFFFFFFF`; the 64-bit entry was never used (the router answered U32 in every session).

**Before and after.** Same router, network and arguments; only the attack image changes. The client row comes from the runs with a client, in the real flood window (9.89 to 10.00 s).

| | BEFORE (8613c66) | AFTER (this commit) |
|---|---|---|
| on the wire | 4,470,600 UDP datagrams (`0x20`), 0 TCP | 4 TCP connections: InitSyn, OpenSyn and 6,796,747 FRAME (`0x25`, no payload) |
| sessions | 0 | 4 (SN resolution U32) |
| reaches the router | nothing (`Udp NoPorts` 100%) | the router's kernel acknowledges 100% of the bytes; SN check replay: 0 dropped, all jumps (1 to 109,999) accepted; each session's SN wraps 370 to 385 times in 2^28 |
| `zenohd` side (`trace` log, 3 s) | n/a | 1,197,190 FRAME decoded of 1,251,708 on the wire (95.6% before the final RST), 0 dropped by SN |
| router response | 17 ICMP | InitAck, OpenAck, 3-4 KEEP_ALIVE per session; 0 FIN/RST/CLOSE; 332 zero windows (the router is the bottleneck) |
| router CPU | 0.00% | 203 to 207% (~2 cores) |
| router memory | 1.16 MiB | 4.2 to 4.5 MiB |
| router log | 10 startup lines | same, no errors |
| legitimate client (flood window) | 498/498 put, p95 1.14 ms, max 6.07 ms; get 20/20 | 493/493 put, p95 0.47 ms, max 19.27 ms; get 20/20 |
| legitimate client ordering | 0 out of order, 0 errors | 0 out of order, 0 errors |

In a reproduction on 2026-11-17, with other tests running (load 7.7 to 11.9), AFTER gave 7,464,858 FRAME on the 4 connections (from 1,741,837 to 2,145,367 per connection), router CPU at 202.69% in one `docker stats` sample and no errors in the log [measured].

Measured effect: router CPU (~2 cores, probably the runtime's 2 receive threads, `commons/zenoh-runtime/src/lib.rs:119-122` [inferred]), with no denial of service and no degradation of third parties' ordering or reliability. A flood of empty FRAMEs with SN + 1 would load the router the same way: the jumps add no effect of their own [inferred from the code].

**How to reproduce.** In the reproduction file, section ZEN-03; uses P1, P2, P3, P4, P5.

**Caveats.**
- "Fixed" here means that the FRAMEs arrive and the router processes them; the effect of `attack.yaml:5` (degrading ordering, reliability or session-state control) is not reached in Zenoh 1.7.2.
- The 100% acceptance in the 10 s AFTER comes from the kernel's ACK and the code replay; the `zenohd` side was only measured in the 3 s `trace` run (95.6% decoded before the RST, 0 dropped by SN).
- The attacker counts 7,808,100 FRAME and 6,796,747 appear on the wire: the difference stayed in the send buffer and was discarded at the RST from `close()` [inferred].
- CPU is qualitative (host load).
- Not tested: campaign path, `docker0`.

**Versions.** Router: `eclipse/zenoh:1.7.2` (zenohd v1.7.2-790faadb; source read at tag 1.7.2, commit `790faad`). Attack: `ubuntu:24.04` + `build-essential` (no pin, as in upstream). Legitimate client: `eclipse-zenoh` 1.7.2 (Python). Docker 29.6.2.

### ZEN-04 · zenoh-pico-timestamp-mess: No Message Reaches The Router, And The Timestamp Goes In A Format Zenoh Does Not Have

| | |
|---|---|
| Class | (a) the code does something other than what it promises; the transport part (UDP against the router, which is TCP-only in attackzoo itself) is also (b) |
| In this PR | commit |
| Files | `docker/attackers/zenoh-pico-timestamp-mess/attack_timestamp_manipulation.c` |
| Depends on | none |

**Promise.**
- `docker/attackers/zenoh-pico-timestamp-mess/attack.yaml:5` (same in `README.md:3`): "Flood of Zenoh/Zenoh-Pico packets with manipulated timestamps to affect target ordering, expiration, or time logic."
- `attack_timestamp_manipulation.c:2-3`: "Attack 13: Timestamp Manipulation Attack" / "Sends messages with manipulated timestamps to cause ordering issues"; variants printed at `:161-165` ("Future timestamps (+1 year)", "Past timestamps (-1 year)", "Zero timestamps", "Maximum timestamps", "Microsecond manipulation"), code at `:85-101`.
- Target: `attack.yaml:9-10` `target_services: - zenoh-router` (TCP-only, `docker/servers/zenoh-router/server.yaml:11-14`).

**What happens.** [measured]
- In the attackzoo flow: 36,385 UDP datagrams to port 7447, all with first byte `0xa0`; the router's `Udp NoPorts` = 36,385 (100%); 15 ICMP; router CPU 0.00%; log with only the startup lines. Nothing reaches `zenohd`. With the UDP port forcibly opened (diagnostic), `zenohd` reads `0xa0` as OAM ("Unknown OAM ext"), every response from it is CLOSE INVALID (`03 02`) and no session opens.
- With only the transport ported, the timestamp format brings the session down or shifts time (three defects that only appear after the first one, measured with variants of the fix):
  - the timestamp goes as a FRAME extension: the 4 sessions drop on the first FRAME with "decoding error";
  - "now" is in the 1900 epoch: the -1 year and the "microsecond" reach the router as +69 to +71 years (21,526 "future" with +25,202 to +25,932 days, 0 "past", 0 "now");
  - the maximum timestamp becomes a 10-byte integer: each session drops exactly on the first FRAME with `ff ff ff ff ff ff ff ff ff 01`.
- With this commit the messages arrive and are decoded, but in the attackzoo scenario (nobody subscribed to the key) the router decodes and discards without looking at the timestamp: no effect on time or ordering. The effect only appears with a subscriber (see ZEN-09).

**Cause.**
- Transport, ID and session [read in code]: `attack_timestamp_manipulation.c:64` `socket(AF_INET, SOCK_DGRAM, 0)` and `:125-126` `sendto`, against a TCP-only router (`docker/servers/zenoh-router/Dockerfile:1-2`; Zenoh 1.7.2 `commons/zenoh-config/src/defaults.rs:167-181`, router at `:174`); `:18` `#define Z_MSG_FRAME 0x00`, which in 1.7.2 is OAM (FRAME is `0x05`, `commons/zenoh-protocol/src/transport/mod.rs:54,59`); without InitSyn/OpenSyn (the client messages that open the Zenoh session; the router replies with InitAck and OpenAck) the router closes the connection (`io/zenoh-transport/src/unicast/establishment/accept.rs:162-183`).
- FRAME extension [read in code + measured]: `:105-118` builds "FRAME header with extensions" with `Z_EXT_TIMESTAMP 0x01`, size 8 and 8 big-endian bytes. In 1.7.2 the only FRAME extension is QoS (`commons/zenoh-protocol/src/transport/frame.rs:79-83`); the router skips extension `0x01` (`debug` log "Unknown Frame ext ... Mandatory: false") and the error comes from the byte `0x08` and the timestamp that follow, which are not a valid message. The timestamp the router handles is the PUT's (the publication message; T flag `0x20`, `commons/zenoh-protocol/src/zenoh/put.rs:43`), inside a PUSH (network message `0x1d`, `commons/zenoh-protocol/src/network/mod.rs:42`), inside the FRAME; the PUSH has an optional timestamp extension (`network/push.rs:49`), but the router's time check uses the PUT's (`zenoh/src/net/routing/dispatcher/pubsub.rs:185-188`). Format: variable-length integer of the NTP64 time + id with size (`commons/zenoh-codec/src/core/timestamp.rs:51-63`), not 8 big-endian bytes.
- Epoch [read in code + measured]: `:51-52` "Convert to NTP timestamp (simplified)" adds `2208988800` (seconds from 1900 to 1970). The router's clock (uhlc library 0.8.2) counts from the UNIX_EPOCH (`uhlc` `src/lib.rs:332-338` and `:133-138`).
- Integer size [read in code + measured]: `:37-45` `encode_zint` is pure LEB128, which uses 10 bytes for values from 2^63; Zenoh's variable-length integer has at most 9 bytes and the ninth carries 8 bits (`commons/zenoh-codec/src/core/zint.rs:21-52`, write `:114-147`, read `:156-169`); the router reads 9 bytes and the rest of the PUT misaligns.
- Without a subscriber there is no time effect [read in code + measured]: `zenoh/src/net/routing/dispatcher/pubsub.rs:283-284` only calls `treat_timestamp` when the route is not empty; without a subscriber the PUT is decoded and discarded. attackzoo has no Zenoh receiver (`docker/servers/zenoh-router/server.yaml:29-30` only lists `client-super:zenoh`, which only opens a TCP connection, `super-client.py:296-302`).
- With a subscriber [read in code]: the router has a hybrid clock (HLC, a logical clock that follows the physical one) on by default in router mode, with `drop_future_timestamp` false (`commons/zenoh-config/src/defaults.rs:139-147`; `zenoh/src/net/runtime/mod.rs:456-457`); a future timestamp beyond 500 ms (`uhlc` `lib.rs:89`) is rejected with a WARN (`lib.rs:289-305`) and the router replaces it with its own, with an ERROR "Replace timestamp" (`pubsub.rs:198-202`); past and zero pass, and the clock stays at the maximum of now, the timestamp and the last one (`lib.rs:306-315`), so it does not move.

**How we tested.**
- Machine, images, network and capture as in ZEN-01: router `server-zenoh-router` from `8613c66` (zenohd v1.7.2), no arguments, `RUST_LOG=info`; `--memory 1g --memory-swap 1g`.
- Attack: the `docker run` that `attackzoo.py run iot_zenoh_pico_timestamp_mess --target <IP> --port 7447` generates: `-e DURATION_S=10 -e THREADS=4 <image> <IP> 7447`; stopped by the `timeout -s INT` in `entrypoint.sh:7`. BEFORE = image from `8613c66`; AFTER = image with this commit (the measurement used a build with a binary identical to this commit's; the source only differs in a comment).
- Count: a parser of ours decodes each connection as 1.7.2 does (batch, which is Zenoh's unit of sending; FRAME; PUSH; PUT; 9-byte integer), repeats the SN check and classifies each timestamp against the capture time. On the router side: `info` log (default), and runs with only the log level changed (`debug`; `trace` of publication routing) to count routed messages and errors.
- Subscriber: ours (Python, `eclipse-zenoh==1.7.2`), 2 sessions through the router, put at 50 Hz and get at 2 Hz on its own key and a subscriber on `**` that records each sample's timestamp; it starts 8 s before the attack and lasts 34 s.
- Runs: BEFORE 1, plus 1 with the subscriber; AFTER 1 without a subscriber, 1 with a subscriber, 1 `debug`, 1 `trace`; 3 diagnostic variants (FRAME extension, 1900 epoch, LEB128 integer), each changing a single point of the fix. The measurement with a subscriber was repeated later with the subscriber proposed in ZEN-09 (another implementation), with equivalent results (see ZEN-09).
- Load: load 2.4 to 8.2.
- Stop (forced): router paused before the handshake, the threads give up in ~5 s and the process exits 0.00 s after the SIGINT; paused during the flood, it exits 0.03 s after.
- Independent review: a second reviewer wrote their own pcap reader and Zenoh 1.7.2 decoder (from the source) and reproduced all the counts, including the router → subscriber direction on the wire; checked the uhlc version inside the router binary. It matched; their corrections are applied here (exact mechanism of the extension; uhlc lines for the epoch; nothing about "effect on time logic" in the attackzoo scenario).
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `attack.yaml` does not change; `gcc -Wall -Wextra`: only the 2 warnings that already exist upstream ("unused parameter 'sig'" and "timestamp may be used uninitialized").
- Not tested: "expiration" (the attackzoo router starts without a plugin or storage, `"plugins":{}` in the startup log, so there is nothing that expires by timestamp).

**Fix.** Only the `.c`; `attack.yaml`, `entrypoint.sh`, `README.md`, `Dockerfile` and parameters do not change.
- TCP + `connect` + session opening (InitSyn → InitAck → OpenSyn → OpenAck), 2-byte prefix per batch; SN resolution read from the InitAck and the router's mask; OpenSyn with initial SN = thread base.
- Each iteration sends 1 batch = FRAME `0x25` (thread SN) + PUSH `0x3d` on the key `attackzoo/timestamp-mess` + PUT `0x21` with timestamp (NTP64 integer + the session's zid (node identifier) as id) + the same "TIMESTAMP_MANIPULATED" payload with size.
- `get_timestamp_ntp` in UNIX epoch (without the `+ 2208988800`); `encode_zint` with at most 9 bytes (for values < 2^63 the output is the same as before).
- Kept: the 5 variants, the `rand() % 5` choice, the per-thread SN base, the loop (1 message + `usleep(1000)`), the printed messages.
- `send_all` completes partial sends; `SO_SNDTIMEO` 1 s and `SO_RCVTIMEO` 5 s before `connect`; a thread that fails to send stops and says so.
- The key `attackzoo/timestamp-mess` is our choice: upstream had no key.
- The SN mask table repeats `io/zenoh-transport/src/common/seq_num.rs:17-20` converted to `TransportSn = u32` (`commons/zenoh-protocol/src/transport/mod.rs:99`): `0x7F`, `0x3FFF`, `0x0FFFFFFF`, `0xFFFFFFFF`; the 64-bit entry was never used (the router answered U32 in every session).

**Before and after.** Same router, network and arguments; only the attack image changes.

attackzoo scenario (router only, no subscriber):

| | BEFORE (8613c66) | AFTER (this commit) |
|---|---|---|
| on the wire | 36,385 UDP datagrams (`0xa0`) | 4 TCP connections: InitSyn, OpenSyn, 35,731 FRAME with PUSH + PUT |
| sessions | 0 | 4 |
| messages that `zenohd` decodes | 0 (`Udp NoPorts` 100%) | 35,731 PUT on the wire, 0 malformed, 0 dropped by SN in the replay; `trace` run: 36,332 FRAME on the wire = 36,332 "Route data for res attackzoo/timestamp-mess" in the log |
| timestamps on the wire | (do not arrive) | +365 days 7,129, -365 days 7,175, zero 7,069, maximum 7,214, now - 1000 7,144 |
| decoding errors (`debug` run) | n/a | 0 |
| router log (`info`) | 10 startup lines | 10 startup lines, 0 timestamp errors |
| router CPU | 0.00% | 4.9 to 6.0% |

With our subscriber on `**`:

| | BEFORE (8613c66) | AFTER (this commit) |
|---|---|---|
| attack samples at the subscriber | 0 | 36,249 (100% of the FRAME on the wire) |
| future and maximum timestamps replaced by the router | 0 | 14,350 (+365 days 7,286 + maximum 7,064), each with 1 ERROR "Replace timestamp" and 1 uhlc WARN (28,710 log lines in ~10 s, counting the 10 startup ones) |
| manipulated ones delivered intact, with the attacker's id | 0 | -365 days 7,317, zero (1970) 7,326, now - 1000 7,256 |
| timestamp inversions in arrival order | 0 | 13,344 in 36,249 |
| router clock (router timestamp on the legitimate samples - send) | 0.1 to 5.0 ms | 0.1 to 6.4 ms in the 3 phases (intact) |
| legitimate put before, during, after | 364/364, 538/538, 789/789 | 491/491, 573/573, 627/627 |
| router CPU during | 0 to 1.7% | 17 to 39% |

**How to reproduce.** In the reproduction file, section ZEN-04; uses P1, P2, P3, P4, P5.

**Caveats.**
- The fix only delivers the messages and makes the router decode them. In the attackzoo scenario, without a subscriber, the measured effect is only decoding (CPU ~5%, qualitative). With a subscriber, what is measured is the router's time check working (it rejects and rewrites 100% of the future and maximum ones, clock intact), 2 log lines per rejected message, and timestamps from 1 year ago and from 1970 arriving intact at the receiver; no application failure was measured.
- "expiration" not measured (the router starts without storage).
- The diagnostic variants (FRAME extension, 1900 epoch, LEB128) are not in the PR; they only justify the format of the fix.
- Not tested: campaign path, `docker0`.

**Versions.** Router: `eclipse/zenoh:1.7.2` (zenohd v1.7.2-790faadb; source read at tag 1.7.2, commit `790faad`); uhlc 0.8.2 (the `Cargo.lock` version of 1.7.2, also checked inside the router binary). Attack: `ubuntu:24.04` + `build-essential` (no pin, as in upstream). Subscriber and client: `eclipse-zenoh` 1.7.2 (Python). Docker 29.6.2.

### ZEN-05 · zenoh-pico-memory-exhaustion: No Byte Reaches The Router And, Even Fixed, The Design (Maximum Batch) Does Not Make Memory Rise

| | |
|---|---|
| Class | (a) the code does something other than what it promises; the transport part (UDP against the router, which is TCP-only in attackzoo itself) is also (b) |
| In this PR | commit |
| Files | `docker/attackers/zenoh-pico-memory-exhaustion/attack_memory_exhaustion.c` |
| Depends on | none |

**Promise.**
- `docker/attackers/zenoh-pico-memory-exhaustion/attack.yaml:5` (same in `README.md:3`): "Memory exhaustion of the Zenoh router/peer through mass creation of resources, sessions, declarations, or pending messages."
- `attack_memory_exhaustion.c:2-3`: "Attack 9: Memory Exhaustion via Large Payloads" / "Sends maximum-size messages to exhaust router memory"; `:141`: "[*] Expected memory pressure: HIGH".
- Target: `attack.yaml:9-10` `target_services: - zenoh-router`, which declares itself TCP-only (`docker/servers/zenoh-router/server.yaml:11-14`).

**What happens.** [measured]
- In the attackzoo flow: 3,818 and 3,866 UDP datagrams of 65,435 bytes (first byte `0x20`) in the two runs, each broken into 45 IP fragments (171,810 fragments in the first); the router's `Udp NoPorts` = 100% (3,818; 3,865 + 1 failed IP reassembly); 17 and 15 ICMP; router CPU 0.1 to 0.2%; memory 1.6 to 2.6 MiB; our test client with no failures.
- With this commit the maximum-size messages arrive and are decoded and routed (100%), but the router's memory stays flat: 1.6 to 5.2 MiB in 10 s, and 1.6 to 3.4 MiB even with ~1.5 GB of messages in 60 s. The promised memory exhaustion is not reached.

**Cause.**
- Transport, ID and session [read in code]: `attack_memory_exhaustion.c:51` `socket(AF_INET, SOCK_DGRAM, 0)` and `:99-100` `sendto`, against a TCP-only router (`docker/servers/zenoh-router/Dockerfile:1-2`; Zenoh 1.7.2 `commons/zenoh-config/src/defaults.rs:167-181`, router at `:174`); `:17` `#define Z_MSG_FRAME 0x00`, which in 1.7.2 is OAM (`commons/zenoh-protocol/src/transport/mod.rs:54,59`); without InitSyn/OpenSyn (the client messages that open the Zenoh session; the router replies with InitAck and OpenAck) the router closes the connection (`io/zenoh-transport/src/unicast/establishment/accept.rs:162-183`). With the UDP port forcibly opened (diagnostic), `zenohd` reads `0x20` as OAM and every response is CLOSE INVALID (`03 02`).
- Constraint of the fix, not an upstream defect [read in code + measured]: over TCP the 65,435-byte batch (Zenoh's unit of sending) (`:91`, `MAX_FRAME_SIZE - offset - 100`) does not fit. The router fixes the link's maximum batch size at a multiple of MSS/2 (`io/zenoh-links/zenoh-link-tcp/src/unicast.rs:84-97`; with MSS 1448, 65,160 bytes), uses the smaller of the configuration and that value (`io/zenoh-transport/src/unicast/establishment/accept.rs:726`), announces it in the InitAck (S flag) and drops the link that sends a larger batch ("Invalid batch length or buffer size", `io/zenoh-transport/src/unicast/link.rs:213-223`). A first version of the fix with a fixed 65,435-byte batch was refused this way in 2 of 2 sessions.
- Why memory does not rise [read in code]: a complete FRAME fits in a batch and is delivered at once; without a subscriber the PUSH is not stored (`zenoh/src/net/routing/dispatcher/pubsub.rs:283` only forwards if the route is not empty) and the receive buffer goes back to the pool (`io/zenoh-transport/src/unicast/universal/link.rs:305-313`); with a subscriber, the PUSH uses `CongestionControl::Drop` by default (`commons/zenoh-protocol/src/core/mod.rs:606`) and the send queue has 2 batches per priority (`DEFAULT_CONFIG.json5:628-637`, at the root of the Zenoh repository). Nothing stays pending. `attack.yaml:5` cites other means ("resources, sessions, declarations, or pending messages"); the code only uses "large payloads".

**How we tested.**
- Machine, images, network and capture as in ZEN-01: router `server-zenoh-router` from `8613c66` (zenohd v1.7.2), no arguments, `RUST_LOG=info`; `--memory 1g --memory-swap 1g` on router and attack.
- Attack: the `docker run` that `attackzoo.py run iot_zenoh_pico_memory_exhaustion --target <IP> --port 7447` generates: `-e DURATION_S=10 -e THREADS=4 <image> <IP> 7447`; stopped by the `timeout -s INT` in `entrypoint.sh:7`. BEFORE = image from `8613c66` (md5 of the `.c` in the image = source); AFTER = image with this commit.
- Count: a parser of ours reassembles each connection by TCP sequence number and walks the batches as the router does, checking header, key, size and the byte pattern of each message. On the router side, every 0.25 s: CPU, `memory.current`, `memory.peak`, `memory.stat` (anon) and `memory.events` of the cgroup; `/proc/net/tcp6`; `docker stats`.
- Legitimate client: ours (Python, `eclipse-zenoh==1.7.2`), from 6 s before the attack: every 0.5 s a put, a get and the router's session list.
- Runs: BEFORE 2; AFTER 2, plus 1 with a subscriber of ours on `attackzoo/**` and `debug` log (to prove decoding at the router) and 1 of 60 s (`DURATION_S=60`, deviation: the README flow uses 10 s and the campaign 20 s).
- Variant measured and not proposed: the same session sending a single 1 GiB message in FRAGMENT (pieces the router keeps until the last one).
- Load: load 1.6 to 7.0; counts and memory do not depend on it.
- Stop (forced): router paused before the handshake, the threads give up in ~5 s and the process exits 0.00 s after the SIGINT; paused during the flood, it exits 0.54 s after.
- Independent review: a second reviewer redid the counts with their own parser, tshark filters and cgroup and `/proc/net/snmp` readers. It matched; their corrections are applied here (171,810 IP fragments in the first run, counting the first of each datagram; "decoded" in the 60 s run is inferred from the pcap; "one variant tested", not "only one").
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `attack.yaml` does not change; `gcc -Wall -Wextra`: only the warning that already exists upstream ("unused parameter 'sig'").
- Not tested: the promise's other means as a fix (see the optional proposal ZEN-08).

**Fix.** Only the `.c`; `attack.yaml`, `entrypoint.sh`, `README.md`, `Dockerfile` and `build.sh` do not change. This commit fixes the delivery; it does not make memory rise.
- TCP + `connect` + session opening: InitSyn (version `0x09`, client, random zid (node identifier)) → from the InitAck it reads the SN resolution and the batch size (S flag) → OpenSyn (10 s lease, initial SN = thread base, cookie) → OpenAck.
- Each send is a batch of the maximum size the router declares, with the same 100-byte margin as upstream: 2-byte prefix + FRAME `0x25` + SN + PUSH `0x3d` on the key `attackzoo/memory-exhaustion` + PUT `0x01` + size + the same `(seq + i) % 256` pattern.
- Kept: `usleep(10000)`, `THREADS`, `seq` base `thread_id * 1000000`, `SO_SNDBUF` of 1 MB, the printed messages (each thread's start message gains the batch size) and `main()`. The printed "Frame size: 65535 bytes" stays (it is now the ceiling; each thread prints the real batch, "router batch ... bytes").
- `send_all` completes partial sends and retries on EAGAIN/EINTR; `SO_SNDTIMEO` 1 s and `SO_RCVTIMEO` 5 s; the thread exits if the link closes.
- The key `attackzoo/memory-exhaustion` is our choice: upstream had no key.
- The SN mask table repeats `io/zenoh-transport/src/common/seq_num.rs:17-20` converted to `TransportSn = u32` (`commons/zenoh-protocol/src/transport/mod.rs:99`): `0x7F`, `0x3FFF`, `0x0FFFFFFF`, `0xFFFFFFFF`; the 64-bit entry was never used.
- Alternative measured and not proposed: a 1 GiB message in FRAGMENT raises the router's memory by 240 MiB in 10 s and kills it by out-of-memory (OOM) in 42 s with a 1 GiB cap; it repeats the mechanism of `zenoh-pico-fragments-reassembly` (ZEN-02). The other one, by mass declarations, is in the PR description as an optional proposal (ZEN-08).

**Before and after.** Same router, network, arguments and client; only the attack image changes (2 runs on each side).

| | BEFORE (8613c66) | AFTER (this commit) |
|---|---|---|
| on the wire | 3,818 / 3,866 UDP datagrams of 65,435 bytes (`0x20`), 0 TCP | 4 TCP connections: InitSyn, OpenSyn and FRAME/PUSH/PUT batches of 65,060 bytes |
| messages accepted | 0 (`Udp NoPorts` 100%) | 3,862 / 3,900 valid batches (= the attack's "Total Frames"), 0 invalid, 0 SN gaps; 251,115,092 / 253,585,928 payload bytes; the router acknowledges 100% of the bytes |
| decoding at the router (run with subscriber and `debug` log) | nothing arrives | 3,900 samples at the subscriber, 253,585,928 bytes = the pcap; 0 decoding errors |
| router response | ICMP port unreachable | InitAck, OpenAck, 3 KEEP_ALIVE per session; 0 FIN/RST/CLOSE |
| sessions at the router | 2 (only the client) | 2 → 6 → 2 |
| router CPU | 0.1 to 0.2% | 4.8% / 2.4% (with subscriber 6.0%) |
| router memory during | 1.6 to 2.6 MiB; peak 4.9 / 4.7 MiB | 1.6 to 3.2 / 3.3 to 5.2 MiB; peak 4.7 / 5.5 MiB; 0 OOM |
| legitimate client | 0 failures | 0 failures (median put 0.4 to 0.6 ms) |
| 60 s (`DURATION_S=60`) | n/a | 23,160 valid batches, 1,505,909,647 bytes; memory 1.6 to 3.4 MiB with no trend, peak 4.6 MiB; 0 client failures |

**How to reproduce.** In the reproduction file, section ZEN-05; uses P1, P2, P3, P4, P5.

**Caveats.**
- This commit only fixes the delivery: the promise of memory exhaustion is not reached by the attack's own design (measured in 10 s, 60 s and with a subscriber).
- In the 60 s run, "decoded" is inferred from the pcap (valid SN and 100% ACK); decoding by the router was only measured in the 10 s run with a subscriber.
- With the subscriber proposed in ZEN-09 up and the default key `attackzoo/**`, the router forwards 100% of these batches to the subscriber (~256 MB more on TCP/7447 in a 10 s run); router memory and log do not change [measured, 1 run].
- Not tested: campaign path, `docker0`.

**Versions.** Router: `eclipse/zenoh:1.7.2` (zenohd v1.7.2-790faadb; source read at tag 1.7.2, commit `790faad`). Attack: `ubuntu:24.04` + `build-essential` (no pin, as in upstream). Legitimate client and diagnostic subscriber: `eclipse-zenoh` 1.7.2 (Python). Docker 29.6.2.

### ZEN-06 · zenoh-pico-proto-fuzzer: No Fuzz Case Reaches The Router And The Crash Detection Never Fires

| | |
|---|---|
| Class | (a) the code does something other than what it promises; the transport part (UDP against the router, which is TCP-only in attackzoo itself) is also (b) |
| In this PR | commit |
| Files | `docker/attackers/zenoh-pico-proto-fuzzer/attack_protocol_fuzzer.c` |
| Depends on | none |

**Promise.**
- `docker/attackers/zenoh-pico-proto-fuzzer/attack.yaml:5` (same in `README.md:3`): "Sending malformed or mutated Zenoh/Zenoh-Pico messages to trigger errors, exceptions, or crashes on the target."
- `attack_protocol_fuzzer.c:3`: "Sends randomized/mutated protocol messages to find bugs"; `:51` and `:73` `buf[0] = 0x00; // FRAME`; `:125-127` prints "[!] Empty response - possible crash?" and counts the crash; `:128-129` treats `0x06` as "Connection closed by peer".
- Target: `attack.yaml:9-10` `target_services: - zenoh-router`; the router claims to serve "fuzzing" (`docker/servers/zenoh-router/README.md:3`) and declares itself TCP-only (`server.yaml:11-14`, `README.md:16-17`).

**What happens.** [measured]
- In the attackzoo flow (`DURATION_S=0`, `COUNT=1000`): 1,000 UDP datagrams to port 7447; the router's `Udp NoPorts` = 1,000; 107 ICMP; 0 TCP; 0 sessions; router log with only the startup lines. No case reaches the in-session handling. The container takes 102.97 s (the fuzzer prints "Duration: 101").
- The crash detection never fires: with the router dead in the middle of the run (crash simulated with `docker kill`), upstream prints "Potential Crashes: 0" and keeps sending UDP for 41 s.
- With the UDP port forcibly opened (diagnostic), the router answers 30 CLOSE INVALID (`03 02`) and the fuzzer prints 0 "Connection closed", because it waits for `0x06`.

**Cause.**
- Transport [read in code]: `attack_protocol_fuzzer.c:156` `socket(AF_INET, SOCK_DGRAM, 0)` and `:108-109` `sendto`, against a TCP-only router (`docker/servers/zenoh-router/Dockerfile:1-2`; Zenoh 1.7.2 `commons/zenoh-config/src/defaults.rs:174`).
- IDs [read in code + measured]: in Zenoh 1.7.2 `0x00` is OAM, CLOSE is `0x03`, FRAME is `0x05` and `0x06` is FRAGMENT (`commons/zenoh-protocol/src/transport/mod.rs:54,57,59,60`). Measured with a variant that only swaps the 2 FRAME bytes, same session and same router with `debug` log: with `0x00` the router reads 180 of 180 "overflow" cases and 143 of 143 "injection" cases as OAM; with `0x05`, 160 of 160 and 152 of 152 as FRAME.
- Session [read in code]: the fuzz case goes as the first datagram (`:94-109`), without InitSyn/OpenSyn (the client messages that open the Zenoh session; the router replies with InitAck and OpenAck); the router closes the connection whose first message is not InitSyn (`io/zenoh-transport/src/unicast/establishment/accept.rs:162-183`). The cases still reach the opening decoder (17 of 30 in the diagnostic), but none reaches the in-session handling (FRAME, SN, payload).
- Crash detection [read in code]: `:125` counts a crash when `recv_len == 0`. On an unconnected UDP socket Linux does not deliver the ICMP error (Linux v7.0 `net/ipv4/udp.c:1013-1015`), and even if delivered `recvfrom` would return -1, never 0.
- Time [read in code]: a 100 ms wait for a response on each case (`:116`) plus `usleep(1000)` (`:182`); with no response at all, 1,000 × ~101 ms.

**How we tested.**
- Machine, images, network and capture as in ZEN-01: router `server-zenoh-router` from `8613c66` (zenohd v1.7.2), no arguments; `--memory 1g --memory-swap 1g` on router, attack and client; 0 drops in the 8 captures.
- Attack: the `docker run` that `attackzoo.py run iot_zenoh_pico_proto_fuzzer --target <IP> --port 7447` generates: `-e DURATION_S=0 -e COUNT=1000 <image> <IP> 7447` (no `timeout`, `entrypoint.sh:6-11`). BEFORE = image from `8613c66` (md5 of the `.c` in the image = source); AFTER = image with this commit.
- Pair 1: router exactly as attackzoo starts it (`info` log) and a legitimate client of ours (Python, `eclipse-zenoh==1.7.2`, put at 20 Hz and get at 2 Hz); the client ran 125 s in BEFORE and 45 s in AFTER (only the length of its phases changes, not the attack counts). BEFORE 1 run, AFTER 2.
- Pair 2: router with `RUST_LOG=debug` and `trace` of the receive module (only the log level changes), no client, to count per case what the router decoded and why it closed; log × pcap join by port and by time. BEFORE 1 run, AFTER 1.
- Simulated crash: router in a network namespace held by a container that only sleeps (the IP keeps answering, the port closes), `docker kill` of the router ~4.5 s after the start, `COUNT=400`, the same on both sides.
- Count: a parser of ours per TCP connection (handshake, the case's batch, the batch being Zenoh's unit of sending; who closes first and how long after); the fuzzer's output; the router's `/proc/net/snmp`; the router's PID, restarts and `OOMKilled`.
- Load: load 2.5 to 4.0 (other tests running).
- Independent review: a second reviewer recounted with their own tshark and batch parser and joined log and pcap by port and by time. It matched; their corrections are applied here (the `0x03` CLOSE branch never ran; the crash counter counts failed cases, not distinct crashes; "no case reaches the in-session handling" in place of "nothing reaches the parser").
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `attack.yaml` does not change; `gcc -Wall -Wextra`: only the warning that already exists upstream ("unused parameter 'sig'").
- Not tested: the 1 s deadline and "unexpected reply" branches of the crash detection; stopping with the router stopped (only read: the entrypoint sends SIGTERM, which the binary does not handle, and it dies at once); the fuzzer against a router that accepts TCP and does not respond (only read: each case waits the 1 s handshake deadline, about 17 min for 1,000 cases, and in the attackzoo flow, with `DURATION_S=0`, there is no stop signal).

**Fix.** Only the `.c`; `attack.yaml`, `entrypoint.sh`, `Dockerfile`, `README.md` and parameters (`COUNT`, `DURATION_S`) do not change; the 6 generators, the `usleep(1000)` and the 100 ms wait stay.
- Each case opens a new TCP session (InitSyn → InitAck → OpenSyn → OpenAck), because the router drops the session after a batch that does not decode (`io/zenoh-transport/src/unicast/universal/rx.rs:259` → `io/zenoh-transport/src/unicast/universal/link.rs:178` → `io/zenoh-transport/src/unicast/universal/transport.rs:178-179,207`).
- The case goes as one TCP batch (2 size bytes + the case's bytes); every send goes through `send_all`; `SO_RCVTIMEO`/`SO_SNDTIMEO` of 1 s so a router that stopped does not hang the fuzzer.
- FRAME `0x05` in the "overflow" and "injection" generators.
- Response: CLOSE `0x03` after the 2-byte prefix, or end of connection/reset, counts as "Connection closed by peer".
- "possible crash" becomes "the session did not open" (connection refused, deadline exceeded or unexpected reply).
- This attack's `send_all` does not retry on EAGAIN, unlike the other Zenoh fixes [read in code]; immaterial here (1 batch per session, 1 case every ~100 ms).

**Before and after.** Pair 1: same router (as attackzoo starts it), network, arguments and client; only the attack image changes.

| | BEFORE (8613c66) | AFTER (this commit, 2 runs) |
|---|---|---|
| on the wire | 1,000 UDP datagrams, 0 TCP | 1,000 TCP connections, each with InitSyn, OpenSyn and 1 fuzz batch |
| sessions opened (router's InitAck + OpenAck) | 0 | 1,000 / 1,000 |
| cases that arrive inside a session (whole batch acknowledged after the OpenAck) | 0 (`Udp NoPorts` = 1,000) | 1,000 / 1,000 |
| router reaction | 107 ICMP, nothing else | closes the session (FIN; 0 CLOSE, 0 RST) in 913 / 880 cases, median 0.43 / 0.32 ms after the batch; accepts silently 87 / 120 |
| router log (default level) | 10 lines, 0 ERROR/WARN | 21 / 21 ERROR "Unknown <X> ext" + 1 / 3 WARN "Route final reply: Query not found!" |
| `zenohd` crash | no | no (same PID, 0 restarts, no OOM) |
| router CPU (median / max) | 0.66% / 0.86% | 11.3% (10.7% in the reviewer's count, with another definition of median) / 16.7% and 7.1% / 11.8% |
| legitimate client | all delivered | all delivered; median put 0.6 to 0.8 ms |
| fuzzer output | 0 "Connection closed"; Potential Crashes 0; Duration 101 | 913 / 880 "Connection closed by peer"; Potential Crashes 0; Duration 11 / 15 |
| container time | 102.97 s | 12.62 / 15.11 s |
| simulated crash (`COUNT=400`) | Potential Crashes 0; 400 datagrams, 46 ICMP | Potential Crashes 192 = 192 "Session not opened (Connection refused) - possible crash?" = 192 RST |

Pair 2 (`debug` + `trace` log): AFTER 1,000 "New transport opened"; the router ends each session through 735 "decoding error" (`rx.rs:259`) + 163 "sequence number ... must be smaller than the resolution" (`io/zenoh-transport/src/common/seq_num.rs:147`) + 102 connection ends by the attacker; the router closes first in 898 = 735 + 163. No `zenohd` crash: a result of the fuzzing, not a defect of the attack.

**How to reproduce.** In the reproduction file, section ZEN-06; uses P1, P2, P3, P4, P5.

**Caveats.**
- The test of the `0x03` CLOSE after the prefix never ran: the router did not send any CLOSE after the OpenAck in 4,000 sessions (the three AFTER runs and the ID-variant run, 1,000 each); the "Connection closed by peer" notice fires on the end of the connection. The CLOSE branch is [read in code].
- The "Potential Crashes" counter counts failed cases, not distinct crashes (192 for 1 crash). Measured only with connection refused; the 1 s deadline and unexpected-reply branches were not measured.
- Attributing the "Query not found" WARNs to fuzz cases is inferred (0 WARN in BEFORE with the same client).
- Time note: with `COUNT=1000` the run takes 10 to 15 s, depending on the cases drawn at random, and the "Duration" the fuzzer prints went past the declared `max_runtime_s` of 10 s (`attack.yaml:8`; `README.md:14` "Suggested max runtime `10s`") in 3 of the 4 runs with a quiet machine [measured: "Duration" 13, 14, 13 and 10, on 2026-11-17 and 2026-11-18; the container time, which is what the attackzoo interface cuts off, was not noted in those runs; in the test, under load, "Duration" 11 and 15, with 12.6 and 15.1 s of container]. The mechanism [read in code in `attack_protocol_fuzzer.c` at this item's commit]: the seed of the random draw is the clock (`srand(time(NULL))`, `:280`), so each run draws other cases, and each case the router accepts silently waits the 100 ms for the response (`:244`, `:248`), while a case the router closes returns in under 1 ms (median 0.32 to 0.43 ms) [measured]. The silent cases were 75 to 120 per run (87 and 120 in the test) [measured]; the rest is ~3 s of startup and of opening the 1,000 sessions [inferred]. Upstream took ~100 s for the same reason: with no response at all, each of the 1,000 cases waited the 100 ms. We did not touch it (it would change the attack's design).
- The "Malformed" strategy is drawn but has no generator; that is ZEN-07.
- Not tested: campaign path, `docker0`.

**Versions.** Router: `eclipse/zenoh:1.7.2` (zenohd v1.7.2-790faadb; source read at tag 1.7.2, commit `790faad`). Attack: `ubuntu:24.04` + `build-essential` (no pin, as in upstream). Host kernel 7.0.0-38-generic (source of `net/ipv4/udp.c` read at v7.0). Legitimate client: `eclipse-zenoh` 1.7.2 (Python). Docker 29.6.2.

### ZEN-07 · zenoh-pico-proto-fuzzer: The "Malformed" Strategy Is Drawn And Printed, But Has No Generator (It Sends Random Bytes)

| | |
|---|---|
| Class | (a) the code does something other than what it promises (minor) |
| In this PR | commit |
| Files | `docker/attackers/zenoh-pico-proto-fuzzer/attack_protocol_fuzzer.c` |
| Depends on | ZEN-06 (effect: without it no case reaches the router). The diff was written on top of ZEN-06, in the same file, but applies the same without it, with an offset of -121 lines |

**Promise.**
- `docker/attackers/zenoh-pico-proto-fuzzer/attack.yaml:5` (same in `README.md:3`): "Sending malformed or mutated Zenoh/Zenoh-Pico messages to trigger errors, exceptions, or crashes on the target."
- `attack_protocol_fuzzer.c:19-26`: enumeration with 6 strategies, `:22` `FUZZ_MALFORMED`; `:86` `case FUZZ_MALFORMED: return "Malformed";`, `:151` "[*] Strategies: 6", `:178-179` prints `Strategy: %s` every 100 cases.

**What happens.** [measured, with ZEN-06 applied] One sixth of the cases draw "Malformed", but send the same random bytes as the "Random" strategy: in 1,000 cases, 171 drew "Malformed"; their bytes are random in 169 and similar to "valid header" in 2, with 5 to 4,083 bytes (the "Random" ones: 53 to 4,077). About 2/6 of the cases are random bytes. The bytes remain malformed, so `attack.yaml:5` holds anyway; what fails is the code's own promise (a named, printed strategy that does not exist), and 1/6 of the budget repeats "Random".

**Cause.** [read in code] `:174` `rand() % 6` draws `FUZZ_MALFORMED` (value 2); the `switch` at `:99-106` has no `case` for it and falls into `:105` `default: fuzz_random(buffer, &len);`. Same after ZEN-06 (lines `:294` and `:220-227` there).

**How we tested.**
- ZEN-06 setup: router `server-zenoh-router` from `8613c66` (zenohd v1.7.2), no arguments; `--memory 1g --memory-swap 1g`; 0 drops in the 7 captures (the 5 of the two pairs, the one of the measured alternative, with 200 cases, and a short one, for checking, with 30); no legitimate client.
- Attack: `-e DURATION_S=0 -e COUNT=1000 <image> <IP> 7447`, as `attackzoo.py run` generates it. BEFORE = image with ZEN-06; AFTER = image with ZEN-06 and this commit (md5 of the `.c` inside each image = source).
- Strategy of each case: the fuzzer uses `srand(time(NULL))`, so the sequence is reproducible. We redid, per case, the draws and the bytes with the very `.c` compiled in the same image, finding the seed from the zid (node identifier) of the first InitSyn (the first message of the Zenoh session opening) in the pcap; zid and case bytes matched 1,000 of 1,000 in all runs.
- Pair 1: router with `debug` + `trace` receive log (only the log level changes); BEFORE 1 run, AFTER 2. Pair 2: router with the default log; BEFORE 1 run, AFTER 1.
- Load: load 2.85 to 6.05.
- Independent review: a second reviewer rewrote the replay in C without including our `.c`, classified the bytes with their own templates and attributed the log lines by port and by time window. It matched in all runs. They also ran a control: each subtype next to a "twin" that fixes only the inconsistency; the 4 malformed cases make the router close the session with "decoding error" in 0.1 to 0.8 ms, and the 4 twins are accepted with the session open (this measured the m-len and m-enc mechanism, two of the subtypes described in the Fix, which had only been read before).
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `attack.yaml` does not change; `gcc -Wall -Wextra`: only the warning that already exists ("unused parameter 'sig'").

**Fix.** A function `fuzz_malformed()` with the same signature as the other 5 and the `case FUZZ_MALFORMED` in the `switch`; 32 lines added, 0 removed. Each case is a message with a valid Zenoh 1.7.2 transport ID (KEEP_ALIVE `0x04`, FRAME `0x05`) in which one field contradicts the rest; `rand() % 4` picks the subtype; 3 to 18 bytes. Rules broken [read in code, Zenoh 1.7.2]:
- m-len: KEEP_ALIVE extension that declares more bytes than follow (`84 42 L` + bytes; ZBuf extension = size + bytes, `commons/zenoh-protocol/src/common/extension.rs:42-44`).
- m-zint: FRAME SN in an 11-byte variable-length integer, above the maximum of 9 (`commons/zenoh-codec/src/core/zint.rs:21`).
- m-extchain: FRAME extension chain that announces one more and ends ("Z: More ... another extension will follow", `extension.rs:36`).
- m-enc: FRAME extension with the reserved encoding `0b11` (`extension.rs:51`).

Alternative measured and not proposed: remove "Malformed" (5 strategies, `rand() % 5`, banner "Strategies: 5"; 4 lines). It stays in reserve, because it loses 1/6 of the cases and the author designed 6 strategies. In 200 cases it ran without "Malformed" in the log, with the session open and the batch (Zenoh's unit of sending) acknowledged in 200 of 200.

**Before and after.** Same router, network and arguments; only the attack image changes. Pair 1 (`debug` log; AFTER repeat in parentheses):

| | BEFORE (with ZEN-06) | AFTER (ZEN-06 + this commit) |
|---|---|---|
| cases that drew "Malformed" | 171 of 1,000 | 181 of 1,000 (152) |
| bytes of those cases | random 169 + 2 similar to "valid header"; 5 to 4,083 bytes | 181 of 181 in an m-* template (m-enc 47, m-extchain 44, m-len 45, m-zint 45); 3 to 18 bytes (152 of 152) |
| cases of other strategies in an m-* template | 0 | 0 (0) |
| reason for closing in the router log | decoding error 161, connection end by the attacker 8, SN 1, no failure 1 | decoding error 181 of 181 (152 of 152) |
| who closes | router 163, attacker 8 (silent 100 ms) | router 181 of 181, median 0.51 ms after the batch |
| totals: sessions / acknowledged batches | 1,000 / 1,000 | 1,000 / 1,000 |
| `zenohd` crashed? | no | no |
| fuzzer Duration | 14 s | 12 s (12 s) |

Pair 2 (default log, as attackzoo starts the router): "Malformed" 158 → 165; router closes 155 of 158 → 165 of 165; ERROR lines in the log coming from "Malformed" cases 7 (in 6 cases) → 0 (the subtypes use non-mandatory extensions, logged at `debug`). `zenohd` did not crash in any of the 7 runs (same PID, 0 restarts, no OOM).

**How to reproduce.** In the reproduction file, section ZEN-07; uses P1, P2, P3, P4, P5.

**Caveats.**
- The effect of `attack.yaml:5` already held before (random bytes also give an error at the router); the commit makes the named strategy exist and covers 4 decoder rules that the others only hit by chance.
- The subtypes depend on the Zenoh 1.x IDs (`0x04`, `0x05`), consistent with ZEN-06 and with attackzoo's 1.7.2 router.
- In the router's default log the "Malformed" cases only appear as session closes (0 ERROR).
- No `zenohd` crash in 7 runs: a result of the fuzzing, not a defect.
- Same time within the noise (Duration 12 to 14 s on both sides).
- Not tested: campaign path, `docker0`.

**Versions.** Router: `eclipse/zenoh:1.7.2` (zenohd v1.7.2-790faadb; source read at tag 1.7.2, commit `790faad`). Attack: `ubuntu:24.04` + `build-essential` (no pin, as in upstream). Docker 29.6.2.

## Commits: MQTT

### MQTT-01 · mqtt-publisher-flood, mqtt-lwt-abuse, mqtt-qos-amplification And mqtt-broker: The Three Attacks Connect Without Credentials To A Broker That Refuses Anonymous, So Only The Refusal Is Exercised

| | |
|---|---|
| Class | (b) inconsistency between parts of attackzoo |
| In this PR | commit |
| Files | `docker/attackers/mqtt-publisher-flood/entrypoint.sh`, `docker/attackers/mqtt-lwt-abuse/mqtt-lwt-abuse.py` (only the credential line), `docker/servers/mqtt-broker/Dockerfile` |
| Depends on | none |

**Promise.**
- `docker/servers/mqtt-broker/server.yaml:19` (same in `README.md:3`): "Act as an MQTT broker for publishing, brute force, LWT abuse, and QoS amplification in IoT experiments."; `server.yaml:24-28` lists `iot_mqtt_bruteforce`, `iot_mqtt_publisher`, `iot_mqtt_lwt_abuse` and `iot_mqtt_qos_amplification`.
- `docker/attackers/mqtt-publisher-flood/attack.yaml:5`: "MQTT publish flood to evaluate broker availability and behavior under load."
- `docker/attackers/mqtt-lwt-abuse/attack.yaml:5`: "Abuse of the MQTT Last Will and Testament mechanism to force critical publications or false alarms on sensitive topics."
- `docker/attackers/mqtt-qos-amplification/attack.yaml:5`: "Traffic and state-load amplification on the MQTT broker through multiple QoS 2 handshakes."
- On the other side, `docker/servers/mqtt-broker/mosquitto.conf:12`: "allow_anonymous false preserva o comportamento original (anonimo rejeitado);" (Portuguese: "allow_anonymous false preserves the original behavior (anonymous rejected);").

**What happens.** The broker (the MQTT server that receives and relays the messages) answers every anonymous CONNECT with CONNACK rc=5 (CONNACK is the reply to the connection request; rc=5 means "not authorized") and closes the connection. None of the three attacks sends a username and password, so none reaches the part it promises [measured, mosquitto 2.1.2]:
- `mqtt-publisher-flood`: 1000 CONNECT (ClientId `mosq_pub1`, no username), 1000 CONNACK rc=5, 0 PUBLISH; a legitimate subscriber receives 0 messages. The broker logs `disconnected: not authorised.` 1000 times and the attacker logs `Connection Refused: not authorised.` 1000 times. The flood becomes 1000 refused-connection cycles.
- `mqtt-lwt-abuse`: 50 CONNECT with a Will (QoS 2, retained, topic `alerts/device/failure`) and 50 CONNACK rc=5; no Will reaches the subscriber. (A Will, or LWT, is the message the client registers in the CONNECT for the broker to publish if the connection drops without notice.) With the CONNECT refused, the broker deletes the Will; the second, independent reason is MQTT-02.
- `mqtt-qos-amplification`: paho (the attack's MQTT library) neither waits for nor reads the CONNACK, so the client sends the CONNECT and then a QoS 2 PUBLISH right away: 20 to 21 with 20 clients in the tests (about 1 per connection; 21 and 22 in runs of the reproduction file, the MQTT-03 section); 3233 in 1247 connections with the defaults (2000 threads x 2000 messages) in a 20 s window. The broker answers CONNACK 5, closes and answers no PUBREC to any. This attack's credential goes in MQTT-03.
- The refusal dates from the repository's first commit: with the `Dockerfile` and `mosquitto.conf` from `28c8d5f`, the same flood gives 1000 CONNACK rc=5 and 0 PUBLISH.

**Cause.** [read in code]
- `docker/servers/mqtt-broker/mosquitto.conf:14` (`allow_anonymous false`) and `:15` (`password_file`); `docker/servers/mqtt-broker/Dockerfile:5` creates only the user `benign`.
- No attack sends a credential: `docker/attackers/mqtt-publisher-flood/entrypoint.sh:21` (`mosquitto_pub` without `-u`/`-P`), `docker/attackers/mqtt-lwt-abuse/mqtt-lwt-abuse.py:8,15` and `mqtt-qos-amplification.py:9-10`, in the folder `docker/attackers/mqtt-qos-amplification/` (no `username_pw_set`).
- History: at `28c8d5f` (2026-06-28) `mosquitto.conf:11` only had `#allow_anonymous true` commented out, and mosquitto 2.x refuses anonymous by default when a `listener` is configured (mosquitto 2.0.18, `ChangeLog.txt:620` and `mosquitto.conf:529-532`); `6be0e9e` (2026-11-05) made `allow_anonymous false` explicit.
- Will deleted on refusal: requirement [MQTT-3.1.2-8] of the MQTT 3.1.1 standard ("if the Connect request is accepted, a Will Message MUST be stored"); mosquitto 2.1.2 `src/handle_connect.c:1217` attaches the Will, `:1265-1267` sends CONNACK 5 and `:1297-1309` deletes the Will without publishing it (2.0.18: `:888`, `:936-939`, `:953-971`).

**How we tested.**
- Images built from upstream at `8613c66` (BEFORE) and with this commit (AFTER), as `docker/build-images.sh` does (`docker build -f <folder>/Dockerfile .` inside `docker/`); the file inside each image was checked against the tree (sha256). `eclipse-mosquitto:2` resolved to mosquitto 2.1.2; the publisher uses `ubuntu:24.04` with `mosquitto-clients` 2.0.18-1build3; lwt and qos use Python 3.11.18 and `paho-mqtt` 1.6.1 (pinned in their `requirements.txt`).
- Variants only to isolate the cause, outside the commit: broker with `allow_anonymous true`; broker with the `Dockerfile` and `mosquitto.conf` from the first commit (`28c8d5f`).
- Network: broker on port 1883 (the same one `servers.sh` publishes), attacker, a legitimate subscriber (`mosquitto_sub -u benign -P benignpass -q 2 -t <topic> -v`, from the broker's own image) and, in lwt, a late subscriber that starts 3 s after the attack ends (`-C 1 -W 5`) to see the retained message.
- Arguments: the exact command that `python3 attackzoo.py run <id> --target <IP> --port 1883` builds: publisher `-e COUNT=1000 -e DELAY_MS=0 -e PAYLOAD_SIZE=0 <IP> 1883`; lwt `-e COUNT=50 -e DELAY_MS=100 <IP> 1883`; qos `-e THREADS=2000 -e COUNT=2000 -e DELAY_MS=0 <IP> 1883`, stopped with `docker kill` at 20 s, and also `THREADS=20 COUNT=200` until it exits, for an exact count. Publisher and lwt ran until they exited on their own.
- Counting with `tshark` by MQTT message type (`mqtt.hdrflags`), CONNACK code (`mqtt.conack.val`) and presence of a username and of a Will in the CONNECT; recount by the `mqtt.msgtype` field. Broker CPU read from the container's cgroup. Logs of the broker, the attacker and the subscribers.
- One run per condition (publisher: 5 conditions; lwt: 6; qos: 6 in 20x200, plus the runs with the defaults). Machine load (load average) from 2.1 to 5.5 in the first session (2026-11-13, with other tests in parallel) and from 0.7 to 5.2 in the second (2026-11-15).
- A second reviewer recounted all the pcaps with their own MQTT parser (reassembles the TCP and reads the MQTT without the `tshark` dissector) and checked the cited paho lines inside the image and the mosquitto ones in the official tags: all the counts match.
- Deviations from the attackzoo flow: extra subscribers, which only observe.
- Not tested: the campaign path [inferred: the refusal does not depend on the origin]; mosquitto 2.0.18 (only read); a second `listener` with `per_listener_settings`.

**Fix.**
- Credential through an environment variable in the attacks: `MQTT_USER` and `MQTT_PASS`, defaulting to `attacker`/`attackerpass`. In the publisher it becomes `-u`/`-P` of `mosquitto_pub` (`entrypoint.sh`); in lwt, a `client.username_pw_set(...)` (`mqtt-lwt-abuse.py`). qos gets the same credential in the MQTT-03 commit.
- User `attacker` added to the broker's `password_file` (`Dockerfile`, one more `mosquitto_passwd -b`).
- Why this way: a separate attacker user does not mix the attack's identity with the benign client's (`benign`) and keeps the `allow_anonymous false` that `mosquitto.conf:12` declares. The names `attacker`/`attackerpass` are our choice.
- Broker and attack go together: the new attack against the old broker gets rc=5 [measured with qos].
- `attack.yaml` untouched: the variable has a default in the code. `contrib/docs/CATALOG_MAINTENANCE.md:72` prefers controls declared in `attack.yaml`; declaring `MQTT_USER`/`MQTT_PASS` as `params` with `positional: false` and `env_var` (`modules/loader.py:118-119`) is an alternative that changes the CLI and the smoke test, and was not done. Today's `benign` user also does not appear in the README.
- Alternatives measured, with the same counts as AFTER [measured]: (B) use the `benign` user without touching the broker (`-e MQTT_USER=benign -e MQTT_PASS=benignpass` with this commit's attack); (C) `allow_anonymous true` on the broker, one line, with the original attacks, contradicting `mosquitto.conf:12`.
- Cost at the broker, CPU per 1000 CONNECT [measured]: 1.03 s with `attacker`, 0.91 s with `benign`, 0.15 s with anonymous accepted, 0.10 s before (refusal). The mosquitto password hash (`$7$`, PBKDF2-SHA512 with 1000 iterations) comes to dominate the cost of the authenticated flood. That cost is mosquitto 2.1.2's; 2.1.4, which the `eclipse-mosquitto:2` tag has given since 2026-11-17, stores the password with 20000 iterations, and the same 1000 CONNECT cost the broker 13.28 to 13.91 s, about 12 times the 2.1.2 cost (12.4 at the median of the ratios of twelve paired measurements, from 8 to 18 times per pair) [measured on 2026-11-18; see MQTT-03].
- Side effect checked: `mqtt-bruteforce` (ralmqtt `3dd72cb`) only tries `admin, root, mosquitto, user, broker, mqtt` (`ralmqtt.py:157`) and its `passwords.txt` has neither `attacker` nor `attackerpass` [read in code], so the new user does not give it a valid pair [inferred]. Against the `8613c66` broker it sent 252 CONNECT with a username (6 users x 42 passwords), all rc=5 [measured].

**Before and after.** `mqtt-publisher-flood`, `COUNT=1000 DELAY_MS=0 PAYLOAD_SIZE=0`, one run per column:

| Measure | Before (`8613c66`) | First-commit broker (`28c8d5f`) | After (this commit) | Alternative B (`benign`, `8613c66` broker) | Alternative C (broker accepting anonymous, `8613c66` attack) |
|---|---|---|---|---|---|
| Attacker CONNECT | 1000, no username | 1000, no username | 1000, user `attacker` | 1000, user `benign` | 1000, no username |
| CONNACK | rc=5 in 1000 | rc=5 in 1000 | rc=0 in 1000 | rc=0 in 1000 | rc=0 in 1000 |
| Attacker PUBLISH | 0 | 0 | 1000 | 1000 | 1000 |
| Attacker DISCONNECT | 0 | 0 | 1000 | 1000 | 1000 |
| messages at the legitimate subscriber | 0 | no subscriber in this run | 1000 | 1000 | 1000 |
| Broker CPU | 0.10 s | not compared | 1.03 s | 0.91 s | 0.15 s |

**How to reproduce.** In the reproduction file, section MQTT-01; uses P1, P2, P3, P9.

**Caveats.**
- On its own, this commit makes lwt be accepted, but the Will is still discarded by the graceful DISCONNECT (MQTT-02). In the measured equivalent (broker accepting anonymous, `8613c66` lwt): 50 CONNACK rc=0, 50 DISCONNECT and 0 Will [measured on the equivalent; lwt with only the credential line was not built separately].
- qos only gets a credential in MQTT-03; without it, it stays anonymous and refused.
- The credential is fixed and public in the repository, like `benign`'s; it suits a lab broker.
- The before and after table is for mosquitto 2.1.2; on 2.1.4 the cost per CONNECT (Fix) and, in a run of the reproduction file on 2026-11-17, the same counts as the item's section were measured; 2.0.18 was only read. `eclipse-mosquitto:2` is a moving tag (`Dockerfile:1`).
- The campaign path (`--network host`, `127.0.0.1`) was not tested.
- The new comments were rewritten in English after the measurements; no line of code changed.

**Versions.** mosquitto 2.1.2 (`eclipse-mosquitto:2` resolved on 2026-11-13; 2.0.18 only read) and 2.1.4 (`eclipse-mosquitto:2` since 2026-11-17; in the cost measurements of 2026-11-18, `eclipse-mosquitto:2.1.4-alpine`, digest sha256 `fa12172a051310efe5bcb7a6a11b77bd5faacb82cbacd7742aa758bf024fd8e4`); `mosquitto-clients` 2.0.18-1build3 (`ubuntu:24.04`); `paho-mqtt` 1.6.1 (pinned); Python 3.11.18 (`python:3.11-alpine`); ralmqtt `3dd72cb`; Docker 29.6.2.

### MQTT-02 · mqtt-lwt-abuse: `disconnect()` Sends A Graceful DISCONNECT, The Broker Discards The Will And The False Alarm Never Goes Out

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/mqtt-lwt-abuse/mqtt-lwt-abuse.py` (line 17) |
| Depends on | MQTT-01 (effect: in the attackzoo flow the broker only keeps the Will if it accepts the CONNECT). The diff was written on top of MQTT-01, in the same file, but applies the same without it, with an offset of -1 line |

**Promise.**
- `docker/attackers/mqtt-lwt-abuse/mqtt-lwt-abuse.py:14`: "# Connect and disconnect abruptly to trigger the LWT."; `:17`: `client.disconnect()  # Dispara Last Will Testament`.
- `docker/attackers/mqtt-lwt-abuse/attack.yaml:5`: "Abuse of the MQTT Last Will and Testament mechanism to force critical publications or false alarms on sensitive topics."

**What happens.** The Will (or LWT) is the message the MQTT client registers in the CONNECT for the broker (the MQTT server) to publish if the connection drops without notice. The attack creates 50 "sensors" that connect with an alarm Will (QoS 2, retained, topic `alerts/device/failure`) and leave. Isolating this cause, with a broker that accepts anonymous and the `8613c66` attack: 50 CONNACK rc=0 (connection accepted), 50 DISCONNECT from the attacker, 0 Will published; the topic's legitimate subscriber receives 0 messages, a late subscriber finds no retained message, and the broker logs `disconnected.` (clean exit) 50 times [measured]. In the attackzoo flow, added to the refusal from MQTT-01: 50 CONNACK rc=5, 50 DISCONNECT, 0 Will [measured]. In every case the script prints `[!] LWT triggered` 50 times (note MQTT-04).

**Cause.**
- `mqtt-lwt-abuse.py:17` calls `client.disconnect()`. In paho-mqtt 1.6.1 the DISCONNECT goes out at once, even with no network loop running (`paho/mqtt/client.py:1345-1358`, `:2821`, `:3013-3016`) [read in code].
- requirement [MQTT-3.14.4-3] of the MQTT 3.1.1 standard (§3.14.4): on receiving DISCONNECT the server "MUST discard any Will Message associated with the current connection without publishing it" [read in code].
- mosquitto 2.1.2: `src/handle_disconnect.c:79-83` only preserves the Will with the MQTT 5 reason code "disconnect with will message" (the MQTT 3.1.1 DISCONNECT, which paho 1.6.1 uses by default, has no reason code and counts as 0) and `src/context.c:216-218`; 2.0.18: `src/handle_disconnect.c:74-75` and `src/context.c:185-187` [read in code].

**How we tested.**
- Images: lwt and broker built from upstream at `8613c66` and with this commit and MQTT-01 (Python 3.11.18, `paho-mqtt` 1.6.1 pinned; `eclipse-mosquitto:2` resolved to mosquitto 2.1.2). Variants only to isolate the cause, outside the commit: broker with `allow_anonymous true`; lwt with only the swap of this line, without the credential.
- Network: broker on 1883, attacker, legitimate subscriber (`mosquitto_sub -u benign -P benignpass -q 2 -t alerts/device/failure -v`) and a late subscriber that starts 3 s after the end (`-C 1 -W 5`), to see the retained Will.
- Arguments: the command that `python3 attackzoo.py run iot_mqtt_lwt_abuse --target <IP> --port 1883` builds: `-e COUNT=50 -e DELAY_MS=100 <IP> 1883`, until it exits on its own (~33 s).
- Six conditions, one run each (table below, plus the one in MQTT-05). Counting with `tshark`: CONNECT with Will, CONNACK by code, DISCONNECT and RST (TCP reset) from the attacker, PUBLISH from the broker to the subscriber and the rest of QoS 2 (PUBREC, PUBREL, PUBCOMP). Broker logs (`disconnected.`, `connection closed by client.`, `not authorised`). Load (load average) from 2.1 to 5.5.
- A second reviewer recounted the pcaps with their own MQTT parser, without the `tshark` dissector, and checked the paho lines inside the image and the mosquitto and specification ones in the originals: everything matches.
- Deviations: extra subscribers that only observe. Not tested: the campaign path [inferred: the discard does not depend on the origin]; mosquitto 2.0.18 (only read); killing the process instead of closing the socket.

**Fix.** `client.disconnect()` becomes `client.socket().close()` (paho public API, `client.py:1711-1713`): the TCP closes without a DISCONNECT, the broker sees the connection drop and publishes the Will. On the wire the attacker closes with an RST [measured: 50 RST]; the likely reason is the CONNACK received and not read [inferred]. One line; ClientId, Will, topic, timings and parameters stay the same. Checking the CONNACK before printing (MQTT-04) and `max_runtime_s` (MQTT-05) remain as notes.

**Before and after.** `COUNT=50 DELAY_MS=100`, one run per row [measured]:

| Condition | CONNACK | Attacker DISCONNECT | Will delivered to the subscriber | Late subscriber |
|---|---|---|---|---|
| Before: `8613c66` broker and attack | rc=5 in 50 | 50 | 0 | nothing ("Timed out") |
| Only the DISCONNECT: broker accepting anonymous, `8613c66` attack | rc=0 in 50 | 50 | 0 | nothing |
| Only the refusal: `8613c66` broker, attack with only this line | rc=5 in 50 | 0 (50 RST) | 0 | nothing |
| Only this line: broker accepting anonymous, attack with only this line | rc=0 in 50 | 0 (50 RST) | 50 (`sensor_0` to `sensor_49`) | receives retained `sensor_49` |
| After: MQTT-01 + this commit | rc=0 in 50, user `attacker` | 0 (50 RST) | 50 | receives retained `sensor_49` |

In AFTER each Will goes out as a QoS 2 PUBLISH to the subscriber, with PUBREC, PUBREL and PUBCOMP (50 of each); the run lasted 33.4 s.

**How to reproduce.** In the reproduction file, section MQTT-02; uses P1, P2, P3, P9.

**Caveats.**
- In the attackzoo flow this commit only has an effect together with MQTT-01: with the CONNECT refused the broker deletes the Will before any drop (measured in isolation: 0 Will).
- The script still prints "LWT triggered" without checking anything (MQTT-04) and `max_runtime_s: 10` cuts the loop (MQTT-05).
- Measured on mosquitto 2.1.2 (and, in a run of the reproduction file on 2026-11-17, on 2.1.4, with the same counts); 2.0.18 was only read. Campaign path not tested.
- The line's new comment was rewritten in English after the measurements; the code is the one measured.

**Versions.** `paho-mqtt` 1.6.1 (pinned in `requirements.txt`); Python 3.11.18 (`python:3.11-alpine`); mosquitto 2.1.2 (`eclipse-mosquitto:2` on 2026-11-13; 2.0.18 only read) and 2.1.4 (`eclipse-mosquitto:2` on 2026-11-17, only in that run); MQTT 3.1.1 specification (OASIS); Docker 29.6.2.

### MQTT-03 · mqtt-qos-amplification: Without The paho Network Loop, Each Client Sends At Most 20 QoS 2 PUBLISH And No PUBREL

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/mqtt-qos-amplification/mqtt-qos-amplification.py` |
| Depends on | MQTT-01 (effect: the `attacker` user must exist on the broker; without it, CONNACK rc=5) |

**Promise.**
- `docker/attackers/mqtt-qos-amplification/attack.yaml:5`: "Traffic and state-load amplification on the MQTT broker through multiple QoS 2 handshakes."
- `mqtt-qos-amplification.py:12-13`: "# QoS 2 garante entrega exatamente uma vez - 4 handshakes!" (the comment says this QoS level guarantees exactly-once delivery with four handshakes) / "# PUBLISH -> PUBREC -> PUBREL -> PUBCOMP"; `:30`: "# clients x QoS 2 messages".
- Defaults: `attack.yaml:29-32` (`threads` 2000, `count` 2000), repeated in `README.md:29-30`.

**What happens.** QoS 2 is the "exactly once" delivery level of MQTT: each message takes four packets (PUBLISH from the client, PUBREC from the broker, PUBREL from the client, PUBCOMP from the broker). The attack never completes this cycle [measured]:
- Isolated from MQTT-01's refusal (broker accepting anonymous): with 20 clients x 200 messages, 400 PUBLISH (at most 20 per client), 400 PUBREC, 0 PUBREL and 0 PUBCOMP; at the defaults, in a 20 s window, 1525 connections, 30134 PUBLISH (at most 20 per connection), 29702 PUBREC and 0 PUBREL. The other messages of each client never leave.
- With the refusal, as in attackzoo today (anonymous attack on `8613c66`; the `8613c66` broker and MQTT-01's broker refuse anonymous the same way): 20x200 gives 20 CONNECT, 20 CONNACK rc=5 and 20 to 21 PUBLISH (one run with each broker), 0 PUBREC; at the defaults, 20 s, with MQTT-01's broker: 1580 CONNECT, 1580 CONNACK rc=5, 1646 PUBLISH, 0 PUBREC (in another run, with the `8613c66` broker, 1247 CONNECT and 3233 PUBLISH; see MQTT-01). The ramp is also slow: CONNECT number 1000 goes out at 13.5 s and number 1580 at 20.9 s from the start of the capture (the first, at 0.7 s); never 2000 clients in the window.
- The script prints "Client N completed QoS amplification" for each client and exits with 0, even when nothing was accepted.
- Same with mosquitto 2.1.4, which the `eclipse-mosquitto:2` tag in the broker's `Dockerfile` has given since 2026-11-17 (the numbers above are from 2.1.2) [measured on 2026-11-18, at the defaults, stopped at 20 s, two runs per condition]: with the attack and the `8613c66` broker, 1608 and 1550 CONNECT, all with CONNACK rc=5, and 0 PUBREC; with the `8613c66` attack plus only the credential line (no network loop), against MQTT-01's broker, 1232 and 1255 CONNECT accepted, 24503 and 24947 PUBLISH, 1297 and 1433 PUBREC and 0 PUBREL. With 2.1.4 the broker sends PUBREC to few PUBLISH because it takes long to verify the password and, by the time it gets to the CONNECT, the client has already sent the 20 PUBLISH and the DISCONNECT and closed [inferred from timing; the DISCONNECT are in the pcap].
- 2.1.4 also changes what the fix has to withstand: each authenticated CONNECT costs the broker about 12 times the CPU of 2.1.2 (13.28 to 13.91 s per 1000 CONNECT, against 0.78 to 1.70 s, in twelve measurements of each; 8 to 18 times per pair, 12.4 at the median of the ratios; median from CONNECT to CONNACK, read in six of them, 12.23 to 12.34 ms against 0.71 to 1.31 ms) [measured]. In the burst of 2000 clients, the SYN of some of them goes unanswered for more than 5 s (Cause), and a client that does not handle the `connect()` failure dies with an exception (Fix, item 6).

**Cause.**
- `mqtt-qos-amplification.py:9-19` does `connect()`, `publish(qos=2)` COUNT times and `disconnect()`, with no `loop_start()`, `loop()` or `loop_forever()` [read in code].
- paho-mqtt 1.6.1 [read inside the image]: `client.py:585` (`_max_inflight_messages = 20`): `publish` only sends with fewer than 20 messages in flight and keeps the rest in `_out_messages` (`:1279-1280`, `:1298`); a slot only opens when the client processes the PUBCOMP read from the socket (`:3482-3504`), and with no network loop nobody reads the socket: the PUBREC is never processed, so the PUBREL never goes out.
- Mosquitto 2.1.3, from 2026-11-17 [read in the source code of tags `v2.1.2` and `v2.1.4`]: `ChangeLog.txt:45` "Increase default iterations for sha512-pbkdf2 to 20000 and document it."; `libcommon/password_common.c:47` defines `PW_DEFAULT_ITERATIONS` as 20000 (1000 on the same line in 2.1.2). 2.1.4 came out the same day and, for passwords, only fixes the refusal of legacy hashes. The iteration count is stored in the password file that the broker `Dockerfile`'s `mosquitto_passwd -b` generates at build time (`$7$20000$` with the 2.1.4 base, `$7$1000$` with the 2.1.2 one [measured in the images]), and each CONNECT redoes the PBKDF2 with that number (`plugins/password-file/password_check.c:45` → `mosquitto_pw_verify` → `password_common.c:234-242`).
- A single event loop in the broker [read in code, 2.1.4]: `src/mux_epoll.c:165-190` handles the client events (the CONNECT, with the password check) and then accepts the pending connections, and the `listen()` queue is 100 (`src/net.c:910`). While the loop verifies passwords nobody calls `accept()`, the queue fills and the kernel drops the following SYN [read in code; the drop measured by the `ListenOverflows` counter of the broker's kernel: 8234 to 9433 per run on 2.1.4 with the fix without the retry, against 1922 to 2561 on 2.1.2, where the queue empties in ~3 s].
- paho-mqtt 1.6.1 [read inside the image]: `connect()` waits for TCP to open for a fixed 5 s (`client.py:537`, `self._connect_timeout = 5.0`, no public setter in this version; `:3680-3685`, `socket.create_connection(..., timeout=self._connect_timeout, ...)`); with no reply to the SYN in that time, `TimeoutError: timed out` is raised. Unhandled, the exception ends the client's thread, which does not try again. With 2.1.2 the broker empties the queue in ~3 s and every `connect()` finishes before the 5 s; with 2.1.4 the queue stays full for more than 5 s.

**How we tested.**
- Images: the attack built from upstream at `8613c66` (BEFORE) and with this commit (AFTER); for comparison, a minimal alternative (only `loop_start()` after the `connect()` and `loop_stop()` before the `disconnect()`, plus the credential). All with Python 3.11.18 and `paho-mqtt` 1.6.1 (`client.py` with the same sha256); the `.py` inside each image checked against the tree. In the runs from 2026-11-13 to 2026-11-17, the broker is the same in all: the `8613c66` one with MQTT-01's `attacker` user (mosquitto 2.1.2). The separation of the refusal used earlier runs with a broker accepting anonymous.
- Network: broker on 1883 with `--memory 1g`, attacker with `--memory 2500m --memory-swap 2500m` (our limits; no container was killed for memory).
- Arguments: the command that `python3 attackzoo.py run iot_mqtt_qos_amplification --target <IP> --port 1883` builds (`-e THREADS=2000 -e COUNT=2000 -e DELAY_MS=0 <IP> 1883`). At the defaults the attack was stopped with `docker kill` at 20 s, the effect of the `docker rm -f` of the published campaign's 20 s window. Exact counts with the attack running until it exits: 20x200, 2000x20 and 5x20 with `DELAY_MS=100`.
- Count with `tshark` by MQTT type (`mqtt.hdrflags`), by CONNACK code and by TCP connection (`tcp.stream`: PUBCOMP per connection, maximum of sessions open together, instant of the k-th CONNECT), retransmissions (`tcp.analysis.retransmission`). Logs: `completed`, `lost connection` and `Traceback` on the attacker; `Unable to accept new connection` on the broker. Samples at 5, 10 and 15 s: open descriptors (fd) and the `nofile` limit (the per-process file descriptor limit) of the attacker and the broker, connections established on 1883. Memory and CPU from the cgroup.
- One run per condition in the numbers cited; a second run of the AFTER under higher load (below). Machine load (load average) from 2.3 to 11.7, with other tests in parallel; the volume in 20 s is only compared between neighboring runs.
- A second reviewer recounted the 27 pcaps of this measurement and the 2 of the separation with a parser of their own for MQTT (own TCP reassembly, no `tshark`): all counts match. They also redid the variant without a common start (780 clients in 20 s, against 763) and measured inside the image that `select()` fails and `poll()` works with a descriptor above 1023, and that paho's `loop()` returns `MQTT_ERR_CONN_LOST` with descriptor 1103.
- Mosquitto 2.1.4, on 2026-11-18: MQTT-01's broker built with the base pinned by digest in each version (`--build-context`, without changing the `Dockerfile`), checked by `mosquitto -h` (`version 2.1.2` and `version 2.1.4`) and by the password file (`$7$1000` and `$7$20000`). Attacks: the `8613c66` one; the `8613c66` one with only the credential line (no network loop); this commit without the connection retry (items 1 to 5 of the Fix); this commit. Python 3.11.18 and `paho-mqtt` 1.6.1 in all; the `.py` inside each image checked against the tree (sha256). Same network, limits and arguments as the test above; defaults stopped at 20 s; until exit: 20x200, 2000x20, and 20x20 and 2000x2000 against a port with no service. In our runs, before each one, 1-minute load below 1.5 (0.15 to 1.46) and 60 s with no other test on the machine, except in three of those cited: the 1640 CONNECT one of the longer timeout (another test ran alongside), one of the two of the semaphore (it started 40 s after another test) and one of the 5 of the fix without the retry on 2.1.4 (a count of ours, with `tshark`, ran alongside); in the executions of the reproduction file's section, load below 1.5 at the start (up to 1.49). Besides the counts above: TCP connections and SYN of the attacker, CONNACK within 10 s of the first SYN, the `ListenOverflows` and `SyncookiesFailed` counters of the broker's kernel, the `connect failed`, `could not connect`, `lost connection` and `Exception in thread` lines of the attacker and `New client connected` of the broker. Cost per CONNECT: MQTT-01's `mqtt-publisher-flood` (1000 authenticated CONNECT in sequence), broker CPU from the cgroup. This commit was measured with the retry's 20 s deadline and, earlier, with 60 s; within the 20 s window the two run the same path (0 `could not connect` in all runs), and the ranges below combine the two.
- Two independent reviewers, each with their own runner and MQTT counter (pure Python, no `tshark`), redid runs on both versions, executed as written the two blocks that the reproduction file's section then had (today the second and the third, the ones that compare the two versions) and recounted the pcaps: the counts match. The ranges below combine our runs, the reproductions and theirs; their corrections are in the text (the SYN cookie failure mode (a reply to the SYN that the kernel gives without keeping state, when the pending connection queue is full), the 10 s window, the dead target and wider ranges).
- Deviations: memory limits; in six isolation runs (two of them cited below, marked) the broker came up with `--ulimit nofile=8192` (not the attackzoo flow; it only takes the broker out of the equation). Not tested: the campaign path (`--network host`, `127.0.0.1` via docker-proxy, the Docker process that forwards the port published with `-p` to the container); a Docker daemon with another default `nofile`.

**Fix.** Only the `.py`:
1. No `loop_start()`, `loop()` or `select()`: each thread runs its own client's network with `select.poll()` on `client.socket()` and `loop_read()`, `loop_write()` and `loop_misc()`, paho's public API for an external loop (`client.py:1538-1626`, `:1711`). One descriptor per client.
2. `resource.setrlimit(RLIMIT_NOFILE, (hard, hard))`: the soft descriptor limit rises to the hard one (from 1024 to 524288 on this Docker).
3. Window of 20 messages in flight (paho's default `max_inflight`): the next message is only created when there is a slot, instead of queueing all COUNT at once; `on_publish` counts the PUBCOMP.
4. Common start (`threading.Event`): each thread connects and waits; all start publishing after the last one was created (the `start.set()` is in a `finally`).
5. Credential `MQTT_USER`/`MQTT_PASS` (default `attacker`/`attackerpass`), as in MQTT-01. If the connection drops, the client prints `lost connection after N/COUNT` instead of `completed`.
6. Connection retry: if `connect()` fails (`OSError`, which covers the timeout and the refusal), the client prints `Client N connect failed (<error>), retrying` and tries again 1 s later, up to 20 s after the first attempt; past the deadline, it prints `Client N could not connect: <error>` and the thread exits. Both lines go out with `flush=True`. The 1 s and the 20 s (the campaign window) are our choices.

Staying the same: `paho-mqtt==1.6.1`, `attack.yaml`, `Dockerfile`, `entrypoint.sh`, README, THREADS threads, topic `amp/target`, payload `QoS2_Amplified_<id>_<i>`, ClientId `amplifier_<id>` and `DELAY_MS` as the pause between PUBLISH of the same client (measured: 0.100 s with `DELAY_MS=100`).

Changes on the wire (declared): the clients only publish after the common start; the burst of 2000 `connect()` generates retransmitted SYN (1607 in the run cited; the cause is the 100-connection `listen()` queue of mosquitto, `src/net.c:910`, inferred in that test and measured on 2026-11-18, Caveats); the DISCONNECT goes out 0.1 to 0.2 ms after the last PUBCOMP; with 2.1.4, the retries of item 6: more TCP connections than clients (3058 to 4262 in 20 s) and 1058 to 2334 `connect failed` lines in the log, and, against a target that refuses the connection, one attempt per second per client until the deadline (Caveats).

Isolated pieces [measured]: without the common start, only 763 clients connect in 20 s (780 in the second reviewer's repeat), because the main thread creates the others while contending for the GIL (Python's global lock) with the clients already active [inferred]; without the `setrlimit` (broker with `nofile` 8192), 1021 CONNECT and 933 CONNACK.

Why the retry (item 6) [measured on 2026-11-18]: without it, on 2.1.4, at the defaults and stopped at 20 s, only 574 to 1013 of the 2000 clients send CONNECT and 480 to 694 receive CONNACK (5 runs; 719 to 1367 and 625 to 685 in 3 executions on 2026-11-17 of the reproduction file, two of the section and one diagnostic, with the earlier version of the commit, without the retry, and the P9 broker still without the pinned base), and each client that did not connect dies with an exception in the thread: the `Exception in thread` lines are exactly 2000 minus the CONNECT in every run, and the `Traceback` counted (987 to 1416) are a floor, because the SIGKILL cuts the output of the threads still printing. The type, `TimeoutError: timed out`, appears in full in the run that goes to the end (1148 of 1148). From +3.4 to +4.7 s after the first SYN on, no new CONNECT goes out. On 2.1.2 the retry changes nothing: 2000 CONNECT, 1016 CONNACK and no new line, as without it.

Alternatives measured on 2.1.4 and not proposed: a longer connection timeout (`client._connect_timeout = 60`, a private attribute of paho 1.6.1, and a `try` with no retry) leaves the attempts to the kernel's SYN retransmission (1, 3, 7, 15 s) and gives 1640 (in a run with another test running alongside) and 1806 CONNECT in 20 s; a semaphore of 100 clients until the CONNACK gives the same counts as this commit (2000 and 1637 CONNECT, 1016 CONNACK, 0 `Traceback`) without a dropped SYN, but ties the attack to mosquitto's queue of 100, waits for the CONNACK before the common start and does not retry if `connect()` fails for another reason.

Why not the minimal alternative: it closes the cycle on a small scale (20x200: 4000 of each type), but at the defaults only 345 clients connect in 20 s. With `loop_start()` each client uses 3 descriptors (the socket and an internal socket pair, `client.py:275-294`, `:1795`), the container's `nofile` is 1024 (attackzoo runs without `--ulimit`, `modules/runners.py:147`), and raising `nofile` is not enough, because paho's `select()` (`client.py:1150`) does not accept a descriptor above 1023 and the error becomes `MQTT_ERR_CONN_LOST` (`:1154-1157`). Besides, each client keeps all COUNT messages in the queue: 1337 MB on the attacker with 345 clients. The log had 155 tracebacks, with `OSError: [Errno 24]` visible in 1 (the rest was cut by the SIGKILL); in the runs that end on their own, 70 of 70 and 336 of 336 are `Errno 24`. Largest THREADS the minimal alternative handles with the default `nofile` [measured]: 300x200 and 340x200 clean (300 and 340 complete clients, 0 tracebacks, 177 and 170 MB); 400x200 with 347 CONNECT and 70 tracebacks; 1000x200 with 829 CONNECT and 336 tracebacks; with COUNT=2000, 300 clients reach 1188 MB and 340 reach 1341 MB in 20 s. 340 is the calculated limit (340 x 3 + 3 = 1023 of 1024 descriptors); 341 to 399 were not run. Lowering the default to 300 would keep the minimal alternative, but would change the `attack.yaml` parameter (it stops being "2000 clients") and would depend on the daemon's `nofile`.

Another alternative measured and not proposed: a single `epoll` loop with no threads. With the default broker: 1016 CONNACK, 208355 PUBLISH and 202456 PUBCOMP in 20 s, with 14.3 s of CPU on the attacker (against 50.1 s); but it rewrites the attack, ignores `DELAY_MS` and the sequential `connect()` blocks 1 s for each lost SYN.

**Before and after.** The first two tables are from the test with mosquitto 2.1.2, measured before item 6 of the Fix (the retry); on 2.1.2 it does not change the result (counts within the variation between runs: 2000 CONNECT, 1016 CONNACK, 0 `Traceback`, no new line; 2000x20 until exit: 1036 CONNACK and 961 `lost connection`, against 1034 and 966 in the second table) [measured on 2026-11-18]. Defaults (`THREADS=2000 COUNT=2000 DELAY_MS=0`), stopped at 20 s, MQTT-01's broker with default `nofile`, one run per column [measured]:

| Measure | Before (`8613c66`) | Minimal alternative (`loop_start`/`loop_stop`) | After (this commit) |
|---|---|---|---|
| CONNECT | 1580 | 345 | 2000 (between 1.12 and 3.84 s) |
| CONNACK rc=0 | 0 (rc=5 in 1580) | 345 | 1016 |
| PUBLISH | 1646 | 112009 | 113755 |
| PUBREC | 0 | 112009 | 113561 |
| PUBREL and PUBCOMP (each) | 0 | 108537 | 112714 |
| PUBCOMP per session | 0 | n/a | 87 to 137 |
| Retransmitted SYN | 0 | 0 | 1607 |
| Broker CPU | 0.27 s | 3.81 s | 8.22 s |
| attacker peak memory | 33 MB | 1337 MB | 145 MB |
| tracebacks in the attacker log | 0 | 155 | 0 |

A second run of the AFTER, with more load on the machine (load up to 11.7): 2000 CONNECT, 1016 CONNACK rc=0, 73855 PUBLISH, 72761 PUBCOMP, 143 MB.

Exact counts, until exit [measured]:

| Run | CONNECT | CONNACK rc=0 | PUBLISH | PUBREC | PUBREL | PUBCOMP | DISCONNECT | Attacker log |
|---|---|---|---|---|---|---|---|---|
| 20x200, before | 20 | 0 (rc=5 in 20) | 21 | 0 | 0 | 0 | 0 | 20 false `completed` |
| 20x200, after | 20 | 20 | 4000 | 4000 | 4000 | 4000 | 20 | 200 PUBCOMP on each connection |
| 2000x20, after, default broker | 2000 | 1034 | 21721 | 20680 | 20680 | 20680 | 1034 | 1034 `completed`, 966 `lost connection` |
| 2000x20, after, broker with `nofile` 8192 (deviation) | 2000 | 2000 | 40000 | 40000 | 40000 | 40000 | 2000 | 2000 `completed` |
| 5x20 with `DELAY_MS=100`, after | 5 | 5 | 100 | 100 | 100 | 100 | 5 | interval between PUBLISH of 0.100 s |

On both mosquitto versions [measured on 2026-11-18; load below 1.5 at the start of each run; in one of the 5 runs of the fix without the retry on 2.1.4, a count of ours ran alongside]: defaults, stopped at 20 s, MQTT-01's broker (in the BEFORE, the `8613c66` one) with each version's base. CONNACK rc=0, PUBREL = PUBCOMP, `Traceback`, `connect failed` and `Unable to accept` counted in each run; "-" when the code does not print the line.

| Attack | Broker | Runs | CONNECT | CONNACK rc=0 | PUBREL = PUBCOMP | `Traceback` | `connect failed` | `Unable to accept` | Broker CPU |
|---|---|---|---|---|---|---|---|---|---|
| Before (`8613c66`) | 2.1.2 | 2 | 1258, 1560 | 0 (rc=5 in all) | 0 | 0 | - | 0 | 0.19 and 0.22 s |
| Before (`8613c66`) | 2.1.4 | 2 | 1608, 1550 | 0 (rc=5 in all) | 0 | 0 | - | 0 | 0.22 s |
| Only the credential, no network loop | 2.1.2 | 2 | 1366, 1587 | all | 0 (PUBREC 27227 and 31614) | 0 | - | 0 | 1.63 and 1.85 s |
| Only the credential, no network loop | 2.1.4 | 2 | 1232, 1255 | all | 0 (PUBREC 1297 and 1433) | 0 | - | 0 | 20.60 and 20.83 s |
| This commit without the retry (items 1 to 5) | 2.1.2 | 2 | 2000, 2000 | 1016, 1016 | 123617, 127351 | 0 | - | 895, 939 | 8.32 and 8.33 s |
| This commit without the retry (items 1 to 5) | 2.1.4 | 5 | 574 to 1013 | 480 to 694 | 69249 to 82852 (in 4) | 987 to 1416 (floor) | - | 0 | 11.80 to 15.32 s |
| This commit | 2.1.2 | 2 | 2000, 2000 | 1016, 1016 | 128358, 131504 | 0 | 0 | 871, 837 | 8.39 and 8.30 s |
| This commit | 2.1.4 | 3 | 2000, 2000, 1741 | 1016 in the 3 | 83956 to 87300 | 0 | 2080, 1650, 1773 | 690, 391, 234 | 17.76 to 18.55 s |

In all runs of this commit on 2.1.4 stopped at 20 s (19 runs: ours, the reproductions' and the reviewers', with both deadlines): 1010 to 1017 CONNACK, 1484 to 2000 CONNECT, 3058 to 4262 TCP connections, 0 `Traceback`, 0 `could not connect`, 1058 to 2334 `connect failed`, 86 to 690 `Unable to accept`, 266 to 683 SYN cookies refused by the broker's kernel (`SyncookiesFailed`, counted in 12), PUBREL = PUBCOMP from 78379 to 87300 and broker CPU from 17.8 to 18.9 s. On 2.1.2 (14 runs: ours, the reproduction file section's third block's and the reviewers'): 2000 CONNECT, 1016 CONNACK, 0 `Traceback`, 0 `connect failed`, 811 to 961 `Unable to accept` and 24 to 175 SYN cookies refused (counted in 8); in the three executions on 2026-11-18 of the section's first block, which are not among those 14, 2000 CONNECT, 1016 CONNACK, 0 `Traceback` and 835, 984 and 886 `Unable to accept`. On 2.1.4 the broker reaches the same ceiling as 2.1.2, 1016 connections open at the same time (the total CONNACK in the pcap can exceed it by 1; Caveats); the QoS 2 volume in 20 s is below 2.1.2 (PUBCOMP 78379 to 87300, against 128358 to 142266 in our runs on 2.1.2), because the broker spends ~18 s of CPU, much of it verifying passwords [measured; the split of the time is inferred]. It is not a defect of the attack.

Until exit, on 2.1.4 [measured]: 20x200 with this commit gives 20 CONNACK, 4000 of each of the types PUBLISH, PUBREC, PUBREL and PUBCOMP and 20 DISCONNECT, as on 2.1.2. With 2000x20:

| Run | Duration | CONNECT | CONNACK rc=0 | PUBCOMP | Attacker log | Broker kernel |
|---|---|---|---|---|---|---|
| This commit | 21.2 s | 2000 (the last at +15.5 s) | 1378 | 27560 | 1376 `completed`, 620 `lost connection`, 1421 `connect failed`, 0 `could not connect`, 0 `Traceback` | 622 RST from the broker, `SyncookiesFailed` 622; 0 `Unable to accept` |
| This commit without the retry | 11.4 s | 852 | 478 | 9560 | 476 `completed`, 372 `lost connection`, 1148 `Traceback` (`TimeoutError`) | not read |

**How to reproduce.** In the reproduction file, section MQTT-03; uses P1, P2, P3, P4, P9.

**Caveats.**
- With this commit, `THREADS=2000` exhausts the broker's descriptors in the attackzoo flow itself: the broker accepts at most 1016 simultaneous connections, logs "Unable to accept new connection, system socket count has been exceeded. Try increasing "ulimit -n" or equivalent." (984 times in the run cited) and closes the excess. It is an effect on the target, logged by it, and not a defect of the attack. The 1016 comes from the containers' default `nofile` on this Docker 29.6.2 (1024 soft, 524288 hard): mosquitto (2.1.2 and 2.1.4) does not call `setrlimit` and `servers.sh:110` brings the broker up without `--ulimit`. On a daemon with another default (`default-ulimits`, the service's `LimitNOFILE`, Docker Desktop) the number changes.
- The `setrlimit` only helps if the hard limit is larger than the soft one; on a daemon with both at 1024 the gain disappears [inferred].
- The volume in 20 s depends on the machine (113755 and 73855 PUBLISH in two runs with different loads); the conclusions use counts bounded by descriptors and memory, not rates.
- The cause of the retransmitted SYN (mosquitto's `listen()` queue) was inferred in the test with 2.1.2, in which the queue overflow counter was not read; on 2026-11-18 it was read (the broker kernel's `ListenOverflows`), per run stopped at 20 s [measured]: on 2.1.2, 1922 to 2561 with the fix without the retry (2 runs) and 2163 to 2727 with this commit (5); on 2.1.4, 8234 to 9433 without it (5) and 13406 to 17802 with this commit (10). The reproductions do not read this counter.
- On 2.1.4 there is a second failure mode, which the retry does not cover [measured; the reading of why is inferred]: with the `listen()` queue full, the broker's kernel answers some of the SYN with a SYN cookie, and some of those connections are not accepted: the client's CONNECT gets an RST ~0.2 s later, mosquitto never sees that client, and the thread ends with `lost connection after 0/COUNT`, without trying again, because only the `connect()` failure is handled. Until exit, with 2000x20, 622 of the 2000 clients are lost this way (`SyncookiesFailed` 622; 527 and 722 in two runs with the 60 s deadline). In the 20 s window the effect is hidden by the ceiling of 1016 (266 to 683 `SyncookiesFailed` per run). The fix without the retry also has this mode. Treating the drop before the CONNACK as a `connect()` failure would be a possible extension, not measured.
- The ceiling of ~1016 CONNACK (1010 to 1017 per run) is that of the campaign's 20 s window. The 1016 is the maximum of connections open at the same time (first caveat); the total CONNACK in the pcap can exceed it by 1 [measured in the run with 1017, the only one of 19]: in it, at most 1016 connections with CONNACK stayed open together; the 1017th had been trying since +12.4 s from the first SYN, the broker's kernel retransmitted its SYN-ACK and only confirmed the retransmitted CONNECT at +20.3 s, when the `docker kill` closed the other connections, and the broker sent the CONNACK and 20 PUBREC 32 ms after the client's FIN, within the 3 s in which the capture continues after the kill. attackzoo's interface stops the attack at `max_runtime_s: 10` (`attack.yaml:8`; `modules/attackzoo_st.py:163-188`): up to +10 s from the first SYN, on 2.1.4, this commit has 614 to 653 CONNACK (16 runs) and the fix without the retry 449 to 614 (5); the PUBCOMP up to +10 s is not larger (19552 to 25325 against 13548 to 29972). At 10 s, the retry mainly removes the `Traceback`. On 2.1.2 the 1016 CONNACK go out in the first 2 s.
- Against a target that refuses the connection (a port with no service), the `8613c66` attack and the fix without the retry die in ~1 s (with 20x20, 20 `Traceback` with `ConnectionRefusedError`); this commit keeps trying until the deadline, one attempt per second per client, and ends on its own, with exit 0 and the final line "QoS Amplification attack completed" [measured on 2.1.4, port 1884 with no service]: 20x20 in 21.1 s, with 420 SYN and 420 log lines (400 `connect failed` and 20 `could not connect`); at the defaults, in 22.5 s, with 36,364 SYN, all answered with RST, and 36,364 lines (34,364 `connect failed` and 2000 `could not connect`), 18 to 20 attempts per client (with 2000 threads, each turn of the loop takes more than 1 s); 0 `Traceback`. A client gives up at most ~26 s after the first attempt: a failure just before the deadline still leads to one more attempt, 1 s later, which can wait the paho's 5 s [read in code]. Within the 20 s window no client reaches `could not connect`: the attempts come in waves of ~6 s (paho's 5 s plus 1 s; new SYN at +0, +6, +12 to 13 and +18 to 20 s from the first SYN) and the next failure would fall after the cut [measured in the pcaps; the instant of the next failure is inferred]. A target that drops the SYN without answering would give ~4 attempts per client in 20 s [inferred; not measured]. In the campaign the 20 s window cuts earlier.
- The `eclipse-mosquitto:2` tag is moving (`docker/servers/mqtt-broker/Dockerfile:1`) and changed between our measurements (GEN-02): the numbers of the test with 2.1.2 do not hold for whoever builds today without pinning the base. The commit does not pin the version; it works on both.
- The memory of the minimal alternative with 2000 clients would exceed the test's 2500 MB [inferred; not run so as not to cause an out-of-memory condition].
- Campaign path (`--network host`, `127.0.0.1` via docker-proxy) not tested.
- Depends on MQTT-01's `attacker` user on the broker.
- The new comments were rewritten in English after the measurements with 2.1.2, without changing a line of code; the measurements with 2.1.4 already used the final comments, and the retry with the 20 s deadline was measured with the final `.py`.

**Versions.** `paho-mqtt` 1.6.1 (pinned; `client.py` the same in all images); Python 3.11.18 (`python:3.11-alpine`); mosquitto 2.1.2 (`eclipse-mosquitto:2` on 2026-11-13; base pinned at `eclipse-mosquitto:2.1.2-alpine`, digest sha256 `75d6662dee52c947dc9dd9c29f1d8d7ffef78ddaf38001caa09755681e8bbc98`, in the 2026-11-18 measurements) and mosquitto 2.1.4 (`eclipse-mosquitto:2` since 2026-11-17; `eclipse-mosquitto:2.1.4-alpine`, digest sha256 `fa12172a051310efe5bcb7a6a11b77bd5faacb82cbacd7742aa758bf024fd8e4`, the same as tag `2` on 2026-11-18); mosquitto source code read at tags `v2.1.2` (`99fa50f3`) and `v2.1.4` (`d69b6b75`); Docker 29.6.2 (containers' default `nofile` 1024/524288).

## Commits: CoAP

### COAP-01 · coap-server And coap-response-fuzz: The Server Dies On The First Datagram The Parser Rejects And Nothing In attackzoo Brings It Back

| | |
|---|---|
| Class | (b) inconsistency between parts of attackzoo |
| In this PR | commit |
| Files | `servers.sh` (root, line 113), `docker/build-images.sh` (line 65), `docker/servers/coap-server/server.yaml` (line 16), `docker/servers/coap-server/README.md` (line 22) |
| Depends on | none |

**Promise.**
- `docker/servers/coap-server/server.yaml:18` (same in `README.md:3`): "Serve as a target for CoAP GET requests, resource discovery, fuzzing, and token collisions."; `server.yaml:23-27` lists `iot_coap_get_flood`, `iot_coap_resource_exhaustion`, `iot_coap_response_fuzz` and `iot_coap_token_collision`.
- `docker/attackers/coap-response-fuzz/attack.yaml:5`: "Burst of randomized or mutated CoAP messages intended to trigger errors, exceptions, or crashes on the target." Bringing the target down is the goal of the fuzz; the defect is that the declared target of fuzzing and of Token collisions does not come back.
- `docker/attackers/coap-token-collision/attack.yaml:5` and `:9-10` (`target_services: coap-server`): the attack that the campaign runs after the fuzz aims at the same server (`contrib/scripts/run_full_campaign.py:73-76`).

**What happens.** The CoAP target (CoAP is a request and response protocol over UDP, port 5683) is CoAPServer, a third-party project. `coap-response-fuzz` brings it down on the fourth request (method code 0.08, which RFC 7252 does not define; it is the seventh datagram from the attacker, counting the empty ACKs the client sends), within a few seconds (2 to 5 s measured). The process exits with code 1 (`ValueError: '0.08' is not a valid CoapCode`) and, since the container starts with `--rm`, it is deleted. Nothing in attackzoo starts it again [measured]:
- the rest of the fuzz runs against a dead target: 0 PUT and 0 POST reach the wire (the kernel returns `[Errno 113] Host is unreachable`); attackzoo's own availability probe (`probe_coap`) gives ok in 72 of 1130 samples during the fuzz, all before the crash;
- the `coap-token-collision` run right after gets 0 responses (406 `Errno 113` errors);
- in an emulation of the campaign timeline (10 s wait, 20 s attack and 10 s pause per run; server started once), the fuzz's second run and the `coap-token-collision` run do not exchange a single CoAP datagram with the server.

The server also dies with valid CoAP and with a malformed datagram (one datagram of each against a new server) [measured]: GET with Observe (option 6), Block2 (23), Size2 (28), No-Response (258) or Request-Tag (292); PUT with Block1 (27, which the fuzz itself generates in the 65535 and 100000 byte PUT); a datagram with fewer than 4 bytes and a truncated extended option header (both with `IndexError`); value 15 in the option delta or length field. All end the process with code 1. By RFC 7252, an unknown elective option must be ignored (§5.4.1), an unknown critical option calls for 4.02 and an unknown method calls for 4.05 (§5.8) [read in code]. In the fuzz's aiocoap 0.4.7, codes 0 and 255 do not even leave the client: when routing, aiocoap reads `message.requested_scheme` (`aiocoap/transports/tcp.py:410`), which for a code that is not a request accesses `self.request` (`aiocoap/message.py:587-591`) and raises `AttributeError` [measured + read in code].

**Cause.**
- CoAPServer `744cc22` [read in code]: `coap_server/request_handler.py:31` calls `parse_message` before the `try` at `:34`; `coap_server/utils/parser.py:50` (`CoapOption(...)`) and `:63` (`CoapCode(...)`) raise `ValueError` outside the enumerations (`coap_server/utils/constants.py:56-73` only has options 1, 3, 4, 5, 7, 8, 11, 12, 14, 15, 17, 20, 35, 39 and 60; `:5-49` has no 0.08, 0.15 or 0.31); `parser.py:17` and `:29` index without checking the size; `:35` and `:47` raise `ValueError` on purpose; `coap_server/server.py:36-56` only handles `socket.timeout`, `KeyboardInterrupt` and `OSError`, so the exception ends the process.
- attackzoo [read in code]: `docker/servers/coap-server/Dockerfile:3` clones CoAPServer without a ref and `:9` runs the cloned package; `servers.sh:113` and `docker/build-images.sh:65` start the container with `--rm` and no restart policy; `contrib/scripts/run_full_campaign.py:937` calls `start_servers` once, before the loop at `:963`, which restarts nothing; `modules/attackzoo/experiment.py:145-146` runs all levels and runs of an attack in sequence.

**How we tested.**
- Images: server, `coap-response-fuzz` and `coap-token-collision` built from upstream at `8613c66` (cloned CoAPServer = `744cc22`, checked inside the image). The same server image on both sides: this commit does not change an image, and BEFORE and AFTER differ only in `--rm` swapped for `--restart on-failure` in the start line.
- Network: server, fuzz, second fuzz, `coap-token-collision` and probe, each on its own IP. Server with the `servers.sh:113` line swapping only the mode, plus the test's name, network and IP, with `--memory 1g`.
- Attacks as in each one's README (`docker run ... <IP> 5683`, no `-e`; it is also what `attackzoo.py run` builds). In the complete runs, the fuzz runs until it exits on its own and the `coap-token-collision` starts right after. In the campaign emulation, each attack runs 20 s and is stopped with `docker kill`.
- Probe: attackzoo's own `probe_coap` (`modules/attackzoo/probes.py:290-328`: one CON GET `/.well-known/core`, ok if the Token comes back and the code is not empty, so 4.04 counts as alive; CON is the confirmable message, which asks for an ACK), imported from the clone in read-only mode. Every 0.2 s with a 0.2 s timeout in the complete runs; like `probe_loop` (`probes.py:442-465`: probe, then 0.5 s; timeout 2.0 s) in the campaign emulation.
- Counting with `tshark` filters by direction (`ip.src`, `udp.dstport==5683`, `!icmp`), PUT and POST (`coap.code==2 || coap.code==3`), ICMP and ARP. The server's `docker events` (`die` with exit code and run time, `start`), the server log (one traceback per crash), `RestartCount`.
- Runs: complete, 1 BEFORE and 2 AFTER; campaign emulation, 1 on each side; a loop of consecutive crashes (0.08 every 0.2 s for 380 s) to measure the backoff (Docker's growing wait between restarts); lifecycle (`start`, `stop`, `restart`, `docker stop`, SIGINT) on a copy of `servers.sh` with only the coap block and the name, network and IP swapped. The server-side alternative (in Fix) ran under the same conditions. The complete fuzz and the raw datagrams were run earlier, on 2026-11-13 and 2026-11-15, each case against a new server.
- Machine load (load average) from 3.9 to 7.8, with other tests in parallel: restart delay and downtime depend on it, so the conclusions use counts and the shape of the backoff (it doubles, caps, resets).
- A second reviewer recounted everything with their own extraction (`tshark` fields in TSV and their own analyzer that reads the CoAP code straight from the payload byte; events and logs read separately): the counts match (159 against 153 fuzz -> server frames in one run are 6 IP fragments of one large datagram). They also redid the `--rm`/`--restart` conflict and the lifecycle, and tested the restart without a fixed IP (see Caveats).
- Deviations: `--memory 1g`, probe on the whole time (the campaign also probes during the attack).
- Not tested: the campaign path, which generated the published dataset; the whole campaign; the `docker0` without a fixed IP; host reboot or daemon restart; the `docker/build-images.sh` path (it does `docker rm -f` of every container whose name matches `server` or `attack` on the host).
- From the owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): there is no new image; the start line was tested in a container; in the tree with the whole PR, `bash -n` on `servers.sh` and `docker/build-images.sh` and the `server.yaml` read by `run_full_campaign.py` without error.

**Fix.**
- Swaps `--rm` for `--restart on-failure` in the line that starts coap, in the 4 places where it appears in the repository (`servers.sh:113`, `docker/build-images.sh:65`, `docker/servers/coap-server/server.yaml:16`, `docker/servers/coap-server/README.md:22`). It changes no image, attack or `attack.yaml`; the other 8 servers stay as they are.
- Removing `--rm` is mandatory: Docker refuses the two together (`docker: conflicting options: cannot specify both --restart and --rm`, code 125; through the API, `can't create 'AutoRemove' container with restart policy`) [measured, Docker 29.6.2; read in docker/cli `cli/command/container/opts.go:715-716` and moby `daemon/container.go:258-259`].
- Why `on-failure`: the crash exits with code 1 [measured in all events]; `on-failure` only restarts an exit other than 0 and, without `MaximumRetryCount`, tries without limit (moby `daemon/internal/restartmanager/restartmanager.go:86-90`) [read in code]. `always` and `unless-stopped` would also restart an exit 0 and would bring the container back along with the daemon or the host, a bigger change than needed [read in code, not tested]. The repository already uses `--restart unless-stopped` for dozzle (`docker/build-images.sh:142`).
- Why also `docker/build-images.sh:65`: `servers.sh:112` only creates the container if `docker ps -a | grep -c` gives 0, so a container created by `setup.sh full` without the policy would stay without it. `server.yaml:16` and `README.md:22` repeat the command and change so as not to diverge.
- Why restart instead of hardening the server: it keeps the fuzz's declared effect (bringing the target down) and does not touch third-party code.
- Alternative measured, outside this commit: handle the exception per datagram in the server's receive loop, pin CoAPServer at `744cc22` and copy `server.py` over the clone (the `Dockerfile` only copies `requirements.txt`, `:5`, and runs the cloned package, `:9`, so fixing only `docker/servers/coap-server/server.py` would have no effect). Under the same conditions: 0 crashes (84 datagrams rejected, dropped and logged), probe ok in 405 of 405 samples during the fuzz, `coap-token-collision` right after with 406 of 406 responses; in the campaign emulation, 56/34 datagrams exchanged with the fuzz's second run and 812/812 with `coap-token-collision`. In exchange, the fuzz no longer brings the target down (the effect becomes a logged exception) and a valid GET with an elective option stays unanswered (the datagram is dropped). Answering 4.02 or 4.05 as the RFC asks was not tested, and neither was a restart loop in the `ENTRYPOINT`, which would keep the `--rm`.

**Before and after.** Complete fuzz and `coap-token-collision` right after, same server image [measured]:

| Measure | Before (`--rm`) | After, run 1 | After, run 2 | Server-side alternative (outside the PR) |
|---|---|---|---|---|
| server crashes (exit 1) | 1, and the container is deleted | 8 | 10 | 0 (84 logged drops) |
| restarts | 0 | 8 | 10 | 0 |
| probe ok during the fuzz | 72/1130 (6.4%), only before the crash | 105/565 (18.6%) | 143/783 (18.3%) | 405/405 (100%) |
| downtime per crash | until the end | ~6 to ~20 s | ~6 to ~58 s | 0 |
| fuzz PUT and POST on the wire | 0 | 69 | 65 | 72 |
| fuzz summary (tests / errors / suspected crashes) | 3 / 57 / 32 | 19 / 54 / 19 | 26 / 44 / 22 | 64 / 8 / 20 |
| responses to `coap-token-collision` | 0 of 406 | 406 of 406 | 307 of 406 (a 51 s backoff caught the start of it) | 406 of 406 |

Campaign emulation (10/20/10 s per run: fuzz run 1, fuzz run 2, 40 s without attack, `coap-token-collision`; server started once) [measured]:

| Measure | Before (`--rm`) | After | Alternative (outside the PR) |
|---|---|---|---|
| crashes / restarts | 1 / 0 (container deleted) | 8 / 8 (3 in run 1, 5 in run 2) | 0 / 0 (36 drops) |
| fuzz run 1 -> server / server -> fuzz run 1 datagrams | 19 / 6 | 41 / 14 | 42 / 28 |
| fuzz run 2 -> server / server -> fuzz run 2 | 0 / 0 | 52 / 20 | 56 / 34 |
| `coap-token-collision` -> server / server -> it | 0 / 0 | 812 / 812 | 812 / 812 |
| probe ok: fuzz 1, fuzz 2, no attack, `coap-token-collision` | 13/22, 0/11, 0/15, 0/10 | 16/30, 14/27, 80/80, 47/47 | 53/53, 54/54, 80/80, 46/46 |

The 812 on each side are 406 GET and 406 empty ACKs from the client; the server answers both. Between fuzz run 1 and fuzz run 2 the server stays up (40 of 40 probes ok) and the backoff resets: the first crash of run 2 came after 28 s up and came back in 1.9 s.

Docker's backoff, with 0.08 every 0.2 s for 380 s and, after 15 s without attack, one more (15 crashes, 15 restarts) [measured]: delay between `die` and `start`, in the 14 crashes of the flood, of 3.0 3.5 2.9 1.5 2.1 4.5 6.8 12.6 25.7 51.6 60.1 59.9 61.1 62.7 s. By the code (`restartmanager.go:12-14`, `:65-78`: starts at 100 ms, doubles with each crash of under 10 s of run time, cap of 1 min, resets at 10 s or more) it would be 0.1 0.2 0.4 ... 12.8 25.6 51.2 60 60 60 60; the small values vanish in the cost of cleaning up and starting the container (1.5 to 4.5 s with the machine loaded). After 32 s up, the 15th crash came back in 4.7 s (it reset).

**How to reproduce.** In the reproduction file, section COAP-01; uses P1, P2, P3, P10.

**Caveats.**
- The target is down for most of the fuzz: probe ok in 18.6% and 18.3% of the samples in the table's runs, in 16.7%, 32.5% and 12.6% in three repeats on 2026-11-17 (the last with the machine loaded, load ~10, and with an earlier form of the block) and in 7.8% in one on 2026-11-18 (load 1.26) [measured]; it is an approximation by the probe, not exact time. With crashes less than 10 s apart the backoff doubles up to ~60 s; with the next attack stuck to the end of the fuzz, a 51 s backoff caught the start of `coap-token-collision` (307 of 406). In the campaign there is a pause and runs without attack between attacks, which covers the 60 s cap [inferred from the order; measured with a run without attack].
- It does not fix valid CoAP: Observe, Block1, Block2, Size2, No-Response and Request-Tag still bring the server down; now it comes back.
- Without a fixed IP the server may come back with another IP: Docker 29.6.2 releases the IP during the backoff and, at each restart, gives the lowest free IP of the network. Measured by the second reviewer on a user-defined network: a container created during the backoff took the server's `.2` and the server came back on `.3`; in another test the server went down from `.3` to a free `.2`. On `docker0` the behavior is the same [inferred: same allocator]. Whoever aims at the container's IP (the server's `README.md:28` says to get it with `docker container inspect`) needs to reread it after the server comes back; during the backoff `inspect` returns an empty IP. The 307 of 406 above would be worse without a fixed IP [inferred]. The campaign path aims at `127.0.0.1` through the published port and does not depend on the container's IP [inferred, not tested].
- Without `--rm`, a stopped container is left over: after `docker stop` or SIGINT the container stays `Exited` and `./servers.sh start` does not recreate it (`servers.sh:112` also counts the stopped ones), leaving the server down; `./servers.sh restart` recovers and `./servers.sh stop` removes it, including during the backoff [measured]. After a host reboot or daemon restart it was not tested: by the code it depends on the exit code at shutdown (exit 0 stays `Exited` and `start` does not recreate; 137 the daemon restarts; moby `daemon/daemon.go:550` and `daemon/container/container.go:544-550`) [read in code].
- The consequence in the campaign was measured by emulation (README path, fixed IP, 2 fuzz runs, 1 run without attack and 1 `coap-token-collision` run), not in the whole campaign nor in the `--network host` path that generated the published dataset.
- Times depend on load (load average from 3.9 to 7.8): the process takes 0.3 to 17 s to exit after the fatal datagram (while it prints the traceback it does not read the socket) and this goes into the downtime [measured; cause inferred].
- The AFTER counts in the tables are from single runs and depend on the instant of each crash and each restart: a PUT or POST only reaches the wire while the server's container exists (during the backoff the IP disappears and the fuzz gets `Errno 113`). In three repeats on 2026-11-17 (two with load below 1; one with load ~10 and an earlier form of the block), the complete run gave 10, 17 and 15 crashes and 56, 59 and 73 PUT and POST on the wire, and the emulation gave 62, 32 and 6 datagrams from the server to fuzz run 2, against 20 in the table; the 812/812 with `coap-token-collision` and the BEFORE's 0 repeated in all [measured]. In a fourth repeat, on 2026-11-18 (load 1.26), 10 crashes, 43 PUT and POST and 62 datagrams to fuzz run 2, with the same 812 from the server to `coap-token-collision` and the same BEFORE 0 [measured].
- Hardening the START (`docker rm` of a stopped container before the `servers.sh:112` test) was not tested and is not in the commit.
- `Dockerfile:3` still clones CoAPServer without a pin; on 2026-11-16 master was still `744cc22`.

**Versions.** CoAPServer (`maksnowak/CoAPServer`) `744cc22`, from 2025-01-31, cloned without a pin; Python 3.11.18 (`python:3.11-alpine@sha256:7fbad8e4...`), aiocoap 0.4.17 and typer 0.29.1 on the server (no version in its `requirements.txt`); aiocoap 0.4.7 in the attacks (pinned); Docker 29.6.2 (daemon `3d80467`, CLI `dfc4efb`), Ubuntu with 8 CPUs.

### COAP-02 · coap-token-collision: The Chosen Token Never Reaches The Wire And Each Request Uses A New Socket, So There Is No Collision

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/coap-token-collision/coap-token-collision.py` |
| Depends on | none |

**Promise.**
- `docker/attackers/coap-token-collision/attack.yaml:5` (same in `README.md:3`): "Burst of CoAP messages that forces token reuse or collisions to degrade target state tracking and transaction correlation."
- `coap-token-collision.py:93-94`: "# Phase 1: Massive collision with token 0x01" and `collision_token = b'\x01'`; `:98-100`: "# Phase 2: Collision with empty token (0 bytes)" and `b''`; `:63` and `:66-67`: "Testing the full 1-byte token space (0x00-0xFF)..." with `bytes([token_value])`; `:48`: "The server will need to correlate {num_requests} responses to the same token!".

**What happens.** The Token is a field of 0 to 8 bytes that the CoAP client puts in the request to match the response (TKL is its length in the header); by RFC 7252 §5.3.1 it only needs to be unique among requests between the same pair of endpoints, so a Token collision only exists between requests that leave the same port for the same server [read in code]. In 3 runs, 406 GET each [measured]:
- 0 of 100 GET with Token `01` in phase 1, 0 of 50 with an empty Token in phase 2 and 0 of 256 with the requested Token in the phase 3 sweep;
- TKL 2 in 403 to 406 of the 406 (sometimes 1 or 3); 404, 405 and 406 distinct tokens; 404 to 406 source ports; at most 1 GET per (port, Token) pair;
- the server log confirms: 0 requests with `token=b'\x01'` and 0 with `token=b''`. The attack log prints `Token=01` 101 times, but that is the argument, not what went out on the wire.
- The sockets do not stay open forever: the attack never closes the `Context`, Python's garbage collector does (`aiocoap/util/asyncio/recvmsg.py:92-94`), and aiocoap logs `Connection loss was not expected.` for each one (`aiocoap/transports/udp6.py:525`); sampled every ~0.2 to 0.3 s, a peak of 162 to 250 sockets open at the same time.

**Cause.**
- `coap-token-collision.py:25` creates a `Context` (a new UDP socket) per request, `:30` assigns `request.token` and `:34` sends [read in code].
- aiocoap 0.4.7 (pinned in `requirements.txt:1`) [read in the image]: `aiocoap/tokenmanager.py:203-214` does `msg.token = self.next_token()` unconditionally (`:214`); the counter starts at a random 16-bit value (`:21`) and adds 1 stripping leading zeros (`:63-67`), hence TKL 2 almost always. `aiocoap/protocol.py:133-141` puts every client UDP transport behind a `TokenManager`, and `Context.request` reaches it (`:338-351`, `:349`, `:662`, `:664`).
- A second reviewer reproduced it without a network (container with `--network none`, over loopback): the requested Tokens `01`, empty and `7f` went out as `2478`, `6fd7` and `a04d`; and in a shared `Context` the Token `01` became `1f04`, `1f05`, `1f06`. Merely reusing the `Context` does not fix it [measured].

**How we tested.**
- Images: the attack built from upstream at `8613c66` (BEFORE) and with this commit (AFTER), `python:3.11-alpine@sha256:7fbad8e4...`, Python 3.11.18, aiocoap 0.4.7 from `requirements.txt`; the two images differ only in the last layer (the `.py`). Server: a `server-coap-server` image built earlier, on 2026-11-09, with CoAPServer at `744cc22` (checked inside the image; it is the same commit that the `8613c66` `Dockerfile` clones today), a new container for each run, with no arguments, as in `servers.sh:113`.
- Arguments as in the attack's README and in what `attackzoo.py run` builds: `<IP> 5683`, no `-e`, until it exits on its own (9 to 12 s).
- Own probe before and after each run (a hand-built CON GET `/sensors`; CON is the confirmable message, which asks for an ACK): 2.05 in all.
- 0 truncated frames in the capture. Counting with a pcap parser of our own in Python, cross-checked with `tshark` (`coap.type==0 && coap.code==1`, `coap.token==01`, `coap.token_len==0`, distinct source ports) and with the server log (`Handling request` lines with `token=...`). Attacker sockets sampled every ~0.2 to 0.3 s (`/proc/net/udp6` in its network namespace); control with `gc.disable()` in the same image: the sockets rise without dropping up to 400 and the warning goes away.
- 3 runs on each side, interleaved (before 1, after 1, before 2, ...). Load (load average) from 1.8 to 3.5, with other tests on the machine.
- Robustness outside the attackzoo flow: against a dead target (closed port, 40 s, stopped with SIGKILL) and against a test server that answers separately (empty ACK, then CON 2.05 with another MID; MID is the message identifier).
- A second reviewer recounted the 6 pcaps with their own parser, their own `tshark` filters and `grep` on the logs: same numbers (with two wording corrections already applied here: 454 B, not 456, of difference in the 1st run; `protocol.py:133-141`).
- Not tested: target by name (FQDN) or IPv6.

**Fix.** Only the `.py`: `build_get` builds the CON GET by hand (version and type, TKL, code 0.01, MID, Token, Uri-Path options) and `CoapEndpoint` sends all requests through a single UDP socket (`loop.create_datagram_endpoint(..., remote_addr=...)`). Since the Tokens collide on purpose, the response is matched by the MID; every CON received gets an empty ACK, as aiocoap does; a CON without a response is retransmitted with aiocoap's defaults (initial wait of 2 to 3 s, doubling, up to 5 sends). Staying the same: the three phases, counts, resources, pauses, messages, statistics, `main()` and the `attack.yaml` parameters. `requirements.txt` and `Dockerfile` stay as they are: aiocoap remains installed, unused (removing it would change the image and was left out of this commit).

Changes on the wire and in the log (declared): 1 source port instead of ~406, denser burst (the 100 GET of phase 1 go out in 7 to 12 ms); the log prints the raw code (`4.04`, instead of `4.04 Not Found`); an empty ACK of a separate response (log `0.00`) or an RST count as a response; for a target by name the Uri-Host option that aiocoap would add is not sent [read in code, not tested].

**Before and after.** 3 runs on each side, same server and same arguments [measured]:

| Measure | Before (`8613c66`) | After (this commit) |
|---|---|---|
| GET sent | 406 | 406 |
| phase 1: GET with Token `01` | 0 of 100 | 100 of 100 |
| phase 2: GET with empty Token | 0 of 50 | 50 of 50 |
| phase 3: GET with the requested Token | 0 of 256 | 256 of 256, from `00` to `ff` in order |
| TKL | 2 in 403 to 406; 1 or 3 in the rest | 1 in 356; 0 in 50 |
| source ports | 404 to 406 | 1 |
| maximum GET with the same (port, Token) | 1 | 101 |
| maximum GET open at the same time with the same (port, Token `01`) | 1 | 84 to 89 |
| UDP sockets open at the same time on the attacker (sampled) | peak of 162 to 250 | 1 |
| IP bytes attacker -> server | 32071 to 32073 | 31617 (454 B less in the 1st run: only the Token) |
| GET answered | 406 of 406 | 406 of 406 |
| server | alive, probe 2.05, 0 errors in the log | alive, probe 2.05, 0 errors in the log |

Robustness [measured]: against a dead target, 415 GET before and 466 after, both stuck in phase 1 retransmitting CON; against the separate-response server, 406 GET and 0 errors in both (only the fixed one's log prints `0.00`).

**How to reproduce.** In the reproduction file, section COAP-02; uses P1, P2, P3, P10.

**Caveats.**
- Against attackzoo's `coap-server` the collision has no victim, before or after: CoAPServer keeps no state per Token or per MID; it answers each datagram by copying type, MID and Token (`coap_server/construct_response.py:11-20`) [read in code; no effect observed in 6 runs: server alive, probe 2.05, 406 of 406 answered]. The commit makes the attack send on the wire what it promises; it does not make the target suffer the promised effect ("degrade target state tracking").
- It changes the profile on the wire: 1 source port instead of ~406 and a denser burst; rules or counts that look at source ports change.
- "No collision" in the BEFORE rests on the port measurement and on the reading of RFC 7252 §5.3.1.
- Times (7 to 12 ms in phase 1; 84 to 89 open) measured with other tests on the machine; they are descriptive.
- aiocoap stays in `requirements.txt` unused.
- Target by name or IPv6 and the campaign path were not tested.

**Versions.** aiocoap 0.4.7 (pinned in the attack's `requirements.txt`); Python 3.11.18 (`python:3.11-alpine@sha256:7fbad8e4...`); CoAPServer `744cc22`; Docker 29.6.2.

## Commits: Web (DVWA And Scanning)

### WEB-01 · web-wide-scanner: SpiderFoot Receives "IP PORT" As The Target, Treats It As A Person's Name And No Packet Reaches The Server

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/web-wide-scanner/entrypoint.sh`, `docker/attackers/web-wide-scanner/attack.yaml`, `docker/attackers/web-wide-scanner/README.md` |
| Depends on | none |

**Promise.**
- `docker/attackers/web-wide-scanner/attack.yaml:5`: "Broad scanner for known web vulnerabilities." (same in `README.md:3`).
- `attack.yaml:14`: "This attack can generate a large amount of data if captured until its automatic completion. For demonstrations, use less than 5 seconds of execution." (same in `README.md:27`).
- `attack.yaml:9-10`: `target_services: - http-server`. `attack.yaml:15-20`: MITRE TA0043, T1590, T1592, T1595 and T1595.002 (active scanning and vulnerability scanning).
- `attack.yaml:22-30`: `target_ip` ("Target IP address or FQDN") and `target_port` ("Target port", default 8080).
- `README.md:34`: `python3 attackzoo.py run web_wide_scanner --target <TARGET>`. `README.md:40`: `docker run --rm -d --name attack-web-wide-scanner attack-web-wide-scanner:latest "<TARGET_IP>" "8080"`.

**What happens.** [measured] Upstream image, path A arguments (the flow of `README.md:330-335` at the repository root: the server's internal IP and port 80), 180 s window with full network capture, on a network with no route to the internet and with the list of domain suffixes that SpiderFoot downloads at startup already in its cache (see How we tested):
- 0 frames between the scanner and the server; 0 lines in the Apache `access.log`.
- The scanner exits on its own (exit 0) about 90 s after starting. The scan ends with status FINISHED in 36 s, and SpiderFoot's own database only has two events: `ROOT` and `HUMAN_NAME` (type "person's name") with the value `<server IP> 80` (here and below, `<server IP>` is the server's IP on the test network). The stdout prints `SpiderFoot UI  Human Name  <server IP> 80`.
- The stderr warns "You didn't specify any modules, types or use case, so all modules will be enabled." and "Modules enabled (235)".
- The modules that receive the `HUMAN_NAME` only try third-party URLs: `ahmia.fi/search/?q=<server IP>+80`, `whois.arin.net/rest/pocs;first=<server IP>;last=80` (ARIN treats it as first name and last name), `onionsearchengine.com`, `search.wikileaks.org`, `darksearch.io` and a `.onion` address. No attempt at the target.
- With the yaml's default port (`8080`, the form of `README.md:40`) it gives the same: 0 frames, FINISHED in 30 s, `HUMAN_NAME` `<server IP> 8080`.
- [read in code] The published campaign is consistent with this: in `contrib/docs/campaign/web_wide_scanner.md:25-28`, the levels with attack (L1 to L3) stay the same as the level without attack (L0): PCAP from 1.67 to 1.66 MB, dataset from 3,160 to 3,136 lines. It is weak corroboration: it does not show the mechanism.

**Cause.**
- `entrypoint.sh:6`: `exec python3 /spiderfoot-4.0/sf.py -s "${TARGET} ${PORT}"`. Target and port become a single string, with a space.
- SpiderFoot v4.0 (the tarball that `Dockerfile:3` downloads) [read in code]:
  - `sf.py:297-298` quotes a target with a space; `sf.py:301` calls `targetTypeFromString`.
  - `spiderfoot/helpers.py:72-90`: the regexes are tested in order. The IP one (`:73`) does not match (quotes and the " PORT"); the one at `:77` (`^".+\s+.+"$`) returns `HUMAN_NAME`.
  - `sf.py:307` strips the quotes. `sf.py:310-315`: without `-m`, `-t` or `-u`, it turns on all modules.
  - `sfscan.py:383-387`: the first event goes out with the seed's type, `HUMAN_NAME`.
- Who consumes `HUMAN_NAME`: 8 of the 235 modules (`sfp_accounts`, `sfp_ahmia`, `sfp_arin`, `sfp_darksearch`, `sfp_onionsearchengine`, `sfp_socialprofiles`, `sfp_torch`, `sfp_wikileaks`), all searches on third-party services. The modules that touch the target (`sfp_portscan_tcp`, `sfp_sslcert`, `sfp_spider`) consume `IP_ADDRESS`, `NETBLOCK_OWNER`, `INTERNET_NAME` or `LINKED_URL_INTERNAL`, and none of the 8 produces those types [measured: the 235 modules instantiated inside the image, reading what each consumes and produces; holds for 1 hop].
- [measured] Every way of calling from attackzoo gives `HUMAN_NAME`: `<server IP> 80`, `<server IP> 8080`, `127.0.0.1 8080` (the campaign form), `172.17.0.2 80`, `example.com 8080`. Only the target alone becomes `IP_ADDRESS` (or `INTERNET_NAME`, if it is a name).

**How we tested.**
- Images: `web-wide-scanner` built on 2026-11-16 from the upstream tree at `8613c66` (base `python:3.11-alpine` resolved at `@sha256:7fbad8e4...`; the SpiderFoot tarball inside the image has the sha256 in Versions) and from the same tree with this commit. Layers 1 to 10 of the two images are identical; only the `entrypoint.sh` ones change. A third image, with only `-s "${TARGET}"`, for the variant. Server: upstream's `server-http-server:latest` image, with no arguments, as in `servers.sh:101`.
- Network: the scanner ran in the network namespace of a helper container with a blackhole route to the host (.1), for safety; the attack process gained no extra capability.
- Arguments: the path A form (`README.md:330-335` at the root: the server's internal IP and port 80, which `attackzoo.py run` passes as `docker run --rm -d --name attack-web-wide-scanner <image> <IP> 80`, `modules/runners.py:147`) and the form of `README.md:40` (port 8080). The `attack.yaml` declares no intensity parameters, so attackzoo does not pass `-e`. We pass `-e PYTHONUNBUFFERED=1`, only so as not to lose stdout on a SIGKILL; the second review repeated the BEFORE with no `-e`, with the same result.
- No internet. SpiderFoot 4.0 downloads the public suffix list (PSL) at startup (`sfscan.py:200-208`); without internet it dies and the scan stays in CREATED, with or without this commit. For the scan to get past startup, we mounted at `/root/.spiderfoot/cache` the cache file that SpiderFoot itself would write after the download (name `sha224("internet_tlds")`), with the PSL that already comes in the image (package `publicsuffixlist` 0.7.14). SpiderFoot reads this cache (validity of 72 h) instead of downloading.
- DNS: on a Docker network of its own, Docker's embedded DNS answers PTR with the container name; on docker0 that DNS does not exist [inferred]. The "no PTR" run mounted a `/etc/resolv.conf` with `nameserver 127.0.0.1` (a dead resolver) to imitate docker0.
- 180 s window; if the scanner did not exit on its own, `docker kill`. Of the 7 runs in the table, only the variant without `-m` needed it; the 2 without the PSL cache too.
- Capture: from before the attack to the end of the window plus 3 s.
- Counting: tshark with display filters (`ip.src==<scanner> && ip.dst==<target> && !icmp`, `tcp.flags.syn==1 && tcp.flags.ack==0`, `http.request`, `tls.handshake.type==1`); SpiderFoot's SQLite database (scan status, events, enabled modules, scan log); Apache's `access.log` and `error.log`.
- Runs: 1 per condition (the 7 in the table, plus 2 without the PSL cache, which only show the hang without internet). Host load: load from 2 to 3.5 in the first runs (other tests on the same host) and from 0.4 to 1.6 afterward. The times in the table are only illustrative.
- Second independent review: recounted all pcaps with their own tshark filters, read SpiderFoot's databases with their own queries, instantiated the 235 modules in the upstream image to list who consumes and produces each type, and repeated the BEFORE without `-e`, with the `README.md:40` arguments, plus a positive control: a `wget` from the scanner to the server at the end showed up in the capture and in the `access.log`, so the capture was alive and the zero is real.
- Owner's checklist: the commit changes the `attack.yaml` only in the port label (see Fix). In the PR's final tree, the `attack.yaml` passes `yaml.safe_load` and `python3 attackzoo.py list --json` brings the `web_wide_scanner`'s `target_port` with the new label (`kind` port, default 8080, not required); the Dockerfile copies only `requirements.txt` and `entrypoint.sh`, and the image rebuild with the new label, with cache, gave the same image ID as without the label [measured].
- Not tested: with internet (attackzoo's real flows have it); path B (the campaign, `contrib/scripts/run_full_campaign.py`, with `--network host` and target `127.0.0.1 8080`; that seed also gives `HUMAN_NAME`, measured); the cut by `max_runtime_s` (with the cache, the upstream scanner and this commit's exited on their own in every run).

**Fix.** `entrypoint.sh:6` becomes `exec python3 /spiderfoot-4.0/sf.py -s "${TARGET}" -m sfp_dnsresolve,sfp_portscan_tcp,sfp_sslcert,sfp_spider`.
- `-s "${TARGET}"`: the seed becomes `IP_ADDRESS` (or `INTERNET_NAME`, if the target is a name, as the yaml's label allows).
- `-m` with 4 modules is our choice, and it defines what the attack now does: `sfp_portscan_tcp` and `sfp_sslcert` touch the IP; `sfp_spider` does the HTTP crawl from a name; `sfp_dnsresolve` gives that name (PTR query, reverse DNS from IP to name) and the IP of a name.
- Alternative measured and not proposed: only `-s "${TARGET}"`, without `-m`. It turns on the 235 modules; without internet, the scan was still RUNNING at 180 s, with connect scan (full TCP connection, port by port) on 49 ports and 0 HTTP. With internet, it would send the target's IP to the 88 modules that consume `IP_ADDRESS` (VirusTotal, Shodan, AbuseIPDB and others) [the count was measured in the image; the sending is inferred].
- The port remains unused, and there is no way to use it through SpiderFoot 4.0's CLI, which has no port option: `-s` is only "Target for the scan" (`sf.py:99`); `sfp_portscan_tcp` uses the fixed list at `modules/sfp_portscan_tcp.py:36-41` (includes 80 and 8080); `sfp_sslcert` uses a fixed 443 (`modules/sfp_sslcert.py:97-99`) or a URL's port (`:88-92`); `sfp_spider` builds `http://` or `https://` plus the name (`modules/sfp_spider.py:37`, `:291-296`). The `target_port` parameter stays, because the runner passes 2 positional arguments and `entrypoint.sh:2` requires 2. The commit documents this in the port label: in `attack.yaml:27`, `label: Target port` becomes `label: Target port (ignored by the scan; sfp_portscan_tcp uses its default port list)`, and the same phrase goes into the description of the `--target_port` line of `README.md:23`. It is text only: the Dockerfile copies only `requirements.txt` and `entrypoint.sh` [read in code].

**Before and after.** [measured] Same setup, suffix list in SpiderFoot's cache, 180 s window; only the attack image changes. "Scanner -> target" excludes ICMP.

| run | frames | scanner -> target | SYN (distinct ports) | SYN-ACK from target | RST from target | HTTP | lines in access.log | scan |
|---|---|---|---|---|---|---|---|---|
| upstream, port 80 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | FINISHED in 36 s, only ROOT and HUMAN_NAME |
| upstream, port 8080 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | FINISHED in 30 s, only ROOT and HUMAN_NAME |
| with the commit, port 80, IP with PTR | 131 | 67 | 53 (49) | 3 (port 80) | 50 | 3 | 3 | FINISHED in 20 s |
| with the commit, port 8080, IP with PTR | 131 | 67 | 53 (49) | 3 (port 80) | 50 | 3 | 3 | FINISHED in 20 s |
| with the commit, port 80, IP without PTR | 108 | 53 | 50 (49) | 1 (port 80) | 49 | 0 | 0 | FINISHED in 25 s |
| with the commit, target by name (FQDN) | 30 | 14 | 3 (2: 80 and 443) | 2 (port 80) | 1 | 3 | 3 | FINISHED in 3.6 s |
| `-s`-only variant (235 modules, not proposed) | 114 | 53 | 50 (49) | 1 (port 80) | 49 | 0 | 0 | RUNNING at 180 s |

- The 49 ports with SYN are exactly the default list of `sfp_portscan_tcp.py:36-41`, and the set is the same with port 80 and with 8080.
- The 3 HTTP are `GET /` (302), `GET /login.php` (200) and `HEAD /`, from `sfp_spider`, from the name that the Docker network's DNS returned by PTR.
- Port 443 only receives SYN (`sfp_sslcert` tries TLS) and answers RST, because DVWA does not listen on 443; 0 ClientHello.

**How to reproduce.** In the reproduction file, section WEB-01; uses P1, P2, P3, P8.

**Caveats.**
- Partial fix. The scanner now touches the target, but in the run closest to path A (IP without PTR, as on docker0) the `http-server` receives 0 HTTP requests: only connect scan on 49 ports and SYN on 443. The attack does not become the "web vulnerability scanner" of `attack.yaml:5`; the 3 HTTP only appear when the IP has a reverse name or the target is a name. On a site with more pages the spider would fetch up to 100 (`sfp_spider.py:34`) [read in code].
- The `-m` list is our choice and defines what the attack becomes. With all modules and with internet, the behavior was not tested.
- Everything was measured without internet, with the PSL in the cache. The upstream's zero in the real flow rests on the seed's type (measured for every way of calling), on reading the code and on the published campaign (consistent, but weak as proof).
- "None of the 8 consumers of `HUMAN_NAME` produces the types that touch the target" holds for 1 hop; longer chains, with internet, were not tested.
- With a private-name target there is no port scan: `sfp_dnsresolve` marks the target's own IP as `INTERNAL_IP_ADDRESS` (`modules/sfp_dnsresolve.py:461-463`), a type that `sfp_portscan_tcp` does not consume (`modules/sfp_portscan_tcp.py:97-98`); what remains is the spider on 80 and sslcert on 443.
- The port remains ignored (see Fix).
- We did not measure whether the effect fits in `max_runtime_s: 10` (`attack.yaml:8`) or in the "less than 5 seconds" of `attack.yaml:14`: the time to the first packet varied with the host's load.
- Note, outside the defect: SpiderFoot 4.0 needs internet at startup to download the PSL; without it the scan stays in CREATED with 0 packets, with or without this commit. In attackzoo's flows there is internet; on an isolated network, the preloaded cache above solves it.

**Versions.** SpiderFoot v4.0 (`https://github.com/smicallef/spiderfoot/archive/v4.0.tar.gz`, sha256 `8b5dac6b846ae854f85243839e3a16c7412cdfbb87b2c3689829a5e40d3ccf4e`; `Dockerfile:3` does not check a checksum); `python:3.11-alpine` at `@sha256:7fbad8e4...` on 2026-11-16 (Python 3.11.18); `publicsuffixlist` 0.7.14 and PyYAML 5.3.1 in the image; server `vulnerables/web-dvwa` (pinned in `Dockerfile:1` by the sha256 digest `dae203fe11646a86937bf04db0079adef295f426da68a92b40e3b181f337daa7`; DVWA 1.10, Apache 2.4.25); Docker 29.6.2.

### WEB-02 · http-server (DVWA): The Server Comes Up With The DVWA Database Empty, And Every Correct Login Is Sent To `setup.php`

| | |
|---|---|
| Class | (b) inconsistency between parts of attackzoo |
| In this PR | commit |
| Files | `docker/servers/http-server/Dockerfile`, `docker/servers/http-server/init-db.php` (new) |
| Depends on | none |

**Promise.**
- `docker/servers/http-server/server.yaml:16`: "Provide a vulnerable web application for web attacks, scanners, enumeration, and controlled HTTP DoS." (same in `README.md:3`). `server.yaml:7`: "HTTP with Damn Vulnerable Web Application (DVWA)". DVWA is a PHP application built to be vulnerable, with one flaw per module.
- `server.yaml:21-32` (`related_attacks`): the 11 attacks that target this server, among them `web_sql_injection` (`:22`), `php_lfi_enumeration` (`:26`), `web_post_bruteforce` (`:27`) and `web_xss_scanner` (`:30`). The flaws that these attacks promise to exploit are in the DVWA modules that require login (see WEB-03 to WEB-06).

**What happens.** [measured]
- The image comes up with the `dvwa` database with no tables at all: `/var/lib/mysql/dvwa` only has `db.opt`, and `SHOW TABLES` on the `dvwa` database comes back empty at the start and at the end of every execution.
- A login with a complete form and the correct credential (`admin`/`password`, with a valid anti-CSRF token; the anti-CSRF token is the value DVWA puts in the form and checks on the POST) is sent to `setup.php` without the password being checked: 1 POST, 302 response to `setup.php`. In MariaDB's general log (the record of every query the database receives): 1 query to `information_schema`, 0 credential queries.
- With the fixed `web-post-bruteforce` (WEB-04): 1,000 POST, 1,000 302 responses to `setup.php`, 0 credential queries.
- On its own, the empty database changes no upstream attack: none of them logs in (all hit URLs without a session), and each gave the same counts with the empty database and with the created database (regression table below). The failure appears when an attack tries to reach an authenticated module. That is why this commit is a prerequisite for the fixes WEB-03 to WEB-06.

**Cause.** DVWA files cited as they are in `/var/www/html` inside the `vulnerables/web-dvwa` image that `Dockerfile:1` pins by digest [read in code].
- `login.php:23-31`: if `information_schema` does not have the `users` table in the `dvwa` database, the login redirects to `setup.php` before checking the credential (the credential query is the one at `:33`).
- The table is only created by the "Create / Reset Database" button of `setup.php` (`setup.php:12-17`, which includes `dvwa/includes/DBMS/MySQL.php:41-80`).
- Nobody presses the button. The base image's entrypoint (`/main.sh:1-15`) only does `chown`, `service mysql start`, `service apache2 start` and `tail`. In attackzoo, `servers/http-server/Dockerfile:1-2` is only `FROM` and `EXPOSE`, and `servers.sh:100-101` and `docker/build-images.sh:15-16` and `:52-53` start the container with nothing more. A search of the whole repository (outside the wordlists) for `setup.php`, `create_db`, `user_token` and `PHPSESSID`: nothing.
- Every vulnerable DVWA module starts with `dvwaPageStartup( array( 'authenticated', ... ) )`, which sends anyone not logged in to `login.php` (`dvwa/includes/dvwaPage.inc.php:61-65`).

**How we tested.**
- Server images: build of `servers/http-server` from the upstream tree at `8613c66` (same image ID as the `server-http-server:latest` that `build-images.sh` generates, `sha256:e55f9e7c8b2b...`) and from the same tree with this commit (`sha256:cf488b4f9b3d...`). In the fixed build's log, MariaDB and Apache come up and `php` exits with 0. The fixed image has `users` and `guestbook`, has the `config.inc.php.bak` and does not have the `init-db.php`.
- Server with no arguments (as in `servers.sh:101`). "Ready" when `mysqladmin ping` answers and the Apache pid exists (checked with `docker exec`, no network traffic). MariaDB's general log on in both servers, to count credential queries (`SELECT * FROM users WHERE user=...`) and `information_schema` checks; database tables printed at the start and at the end.
- Upstream attacks built from the `8613c66` tree and run in the path A form (`README.md:330-335` at the root: the server's internal IP and port 80, no `-e`; only the two `dos-*` take the `-e` that path A passes). Those that exit on their own run until they exit; those that do not (slowloris 60 s, gobuster 5 s and 60 s, SpiderFoot 300 s) had the same window on both servers and then `docker kill`. In the regression batch, server with `--memory 1536m` and attack with `--memory 1g` (no OOM).
- Capture: from 2 s before to 2 s after the attack. The 60 s gobuster pair hit our ceiling of 2 million frames per capture: the counts for that pair come from the `access.log` and the general log, which are complete; the 5 s pair has the whole capture.
- Counting: tshark (`http.request.method`, `http.request.uri`, `http.response.code`, `http.location`, `http.file_data contains "root:x:0:0"` or `"name='user_token'"`); Apache's `access.log` and `error.log`; general log. `.bak` check: GET on `/config/` and on the 3 configuration files from the attacker's IP, recording status, size, variable names and the md5 of the password line, never the value.
- Executions: 8 for login, LFI and brute force (2 × 2 matrix per attack); 26 attack runs for the regression (one pair per attack for 10 of the 12 in the regression table, because `php-lfi-enumeration` and `web-post-bruteforce` are in the matrix, plus the pairs for the 5 s gobuster and for the `sql-injection` and `idor-url-parameter` fixes); 2 for the `.bak` check.
- Load: load from 2.6 to 5.5 in the first batch (floods from other tests on the same host) and from 0.6 to 13.8 in the regression batch.
- Second independent review: recounted the pcaps with their own filters and with `tshark --export-objects http` (a method independent of `http.file_data`); redid the brute force BEFORE from scratch; sent 7 isolated requests to measure each cause of WEB-04; recounted all the regression pcaps and logs with their own parsers (in `idor-path-traversal` and `idor-url-parameter`, the multiset of URIs is the same on both servers); checked, without printing, that the `.bak` is equal to the `config.inc.php` in use.
- Deviations from the attackzoo flow: general log on, `web-https-heartbleed` on port 80 (DVWA does not serve 443).
- Not tested: path B (the campaign, `contrib/scripts/run_full_campaign.py`, with `--network host`, target `127.0.0.1:8080` and the docker-proxy, the process that publishes the container's port on the host, in the middle); the generic TCP and UDP floods, whose `target_services` is `target` and which in path B also hit DVWA (this commit does not touch layer 4 [read in code]); gobuster with the whole list; `web-wide-scanner` with internet; deleting the `.bak`; truncating the logs.

**Fix.**
- `servers/http-server/Dockerfile` copies `init-db.php` and, in a single `RUN`: fixes the owner of the MariaDB directories, starts MariaDB and Apache, runs `php /tmp/init-db.php`, stops both services and deletes the script.
- `init-db.php` (new) does the same request flow as the button: GET on `setup.php`, extracts `user_token` and `PHPSESSID`, POST of `create_db` with the token. Then it checks that the `admin` user exists and exits with 1 if it does not, which fails the build.
- Why this way: it uses DVWA's own setup (same tables and users as the button; the `admin`/`password` user comes from `MySQL.php:53`), and does it at build time, so no start line changes: `servers.sh`, `build-images.sh`, the `startup` of `server.yaml`, the ports and `/main.sh` stay the same.
- Side effects, declared:
  - `config/config.inc.php.bak`. DVWA's setup creates this file on purpose: `MySQL.php:85-93`, "// Copy .bak for a fun directory listing vuln". With this commit the server starts serving `/config/config.inc.php.bak` (200, 1,859 B, `application/x-trash`, delivered raw because Apache only passes names such as `.php` to PHP); upstream it is 404. The file has the same variables as the `config.inc.php` in use, including the database password (compared without printing the value). That password is the public default of the `vulnerables/web-dvwa` image and already appears literally in `init-db.php`; the `config.inc.php.dist`, with another password, is already served by upstream (200, 1,864 B). The image's MariaDB listens only on 127.0.0.1 (read in the image's configuration), so the password would not work from outside the container [inferred, not tested]. No attackzoo attack requests the file (0 requests for the `.bak` in 26 attack runs); `web-simple-scanner` (nikto) requests `/config/` and sees the listing with the `.bak`; `web-dir-enumeration` (gobuster) sees `/config` (301) and does not descend. We did not delete the `.bak`: it is a flaw that DVWA itself creates on purpose, and the server is vulnerable by design (`server.yaml:16`). Deleting it in the same `RUN` was not tested.
  - The image carries the build's lines in the `access.log` and the `error.log` (requests from 127.0.0.1 to `setup.php`, a Notice from `MySQL.php:9`, Apache's SIGTERM). Cosmetic; truncating the logs in the same `RUN` was not tested.
  - It changes the server for the 11 attacks of `related_attacks` and for `web-https-heartbleed`, which in `8613c66` also has `http-server` in `target_services` (the campaign sends it to `ssl-heartbleed`; the GEN-03 commit changes that `target_services` to `ssl-heartbleed`). The regression is below.

**Before and after.** [measured] Effect on the server (the fixed attacks are those of WEB-03 and WEB-04):

| measure | upstream server | server with this commit |
|---|---|---|
| tables in the `dvwa` database | none | `guestbook`, `users` |
| complete, correct login (`admin`/`password`) | 302 `setup.php`; 0 credential queries | 302 `index.php`; 1 credential query |
| `web-post-bruteforce` with WEB-04 (1,000 passwords) | 1,000 × 302 `setup.php`; 0 credential queries | 999 × 302 `login.php` and 1 × 302 `index.php`; 1,000 credential queries |
| `php-lfi-enumeration` with WEB-03 | 11,580 × 302 `../../login.php`; `root:x:0:0` in 0 responses | 11,580 × 200; `root:x:0:0` in 42 responses |
| `GET /config/config.inc.php.bak` | 404 | 200, 1,859 B |

Regression: the 12 upstream attacks that have `http-server` in `target_services`, each against both servers [measured]:

| upstream attack | upstream server | server with this commit |
|---|---|---|
| `dos-http-simple` | 200 GET, 200 × 404 | same |
| `dos-http-slowloris` (60 s window) | 250 SYN; 150 × 408 and 100 × 400 | same |
| `idor-path-traversal` | 570 GET: 374 × 404, 195 × 400, 1 × 302; 0 files read | same |
| `idor-url-parameter` | 5,965 GET: 5,920 × 200 (login form) and 45 × 400 | same |
| `php-lfi-enumeration` | 11,580 GET, 11,580 × 200 (login form); 0 files read | same |
| `sql-injection` | 6,718 GET; 0 queries beyond `USE dvwa` | same |
| `web-dir-enumeration` (gobuster, 5 and 60 s windows) | 15 and 19 findings | the same 15 and 19 (the total GET depends on how far it gets in the window: 184,021 and 170,971 in 5 s) |
| `web-https-heartbleed` (on port 80) | 200 ClientHello, 200 × 400 | same |
| `web-post-bruteforce` | 1,000 POST on `/`, 1,000 × 302 `login.php`; 0 credential queries | same |
| `web-simple-scanner` (nikto) | 22,020 requests: 21,462 × 404, 294 × 400, 243 × 302, 19 × 200 | same; only the body of `GET /config/` goes from 1,407 to 1,624 B (the listing shows the `.bak`) |
| `web-wide-scanner` | 0 packets (test without internet) | same |
| `xss-scanner` | 192 requests, 185 × 200; "XSS found 0" | same |

**How to reproduce.** In the reproduction file, section WEB-02; uses P1, P2, P8.

**Caveats.**
- On its own, this commit does not change what any upstream attack reaches (measured in the 12); it is a prerequisite for WEB-03 to WEB-06.
- The attack fixes use the fixed credential `admin`/`password`, the one DVWA's setup creates (`MySQL.php:53`). If the password is changed on the server, they stop at the login.
- The server now exposes `/config/config.inc.php.bak` (see Fix) and carries the build's log lines.
- The regression covers only path A, on an `--internal` network; heartbleed ran on port 80; `web-wide-scanner` stayed inert in the test (without internet, 0 packets on both servers); gobuster ran in 5 and 60 s windows, not the whole list; the layer 4 floods were left out.

**Versions.** `vulnerables/web-dvwa` (pinned in `Dockerfile:1` by the sha256 digest `dae203fe11646a86937bf04db0079adef295f426da68a92b40e3b181f337daa7`; DVWA "1.10 *Development*", `dvwa/includes/dvwaPage.inc.php:42`; Apache 2.4.25, Debian package 2.4.25-3+deb9u5; MariaDB); Docker 29.6.2.

### WEB-03 · php-lfi-enumeration: Enumerates `?page=` On `login.php`, Which Does Not Read `page`, And No File Is Included

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/php-lfi-enumeration/entrypoint.sh`, `docker/attackers/php-lfi-enumeration/lfi.py` |
| Depends on | WEB-02 (effect): without the DVWA database created, the login goes to `setup.php` and no file is read (measured) |

**Promise.**
- `docker/attackers/php-lfi-enumeration/attack.yaml:5`: "Controlled enumeration of Local File Inclusion (LFI) vectors in a vulnerable PHP application." (same in `README.md:3`). LFI, local file inclusion, is when the PHP application includes a file whose path comes from the client.
- `attack.yaml:9-10`: `target_services: - http-server`; `docker/servers/http-server/server.yaml:26` lists `php_lfi_enumeration`. `attack.yaml:21`: MITRE T1005 (Data from Local System).

**What happens.** [measured] Upstream attack against the `http-server` (DVWA), on path A (the flow of `README.md:330-335` at the repository root: `attackzoo.py run` with the server's internal IP and port 80, which becomes `docker run --rm -d --name attack-<folder> <image> <IP> 80` on docker0, `modules/runners.py:147`):
- 11,580 `GET /login.php?page=<path>`, 11,580 200 responses, all the login page (with the `user_token` field, title "Login :: Damn Vulnerable Web Application (DVWA) v1.10 *Development*").
- `root:x:0:0` (the start of `/etc/passwd`) in 0 responses; "Linux version" (from `/proc/version`) in 0. In the `access.log`: 11,580 `GET /login.php` with 200.
- The same against the server with the database created (WEB-02): the wrong endpoint does not depend on the database.

**Cause.**
- `entrypoint.sh:6`: `exec python3 lfi.py "http://${TARGET}:${PORT}/login.php?page=" --wordlist /tmp/LFISuite-pathtotest.txt`.
- In DVWA (files in `/var/www/html` of the server image) [read in code]: `login.php` does not read `page`; it only reads `Login`, `user_token`, `username` and `password` (`login.php:10-20`). In all of DVWA, only `vulnerabilities/fi/source/{low,medium,high,impossible}.php:4` read `$_GET[ 'page' ]`, and what includes is `vulnerabilities/fi/index.php:35-36` (`include( $file )`).
- `vulnerabilities/fi/index.php:6` requires a session (`dvwaPageStartup( array( 'authenticated', 'phpids' ) )`); without login, `dvwa/includes/dvwaPage.inc.php:61-65` redirects to `login.php`.
- `lfi.py` has no way to send a session cookie: the headers are fixed, `{'User-Agent': '--'}` (`lfi.py:31-33`), and `--cookie-mode` (`lfi.py:400-410`) puts the payload in the cookie, it does not keep a session.

**How we tested.**
- Images: `php-lfi-enumeration` built on 2026-11-16 from the upstream tree at `8613c66` and from the same tree with this commit (Python 3.11.18, `beautifulsoup4` 4.15.0 and `requests` 2.34.2, which `requirements.txt` does not pin). Servers: the upstream one and the one with WEB-02 (same images described there).
- Server with no arguments; "ready" when `mysqladmin ping` answers and the Apache pid exists; MariaDB's general log (the record of every query the database receives) on.
- Path A arguments (`README.md:330-335` at the root): `<image> <server IP> 80`, no `-e` (the `attack.yaml` declares no environment variables). Each execution exited on its own (exit 0) within the 400 s window.
- Capture: from 2 s before to 2 s after; about 115,800 frames per execution.
- Counting: tshark (requests by method and path; responses by code and `Location`; `http.file_data contains "root:x:0:0"`, `"Linux version"`, `"name='user_token'"`), `access.log`, `error.log` and general log.
- 4 executions (the matrix). Load: load from 2.6 to 5.5 (other tests on the host).
- Second independent review: recounted with their own filters and with `tshark --export-objects http` (in the BEFORE, 11,543 exported objects, all with the login form, 0 with `root:x:0:0`); tied each hit to its URI (25 distinct); checked the cited DVWA lines inside the image.
- Deviations: general log on.
- Not tested: path B (the campaign, `contrib/scripts/run_full_campaign.py`, with `--network host` and target `127.0.0.1:8080`; the endpoint is fixed in the entrypoint, so the same result is expected [inferred]); behavior against a target that is not DVWA.

**Fix.**
- `entrypoint.sh` logs in first: GET on `login.php`, extracts `user_token`, POST of `admin`/`password`/`Login`/`user_token` without following the redirect (with the `requests` that the image already has), and exports the cookies in `LFI_COOKIE`: `PHPSESSID` and `security=low`, which DVWA sets on the first request (`dvwaPage.inc.php:25-28`, `config/config.inc.php:35`). The URL becomes `/vulnerabilities/fi/?page=`.
- `lfi.py`: `import os` and 2 lines; if `LFI_COOKIE` exists, it goes in the `Cookie` header.
- Wordlist, engine, `page` parameter, arguments and `attack.yaml` stay the same.
- Fixed credential `admin`/`password`: it is the user that DVWA's own setup creates (`dvwa/includes/DBMS/MySQL.php:53`). Declared choice.
- Behavior change [read in code, not measured for this attack]: with the `set -e` already in `entrypoint.sh:5`, an error in the login step (target down, or a page without the `user_token` field, as on a target that is not DVWA) ends the attack before `lfi.py`; before, `lfi.py` ran against any target. The `sql-injection` fix (WEB-05) has the same pattern, and there the target-down case was measured. A login that DVWA refuses (changed password) gives no error: `lfi.py` runs without a session and only gets 302, as on the server without a database (Before and after, measured).

**Before and after.** [measured] 2 × 2 matrix, same setup; only the images change:

| attack \ server | upstream server (empty database) | server with WEB-02 |
|---|---|---|
| upstream | 11,580 GET `/login.php?page=...`, 11,580 × 200 (login page); `root:x:0:0` in 0 | same |
| with this commit | login POST, 302 `setup.php`; 11,580 GET `/vulnerabilities/fi/?page=...`, 11,580 × 302 `../../login.php`; `root:x:0:0` in 0 | login POST, 302 `index.php`; 11,580 GET `/vulnerabilities/fi/?page=...` with the session, 11,580 × 200; `root:x:0:0` in 42 responses (25 distinct URIs, for example `?page=../../../../../../../../../../../../../../../etc/passwd`); "Linux version" in 2 (`?page=/proc/version`); `error.log` with 11,327 "Failed opening" (the server tried to include each path) |

**How to reproduce.** In the reproduction file, section WEB-03; uses P1, P2, P3, P8.

**Caveats.**
- It only has an effect with WEB-02: without it the login goes to `setup.php` and no file is read (measured).
- The `admin`/`password` credential stays fixed in the attack.
- `lfi.py`'s output does not separate a hit from an error: without `--exclude`, every 200 response with a body becomes a "finding" (11,579 `> http...` lines before and after), and the 42 real hits do not stand out. The effect is seen on the server or in the capture.
- Timing, only illustrative: `max_runtime_s: 10` (`attack.yaml:8`, used by the web interface's watchdog, `modules/attackzoo_st.py:163-188`); the fixed attack sent requests from +1.5 s to +30.8 s of the capture; 41 of the 42 hits came out in the first 10 s after the first SYN, the first at +0.74 s (load of about 3.6).

**Versions.** `python:3.11-alpine` (Python 3.11.18 in the 2026-11-16 build); `beautifulsoup4` 4.15.0 and `requests` 2.34.2 (no version in `requirements.txt`); server `vulnerables/web-dvwa` (pinned in `Dockerfile:1` by the sha256 digest `dae203fe11646a86937bf04db0079adef295f426da68a92b40e3b181f337daa7`; DVWA 1.10, Apache 2.4.25); Docker 29.6.2.

### WEB-04 · web-post-bruteforce: POSTs To `/` With No Form, Session Or Token, And No Password Is Evaluated

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/web-post-bruteforce/entrypoint.sh` |
| Depends on | WEB-02 (effect): without the DVWA database created, every login goes to `setup.php` and no password is evaluated (measured) |

**Promise.**
- `docker/attackers/web-post-bruteforce/attack.yaml:5`: "Web application POST authentication brute force using a wordlist." (same in `README.md:3`).
- `attack.yaml:9-10`: `target_services: - http-server`; `docker/servers/http-server/server.yaml:27` lists `web_post_bruteforce`. `attack.yaml:16-18`: MITRE TA0006, T1110 and T1110.001 (password guessing).

**What happens.** [measured] Upstream attack against the `http-server` (DVWA), on path A (the flow of `README.md:330-335` at the repository root: `attackzoo.py run` with the server's internal IP and port 80, which becomes `docker run --rm -d --name attack-<folder> <image> <IP> 80` on docker0, `modules/runners.py:147`):
- 1,000 `POST /` (the `index.php`), with no `Content-Type` and no cookie. Body of the first: `username=admin\&password=qwerty` (the backslash goes literally).
- 1,000 302 responses with `Location: login.php`; in the `access.log`, 1,000 `POST / 302`; ffuf prints `Status: 302, Size: 0` 1,000 times.
- MariaDB's general log (the record of every query the database receives): 0 credential queries and 0 checks of the `users` table. No password is evaluated.
- The same against the server with the database created (WEB-02).

**Cause.**
- `entrypoint.sh:5`: `/tmp/ffuf -w /tmp/Pwdb_top-1000.txt -X POST -d "username=admin\&password=FUZZ" -u http://"${TARGET}:${PORT}" -fc 401`.
- In DVWA (files in `/var/www/html` of the server image) [read in code]: the URL `/` is `index.php`, which starts with `dvwaPageStartup( array( 'authenticated', 'phpids' ) )` (`index.php:6`) and redirects to `login.php` (`dvwa/includes/dvwaPage.inc.php:61-65`) without reading the body.
- Even on `login.php` the POST would be ignored: the `Login` field is missing (`login.php:10`); the anti-CSRF token `user_token` (the value DVWA puts in the form and checks on the POST) equal to the session's is missing, and the session cookie `PHPSESSID` itself is missing (`login.php:12`); and `Content-Type: application/x-www-form-urlencoded` is missing, without which PHP does not fill `$_POST`.
- [measured] Each cause isolated, with 1 request at a time against the server with a database, counting credential queries in the general log: no cookie, 302 `login.php` and 0; no `Content-Type`, 200 with the form and 0; no `Login`, 200 with the form and 0; wrong token, 302 `login.php` and 0; POST to `/` with everything else right, 302 `login.php` and 0; complete, 302 `index.php` and 1. The literal `\&` is harmless against DVWA: with it and the rest complete, 302 `index.php` and 1 query with `user='admin'` (the `stripslashes` of `login.php:15` removes the backslash).

**How we tested.**
- Images: `web-post-bruteforce` built on 2026-11-16 from the upstream tree at `8613c66` and from the same tree with this commit (ffuf 2.1.0, downloaded with a checksum by the `Dockerfile`). Servers: the upstream one and the one with WEB-02.
- Server with no arguments; "ready" when `mysqladmin ping` answers and the Apache pid exists; general log on to count credential queries (`SELECT * FROM users WHERE user=...`) and `information_schema` checks.
- Path A arguments (`README.md:330-335` at the root): `<image> <server IP> 80`, no `-e`. Each execution exited on its own (exit 0) within the 120 s window.
- Capture: from 2 s before to 2 s after; about 2,400 frames per execution.
- Counting: tshark (method, URI, `http.content_type`, `http.cookie`, `urlencoded-form.value`; responses by code and `Location`), `access.log`, general log (credential queries and distinct md5).
- 4 executions (the matrix). Load: load from 2.6 to 5.5.
- Second independent review: recounted the pcaps and decoded the POST bodies with their own tools; redid the BEFORE from scratch (2,378 frames, 1,000 `POST /` with no `Content-Type` or cookie, 1,000 × 302 `login.php`, 0 credential queries); sent the 7 isolated requests described in Cause, with their own capture.
- Deviations: general log on.
- Not tested: path B (the campaign, `contrib/scripts/run_full_campaign.py`, with `--network host` and target `127.0.0.1:8080`; inferred to be the same, because the URL path is fixed in the entrypoint).

**Fix.**
- `entrypoint.sh` does 1 GET on `login.php` with `curl` (already installed, `Dockerfile:5`) to get `PHPSESSID`, `security` and `user_token`, and runs the same ffuf with `-H "Content-Type: application/x-www-form-urlencoded" -b "<cookies>" -d "username=admin&password=FUZZ&Login=Login&user_token=<token>" -u http://<target>:<port>/login.php -fc 401`.
- Wordlist, user, threads, filter, arguments and `attack.yaml` stay the same.
- One token serves all 1,000 attempts: DVWA only generates a new token when it renders `login.php` (`login.php:53`), and every login POST leaves earlier through `dvwaRedirect` (`:30`, `:38`, `:43`) [read in code]. [measured] The 1,000 POST carried the same `user_token` and the same `PHPSESSID`, and the 1,000 passwords were checked.

**Before and after.** [measured] 2 × 2 matrix, same setup; only the images change:

| attack \ server | upstream server (empty database) | server with WEB-02 |
|---|---|---|
| upstream | 1,000 POST on `/` (no `Content-Type`, no cookie), 1,000 × 302 `login.php`; 0 credential queries | same |
| with this commit | 1 GET and 1,000 POST on `/login.php` (urlencoded, with `PHPSESSID`), 1,000 × 302 `setup.php`; 1,000 checks of the `users` table and 0 credential queries | 1 GET and 1,000 POST on `/login.php`, 999 × 302 `login.php` and 1 × 302 `index.php`; 1,000 credential queries (1,000 distinct passwords); the password `password`, line 3 of the wordlist, is accepted |

**How to reproduce.** In the reproduction file, section WEB-04; uses P1, P2, P3, P8.

**Caveats.**
- It only has an effect with WEB-02 (measured: without it, 1,000 × 302 `setup.php`).
- The `admin` credential stays as in upstream; the right password is only found because it is in the wordlist.
- ffuf's output does not distinguish the hit: `-fc 401` filters nothing on DVWA, which never answers 401, and ffuf shows `Status: 302, Size: 0` 1,000 times, including the accepted password. The hit is seen on the server (general log) or in the capture (the 302 to `index.php`).

**Versions.** ffuf 2.1.0 (pinned with sha256 in the `Dockerfile`); `ubuntu:24.04` resolved at `@sha256:73b99939...` on 2026-11-16; server `vulnerables/web-dvwa` (pinned in `Dockerfile:1` by the sha256 digest `dae203fe11646a86937bf04db0079adef295f426da68a92b40e3b181f337daa7`; DVWA 1.10, Apache 2.4.25); Docker 29.6.2.

### WEB-05 · sql-injection: Runs sqlmap On `/` Without A Session And Never Reaches The Injectable Parameter Of DVWA

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/sql-injection/entrypoint.sh` |
| Depends on | WEB-02 (effect): without the DVWA database created, the login goes to `setup.php` and sqlmap does not find the injectable point (measured) |

**Promise.**
- `docker/attackers/sql-injection/attack.yaml:5`: "SQL injection exploitation tests." (same in `README.md:3`). SQL injection is when a value coming from the client enters a database query without sanitizing.
- `attack.yaml:9-10`: `target_services: - http-server`; `docker/servers/http-server/server.yaml:22` lists `web_sql_injection`; `server.yaml:16`: "Provide a vulnerable web application for web attacks, ...". `attack.yaml:19`: MITRE T1190 (Exploit Public-Facing Application).

**What happens.** [measured] Upstream attack against the `http-server` (DVWA), on path A (the flow of `README.md:330-335` at the repository root: `attackzoo.py run` with the server's internal IP and port 80, which becomes `docker run --rm -d --name attack-<folder> <image> <IP> 80` on docker0, `modules/runners.py:147`):
- 6,718 GET: 3,359 `GET /` (302 to `login.php`) and 3,359 `GET /login.php` (200, the form). 0 requests to `/vulnerabilities/`.
- In the sqlmap log: "you have not declared cookie(s), while server wants to set its own (...). Do you want to use those [Y/n] Y"; "parameter 'User-Agent' does not seem to be injectable"; "parameter 'Referer' does not seem to be injectable"; "[CRITICAL] all tested parameters do not appear to be injectable". The traffic carries SQL injection payloads in the `User-Agent` and the `Referer` (3,356 requests), which DVWA does not use in any query: the attack tests, but never reaches an injectable point.
- MariaDB general log (a record of every query the database receives): 6,718 connections and 3,359 `USE dvwa` (the opening of each page), 0 other queries.
- sqlmap ends on its own (exit 0) in 210 s. Same against the server with the database created (241 s).

**Cause.**
- `entrypoint.sh:6`: `exec python /sqlmap/sqlmap.py -u "http://${TARGET}:${PORT}/" --batch --level=3`. The URL `/` has no parameter.
- In DVWA (files in `/var/www/html` of the server image) [read in code]: `/` is `index.php`, which requires a session (`index.php:6`) and redirects to `login.php` (`dvwa/includes/dvwaPage.inc.php:61-65`).
- In the image's sqlmap (commit `1b1f93ae`) [read in code]: the cookies the server sends become only a session header (`lib/controller/checks.py:1876-1884` puts them in `conf.httpHeaders` without touching `conf.cookie`), and the `Cookie` injection place is only created with `--cookie` (`lib/core/target.py:398-400`). What is left is `User-Agent` and `Referer`, tested with `--level` 3 or higher (`lib/controller/controller.py:626-629`), which `login.php` does not use in SQL.
- The injectable point of DVWA is `vulnerabilities/sqli/source/low.php:3-8`: `$_REQUEST[ 'id' ]` goes straight into `WHERE user_id = '$id'` (requires `Submit`), behind `vulnerabilities/sqli/index.php:6` (session). The default level is `low` (`config/config.inc.php:35`).

**How we tested.**
- Images: `sql-injection` built from the upstream tree at `8613c66` and from the same tree with this commit; both with sqlmap at commit `1b1f93ae` (1.10.10#stable) and Python 3.9.25. Servers: the upstream one and the one with WEB-02.
- Server without arguments, with `--memory 1536m`; attack with `--memory 1g` (no OOM). "Ready" when `mysqladmin ping` answers and the Apache pid exists; general log on.
- Path A arguments (`README.md:330-335` at the root): `<image> <server IP> 80`, without `-e`. A 600 s window; all runs ended on their own.
- Capture: from 2 s before to 2 s after.
- Count: tshark (requests by method and path; responses by code and `Location`), general log (queries by type, `WHERE user_id`), sqlmap output.
- 4 runs (the matrix). The 16.6 s is wall-clock, from `docker run` to the exit (the container itself was up for 14.5 s), with load 1.3 and no other test running on the host; in the sqlmap log, the boolean and error-based techniques appear about 1 s after the first test.
- A second independent review: recounted with tshark and its own parsers (pcap, general log, sqlmap output); read the cited sqlmap lines inside the image (`git log -1` = `1b1f93ae5cba`) and the DVWA ones inside the server image; tested both images against the unreachable target, finding the behavior change described in Fix.
- Deviations: general log on.
- Not tested: path B (the campaign, `contrib/scripts/run_full_campaign.py`, with `--network host` and target `127.0.0.1:8080`; only the IP and port change); today's sqlmap (`Dockerfile:3` clones without a pin).

**Fix.**
- `entrypoint.sh` logs in with the Python standard library (`urllib` and `http.cookiejar`): GET on `login.php`, extracts `user_token`, POST of `admin`/`password`/`Login`/`user_token`. Then it runs the same sqlmap with `-u "http://<target>:<port>/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="<PHPSESSID; security>" --batch --level=3`.
- Engine, `--batch`, `--level=3`, arguments and `attack.yaml` stay the same.
- Fixed credential `admin`/`password`: it is the user that DVWA's own setup creates (`dvwa/includes/DBMS/MySQL.php:53`). Declared choice. Same pattern as the fix of `php-lfi-enumeration` (WEB-03).
- Behavior change: with the `set -e` already at `entrypoint.sh:5`, an error in the login step ends the attack before sqlmap. [measured] Against an unreachable target (`127.0.0.1 9`, no network), the image with this commit exits with 1 and a `URLError` traceback, without running sqlmap; the upstream one runs sqlmap ("[CRITICAL] unable to connect") and exits with 0. [read in code] The same holds for a target that answers without the `user_token` field (outside a DVWA): the fixed attack does not run, where before sqlmap ran against `/`. A login that DVWA refuses does not raise an error: sqlmap runs with the unauthenticated session and does not reach the injectable point (measured against the server without the database, see Before and after; with the password changed, inferred to be the same). On the declared target (`http-server` with WEB-02) nothing else changes.

**Before and after.** [measured] 2 × 2 matrix, same setup; only the images change:

| attack \ server | upstream server (empty database) | server with WEB-02 |
|---|---|---|
| upstream | 6,718 GET (`/` and `/login.php`); 0 requests to `/vulnerabilities/`; 0 queries besides `USE dvwa`; "all tested parameters do not appear to be injectable" | same |
| with this commit | login POST, 302 `setup.php`; sqlmap follows the redirect: 8,381 `GET /vulnerabilities/sqli/`, 302 `../../login.php`; 0 credential queries, 0 by `user_id`; "all tested parameters do not appear to be injectable"; 475.9 s | 97 requests: `GET /login.php`, `POST /login.php` (302 `index.php`), `GET /index.php`, 94 `GET /vulnerabilities/sqli/?id=...` (200). General log: 1 credential query and 94 `SELECT first_name, last_name FROM users WHERE user_id = '<payload>'`, 13 of them with `UNION ALL SELECT` or `SLEEP(`. sqlmap: "Parameter: id (GET)" with 4 techniques (boolean-based blind, error-based, time-based blind, UNION query), "identified the following injection point(s) with a total of 86 HTTP(s) requests", "back-end DBMS: MySQL >= 5.1 (MariaDB fork)"; exit 0 in 16.6 s |

**How to reproduce.** In the reproduction file, section WEB-05; uses P1, P2, P3, P8.

**Caveats.**
- It only has an effect with WEB-02 (measured: without it, 8,381 302 responses and 0 injected queries).
- The `admin`/`password` credential is fixed. Outside a DVWA the fixed attack exits with 1 before sqlmap; on a DVWA with another password, it runs without a session and does not reach the injectable point (see Fix).
- Timing note, no fix: `max_runtime_s: 10` (`attack.yaml:8`) against 16.6 s of wall-clock for the fixed sqlmap (load 1.3; the injection already shows up in the traffic about 1 s after the first test; the final sqlmap report does not). Upstream took 210 to 241 s. The field is only used by the web interface watchdog (`modules/attackzoo_st.py:163-188`), which does `docker rm -f` at the end of the deadline [read in code].

**Versions.** sqlmap at commit `1b1f93ae` (1.10.10#stable) in the tested image; on 2026-11-12 `master` was at `8b78b676`, 124 commits later, and `Dockerfile:3` clones with `--depth 1` without a pin; `python:3.9-alpine` (Python 3.9.25); server `vulnerables/web-dvwa` (pinned in `Dockerfile:1` by the sha256 digest `dae203fe11646a86937bf04db0079adef295f426da68a92b40e3b181f337daa7`; DVWA 1.10, MariaDB); Docker 29.6.2.

### WEB-06 · xss-scanner: Scans Parameters That DVWA Does Not Have (Copied From The dalfox Example) And Never Tests DVWA's Reflected XSS

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/xss-scanner/entrypoint.sh`, `docker/attackers/xss-scanner/Dockerfile` |
| Depends on | WEB-02 (effect): without the DVWA database created, the login goes to `setup.php` and there is no reflection (measured) |

**Promise.**
- `docker/attackers/xss-scanner/attack.yaml:5`: "Automated scan and analysis of parameter flaws susceptible to XSS." (same in `README.md:3`). XSS (cross-site scripting) is when the page returns to the browser, without escaping, a snippet that came from the request.
- `attack.yaml:9-10`: `target_services: - http-server`; `docker/servers/http-server/server.yaml:30` lists `web_xss_scanner`; `server.yaml:16`: "Provide a vulnerable web application for web attacks, scanners, ...".

**What happens.** [measured] Upstream attack against the `http-server` (DVWA), on path A (the flow of `README.md:330-335` at the repository root: `attackzoo.py run` with the server's internal IP and port 80, which becomes `docker run --rm -d --name attack-<folder> <image> <IP> 80` on docker0, `modules/runners.py:147`):
- dalfox starts with `start scan to http://<IP>/login.php?cat=123&artist=123&asdf=ff`.
- 192 requests: 190 to `/login.php` (185 `GET ?cat=..&artist=..&asdf=..`, all with the login form in the response, 184 with 200 and 1 with 206; 4 `POST`, form mined by dalfox, no cookie, 302 `login.php`; 1 `HEAD`, 200) and 2 path probes (404).
- DVWA's reflection block (`<pre>Hello `) appears in 0 responses. dalfox says "found reflected 0 params" and "XSS found 0 XSS", and exits with 0. No payload is sent (the 3 URIs with `<` or `alert` are dalfox's own probes).
- `error.log`: 4 lines "Undefined index: session_token in login.php on line 12". Same against the server with the database created (WEB-02).

**Cause.**
- `entrypoint.sh:4`: `/app/dalfox url --url http://${TARGET}:${PORT}/login.php\?cat\=123\&artist\=123\&asdf\=ff --custom-payload /app/XSS-payloadbox.txt`. Like this since the first commit of the repository (`28c8d5f`); the server has always been DVWA.
- The parameters come from the dalfox README example for `testphp.vulnweb.com` (Acunetix's demo site), with the same escaping: dalfox v2.9.3, `README.md:95`, `dalfox url http://testphp.vulnweb.com/listproducts.php` followed by `\?cat\=123\&artist\=123\&asdf\=ff` [read in code].
- In DVWA (files in `/var/www/html` of the server image) [read in code]: `login.php` only reads `Login`, `user_token`, `username` and `password` (`login.php:10-20`); `cat`, `artist` and `asdf` do not appear in any DVWA PHP file (search: 0 lines).
- DVWA 1.10's reflected XSS is `vulnerabilities/xss_r/source/low.php:6-8` (`'<pre>Hello ' . $_GET[ 'name' ]`, no escaping), behind a session (`vulnerabilities/xss_r/index.php:6`, `dvwa/includes/dvwaPage.inc.php:61-65`). The level comes from the `security` cookie (`xss_r/index.php:17-32`; without the cookie, it falls to `impossible.php`); DVWA sets `security=low` on the first request (`dvwaPage.inc.php:25-28`, `config/config.inc.php:35`).

**How we tested.**
- Images: `xss-scanner` built on 2026-11-16 from the upstream tree at `8613c66` (dalfox v3.1.2, pinned by digest in `Dockerfile:1`) and from the same tree with this commit (which installed `curl` 8.23.0-r0 via `apk`). Servers: the upstream one and the one with WEB-02.
- Server without arguments, with `--memory 1536m`; attack with `--memory 1g`. "Ready" when `mysqladmin ping` answers and the Apache pid exists; MariaDB general log (a record of every query the database receives) on.
- Path A arguments (`README.md:330-335` at the root): `<image> <server IP> 80`, without `-e` (`attack.yaml` declares no environment variables). All runs ended on their own (the 300 s window was never used).
- Capture: from 2 s before to 2 s after.
- Count: tshark (requests and responses linked by `http.request_in`; `http.file_data contains "<pre>Hello "`), dalfox output, `access.log`, `error.log` and general log.
- Runs: the upstream attack 1 time against each server; the attack with this commit 2 times against each server (in the first round the image differed only in a comment line), with the same counts. Load: load from 0.8 to 1.5 in the upstream runs and from 3.5 to 6.0 in the final round (other tests on the host).
- A second independent review: recounted the 12 pcaps of this item and of WEB-07 (6 of each) with its own tshark fields and with its own TCP reassembly in Python (0 gaps); classified the reflected value in each of the 169 responses (it was what separated the 1 raw payload from the regex count, which also matched the closing `</pre>`); checked the cited dalfox lines (copy identical to the one on GitHub at commit `8926c464`, the v3.1.2 tag) and the DVWA ones; measured the times by `frame.time_epoch` against the container's `StartedAt`.
- Deviations: general log on.
- Not tested: path B (the campaign, `contrib/scripts/run_full_campaign.py`, with `--network host` and target `127.0.0.1:8080`); running the script in a browser; DVWA's `medium` and `high` levels.

**Fix.**
- `entrypoint.sh` logs in with `curl` (GET on `login.php`, extracts `user_token`, POST of `admin`/`password`/`Login`/`user_token` with a cookie file) and runs the same dalfox, with the same `--custom-payload`, on `--url "http://<target>:<port>/vulnerabilities/xss_r/?name=123"` with `--cookies PHPSESSID=...` and `--cookies security=...`. One cookie per flag because dalfox v3.1.2 does `split_once('=')` on each `--cookies` (`src/cmd/scan/input.rs:751-757`): `a=b; c=d` in a single flag would become one wrong cookie [read in code].
- `Dockerfile`: `apk add --no-cache curl` on the `chmod` line. The dalfox image is Alpine and has neither `curl` nor Python. We tried BusyBox's `wget` first, which already ships in the image: it follows the `Location: index.php` of the POST as if `index.php` were a host ("wget: bad address 'index.php'") and has no option to not follow a redirect; discarded. `curl` goes in without a pinned version (in the 2026-11-16 build, 8.23.0-r0): declared choice. An alternative without a new package, a raw POST with `nc`: not tested.
- Fixed credential `admin`/`password`: it is the user that DVWA's setup creates (`dvwa/includes/DBMS/MySQL.php:53`).
- Arguments and `attack.yaml` stay the same. The entrypoint has no `set -e`: outside a DVWA, or with the password changed, the login fails silently and dalfox hits the DVWA URL anyway [read in code].

**Before and after.** [measured] 2 × 2 matrix, same setup; only the images change:

| attack \ server | upstream server (empty database) | server with WEB-02 |
|---|---|---|
| upstream | 192 requests, 185 of them GET `/login.php?cat=...` with the login form in the response; `<pre>Hello ` in 0; "found reflected 0 params", "XSS found 0 XSS"; exit 0 | same |
| with this commit | login POST, 302 `setup.php`; 171 GET and 1 HEAD on `/vulnerabilities/xss_r/`, 302 `../../login.php`; `<pre>Hello ` in 0; "XSS found 0 XSS"; exit 0 | login POST, 302 `index.php`; 171 GET on `/vulnerabilities/xss_r/`: 167 with a 200 response, 1 with the `Range` header (206 response with the whole page) and 3 with dalfox's marker in a cookie (302); plus 1 POST and 1 HEAD with 200; `<pre>Hello ` block in 169 responses (those of the GETs with 200 and with 206 and that of the POST), of which 167 reflect text (`123` and markers from dalfox's parameter mining), 1 reflects dalfox's character probe raw, 1 reflects the payload `<svg onload=alert(1) class=dlx..>` raw. 1 XSS payload sent. dalfox: "found reflected 1 params", "XSS found 1 XSS", `[POC][V][GET][inHTML] .../vulnerabilities/xss_r/?name=%3Csvg%20onload%3Dalert%281%29...`; exit 1 |

**How to reproduce.** In the reproduction file, section WEB-06; uses P1, P2, P3, P8.

**Caveats.**
- It only has an effect with WEB-02 (measured: without it, 0 reflection).
- What was measured is the delivery: the server returns the payload unescaped, and dalfox's `[V]` means it found the injected element in the response DOM. Running the script in a browser was not measured.
- Note, no fix: with this commit, when it finds XSS the attack exits with 1 (measured; dalfox does this by design, `src/main.rs:471-474`). `contrib/scripts/check_attack_smoke.py:368-376` counts any exit other than 0 as a failure (`exited_nonzero`, `passed = False`) [read in code, not measured]: against a DVWA with WEB-02, and with a smoke deadline longer than the attack's duration, the working attack would show up as a failure. Handling the exit in the entrypoint would need a new measurement.
- `XSS-payloadbox.txt` (2,689 lines) is not used, neither before nor after this commit: upstream, dalfox finds no reflected parameter and sends no payload; with the commit, it sends 1 built-in payload, verifies and stops (0 requests with `prompt(8)`, the first line of the file). dalfox v3.1.2's help has `--deep-scan` ("test all payloads even after finding XSS"), which we did not test.
- Timing, not measured against the watchdog: the payload is the last request, 7.9 s after the first frame and 8.6 s after the container start (load 3.5 to 4.2). That the reflection fits in `max_runtime_s: 10` (`attack.yaml:8`) is an inference; the commit's runs against the server with WEB-02 took 12.9 and 17.5 s of wall-clock under load 3.5 to 6 (from `docker run` to the exit, including starting the container and the login; against the server without the database, 18.3 and 21.5 s), and the upstream ones, 8.5 and 8.6 s.

**Versions.** dalfox v3.1.2 (`hahwul/dalfox`, pinned in `Dockerfile:1` by the sha256 digest `91d5cebda9114fb7c2bfc7ad179ac5d605705c0bf4632a68f572f7a2f1d8a6dc`, revision `8926c464`; Alpine 3.24 image); `curl` 8.23.0-r0 from the Alpine repository on 2026-11-16, not pinned; the URL pattern comes from the dalfox v2.9.3 README; server `vulnerables/web-dvwa` (pinned in `Dockerfile:1` by the sha256 digest `dae203fe11646a86937bf04db0079adef295f426da68a92b40e3b181f337daa7`; DVWA 1.10, Apache 2.4.25); Docker 29.6.2.

## Commits: Layer 2 And SMB

### NET-01 · arp-spoof: ArpSpoof Resolves The CIDR One Address At A Time (2 S Per Silent Address) Before Forging The First Reply

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/arp-spoof/entrypoint.sh` |
| Depends on | none |

**Promise.**
- `docker/attackers/arp-spoof/attack.yaml:5`: "Network gateway interception attack through ARP spoofing."
- `docker/attackers/arp-spoof/attack.yaml:8`: `max_runtime_s: 10` (in the attack's `README.md:14`, "Suggested max runtime | `10s`").
- `contrib/scripts/DEMO-SF/DEMO.md:68`: "Simula interceptação entre o gateway e a rede Docker por 5 segundos." (command at `:71`, with the CIDR and the gateway of Docker's `bridge` network, `:47-48`).

**What happens.** ARP spoofing is answering ARP requests (the protocol that translates IP into MAC address) with the attacker's MAC, to divert traffic. Here it only starts after the tool discovers the MAC of every address in the CIDR (the network range passed as the target), one at a time, waiting 2 s for each address that does not answer ("silent"). No forged reply goes out before the end of this scan [measured]:
- /29 (6 addresses, 4 silent): 2.01 to 2.07 s per silent address and ~0.02 s per live address; the scan takes 8.1 s and the 1st forged reply went out 15.0 and 26.7 s after the container start (11.0 s in an earlier run; 9.99 s in a repetition of 2026-11-17 on a quiet machine, in which the container took 1.87 s from start to the 1st who-has, and 9.85 s in another, of 2026-11-18, with 1.70 s [measured]). Even on a /29 the 1st forged reply goes out close to the 10 s of `max_runtime_s` or after: it is the 8.1 s of the scan plus the container start.
- /25 (126 addresses, 124 silent): scan of 250.5 s; 1st forged reply at 253.2 and 266.2 s (253.7 s in an earlier run).
- In the campaign (`run_full_campaign.py`) and in the demo the CIDR is the docker0 subnet (Docker's default bridge), 172.17.0.0/16 by default (`contrib/scripts/run_full_campaign.py:313-329`, `:381-382`, `:417-420`; `DEMO.md:47-48`). 60 silent addresses already exceed 120 s, the default window of `experiment` (`modules/attackzoo/parser.py:93`), and the whole scan would take ~36.8 h [inferred: calculation with 2.02 s per silent address]. With the /24 of the README example (`docker/attackers/arp-spoof/README.md:36`), ~8.5 min [inferred: calculation].
- Once it starts, with `-s` only the gateway is poisoned: 100% of the forged replies go to the gateway's MAC [measured].

**Cause.**
- `docker/attackers/arp-spoof/entrypoint.sh:6`: `ArpSpoof "${GW}" "${NETWORK}" -s -t 0.1` passes the whole CIDR to ArpSpoof [read in code].
- ArpSpoof 1.1.2 (PyPI, the latest version), `ArpSpoof.py:313`: `gateway_mac = self.gateway_mac = getmacbyip(gateway, chainCC=1)`; `:314-316`: `{str(ip): getmacbyip(str(ip), chainCC=1) for ip in targets_object}`, one address at a time, before building the packets (`:323`) and the send loop (`:368-370`) [read in code].
- scapy 2.8.0, `scapy/layers/l2.py:179-185`: `getmacbyip` does `srp1(..., timeout=2)`, so each silent address costs ~2 s; the failure is not cached (`:189-193`) [read in code].
- PythonToolsKit 1.3.0, `GetType.py:597`: the CIDR becomes the list `IPv4Network(ip).hosts()` [read in code].
- `max_runtime_s` is only enforced by the Streamlit interface's watchdog, which does `docker rm -f` after the deadline (`modules/attackzoo_st.py:163-188`) [read in code].

**How we tested.** Images built from upstream 8613c66 (`docker build --no-cache`) and with this commit; the two share 8 of 10 layers (only the `entrypoint.sh` copy and the `chmod` differ). Gateway at .250 and victim at .251, both live (each pings the other every 0.2 s), attacker at .20, outside the tested CIDRs. Arguments in the form of the README's `docker run`: `<gateway> <CIDR>`, with the /29 .248/29 and the /25 .128/25; the example /24 and docker0's /16 were left out because they would include .1, which is the host. A 300 s window; t0 = the container's `StartedAt`. Count with tshark by the fields `eth.src`, `arp.opcode`, `arp.src.proto_ipv4` and `arp.dst.proto_ipv4`; forged reply = opcode 2 (reply) with the attacker's source MAC and a source IP different from its own. 2 runs per combination of CIDR and image, the 2nd in reverse order; host load from 2.5 to 7.9 (other tests running). A second reviewer recounted the 8 pcaps with tshark and with its own pcap reader (same times and sets) and repeated one /25 run with the fix: 1st forged reply at 14.6 s, because the container start took 12.4 s. Not tested: /24, /16; traffic actually intercepted.

**Fix.** The commit changes only the body of the `if` in `entrypoint.sh`; `ENTRYPOINT`, Dockerfile and arguments stay the same. A Python snippet does a single burst of who-has (the ARP request "who has this IP?") to the gateway and to every address in the CIDR, with a single 2 s timeout (`scapy.srp`); stores the replies in a dictionary; swaps `ArpSpoof.getmacbyip` for a lookup in that dictionary; and calls `ArpSpoof.main()` with the same arguments (`-s -t 0.1`). ArpSpoof's send loop does not change. Why this way: the set of forged addresses and the send rate stay identical to upstream's (measured). Alternative considered and discarded: scan first and pass ArpSpoof only the hosts that answered; this shrinks the forged set to the live hosts and changes the profile on the wire [read in code]. Outside the commit: version pinning (see Caveats) and an `else` with a usage message. Today, with another number of arguments, the `if` without `else` (`entrypoint.sh:2-7`) exits 0 with no output at all (tested with 0, 1 and 3 arguments), but no documented flow reaches that case and a patch for the `else` alone was not built.

**Before and after.** Same network, same arguments; only the image changes. Where there are two values, they are the two runs.

| Measure | /29 before | /29 after | /25 before | /25 after |
|---|---|---|---|---|
| scan who-has | 6 in 6.08 s | 7 in 3 to 11 ms | 127 in 248.4 s | 127 in 45 to 46 ms; reviewer 99 ms |
| 1st who-has to 1st forged | 8.09 and 8.11 s | 2.02 and 2.03 s | 250.5 and 250.5 s | 2.11 and 2.11 s; reviewer 2.20 s |
| start (container start to 1st packet) | 6.9 and 18.6 s | 2.0 and 5.6 s | 2.7 and 15.8 s | 4.8 and 2.4 s; reviewer 12.4 s |
| start to 1st forged | 15.0 and 26.7 s | 4.0 and 7.7 s | 253.2 and 266.2 s | 6.9 and 4.5 s; reviewer 14.6 s |
| forged in the first 10 s | 0 and 0 | 180 and 73 | 0 and 0 | 198 and 337; reviewer 0 |
| interval between forged replies for the same IP | ~0.19 s | ~0.19 s | 2.09 to 2.12 s | 2.08 to 2.16 s |
| forged set (source IP) | .249 to .254 (6) | identical | .129 to .254 (126) | identical |

In all runs, every forged reply goes to the gateway's MAC, with destination IP .250.

In a repetition of 2026-11-17, on a quiet machine (load from 0.96 to 1.24), in the same column order [measured]: scan who-has 6 in 6.09 s, 7 in 3 ms, 127 in 248.4 s and 127 in 44 ms; 1st who-has to 1st forged 8.12, 2.04, 250.44 and 2.10 s; start (start to 1st who-has) 1.87, 1.62, 1.66 and 1.67 s; start to 1st forged 9.99, 3.66, 252.10 and 3.77 s; forged in the first 10 s 1, 216, 0 and 438; forged set the same.

In another repetition, of 2026-11-18, also on a quiet machine (load from 1.27 to 1.49), in the same order [measured]: scan who-has 6 in 6.118 s, 7 in 3 ms, 127 in 248.4 s and 127 in 45 ms; 1st who-has to 1st forged 8.15, 2.02, 250.48 and 2.10 s; start 1.70, 1.53, 1.71 and 1.81 s; start to 1st forged 9.85, 3.55, 252.19 and 3.91 s; forged in the first 10 s 6, 219, 0 and 416; forged set the same.

**How to reproduce.** In the reproduction file, section NET-01; uses P1, P2, P3, P4.

**Caveats.**
- The fix does not guarantee `max_runtime_s: 10`: with it, the 1st forged reply went out between 3.55 and 14.6 s after the start (n=9, with the two of the 2026-11-17 repetition, 3.66 and 3.77 s, and the two of the 2026-11-18 one, 3.55 and 3.91 s), because the container start (from the start to the 1st packet, which includes loading Python and scapy) varied from 1.53 to 18.58 s on this host, shared in the tests and quiet in the repetitions (from 1.62 to 1.87 s in the 2026-11-17 one and from 1.53 to 1.81 s in the 2026-11-18 one), before and after [measured]. The cause of the variation was not measured and the fix does not act on it. What it changes is the resolution: from ~2 s per silent address to a single ~2 s timeout (2.02 to 2.20 s, 9/9).
- docker0's /16 was not measured with the fix (it would be 65,535 who-has in a single burst; cost and losses not measured); only the upstream calculation above holds for it. The example /24 was not measured either.
- Swapping `ArpSpoof.getmacbyip` depends on the internal structure of ArpSpoof 1.1.2, and the Dockerfile installs without a version (`docker/attackers/arp-spoof/Dockerfile:5`): if ArpSpoof changes, the swap may stop working without raising an error [read in code, not measured]. Suggestion, outside this commit: pin `ArpSpoof==1.1.2 PythonToolsKit==1.3.0 scapy==2.8.0`.
- The dictionary does not follow routes, does not handle multicast or broadcast and does not expire. For targets on the same link with `-s` (only the gateway's MAC goes into the packets, `ArpSpoof.py:385-394`) the measured result was the same as upstream's [read in code + measured]. Off the link, scapy uses the route's gateway and the cache (`l2.py:159,170-171`) [read in code, not tested].
- We did not measure traffic interception, only the sending of the forged replies.

**Versions.** ArpSpoof 1.1.2, PythonToolsKit 1.3.0 and scapy 2.8.0 (the Dockerfile's `pip install` does not pin versions; these were the ones resolved on 2026-11-16); base `python:3.11-alpine@sha256:7fbad8e4...` (Python 3.11.18, Alpine 3.24.4); Docker 29.6.2.

### NET-02 · stp-conf-flood, stp-tcn-flood, cdp-table-flood And dhcp-starvation: yersinia In The Background Gets /dev/null As Stdin And Stops Right Away (0 To 1 Frame Per Run)

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/stp-conf-flood/entrypoint.sh`, `docker/attackers/stp-tcn-flood/entrypoint.sh`, `docker/attackers/cdp-table-flood/entrypoint.sh`, `docker/attackers/dhcp-starvation/entrypoint.sh` |
| Depends on | none |

**Promise.**
- `docker/attackers/stp-conf-flood/attack.yaml:5`: "BPDU (Bridge Protocol Data Unit) packet flood with STP topology reconfiguration information and random MAC addresses."
- `docker/attackers/stp-tcn-flood/attack.yaml:5`: "BPDU (Bridge Protocol Data Unit) packet flood with STP topology change information and random MAC addresses."
- `docker/attackers/cdp-table-flood/attack.yaml:5`: "CDP (Cisco Discovery Protocol) table flood on the local network."
- `docker/attackers/dhcp-starvation/attack.yaml:5`: "DHCP lease exhaustion on the local network."
- Label of `active_s`, "Active flood duration inside the attack window (s)": `attack.yaml:21` (stp-conf, stp-tcn, dhcp) and `:19` (cdp). `README.md:26` (stp-tcn, cdp, dhcp): "Maximum time spent generating ... traffic inside the attack window." `cdp-table-flood/README.md:37`: "preserving representative CDP flood traffic". `stp-conf-flood/README.md:24`: "This attack can generate a large amount of data".
- yersinia itself prints `<*> Starting DOS attack sending conf BPDUs...` (or the equivalent for each attack) on every run.

STP is the protocol that bridges use to avoid loops; BPDU is its message (configuration or TCN, a topology change notice). CDP is Cisco's neighbor discovery protocol. DHCP is the protocol that hands out IP addresses (DISCOVER is the client's initial request).

**What happens.** With the defaults (COUNT=1, one yersinia process), each run sends 0 or 1 frame [measured]. In 12 runs (the 4 attacks, each in the README form, in the README form with `-i -t` and in the campaign form), the attacker side had 0 or 1 frame and the bridge 0 or 1. The 12 logs have "Starting DOS attack" and "Press any key to stop the attack" and none has "TERM signal received": yersinia exits on its own, before the `timeout`'s SIGTERM (the container lived from 0.8 to 3.3 s, depending on the host load). This holds for the current launcher, which came in with `5aab85b` (2026-07-13) in stp-tcn, cdp and dhcp and with `ae469fb`/`33b0c6c` (2026-07-17) in stp-conf. The pages of the published campaign (`contrib/docs/campaign/net_*.md`, numbers since `f835bf5`, 2026-07-05) come from the old launcher, which fired 2000 processes (1000 in dhcp) without waiting for them, and so they show traffic (e.g. stp-conf with an average of 260,994 rows at the campaign's L1 level, with attack, against 9,599 at L0, without attack) [read in code]. Why the old launcher generated traffic even with the same stdin was not tested [inferred: each of the 2000 processes would send something before reading stdin].

**Cause.**
- `stp-conf-flood/entrypoint.sh:40`, `stp-tcn-flood/entrypoint.sh:37`, `cdp-table-flood/entrypoint.sh:37`, `dhcp-starvation/entrypoint.sh:37`: `timeout -k 2s "${ACTIVE_S}s" nice -n "${NICE_LEVEL}" /usr/bin/yersinia <proto> -attack N -interface eth0 &`, in a `#!/usr/bin/env bash` script (non-interactive shell, no job control) [read in code].
- Without job control, the shell gives a background command (`&`) the stdin `/dev/null` when there is no explicit redirection (POSIX, Shell Command Language, "Asynchronous Lists"; bash manual, section "Lists") [read in code + measured: in the image's bash 5.2.21 the job gets `/dev/null` with `docker run -d`, `-i`, `-t` and `-i -t`].
- yersinia v0.8.2 (github.com/tomac/yersinia, tag v0.8.2 = `701b59b`), `src/yersinia.c`, function `doloop`: `:479` prints "Starting %s attack", `:481` launches the attack, `:494` enters the loop if the attack is continuous, `:496` prints "Press any key to stop the attack", `:504` does `select()` on fd 0 and `:516-517` does `getchar(); fail = 1;`. That is, it stops the attack as soon as stdin becomes readable, and `/dev/null` is readable right away, with EOF (end of file). The 4 attacks used are continuous: `src/xstp.h:240-241`, `src/cdp.h:201`, `src/dhcp.h:428` [read in code; the Ubuntu package's 2 patches do not touch these files].
- No attackzoo path gives the job an open stdin: `modules/runners.py:147` (`docker run --rm -d`, without `-i`/`-t`), `contrib/scripts/check_attack_smoke.py:317` (`docker run -d`) and the READMEs (`docker run --rm -d`); and even with `-i`/`-t` the job still gets `/dev/null` [read in code + measured].

**How we tested.** Images built from upstream 8613c66 and with this commit; only the 2 entrypoint layers differ, and `/usr/bin/yersinia` has the same md5 in both and in images built earlier. Isolated Docker network (`--internal`, STP off on the bridge, as on docker0), with fixed IPs; the attack ran in the network namespace of an idle container, so that the attacker-side capture started before it. Two full-frame captures (`-s 0`) without a filter, from 1 s before the attack to 2 s after the end: on the attacker's eth0 and on the bridge, 0 drops. Count by raw BPF in tcpdump (BPF is libpcap's packet filter language; e.g. configuration BPDU: `ether dst 01:80:c2:00:00:00 and ether[14:2]=0x4242 and ether[20]=0x00`) and by field in tshark, with the same number in every run. Environment variables the same as the ones attackzoo's `cmd_run` generates. README form (the container runs until it exits on its own): STP `-e ACTIVE_S=1 -e NICE_LEVEL=19 -e DURATION_S=0 -e COUNT=1 -e DELAY_MS=2000`; cdp `-e ACTIVE_S=5 -e NICE_LEVEL=10 -e DURATION_S=0 -e COUNT=1 -e DELAY_MS=500`; dhcp the same as cdp with `DELAY_MS=1000`. Campaign form: the same env with `DURATION_S=20` and `docker kill` at 20 s. Also the README form with `-i -t`. Stdin test without network (`--network none`): the image's own entrypoint with a fake yersinia that only prints its own fd 0, 16/16 with `/dev/null` upstream (4 attacks x 4 `docker run` modes) and 16/16 with a pipe in the fixed one. Host load from 3.0 to 4.9, with other tests running; the finding rests on counts (0 to 1 against 10^5 to 10^6), not on a rate.

A second reviewer recounted the 40 pcaps with its own Python parser, which reads the raw bytes without tcpdump or tshark: all the numbers matched. It also redid the before without the idle container (each attack in its own network namespace, `docker run -d` with the exact env, counting by the veth counter on the host): 2 to 4 frames in the container's whole life, including with the README's exact command and with an image built earlier; with the fix, 316 thousand to 1.42 million. Afterwards there was a re-measurement on a quiet machine, with the same fixed images, README form: 34/34 runs with frames on this machine, without disk contention, recounted by the reviewer with its own parser. Not tested: effect on a victim (see NET-04 and NET-05).

**Fix.** One line and one comment per entrypoint: `... /usr/bin/yersinia <proto> -attack N -interface eth0 < <(sleep "${ACTIVE_S}") &`. Stdin becomes a pipe that only closes at `ACTIVE_S`, the same instant as the `timeout`. Same tool, same `-attack`, same interface, same `ACTIVE_S`, `NICE_LEVEL`, `COUNT`, `DELAY_MS`, `DURATION_S` and `HOLD_GRACE_S`, and the same `timeout -k 2s` ceiling; `ACTIVE_S` is still limited by `DURATION_S` (`entrypoint.sh:11-13`). Running with `-i`/`-t` does not solve it (measured above). Side effects: one extra `sleep` per worker, outside `pids[]`; and yersinia now ends on the `timeout`'s SIGTERM, see Caveats.

**Before and after.** Attack frames, attacker side / bridge. The bridge drops frames with a group source MAC (yersinia draws all 48 bits of the source MAC at random, including the I/G bit that marks a group address, `src/attack.c:263-267`), about half [measured: 0 group-source frames on the bridge and the same number of unicast on both sides].

| Attack (frame counted) | Before, README form | Before, README with `-i -t` | Before, campaign form | After, README form | After, campaign form |
|---|---|---|---|---|---|
| stp-conf (configuration BPDU) | 1 / 0 | 0 / 0 | 0 / 0 | 296,505 / 148,062 | 277,858 / 138,900 |
| stp-tcn (TCN BPDU) | 0 / 0 | 1 / 0 | 0 / 0 | 125,394 / 62,548 | 131,521 / 65,857 |
| cdp (CDP advertisement) | 1 / 0 | 0 / 0 | 1 / 1 | 1,310,076 / 654,425 | 1,217,838 / 609,500 |
| dhcp (DISCOVER) | 1 / 0 | 1 / 0 | 1 / 0 | 933,633 / 467,037 | 818,578 / 408,499 |
| logs with "TERM signal received" | 0 of 12 (summing the 3 forms) | | | 8 of 8 (summing the 2 forms) | |

Re-measurement with the host quiet, after the fix, README form, attacker side: stp-conf 241,466 to 278,256 (12/12 runs with frames), stp-tcn 209,316 to 293,848 (12/12), dhcp 970,313 to 989,365 (5/5), cdp 1,028,368 to 1,146,886 (5/5); flood duration in the pcap from 0.82 to 0.93 s on the STP ones and ~4.9 s on dhcp and cdp. In the runs with the fix in the table above, every attack frame has a distinct source MAC.

**How to reproduce.** In the reproduction file, section NET-02; uses P1, P2, P3, P4.

**Caveats.**
- Only traffic was measured in this item. We do not say the fix restores lease exhaustion, STP reconfiguration or a full CDP table: the attackzoo scenario has no victim for these protocols (on docker0 STP is off, `stp_state=0` [measured]; no DHCP server; nothing listens to CDP [read in code]). The proposed and measured victims are in NET-04 (DHCP) and NET-05 (CDP). An STP victim (Linux bridge with STP) was tested and stays out of the PR: on by default, it would send a hello BPDU every 2 s on docker0 [measured on the isolated network: 57 to 60 in ~112 s] (it would enter the unfiltered pcaps of 12 campaign attacks [read in code]), and stp-tcn-flood against it generated ~147 thousand messages in the host kernel log in a 1 s run (64,776 written and 81,823 lost by journald) [measured]; it would have to come up only on demand. Against a bridge with STP, 1 TCN from the attack without the fix already re-arms the topology change for 35 s [measured]: the fix changes the volume, not the existence of the effect.
- With `active_s=1` (the default of both STP ones), the `timeout` clock starts at the fork (coreutils 9.4, `timeout.c:563`), before the exec of `nice` and yersinia, so the start eats part of the window: alone, the measured flood was from 0.82 to 0.93 s. With `active_s=1` and a slow yersinia start, the flood shortens and may send nothing. On dhcp and cdp (`active_s=5`) the slack absorbs this.
- With the fix, yersinia sometimes prints "double free or corruption (fasttop)" on receiving the SIGTERM (2 of 8 runs; 0 of 5 in the reviewer's), after the flood; the count and the container's exit do not change. Probable cause [read in code, not proven]: the SIGTERM handler `final()` calls `g00dbye()` from inside the signal (`src/yersinia.c:959-963`). With an open stdin and only the SIGTERM, it appeared 1 time in 40; it does not come from the pipe.
- We do not cite a frames-per-second rate: the numbers above were measured with other tests on the host; the comparison is by count.
- On docker0, which is where attackzoo runs these attacks on all three paths (`modules/registry.py:82-101` only uses `--network host` with a loopback target and port), the flood reaches every container on the network and the host's docker0 interface [read in code, not measured]. Run by hand with `--network host`, `-interface eth0` would be the host's NIC with that name, if it exists, and the flood would go out to the physical network [read in code].
- The stp-tcn-flood README still describes old defaults; see NET-03 (report only).

**Versions.** yersinia 0.8.2 (Ubuntu noble package `0.8.2-2.2build2`, binary md5 `a8e6948fe2ff1b1f8a15f3cbcbc56f1e`; source from tag v0.8.2 = `701b59b`); coreutils 9.4-3ubuntu6.3; bash 5.2.21; base `ubuntu:24.04@sha256:73b99939...` (`apt install yersinia` does not pin a version).

### SMB-01 · smb-server: Nmbd Does Not Start, Even Though The Server Declares NetBIOS And Publishes 137/138 Udp

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/servers/smb-server/Dockerfile` |
| Depends on | none |

**Promise.** NetBIOS over TCP/IP has three services: names (NBNS, 137/udp), datagrams (138/udp) and session (139/tcp). nmbd is the Samba daemon that serves the first two.
- `docker/servers/smb-server/server.yaml:8-10`: `protocols: - smb - netbios`; `:11-15` `internal_ports` with `137/udp` and `138/udp`; `:16-20` `published_ports` with `137:137/udp` and `138:138/udp`; `:24-25` `observability: - SMB/NetBIOS queries`.
- `docker/servers/smb-server/Dockerfile:57`: `EXPOSE 137/udp 138/udp 139 445`.
- `README.md:78` (root): "| SMB/Samba | `server-smb-server` | `139/tcp`, `445/tcp`, `137/udp`, `138/udp` |"; `README.md:194-196`: "Ports that may be exposed on the host: ... **UDP**: 137, 138, 5683, 8888."
- `contrib/scripts/run_full_campaign.py:139`: `SMB_PORTS = {137, 138, 139, 445}`.
- `docker/servers/smb-server/samba.sh:123`: "-n          Start the 'nmbd' daemon to advertise the shares".

**What happens.** Started the way attackzoo starts it, the server answers every NetBIOS name or datagram query with ICMP port unreachable (closed port) [measured]: the nmbd process does not exist, there is no socket on 137/138, 14 NBNS queries got 0 replies (14 ICMP port unreachable) and 5 datagrams to 138 got 5 ICMP. `smb-enumerating` logs "[-] Could not get NetBIOS names information via 'nmblookup': timed out" in 13 of 13 runs. The NetBIOS session on 139/tcp works (it is smbd).

**Cause.** `docker/servers/smb-server/samba.sh:171` (`n) NMBD="true" ;;`) and `:215` (`[[ ${NMBD:-""} ]] && ionice -c 3 nmbd -D`): nmbd only starts with the `-n` option or with the `NMBD` variable [read in code]. None of attackzoo's starts passes either one: `servers.sh:107`, `docker/build-images.sh:59`, `docker/servers/smb-server/server.yaml:21`, `docker/servers/smb-server/README.md:22`, `gerar_campanha_benigna.py:49`; and the Dockerfile does not define `NMBD` [read in code: `git grep -n NMBD` only finds `samba.sh:171` and `:215`]. The `/usr/sbin/nmbd` binary exists in the image [measured]; only the start is missing.

**How we tested.** Server built from upstream 8613c66 with `--no-cache` (as in `docker/build-images.sh:58`) and with this commit; the fixed image has the same layers and only the `Env` changes (`NMBD=true`) [measured with `docker image inspect`]. `smb-enumerating` built from upstream with `--no-cache` (enum4linux-ng `288826f`; Samba 4.23.8 in the attack image); port scanners = images built earlier, with code identical to upstream's (only the `FROM` pinned by digest). Server with the arguments of `servers.sh:107` (`-i -t`, `-g "log level = 3" -s "public;/share" -u "example2;badpass"`). NetBIOS queries from throwaway containers with the tools of the `smb-enumerating` image (`nmblookup -A`, `nmblookup -U`, 5 UDP datagrams to 138, `smbclient -L ... -p 139`); `ps` and `netstat -lnu` inside the server. Full-frame capture on the bridge, 0 drops (the UDP scan's one was cut at 900 s). Count with tshark (NBNS, ICMP type 3 code 3, SMB2). Before and after with the same script, only the server image changes; for the scanners, old and fixed server side by side, one scanner against each. A second reviewer recounted with tshark and its own parsers and ran two more scanners that had not been run (`port-scanner-os` and `port-scanner-vulnerabilities`) and `port-scanner-udp` again, with the host without other floods (load 2 to 3). From the owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): healthcheck of the fixed server `healthy`. Not tested: docker0 (NetBIOS broadcasts on it) and `-p 137:137/udp` through docker-proxy (the Docker process that relays the port published with `-p` to the container).

**Fix.** `ENV NMBD=true` (plus 1 comment line) in the Dockerfile, before the `ENTRYPOINT`. It covers all the start paths above without touching any of them. Equivalent alternative, not chosen: `-n` on the 5 start lines (5 files).

**Before and after.**

| Measure or attack | Before | After |
|---|---|---|
| nmbd process; udp sockets 137/138 | does not exist; 0 | `nmbd -D`; 137 and 138 open |
| NBNS queries to the server / replies / ICMP port unreachable | 14 / 0 / 14 | 3 / 3 / 0 (one query per question, no retransmission) |
| datagrams to 138 / ICMP | 5 / 5 | 5 / 0 |
| `nmblookup -A <server>` | "No reply from ..." | 5 names (host `<00>`, `<03>`, `<20>`; MYGROUP `<00>`, `<1e>`); 7 after nmbd becomes master browser, with `..__MSBROWSE__.` `<01>` and MYGROUP `<1d>`, and 6 (without the `<1d>`) for a few seconds between the two registrations [measured on 2026-11-17, querying every ~5 s: 5 names until ~24 s after the start, 6 at ~30 s, 7 from ~35 s until the end of the probe, ~150 s; 6 also in an earlier reproduction, ~25 s after the start] |
| `smb-enumerating` | 13/13 "Could not get NetBIOS names information via 'nmblookup': timed out" | 2/2 "Got domain/workgroup name: MYGROUP" and 7 names; the rest of the output the same (dialects, sessions, OS, users, groups, "Found 2 share(s)", policy, printers); 180 = 180 SMB2 packets from the client |
| `port-scanner-aggressive` (`nmap -sV -O -A`) | NBNS: 11 queries, 0 replies, 7 ICMP; no nbstat line | 2 queries, 2 replies, 0 ICMP; gains "\|_nbstat: NetBIOS name: ..."; rest the same |
| `port-scanner-os` (reviewer) | 11 queries, 0 replies, 7 ICMP | 2 / 2 / 0; gains "\|_nbstat" |
| `port-scanner-vulnerabilities` (reviewer) | 13 queries, 0 replies, 10 ICMP | 1 / 1 / 0; same output |
| `port-scanner-udp` (`nmap -sU`) | "All 1000 scanned ports ... are closed (port-unreach)" (2 of 2 runs) | "137/udp open netbios-ns", 958 closed, 41 open\|filtered, with 138 among the 41 (2 of 2 runs) |
| NetBIOS broadcasts from the server | 0 | 49 in 900 s (32 NBNS and 17 BROWSER); 41 in the first ~90 s, then announcements at 167, 347, 589 and 889 s |
| server memory | 22.7 MiB | 24.5 MiB |

The ~40 extra `open|filtered` ports of `nmap -sU` depend on the run, not on the fix [measured]. What repeats with the fix is 137 `open` and 138 `open|filtered` (nmbd listens on 138 and does not answer nmap's probe). The others are closed ports whose ICMP port unreachable did not arrive: the kernel limits this ICMP to ~1 per second per destination (`net.ipv4.icmp_ratelimit` = 1000 ms, the default, on the host and in the containers [measured]), and the port without a response is left `open|filtered`; the set changes between runs. In the 2 runs of the test (both scanners side by side, load 4.51 and 2.97 at the start) they appeared only against the fixed server (41 = 41, 138 among them), and against it the first reply from 137 arrived at 36.5 s of the scan and nmap sent 1,720 probes, against 1,145 in the `8613c66` one. On 2026-11-17, with the machine loaded (load 7.81 at the start), they also appeared against the `8613c66` server, which answers nothing on 137 (960 closed and 40 open\|filtered, against 958 and 41 in the fixed one); with the machine quiet, in two runs, they did not appear against either (1000 closed; 998 closed, 137 `open` and 138 `open|filtered`). It is not a regression: the difference the fix guarantees is that of 137 and 138.

**How to reproduce.** In the reproduction file, section SMB-01; uses P1, P2, P4.

**Caveats.**
- Side effect: nmbd advertises the server. On docker0 this becomes new benign traffic (NBNS and BROWSER broadcasts) in the unfiltered pcaps and in the ones that filter 137/138 of smb-server [inferred for docker0; measured on the isolated network: 49 broadcasts in 900 s].
- It changes the output of 4 attacks that send NetBIOS queries (`smb-enumerating`, `port-scanner-aggressive`, `port-scanner-os` and `port-scanner-udp`); `port-scanner-vulnerabilities` starts getting a reply, with the same output. No regression case in the measurements, with the caveat of `nmap -sU` above.
- We do not cite a time gain: enum4linux-ng's "Completed after" is its own internal timer, and the container's wall-clock time varied with the host load.
- `-p 137:137/udp` and `-p 138:138/udp` through docker-proxy on docker0 were not tested; the finding does not depend on the network, only on the process.

**Versions.** Samba 4.19.9 on the server (Alpine 3.20.10, `samba-4.19.9-r0`); enum4linux-ng `288826f` (1.3.10) and Samba 4.23.8 in the `smb-enumerating` image; nmap from the `port-scanner-*` images built earlier (code identical to upstream's).

## Commits: Campaign

### CAMP-01 · run_full_campaign.py: The Capture Filter Of cdp-table-flood ('Ether Dst') Does Not Compile On The Default Iface (-I Any): tcpdump Dies And The Campaign Carries On As 'Completed'

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `contrib/scripts/run_full_campaign.py` |
| Depends on | none |

**Promise.**
- `contrib/docs/SCRIPTS.md:27`: "This is the right script when you want to produce a reproducible experiment set under `experiments/<out>/`, with PCAPs, features, datasets, telemetry, and per-attack reports."
- `contrib/docs/SCRIPTS.md:32`: "Automatically resolves target service, port, probes, and BPF per attack when possible."
- `contrib/scripts/run_full_campaign.py:4-5`: "keeps raw PCAPs and per-run metadata under experiments/<campaign>/"; `:1077`: `--iface` "Interface passed to tcpdump.", with default `any` (`:57`).
- `docker/attackers/cdp-table-flood/README.md:59`: "Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`."

**What happens.** BPF is libpcap's capture filter language, used by tcpdump. In the campaign, with the default iface `any` (all interfaces), the cdp-table-flood filter does not compile: tcpdump exits with code 1 in under 1 s, the error goes to `/dev/null`, no pcap is created, and the campaign marks the attack as `completed`, prints `[OK]` and generates an empty dataset [measured]. In one campaign run (levels L0, without attack, and L1, with attack; with features and dataset): `campaign_attack_result.json` with `status=completed`, `experiment_rc=0` and `report_rc=0`; no `.pcap` in the `L0/run01` and `L1/run01` folders (`meta.json` points to a path that does not exist); tshark CSV with 0 B and scapy CSV with 102 B (only the header); datasets of 160 B with 1 row (only the header); attackzoo's own reports (the T6, T7 and T8 tables of `modules/attackzoo/reports/stability.py`: per-run metrics, validation and artifact inventory) show `T6 pcap_exists=0`, `T7 capture_valid=0` and `T8 dataset_rows=0`. Meanwhile the bridge showed 625,880 CDP advertisements from the attack. It holds for levels L0 to L3, because the filter is the same for the whole session.

**Cause.**
- `contrib/scripts/run_full_campaign.py:57`: `DEFAULT_IFACE = "any"`; `:60`: `"net_cdp_table_flood": "ether dst 01:00:0c:cc:cc:cc"`; `build_bpf` returns that entry (`:482-488`) and the plan passes `--iface any --bpf <filter>` to `attackzoo.py experiment` (`:677-680`) [read in code]. The cdp entry came in with `ae469fb` (2026-07-17, "Yersinia params"); `any` has been the default since `a2c7f65` (2026-06-28) [read in `git log -S`].
- On the `any` device tcpdump 4.99.4 uses the link type `DLT_LINUX_SLL2` (`tcpdump.c:1972-1977`), a Linux "cooked" header, without an Ethernet destination address (libpcap 1.10.4, `gencode.c:1436-1441`). `ether host`/`ether dst` only compiles on Ethernet, FDDI, Token Ring, 802.11 and IP over Fibre Channel; on other types it gives `bpf_error("ethernet addresses supported only on ethernet/FDDI/token ring/802.11/ATM LANE/Fibre Channel")` (`gencode.c:7235-7262`) [read in code; the Ubuntu patches of libpcap and tcpdump do not touch `gencode.c`]. It also does not compile with the cooked v1 header (`-y LINUX_SLL`) [measured], so it fails on `-i any` in any tcpdump version.
- The failure is silent by design [read in code]: `modules/attackzoo/capture.py:26` opens tcpdump with `stdout` and `stderr` on `subprocess.DEVNULL`; `modules/attackzoo/experiment.py:232-236` only handles `FileNotFoundError` (tcpdump missing); `:274` stops a process that already died; `:279-303` extracts features and builds the dataset without checking the pcap; `:353` prints `[OK]`. `modules/features.py:303-309` writes the scapy CSV header before opening the pcap, `modules/datasets.py:251` accepts any CSV larger than 0 B, and `run_full_campaign.py:1002` marks `completed` with code 0.

**How we tested.** Whole upstream tree 8613c66 (`git archive`) before and with this commit. The documented host environment (`README.md:98`, Ubuntu 24.04; `README.md:138`, `tcpdump 4.99.4-3ubuntu4.24.04.1`) reproduced in an `ubuntu:24.04` image with that tcpdump, `libpcap0.8t64 1.10.4-4.1ubuntu3.1`, tshark and the `requirements.txt` venv, set up as in `setup.sh:22-43`. The attack was `cdp-table-flood` with NET-02 applied (without it yersinia sends 0 to 1 frame), with the env of the campaign form `-e ACTIVE_S=5 -e NICE_LEVEL=10 -e DURATION_S=20 -e COUNT=1 -e DELAY_MS=500`. Ground truth = unfiltered Ethernet capture on the bridge, 0 drops.
1. Compilation: all the filters of the campaign plan (dry-run of `run_full_campaign.py` itself, 60 plans: 15 distinct filters and 12 attacks without a filter) with `tcpdump -d` on `-i any` and on `-i eth0`, in tcpdump 4.99.4/libpcap 1.10.4 and in 4.99.6/1.10.7.
2. Capture step: a container on the isolated network calls `start_tcpdump` (from `modules/attackzoo/capture.py`) with the filter from `build_bpf` and `run_full_campaign.py`'s own `DEFAULT_IFACE`, while the attack runs for 20 s on the same segment; it records the argv, whether the process is alive after 1 s and whether the pcap exists.
3. Whole campaign: `python3 contrib/scripts/run_full_campaign.py --only net_cdp_table_flood --runs 1 --levels L0,L1 --warmup 10 --attack 20 --cooldown 10 --no-start-servers --no-collect-server-stats`, run three times (one with the other options at the default, with features and dataset, which is the one in "What happens", and, for the table, one before and one after with `--no-extract-features --no-build-dataset`), in a container on the isolated network with a fake `docker` that only records the calls; from outside, an observer of ours brought up the real attack with the same `docker run` that attackzoo's hook generated (`run --rm -d --name attack-cdp-table-flood -e ACTIVE_S=5 -e NICE_LEVEL=10 -e DURATION_S=20 -e COUNT=1 -e DELAY_MS=500 attack-cdp-table-flood:latest`) and killed it (SIGKILL) when attackzoo called `docker rm -f`. Windows of 10/20/10 s instead of the default 60/120/60.

Count on the bridge and in attackzoo's pcap by raw BPF and by `tshark -Y cdp`, the same in every run. tcpdump ran as root in the container (attackzoo uses a regular user with `setcap`, `setup.sh:26`); the failure is a compile failure in user space and does not depend on this (the reviewer reproduced it in a `--network none` container, without an attack). Host load from 0.2 to 1.3. A second reviewer redid the dry-run and the compilation of the 17 filters (the 15 of the plan plus the new one for cdp and the new one for the STP ones) with its own scripts and recounted all the pcaps with its own parser that reads the raw pcap; everything matched. From the owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): no new image; campaign script run with a fake docker and in dry-run. Not tested: `-i any` in the host's network namespace; features and dataset after the fix (see Caveats).

**Fix.** One line and one comment: `"net_cdp_table_flood": "not ip and not ip6 and not arp"`. It compiles on `any` (cooked v1 and v2) and on Ethernet [measured]; it keeps the intent of `ae469fb` (keep only the layer 2 flood, without the host's IP traffic). Discarded [measured]: `ether proto 0xaa` (on SLL2 it becomes "protocol == 0xaa" and never matches), `llc` and `ether multicast` (do not compile on SLL2); and removing the entry, which would make the campaign capture without a filter (`run_full_campaign.py:489-490`), the opposite of what `ae469fb` wanted. Outside the commit: warn when tcpdump dies. Today nothing checks the process or the pcap (see Cause); it would be a change in `capture.py`/`experiment.py` that we neither wrote nor measured.

**Before and after.** Same attack, same network, same options; only the tree changes.

| Run | Filter | attackzoo pcap (`-i any`) | CDP in the pcap | CDP on the bridge |
|---|---|---|---|---|
| capture step, before | `ether dst 01:00:0c:cc:cc:cc` | does not exist (tcpdump exits with code 1 in < 1 s) | 0 | 654,699 |
| capture step, after | `not ip and not ip6 and not arp` | SLL2, 633,624 frames | 633,624 (100% of the pcap) | 633,624 |
| campaign, before | old | L0 and L1 do not exist; `status=completed` | 0 | 640,727 |
| campaign, after | new | L1 with 690,238 frames; L0 with 0 frames | 690,238 | 690,238 |

In the campaign after the fix, attackzoo's own report moves to `T7 L1 capture_valid=1 acceptance_pass=1`. L0 stays `capture_valid=0`: without an attack there is no non-IP frame on the isolated network and the pcap stays at 24 B (`stability.py:244` requires more than 24 B); with the old filter on an Ethernet interface the same would happen. In the pcap after the fix every CDP frame has protocol `0x0004` (ETH_P_802_2) in the cooked header. The two campaign runs in the table used `--no-extract-features --no-build-dataset` on both sides, because a pcap of ~690 thousand frames would exceed the 1 GB memory ceiling we gave the container in pandas.

**How to reproduce.** In the reproduction file, section CAMP-01; uses P1, P2, P3, P4, P11.

**Caveats.**
- The new filter is wider than the original: on `-i any` on a real host it keeps every frame that is not IPv4, IPv6 or ARP, from all interfaces (LLDP, BPDU from other bridges, EAPOL and the like), not just the destination `01:00:0c:cc:cc:cc`. We measured only on the isolated network, where the pcap was 100% CDP.
- The after was measured at the capture level (pcap and T6/T7 reports); features and dataset were not run after the fix.
- The published dataset was not generated with this filter: the lines of `contrib/docs/campaign/net_cdp_table_flood.md:25-26` (44.28 MB of PCAP at L0 in 5 runs, 8.82 MB at L1) have been the same since `f835bf5` (2026-07-05), before the campaign had a per-attack filter (`AUTO_BPF_BY_ATTACK` came in with `5aab85b`, 2026-07-13, and the cdp entry with `ae469fb`, 2026-07-17) [read in git]. The finding holds for whoever runs the campaign from HEAD.
- `... or port 8080` in the cdp filter, as in the STP filters, was not measured.
- The STP (CAMP-02) and MLD (CAMP-03) filters are in the same `AUTO_BPF_BY_ATTACK` dictionary; the MLD commit uses the new cdp line as context.

**Versions.** tcpdump `4.99.4-3ubuntu4.24.04.1` and libpcap `1.10.4-4.1ubuntu3.1` (those of `README.md:138` and of Ubuntu 24.04), also checked with tcpdump 4.99.6 / libpcap 1.10.7; sources read: tcpdump tag `tcpdump-4.99.4`, libpcap tag `libpcap-1.10.4` (`104271b`); tshark 4.2.2 in the test environment.

### CAMP-02 · run_full_campaign.py: The 'Stp' Filter Of stp-conf-flood And stp-tcn-flood Never Matches A BPDU On The Default Iface (-I Any With tcpdump >= 4.99): 0 BPDU In The Pcap

| | |
|---|---|
| Class | (a) the code does something other than what it promises, only with tcpdump >= 4.99 on `-i any` |
| In this PR | commit |
| Files | `contrib/scripts/run_full_campaign.py` |
| Depends on | none (written after CAMP-01; alone it applies with a 1-line offset) |

**Promise.**
- `contrib/docs/SCRIPTS.md:27` ("... with PCAPs, features, datasets, telemetry, and per-attack reports.") and `:32` ("Automatically resolves target service, port, probes, and BPF per attack when possible.").
- `contrib/scripts/run_full_campaign.py:4-5`: "keeps raw PCAPs and per-run metadata under experiments/<campaign>/".
- `docker/attackers/stp-conf-flood/README.md:43` and `docker/attackers/stp-tcn-flood/README.md:59`: "Expected artifacts include PCAP files, ..."; `attack.yaml:5` of both: "BPDU (Bridge Protocol Data Unit) packet flood ...".

**What happens.** BPDU is the STP message, the bridge protocol against loops. BPF is tcpdump's capture filter language. On the campaign's default iface (`any`), the filter `"stp or port 8080"` compiles, but the `stp` part never matches a BPDU: the campaign pcap ends up with none of the attack's BPDUs and only the port 8080 traffic [measured]. With the attack sending BPDUs (NET-02 applied), attackzoo's pcap ended up with 24 B (only the file header) and 0 BPDU, against 129,898 configuration BPDUs (stp-conf) and 139,453 TCN (stp-tcn) on the bridge.

**Cause.**
- `contrib/scripts/run_full_campaign.py:65-66`: `"net_stp_conf_flood": "stp or port 8080"` and `"net_stp_tcn_flood": "stp or port 8080"` (`33b0c6c`, 2026-07-17, "Campaign", changed `"stp"` to `"stp or port 8080"`); `:57` `DEFAULT_IFACE = "any"` [read in code].
- On the `any` device tcpdump 4.99 uses Linux's "cooked" v2 header (`DLT_LINUX_SLL2`; tcpdump 4.99.4 `tcpdump.c:1972-1977`). In libpcap 1.10.4, `stp` is `gen_linktype(LLCSAP_8021D)` (`gencode.c:5560-5561`); `gen_linktype` (`:3191`) handles cooked v1 (`DLT_LINUX_SLL`, `:3283-3284`, which tests the 802.2 protocol and the DSAP), but has no case for v2, which falls into the default `:3661-3674` and compares the cooked header's protocol field with the SAP `0x42` [read in code]. The filter listing on `-i any` is `(000) ldh [0]` / `(001) jeq #0x42` in both versions tested [measured]. The kernel delivers the BPDU with protocol `0x0004` (ETH_P_802_2) [measured], so the comparison is never true. libpcap 1.10.5 and the current master (`6e0ef34`) also lack the SLL2 case in `gen_linktype` [read in code].
- The failure is silent: the filter compiles, tcpdump stays alive and the pcap exists; it just does not have the BPDUs. attackzoo's capture also discards tcpdump's stderr (`modules/attackzoo/capture.py:26`) and nobody checks the pcap's content.

**How we tested.** Same arrangement as CAMP-01's capture step: whole upstream tree 8613c66 before and with this commit; documented host environment (Ubuntu 24.04, `tcpdump 4.99.4-3ubuntu4.24.04.1` from `README.md:138`, libpcap 1.10.4) in an `ubuntu:24.04` image; a container on an isolated Docker network (`--internal`) calls `start_tcpdump` (`modules/attackzoo/capture.py`) with the filter from `build_bpf` and `run_full_campaign.py`'s own `DEFAULT_IFACE`, with `-i any` (the container sees eth0 and lo), while the attack runs for 20 s on the same segment. Attacks = `stp-conf-flood` and `stp-tcn-flood` with NET-02 applied (without it yersinia sends 0 to 1 frame), env of the campaign form `-e ACTIVE_S=1 -e NICE_LEVEL=19 -e DURATION_S=20 -e COUNT=1 -e DELAY_MS=2000`, stopped by SIGKILL at 20 s. Ground truth = unfiltered Ethernet capture on the bridge, 0 drops. Count by raw BPF and by tshark field (`stp.type`), the same. `port 8080` part: 3 GETs to `127.0.0.1:8080` captured with `-i any` with the old filter and with the new one. Filter listing (`tcpdump -d`) in tcpdump 4.99.4/libpcap 1.10.4 and in 4.99.6/1.10.7. Dry-run of `run_full_campaign.py` with the fixed tree: compilation of all the filters on `any` and on Ethernet. Runs: one capture step per attack and per tree (4 in total) and one capture of the `port 8080` part with each filter; host load from 0.7 to 1.3 (1-minute average at the start of each capture-step run). A second reviewer redid listings, dry-run and compilation with its own scripts, recounted the pcaps with its own parser (BPDU by LLC `42 42 03` and type) and checked the libpcap lines by downloading the sources again. From the owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): no new image; dry-run. Not tested: the whole campaign for STP; `-i any` in the host's network namespace; features and dataset.

**Fix.** The two lines become `"(not ip and not ip6 and not arp) or port 8080"`, with 1 comment. The `port 8080` part (the HTTP probe) stays the same; the layer 2 part uses the same filter as CDP (CAMP-01), which compiles on cooked v1, v2 and Ethernet. Alternative considered: `llc` or `ether proto` do not work on SLL2 (see CAMP-01). Because it is environment-specific (tcpdump >= 4.99 on `-i any`) and widens the scope of the cdp fix, it went into a separate commit.

**Before and after.** Same attack, same network, same capture code; only the tree changes.

| Run | Filter | attackzoo pcap (`-i any`) | BPDUs in the pcap | BPDUs on the bridge |
|---|---|---|---|---|
| stp-conf, before | `stp or port 8080` | 24 B | 0 | 129,898 (configuration) |
| stp-conf, after | `(not ip and not ip6 and not arp) or port 8080` | SLL2 | 118,884 | 118,884 |
| stp-tcn, before | `stp or port 8080` | 24 B | 0 | 139,453 (TCN) |
| stp-tcn, after | `(not ip and not ip6 and not arp) or port 8080` | SLL2 | 139,021 | 139,021 |
| 3 GETs to 127.0.0.1:8080 | old / new | 37 / 36 frames | all tcp/8080 in both | n/a |

After the fix, all the BPDUs in the pcap have protocol `0x0004` in the cooked header. The difference from 37 to 36 frames in the `port 8080` part is an ACK between runs. In the dry-run with the fixed tree, only the commands of cdp and of the 2 STP ones change (3 of 60) and all the filters compile.

In three reproductions of the stp-conf capture step with the commands of the reproduction file, one of 2026-11-17 and two of 2026-11-18 [measured]: with the new filter, the same BPDUs in the `-i any` pcap and on the bridge (139,997, 24,380 and 142,870); with the old one, 0 in the pcap, with 24 B, against 124,751, 137,733 and 132,536 on the bridge. The flood volume varies from one run to another; the equality with the new filter and the 0 with the old one repeat.

**How to reproduce.** In the reproduction file, section CAMP-02; uses P1, P2, P3, P4, P11.

**Caveats.**
- It depends on the environment: it holds for tcpdump >= 4.99 on `-i any` (cooked v2), which is the tcpdump of `README.md:138`. The root is libpcap's code generator, which still does not handle SLL2 in `gen_linktype`, not even in master. With cooked v1 (old tcpdump) or on an Ethernet interface, `stp` matches.
- The published stp-conf data (`contrib/docs/campaign/net_stp_conf_flood.md:25-26`: L1, the level with attack, with an average of 260,994 rows against 9,599 at L0, without attack) predates this filter: the lines have been the same since `f835bf5` (2026-07-05), and the stp-conf filter came in with `ae469fb` (2026-07-17) [read in git]. It says nothing about the environment; what decides is the capture's link type (caveat above).
- The new filter is wider than `stp`: on `-i any` on a real host it keeps every frame that is not IPv4, IPv6 or ARP from all interfaces (LLDP, CDP, BPDU from other bridges). Measured only on the isolated network.
- The whole campaign was not run for the STP attacks; what was measured is the capture step with attackzoo's code and argv. Features and dataset were not run.
- The MLD commit (CAMP-03) has this commit's lines in the diff context.

**Versions.** tcpdump `4.99.4-3ubuntu4.24.04.1` / libpcap `1.10.4-4.1ubuntu3.1` and tcpdump 4.99.6 / libpcap 1.10.7; sources read: libpcap tags `libpcap-1.10.4` and `libpcap-1.10.5` and master `6e0ef34`, tcpdump tag `tcpdump-4.99.4`.

### CAMP-03 · run_full_campaign.py: The 'icmp6' Filter Of ipv6-mld-flood Drops All The MLD, Which Carries A Hop-by-Hop Header Before The ICMPv6

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `contrib/scripts/run_full_campaign.py` |
| Depends on | CAMP-01 (textual), CAMP-02 (textual): the diff context includes the new cdp and stp lines in the same dictionary |

**Promise.**
- `docker/attackers/ipv6-mld-flood/attack.yaml:5`: "ICMPv6 Multicast Listener Report MLD (131) flood on the local network."
- `docker/attackers/ipv6-mld-flood/README.md:36`: "The available campaign artifacts show completed L1/L2 MLD runs producing roughly 0.7-0.9 GB of raw PCAP data per run" (L1 and L2 are campaign levels with attack); `:58`: "Expected artifacts include PCAP files, probe CSVs, ... under `experiments/`."
- `contrib/docs/SCRIPTS.md:27` ("... with PCAPs, features, datasets, telemetry, and per-attack reports.") and `:32` ("Automatically resolves target service, port, probes, and BPF per attack when possible."); `contrib/scripts/run_full_campaign.py:4-5`.

**What happens.** MLD is the protocol with which an IPv6 host tells routers that it wants to receive a multicast group; the MLD Report is an ICMPv6 type 131 message, and it always goes after a Hop-by-Hop extension header (with the Router Alert option). BPF is tcpdump's capture filter language. The filter the campaign gives the MLD flood, `icmp6`, drops all the MLD: with the flood on the wire, the campaign pcap ended up with 3 frames (the host's own Router Solicitation) and 0 MLD, against 864,077 MLD at the receiver and on the bridge [measured].

**Cause.**
- `contrib/scripts/run_full_campaign.py:62`: `"net_ipv6_mld_flood": "icmp6"` (came in with `5aab85b`, 2026-07-13, the commit that created the `AUTO_BPF_BY_ATTACK` dictionary, with a filter for the protocol itself for dhcp-starvation, MLD and stp-tcn-flood); `build_bpf` (`:482-488`) returns that entry; `:677-680` passes `--iface any --bpf icmp6`; `modules/attackzoo/capture.py:23-25` runs `tcpdump -i any -U -s 0 -w <pcap> icmp6` [read in code].
- The attack runs `flood_mld6 eth0` (`docker/attackers/ipv6-mld-flood/entrypoint.sh:19`), a precompiled thc-ipv6 binary in the repo. In the thc-ipv6 source (`477fa5b`), `flood_mld6.c:86-90` calls `thc_add_hdr_hopbyhop` before `thc_add_icmp6(ICMP6_MLD_REPORT)` [read in code]. On the wire: next-header 0 (Hop-by-Hop), Router Alert, then ICMPv6 131, destination `ff02::2`, group `ff0d::<random>` [measured].
- libpcap 1.10.4: `icmp6` is `gen_proto(58, Q_IPV6)` (`gencode.c:5466-5467`), which only accepts next-header 58 (ICMPv6) or 44 (fragment) followed by 58 (`gencode.c:6506-6518`); the man page says `icmp6` is an abbreviation of `ip6 proto 58` (`pcap-filter.manmisc.in:329-335`) and that `ip6 proto` "does not chase the protocol header chain" (`:328`) [read in code]. With Hop-by-Hop the next-header is 0 and the packet falls to `ret #0` (dropped) [measured in the filter listing].
- It does not depend on the iface: the same `icmp6` applied afterwards to the sender's Ethernet pcap matches 0 of the 864,078 MLD [measured].

**How we tested.** Whole upstream tree 8613c66 (`git archive`) before and with the new filter. Attack = image built from upstream (`ipv6-mld-flood`, which uses the repo's binary), with the env of the campaign form `-e ACTIVE_S=5 -e NICE_LEVEL=10 -e DURATION_S=20`, killed by SIGKILL at 20 s. attackzoo's capture: in a container of its own on the network (the receiver), in the documented host environment (`tcpdump 4.99.4-3ubuntu4.24.04.1` from `README.md:138`, libpcap 1.10.4), calling `start_tcpdump` with the filter from `build_bpf` and `run_full_campaign.py`'s own `DEFAULT_IFACE`; the argv was recorded. Isolated Docker network (`--internal`), recreated on each run, not docker0. Ground truth: unfiltered Ethernet captures on the sender's eth0, on the receiver's eth0 and on the bridge, 0 drops, plus the sender's `tx_packets` counter. Count by raw BPF (`ether[20]=0 and ether[54]=58 and ether[62]=131`) and by `tshark -Y "icmpv6.type == 131 && ipv6.nxt == 0"`, the same; both filters also applied offline to the Ethernet pcaps. Dry-run of `run_full_campaign.py` with both trees and compilation of all the filters on `-i any` and `-i lo`, in tcpdump 4.99.4/libpcap 1.10.4 and in 4.99.6/1.10.7. Host load from 3.1 to 4.3. A second reviewer recounted with its own parser, with tshark 4.6.9 and with libpcap 1.10.7, and checked the libpcap and thc-ipv6 lines by downloading the sources again. From the owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): no new image; capture step and dry-run. Not tested: the whole campaign with the attack hook for MLD (what was measured is the capture step with attackzoo's code and argv); the host's network namespace.

A trap in the test, unrelated to attackzoo: in the sender's own network namespace, `-i any` sees the MLD that thc-ipv6 injects with protocol `0xdd86` in the cooked header, and no IPv6 filter matches it there; that is why attackzoo's capture ran on a receiver, as the host receives over the veth in the campaign.

**Fix.** One line and one comment: `"net_ipv6_mld_flood": "icmp6 or (ip6[6] == 0 and ip6[40] == 58)"`. It keeps everything the old filter caught (all ICMPv6) and adds the ICMPv6 right behind a Hop-by-Hop (byte 6 of IPv6 = 0, byte 40 = 58), which is the MLD; the host's own MLDv2 is also included. It runs in the kernel: 13 instructions, only forward jumps [measured]. Discarded alternative: `ip6 protochain 58`, which follows the header chain but generates a backward jump (`ja`), and the man page warns that this "is not supported by filter engines in the kernel, so this can be somewhat slow, and may cause more packets to be dropped" (`pcap-filter.manmisc.in:364-367`), bad for a flood of ~10^6 frames (not measured). `capture.py:25` passes the filter through `shlex.split`, and the argv with parentheses reaches tcpdump intact [measured].

**Before and after.** Same attack, same capture code; only the filter changes.

| Count | Before (`icmp6`) | After |
|---|---|---|
| MLD leaving the sender (`tx_packets` and pcap) | 864,078 | 951,473 |
| MLD at the receiver and on the bridge | 864,077 | 951,472 |
| attackzoo pcap (`-i any`) | 3 frames (host's Router Solicitation), 0 MLD | 951,475 frames: 951,472 MLD and 3 RS; 102.7 MB |
| filter applied offline to the sender's Ethernet pcap | matches 0 MLD | matches all |

In the dry-run, of the 60 plans only the MLD one changes; the 15 distinct filters of the campaign plus the new one compile on `-i any` and `-i lo`, except the cdp one, which is CAMP-01.

**How to reproduce.** In the reproduction file, section CAMP-03; uses P1, P2, P3, P4, P11.

**Caveats.**
- With the fix the MLD pcap is big again: 102.7 MB for ~5 s of flood here; the MLD README speaks of 0.7 to 0.9 GB per run. The volume follows the flood rate, which depends on the machine: in a repetition of 2026-11-17 on a quiet machine, the bridge carried 1,649,587 MLD in the same ~5 s (168 MB in the filtered Ethernet pcap), 1.7 to 1.9 times that of the table's runs [measured].
- The whole campaign with the attack hook was not run for MLD; we measured the capture step with attackzoo's code and argv.
- The `icmp6` entry came in after the pages of the published campaign (`f835bf5`/`6ca93fb`, 2026-07-05/06); the published MLD PCAP (`contrib/docs/campaign/net_ipv6_mld_flood.md:26`, 3,917.75 MB at L1) did not come from this filter [read in code + inferred]. The finding holds for whoever runs the campaign from HEAD.
- The filters of ipv6-ns-flood and ipv6-ra-flood (`icmp6 and ip6[40] == 135` and `== 134`, `:63-64`) do not have the problem: `flood_solicitate6` and `flood_router6` only add Hop-by-Hop with an option (`-a`, `-H`), and the entrypoints call them without an option; the strings of the repo's binaries confirm it [read in code, not measured].
- This commit's diff has the cdp and stp lines in its context; after CAMP-01 and CAMP-02 it applies cleanly; without them, `git apply` refuses the diff and `patch` applies with fuzz, but `git cherry-pick` applies, by 3-way merge [measured].

**Versions.** tcpdump `4.99.4-3ubuntu4.24.04.1` / libpcap `1.10.4-4.1ubuntu3.1` and tcpdump 4.99.6 / libpcap 1.10.7; tshark 4.6.9 in the recount; thc-ipv6 with source read at commit `477fa5b` (the repo's `flood_mld6` binary is precompiled and was not proven to be from that commit; the traffic was measured).

### CAMP-04 · setup.sh: The Pinned NTLFlowLyzer (86d0102) Does Not Import, And The Campaign Carries On As 'Completed' Without The Flow CSV

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `setup.sh`, `README.md`, `contrib/docs/REPRODUCIBILITY_NOTES.md` |
| Depends on | none |

**Promise.**
- `README.md:148`: "... installs NTLFlowLyzer Project directly from its GitHub repository at commit `86d0102466ea42ba03ddda5c649ac7e533fb25d9` by default."; `:164`: "The validated `.venv` also contains `NTLFlowLyzer==0.1.0`"; `:171`; `contrib/docs/REPRODUCIBILITY_NOTES.md:41`.
- `contrib/docs/CLI.md:460`: `--tools` with default `ntlflowlyzer,tshark,scapy`; `:479`: "| `ntlflowlyzer` | Flow-level CSV | ...".
- `contrib/scripts/run_full_campaign.py:4-6`: "enables feature extraction, dataset generation, ..."; `:1095-1097`: `--feature-tools` with default `ntlflowlyzer,tshark,scapy`, `--extract-features` and `--build-dataset` on; `contrib/docs/SCRIPTS.md:27`.

NTLFlowLyzer is the per-flow (connection) feature extractor that attackzoo uses alongside tshark and scapy, which extract per packet.

**What happens.** In the image built by `./setup.sh dependencies` itself, `ntlflowlyzer -h` exits with code 1: `ImportError: cannot import name 'NLFlowLyzer' from 'NTLFlowLyzer.network_flow_analyzer' ... Did you mean: 'NTLFlowLyzer'?` [measured]. Any import of the package fails. The campaign does not warn: it ends `completed`, with the T7 report (artifact validation, in `modules/attackzoo/reports/stability.py`) at `pass`, T8 (artifact inventory) with 2 of 3 extractors ok, no flow CSV and a dataset with only the per-packet rows from tshark and scapy [measured].

**Cause.**
- `setup.sh:10` pins `NTLFLOWLYZER_REF` to `86d0102466ea42ba03ddda5c649ac7e533fb25d9` when the variable is not passed; `:34-40` clones, checks out that commit and does `pip install .` [read in code].
- NTLFlowLyzer (github.com/ahlashkari/NTLFlowLyzer) at `86d0102`: `NTLFlowLyzer/__init__.py:5` does `from .network_flow_analyzer import NLFlowLyzer`, but `network_flow_analyzer.py:12` defines `class NTLFlowLyzer` [read in code]. The import broke in `942629b` (2024-04-01, "Update the naming.") and was fixed in `36e8824` (2024-04-12), 50 s after `86d0102`; the 9 commits from `942629b` to `86d0102` have the import broken [read in a fresh clone]. It does not depend on the Python version or on dependencies.
- The pin came in with `a8a5b68` (2026-07-14, "Repor rework 10"). In the previous version of `setup.sh` (`98b3dd2`, same day) the setup cloned master without a checkout, and master had been `d99cd53` since 2026-05-28 (with the same code as `6e526d3`, from 2025-06-17; `git diff 6e526d3 d99cd53` only changes the README) [read in code].
- attackzoo swallows the error [read in code]: `modules/features.py:162-179` runs `ntlflowlyzer -c` and returns `ok=False` without raising an exception; `modules/attackzoo/experiment.py:286-303` carries on and builds the dataset; `modules/datasets.py:251` uses only the CSVs that exist; `contrib/scripts/run_full_campaign.py:1002` marks `completed` with code 0; `modules/attackzoo/reports/stability.py:346` passes T7 with 1 extractor ok.

**How we tested.** `ubuntu:24.04` image with `sudo` and `libcap2-bin` (present on a regular Ubuntu, absent from the minimal image) in which we ran attackzoo's own `./setup.sh dependencies`, with `docker-install.sh` swapped for an empty stub, plus a layer with `iproute2` (`run_full_campaign.py:314` calls `ip`); one image per pin (`86d0102` from upstream, `d99cd53` from this commit and `36e8824` as a variant, via the documented `NTLFLOWLYZER_REF` override). The build log shows "HEAD is now at 86d0102" and "Successfully installed NTLFlowLyzer-0.1.0". Python 3.12.3, tcpdump 4.99.4, numpy 2.5.0, pandas 3.0.4, scipy 1.18.0 and dpkt 1.9.8 the same in the three images. Containers with `--network none` and `--cap-add NET_ADMIN` (`setup.sh:26` does `setcap cap_net_raw,cap_net_admin=eip` on tcpdump, and without NET_ADMIN in the container the tcpdump exec gives EPERM). Campaign: `python3 contrib/scripts/run_full_campaign.py --only dos_http_simple --runs 1 --levels L0 --warmup 5 --attack 10 --cooldown 5 --no-start-servers --no-collect-server-stats`, other options at the default (features `ntlflowlyzer,tshark,scapy` and dataset), with a fake `docker` and `python3 -m http.server` on `127.0.0.1:8080` in place of the published `http-server`. Only L0, without the attack hook: NTLFlowLyzer runs the same at any level. 5 runs; host load from 0.2 to 1.3. A second reviewer ran `ntlflowlyzer -h` again on the images, read the metadata, CSVs, datasets and reports with its own script and checked NTLFlowLyzer's history in a fresh clone. From the owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): images built by the repo's own `setup.sh`, one per pin; L0 campaign run. Not tested: the campaign with an attack and real servers; the host without a container.

**Fix.** `setup.sh:10` becomes `d99cd5377faaed53b39450ce262652902501188d`, and the 3 mentions of the commit in the docs (`README.md:148`, `:171` and `REPRODUCIBILITY_NOTES.md:41`) follow. Why `d99cd53`: it was what the unpinned `setup.sh` installed when the campaign was documented and when the pin came in, and it has NTLFlowLyzer's own feature fixes. Measured alternative: `36e8824`, the commit closest to the current pin where the import works; it works, but lacks `944559b` ("Fix and Add Segment-Size-related features") and `9cd73cc` ("Fix some of the fwd/bwd payload bytes features") and generates 323 columns against 347 [measured].

**Before and after.** Same campaign and same tree; only the image changes, generated by the `setup.sh` from before or after.

| Run | Pin | Iface | pcap | `ntlflowlyzer` | Flow CSV | Dataset (rows per source) | Status / T7 / T8 |
|---|---|---|---|---|---|---|---|
| before | `86d0102` | `lo` | Ethernet, 468 packets | code 1, ImportError | does not exist | 936: tshark 468 + scapy 468 | completed / pass / 2 of 3 |
| after | `d99cd53` | `lo` | Ethernet, 480 packets | code 0 | 80 flows x 347 columns | 1,040: ntlflowlyzer 80 + tshark 480 + scapy 480 | completed / pass / 3 of 3 |
| variant | `36e8824` | `lo` | Ethernet, 480 packets | code 0 | 80 flows x 323 columns | 1,040 | completed / pass / 3 of 3 |
| before, default iface | `86d0102` | `any` | SLL2, 468 packets | code 1, ImportError | does not exist | 936 | completed / pass / 2 of 3 |
| after, default iface | `d99cd53` | `any` | SLL2, 468 packets | code 0, 0 flows | 0 B | 936 | completed / pass / 3 of 3 |

The 80 flows come from 40 HTTP probes in the 20 s window, 2 flows per probe. `--iface lo` is a documented option (`run_full_campaign.py:1077`), and `attackzoo.py experiment` already uses `lo` by default (`modules/attackzoo/parser.py:105`). The last row is CAMP-05.

**How to reproduce.** In the reproduction file, section CAMP-04; uses P1, P11.

**Caveats.**
- The pin alone does not bring back the flow CSV in the default campaign: on the `any` iface the capture comes out in SLL2 and NTLFlowLyzer creates 0 flows (CAMP-05, report only). The flow CSV comes back on an Ethernet capture: `attackzoo.py experiment` with the default iface `lo`, or the campaign with `--iface lo` or another Ethernet interface.
- Measured only at level L0 and without an attack; the features themselves were not validated beyond counting flows and columns.
- `d99cd53` is a fixed ref, but NTLFlowLyzer's `pip install -r requirements.txt` does not pin versions (scipy, multipledispatch, dpkt).

**Versions.** NTLFlowLyzer: current pin `86d0102466ea42ba03ddda5c649ac7e533fb25d9` (broken), proposed `d99cd5377faaed53b39450ce262652902501188d`, variant `36e8824`; Python 3.12.3 from Ubuntu 24.04; numpy 2.5.0, pandas 3.0.4, scipy 1.18.0, dpkt 1.9.8; tcpdump `4.99.4-3ubuntu4.24.04.1`.

## Commits: Build And Catalog

### GEN-01 · Build Scripts Of The 7 XRCE Attacks Exit With 0 When The Compilation Or The Clone Fails (Latent Defect)

| | |
|---|---|
| Class | (a) the code does something other than what it promises (latent) |
| In this PR | commit |
| Files | `docker/attackers/xrce-dds-*/install.sh` and `docker/attackers/xrce-dds-*/compile.sh` of the 7 XRCE attacks: discovery-poison, entity-flood, fragment-abuse, malformed-inject, session-hijack, time-desync and udp-dos (14 files) |
| Depends on | none |

**Promise.**
- `README.md:248`: "This builds all server, attacker, and client images, starts target servers, and other elements."
- `attack.yaml:5` of each XRCE attack, e.g. `docker/attackers/xrce-dds-udp-dos/attack.yaml:5`: "UDP packet flood against the XRCE-DDS agent to degrade network or service availability."
- `compile.sh` itself only handles the success path: `compile.sh:17-20` does `gcc ...` and then `if [ $? -eq 0 ]; then chmod +x bin/$attack; fi`.

**What happens.** When the attack's compilation or the clone of a dependency fails, `docker build` finishes successfully and the image comes out without the attack binary; the error only shows up at run time, with exit 127 [measured with an injected failure]. With an invalid line in the `.c`, the 7 upstream builds passed (code 0) with an empty `bin/` and the 7 containers exited with 127 ("timeout: failed to run command '/opt/Micro-XRCE-DDS-Client/bin/attack_<x>': No such file or directory"; in discovery-poison, with `DURATION_S=0`, the 127 comes from bash, `entrypoint.sh:9`). With GitHub unreachable during the build, `install.sh` also finished with 0 and the image came out without Micro-CDR, without the Micro-XRCE-DDS-Client code and without a binary. In `attackzoo.py run` (`docker run --rm -d`, `modules/runners.py:147`) the runner prints "[OK] Container started" (`modules/attackzoo/commands.py:289`) and `--rm` deletes the log; attackzoo's own `check_attack_smoke.py`, which `contrib/docs/SCRIPTS.md:216` says to run after a rebuild, would catch the exit 127 and the "No such file" (`docker run -d` without `--rm` at `:317`, `docker wait` at `:361`, `exited_nonzero` at `:374-376`, "no such file" pattern at `:40`) [read in code]. The gcc or git message stays in the build log; what is missing is for the build to fail. It is latent: today the upstream build passes and the 7 binaries come out identical (md5) to those of images built earlier [measured].

**Cause.**
- `compile.sh:15-22`, the same in the 7 (only the attack name at `:6` changes): without `set -e`, with `if [ -f "${attack}.c" ]` and `if [ $? -eq 0 ]` without an `else`. An `if` whose branch does not run returns 0, the `for` ends with 0 and the Dockerfile's `RUN` passes [read in code + measured].
- `install.sh:1-22`, the same in the 7 except line 16 (the `.c` `cp`): without `set -e`; the last command, `ldconfig` (`:22`), exits with 0 even after `git clone`, `cmake` and `make` fail [read in code + measured].

**How we tested.** Clone of upstream 8613c66. For each of the 7 attacks, 4 builds: upstream; upstream with an injected failure (`int injected_syntax_error = ;` at the end of the `.c`, the rest the same); this commit with the same failure; and this commit without a failure. Network failure simulated only on `xrce-dds-udp-dos`, with `docker build --no-cache --add-host github.com:127.0.0.1`, upstream and fixed (the other 6 `install.sh` are identical except line 16, checked). Binaries extracted from each image and compared by md5. Short run of each image in the README form (`-e DURATION_S=<attack.yaml default>`, arguments `<agent IP> 8888`) against the XRCE agent (`server-xrce-dds-agent`, `udp4 -p 8888`): with the injected failure, 0 IP frames from the attacker in the 7; upstream and fixed without a failure with the same binary. Also `docker run --rm -d` on the image with the failure, as the runner does: code 0 from `docker run`, `die` event with exitCode 127, container and log removed. Host load from 5 to 8 during builds and runs, with other tests; only counts and exit codes count as evidence. A second reviewer reread the 28 build logs, inspected `bin/` and the md5 inside each image, recounted the 21 pcaps with its own tshark and awk (100% the same) and repeated the run in the runner's format. From the owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): build with and without a failure and short run; `check_attack_smoke.py` was not run (we tested its mechanism: `docker run -d` without `--rm`, `docker wait` and `docker logs` on the image with the failure give 127 and "No such file"). No organic failure was observed.

**Fix.** In the 7 `compile.sh`: `set -e` at the top; `gcc` directly, without the `if -f` and the `if $?`; `chmod +x`; and `[ -x bin/$attack ] || { echo "ERROR: bin/$attack was not built" >&2; exit 1; }`. In the 7 `install.sh`: `set -e` at the top. Flags (`DDS_CFLAGS`, `DDS_LIBS`) and `SPECIAL_*` lines untouched; no `attack.yaml`, `.c` or entrypoint touched. We kept the shebang and the file mode.

**Before and after.**

| Case | Before (upstream) | After |
|---|---|---|
| build without a failure | code 0, binary present (x7) | code 0, binary with the same md5 as upstream's and as old images' (x7) |
| build with a broken `.c` | code 0, empty `bin/` (x7) | code 1: "compile.sh ... did not complete successfully: exit code: 1" (x7) |
| running the image with a broken `.c` | exit 127, "No such file or directory" (x7); 0 IP frames from the attacker | there is no image |
| build with GitHub unreachable (udp-dos) | code 0; image without Micro-CDR, without the Client code and without a binary | code 1, "exit code: 128" on the 1st `git clone` |

Runs without a failure, same binary before and after, attacker packets to the agent: malformed-inject 22 / 22 and time-desync 2,040 / 2,040 identical; udp-dos 515,663 / 503,943, entity-flood 1,850 / 2,290, fragment-abuse 7 / 6 and session-hijack 26 / 27 vary with the run time under load; discovery-poison 0 / 0 (it only answers after receiving something). Exit codes the same before and after in all.

**How to reproduce.** In the reproduction file, section GEN-01; uses P1.

**Caveats.**
- Latent defect: the failures were injected (broken `.c`, GitHub unreachable); today the upstream build passes and no organic failure was seen.
- The network failure was simulated only on `xrce-dds-udp-dos`; the other 6 `install.sh` are identical except line 16 [read in code].
- The line `[ -x bin/$attack ] || ...` is redundant with `set -e` (`gcc` or `chmod` already bring the script down); it is harmless and makes the message explicit. It can go, if you prefer.
- `set -e` in `docker/build-images.sh`, so the whole setup stops when a build fails, stays as a suggestion without a patch (GEN-02) [read in code: without it the setup may finish with 0 with a broken XRCE build; not tested].
- The 6 Zenoh attacks do not have this defect: `build.sh:8` discards gcc's stderr (`2>/dev/null`), but the build fails (exit 1), only with "chmod: cannot access" in place of gcc's message [measured on proto-fuzzer]; see GEN-02.

**Versions.** Micro-CDR v2.0.2 (`99672492`) and Micro-XRCE-DDS-Client v3.0.2 (`6884d7bd`), cloned without a pin (they were master on 2026-11-16); base `ubuntu:24.04` (serial 20261110 in the 2026-11-16 build); XRCE agent of the runs: `server-xrce-dds-agent` image built earlier (Agent v3.0.1); Docker 29.6.2.

### GEN-03 · target_services Points To The Wrong Server In web-https-heartbleed And smb-enumerating (Catalog Correction)

| | |
|---|---|
| Class | (b) inconsistency between parts of attackzoo |
| In this PR | commit |
| Files | `docker/attackers/web-https-heartbleed/attack.yaml`, `docker/attackers/web-https-heartbleed/README.md`, `docker/attackers/smb-enumerating/attack.yaml`, `docker/attackers/smb-enumerating/README.md` |
| Depends on | none |

**Promise.** `target_services` is the `attack.yaml` field that says which catalog server the attack runs against.
- `docker/attackers/web-https-heartbleed/attack.yaml:5`: "Heartbleed scanner/exploitation against a vulnerable HTTPS server."; `:9-10`: `target_services: - http-server`; `:27-31`: `target_port` with default 8443.
- `docker/servers/ssl-heartbleed/server.yaml:17`: "Provide a vulnerable HTTPS target for Heartbleed attack validation and observable TLS traffic generation."; `:22-23`: `related_attacks: - web_https_heartbleed`; `:11-14`: `443/tcp`, published as `8443:443`.
- `docker/servers/http-server/server.yaml:8-14`: only `http`, `80/tcp` (published as `8080:80`); its `related_attacks` list does not have heartbleed.
- `docker/attackers/smb-enumerating/attack.yaml:5`: "Enumeration of SMB share directories and vulnerabilities."; `:9-10`: `target_services: - target IP service` (the generic placeholder of 13 `attack.yaml`).
- `docker/servers/smb-server/server.yaml:23`: "Provide an SMB/Samba share for enumeration and benign share-listing traffic."; `:28-29`: `related_attacks: - recon_smb_enum`.
- `contrib/scripts/run_full_campaign.py:95`: `"recon_smb_enum": "smb-server"`; `:97`: `"web_https_heartbleed": "ssl-heartbleed"`. `gerar_campanha_benigna.py:49` and `:51` also link the two attacks to `server-smb-server` and `server-ssl-heartbleed`.

**What happens.** The `attack.yaml` of these two attacks points to a different server from the one that `server.yaml`, the campaign script and the benign generator use [read in code + measured]. In the campaign it has no effect, because the script's `SERVICE_OVERRIDES` wins first (`run_full_campaign.py:352-353`): the dry-run picks `server-ssl-heartbleed` and `server-smb-server` with the current yaml and with the corrected one [measured]. Whoever reads the catalog (the READMEs, the campaign pages) or uses `target_services` without the override lands on `http-server`, which serves neither of the two: calling `resolve_service_id` without `SERVICE_OVERRIDES` on the 60 attacks, only these 2 change, both to `http-server` [measured with attackzoo's code]. Against `http-server` heartbleed does not negotiate TLS (8443 refuses the connection; on 80 Apache answers HTTP 400) and enum4linux-ng gives up (445 and 139 refused) [measured]. Against the right servers both work: 200 of 200 heartbeats returned 16 KB of memory for a request without a payload (148 B non-zero, the rest from the ClientHello itself), and the enumeration listed the shares `public` and `IPC$` [measured].

**Cause.** `docker/attackers/web-https-heartbleed/attack.yaml:10` (`- http-server`) and `docker/attackers/smb-enumerating/attack.yaml:10` (`- target IP service`); the value repeats on two lines of each README (`README.md:15` and `:43` in heartbleed; `:15` and `:42` in smb-enumerating) and in `contrib/docs/campaign/{web_https_heartbleed,recon_smb_enum}.md:14`, whose per-level table, on the same page (`:25-28`), shows the real service (`https`, `smb`) [read in code]. Masked in the campaign by `run_full_campaign.py:95,97` and `:352-353` [read in code]. Only `run_full_campaign.py` reads `target_services` (`:156`, `:275`, `:354`, `:357`, `:498`, `:534`); the CLI, the runner and the UI ignore the field [read in code: `git grep target_services`].

**How we tested.** Without containers: the dry-run of `run_full_campaign.py` (`--dry-run --only recon_smb_enum,web_https_heartbleed`) on the upstream tree 8613c66 and on the corrected one; and the script's own functions (`load_attack_metadata`, `load_server_specs`, `resolve_service_id`) called on the 60 attacks with and without `SERVICE_OVERRIDES`. With containers: servers without `-p` (smb-server with the arguments of `servers.sh:107`); attacks built from upstream in the README's `docker run` form (`<IP> [internal port]`, without `-e`), running until they exit on their own; heartbleed against `ssl-heartbleed` on 443 and against `http-server` on 8443 and on 80; `smb-enumerating` against `smb-server` and against `http-server`. Servers: images built earlier (smb-server and http-server identical to upstream; ssl-heartbleed differs only in the `FROM` pinned by digest). Count with tshark (TLS handshake and heartbeat, HTTP 400, RST, SMB2, srvsvc). A second reviewer redid the dry-run and the resolution with its own script, recounted the pcaps with its own TLS and SMB parser, confirmed that only these 2 of the 60 have a `target_services` different from the server that the `server.yaml` files associate with them, and read in the `http-server` image that Apache only listens on 80 (no SSL module). The images do not change with the commit (the Dockerfiles do not copy the touched files). From the owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): dry-run and loader. Not tested: heartbleed through the published port `127.0.0.1:8443` (docker-proxy, the Docker process that relays that port to the container).

**Fix.** `attack.yaml:10` becomes `ssl-heartbleed` and `smb-server`, and the two lines of each README that repeat the value follow (6 lines in 4 files). No parameter, code or Dockerfile changes. The `:95` and `:97` entries of `SERVICE_OVERRIDES` stay: with the corrected yaml they become redundant, but removing them is not necessary and was not tested. The pages of `contrib/docs/campaign/*.md:14` document the published campaign and stay as they are (suggestion: correct them if they are regenerated).

**Before and after.**

| Measure | Before | After |
|---|---|---|
| `resolve_service_id` without override, on the 60 attacks | 2 diverge: heartbleed and smb-enumerating, both to `http-server` | 0 diverge: `ssl-heartbleed` and `smb-server` |
| campaign dry-run | `server-ssl-heartbleed` and `server-smb-server` | identical |
| `attackzoo.py list --json` | 60 attacks, 7 categories | same |

Traffic against each server (the same attack, without an image change):

| Run | Counts in the pcap | Attack output |
|---|---|---|
| heartbleed against `http-server`:8443 (server from the old yaml, default port) | 200 SYN, 200 RST, 0 TLS | 200x `ConnectionRefusedError` |
| heartbleed against `http-server`:80 | 200 ClientHello, 200 HTTP 400, 0 ServerHello | 200x "Server closed connection without sending Server Hello." |
| heartbleed against `ssl-heartbleed`:443 (server from the corrected yaml) | 200 handshakes; 200 complete heartbeat responses of 16 KB for requests without a payload | 200x "WARNING: server returned more data than it should - server is vulnerable!" |
| smb-enumerating against `http-server` | SYN on 445, 139, 389 and 636: 4 RST; 0 SMB | "Could not connect to SMB on 445/tcp: connection refused"; "Aborting remainder of tests" |
| smb-enumerating against `smb-server` | complete SMB2; NetShareEnumAll returns `public` and `IPC$` | "Found 2 share(s)" |

**How to reproduce.** In the reproduction file, section GEN-03; uses P1, P2, P8, P11.

**Caveats.**
- No effect on the campaign (the script's override wins): it is a catalog correction, of low severity.
- That the published campaign used the right servers is an inference: the current script picks the right server for both (override, present since `a2c7f65`, before the campaign pages), and the published page shows Service `https`/`smb`, consistent with that; the exact command of the published campaign is not in the repo [inferred].
- "Returned 16 KB of memory" is Heartbleed's over-read (0 B sent, 16,384 B declared, 16,384 B returned); only 148 B were non-zero, and they were the rest of the client's own ClientHello. We do not say a secret leaked.
- Heartbleed through the published port `127.0.0.1:8443` (as the campaign calls it, via docker-proxy) was not tested; docker-proxy relays the TCP stream [inferred].

**Versions.** enum4linux-ng `288826f` (1.3.10) in the `smb-enumerating` image; Samba 4.19.9 in `smb-server`; DVWA 1.10 with Apache 2.4.25 in `http-server`; `ssl-heartbleed` on `vulhub/openssl:1.0.1c-with-nginx`.

### GEN-04 · syn-flood And dos-http-slowloris Ignore DURATION_S: BusyBox 'Exec Timeout' Leaves Python As PID 1, Which Discards SIGTERM

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | commit |
| Files | `docker/attackers/syn-flood/entrypoint.sh`, `docker/attackers/dos-http-slowloris/entrypoint.sh` |
| Depends on | none |

**Promise.**
- `modules/loader.py:13-18`: intensity parameter `duration_s`, label "Internal attack duration (s)", default 0, variable `DURATION_S`; both `attack.yaml` files declare `- key: duration_s` (`syn-flood/attack.yaml:30`, `dos-http-slowloris/attack.yaml:29`).
- `contrib/docs/CLI.md:113-118`: `run` accepts `--duration_s`.
- `syn-flood/entrypoint.sh:16-17` and `dos-http-slowloris/entrypoint.sh:11-12`: `if [ "${DURATION_S}" -gt 0 ]; then exec timeout "${DURATION_S}" ...`: the intent of the code is to stop at `DURATION_S`.
- `docker/attackers/syn-flood/attack.yaml:14`: "This attack can generate a large amount of data if captured until its automatic completion. For demonstrations, use less than 5 seconds of execution."

**What happens.** With `DURATION_S` greater than 0 the attack does not stop on time; it only stops when someone from outside removes the container [measured]. With `attackzoo.py run ... --duration_s 10` (no external stop), syn-flood was still running 42 s after the start and sent 1,627 SYNs after the deadline; slowloris sent 300 more `X-a` headers (2 keep-alive rounds) after the deadline. With the web interface's internal duration (5 s) smaller than the "Maximum runtime" (10 s), both only stop at the UI watchdog. The reviewer measured the same with `DURATION_S=5` (syn-flood alive at +21 s, 822 SYNs after the deadline) and with the commands that `check_attack_smoke.py` generates (`DURATION_S=1`, `COUNT=1`): slowloris was still running at +5 s, and syn-flood exited on its own with 0 after sending the single SYN of `COUNT=1`. On the campaign path (`attackzoo.py run --duration W`, which sets `DURATION_S=W` and does `docker rm -f` at the end of W, `modules/attackzoo/commands.py:243-244` and `:291-301`; `run_full_campaign.py:449-456`), the `docker rm -f` at the same instant masks the defect [measured]. With the default `DURATION_S=0` there is no internal limit, before and after.

**Cause.**
- `docker/attackers/syn-flood/entrypoint.sh:17`: `exec timeout "${DURATION_S}" "$@"`; `docker/attackers/dos-http-slowloris/entrypoint.sh:12`: `exec timeout "${DURATION_S}" python3 /slowloris/slowloris.py ...`; `Dockerfile:1` of both: `FROM python:3.11-alpine` [read in code]. In these images `/usr/bin/timeout` is BusyBox 1.37.0 [measured].
- BusyBox 1.37.0, `coreutils/timeout.c:121-135`: `timeout` forks, the child detaches and the grandchild sleeps and then does `kill(parent, signal)`; `:146-157`: the parent does `exec` of the program ("Ok, exec a program as requested") [read in code from the official tarball, sha256 checked; the Alpine 3.24 package has no patch on timeout]. The program inherits the PID of `timeout`, which, through the entrypoint's `exec`, is PID 1 of the container.
- PID 1 of a PID namespace only receives, from other processes in the namespace, the signals for which it installed a handler (Linux v7.0 `kernel/signal.c:94-96`; `pid_namespaces(7)`) [read in code]. Python only installs a SIGINT handler (`SigCgt`, the mask of signals with a handler in `/proc/<pid>/status`, 0x2 [measured]), and `slowloris.py:221` (gkbrk `890f72d`) only handles `KeyboardInterrupt`/`SystemExit` [read in code]. The SIGTERM from the `timeout` grandchild is discarded.
- Scope: only these 2 of the 60 attacks use `exec timeout` (`git grep -nE 'exec[[:space:]]+timeout'`); the other 26 uses of `timeout` are the coreutils one, in `ubuntu:24.04` and without `exec`, which stays as the parent and signals the child [read in code + mechanism measured: `sh -c "exec timeout 3 sleep 60"` with coreutils 9.4 exits with 124 in 3.98 s].

**How we tested.** Images built from upstream 8613c66 and with this commit (BusyBox 1.37.0, scapy 2.8.0, slowloris `890f72d`; the same versions as in the images built earlier). The commands were the ones attackzoo's own `cmd_run` generates, reproduced with the same `-e` flags and arguments: syn-flood `-e DURATION_S=<N> -e COUNT=9999999999 -e RATE_PPS=0 -e DELAY_MS=0 -e PAYLOAD_SIZE=0 <target> 80`; slowloris `-e DURATION_S=<N> <target> 80`. Target = `server-http-server` on port 80. Scenarios: S1, `DURATION_S=10` with no external stop (like `run --duration_s 10`); S2, `DURATION_S=5` and `docker rm -f` at +10 s (UI watchdog); S3, `DURATION_S=10` and `docker rm -f` at +10 s (campaign path); S0, the default. Counting with tshark (attacker SYNs to port 80; for slowloris, SYN, GET and `X-a`), with time relative to `StartedAt`. PID 1 observed at +3 s (`docker top` and `/proc/<pid>/status` from the host). Mechanism isolated with `--network none`: `exec timeout 3 sleep 60` and `exec timeout 3 python3 ...` on BusyBox, the same on coreutils 9.4, and `docker stop -t 5` before and after. Host load from 0.25 to 6.08 (other tests part of the time): it changes the start delay, not the result. A second reviewer recounted the 18 pcaps with their own pcap reader (all the same), checked BusyBox against the official tarball and the kernel, repeated with `DURATION_S=5` and ran the exact commands of `check_attack_smoke.py` (taken from its `--dry-run`) on upstream, on images built earlier and on the fixed one. Not run: the real UI and CLI, because they would put traffic on docker0; we reproduced the `docker run` commands they generate and the same stop.

**Fix.** Minimal patch: `exec timeout` becomes `timeout` on both lines. The entrypoint's `sh` stays as PID 1, the program becomes a child and dies with the SIGTERM from the `timeout` grandchild, and `set -e` makes the `sh` exit with 143. Same `sf.py`, `slowloris.py`, arguments, env and defaults. Alternative not tested end to end: `apk add coreutils` in the Dockerfile, keeping the `exec` (coreutils `timeout` stays as PID 1 and handles SIGTERM; the mechanism was measured: exit 124); it is not the minimum because it changes the Dockerfile, but it would also make `docker stop` work.

**Before and after.** Times since the container's `StartedAt`; "after the deadline" = frames with t > `DURATION_S` + 1 s.

| Scenario | Before (upstream) | After |
|---|---|---|
| S1 syn-flood, `DURATION_S=10`, no stop | running at +42 s; 1,940 SYNs, last at +42.28 s, 1,627 after the deadline | exits on its own with 143, lifetime 11.19 s; 498 SYNs, last at +11.14 s, 7 after the deadline |
| S1 slowloris, `DURATION_S=10`, no stop | running at +42 s; 150 SYN, 150 GET, 450 `X-a` (+3.06 / ~+18 / +33.07 s), 300 `X-a` after the deadline | exits with 143, lifetime 11.51 s; 150 / 150 / 150; 0 after the deadline |
| S2 syn-flood, `DURATION_S=5`, rm at +10 s | only stops at the rm (+11.24 s); 483 SYNs, 286 after the deadline | exits with 143, lifetime 5.93 s; 238 SYNs, 0 after the deadline |
| S2 slowloris, `DURATION_S=5`, rm at +10 s | 150 connections open from +4.32 to +12.40 s | exits with 143, lifetime 6.19 s; connections from +3.22 to +6.18 s |
| S3 (campaign path), rm at +10 s | stops at the rm (last SYN +11.85 s; slowloris closes at +11.66 s) | exits with 143 (11.31 s; slowloris 13.73 s); masked on both sides |
| S0, `DURATION_S=0` | no internal limit | same (the patch does not touch that branch) |
| PID 1 at +3 s | `python3 ...`, `SigCgt` 0x2 | `/bin/sh .../entrypoint.sh` |
| traffic | syn 52 to 58 SYN/s; slowloris 150/150/150 per round | syn 55 to 59 SYN/s; slowloris the same |

With the fix the container exits at `DURATION_S` plus 0.8 to 3.7 s (container start, depending on load) [measured].

**How to reproduce.** In the reproduction file, section GEN-04; uses P1, P2, P8.

**Caveats.**
- With the minimal patch the container exits on its own with 143, and attackzoo's `contrib/scripts/check_attack_smoke.py` goes from PASS to FAIL on both attacks: it uses `DURATION_S=1` by default (`:103`, `:208-211`), waits 5 s (`:509`, `:361`) and treats any exit other than 0 as `exited_nonzero`, failed (`:368-376`) [read in code + measured by the reviewer with the commands the smoke test generates: before exit 0 or still running, after exit 143]. The whole script was not run. Making the timeout path exit 0 would require handling the 143 in the entrypoint and a new measurement; it is not in this commit.
- `docker stop` still gives 137 after the deadline, before and after (`docker stop -t 5`: 6.85 s before and 6.89 s after): the `sh` as PID 1 also ignores SIGTERM. attackzoo does not use `docker stop`, it uses `docker rm -f`.
- We did not reproduce "0 SYNs if the start takes longer than `DURATION_S`": with `DURATION_S=1`, 1 SYN went out.
- SYN rates were measured with other tests on the host; they only serve to show that the traffic does not change. The syn-flood at ~55 SYN/s (one socket per packet) is a separate matter, with no rate promise in attackzoo; it is not in the PR.

**Versions.** BusyBox 1.37.0 (`python:3.11-alpine`, Alpine 3.24, package `busybox 1.37.0-r31`; official tarball sha256 `3311dff3...`); scapy 2.8.0; slowloris `890f72d` (cloned without a pin); coreutils 9.4 (Ubuntu 24.04) in the comparison; host kernel 7.0.0-38-generic.

## Optional Commits: Victims

New servers and clients that give the attack something to hit in the attackzoo scenario. They sit at the end of the
series and can be left out without affecting the fix commits; among them, NET-05 needs NET-04.

### NET-04 · dhcp-starvation: The Scenario Has No DHCP Server To Exhaust (Victim Proposal: dhcp-server)

| | |
|---|---|
| Class | (b) inconsistency between parts of attackzoo |
| In this PR | optional commit (victim) |
| Files | `docker/servers/dhcp-server/Dockerfile`, `docker/servers/dhcp-server/entrypoint.sh`, `docker/servers/dhcp-server/server.yaml`, `docker/servers/dhcp-server/README.md` (new); `servers.sh` (`ALL_SERVER_IMAGES` and start block); `docker/build-images.sh` (build and run after ssl-heartbleed); `docker/README.md` (Target Servers table); `README.md` (Target Servers table, protocol list and server count) |
| Depends on | NET-02 (effect) |

**Promise.**
- `docker/attackers/dhcp-starvation/attack.yaml:5`: "DHCP lease exhaustion on the local network."
- `docker/attackers/dhcp-starvation/attack.yaml:12` (same in `README.md:33`): "Increase count or active_s only after validating host load, DHCP state churn, and capture volume." The text presupposes DHCP state to validate.
- On the other hand, `attack.yaml:11`: "This attack does not require a target and operates at the local network level."

DHCP is the protocol that hands out IP addresses on a network; a lease is the loan of an address to a client; DHCP starvation is exhausting the server's address pool with requests (DISCOVER) from fake MACs.

**What happens.** The attackzoo scenario has no DHCP server [read in code]: `docker/servers/` has 9 servers and `servers.sh:22-32` starts the same 9; none speaks DHCP. On docker0, what gives IPs to the containers is Docker's IPAM, with no DHCP. The only DHCP in the repo is the dnsmasq in `gerar_benigno_infra.py:102-103`, on its own network and only for benign traffic. Even with the traffic fixed (NET-02), the 467,037 DISCOVERs that reached the bridge got 0 replies (no frame with `udp.srcport == 67`) [measured]. There is no lease to exhaust.

**Cause.** Scenario, not attack code: no attackzoo server implements DHCP [read in code]. The campaign pairs dhcp-starvation with `http-server` through the category prefix "2)" (`contrib/scripts/run_full_campaign.py:107-109`).

**How we tested.** Isolated Docker network (`--internal`, bridge with STP off, of the same kind as docker0), with fixed IPs. Attack: image built from upstream 8613c66 (control) and with NET-02, running in the network namespace of an idle container (.20), with the README-style env generated by attackzoo's `cmd_run`: `-e ACTIVE_S=5 -e NICE_LEVEL=10 -e DURATION_S=0 -e COUNT=1 -e DELAY_MS=1000`; wait for the container to exit; t=0 is the attack's `docker run`. New victim (image from this commit) at .10 on every run. To see side effects, a `server-http-server` at .30 and an HTTP probe (`wget` every 0.5 s) at .40. Full-frame capture with no filter in the victim's namespace and in the attacker's, 0 drops. Our own legitimate DHCP client: `busybox` `udhcpc -i eth0 -f -n -q -s /bin/true -t 3 -T 2` (asks for the lease and configures nothing), with a fixed MAC, started at t=-15 s, 1.5 s after the attack start, 2 s after the attack exit, at t=45 s and at t=95 s. Counting with tshark (attack DISCOVER = `dhcp.option.dhcp == 1`, excluding the clients' MACs) and from the udhcpd log. Victim, attack and HTTP server with `--memory 1g`, no OOM. Host load from 1.5 to 7.1 (other tests); the finding rests on counts and state, not on fine timing. A second reviewer recounted the pcaps with their own tshark fields and awk, checked the busybox lines by downloading the source again, and repeated 1 run with the host quieter (load 1.08 at the start and 0.57 at the end): pool exhausted at t=19.6 s, clients without a lease at t=30 and t=50 s, lease back at t=100 s. From the owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `bash -n` on `servers.sh` and `docker/build-images.sh`, and the `server.yaml` read by `run_full_campaign.py`'s own functions. Not tested: the campaign with the victim (it still pairs the attack with `http-server`); the text-only edits to the server README and to the root `README.md` (table row, list and server count), made after the test.

**Fix.** New server `dhcp-server`, in the mold of the existing ones (`FROM ubuntu:24.04`, `RUN apt install ... -y`, `docker run -d --rm --name server-<id>`, `server.yaml` and README with the same sections): busybox udhcpd serving a pool of 10 addresses, `.240` to `.249` of the container's own /24 (on docker0, 172.17.0.240-249; `POOL_START` and `POOL_END` change this), `max_leases 10`, only `eth0`, no published port and no extra capability. Registered in `servers.sh` and `docker/build-images.sh`, so it starts by default, including in the campaign (`run_full_campaign.py:884` calls `servers.sh start`). Why udhcpd [read in code, busybox 1_36_1]: on each OFFER (the address offer) it reserves the address for `offer_time` = 60 s (`networking/udhcp/dhcpd.c:411`, `:774-778`); with no free address it logs "no free IP addresses. OFFER abandoned" (`:771`, `:782`); before offering it does a 2000 ms ARP ping per address (`:249-263`, `:314`, `:872`). Pool of 10: chosen for the default intensity, because with the ARP ping udhcpd makes 1 OFFER every ~2 s and only 9 OFFERs fit in a default run of the attack [measured]. Alternative measured and discarded: dnsmasq 2.91, which requires `--cap-add NET_ADMIN` (without it, it exits with exit 5) and did not exhaust: 228 repeated OFFERs over the 9 free addresses and clients with a lease [measured]. The names `dhcp-server` and `server-dhcp-server` and the pool `.240-.249` are our choice.

**Before and after.** Same network, same victim, same clients; only the attack image changes.

| Measure | Upstream attack + victim | Attack with NET-02 + victim |
|---|---|---|
| attack DISCOVER: attacker side / at the victim | 1 (group origin) / 0 | 766,071 (382,435 of group origin) / 383,636 |
| OFFER to fake MAC | 0 | 9, from t=3.5 to 19.6 s (one every ~2 s) |
| pool addresses reserved | up to 5 of 10 (only the clients) | 10/10 at t=19.65 s; 10/10 until t=60 s; 1/10 at t=80 s |
| "no free IP addresses" in the log | 0 | 216, from t=19.7 to 52.9 s |
| legitimate client (start t: result) | -15.6 / 2.9 / 10.8 / 45.0 / 95.0 s: lease on all 5 | -18.9 lease; 3.0 fail; 13.7 fail; 45.0 fail; 95.0 lease |
| reviewer's repeat | | -13.7 lease; 30 fail; 50 fail; 100 lease |
| HTTP probe on the other server | 291 ok, 0 fail | 294 ok, 0 fail |
| frames the victim sent | 9 OFFER, 5 ARP, 5 ACK | 12 OFFER, 11 ARP, 2 ACK |

The client at t=3.0 failed with the pool still free: in the flood udhcpd serves ~1 DISCOVER every 2 s, and the client's DISCOVER competes with hundreds of thousands.

**How to reproduce.** In the reproduction file, section NET-04; uses P1, P2, P3, P4.

**Caveats.**
- Depends on NET-02 for the volume: with the upstream attack, 0 DISCOVERs reach the victim and 5/5 clients get a lease.
- The effect is temporary: failure measured up to ~60 s and lease again at ~95 s; the reservations last 60 s after each OFFER [read in code from `offer_time`]; the interval between 60 and 95 s was not sampled.
- Measured on a bridge of the same kind as docker0, not on docker0.
- Starting by default (`ALL_SERVER_IMAGES` and `build-images.sh`), it becomes a new host on docker0, visible to arp-scan, ping-sweep and port scanners (not measured). Outside DHCP it stays quiet: it only sends OFFER, ACK and ARP [measured]. Starting by default was our choice; the alternative is to leave it on demand, removing the lines from `servers.sh` and `build-images.sh`.
- The campaign still pairs dhcp-starvation with `http-server` (`run_full_campaign.py:107-109`): without an entry in `SERVICE_OVERRIDES` (`:69-105`), the campaign's server telemetry does not look at the victim. The commit does not touch this.
- Do not send SIGUSR1 to udhcpd during the attack (the way to ask it to write out the leases): in our tests, sampling leases this way every ~1.4 s froze the OFFERs for 58 s with free addresses, because the ARP ping is a 2000 ms `poll` that busybox restarts on every signal (`libbb/safe_poll.c:16-25`) [measured + read in code]. Those runs were discarded, and the server README carries the warning.
- `FROM ubuntu:24.04` and `apt install udhcpd` without a version, like the other servers in the repo; it does not follow the pin suggestion from GEN-02.
- The commit also updates the root `README.md`: DHCP enters the servers' protocol list (`README.md:61`), and the count "60 attackers, 9 servers" (`README.md:240`) becomes 10 servers. At `8613c66` the 9 counts the 9 servers of `ALL_SERVER_IMAGES` (`servers.sh:22-32`), which are the 9 servers of the full profile of `docker/build-images.sh`, the 9 folders of `docker/servers/` and the 9 rows of the Target Servers table in `docker/README.md`; the Zenoh subscriber from ZEN-09 starts on demand, outside `servers.sh` and `docker/build-images.sh`, and is not in the count [read in code]. Text only, done after the test.
- After the test, the server README gained the sections `Related Benign Clients`, `Notes` and the closing sentence of the other servers, and the root table row became "DHCP/udhcpd". Text only: no line of Dockerfile, script or field read at runtime changed.

**Versions.** udhcpd `1:1.36.1-6ubuntu3.1` (busybox 1.36.1; source read at tag `1_36_1`), base `ubuntu:24.04`; test client `busybox:latest` (udhcpc); dnsmasq 2.91 in the discarded alternative.

### NET-05 · cdp-table-flood: Nothing In The Scenario Listens To CDP (Victim Proposal: cdp-listener)

| | |
|---|---|
| Class | suggestion |
| In this PR | optional commit (victim) |
| Files | `docker/servers/cdp-listener/Dockerfile`, `docker/servers/cdp-listener/entrypoint.sh`, `docker/servers/cdp-listener/server.yaml`, `docker/servers/cdp-listener/README.md` (new); `servers.sh` (`ALL_SERVER_IMAGES` and start block); `docker/build-images.sh` (build and run); `docker/README.md` (Target Servers table); `README.md` (Target Servers table, protocol list and server count) |
| Depends on | NET-02 (effect); NET-04 (textual: the rows for the two victims sit side by side in `servers.sh`, `build-images.sh` and in the root `README.md` table, and NET-05 rewrites the server list and count that NET-04 changed in that `README.md`) |

**Promise.**
- `docker/attackers/cdp-table-flood/attack.yaml:5`: "CDP (Cisco Discovery Protocol) table flood on the local network."
- But `attack.yaml:11`: "This attack does not require a target and operates at the local network level.", and `docker/attackers/cdp-table-flood/README.md:37` declares as the launcher's goal "preserving representative CDP flood traffic". That is why we treat the victim as a suggestion, not a defect: "table flood" is the name of the technique (yersinia itself calls the attack "flooding CDP table").

CDP is Cisco's neighbor discovery protocol: each device announces itself by multicast, and whoever listens keeps a table of neighbors. The "table flood" fills that table with fake neighbors.

**What happens.** Nothing in the attackzoo scenario listens to CDP [read in code: none of the 9 servers in `docker/servers/` nor any other component of the repo]. With the traffic fixed (NET-02), the CDP announcements reach everyone on the network and nobody processes them.

**Cause.** Scenario: no attackzoo server keeps a CDP table [read in code]. The campaign pairs cdp-table-flood with `http-server` (`contrib/scripts/run_full_campaign.py:107-109`).

**How we tested.** Same setup as NET-04: isolated Docker network (`--internal`, bridge with STP off, of the same kind as docker0); attack built from upstream 8613c66 (control) and with NET-02, in the network namespace of an idle container (.20), with the README-style env generated by attackzoo's `cmd_run`: `-e ACTIVE_S=5 -e NICE_LEVEL=10 -e DURATION_S=0 -e COUNT=1 -e DELAY_MS=500`; t=0 is the attack's `docker run`. New victim (image from this commit) at .10 on every run; `server-http-server` at .30 and an HTTP probe (`wget` every 0.5 s) at .40. Two legitimate CDP neighbors of ours, from the same image with `lldpd -d -ll -cc -I eth0` (CDPv1 forced, no LLDP): the 1st before the attack, the 2nd 2 s after the attack exit. Table state sampled at ~1 s with `lldpcli` (neighbors and statistics), observed until t=300 s. Full-frame capture with no filter in the victim's namespace and in the attacker's, 0 drops; counting with tshark (`cdp`). Victim, attack and HTTP server with `--memory 1g`, no OOM; host load from 1.5 to 7.1. A second reviewer recounted the pcaps and the state with their own tshark and awk and checked the lldpd lines by downloading the source again; the numbers matched. From the owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `bash -n` on the touched scripts and the `server.yaml` read by `run_full_campaign.py` itself. Not tested: the campaign with the victim; the text-only edits to the server README and to the root `README.md` (table row, list and server count), made after the test.

**Fix.** New server `cdp-listener`, in the mold of the existing ones (`FROM ubuntu:24.04`, `apt install lldpd`, `docker run -d --rm --name server-<id>`, `server.yaml` and README with the same sections): lldpd 1.0.18 receive-only (`-r`), with CDP on (`-c`), on `eth0` (`lldpd -d -r -c -I eth0`); no published port and no extra capability. Registered in `servers.sh` and `docker/build-images.sh`, so it starts by default, including in the campaign (`run_full_campaign.py:884`). Why lldpd [read in code, lldpd 1.0.18]: `-r` sends nothing (`src/daemon/lldpd.c:1619-1620`, `:1917`); `-c` turns on CDPv1/v2 (`:57-60`, `:1978-1987`); it keeps at most 32 neighbors per port and protocol (`src/daemon/lldpd.h:71`, `lldpd.c:1922`) and silently drops a new neighbor beyond the cap (`lldpd.c:636-649`). The log warns "unable to drop privileges, monitor running as root" and carries on [measured]. The names `cdp-listener` and `server-cdp-listener` are our choice.

**Before and after.** Same network, same victim, same neighbors; only the attack image changes.

| Measure | Upstream attack + victim | Attack with NET-02 + victim |
|---|---|---|
| attack CDP: attacker side / at the victim | 0 / 0 | 691,977 (345,971 of group origin) / 346,006 |
| neighbors in the table | at most 2 (the legitimate ones) | 32 (the cap) from t=3.1 s to t=260.5 s: 1 legitimate + 31 fake |
| 2nd legitimate neighbor (start: enters the table) | t=4.3 s: enters at t=7.9 s | t=9.5 s: stays out until t=284.7 s |
| expiry of the fakes | n/a | t=261.6 to 262.7 s (TTL 255 of each fake announcement) |
| frames the victim sent | 0 | 0 |
| HTTP probe on the other server | 641 ok, 0 fail | 646 ok, 0 fail |

lldpd counters [measured]: 346,006 announcements received at t=10.8 s, 32 inserted (the legitimate neighbor, before the attack, and the 31 fakes, during the flood) and 31 expired; the dropped counter stays at 0, because dropping beyond the cap is silent. The legitimate neighbor that was already in the table before the attack stayed in it. The ~275 s block comes from the cap of 32 and the 255 s TTL that yersinia puts on every announcement (`src/cdp.c:315-316`), plus the legitimate neighbor's announcement period (30 s) [read in code + measured].

**How to reproduce.** In the reproduction file, section NET-05; uses P1, P2, P4.

**Caveats.**
- Depends on NET-02: with the upstream attack, 0 CDP announcements from yersinia arrive and the table holds only the legitimate neighbors.
- Measured on a bridge of the same kind as docker0, not on docker0.
- Outside CDP, cdp-listener stays quiet: 0 frames sent [measured]. Starting by default, it becomes a new host on docker0 for arp-scan, ping-sweep and port scanners (not measured). Starting by default was our choice; the alternative is to leave it on demand.
- The campaign still pairs cdp-table-flood with `http-server` (`run_full_campaign.py:107-109`); the commit does not touch `SERVICE_OVERRIDES`.
- `apt install lldpd` without a version, like the other servers; it does not follow the pin suggestion from GEN-02. The Ubuntu package patches (`1.0.18-1ubuntu0.1`) were not read; the behavior was measured.
- This commit was written on top of NET-04: the cdp-listener rows sit next to the dhcp-server ones and use those rows as context. To apply NET-05 without NET-04 the diff has to be regenerated.
- The commit also updates the root `README.md`: CDP enters the servers' protocol list (`README.md:61`), and the server count (`README.md:240` at `8613c66`) goes from 10, with NET-04, to 11. Text only, done after the test.
- After the test, the server README gained the sections `Related Benign Clients`, `Notes` and the closing sentence of the other servers, and the root table row became "CDP/lldpd". Text only.

**Versions.** lldpd 1.0.18 (Ubuntu package `1.0.18-1ubuntu0.1`; source read at tag 1.0.18), base `ubuntu:24.04`; yersinia 0.8.2 in the attack.

### XRCE-11 · Victim Proposal: Benign XRCE Client (client-xrce-dds) For Discovery-Poison And Session-Hijack

| | |
|---|---|
| Class | suggestion |
| In this PR | optional commit (victim) |
| Files | `docker/clients/client-xrce-dds/client.yaml`, `README.md`, `Dockerfile` and `xrce-client.c` (new); `docker/README.md` (one row in the Benign Clients table) |
| Depends on | XRCE-04 (effect), XRCE-05 (effect) |

**Promise.** No attackzoo text promises an XRCE session; these motivate the proposal:
`docker/servers/xrce-dds-agent/server.yaml:17` "Serve as an XRCE-DDS agent for IoT attacks involving discovery,
entities, fragments, sessions, timing, and UDP DoS."; `:30-31` `benign_clients: - client-super:xrce-dds`; `README.md:62`
"Benign clients | `docker/clients/` | Containers that generate benign background traffic."; `client-super/client.yaml:25`
(`xrce-dds`) and `:48` (`xrce-dds-agent`); `client-random/client.yaml:41` "Does not cover XRCE-DDS or Zenoh; use
client-super for those protocols."

**What happens.** attackzoo has no real XRCE client (XRCE-DDS is the version of DDS for small devices: the client
opens a session with an agent and publishes through it). `client-super xrce-dds` sends 20 B (`uxrce_probe_` plus 8
random B) to port 8888 and never opens a session: 5 datagrams, 0 replies from the agent, 0 sessions [measured]. That
is why `discovery-poison` and `session-hijack` have no victim in the attackzoo scenario (XRCE-08, XRCE-10).

**Cause.** `docker/clients/client-super/super-client.py:304-307` (the raw probe); no file outside the 7 XRCE attacks
uses the Client library (`git grep`); `clients.sh` only knows `random` and `super` (`clients.sh:48-55`) [read in code].

**How we tested.**
- New image built on 2026-11-16 from `docker/clients/client-xrce-dds` (context `docker/`, base
  `ubuntu:24.04` resolved that day, Client cloned at tag v3.0.2 = `6884d7b`, 0 gcc warnings); another image with the
  same patch applied to a copy of `8613c66`'s `docker/` gave the same binary (md5 `ca688e8b`).
- Agent: Micro-XRCE-DDS-Agent v3.0.1 (`155cfaaf`), `udp4 -p 8888 -v6`, a new one per run; in the discovery runs,
  with and without `-d 7400`.
- Attacks: `session-hijack` from upstream `8613c66` and with XRCE-05; `discovery-poison` from upstream and with XRCE-04
  (arguments `<attacker IP> 6666`); README form.
- In the discovery runs, default route in each netns through a helper with `NET_ADMIN`; containers with a 1 GB memory
  limit.
- Subscriber for measuring: the official `SubscribeHelloWorld` example (key `0xCCCCDDDD`) from Client v3.0.2, built by
  us; it stays out of the commit.
- Runs: `client-super` (1); client in `publish` with no attack (1); `session-hijack` with the client as the victim, 3
  with upstream and 3 with XRCE-05 (agent, subscriber, client in `publish <agent IP> 8888 0 1000`, attack 8 s later
  with `-e DURATION_S=30`); `discover` with no attack (agent without and with `-d`), with upstream's `discovery-poison`
  (2) and with XRCE-04 (2 without `-d`, 3 with `-d`).
- Counting with tshark and our own XRCE parser; logs of the agent (writes, "session re-established"), of the client
  and of the subscriber.
- Load: load average 3.1 to 6.0, with other tests part of the time.
- Independent review: a second reviewer rechecked all the pcaps and logs with their own export and parser.
- Edits after the review, on 2026-11-17: we removed from the Dockerfile the `-I`/`-L` flags pointing to
  `/usr/local/microcdr-2.0.2`, which does not exist in the image, and the rebuilt binary came out identical (md5
  `ca688e8b`); after that, only text (README and `notes` of `client.yaml` in the mold of attackzoo's clients and the row
  in `docker/README.md`). The final diff applies on its own and together with the rest of the PR on `8613c66`, and with
  the whole PR `attackzoo.py list --json` loads the 60 attacks in 7 categories [measured]. These two edits did not go
  through independent review.
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`, written for attacks):
  `check_attack_smoke.py` does not apply (it is not an attack); no `attack.yaml` changes.
- Not tested: the campaign path (`--network host`), a victim that reconnects, micro-ROS itself and Agent v3.0.2.

**Fix.** Optional commit: a new client in `docker/clients/client-xrce-dds/`, in the mold of the other clients
(`client.yaml`, `README.md`, `Dockerfile` and a 196-line `.c` on top of Client v3.0.2); the README has one extra
section, Related Attacks, which the READMEs of attackzoo's clients do not have [read in code].
- `publish <agent_ip> <agent_port> <count> <interval_ms>`: the official `PublishHelloWorld` example
  (`examples/PublishHelloWorld/main.c:52,69-105,122-135` of Client v3.0.2): key `0xAAAABBBB`, topic
  `HelloWorldTopic`, type `HelloWorld`, reliable stream, one write every `interval_ms`; `count 0` publishes until the
  container stops or the session drops.
- `discover <attempts> <period_ms> <count> <interval_ms>`: GET_INFO to `239.255.0.2:7400`
  (`uxr_discovery_agents_default`) and accepts an agent only if a session opens on it (`uxr_create_session_retries(&session,
  5)`), as micro-ROS does (`rmw_microxrcedds`, `rmw_microxrcedds_c/src/rmw_microros/discovery.c:26-55`); then
  publishes like `publish`.
- Exit 0 = finished, 1 = no agent or no session, 2 = usage, 3 = session lost; stdout is line-buffered (`setvbuf`), so the
  log survives `docker rm -f`.
- Declared choices: name `client-xrce-dds` and folder `clients/` (the client publishes, role `benign-client`); on
  demand, outside `docker/build-images.sh`, `clients.sh` and the agent's `server.yaml` `benign_clients`; the `-d 7400` on
  the agent only documented in the client's README (turning it on changes the server of the 7 XRCE attacks, which we did
  not measure); the key `0xAAAABBBB` on purpose: it is the official example's, so that of a client written from the
  Client's documentation, and it is the first of the 7 keys of `session-hijack` (`attack_session_hijack.c:18`).

**Before and after.** Same network, agent and subscriber; "before" = only what attackzoo has.

| Condition | Before (`client-super xrce-dds`) | After (`client-xrce-dds`) |
|---|---|---|
| No attack | 5 probe datagrams, 0 replies, 0 sessions | session `0xAAAABBBB`, 4 CREATE with STATUS 0x00, 54 writes in the agent log, subscriber receives 53 |
| upstream `session-hijack` (3 runs) | no victim | hijack 3 of 3, 1.8 to 2.2 s after the attack starts; the victim exits with 3; 0 INJECTED in DDS |
| `session-hijack` with XRCE-05 (3 runs) | no victim | hijack 3 of 3, 1.3 to 2.6 s; the victim exits with 3; 100 INJECTED in DDS in each; the subscriber receives 71, 74 and 73 |
| `discover`, agent with `-d 7400`, no attack or with upstream | no discovery | session on the real agent 5.01 s after the first GET_INFO |
| `discover`, agent with `-d 7400`, with XRCE-04 (3 runs) | no discovery | fake offer first, 5 CREATE_CLIENT to the fake, session on the real one at 10.01 s (+5.0 s) |
| `discover`, agent without `-d` (as attackzoo starts it) | no discovery | no agent, with or without the attack; with XRCE-04, 15 CREATE_CLIENT to the fake and 15 s until giving up, instead of 3 s |

After the hijack, the victim's next write does not reach DDS (0 of 6); on the wire (checked in 2 runs), one
WRITE_DATA and 9 HEARTBEAT with no ACKNACK, and the victim reports "session lost" 1.0 to 1.9 s later [measured]. With no attack, the client only adds its own
traffic: 60 frames in ~53 s (7 ARP and 53 UDP to port 8888) in `publish`, 0 frames of another protocol [measured].

**How to reproduce.** In the reproduction file, section XRCE-11; uses P1, P2, P6, P7.

**Caveats.**
- 6 of 6 hijacks, not "always", and the number depends on the key: the victim deliberately uses the first of the
  attack's 7 keys. micro-ROS draws the client key at random (`rmw_microxrcedds`, `rmw_init.c:111-115`) and would not be
  hit [read in code].
- The victim exits when it loses the session (exit 3), like the official example. A victim that reconnects would resume
  the key (Agent `SessionManager.hpp:69-79` in v3.0.1, `:72-82` in v3.0.2; read in code) and would cut off the injection; not tested.
- `discover` mode only finds the real agent when the agent starts with `-d 7400`; without `-d`, as in attackzoo, it
  finds none.
- With a participant created, the agent itself starts announcing it in DDS (RTPS to `239.255.0.1:7400`, plus IGMP),
  as it would with any legitimate XRCE client: it is new traffic, visible to an IDS. Without a participant the agent
  sends no IP frame at all (only 3 gratuitous ARPs).
- In the no-attack run's pcap there are 47 WRITE_DATA, not 54: the capture stopped before the victim did; 54 is the agent's log.
- On the subscriber, the first Hello (id 1) was missing in 5 of 7 runs, including with no attack: it is the reader
  pairing with the newly created datawriter, not an effect of the attack.
- The Dockerfile pins the Client by tag `v3.0.2` and the base by tag `ubuntu:24.04`, not by commit and digest.
- Not tested: campaign path, a victim that reconnects, micro-ROS and Agent v3.0.2.

**Versions.**
- attackzoo `8613c66`; Micro-XRCE-DDS-Client tag v3.0.2 (`6884d7b` inside the image); base
  `ubuntu:24.04` with digest sha256 `73b999393d07f2bf65a40373778a44dc9a6d54ad7718d29247d8ff9413c4d6a8` in the measured build.
- Micro-XRCE-DDS-Agent run: v3.0.1 (`155cfaaf`) with Fast-DDS v3.6.2 (`39303846`) and Fast-CDR v2.2.8
  (`1bc9c919`).
- micro-ROS `rmw_microxrcedds` branch kilted (`9d49b4d`), read only; Docker 29.6.2; tcpdump 4.99.6; tshark 4.6.9.

### ZEN-09 · zenoh-subscriber (New Server): Proposal For A Zenoh Subscriber To Make The Effect Of zenoh-pico-timestamp-mess Observable

| | |
|---|---|
| Class | suggestion |
| In this PR | optional commit (victim) |
| Files | `docker/servers/zenoh-subscriber/Dockerfile`, `docker/servers/zenoh-subscriber/zenoh-subscriber.py`, `docker/servers/zenoh-subscriber/server.yaml`, `docker/servers/zenoh-subscriber/README.md` (new); `docker/README.md` (one row in the servers table) |
| Depends on | ZEN-04 (effect: without it no sample reaches the subscriber) |

**Promise.**
- `docker/attackers/zenoh-pico-timestamp-mess/attack.yaml:5`: "Flood of Zenoh/Zenoh-Pico packets with manipulated timestamps to affect target ordering, expiration, or time logic."; `attack_timestamp_manipulation.c:2-3`: "Sends messages with manipulated timestamps to cause ordering issues".
- `docker/servers/zenoh-router/README.md:3` (= `server.yaml:17`): "Serve as a Zenoh router for Zenoh-Pico attacks against fragmentation, keepalive, memory, fuzzing, sequence, and timestamp behavior."
- The scenario has no Zenoh receiver: `docker/servers/zenoh-router/server.yaml:29-30` only lists `client-super:zenoh`, which only opens and closes a TCP connection (`docker/clients/client-super/super-client.py:296-302`); `docker/clients/client-random/client.yaml:41`: "Does not cover XRCE-DDS or Zenoh". No server or client subscribes to a Zenoh key.

**What happens.** Even with ZEN-04, with nobody subscribing to the key the router decodes each PUT and discards it without looking at the timestamp: 36,328 PUTs on the wire, 0 malformed, 0 log lines about timestamps [measured]. There is nowhere for the promised time and ordering effect to show up.

**Cause.** [read in code, Zenoh 1.7.2] `zenoh/src/net/routing/dispatcher/pubsub.rs:283-284`: `if !route.is_empty() { treat_timestamp!(...)`. With no subscriber the route is empty and the router's time check does not run. With a route, `treat_timestamp` (`pubsub.rs:180-214`) replaces a future timestamp (more than 500 ms ahead) with the router's own and logs an ERROR (`pubsub.rs:198-202`; check and WARN in `uhlc` 0.8.2 `src/lib.rs:289-305`); past and zero pass.

**How we tested.**
- `--memory 1g` on router, attack and subscriber; cgroup CPU and memory of the router and the subscriber every 0.25 s; `docker logs -t` of all.
- Images: router `server-zenoh-router` from `8613c66` (zenohd v1.7.2); subscriber built from this commit; attacks reused from other items, with the `.c` inside each image checked by md5 against upstream + the corresponding commit: `timestamp-mess` from `8613c66` and with ZEN-04, `memory-exhaustion` with ZEN-05, `sequence-exhaustion` with ZEN-03.
- Attack: `-e DURATION_S=10 -e THREADS=4 <image> <IP> 7447`, as `attackzoo.py run` generates; stopped by the entrypoint's `timeout`; subscriber stopped with `docker stop`. Phases: 20 s with the subscriber idle, the attack (~11.3 s), 20 s after.
- Conditions: ZEN-04 without a subscriber; ZEN-04 with a subscriber; control with `timestamp-mess` from `8613c66` and the subscriber; idle (60 s with only the router, subscriber start, 60 s with the subscriber on and idle, `docker stop`); `memory-exhaustion` (ZEN-05) and `sequence-exhaustion` (ZEN-03) with and without the subscriber.
- Counting: we decoded both directions in the pcap (attacker → router and router → subscriber), the router log and the subscriber log (1 line per sample), and counted timestamp inversions in arrival order.
- Runs: 1 per condition. Independent replica of the main condition: the same measurement done earlier with another subscriber (see ZEN-04): 36,249 of 36,249 samples, 14,350 timestamps rewritten, 13,344 inversions.
- Load: load 2.8 to 3.7 (another test was using ~100% of 1 core in the `memory` and `sequence` runs).
- Independent review: a second reviewer decoded both directions on the wire with their own Zenoh parser, recounted the router and subscriber logs and checked the patch application. The numbers matched. As they pointed out: the subscriber is a victim that makes the effect observable, not a fix; what is measured is the router's time check working, not an effect on the time logic; and with `attackzoo/**` the subscriber also receives `memory-exhaustion`.
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): on a tree with the whole PR, the campaign's `load_server_specs` reads the new `server.yaml` and the per-attack server choice does not change (the 6 Zenoh attacks resolve to `zenoh-router` through `SERVICE_OVERRIDES`, `contrib/scripts/run_full_campaign.py:88-93`) [measured without running the campaign]. The README warning about `attackzoo/**`, the Container IP, Related Benign Clients and Notes sections and the row in `docker/README.md` came after the measurements (text only, no rebuild).
- Not tested: reconnection after restarting the router; "expiration"; the subscriber with the ZEN-08 variant.

**Fix (proposal).** A new server, `docker/servers/zenoh-subscriber/`, with new files only:
- `zenoh-subscriber.py` (47 lines): `zenoh-python` 1.7.2 client (same version as the router), client mode, explicit connection to `tcp/<router_ip>:7447`, multicast discovery off; subscribes to `attackzoo/**` by default (arguments `<router_ip> [port] [key_expr]`); prints 1 line per sample (order, arrival time, kind, key, timestamp in NTP64 and in RFC 3339 with the id, size) and the total on `docker stop`.
- `Dockerfile` (4 lines): `FROM python:3.11-slim`, `pip install eclipse-zenoh==1.7.2`.
- `server.yaml` and `README.md` in the mold of `zenoh-router` (role target-server, no ports of its own), with one extra section in the README, Parameters, which no attackzoo server README has [read in code]; row in the servers table of `docker/README.md` with "Started on demand".
- On demand: it does not go into `servers.sh` or `build-images.sh`, unlike attackzoo's other servers. Measured reason: idle, it keeps 1 session with a KEEP_ALIVE in each direction every 2.5 s, 73 frames per minute on TCP/7447, which would show up in the captures of the 6 Zenoh attacks.
- Why in `servers/` and not as an option of `zenoh-router`: the router is the receiver (the victim); an option on the router would change the image or the start of the target for the 6 attacks; and a separate container keeps the router's telemetry apart from the receiver's.
- README warning: with the default key `attackzoo/**`, the router also forwards to the subscriber the samples of `memory-exhaustion` (`attackzoo/memory-exhaustion`, ~64 KB each), which doubles that attack's traffic on TCP/7447; to receive only `timestamp-mess`, pass `attackzoo/timestamp-mess`. The `attackzoo/...` keys are our choice (ZEN-04, ZEN-05).

**Before and after.** Same router, network and arguments; only the presence of the subscriber changes (and the attack image in the control).

| | ZEN-04 without subscriber | control: `timestamp-mess` from 8613c66 + subscriber | ZEN-04 + subscriber |
|---|---|---|---|
| on the wire | 36,328 PUTs decoded, 0 malformed | 34,110 UDP datagrams to 7447, 0 TCP, 17 ICMP | 37,393 PUTs decoded, 0 malformed |
| samples at the subscriber | n/a | 0 | 37,393 (100% of the PUTs), all during the attack |
| stamped by the router (future and maximum refused) | n/a | 0 | 14,933 (7,391 + 7,542, 1:1), at ~0 days from the arrival time |
| with the attacker's id, intact | n/a | 0 | -365 days 7,545, zero (1970) 7,438, now 7,477 |
| timestamp inversions in arrival order | n/a | 0 | 13,668 of 37,393 (10,544 with a jump back of more than 1 day; largest 20,774.1 days) |
| router log during | 0 lines | 0 lines | 29,866 lines, 10.9 MB: 14,933 ERROR "Replace timestamp" + 14,933 WARN from uhlc |
| router clock | n/a | n/a | intact |
| router CPU (qualitative) | 3.6% | 0.0% | 8.0% |
| subscriber | n/a | 0.0% CPU, 14.0 to 14.7 MiB | 14.0% CPU, 16.8 to 18.9 MiB; 5.5 MB log |

With the other attacks fixed, 1 run each: `memory-exhaustion` (ZEN-05) with the subscriber: the router forwards 3,935 of 3,935 batches (Zenoh's unit of sending) to the subscriber (65,021 to 65,024 bytes each, ~256 MB more on TCP/7447; the pcap went from 254 to 513 MB); router memory and log do not change. `sequence-exhaustion` (ZEN-03): 0 samples (FRAME with no message, nothing to route); router CPU the same. Without a router, the subscriber exits with code 1 in a few seconds (~5 s on the test network; the time depends on the network); `docker stop` prints "stopped, N samples received" and exits with 0.

**How to reproduce.** In the reproduction file, section ZEN-09; uses P1, P2, P4, P5.

**Caveats.**
- It is not a fix: it is a victim that makes the effect observable. The attack does not start affecting the router's time logic: what is measured is the router's time check working as designed (refuses and rewrites 100% of the future and maximum values, clock intact), log amplification (2 lines per refused message, ~10.9 MB in ~10 s) and timestamps from 1 year ago and from 1970 arriving intact at the receiver with the attacker's id. No application failure was measured (the subscriber only records).
- "expiration" not measured.
- One run per condition (replica with another subscriber in the ZEN-04 measurement).
- With `attackzoo/**` the subscriber also receives `memory-exhaustion`; only ZEN-05 was measured this way, not the ZEN-08 variant.
- `FROM python:3.11-slim` by tag, without a digest (the measured image had `sha256:07d48240...`).
- Not tested: campaign path, `docker0`, reconnection after restarting the router.

**Versions.** Router: `eclipse/zenoh:1.7.2` (zenohd v1.7.2-790faadb). Subscriber: `python:3.11-slim` (by tag; measured digest `sha256:07d48240...`) + `eclipse-zenoh` 1.7.2. uhlc 0.8.2 on the router. Docker 29.6.2.

## Optional Diffs (Only In The PR Description)

Proposals that do not go into the commits; the diff is in the PR description.

### ZEN-08 · zenoh-pico-memory-exhaustion: Optional Proposal For A Mass-Declaration Variant (DeclareSubscriber) That Makes The Router's Memory Grow

| | |
|---|---|
| Class | suggestion |
| In this PR | optional diff in the description |
| Files | `docker/attackers/zenoh-pico-memory-exhaustion/attack_memory_exhaustion.c` (only in the PR description, not in the commits) |
| Depends on | ZEN-05 (textual: the diff only applies on top of it) |

**Promise.**
- `docker/attackers/zenoh-pico-memory-exhaustion/attack.yaml:5` (same in `README.md:3`): "Memory exhaustion of the Zenoh router/peer through mass creation of resources, sessions, declarations, or pending messages."
- `attack_memory_exhaustion.c:3`: "Sends maximum-size messages to exhaust router memory"; `:141`: "[*] Expected memory pressure: HIGH".

**What happens.** With ZEN-05 the attack reaches the router, but its design (maximum-size PUT) does not make memory rise: the router delivers and frees each message (see ZEN-05). Of the four means the promise lists, we measured which one makes the router's memory grow with the smallest change to the attack: declarations (DeclareSubscriber, the message with which a session tells the router "I want to receive this key"). With the variant, the router [measured]:
- goes to ~100% of one CPU core during the whole attack;
- denies publish and query to the legitimate client that is already connected (put does not arrive, get times out, latency in the range of seconds), which recovers a few seconds after the end; new sessions keep opening;
- has memory that always grows, but ever more slowly: it reached 130.5 MiB at the end of 180 s (13% of the test's 1 GiB cap), still rising ~0.25 MiB/s; the ceiling was not measured. Memory is not exhausted.

**Cause.** [read in code, Zenoh 1.7.2; the `dispatcher/` and `hat/` paths are under `zenoh/src/net/routing/`]
- Why it grows: each DeclareSubscriber makes the router keep state. `declare_subscription` (`zenoh/src/net/routing/dispatcher/pubsub.rs:46`) creates a node in the key tree (`make_resource`, `dispatcher/resource.rs:504`) and `register_simple_subscription` (`hat/router/pubsub.rs:360-385`) stores the subscription in the session. The identifier is `u32` (`commons/zenoh-protocol/src/network/declare.rs:317`; `core/mod.rs:280`) and the state is only released when the declaration is undone or the session closes (`hat/router/mod.rs:502`; `Resource::clean`, `resource.rs:455`); that is why memory goes back to ~3-5 MiB when the session closes.
- Why CPU goes to 100%: each declaration calls `Resource::get_matches` (`dispatcher/pubsub.rs:78-80`), which at node `t<thread>` walks all the children (`dispatcher/resource.rs:799`); since the keys are `.../t<thread>/0, 1, 2, ...`, each declaration walks the N siblings already registered: O(N) cost per declaration. This runs under the tables' read lock (`pubsub.rs:56`, `:78-81`); the write lock only comes afterward, to insert (`:82`). That this cost also slows acceptance, and with it the memory growth, is [inferred].

**How we tested.**
- Same setup as ZEN-05: router `server-zenoh-router` from `8613c66` (zenohd v1.7.2), no arguments, `--memory 1g --memory-swap 1g`; router cgroup every 0.25 s; our own legitimate client (Python, `eclipse-zenoh==1.7.2`) with the sessions opened before the attack, plus a probe that opens a new session on each cycle.
- Attack: `-e DURATION_S=10 -e THREADS=4 <image> <IP> 7447` (and 60 s, 180 s in the long runs). Only the attack image changes: BEFORE = ZEN-05; AFTER = ZEN-05 + this diff. We measured two builds of the variant with the same bytes on the wire: a first one, with leftover code, and this one, clean (wire identical byte for byte on the 4 connections).
- Counting: declarations accepted and acknowledged (ACK) by the router, counted in the pcap by two independent parsers (ours and the reviewer's); memory and CPU from the cgroup; client per phase (before, during the attack container's life, after).
- Runs: 10 s: BEFORE 1, first build 1, this one 1; 60 s: BEFORE 1, first build 1; 180 s: 1 (done by the reviewer, without the legitimate client); 1 run of 2 s with `RUST_LOG=zenoh=debug` and 1 thread to see the router register each declaration. One run per condition.
- Printed-text change, after the measurements above: only the `printf` of each thread's final line changes, from "stopped after sending ..." to "stopped after writing ... to the socket ...". 1 run of 10 s (`THREADS=4`) with the final diff, without the legitimate client or the probe, load 0.37 before and 0.76 after: exit 0 and the new line on the 4 threads (for example, "[*] Thread 3 stopped after writing 58048 subscriber declarations to the socket in 40 batches"); on the wire, the same message types as the earlier builds (FRAME with DeclareSubscriber, 0 FRAGMENT, 0 malformed), and each thread's wire is identical byte for byte to the same thread's in the two earlier builds, up to the end of the shorter one [measured]. In that run the router accepted 34,501 DeclareSubscriber (every attacker byte with an ACK), fewer than the 54,907 and 70,601 of the table's 10 s runs, and the 4 threads wrote 224,406 to the socket [measured].
- Load: load 0.8 to 5.2 depending on the run; 0.37 to 0.76 in the printed-text change run.
- Other means from the promise: DeclareKeyExpr (resources) measured for 10 s; sessions and pending queries only read.
- Independent review: two reviews, each with its own pcap parser and its own cgroup reader; the second checked the assembly of the proposed diff. The numbers and claims in this text are the ones they checked (for example: memory slows down but was not seen to stabilize; the lock is a read lock; client numbers counted in the attack window; the difference between the two builds is run-to-run variation, not load).
- Owner's checklist (`contrib/docs/CATALOG_MAINTENANCE.md:88-104` and `:123-132`): `gcc -Wall -Wextra`: only the warning that already exists ("unused parameter 'sig'").
- Not tested: this variant with the subscriber proposed in ZEN-09; memory ceiling beyond 180 s.

**Fix (proposal, not in the commits).** The diff applies after ZEN-05 and changes only the body of each batch (Zenoh's unit of sending): instead of a maximum-size PUSH/PUT, the batch holds as many DeclareSubscriber as fit (up to `batch_size - 100`), one per Declare message (`0x1e`), each with a distinct entity id and a distinct key under `attackzoo/memory-exhaustion/t<thread>/<n>`. What stays from ZEN-05: TCP, session opening, `send_all`, FRAME with SN per thread, `usleep(10000)`, `THREADS`, `main()`, `attack.yaml`, `entrypoint.sh`, `README.md`, `Dockerfile`. The defines that would be left unused are removed; the header and printed messages now describe the declarations, and each thread's final line says the count is of what was written to the socket ("stopped after writing X subscriber declarations to the socket in N batches"), not of what the router accepted. Why this one: among the four in the promise it is the one that grows with the smallest change and it is distinct on the wire from `zenoh-pico-fragments-reassembly` (0 FRAGMENT; complete FRAMEs with Declare messages). The others:
- resources (DeclareKeyExpr): grows similarly in 10 s (45.4 MiB, 48,190 declarations) but is limited to 65,535 per session (`ExprId = u16`, `commons/zenoh-protocol/src/core/wire_expr.rs:28`; remapping refused, `dispatcher/resource.rs:873-883`) [measured 10 s + read in code];
- sessions: cap `max_sessions = 1000` (`commons/zenoh-config/src/defaults.rs:207`) [read in code; the memory for this, "tens of MiB", is an unmeasured estimate];
- pending queries: with nobody to answer, the router sends the final reply immediately (`dispatcher/queries.rs:440-452`), and the pending ones are limited by the rate times `queries_default_timeout = 10000` ms (`defaults.rs:151`) [read in code].

The key `attackzoo/memory-exhaustion/...` is our choice.

**Before and after.** Same router, network and arguments; only the attack image changes. `THREADS=4`.

10 s:

| | BEFORE (ZEN-05, PUT) | first build (same bytes on the wire) | this version |
|---|---|---|---|
| accepted by the router | 3,850 PUT batches | 70,601 DeclareSubscriber, 100% ACK, 0 FRAGMENT | 54,907 DeclareSubscriber, 100% ACK, 0 FRAGMENT, 0 malformed |
| router memory (max.) | 3.5 MiB | 46.9 MiB (43.6 during the attack container's life) | 54.8 MiB (49.8 during; baseline of this run 8.9 MiB) |
| router CPU | 4.8% | ~100% | ~100% (1 s peak 104%) |
| legitimate client during | 0 failures | 2 of 8 puts lost, 3 of 8 gets failed, up to 1,532.5 ms | 3 of 5 puts lost, 3 of 5 gets failed; new session 7 of 7, with latency up to 3,018.9 ms |

60 s:

| | BEFORE (ZEN-05, PUT) | first build (same bytes on the wire) |
|---|---|---|
| accepted by the router | 23,217 PUT batches | 112,845 DeclareSubscriber, 100% ACK |
| router memory | 3.6 MiB | 97.4 MiB (peak 100.7 after the attacker exited); anon 93.2 MiB; no OOM |
| router CPU | 5.2% | ~95 to 100% |
| legitimate client during | 0 failures | 14 of 22 puts lost, 15 of 22 gets failed, maximum 1,745.7 ms |

180 s (without the legitimate client): 110,049 declarations accepted (53,341 in the first 30 s; then 30 s blocks of 16,496, 7,458, 7,492, 17,804 and 7,458); memory 104.5 MiB at 120 s and 130.5 MiB at 180 s (peak 133.5 after the exit), still rising ~0.25 MiB/s at the end; 490 zero windows (the router is the bottleneck); CPU 99.9%; no OOM. Bytes of memory per accepted declaration, only as a measure: ~645 (10 s, first build), ~876 (10 s, this version, over its own baseline), ~872 (60 s), ~1,150 (180 s). In all of them, memory goes back to ~3-5 MiB when the attacker's session closes. 2 s run with `debug` log: 9,546 lines "Declare subscriber ... (attackzoo/memory-exhaustion/t0/<n>)" from the attacker (plus 1 internal router subscription), 0 decoding errors. In two reproductions with the commands of the reproduction file (memory from `docker stats`) [measured]: at 180 s, 130.3 MiB on 2026-11-18, with a quiet machine, and 119.8 MiB on 2026-11-17, with other tests running (load 6 to 7.5), still rising in both; in the 2 s run with `debug` log, 10,056 and 11,106 lines with "Declare subscriber".

**How to reproduce.** In the reproduction file, section ZEN-08; uses P1, P2, P4, P5.

**Caveats.**
- Memory is not exhausted in what was measured: in the 180 s it reached 13% of the cap and was still rising, slowly; the ceiling was not measured. The growth is also not linear: the rate falls from ~4 MiB/s in the first 5 s to 0.1 to 0.6 MiB/s in the last 60 s of the 180 s run.
- The dominant effect measured is CPU at 100% and denial of publish and query to the legitimate client, plus the growing memory.
- 54,907 against 70,601 declarations in 10 s in the two builds, both with the legitimate client: run-to-run variation with a wire identical byte for byte; cause not isolated (of the two, the 54,907 one was on the quieter host). The printed-text change run, of 2026-11-17, had other conditions (no legitimate client or probe, load 0.37 to 0.76) and gave 34,501, fewer than both [measured]; whether the difference comes from those conditions or from run-to-run variation was not isolated (see "How we tested").
- The number the attack prints counts what was written to the socket, not what the router accepted (247,256 writes against 54,907 accepted in 10 s): the `close` on SIGINT discards what the router has not yet read. That is why each thread's final line says "stopped after writing X subscriber declarations to the socket in N batches"; in the measurements above it said "stopped after sending X subscriber declarations in N batches". The change is only to that text and does not change the wire (see "How we tested").
- One run per condition; the 180 s one without the legitimate client.
- Not tested: campaign path, `docker0`, the variant with ZEN-09's subscriber.

**Versions.** Router: `eclipse/zenoh:1.7.2` (zenohd v1.7.2-790faadb; source read at tag 1.7.2, commit `790faad`). Attack: `ubuntu:24.04` + `build-essential` (no pin, as upstream). Legitimate client: `eclipse-zenoh` 1.7.2 (Python). Docker 29.6.2.

### WEB-07 · idor-path-traversal: Does The Traversal In The URL Path Against An Apache That Normalizes `/../`, So No File Is Read

| | |
|---|---|
| Class | (b) inconsistency between parts of attackzoo |
| In this PR | optional diff in the description |
| Files | `docker/attackers/idor-path-traversal/entrypoint.sh` (optional diff); for the recommended alternative, `docker/attackers/idor-path-traversal/attack.yaml:9-10`, `docker/attackers/idor-path-traversal/README.md:15` and `:43`, `docker/servers/http-server/server.yaml:24`, `contrib/scripts/run_full_campaign.py:98` |
| Depends on | WEB-02 (effect): the optional diff only reads a file once the DVWA database is created (measured) |

**Promise.**
- `docker/attackers/idor-path-traversal/attack.yaml:5`: "Attempts to access local files through the web server using a wordlist." (same in `README.md:3`). Path traversal is using `../` in the requested path to get out of the web server's public folder.
- `attack.yaml:4`: subcategory "3.2 Insecure Direct Object Reference (IDOR)"; `attack.yaml:21`: MITRE T1005 (Data from Local System).
- attackzoo pairs this attack with `http-server`: `attack.yaml:9-10` (`target_services: - http-server`), `docker/servers/http-server/server.yaml:24` (`web_idor_path_traversal` in `related_attacks`) and `contrib/scripts/run_full_campaign.py:98` (the campaign sends it to `http-server`).

**What happens.** [measured] Upstream attack against `http-server` (DVWA), on path A (the flow in the repository root's `README.md:330-335`: `attackzoo.py run` with the server's internal IP and port 80, which becomes `docker run --rm -d --name attack-<folder> <image> <IP> 80` on docker0, `modules/runners.py:147`):
- 570 GETs, one per wordlist line (`LFI-LFISuite-pathtotest.txt`, 570 lines), with the line in the URL path. By line shape: 195 `/../...`, response 400; 113 `/../...%00`, 404; 252 starting with `/` (becomes `//...`), 404; 9 relative or with a Windows drive, 404; 1 empty (`GET /`), 302 to `login.php`.
- `root:x:0:0` (the start of `/etc/passwd`) in 0 responses. `error.log`: 195 lines "AH00126: Invalid URI in request GET /../...". MariaDB general log (the record of every query the database receives): 0 connections. ffuf prints 1 line (the 302 of the empty line).
- Same against the server with the database created (WEB-02).

**Cause.**
- `entrypoint.sh:5`: `/tmp/ffuf -w /tmp/LFI-LFISuite-pathtotest.txt -u http://"${TARGET}:${PORT}/FUZZ" -fc 400`. The wordlist goes in the URL path, so the attack depends on the HTTP server getting out of the web root. That has been the case since the first commit (`28c8d5f`).
- The DVWA Apache (Debian package `2.4.25-3+deb9u5`, `DocumentRoot /var/www/html`) does not get out. Lines from the httpd 2.4.25 tag; the image runs the Debian package with patches on top, and the behavior was measured:
  - `/../x`: `server/request.c:190` calls `ap_getparents(r->uri)`; `server/util.c:524-539` removes the leading `/../` (the index goes negative and returns to 0), and `/../etc/passwd` becomes `etc/passwd`, with no leading `/`; `server/core.c:4507-4510` refuses a URI without a leading `/` with AH00126 and 400 (the 195).
  - `/../x%00`: `server/request.c:175-186` decodes first; `server/util.c:1816-1818` marks the `%00` as a bad path and `:1838-1839` returns 404 (the 113).
  - `//abs`: the path still starts with `/` and is mapped inside `/var/www/html`, where the file does not exist: 404 (the 252).
- In DVWA 1.10, the only point that reads a local file chosen by the client is the file inclusion module: `vulnerabilities/fi/source/low.php:4` (`$file = $_GET[ 'page' ]`) and `vulnerabilities/fi/index.php:35-36` (`include( $file )`), behind a session (`fi/index.php:6`) [read in code]. DVWA has no IDOR module.
- Why (b) and not (a): the code does what the description promises ("Attempts", 570 attempts measured). The inconsistency is that attackzoo pairs the attack with a server whose Apache normalizes `/../` and does not let it out of the root.

**How we tested.**
- Images: `idor-path-traversal` built on 2026-11-16 from the upstream tree at `8613c66` and from the same tree with the optional diff (ffuf 2.1.0, downloaded with a checksum by the `Dockerfile`; the first 3 layers are the same in both). Servers: upstream's and the one with WEB-02.
- Server with no arguments, with `--memory 1536m`; attack with `--memory 1g`. "Ready" when `mysqladmin ping` answers and the Apache pid exists; general log on.
- Path A arguments (root `README.md:330-335`): `<image> <server IP> 80`, no `-e`. All runs exited on their own (6 to 8 s on upstream).
- Capture: from 2 s before to 2 s after.
- Counting: tshark (requests and responses linked by `http.request_in`; responses by code; `http.file_data contains "root:x:0:0"`), classification of each request by the wordlist line's shape, `error.log` (AH00126), general log, ffuf output (sizes).
- Runs: the upstream attack 1 time against each server; the diff 2 times against each server (in the first run the image differed only in a comment), with the same counts. Load: load 0.8 to 1.5 in the upstream runs and 3.5 to 6.0 in the final run (other tests on the host).
- Second independent review: recounted with its own tshark fields and its own TCP reassembly, classified each request by the line's shape, checked that the `request.c`, `util.c` and `core.c` files read are the same as the 2.4.25 tag on GitHub (sha256) and followed the `util.c` loop by hand for `/../etc/passwd`; compared the two attacks' wordlists with `comm`.
- Deviations: general log on.
- Not tested: the recommended alternative; path B (the campaign, `contrib/scripts/run_full_campaign.py`, with `--network host` and target `127.0.0.1:8080`); a server with traversal in the path.

**Fix.** No commit. Two options go in the PR description, for the owner to decide:
- Recommended, not measured: remove `http-server` from this attack's `target_services` (`attack.yaml:9-10` and the `README.md` lines that repeat it, `:15` and `:43`). The pairing also appears in `server.yaml:24` and in `run_full_campaign.py:98` [read in code].
- Labeled suggestion, measured (optional diff): `entrypoint.sh` logs in with `curl` (already installed, `Dockerfile:5`) and runs the same ffuf, same wordlist, same `-fc 400`, with `-b "<PHPSESSID; security>"` and `-u "http://<target>:<port>/vulnerabilities/fi/?page=FUZZ"`. Arguments and `attack.yaml` the same. It changes the vector: from traversal in the URL path (an HTTP server flaw) to file inclusion through a PHP parameter.

**Before and after.** [measured] 2 × 2 matrix with the optional diff, same setup; only the images change:

| attack \ server | upstream server (empty database) | server with WEB-02 |
|---|---|---|
| upstream | 570 GETs: 195 × 400, 374 × 404, 1 × 302; `root:x:0:0` in 0 | same |
| with the optional diff | login POST, 302 `setup.php`; 565 × 302 `../../login.php` and 5 × 400; `root:x:0:0` in 0 | login POST, 302 `index.php`; 570 `GET /vulnerabilities/fi/?page=...`: 565 × 200 and 5 × 400 (the 5 `/Program Files/...` lines, with a space); `root:x:0:0` in 12 responses, all `/etc/passwd`; by response size, 11 with `/etc/group` and 7 with other files [inferred] |

**How to reproduce.** In the reproduction file, section WEB-07; uses P1, P2, P3, P8.

**Caveats.**
- The recommended alternative was not measured, and we do not point to any attackzoo server as the right target for traversal in the URL path [inferred]: removing `http-server` leaves the attack with no declared target.
- The optional diff is not a fix for the attack as written: it changes the vector (URL path to the `page` parameter) and repeats the fixed `php-lfi-enumeration` (WEB-03): same endpoint `vulnerabilities/fi/?page=`, 568 of the 570 wordlist lines are in its wordlist, same subcategory. It changes the tool (ffuf) and the list size, not the target.
- With the diff, `-fc 400` only filters the 5 lines with a space; the hits show up in ffuf among 565 `Status: 200` lines and can only be told apart by size. Only `/etc/passwd` was checked by content; the other files are inferred from size.
- The diff only reads a file with WEB-02 (measured).

**Versions.** ffuf 2.1.0 (pinned with sha256 in the `Dockerfile`); `ubuntu:24.04` resolved to `@sha256:73b99939...` on 2026-11-16; Apache httpd 2.4.25 (Debian package `2.4.25-3+deb9u5`) and DVWA 1.10 in the `vulnerables/web-dvwa` image (pinned in `Dockerfile:1` by the sha256 digest `dae203fe11646a86937bf04db0079adef295f426da68a92b40e3b181f337daa7`); Docker 29.6.2.

## Report Only

Problems measured or read in code for which we do not propose a fix.

### WEB-08 · idor-url-parameter: Fuzzes The `valid_name` Parameter, Which DVWA Does Not Read

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | report only |
| Files | `docker/attackers/idor-url-parameter/entrypoint.sh` |
| Depends on | none |

**Promise.**
- `docker/attackers/idor-url-parameter/attack.yaml:4`: subcategory "3.2 Insecure Direct Object Reference (IDOR)". IDOR, insecure direct object reference, is when the client changes an identifier in the URL and gets back a record that is not theirs.
- `attack.yaml:5`: "Attempts to access resources through URL parameter manipulation using a wordlist." (same in `README.md:3`).
- `attack.yaml:9-10`: `target_services: - http-server`; `docker/servers/http-server/server.yaml:25` lists `web_idor_url_parameter`.

**What happens.** [measured] Upstream attack against `http-server` (DVWA), on path A (the flow in the repository root's `README.md:330-335`: `attackzoo.py run` with the server's internal IP and port 80, which becomes `docker run --rm -d --name attack-<folder> <image> <IP> 80` on docker0, `modules/runners.py:147`):
- 5,965 `GET /login.php?valid_name=<word>`: 5,920 200 responses, all the same login page (1,523 B), and 45 400 responses (words with a space).
- ffuf prints 5,920 lines, all `Status: 200, Size: 1523`.
- MariaDB general log (record of every query the database receives): 11,840 connections and 5,920 `USE dvwa` (the opening of each page), 0 credential queries, 0 queries by `user_id`. `error.log`: nothing new.
- The attack exits on its own in about 9 s. Same against the server with the database created (WEB-02).

**Cause.**
- `entrypoint.sh:5`: `/tmp/ffuf -w /tmp/all-dirs.txt -u http://"${TARGET}:${PORT}"/login.php?valid_name=FUZZ -fc 401`. That has been the case since the repository's first commit (`28c8d5f`), when `servers/http-server/Dockerfile` was already `FROM vulnerables/web-dvwa` [read in git].
- [measured] `grep -rn valid_name /var/www/html` in the server image: 0 lines. `login.php` only reads `Login`, `user_token`, `username` and `password` (`login.php:10-18`); without `Login`, it only shows the form.
- DVWA 1.10 has no IDOR module (the modules in `vulnerabilities/` are brute, captcha, csp, csrf, exec, fi, javascript, sqli, sqli_blind, upload, weak_id, xss_d, xss_r and xss_s). The only GET parameter that picks a database record by id is the `id` in `vulnerabilities/sqli/source/low.php:5-8` (`users.user_id`, with no owner check), behind a session (`vulnerabilities/sqli/index.php:6`) [read in code].

No fix in the PR. We measured a partial fix and decided not to propose it (see Caveats).

**How we tested.**
- Images: `idor-url-parameter` built on 2026-11-16 from the upstream tree at `8613c66` (ffuf 2.1.0, downloaded with a checksum by the `Dockerfile`) and, for the partial fix we do not propose (see Caveats), from the same tree with that fix's `entrypoint.sh` (the first 3 layers are the same in both). Servers: upstream's and the one with WEB-02.
- Server with no arguments, with `--memory 1536m`; attack with `--memory 1g`. "Ready" when `mysqladmin ping` answers and the Apache pid exists; general log on.
- Path A arguments (root `README.md:330-335`): `<image> <server IP> 80`, no `-e`. The attack exited on its own.
- Capture: from 2 s before to 2 s after; about 13,060 frames per run.
- Counting: tshark (requests by path; responses by code; `http.file_data contains "name='user_token'"`), ffuf output, general log.
- Runs: the upstream attack 1 time against each server; the partial fix 1 time against each server (without WEB-02: 5,920 × 302 `../../login.php` and 45 × 400, 0 queries by `user_id`). Load: load 0.6 to 13.8 in the batch (other tests on the host).
- Second independent review: recounted with tshark and its own parsers (identical URI multiset on both servers; 5,920 bodies of 1,523 B with the login form), checked the `grep` on DVWA, the module list and the git history.
- Deviations: general log on.
- Not tested: path B (the campaign, `contrib/scripts/run_full_campaign.py`, with `--network host` and target `127.0.0.1:8080`).

**How to reproduce.** In the reproduction file, section WEB-08; uses P1, P2, P3, P8.

**Caveats.**
- No fix in the PR. We measured a partial fix (login and `?id=FUZZ&Submit=Submit` in `vulnerabilities/sqli`, with WEB-02): 0 to 28 responses with a record (the 5 users) and 5,920 queries by `user_id`. We do not propose it because it uses the same URL as the fixed `sql-injection` (WEB-05), putting two attack classes of the dataset on the same endpoint; only 28 of the 5,965 words (a wordlist of directory names) become a valid `user_id`; and `-fc 401` filters nothing, because DVWA never answers 401.
- Alternatives not tested: a numeric wordlist (changes the attack's wordlist) or removing `http-server` from this attack's `target_services`.

**Versions.** ffuf 2.1.0 (pinned with sha256 in the `Dockerfile`); `ubuntu:24.04` resolved to `@sha256:73b99939...` on 2026-11-16; server `vulnerables/web-dvwa` (pinned in `Dockerfile:1` by the sha256 digest `dae203fe11646a86937bf04db0079adef295f426da68a92b40e3b181f337daa7`; DVWA 1.10, MariaDB); Docker 29.6.2.

### NET-03 · stp-tcn-flood: The README Still Describes Old Defaults (active_s 5, delay_ms 500, "At Most 5 Seconds")

| | |
|---|---|
| Class | (b) inconsistency between parts of attackzoo |
| In this PR | report only |
| Files | `docker/attackers/stp-tcn-flood/README.md` (suggested text, outside the PR) |
| Depends on | none |

**Promise.** `docker/attackers/stp-tcn-flood/README.md:26`: "| `active_s` | `5` | Maximum time spent generating STP TCN flood traffic inside the attack window. |"; `:29`: "| `delay_ms` | `500` | Delay between worker starts. |"; `:37`: "The current defaults start one worker for at most 5 seconds, avoiding the process burst that previously tripped the load kill-switch."

**What happens.** The code uses other defaults [read in code]: `docker/attackers/stp-tcn-flood/attack.yaml:23` `default: 1` (`active_s`) and `:43` `default: 2000` (`delay_ms`); `entrypoint.sh:5` `DELAY_MS="${DELAY_MS:-2000}"` and `:7` `ACTIVE_S="${ACTIVE_S:-1}"`. Whoever reads the README expects up to 5 s of flood per run; the attack runs at most 1 s. The README also does not list `nice_level` (default 19, `attack.yaml:31`). The README's example commands (`:45`, with `--active-s 3 --count 1 --delay-ms 500`, and `:51-53`, with `ACTIVE_S=5` and `DELAY_MS=500`) remain valid, because they pass the values.

**Cause.** Commit `33b0c6c` ("Campaign", 2026-07-17) changed the defaults of stp-conf-flood and stp-tcn-flood from 5 s / 500 ms / nice 10 to 1 s / 2000 ms / nice 19 in `attack.yaml` and `entrypoint.sh`, and did not update the stp-tcn-flood README [read in code: `git show 33b0c6c -- docker/attackers/stp-tcn-flood`].

**How we tested.** Reading only: the stp-tcn-flood `README.md` compared with `attack.yaml`, `entrypoint.sh` and the git history at 8613c66; a second reviewer checked the same lines and the diff of `33b0c6c`. No fix tested: it is only text. The actual defaults (1 s, 2000 ms, nice 19) are the ones that ran in the NET-02 measurements.

**How to reproduce.** In the reproduction file, section NET-03; uses P1.

**Caveats.** Suggested text (not measured, documentation only): `README.md:26` `5` -> `1`; `:29` `500` -> `2000`; `:37` "at most 5 seconds" -> "at most 1 second". Optionally, a line for `nice_level` (default 19). Not verified and outside this item: the old launcher's PCAP volumes cited in `:37` ("approximately 43 GB").

**Versions.** None (text only at 8613c66).

### CAMP-05 · Campaign: On The Default Iface (Any) NTLFlowLyzer Creates 0 Flows And The Empty CSV Counts As An OK Extractor (Report, No Fix)

| | |
|---|---|
| Class | (b) inconsistency between parts of attackzoo |
| In this PR | report only |
| Files | `contrib/scripts/run_full_campaign.py:57`; `modules/features.py:179`; `modules/attackzoo/reports/stability.py:107-113` (no change in the PR) |
| Depends on | CAMP-04 (effect: the problem only shows up once NTLFlowLyzer imports) |

**Promise.** `contrib/docs/CLI.md:479`: "| `ntlflowlyzer` | Flow-level CSV | ..."; `contrib/scripts/run_full_campaign.py:4-6` ("enables feature extraction, dataset generation, ...") and `:1095-1097` (default extractors `ntlflowlyzer,tshark,scapy`).

**What happens.** With NTLFlowLyzer importing (CAMP-04 pin), the campaign on the default iface `any` generates a flow CSV of 0 B: the extractor's output says "Total IP packets: 0 ... 468 packets analyzed and 0 flows created" [measured]. The report counts that extractor as OK (in attackzoo's stability report, `modules/attackzoo/reports/stability.py`: T8, artifact inventory, with 3 of 3 extractors OK; T7, artifact validation, `pass`), even though `features.py` itself marked `ok=False` [measured]. The same campaign with `--iface lo` (Ethernet) gave 80 flows [measured]. The same `any` pcap, rewritten from SLL2 to Ethernet (the cooked header's protocol becoming the ethertype, payload intact), gave 78 flows [measured by the reviewer]. SLL2 is the "cooked" header that tcpdump >= 4.99 uses on the `any` device, in place of Ethernet.

**Cause.**
- `contrib/scripts/run_full_campaign.py:57`: `DEFAULT_IFACE = "any"` (since `a2c7f65`, 2026-06-28, the creation of the script), so the pcap comes out with link type LINUX_SLL2 [read in code + measured with capinfos].
- NTLFlowLyzer `d99cd53`, `network_flow_capturer.py:56` and `:159`: `dpkt.ethernet.Ethernet(buf)` for every packet, without looking at the pcap's link type [read in code]; in an SLL2 pcap no packet becomes IP.
- `modules/features.py:179`: `ok = (rc == 0) and out_csv.exists() and out_csv.stat().st_size > 0` (here `ok=False`), but `modules/attackzoo/reports/stability.py:107-113` counts the extractor as OK if `ok` is true or if the file exists, even empty [read in code].
- `attackzoo.py experiment` uses iface `lo` by default (`modules/attackzoo/parser.py:105`), which gives Ethernet; the problem is in the campaign's default [read in code].

**How we tested.** Same setup as CAMP-04: images built by attackzoo's own `./setup.sh dependencies`, with the `d99cd53` pin; campaign `run_full_campaign.py --only dos_http_simple --runs 1 --levels L0 --warmup 5 --attack 10 --cooldown 5 --no-start-servers --no-collect-server-stats`, other options at their defaults, with a fake `docker` and `python3 -m http.server` on `127.0.0.1:8080`; one run with the default iface (`any`, SLL2 pcap of 468 packets) and another with `--iface lo` (Ethernet, 480 packets). A second reviewer ran NTLFlowLyzer again on the same pcaps and did the SLL2 to Ethernet rewrite. No fix tested.

**How to reproduce.** In the reproduction file, section CAMP-05; uses P1, P11.

**Caveats.** No fix tested. Options, none measured: convert SLL2 to Ethernet before calling NTLFlowLyzer in `features.py`; capture the campaign on an Ethernet interface (changes what goes into the pcap, bad for attacks that use `--network host` on loopback); ask NTLFlowLyzer to respect `pcap.datalink()`; and, separately, `stability.py:107-113` not counting an empty CSV as OK. [inferred, not verified] If the published campaign ran with `-i any` and an NTLFlowLyzer that imports, the "3/3" extractors OK on the campaign pages would be 0 B CSVs; we did not check the published dataset.

**Versions.** NTLFlowLyzer `d99cd5377faaed53b39450ce262652902501188d`; tcpdump `4.99.4-3ubuntu4.24.04.1`; dpkt 1.9.8; Python 3.12.3.

### GEN-02 · Unpinned Builds: Clones, Pip And Base Images Float (Pin Suggestions, No Patch)

| | |
|---|---|
| Class | suggestion |
| In this PR | report only |
| Files | several Dockerfiles and build scripts in `docker/`; `docker/build-images.sh` (no change in the PR) |
| Depends on | none |

**Promise.** There is no promise of a bit-for-bit reproducible build, but the repo already pins versions in several places: `README.md:152`: "`requirements.txt` is frozen with exact versions from the validated `.venv`."; `contrib/docs/REPRODUCIBILITY_NOTES.md:41`: "Python dependencies are pinned in `requirements.txt`. Docker base images that previously used mutable `latest` references are pinned by digest."; `setup.sh:10,36` (NTLFlowLyzer by SHA); ffuf with sha256 in `docker/attackers/idor-path-traversal/Dockerfile:2-3,7` (and in the other 2 Dockerfiles that download ffuf); 3 `FROM` by digest. The suggestion is to extend this to the container builds. A "pin" is fixing a dependency to an exact version (commit, version or digest), so that a build today comes out the same as one from months ago.

**What happens.** A good part of the build floats [read in code, `git grep` on 8613c66]:
- Clones: 20 `git clone` lines in `docker/` (8 repositories), none with a tag or commit: the 7 `attackers/xrce-dds-*/install.sh:4` (Micro-CDR) and `:15` (Micro-XRCE-DDS-Client); `attackers/dos-http-slowloris/Dockerfile:4`; `attackers/mqtt-bruteforce/Dockerfile:3`; `attackers/smb-enumerating/Dockerfile:5` (`--depth 1`); `attackers/sql-injection/Dockerfile:3` (`--depth 1`); `servers/coap-server/Dockerfile:3`; `servers/xrce-dds-agent/agent-source-install.sh:3` (the Agent, built with eProsima's own Dockerfile).
- pip: 16 of the 22 `pip install` lines in `docker/` float (8 `--upgrade pip` and 8 without an exact version, e.g. `attackers/arp-spoof/Dockerfile:5`, `attackers/syn-flood/Dockerfile:5`, `attackers/php-lfi-enumeration/Dockerfile:8`, `servers/coap-server/Dockerfile:7`). `servers/coap-server/requirements.txt` has 8 packages without a version, among them development tools the server does not import (mypy, pytest, coverage, pytest-cov, ruff, pre-commit).
- Base images: 67 of the 70 `FROM` are by tag (48 `ubuntu:24.04`, 14 `python:3.11-alpine`, 2 `python:3.9-alpine`, `eclipse-mosquitto:2`, `eclipse/zenoh:1.7.2`, `vulhub/openssl:1.0.1c-with-nginx`); `ubuntu:24.04`, `python:3.x-alpine` and `eclipse-mosquitto:2` are moving tags. The cloned Agent Dockerfile uses `FROM ubuntu`.
- The SpiderFoot tarball (`attackers/web-wide-scanner/Dockerfile:3`) is the only download without a checksum.
- In the 6 Zenoh attacks, `build.sh:8` compiles with `2>/dev/null`: when gcc fails the build stops (exit 1), but only with "chmod: cannot access", without the cause [measured on proto-fuzzer].
- `docker/build-images.sh` has no `set -e`: without it the setup can finish with 0 even with a broken attack build [read in code, not tested].

Drift already seen on 2026-11-16 [measured in images and read in the repositories]:
- Bases: images built earlier picked up `ubuntu:24.04` serial 20260917 and `python:3.11-alpine` 3.11.17; a build on 2026-11-16 picks up serial 20261110 and 3.11.18; `eclipse-mosquitto:2` also already points to another digest; `python:3.9-alpine` did not move.
- sqlmap: master moved from `1b1f93ae` (2026-10-05, the one in an image built earlier) to `8b78b676` (2026-11-12), 124 commits.
- XRCE Agent: master stayed at v3.0.1 from 2025-03-18 until 2026-09-03 and since then is v3.0.2 (`a88c712b`), 15 commits ahead, among them #392 ("Validate that received MTU...") and #393 ("Catch CDR deserialization exceptions"); master's superbuild also moves Fast-CDR from 2.2.x to 2.3.x and Fast-DDS from 3.x to 3.3.x (`CMakeLists.txt:84,99` in v3.0.1; `:86,101` on master; moving branches in both cases). That #393 changes the response to malformed input, which is what `xrce-dds-malformed-inject` exploits, was not tested.
- XRCE Client and Micro-CDR: master today is the very commit of tags v3.0.2 (`6884d7bd`) and v2.0.2 (`99672492`); the binaries of the 7 XRCE attacks still come out identical to those from images built earlier.
- pip: `--upgrade pip` resolved to 26.2.1; the CoAP server picked up aiocoap 0.4.17, while the CoAP attacks pin 0.4.7; `php-lfi-enumeration` picked up bs4 4.15.0 and requests 2.34.2 (requirements without a version).

One drift changed a result between our measurements [measured]: on 2026-11-17 the `eclipse-mosquitto:2` tag went from mosquitto 2.1.2 to 2.1.4, which stores the password with 20000 PBKDF2 iterations instead of 1000 (`$7$20000$` in the password file that the broker's `Dockerfile` generates at build). With the same `Dockerfile`, the broker started spending about 12 times more CPU per authenticated CONNECT (MQTT-01), and the MQTT-03 fix measured with 2.1.2, without handling the `connect()` failure, lost 633 to 1426 of the 2000 clients in 20 s on 2.1.4 (on 2026-11-17 and 2026-11-18); the MQTT-03 commit now retries the connection. Of the other drifts, we do not claim that any of them changed attack bytes on the wire.

**Cause.** Build choice: clones without a ref, `pip install` without `==` and `FROM` by tag [read in code].

**How we tested.** `git grep` on 8613c66 to count clones, `pip install` and `FROM`; `git ls-remote` and the GitHub API on the third-party repositories on 2026-11-16; `pip freeze`, `/etc/cloud/build.info` and base digests in images built on the test host; registry query without pulling images (`docker buildx imagetools inspect`) for the current digests; proto-fuzzer build with a broken `.c` to see the effect of `2>/dev/null`. A second reviewer redid the counts, the digests, the Agent history (own clone) and the sqlmap one. No fix tested.

**How to reproduce.** In the reproduction file, section GEN-02; uses P1.

**Caveats.** Suggestions, no patch:
- clones by commit, because a tag is a moving ref (Micro-CDR v2.0.2 = `99672492`, Client v3.0.2 = `6884d7bd`). For the Agent, pin the tag or commit and also the superbuild's `_fastcdr_tag`/`_fastdds_tag` and the cloned Dockerfile's `FROM ubuntu`. A `--depth 1` clone does not accept `git checkout <sha>` afterwards ("fatal: reference is not a tree") [measured]; use `git init && git fetch --depth 1 origin <sha> && git checkout FETCH_HEAD` [measured], or a full clone and checkout;
- pip with an exact version per Dockerfile, including transitive dependencies, and not a global lock: there are conflicts between images, for example PyYAML 5.3.1 in `web-wide-scanner` and 6.0.3 in `coap-server`;
- `FROM` by digest and a checksum on the SpiderFoot tarball;
- `set -e` in `docker/build-images.sh` and remove the `2>/dev/null` from the Zenoh `build.sh` files (the XRCE `install.sh`/`compile.sh` are in GEN-01).
The victims proposed in this PR (NET-04, NET-05) and the `curl` of the xss-scanner fix (WEB-06) also install without a version, like the rest of the repo; they do not follow these suggestions.

**Versions.** State on 2026-11-16 (mosquitto's, on 2026-11-17): Micro-CDR v2.0.2 `99672492`; Micro-XRCE-DDS-Client v3.0.2 `6884d7bd`; XRCE Agent master v3.0.2 `a88c712b`; sqlmap master `8b78b676`; CoAPServer master `744cc22`; `eclipse-mosquitto:2` = mosquitto 2.1.4 since 2026-11-17 (`eclipse-mosquitto:2.1.4-alpine@sha256:fa12172a0513...`); ArpSpoof 1.1.2 (latest on PyPI); SpiderFoot v4.0 (tarball sha256 `8b5dac6b...ccf4e`); `ubuntu:24.04` serial 20261110.

## Notes Without A Fix

Minor observations, with no fix tested.

### XRCE-06 · xrce-dds-fragment-abuse: The Script Takes ~77 S And The Default Window Is 30 S

| | |
|---|---|
| Class | (b) inconsistency between parts of attackzoo (low impact) |
| In this PR | note |
| Files | none (no patch); involves `docker/attackers/xrce-dds-fragment-abuse/attack_fragment_abuse.c`, `attack.yaml`, `entrypoint.sh` and `README.md` |
| Depends on | none |

**Promise.** `docker/attackers/xrce-dds-fragment-abuse/attack.yaml:8` `max_runtime_s: 30`; `attack.yaml:29-31`
`duration_s` with default 30; `entrypoint.sh:5-6` `DURATION_S="${DURATION_S:-30}"` and `timeout "${DURATION_S}"`;
`README.md:14` "Suggested max runtime | `30s`". On the other side, the code itself: `attack_fragment_abuse.c:170-171`
"Keeping session alive to maintain fragmentation state..." with `uxr_run_session_time(&session, 60000)`, and `:173-175`
"Attack completed" with `uxr_delete_session`.

**What happens.** With the default window of 30 s, the process is killed during the final wait: exit 124 at 31.2 s, with no session
DELETE on the wire and no "Attack completed" [measured]. Left to run to the end (`DURATION_S=120`), it exits on its own with exit
0 at 76.9 s, sends the DELETE and prints "Attack completed"; with the XRCE-01 fix, 80.4 s [measured]. The impact is
small: only the rest of the keepalive, the DELETE and the final line are lost; with XRCE-01, the attack's traffic fits in ~19 s.

**Cause.** About 16 s of phases (the wait of up to 2 s at `:152` returns in ~0.1 s) plus the 60 s of `:171` against the 30 s of
`attack.yaml` and `entrypoint.sh` [measured; read in code]. `max_runtime_s` is only used by the web interface's watchdog, which does
`docker rm -f` when time runs out (`modules/attackzoo_st.py:163-188`) [read in code]. The campaign passes the attack window as
`--duration` (default 120 s, `contrib/scripts/run_full_campaign.py:53`, `:454-455`), and there the script ends normally
[read in code].

**How we tested.**
- Same setup as XRCE-01: attack image built on 2026-11-16 from the upstream tree `8613c66` (and the XRCE-01 one);
  Micro-XRCE-DDS-Agent v3.0.1 (`155cfaaf`), `udp4 -p 8888`; README form with `-e DURATION_S=30` and
  `-e DURATION_S=120`.
- Duration from `StartedAt` and `FinishedAt` of `docker inspect`; DELETE and "Attack completed" counted in the pcap
  (our XRCE decoder) and in stdout.
- Runs: 2 with 30 s and 1 with 120 s before XRCE-01; 1 with 120 s after; a second reviewer checked the durations,
  the DELETE and the campaign code.
- Not tested: the web interface (the watchdog) and the stop by `docker rm -f`, which would kill with SIGKILL (exit 137).

**No fix tested.** Any fix changes the author's parameter or script; suggestion to the owner: align the 30 s of
`attack.yaml`, `entrypoint.sh` and the README with ~80 s, or shorten the final wait at `:171`.

**How to reproduce.** In the reproduction file, section XRCE-06; uses P1, P2, P6.

**Caveats.**
- One or two runs per condition; the machine was loaded (load 2.2 to 4.5), so the exact seconds may
  vary.
- In BEFORE (without XRCE-01) the attack sends no fragment at all; the note only matters after XRCE-01.

**Versions.**
- attackzoo `8613c66`; Micro-XRCE-DDS-Client v3.0.2 (`6884d7bd`); Micro-CDR v2.0.2 (`99672492`); Micro-XRCE-DDS-Agent
  run v3.0.1 (`155cfaaf`); Docker 29.6.2.

### XRCE-07 · xrce-dds-time-desync: No Message Is Altered On The Wire; The Offset Exists Only In The Attacker's Own Session

| | |
|---|---|
| Class | (a) the code does something other than what it promises, in part |
| In this PR | note |
| Files | none (no patch); the suggested text would touch `docker/attackers/xrce-dds-time-desync/attack.yaml:5`, `README.md:3`, `docker/README.md:77` and `contrib/docs/campaign/iot_xrce_dds_time_desync.md:5` |
| Depends on | none |

**Promise.** `docker/attackers/xrce-dds-time-desync/attack.yaml:5` (repeated in `README.md:3`, `docker/README.md:77` and
`contrib/docs/campaign/iot_xrce_dds_time_desync.md:5`): "Manipulation of XRCE-DDS messages and time-related fields to
induce logical desynchronization between client and agent." `attack.yaml:15-17` maps to TA0040 (Impact), T1565 and
T1565.002 (Transmitted Data Manipulation), repeated in `contrib/docs/MITRE_ATTACK_MAPPING.md:124`.

**What happens.** The attack brings up 20 XRCE sessions (the DDS protocol for small devices) and each one does 100
time syncs (client TIMESTAMP, agent TIMESTAMP_REPLY). The offset exists, but only in the attacker's own memory:
each session's `time_offset` reaches 1 s, and no message is altered [measured]. In the 2000
TIMESTAMPs the clock sent is within 0.07 ms of the frame time (from -0.065 to -0.003 ms), even in the last message
of each session, with the offset already at 990 ms; the agent echoes the client's clock in 2000 of 2000 replies [measured].
A client of ours (same library, default callback) syncing during the attack kept the offset between -73 and
+23 us; alone, between -70 and +19 us [measured]. On a literal reading, "desynchronization between client and agent" happens
in the attacking client's session; what does not happen is the manipulation of messages (nor T1565.002), and the agent and the
other clients are not affected. In the attackzoo flow there is no XRCE client that syncs time: `client-super` and the
campaign probe only send `uxrce_probe_` plus 8 B (`docker/clients/client-super/super-client.py:304-308`,
`modules/attackzoo/probes.py:331-341`) [read in code].

**Cause.** `attack_time_desync.c:28-29` (`malicious_offset += 10000000; session->time_offset = malicious_offset;`) sits
in the callback `:14-33`, registered at `:54`; each of the 20 children (`:10`, `:86-97`) has its own session (`:44-46`, key
`0x71E00000 + client_id`) and does 100 `uxr_sync_session` every 100 ms (`:57-59`) [read in code]. In Micro-XRCE-DDS-Client v3.0.2
(`6884d7bd`), the TIMESTAMP carries the raw clock, `uxr_nanos()` (`src/c/core/session/session.c:540-543`); `time_offset`
only enters `uxr_epoch_nanos` and `uxr_epoch_millis` (`:553-563`), which the attack does not call [read in code]. In Agent v3.0.1,
`src/cpp/processor/Processor.cpp:723-760` reads the clock, copies the client's and replies, keeping no state (same in
v3.0.2, `:730-767`) [read in code].

**How we tested.**
- Attack image built on 2026-11-16 from the upstream tree `8613c66` (Client `6884d7bd` = v3.0.2, same binary as
  an earlier build of ours with Client and Micro-CDR pinned to those commits); Micro-XRCE-DDS-Agent v3.0.1 (`155cfaaf`),
  `udp4 -p 8888 -v6`, a new one per case.
- IPs: agent `.10`, attacker `.20`, our client `.30`; README form with `-e DURATION_S=30`; the attack ends
  on its own in ~12.6 s.
- Our client: same library, default callback, 30 syncs every 400 ms, alone and during the attack.
- Our decoder that reads the clock of each TIMESTAMP and compares it with the frame time.
- Load: load average 0.5 to 1.0, with no flood.
- Independent review: a second reviewer recounted the 5 pcaps of the test, shared by XRCE-03 and XRCE-07 (BEFORE, AFTER,
  unit program, our client alone and during the attack), with tshark and their own parser, confirmed that there is no
  drift between the 1st and the 100th message of each session and read the Client inside the image and the Agent's v3.0.1 and v3.0.2 tags.
- Not tested: campaign path (`--network host`) and Agent v3.0.2 running; the cause is local to the attacker
  [inferred].

**No fix tested.** Creating a real victim would be a different attack (forging TIMESTAMP_REPLY on the agent's behalf
against a client that is syncing, with the victim's IP and port as new parameters), and stamping the TIMESTAMP with
the offset would not affect anyone either, because the agent only echoes. Text suggestion to the owner, only a suggestion: describe
it as "Repeated XRCE-DDS time synchronization (TIMESTAMP/TIMESTAMP_REPLY) from 20 parallel client sessions, about 10
messages/s per session (about 200/s at peak). The offset is changed only inside the sessions of the attacker itself; the
agent keeps no time state." in the 4 places of the Promise, and review T1565.002 (no transmitted data is altered); if
MITRE changes, also update `contrib/docs/MITRE_ATTACK_MAPPING.md`.

**How to reproduce.** In the reproduction file, section XRCE-07; uses P1, P2, P3, P6.

**Caveats.**
- The client that shows "no effect on third parties" is ours, not attackzoo's (attackzoo has no client that
  syncs time).
- Not tested: campaign path and Agent v3.0.2 running.

**Versions.**
- attackzoo `8613c66`; Micro-XRCE-DDS-Client v3.0.2 (`6884d7bd`); Micro-CDR v2.0.2 (`99672492`); Micro-XRCE-DDS-Agent
  run v3.0.1 (`155cfaaf`), read v3.0.2 (`a88c712b`); Docker 29.6.2; tcpdump 4.99.6; tshark 4.6.9.

### XRCE-08 · xrce-dds-discovery-poison: In The attackzoo Scenario No Client Does XRCE Discovery, So The Attack Has Nothing To Poison

| | |
|---|---|
| Class | (b) inconsistency between parts of attackzoo |
| In this PR | note |
| Files | none (no patch); involves `docker/clients/client-super/super-client.py`, `docker/servers/xrce-dds-agent/server.yaml`, `servers.sh` and `docker/build-images.sh` |
| Depends on | none |

**Promise.** `docker/servers/xrce-dds-agent/server.yaml:17`: "Serve as an XRCE-DDS agent for IoT attacks involving
discovery, entities, fragments, sessions, timing, and UDP DoS."; `:23` lists `iot_xrce_dds_discovery_poison`; `:30-31`
gives `client-super:xrce-dds` as the benign client. The attack promises "Poisoning or manipulation of XRCE-DDS agent
discovery messages to induce incorrect association, redirection, or discovery degradation."
(`docker/attackers/xrce-dds-discovery-poison/attack.yaml:5`).

**What happens.** The attack only transmits after receiving an XRCE discovery request (GET_INFO, which the client sends
to find an agent), and in the attackzoo scenario nobody sends one: with the agent as attackzoo starts it (`udp4 -p 8888`, without
`-d`) and `client-super xrce-dds`, the attacker sent 0 UDP datagrams in 60 s, before and after the XRCE-04 fix
[measured]. `client-super` only sends `uxrce_probe_` plus 8 random B to port 8888 (20 datagrams in the test), and the agent
does not reply [measured]. No file in the repository does XRCE discovery (`git grep` for `7400`, `239.255.0.2` and
`uxr_discovery` in `.py`, `.c`, `.sh`, `.yaml` and `.h` only finds the attack itself) [read in code].

**Cause.** `docker/clients/client-super/super-client.py:304-307` (the raw probe) and `:359` (port 8888);
`modules/attackzoo/probes.py:331-341` (the campaign probe does the same); the agent starts without `-d` in `servers.sh:116`,
`docker/build-images.sh:69` and `server.yaml:15`, and its log does not have the discovery server line [read in code; measured].

**How we tested.**
- Attack image built on 2026-11-16 from the upstream tree `8613c66` and the one with XRCE-04; `client-super` as it is at
  `8613c66`; Micro-XRCE-DDS-Agent v3.0.1 (`155cfaaf`) with `udp4 -p 8888`.
- In each netns, a default route put in place by a helper with `NET_ADMIN`, to imitate `docker0`; `client-super xrce-dds
  <agent IP> 8888 30 2 60`; attack with `-e DURATION_S=60` and arguments `<agent IP> 8888` (since the attack
  receives nothing, the arguments do not change the result).
- `tcpdump -s 0` capture on the bridge and on the attacker's `eth0`, no filter, 0 drops; counting with our parser and tshark;
  `/proc/net/udp` and `/proc/net/igmp` of the attacker's netns; agent log.
- One run per image; a second reviewer recounted the pcaps with their own parser and redid the `git grep`.

**No fix tested.** Suggestion to the owner: document that the attack only acts if some client does XRCE discovery, and
no client in the repository does; the optional commit XRCE-11 proposes one. The `-d` on the agent is not a requirement of the attack: without
it, the attacker is the only one that answers discovery; with it, there is a race (the attacker won by 17 to 222 us in the 3
attempts) [measured]. The `-d` is only needed for a legitimate discovery to exist to be diverted.

**How to reproduce.** In the reproduction file, section XRCE-08; uses P1, P2, P3, P6.

**Caveats.**
- On the campaign path we only read the code.
- The client proposed in XRCE-11, in `discover` mode, only finds the real agent when the agent starts with `-d 7400`; without `-d`
  (as attackzoo starts it), it finds no agent at all, with or without the attack [measured].

**Versions.**
- attackzoo `8613c66`; Micro-XRCE-DDS-Client v3.0.2 (`6884d7b`); Micro-XRCE-DDS-Agent run v3.0.1 (`155cfaaf`);
  Docker 29.6.2; tcpdump 4.99.6; tshark 4.6.9.

### XRCE-09 · xrce-dds-discovery-poison: The Rogue Agent Answers RTPS To CREATE_CLIENT, So The Redirection Stops At The Handshake And No Session Opens

| | |
|---|---|
| Class | (a) the code does something other than what it promises (latent: only shows up with XRCE-04) |
| In this PR | note |
| Files | none (no patch); involves `docker/attackers/xrce-dds-discovery-poison/attack_discovery_poison.c` |
| Depends on | XRCE-04 (effect) |

**Promise.** `docker/attackers/xrce-dds-discovery-poison/attack.yaml:5`: "... to induce incorrect association,
redirection, or discovery degradation."; usage printed at `attack_discovery_poison.c:320-321`: "2. Redirect clients to
rogue agent at <ip>:<rogue_agent_port>", "3. Intercept all client communications".

**What happens.** With XRCE-04 applied, the XRCE client (a DDS protocol for small devices) receives the rogue agent's
offer and tries to open a session with it: the handshake is redirected. But the rogue agent answers every CREATE_CLIENT
(the session-opening request) with 12 B of RTPS (the DDS wire protocol, a different format), which never becomes
STATUS_AGENT, and no session opens [measured]. With the client proposed in XRCE-11 (which only accepts an agent if the
session opens, like micro-ROS): 5 CREATE_CLIENT to the rogue agent per offer (15 "Intercepted 24 bytes" in the attack
log in a run of 3 offers), 0 sessions with the rogue agent in 5 of 5 runs, and no topic data intercepted [measured].
Effect that can be attributed to the attack [measured]:
- with the real agent on `-d 7400`: +5.0 s per rogue offer (session on the real agent 10.01 s after the first GET_INFO,
  versus 5.01 s without the attack), 3 of 3 runs;
- with the agent without `-d` (as attackzoo starts it): 15 CREATE_CLIENT to the rogue agent and 15 s until giving up,
  instead of 3 s; the outcome is the same as without the attack (without `-d` the client finds no agent at all).

A client that accepts the first offered agent without validating (our program) sent 10 CREATE_CLIENT, received 10 RTPS
replies and failed to open the session (status 255) [measured].

**Cause.** `attack_discovery_poison.c:92-97` (the rogue agent only acts after receiving) and `:116-126`: it answers 12 B
"RTPS 02 03 01 0f 00000000" to any datagram on the rogue agent's port [read in code]. In Micro-XRCE-DDS-Client v3.0.2,
each session attempt waits 1000 ms for a status (`src/c/core/session/session.c:738-760`,
`UCLIENT_MIN_SESSION_CONNECTION_INTERVAL` 1000 in `CMakeLists.txt:58`); with 5 attempts, each rogue offer costs 5 s
[read in code; measured 5.0 s].

**How we tested.**
- Attack image with XRCE-04, built on 2026-11-16 from `8613c66`; upstream image as control (0 rogue offers).
- First with a discovery client of ours (same v3.0.2 library, accepts the first agent found); then with the client
  proposed in XRCE-11 in `discover 3 1000 5 1000` mode.
- Micro-XRCE-DDS-Agent v3.0.1 (`155cfaaf`), `udp4 -p 8888` with and without `-d 7400`. Test conditions: agent with
  `-d 7400` (attackzoo starts it without) and `target_ip` = IP of the attack's own container, following the label at
  `attack.yaml:23`; arguments `<attacker IP> 6666`.
- Default route set in each netns by a helper with `NET_ADMIN` (imitating `docker0`); containers with a 1 GB memory
  limit; attack stopped with SIGTERM on the binary (PID 1 is the entrypoint's bash, which ignores SIGTERM), so stdout
  reaches the log.
- tshark filters (GET_INFO to `239.255.0.2:7400`, INFO coming from 7400, CREATE_CLIENT to 6666) and a parser of ours;
  client and attack logs.
- Runs: 2 without `-d` and 3 with `-d`, with XRCE-04; controls without the attack and with the upstream. Load: load
  average 3.1 to 6.0, with other tests running; the times come from 5 fixed 1000 ms attempts in the Client, not from
  the load.
- Independent review: a second reviewer recounted the pcaps with their own export and parser and measured the delay on
  the wire from the first GET_INFO.

**No fix tested.** To fulfill "Intercept all client communications", the rogue agent would have to speak XRCE (at least
answer STATUS_AGENT to CREATE_CLIENT) [inferred]; we did not implement or measure it.

**How to reproduce.** In the reproduction file, section XRCE-09; uses P1, P2, P3, P6, P7.

**Caveats.**
- It only exists with XRCE-04 applied; there is no BEFORE.
- The measured effect depends on conditions we set up: agent with `-d 7400` and `target_ip` equal to the attack
  container's IP.
- Not tested: the campaign path.

**Versions.**
- attackzoo `8613c66`; Micro-XRCE-DDS-Client v3.0.2 (`6884d7b`); Micro-XRCE-DDS-Agent executed v3.0.1 (`155cfaaf`);
  micro-ROS `rmw_microxrcedds` branch kilted (`9d49b4d`), read only; Docker 29.6.2; tcpdump 4.99.6; tshark 4.6.9.

### XRCE-10 · xrce-dds-session-hijack: The 30 S Window Covers Only 1 Of The 7 Keys The Attack Tries (43 S Per Key)

| | |
|---|---|
| Class | (b) inconsistency between parts of attackzoo |
| In this PR | note |
| Files | none (no patch); involves `docker/attackers/xrce-dds-session-hijack/attack_session_hijack.c`, `attack.yaml`, `entrypoint.sh` and `README.md` |
| Depends on | none |

**Promise.** `docker/attackers/xrce-dds-session-hijack/attack.yaml:5`: "XRCE-DDS session hijacking or collision attempts
through manipulation of identifiers, keys, or session fields." The code has 7 known keys
(`attack_session_hijack.c:17-25`) and goes through all of them (`:154-157`). The declared window: `attack.yaml:8`
`max_runtime_s: 30`, `:31-32` `duration_s` with default 30, `entrypoint.sh:5-6` (`timeout` with default 30) and
`README.md:14` "Suggested max runtime | `30s`".

**What happens.** Each key takes ~43 s, so the 30 s window only reaches the first one (`0xAAAABBBB`) [measured]: in the
8 runs of 30 s there was 1 CREATE_CLIENT (XRCE session request) from the attacker and 0 DELETE; the attacker's last
datagram goes out ~11 s after the first and the rest is silence until the `timeout` (exit 124). With `DURATION_S=120`
(the default of the campaign's attack window), the CREATE_CLIENT went out at t = 15.93, 58.97 and 102.04 s: 43.04 and
43.07 s per key, 3 of the 7 keys [measured]; the 7 would take ~301 s [inferred]. With a victim on the first key (the
client proposed in XRCE-11), the hijack happened in 6 of 6 runs of 30 s; the second key (`0xCCCCDDDD`, the one in the
official `SubscribeHelloWorld` example) was never taken in 30 s (0 of 6) [measured]. With 120 s, the second key took
over the official subscriber: its participant and topic replaced and, at the end of the keepalive, `delete_client`
closed the victim's session [measured]. In the attackzoo flow there is no legitimate XRCE client (`client-super` only
sends `uxrce_probe_` plus 8 B), so there the hijack has no victim.

**Cause.** Per key the code spends up to 2 s waiting for a status (`:104`), ~11 s of injection (100 x 100 ms plus 10
`uxr_run_session_time(100)`, `:112-131`), 30 s of fixed keepalive (`:133-134`) and 2 s of `sleep` (`:156`) [read in
code; measured 43 s].

**How we tested.**
- Attack images built on 2026-11-16 from the upstream tree `8613c66` and with XRCE-05; Micro-XRCE-DDS-Agent v3.0.1
  (`155cfaaf`), `udp4 -p 8888 -v6` (and without `-v6` in 2 runs).
- README form with `-e DURATION_S=30` (and 120 in one run).
- Victims set up by us: official examples `PublishHelloWorld` (`0xAAAABBBB`) and `SubscribeHelloWorld` (`0xCCCCDDDD`)
  from Client v3.0.2 and, later, the XRCE-11 client publishing on `0xAAAABBBB` (3 runs with each attack image).
- CREATE_CLIENT and DELETE counted with an XRCE decoder of ours; hijack by the "session re-established" line in the
  agent log.
- Load: load average 0.2 to 1.4 in the main runs; 3.3 to 5.4 in the runs with the XRCE-11 client.
- Independent review: a second reviewer recounted the 9 captures with their own parser (intervals of 43.04 and 43.07 s)
  and the hijack times with their own script.
- Not tested: the web interface (30 s watchdog) and the campaign path.

**No fix tested.** Any option changes an attack parameter. Suggestion to the owner: raise `duration_s` and
`max_runtime_s` to ~310 s (with the README and the entrypoint together), so the 7 keys fit; the alternatives (shortening
the keepalive or the injection per key, or using fewer keys) change the script.

**How to reproduce.** In the reproduction file, section XRCE-10; uses P1, P2, P6.

**Caveats.**
- The ~301 s for the 7 keys is arithmetic (43 x 7), not measured.
- The 6 of 6 depends on the victim's key: the one chosen was the official example's, which is the first of the
  attack's 7. micro-ROS draws the client's key at random (`rmw_microxrcedds`, `rmw_init.c:111-115`) and would not be
  hit by the 7 fixed keys [read in code].
- Not tested: web interface and campaign path.

**Versions.**
- attackzoo `8613c66`; Micro-XRCE-DDS-Client v3.0.2 (`6884d7bd`); Micro-XRCE-DDS-Agent executed v3.0.1 (`155cfaaf`);
  micro-ROS `rmw_microxrcedds` branch kilted (`9d49b4d`), read only; Docker 29.6.2; tcpdump 4.99.6; tshark 4.6.9.

### MQTT-04 · mqtt-lwt-abuse: Always Prints "LWT Triggered", Without Checking Anything (Note, No Fix)

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | note |
| Files | `docker/attackers/mqtt-lwt-abuse/mqtt-lwt-abuse.py` (line 19) |
| Depends on | none |

**Promise.** `docker/attackers/mqtt-lwt-abuse/mqtt-lwt-abuse.py:19`: `print(f"[!] LWT triggered for fake device: critical_sensor_{client_num}")`, after `:14` "# Connect and disconnect abruptly to trigger the LWT.".

**What happens.** The script prints the line for every fake device, whether or not the broker (the MQTT server) accepted the connection, and whether or not the Will (the message the broker publishes when a client's connection drops without notice) was published. Measured: 50 `LWT triggered` lines with 0 Wills delivered in three conditions: everything from `8613c66`; broker accepting anonymous with the attack from `8613c66`; broker from `8613c66` with the attack without DISCONNECT [measured].

**Cause.** `:19` checks nothing; paho-mqtt 1.6.1's `connect()` does not wait for the CONNACK (`paho/mqtt/client.py:885-914`, `:1088`) and the attack runs no network loop, so the connection result is never read [read in code].

**How we tested.** In the same runs as MQTT-02: upstream images at `8613c66` (Python 3.11.18, `paho-mqtt` 1.6.1), arguments of `attackzoo.py run` (`-e COUNT=50 -e DELAY_MS=100 <IP> 1883`), legitimate subscriber on the Will topic. Count: `grep -c 'LWT triggered'` on the attack log against the messages received by the subscriber and the broker's PUBLISH in the pcap. A second reviewer recounted the pcap and the log.

**How to reproduce.** In the reproduction file, section MQTT-04; uses P1, P2, P9.

**Caveats.** No fix tested. It does not change the wire, only the log; the line misleads whoever reads the attack log. Unmeasured suggestion: `loop_start()` with `on_connect` and print only with rc=0.

**Versions.** `paho-mqtt` 1.6.1 (pinned); mosquitto 2.1.2 (and 2.1.4 in one run of 2026-11-17 of the reproduction file, with the same result).

### MQTT-05 · mqtt-lwt-abuse: `max_runtime_s: 10` Against A ~33 S Loop; With The Cutoff 17 Of The 50 Wills Go Out (Note, No Fix)

| | |
|---|---|
| Class | (b) inconsistency between parts of attackzoo |
| In this PR | note |
| Files | `docker/attackers/mqtt-lwt-abuse/attack.yaml` (line 8), `docker/attackers/mqtt-lwt-abuse/README.md` (line 14) |
| Depends on | MQTT-01 and MQTT-02 (effect: without them no Will goes out in any window) |

**Promise.** `docker/attackers/mqtt-lwt-abuse/attack.yaml:8`: `max_runtime_s: 10`; `README.md:14`: "Suggested max runtime | `10s`". The script itself creates 50 devices (`mqtt-lwt-abuse.py:24`, `COUNT` default 50; `:27` "# Create 50 fake critical devices that disappear.").

**What happens.** The loop takes 50 x (0.5 s + 0.1 s) = 30 s nominal (`mqtt-lwt-abuse.py:16`, `:24-25`, `:28-31`), 33.4 s measured with the attack fixed. Only the Streamlit interface applies `max_runtime_s`: after that time it runs `docker rm -f` on the container (`modules/attackzoo_st.py:163-188`); the value comes from `attack.yaml` as the default of an editable field (`:2570`, `:2643-2652`) [read in code]. `run`, `experiment` and the campaign do not use it [read in code]. With the cutoff at 10 s and the attack fixed (MQTT-01 + MQTT-02), 17 of the 50 Wills go out (`sensor_0` to `sensor_16`) and the late subscriber receives the retained `sensor_16` [measured]. Each Will is one turn of the loop (0.6 s) completed before the cutoff, so the number depends on the container's start and on the load: in 10 repetitions of 2026-11-17 with the machine free of other tests, 17 or 18 went out (3 of them with mosquitto 2.1.4, the others with 2.1.2), and with other tests running, 13 and 6 (both with 2.1.4) [measured]. With the code from `8613c66`, 0 go out in any window (MQTT-01, MQTT-02).

**Cause.** The suggested `max_runtime_s` (10 s) is shorter than the loop's duration with `attack.yaml`'s own defaults (`count` 50, `delay_ms` 100) [read in code + measured].

**How we tested.** Broker and lwt with MQTT-01 and MQTT-02 (Python 3.11.18, `paho-mqtt` 1.6.1, mosquitto 2.1.2), arguments of `attackzoo.py run` (`-e COUNT=50 -e DELAY_MS=100 <IP> 1883`), and the interface's cutoff simulated: SIGKILL 10 s after the `docker run` returned (the container lived 11.1 s). Legitimate subscriber and late subscriber, as in MQTT-02. One run; load (load average) 2.6. A second reviewer recounted the pcap: 17 CONNECT, 17 CONNACK rc=0, 17 Wills delivered; noted, in the review, that the number depends on the instant of the cutoff and falls between 16 and 17 (later, in 10 repetitions with the machine free of other tests, 17 or 18; see "What happens"). The Streamlit interface was not run; a larger `max_runtime_s` was not tested.

**How to reproduce.** In the reproduction file, section MQTT-05; uses P1, P2, P4, P9.

**Caveats.** No fix tested. Unmeasured suggestion: `max_runtime_s` of at least 35. The effect only shows up with MQTT-01 and MQTT-02, and only on the interface path, where 10 s is the initial value of a field the user can change.

**Versions.** `paho-mqtt` 1.6.1 (pinned); mosquitto 2.1.2 (and 2.1.4 in 3 of the 10 repetitions of 2026-11-17 and in the two with other tests running); Docker 29.6.2.

### COAP-03 · coap-response-fuzz: The "Malformed Options" Phase Sends A Plain GET (Note, No Fix)

| | |
|---|---|
| Class | (a) the code does something other than what it promises |
| In this PR | note |
| Files | `docker/attackers/coap-response-fuzz/coap-response-fuzz.py` (line 65) |
| Depends on | none |

**Promise.** `docker/attackers/coap-response-fuzz/coap-response-fuzz.py:57`: "Fuzzes CoAP options."; `:59`: `print("\nFuzzing: malformed options")`.

**What happens.** For each resource (`/api`, `/sensor`, `/actuator`, `/config`), the phase sends a GET with only the Uri-Path option (the resource path), with no malformed option; the server answers 4.04 (resource not found) [measured: 4 GETs, one per resource, with only Uri-Path]. The effect on the target is that of a plain GET.

**Cause.** `coap-response-fuzz.py:65`: `request = Message(code=GET, uri=uri)`; no option is manipulated [read in code].

**How we tested.** Fuzz built from the upstream at `8613c66` (aiocoap 0.4.7 pinned, Python 3.11.18), against a CoAP server that does not crash (CoAPServer `744cc22` with per-datagram exception handling, the alternative described in COAP-01, used here only so the fuzz reaches all phases); attack as in the README (`<IP> 5683`, no `-e`, until it exits on its own); the phase's GETs identified in the pcap by `tshark` (code, MID, `coap.opt.uri_path`). A second reviewer re-extracted the fields with `tshark` and checked the 4 GETs. One run.

**How to reproduce.** In the reproduction file, section COAP-03; uses P1, P2, P3, P10.

**Caveats.** No fix tested (none was built). No effect on the target; the note only corrects what the log and the docstring say about the phase.

**Versions.** aiocoap 0.4.7 (pinned); CoAPServer `744cc22`; Docker 29.6.2.

## Appendix A: What We Tested That Showed No Problem

| What | Result | Mark |
|---|---|---|
| Regression of WEB-02: the other 10 attacks that target `http-server`, against DVWA with and without WEB-02 | Same counts with the `8613c66` server and with the fixed one: `dos-http-simple` (200 GET, 200 404 responses), `dos-http-slowloris` in 60 s (250 SYN; 150 408 responses and 100 400 responses), `idor-path-traversal` (570 GET, 0 files), `idor-url-parameter` (5,965 GET), `sql-injection` from `8613c66` (6,718 GET, 0 queries), `web-dir-enumeration` (5 and 60 s, identical gobuster findings: 15 and 19), `web-https-heartbleed` on port 80 (200 ClientHello, 200 400 responses), `web-simple-scanner`/nikto (22,020 requests; only `GET /config/` changes, from 1,407 to 1,624 B, from the listing with `config.inc.php.bak`), `web-wide-scanner` (0 packets in both, no internet on the test network), `xss-scanner` from `8613c66` (192 requests, "XSS found 0"). In the README form, on an isolated network; layer 4 floods left out, because the fix does not touch them [read in code] | [measured] |
| `mqtt-bruteforce` with the user `attacker` on the broker (MQTT-01) | Not affected: ralmqtt's user list (`3dd72cb`) and `passwords.txt` do not have `attacker`/`attackerpass`; 252 CONNECT with a user (6 x 42), all refused (rc=5) | [measured + read in code] |
| `web-https-heartbleed` and `smb-enumerating` against the right servers (`ssl-heartbleed` and `smb-server`, GEN-03) | They work: 200 of 200 heartbeats returned 16 KB of memory for a request with no payload; the enumeration listed the shares `public` and `IPC$` | [measured] |
| Campaign server choice across the 60 attacks, without `SERVICE_OVERRIDES` | Only `web-https-heartbleed` and `smb-enumerating` diverge (both land on `http-server`); with the yaml fixed (GEN-03) none diverges; the dry-run picks the right servers with the current yaml and with the fixed one | [measured with attackzoo's code, without containers] |
| Other uses of `timeout` in the attacks | Only `syn-flood` and `dos-http-slowloris` have the GEN-04 problem; the other 26 uses (coreutils, no `exec`, base `ubuntu:24.04`) leave `timeout` as the parent process and signal the child | [read in code; mechanism measured: coreutils 9.4, `exec timeout 3 sleep 60` exits with 124 in 3.98 s] |
| Build of 2026-11-16 of the 7 XRCE attacks | The `8613c66` build passes and the binaries come out identical to those in the machine's old images, despite the unpinned clones; the GEN-01 defect only shows up with an injected failure | [measured] |
| Campaign capture filters (`AUTO_BPF_BY_ATTACK`) on `-i any` | 15 distinct filters (plus 12 attacks without a filter); all compile on `-i any`, except the one for `cdp-table-flood` (CAMP-01); in the dry-run of the 60 plans, with CAMP-03 only the `ipv6-mld-flood` plan changes | [measured: compilation and dry-run] |
| Filters of `ipv6-ns-flood` and `ipv6-ra-flood` (`icmp6 and ip6[40] == 135/134`) | They do not have the MLD problem (CAMP-03): `flood_solicitate6` and `flood_router6` only add a Hop-by-Hop header when called with an option, and the entrypoints call without an option (checked in the strings of the repository's binaries) | [read in code] |
| `xrce-dds-time-desync` inside the window | Completes on its own in ~12.6 s, with all replies (CREATE_CLIENT 20, TIMESTAMP 2000, TIMESTAMP_REPLY 2000, DELETE 20), before the 30 s timeout | [measured] |
| `coap-token-collision` fixed (COAP-02) outside the normal flow | No regression: against a dead target (closed port, 40 s), the `8613c66` one sends 415 GET and the fixed one 466, both stuck in phase 1 retransmitting; against a server with a separate response, 406 GET, 0 RST and 0 errors in both | [measured] |
| XRCE Agent v3.0.1 (executed) versus v3.0.2 (what attackzoo builds today) | `process_timestamp_submessage` identical (`diff -w`); in the session-hijack paths only formatting changes, except two changes that do not affect the attack (minimum MTU of 13, the attack sends 508; binary path, the attack uses XML) | [read in code] |
| Stopping the Zenoh fixes of timestamp-mess, memory-exhaustion, sequence-exhaustion and fragments-reassembly (ZEN-02 to ZEN-05) with the router paused | With the SIGINT from `timeout` itself: router paused before the handshake, the process exits 0.00 s after the signal (the threads had already given up at the 5 s deadline); router paused during the flood, it exits 0.03 to 1.07 s after the signal. The proto-fuzzer's (ZEN-06) only read: the entrypoint sends SIGTERM, which the binary does not handle, and it dies immediately | [measured; ZEN-06 read in code] |
| `port-scanner-vulnerabilities` against `smb-server` with nmbd (SMB-01) | Same output; the NBNS query is now answered (1 of 1) | [measured] |
| Legitimate client during the Zenoh attacks from `8613c66` | 0 failures in all (keepalive, sequence, fragments, memory): no byte of the attack reaches the router | [measured] |
| Tree with the whole PR (`8613c66` + all commits, optional ones and the description's diffs), the repository's own checks | `attackzoo.py list --json`: 60 attacks, 7 categories, no missing field; `load_server_specs` reads the new `server.yaml` files; the campaign's server choice (`resolve_service_id`) is the same as `8613c66`'s across the 60 attacks; `bash -n` and parse of the changed `.py` files ok; no new file with CRLF. Not run: `check_attack_smoke.py` | [measured, without containers and without network] |
| Proposed Zenoh subscriber (ZEN-09) together with the fixed memory-exhaustion (ZEN-05) and sequence-exhaustion (ZEN-03) | The router's memory and log do not change with the subscriber; with the key `attackzoo/**` the router forwards 100% of the memory-exhaustion batches to the subscriber (~256 MB more on tcp/7447) | [measured, 1 run each] |

## Appendix B: Versions

| Component | Version in the tests | Where it enters |
|---|---|---|
| attackzoo | `8613c660722c852bbeb10bfb180d58039f1c3426` (`main`) | everything |
| Docker | 29.6.2, buildx 0.35.0 | test machine |
| Machine | Ubuntu 24.04.4, 8 CPUs, 8 GB of RAM, Docker root on HDD | all tests |
| Base images | `ubuntu:24.04` resolved on 2026-11-16 to `sha256:73b999393d07f2bf65a40373778a44dc9a6d54ad7718d29247d8ff9413c4d6a8` (serial 20261110; the machine's old images: 20260917); `python:3.11-alpine` at `sha256:7fbad8e4...` (Python 3.11.18; old images: 3.11.17), Alpine 3.24.4 | builds of 2026-11-16 |
| Zenoh router | `eclipse/zenoh:1.7.2` (`zenohd` v1.7.2-790faadb; tag 1.7.2 = `790faad`) | `docker/servers/zenoh-router/Dockerfile:1` |
| Zenoh, sources read | 1.0.0 (`6231698`), 0.7.2-rc (`b9103c3`), 0.5.0-beta.9 (`70d7b22`) | message IDs of the ZEN items |
| uhlc (router clock) | 0.8.2 (the one in 1.7.2's `Cargo.lock`) | ZEN-04 |
| eclipse-zenoh (Python) | 1.7.2 | legitimate client of the Zenoh tests; proposed subscriber (ZEN-09, on `python:3.11-slim`) |
| CoAPServer (`maksnowak/CoAPServer`) | `744cc228957344911b11045a28011ebf57a8729e` (2025-01-31), cloned without a pin | `docker/servers/coap-server/Dockerfile:3` |
| aiocoap | 0.4.7 in the attacks (pinned); 0.4.17 in the server | `coap-token-collision`, `coap-response-fuzz`; `coap-server` |
| mosquitto | 2.1.2 (`eclipse-mosquitto:2` resolved on 2026-11-13); 2.1.4 (`eclipse-mosquitto:2` since 2026-11-17) in the measurements of 2026-11-18 for MQTT-01 and MQTT-03, with both versions fixed by digest, and in runs of 2026-11-17 of the reproduction file, from MQTT-01 to MQTT-05, by tag | `docker/servers/mqtt-broker/Dockerfile:1` |
| paho-mqtt | 1.6.1 (pinned) | `mqtt-lwt-abuse`, `mqtt-qos-amplification` |
| ralmqtt | `3dd72cb` | `mqtt-bruteforce` |
| Micro-XRCE-DDS-Client | v3.0.2 (`6884d7bd`, `master` on 2026-11-16) | `install.sh` of the 7 `xrce-dds-*` (unpinned clone); proposed client XRCE-11 (`--branch v3.0.2`) |
| Micro-CDR | v2.0.2 (`99672492`) | `install.sh` of the 7 `xrce-dds-*` |
| Micro-XRCE-DDS-Agent | executed: v3.0.1 (`155cfaaf`) with Fast-DDS v3.6.2 and Fast-CDR v2.2.8; read only: v3.0.2 (`a88c712b`, `master` since 2026-09-03) | `docker/servers/xrce-dds-agent/agent-source-install.sh:3` |
| micro-ROS (read only) | `9d49b4d` | XRCE-10 (random session key) |
| ArpSpoof / PythonToolsKit / scapy | 1.1.2 / 1.3.0 / 2.8.0 (pip without a version) | `arp-spoof` |
| SpiderFoot | v4.0 (tarball sha256 `8b5dac6b846ae854f85243839e3a16c7412cdfbb87b2c3689829a5e40d3ccf4e`, no checksum in the Dockerfile); publicsuffixlist 0.7.14 in the image | `web-wide-scanner` |
| DVWA / Apache / database | DVWA 1.10, Apache 2.4.25, MariaDB | `http-server` |
| sqlmap | `1b1f93ae` in the image (2026-10-05); `master` at `8b78b676` (2026-11-12) | `sql-injection` (`--depth 1` clone without a pin) |
| dalfox | v3.1.2 (pinned by digest in the Dockerfile) | `xss-scanner` |
| curl (Alpine) | 8.23.0-r0, installed by WEB-06 without a fixed version | `xss-scanner` |
| Samba / enum4linux-ng | Samba 4.19.9 (`smb-server`), 4.23.8 (the `smb-enumerating` image); enum4linux-ng `288826f` | `smb-server`, `smb-enumerating` |
| yersinia | 0.8.2 (Ubuntu noble package `0.8.2-2.2build2`); source read at tag v0.8.2 (`701b59b`) | `stp-conf-flood`, `stp-tcn-flood`, `cdp-table-flood`, `dhcp-starvation` |
| udhcpd / lldpd | udhcpd 1:1.36.1-6ubuntu3.1 (BusyBox 1.36.1); lldpd 1.0.18; apt without a version | proposed victims (NET-04, NET-05) |
| BusyBox / coreutils | BusyBox 1.37.0 (`python:3.11-alpine`); coreutils 9.4 (`ubuntu:24.04`) | `syn-flood`, `dos-http-slowloris` (GEN-04); other `timeout` uses |
| slowloris (gkbrk) | `890f72d` | `dos-http-slowloris` |
| thc-ipv6 | source `477fa5b` read; precompiled `flood_mld6` binary in the repository | `ipv6-mld-flood` |
| libpcap / tcpdump / tshark | libpcap 1.10.4 (source read) and tcpdump 4.99.4-3ubuntu4.24.04.1 (Ubuntu 24.04's); capture and counting with tcpdump 4.99.6, libpcap 1.10.7 and tshark 4.6.9 | CAMP-01 to CAMP-03; all captures |
| NTLFlowLyzer (`ahlashkari/NTLFlowLyzer`) | current pin `86d0102466ea42ba03ddda5c649ac7e533fb25d9` (does not matter); proposed `d99cd5377faaed53b39450ce262652902501188d` | `setup.sh:10` |
| `setup.sh` environment (CAMP-04) | Python 3.12.3, numpy 2.5.0, pandas 3.0.4, scipy 1.18.0, dpkt 1.9.8 | `ubuntu:24.04` |
| Other Python packages | typer 0.29.1 (`coap-server`); bs4 4.15.0 and requests 2.34.2 (`php-lfi-enumeration`, no version in `requirements.txt`) | builds of 2026-11-16 |
