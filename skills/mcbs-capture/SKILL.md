---
name: mcbs-capture
description: Capture Worker Output
allowed-tools: Bash
---

# Capture Worker Output

Capture et affiche la sortie d'un worker Claude.

## Commandes

### Capturer les dernières lignes (défaut: 50)
```bash
/home/eric/projects/twich-test/claude capture <worker-name>
```

### Capturer plus de lignes
```bash
/home/eric/projects/twich-test/claude capture <worker-name> --lines 100
```

### Capturer tout le buffer
```bash
/home/eric/projects/twich-test/claude capture <worker-name> --lines 5000
```

## Avant de capturer

Vérifier que le worker existe :
```bash
/home/eric/projects/twich-test/claude list
```

## Interprétation

Chercher dans la sortie :
- **Erreurs** : Messages d'erreur ou exceptions
- **Progress** : Indicateurs de progression
- **Completion** : Messages de fin de tâche
- **/exit** : Le worker a terminé proprement

## Actions suivantes

- **En cours** : Attendre et recapturer plus tard
- **Bloqué** : Analyser, tuer et respawner
- **Terminé** : Récupérer le résultat, mettre à jour le ticket
- **Erreur** : Diagnostiquer et relancer
