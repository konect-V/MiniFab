![capture d'écran](./docs/assets/img/screenshot.png)

## Aperçu

MiniFab est un système intelligent de gestion multimodale pour machines de fabrication basé sur Klipper. Il transforme une seule machine en trois outils distincts : une fraiseuse CNC, une imprimante 3D et un traceur de dessin. Grâce à sa détection automatique d'outils via CAN bus, MiniFab configure dynamiquement votre machine selon l'outil connecté.

## Démarrage

- [Aperçu](#aperçu)
- [Démarrage](#démarrage)
  - [Documentation](#documentation)
  - [Installation](#installation)
    - [Prérequis](#prérequis)
    - [Installation](#installation-1)
    - [Utilisation](#utilisation)
  - [Dépannage](#dépannage)
  - [Plateformes supportées](#plateformes-supportées)
  - [Fonctionnalités principales](#fonctionnalités-principales)

  - [Améliorations futures](#améliorations-futures)
  - [Contribuer](#contribuer)
  - [Licence](#licence)

### Documentation

La documentation complète du projet est disponible dans le dossier `docs/`:
- [Structure du projet](./docs/STRUCTURE.md)
- Guide de configuration : `computer_setup_procedure.md`

Pour comprendre l'architecture du projet, vous pouvez examiner les fichiers clés :
- `src/scripts/autofirmware.py` : Système de détection d'outils
- `src/scripts/confswap.py` : Gestion des configurations
- `src/config/change.cfg` : Macros pour changement de mode
- `src/config/main_printer.cfg` : Configuration de base

### Installation

#### Prérequis

- Raspberry Pi (recommandé : Pi 4)
- Carte contrôleur compatible Klipper avec CAN bus
- Têtes d'outils compatibles (fraiseuse, extrudeur, traceur)
- Carte SD (min. 16 Go)

> [!IMPORTANT]
> Assurez-vous que votre matériel est compatible avec Klipper et dispose d'une interface CAN bus fonctionnelle. Les UUIDs CAN doivent être configurés correctement pour chaque tête d'outil.

#### Installation

1. Flashez l'OS sur votre Raspberry Pi en suivant le guide dans `computer_setup_procedure.md`
2. Connectez-vous via SSH à votre Raspberry Pi
3. Clonez le dépôt :
   ```bash
   git clone https://github.com/DeVinci-FabLab/MiniFab
   ```
4. Lancez le script d'installation :
   ```bash
   cd MiniFab/src/scripts && python setup.py
   ```

> [!NOTE]
> Le script d'installation configurera automatiquement Klipper, Moonraker, Mainsail et les autres dépendances nécessaires.

#### Utilisation

Après installation et redémarrage, vous pouvez accéder aux interfaces suivantes :
- Interface Mainsail/Fluidd : `http://[IP_RASPBERRY]:80`
- Interface de monitoring MiniFab : `http://[IP_RASPBERRY]:8000`

Pour changer de mode de fonctionnement :
1. **Automatique** : Connectez simplement la tête d'outil désirée au CAN bus
2. **Manuel** : Utilisez l'interface web MiniFab et cliquez sur le bouton du mode souhaité
3. **Via G-code** : Utilisez la commande `M453 T[1-3]` où :
   - T1 : Mode Fraiseuse CNC
   - T2 : Mode Imprimante 3D
   - T3 : Mode Traceur

### Dépannage

En cas de problèmes avec MiniFab, voici quelques solutions :

1. **La détection d'outil ne fonctionne pas :**
   - Vérifiez les connexions CAN bus
   - Consultez les logs via l'interface web (`http://[IP_RASPBERRY]:8000/logs`)
   - Vérifiez que l'UUID dans la configuration correspond à celui de l'outil

2. **Erreurs après changement de mode :**
   - Redémarrez Klipper via l'interface Mainsail/Fluidd
   - Vérifiez les erreurs dans les logs Klipper

3. **Problèmes de connexion à l'interface :**
   - Vérifiez que les services sont actifs : `systemctl status klipper moonraker`
   - Redémarrez le Raspberry Pi

> [!TIP]
> L'interface de monitoring MiniFab affiche l'état actuel du système et les erreurs récentes, ce qui facilite le diagnostic.

### Plateformes supportées

- **Raspberry Pi** : Testé sur Pi 4
- **Systèmes d'exploitation** : Raspberry Pi OS (Lite), MainsailOS
- **Firmware** : Klipper (testé avec version 0.11.0 et supérieure)
- **Interfaces CAN** : Testé avec les cartes EBB et Octopus BTT

### Fonctionnalités principales

MiniFab offre plusieurs fonctionnalités clés :

1. **Détection automatique d'outils** :
   - Reconnaissance des têtes d'outils via CAN bus
   - Configuration dynamique de la machine
   - Interface utilisateur adaptative

2. **Mode Fraiseuse CNC** :
   - Contrôle précis de la broche (M3/M4/M5)
   - Arrêt d'urgence lié à l'ouverture de porte
   - Procédure assistée de changement d'outil (M6)
   - Paramètres optimisés pour l'usinage

3. **Mode Impression 3D** :
   - Gestion des températures (extrudeur et lit chauffant)
   - Calibration automatique du lit (mesh)
   - Contrôle des ventilateurs
   - Support pour les fonctionnalités avancées de Klipper

4. **Mode Traceur** :
   - Paramètres de mouvement adaptés au dessin
   - Interface utilisateur simplifiée
   - Gestion optimisée des déplacements

5. **Interface web de monitoring** :
   - Surveillance de l'état du système
   - Logs et diagnostics
   - Possibilité de forcer un mode spécifique

6. **Extension des G-codes** :
   - Support de l'axe B (rotation)
   - Commandes spéciales (M453) pour changement de mode
   - Macros personnalisées pour chaque mode

### Améliorations futures

- [ ] Ajout de nouveaux types d'outils (laser, etc.)
- [ ] Amélioration de l'interface utilisateur
- [ ] Optimisation du temps de transition entre les modes
- [ ] Support pour la communication sans fil avec les têtes d'outils
- [ ] Intégration avec des logiciels CAM/CAD
- [x] ~~Détection automatique des outils via CAN~~
- [x] ~~Interface web de monitoring~~

### Contribuer

Si vous souhaitez contribuer au projet, veuillez consulter notre [guide de contribution](./.github/CONTRIBUTING.md) qui détaille le processus de GitFlow, les conventions de commit et les exigences de documentation.

### Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

Développé par DeVinci Fablab - [fablab@devinci.fr](mailto:fablab@devinci.fr)
