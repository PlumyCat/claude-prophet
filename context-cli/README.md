# context-cli

CLI pour gérer les rôles et directives des workers Claude.

## Installation

```bash
cd context-cli
uv sync
```

## Structure

```
context-cli/
├── roles/
│   ├── prophet-claude.yaml
│   └── worker.yaml
├── directives/
│   ├── base.yaml
│   └── code-quality.yaml
└── main.py
```

## Commandes

### list-roles

Liste les rôles disponibles.

```bash
uv run python main.py list-roles
```

### list-directives

Liste les directives disponibles.

```bash
uv run python main.py list-directives
```

### show

Affiche le contexte complet d'un rôle (prompt + directives).

```bash
uv run python main.py show worker
uv run python main.py show prophet-claude
```

### settings

Génère un settings.json avec les permissions du rôle.

```bash
# Afficher sur stdout
uv run python main.py settings prophet-claude

# Sauvegarder dans un fichier
uv run python main.py settings prophet-claude -o settings.json
```

### validate

Valide la configuration d'un rôle.

```bash
uv run python main.py validate worker
```

## Format des fichiers

### Rôle (roles/*.yaml)

```yaml
name: worker
description: Worker Claude for tasks

prompt: |
  Your role prompt here...

directives:
  - base
  - code-quality

permissions:
  allow:
    - "Bash(git:*)"
    - "Read"
  deny:
    - "Bash(rm -rf:*)"
```

### Directive (directives/*.yaml)

```yaml
name: base
description: Base directives

content: |
  Your directive content here...
```

## Intégration avec claude-cli

```bash
# Le flag --role charge le contexte depuis context-cli
cd ../claude-cli
uv run python main.py spawn --role worker "Implement feature X"
```
