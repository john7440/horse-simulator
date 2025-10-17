
# 🏇 Horse Race Simulator

Une **simulation interactive** de **course de chevaux** en terminal, avec **affichage dynamique**, gestion des vitesses, disqualifications, et **classement final** avec médailles.

### 📦 Fonctionnalités
- Simulation **tour par tour avec lancer de dé**

- **Vitesse dynamique** selon les performances précédentes

- **Disqualification possible** selon les règles de course

- **Affichage coloré et visuel** de la progression

- **Classement final avec médailles** 🥇🥈🥉

### 🚀 Pour lancer le programme
Assurez-vous d’avoir **installé colorama** :

    pip install colorama
**Puis** :

    python horse_race.py

### 🎮 Instructions utilisateur
1. Choisir le **nombre de chevaux** (entre 12 et 20)
2. Choisir le **type de résultat** :
- 3 → Tiercé
- 4 → Quarté
- 5 → Quinté
3. Appuyez sur **Entrée** à chaque tour pour avancer
4. Tapez **Q pour quitter** la course à tout moment


### 🧠 Règles de la simulation
- **Chaque cheval** commence avec une **vitesse de 0** (à l'arrêt)
- Un **dé (1-6)** est **lancé aléatoirement à chaque tour** pour chaque cheval
- La **vitesse est modifiée selon des règles prédéfinies**
- **Si un cheval atteint une vitesse trop élevée** avec un 'mauvais lancer', il **peut être disqualifié**
- **La course se termine quand tous les chevaux ont terminé ou sont disqualifiés**

### 📊 Classement final
- Les **chevaux sont classés par ordre d’arrivée**
- Les **3 premiers reçoivent une médaille**
- Si le **nombre de chevaux disqualifié est trop élevé** pour le résultat final,
    les chevaux auront la **mention 'Did Not Finished'** pour indiquer qu'ils n'ont pas terminé la course.

### 🧱 Structure du code
- **main()** : point d’entrée
- **generate_list()** : initialise les chevaux
- **kind_of_result()** / how_many_horses() : interactions utilisateur
- **simulate_course()** : logique de course
- **format_horse_bar()** : formatage individuel
- **display_race()** : affichage visuel
- **final_ranking()** : classement et médailles

