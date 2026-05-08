````markdown
# Persona Index

Machine-readable roster of every persona in `personas/`. The conductor reads this file to filter by tag, sample randomly, or look up by slug. The persona generator skill updates this file on every persona creation. **Never edit by hand** — the file is regenerated from the actual persona files.

## How to query

- Tag filter: filter rows where `tags` contains all requested tags.
- Random sample: shuffle rows, take first N.
- Single lookup: filter rows where `slug` matches.

## Roster

```yaml
personas: []
```

(Your library starts empty. Generate your first batch by typing `/setup` for guided onboarding, or `generate 10 personas` for a quick start. Each entry will be a YAML mapping with: `slug`, `name`, `created`, `age`, `age_bucket`, `gender`, `device_primary`, `tech_literacy`, `patience`, `trust_disposition`, `tags`. Other fields are looked up from the persona file directly when needed.)
````
