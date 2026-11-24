# Privacy DNS Stack Comparison


> **Decision:** Use this comparison to assign filtering, recursion, encrypted forwarding, service discovery, and routing to explicit DNS layers; skip it if you plan to stack overlapping resolvers without testing fallback.
>
> **For:** home-lab operators, small-network administrators, and privacy-focused self-hosters  ·  **Not for:** users seeking a public resolver ranking or a set-and-forget appliance

This is a non-commercial, source-traceable decision guide. It normalizes upstream declarations; it does not claim that repository reachability proves functionality, security, maintenance, or fitness.

**Start here:** [Download the dns component evidence](assets/dns-trust-path-map.csv) — twelve projects, located upstream evidence, and explicit unknowns.

## Choose by workload


- Network-wide filtering appliance: Pi-hole or AdGuard Home.
- Declarative policy proxy: Blocky; highly composable protocol/routing pipeline: RouteDNS.
- Local validating recursion: Unbound, Knot Resolver, or BIND 9 configured for that role.
- Encrypted stub/forwarder: dnscrypt-proxy or Stubby; pair with policy/recursion only when the trust model requires it.
- Authoritative/service discovery: CoreDNS or PowerDNS; do not expose a recursive listener accidentally.

## Draw the query trust path

DNSSEC authenticates answers; it does not conceal queries. DoH/DoT protects the configured hop, not every observer. Recursion is not anonymity.

## Listener-to-resolver trust map


- **Filtering front ends** — Pi-hole and AdGuard Home own client/blocklist policy; Blocky offers declarative forwarding and filtering. Decide whether they forward or sit before local recursion.
- **Recursive validators** — Unbound, Knot Resolver, and BIND 9 can perform recursion and DNSSEC validation; harden interfaces and resource limits.
- **Encrypted stubs and routers** — dnscrypt-proxy and Stubby focus encrypted upstream transport; RouteDNS composes listeners, routing, modifiers, and resolvers.
- **Authoritative and service DNS** — CoreDNS and PowerDNS can serve zones or discovery roles; their recursion/forwarding capabilities must be deliberately bounded.


## DNS component evidence

| Project | Role | Resolution and authority role | Encrypted transport and validation | Policy and query visibility |
|---|---|---|---|---|
| Pi-hole | filtering front end | The Pi-hole® is a DNS sinkhole that protects your devices from unwanted content without installing any client-side software. | Unknown in the frozen upstream README | - A filterable and sortable query log |
| AdGuard Home | filtering front end | Free and open source, powerful network-wide ads & trackers blocking DNS server. | Unknown in the frozen upstream README | AdGuard Home is a network-wide software for blocking ads and tracking. After you set it up, it'll cover ALL your home devices, and you don't need any client-sid… |
| Blocky | policy proxy | Unknown in the frozen upstream README | - Supports modern DNS extensions: DNSSEC, eDNS, ... - DNSSEC validation of upstream resolvers | - Blocking - Blocking of DNS queries with external lists (Ad-block, malware) and allowlisting |
| Technitium DNS Server | broad DNS server | Technitium DNS Server is an open source authoritative as well as recursive DNS server that can be used for self hosting a DNS server for privacy & security. It … | - DNSSEC validation support with RSA, ECDSA & EdDSA algorithms for recursive resolver, forwarders, and conditional forwarders with NSEC and NSEC3 support. - DNS… | - Built-in system logging and query logging. |
| Unbound | recursive validator | Unbound is a validating, recursive, caching DNS resolver. It is designed to be fast and lean and incorporates modern features based on open standards. If you ha… | Unknown in the frozen upstream README | Unknown in the frozen upstream README |
| dnscrypt-proxy | encrypted forwarder | Unknown in the frozen upstream README | DNS traffic encryption and authentication. Supports DNS-over-HTTPS (DoH) using TLS 1.3 and QUIC, PQDNSCrypt, DNSCrypt, Anonymized DNS and ODoH | DNS query monitoring, with separate log files for regular and suspicious queries |
| CoreDNS | plugin DNS server | Serve as a proxy to forward queries to some other (recursive) nameserver (forward). | Serve zone data from a file; both DNSSEC (NSEC only) and DNS are supported (file and auto). | reloads. Query logging still requires the log plugin. |
| PowerDNS | DNS platform | This repository contains the sources for the PowerDNS Recursor, the PowerDNS Authoritative Server, and dnsdist (a powerful DNS loadbalancer). All three can be b… | Unknown in the frozen upstream README | Unknown in the frozen upstream README |
| BIND 9 | authoritative and recursive DNS server | The BIND name server, named, can act as an authoritative name server, recursive resolver, DNS forwarder, or all three simultaneously. It implements views for sp… | implements views for split-horizon DNS, automatic DNSSEC zone signing and key management, catalog zones to facilitate provisioning of zone data throughout a nam… | throughout a name server constellation, response policy zones (RPZ) to protect clients from malicious data, response rate limiting (RRL) and recursive query lim… |
| Knot Resolver | recursive validator | Knot Resolver is a full caching DNS resolver implementation. The core architecture is tiny and efficient, written in C and [LuaJIT][luajit], providing a foundat… | The LuaJIT modules, support for DNS privacy and DNSSEC, and persistent cache with low memory footprint make it a great personal DNS resolver or a research tool … | The LuaJIT modules, support for DNS privacy and DNSSEC, and persistent cache with low memory footprint make it a great personal DNS resolver or a research tool … |
| Stubby | encrypted stub resolver | Unknown in the frozen upstream README | Stubby is an application that acts as a local DNS Privacy stub resolver (using DNS-over-TLS). Stubby encrypts DNS queries sent from a client machine (desktop or… | tlsquerypaddingblocksize: Use the EDNS0 padding option to pad DNS queries to hide their size ednsclientsubnetprivate: Use EDNS0 Client Subnet privacy so the cli… |
| RouteDNS | composable DNS proxy/router | RouteDNS is a composable DNS stub resolver, proxy and router written in Go. It enables building flexible DNS processing pipelines with support for all modern DN… | RouteDNS is a composable DNS stub resolver, proxy and router written in Go. It enables building flexible DNS processing pipelines with support for all modern DN… | RouteDNS is a composable DNS stub resolver, proxy and router written in Go. It enables building flexible DNS processing pipelines with support for all modern DN… |

Values are short excerpts from the frozen upstream README, not feature-test scores. The CSV retains the located evidence for each cell. “Unknown” means the retrieved document did not establish that axis; it is not a claim that the feature is absent.

## Keep the authority path explicit


A common chain is clients → filtering front end → local validating resolver, with no public listener. Another is clients → policy proxy → selected DoT/DoH upstreams. Capture normal queries, block hits, DNSSEC failures, upstream timeout, cache behavior, and complete upstream loss before rollout.


## Adoption notes by project

### Pi-hole

- **Choose it for:** Home networks wanting familiar blocklist operations.
- **License at the frozen source:** [EUPL-1.2](https://raw.githubusercontent.com/pi-hole/pi-hole/f7c0220e63e753c664a1ec08d42d6b647b86005d/LICENSE).
- **Adoption test:** Define upstream resolver, client identity, DHCP ownership, list-update trust, and backup; do not expose it as an open resolver.
- **Source:** [pi-hole/pi-hole](https://github.com/pi-hole/pi-hole).

### AdGuard Home

- **Choose it for:** Operators wanting filtering plus encrypted listener options.
- **License at the frozen source:** [GPL-3.0](https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/69ee3d389910d5d30701cbe867280cf1809853ac/LICENSE.txt).
- **Adoption test:** Pin stable channels, restrict listeners, test bootstrap DNS and fallback, and export configuration before upgrades.
- **Source:** [AdguardTeam/AdGuardHome](https://github.com/AdguardTeam/AdGuardHome).

### Blocky

- **Choose it for:** Version-controlled network DNS policy.
- **License at the frozen source:** [Apache-2.0](https://raw.githubusercontent.com/0xERR0R/blocky/8088f1aaca9c595a08e075606ec36793b0493831/LICENSE).
- **Adoption test:** Test group/client mapping, cache, upstream health, DNSSEC expectations, and config rollback; it is not an authoritative zone platform.
- **Source:** [0xERR0R/blocky](https://github.com/0xERR0R/blocky).

### Technitium DNS Server

- **Choose it for:** Operators wanting one GUI-driven DNS appliance.
- **License at the frozen source:** [GPL-3.0](https://raw.githubusercontent.com/TechnitiumSoftware/DnsServer/c6d66b3247df8cdc8eecdc9b38be51ba8d3c9498/LICENSE).
- **Adoption test:** Broad scope raises blast radius; separate authoritative and recursive exposure, back up zones/config, and review apps.
- **Source:** [TechnitiumSoftware/DnsServer](https://github.com/TechnitiumSoftware/DnsServer).

### Unbound

- **Choose it for:** Networks wanting local validating recursion.
- **License at the frozen source:** [BSD-3-Clause](https://raw.githubusercontent.com/NLnetLabs/unbound/d1a45312a8473003eacc215bc8be59b928b1cd04/LICENSE).
- **Adoption test:** Harden interfaces, access controls, cache/resource limits, root hints/trust anchors, and failure behavior before client rollout.
- **Source:** [NLnetLabs/unbound](https://github.com/NLnetLabs/unbound).

### dnscrypt-proxy

- **Choose it for:** Devices or gateways prioritizing upstream transport privacy.
- **License at the frozen source:** [ISC](https://raw.githubusercontent.com/DNSCrypt/dnscrypt-proxy/a53345698397bce4267fd80246bd2ba378500d79/LICENSE).
- **Adoption test:** Provider-list trust, bootstrap resolution, fallback, logs, and local cache must match the threat model; it is not full recursion.
- **Source:** [DNSCrypt/dnscrypt-proxy](https://github.com/DNSCrypt/dnscrypt-proxy).

### CoreDNS

- **Choose it for:** Cloud-native or lab service DNS.
- **License at the frozen source:** [Apache-2.0](https://raw.githubusercontent.com/coredns/coredns/996a30df7f5cca79a3bb34078f8897f673ac74dd/LICENSE).
- **Adoption test:** Plugin order changes behavior; test recursion boundaries, cache, loops, zone authority, and exposure outside the cluster.
- **Source:** [coredns/coredns](https://github.com/coredns/coredns).

### PowerDNS

- **Choose it for:** Production DNS teams that want specialized components.
- **License at the frozen source:** [GPL-2.0](https://raw.githubusercontent.com/PowerDNS/pdns/b2d79981dcfe762ce847f7af1ba8b3756c5013fb/COPYING).
- **Adoption test:** Do not treat the authoritative server and Recursor as one mode; secure APIs/backends and test DNSSEC/key backup separately.
- **Source:** [PowerDNS/pdns](https://github.com/PowerDNS/pdns).

### BIND 9

- **Choose it for:** Operators needing broad standards coverage.
- **License at the frozen source:** [MPL-2.0](https://raw.githubusercontent.com/isc-projects/bind9/e68fc6f174308c9def1f6e8715d790a498b65fbb/LICENSE).
- **Adoption test:** Separate authoritative and recursive listeners, apply query limits/RRL, maintain keys, and follow supported branch guidance.
- **Source:** [isc-projects/bind9](https://github.com/isc-projects/bind9).

### Knot Resolver

- **Choose it for:** Operators wanting a modern local recursive resolver.
- **License at the frozen source:** [GPL-3.0](https://raw.githubusercontent.com/CZ-NIC/knot-resolver/ae7d3b9a592fbc0a3282b2f2f813df556269619e/COPYING).
- **Adoption test:** Upstream says container images are for trying the resolver, not production; use supported packages and harden access.
- **Source:** [CZ-NIC/knot-resolver](https://github.com/CZ-NIC/knot-resolver).

### Stubby

- **Choose it for:** Hosts that need a local DoT stub in front of applications.
- **License at the frozen source:** [BSD-3-Clause](https://raw.githubusercontent.com/getdnsapi/stubby/7f07bde70ecb9b53fb5fed765725cef6492daf5c/COPYING).
- **Adoption test:** Canonical README is minimal; use getdns documentation, define bootstrap/fallback, and do not infer filtering or full recursion.
- **Source:** [getdnsapi/stubby](https://github.com/getdnsapi/stubby).

### RouteDNS

- **Choose it for:** Advanced policy routing across protocols.
- **License at the frozen source:** [BSD-3-Clause](https://raw.githubusercontent.com/folbricht/routedns/6ac97b1d409e3929a8cb015bfc975cd2274805d8/LICENSE).
- **Adoption test:** Its flexibility can create loops or duplicate validation/cache layers; diagram and test every listener-to-resolver path.
- **Source:** [folbricht/routedns](https://github.com/folbricht/routedns).

## Test fail-open and fallback

1. Draw listener, policy proxy, resolver and upstream with explicit logged identities.
2. Test DNSSEC failure separately from encrypted-transport failure.
3. Disable the chosen upstream and observe bootstrap/fallback without unexpected cleartext.
4. Restrict recursion to intended clients and restore zones, config and trust anchors.

## What this guide covers

DNS resolution, client policy and query trust; not a VPN buying guide or a promise of anonymity.

## Adjacent guides

- [open-source-secrets-management-landscape](https://github.com/RichardPadavttan/open-source-secrets-management-landscape) — Use it when DNS credentials, API tokens, or encrypted configuration need explicit custody and rotation.
- [self-hosted-uptime-monitoring-map](https://github.com/RoryReeses/self-hosted-uptime-monitoring-map) — Use it when resolver availability and dead-man coverage need independent monitoring.
- [self-hosted-container-management-map](https://github.com/Hervieux39AC/self-hosted-container-management-map) — Use it when the DNS stack runs in containers and must survive dashboard or control-plane loss.

## Located sources and update policy

[`sources.json`](sources.json) binds each cited declaration to a commit, document, exact line range and local snapshot hash. [`assets/projects.json`](assets/projects.json) holds the normalized roles and decision axes. Current HEAD reachability is recorded separately; it is not a maintenance or security assessment. Licensing is version- and directory-specific. Re-read the selected release before adoption.

Run the local evidence and package checks, then opt into public-source reachability:

```bash
python3 scripts/verify_sources.py
python3 scripts/verify_sources.py --online
```

These checks validate source binding, excerpts, hashes, language, the decision asset and nonempty public content. They do not certify feature behavior, migration success or restore success. No popularity score, paid placement or affiliate ranking is used. Restricted-license and historical examples are explicit contrasts, not silently recommended open-source defaults.

If this saved you a decision, star the repo — it is how the next reader finds it.
