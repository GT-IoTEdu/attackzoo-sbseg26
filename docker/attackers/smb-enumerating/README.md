# Attack "SMB Enumerating"

> Enumeration of SMB share directories and vulnerabilities.

## Metadata

| Field | Value |
|---|---|
| ID | `recon_smb_enum` |
| Category | 1) Reconnaissance and Discovery |
| Subcategory | 1.2 Port, service, OS, and vulnerability scanning |
| Image | `attack-smb-enumerating:latest` |
| Container | `attack-smb-enumerating` |
| Suggested max runtime | `10s` |
| Typical targets/services | `smb-server` |
| MITRE ATT&CK | [https://attack.mitre.org/tactics/TA0043/](https://attack.mitre.org/tactics/TA0043/)<br>[https://attack.mitre.org/tactics/TA0007/](https://attack.mitre.org/tactics/TA0007/)<br>[https://attack.mitre.org/techniques/T1590/](https://attack.mitre.org/techniques/T1590/)<br>[https://attack.mitre.org/techniques/T1592/](https://attack.mitre.org/techniques/T1592/)<br>[https://attack.mitre.org/techniques/T1595/](https://attack.mitre.org/techniques/T1595/)<br>[https://attack.mitre.org/techniques/T1595/002/](https://attack.mitre.org/techniques/T1595/002/)<br>[https://attack.mitre.org/techniques/T1046/](https://attack.mitre.org/techniques/T1046/)<br>[https://attack.mitre.org/techniques/T1135/](https://attack.mitre.org/techniques/T1135/)<br>[https://attack.mitre.org/techniques/T1087/](https://attack.mitre.org/techniques/T1087/)<br>[https://attack.mitre.org/techniques/T1069/](https://attack.mitre.org/techniques/T1069/) |

## Parameters

| Parameter | Type | Required | Default/placeholder | Description |
|---|---|---|---|---|
| `--target_ip` | `ip` | yes | `__HOST_IP__` | Target IP address or FQDN |

## Testbed Execution

Use the project CLI to preserve traceability through the declarative catalog:

```bash
python3 attackzoo.py run recon_smb_enum --target <TARGET>
```

Run the container directly for isolated validation:

```bash
docker run --rm -d --name attack-smb-enumerating attack-smb-enumerating:latest "<TARGET_IP>"
```

## Observability

- Use `python3 attackzoo.py experiment` to run controlled warmup/attack/cooldown windows.
- Expected artifacts include PCAP files, probe CSVs, optional telemetry, features, datasets, and reports under `experiments/`.
- Typical testbed target services: `smb-server`.
