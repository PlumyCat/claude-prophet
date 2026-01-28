# STORY-002: Améliorations UX Workers

**Epic:** Multi-Agent Orchestration
**Priority:** Should Have
**Story Points:** 5
**Status:** Completed
**Assigned To:** Claude
**Created:** 2025-01-28
**Sprint:** 1

---

## User Story

As a **Prophet Claude**
I want to **avoir des workers plus autonomes et un meilleur suivi**
So that **le workflow de délégation soit plus fluide et moins manuel**

---

## Description

Suite aux tests du système Multi-Claude Bootstrap, plusieurs points d'amélioration ont été identifiés pour rendre les workers plus autonomes et améliorer l'expérience utilisateur.

---

## Issues identifiées

### 1. Auto-exit workers (Priorité: Haute)
**Problème:** Les workers ne font pas `/exit` automatiquement après avoir terminé leur tâche.
**Solution:** Ajouter une directive dans le rôle worker pour sortir avec `/exit` quand terminé.

### 2. Skill /done pour workers (Priorité: Haute)
**Problème:** Le worker doit manuellement mettre à jour le ticket ET faire /exit.
**Solution:** Créer un skill `/done` qui:
- Met à jour le ticket associé en "done"
- Ajoute un commentaire de completion
- Exécute `/exit`

### 3. Intégration ticket-worker (Priorité: Moyenne)
**Problème:** Pas de lien automatique entre ticket et worker.
**Solution:**
- Option `--ticket` dans `claude spawn` pour lier un ticket
- Le worker connaît son ticket ID via variable d'environnement ou contexte

### 4. Améliorer directives worker (Priorité: Moyenne)
**Problème:** Les workers n'ont pas assez d'instructions sur comment terminer proprement.
**Solution:** Enrichir `worker.yaml` avec des instructions claires de fin de tâche.

---

## Acceptance Criteria

### Skill /done
- [ ] Créer `.claude/commands/done.md`
- [ ] Le skill met à jour le ticket en "done" si un ticket est associé
- [ ] Le skill affiche un message de confirmation
- [ ] Instructions pour faire `/exit` après

### Directives worker améliorées
- [ ] Modifier `context-cli/roles/worker.yaml`
- [ ] Ajouter instructions explicites de fin de tâche
- [ ] Mentionner `/exit` obligatoire

### Option --ticket pour spawn
- [ ] Ajouter `--ticket` à `claude spawn`
- [ ] Passer le ticket ID dans le contexte du worker
- [ ] Auto-update ticket en "in-progress" au spawn

---

## Technical Notes

### Skill /done

```markdown
# Done - Task Completion

Signale la fin de la tâche assignée.

## Actions
1. Si ticket associé: `./tickets update <id> --status done`
2. Afficher message de confirmation
3. Rappeler de faire `/exit`
```

### Worker role amélioré

```yaml
# Ajouter à worker.yaml
completion_instructions: |
  QUAND TU AS TERMINÉ:
  1. Vérifie que tout est fait
  2. Si ticket assigné: ./tickets update <ticket> --status done
  3. Fais /exit pour libérer la session

  IMPORTANT: Ne reste JAMAIS actif après avoir terminé.
```

---

## Definition of Done

- [ ] Skill `/done` créé et fonctionnel
- [ ] Role worker mis à jour avec instructions de fin
- [ ] Option `--ticket` ajoutée à spawn
- [ ] Tests manuels passés
- [ ] Documentation mise à jour

---

## Progress Tracking

**Status History:**
- 2025-01-28: Story créée suite aux tests
