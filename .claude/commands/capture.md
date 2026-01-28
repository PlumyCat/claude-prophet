# Capture Worker Output

Capture et affiche la sortie d'un worker Claude.

## Utilisation

L'utilisateur doit fournir :
1. **Nom du worker** : Le nom de la session à capturer

## Commandes

### Capturer les dernières lignes (défaut: 50)
```bash
./claude capture <worker-name>
```

### Capturer plus de lignes
```bash
./claude capture <worker-name> --lines 100
```

### Capturer tout le buffer
```bash
./claude capture <worker-name> --lines 5000
```

## Avant de capturer

Vérifier que le worker existe :
```bash
./claude list
```

## Interprétation de la sortie

Chercher dans la sortie :
- **Erreurs** : Messages d'erreur ou exceptions
- **Progress** : Indicateurs de progression
- **Completion** : Messages de fin de tâche
- **/exit** : Le worker a terminé proprement

## Actions suivantes

Selon l'état du worker :
- **En cours** : Attendre et recapturer plus tard
- **Bloqué** : Analyser le blocage, éventuellement tuer et respawner
- **Terminé** : Récupérer le résultat, mettre à jour le ticket
- **Erreur** : Diagnostiquer et relancer avec corrections
