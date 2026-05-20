🏹 Ballistic Simulator for Archers
Simulatore Balistico per Tiro con l’Arco – Versione Internazionale

https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/React-18.2-61dafb
https://img.shields.io/badge/jsPDF-2.5.1-red
https://img.shields.io/badge/status-stable-brightgreen

Calcolo balistico avanzato per frecce con modello aerodinamico RK4, correzione posturale, generazione automatica della scala mirino (tabella + grafico), supporto bilingue (ITA/ENG) e doppio sistema di unità (metrico/imperiale).

✨ Funzionalità principali
Fisica realistica – Drag dipendente da Reynolds, effetto dell’angolo d’attacco, influenza di punta e impennatura, instabilità da spine e FOC.

Calcolo ottimale dell’angolo di mira – Ricerca automatica dell’angolo che centra il bersaglio (anche con bersaglio in altura o in depressione).

Correzione posturale – Altezza di lancio variabile in base all’angolo di tiro (rotazione del bacino dell’arciere).

Geometria del mirino – Generazione di una tabella personalizzata (drop, proiezione sul riser, energia residua, velocità) e scala visiva interattiva.

Grafici interattivi – Traiettoria (reale, ideale, linea di mira), velocità, energia residua, drop. Tooltip al passaggio del mouse.

Esportazione – Scala mirino in PDF (con disegno proporzionale del mirino) e in CSV.

Internazionalizzazione completa –

Lingue: 🇮🇹 Italiano / 🇬🇧 English

Unità di misura: metrico (m, cm, m/s, J, hPa, °C) / imperiale (yd, in, ft/s, ft·lb, inHg, °F)

Tutti i campi input/output, i grafici e il PDF si adattano automaticamente.

Tema chiaro/scuro – Rispetta le preferenze dell’utente.

🖥️ Demo live
👉 Clicca per provare il simulatore online
(sostituisci con il link della tua GitHub Pages o Netlify)

📦 Tecnologie utilizzate
React 18 (hooks + context per i18n)

jsPDF – generazione PDF della scala mirino

SVG interattivo – grafici con tooltip e gestione personalizzata delle unità

Modello fisico originale – RK4 adattivo, drag dipendente dal numero di Reynolds, modello di instabilità dello spine

🚀 Come utilizzare (locale)
Clona il repository

bash
git clone https://github.com/tuo-username/ballistic-simulator.git
cd ballistic-simulator
Apri il file index.html nel browser (non serve compilazione, è HTML/JS puro).

Opzionale – Per modificare il codice puoi usare un server locale (es. npx serve .).

🧪 Parametri di input e output
Input (sempre metrici internamente, ma convertibili all’istante)

Freccia: peso, lunghezza, diametro, spine, peso punta, bilanciamento, tipo punta, impennatura

Arco: forza (lb), allungo, brace height, offset incocco, tipo, efficienza

Bersaglio: distanza, altezza, possibilità di usare v₀ misurata

Biometria arciere: altezza sgancio neutra, altezza bacino, lunghezza spalla‑aggancio, correzione posturale

Ambiente: vento, temperatura, pressione, umidità, altitudine

Mirino: distanza occhio‑cocca, cocca‑riser, distanza minima/massima, passo

Output

Angolo di mira, velocità iniziale, tempo di volo, altezza massima, drop al bersaglio, gittata massima

Tabella completa della scala mirino (distanza, drop, proiezione sul riser, energia, velocità)

Scala visiva del mirino (con laser a 30 m e tacche di distanza)

Grafici convertiti nell’unità selezionata

📁 Struttura del repository
text
ballistic-simulator/
├── index.html          # App completa (React + fisica + stili)
├── README.md           # Questa descrizione
├── LICENSE             # MIT
└── assets/             # (opzionale) screenshot
🤝 Contributi
Sono benvenuti suggerimenti, segnalazioni di bug e pull request.
In particolare:

Aggiunta di altre lingue

Modelli di drag più raffinati (es. effetto vento laterale sul piano orizzontale)

Supporto per archi compound con modulo di rilascio a camme

Salvataggio delle preferenze (localStorage)

📄 Licenza
Distribuito sotto licenza MIT. Sentiti libero di usarlo, modificarlo e incorporarlo nei tuoi progetti.

🙏 Crediti
Modello fisico e codice originale: Cesare Pagura

Internazionalizzazione, miglioramenti UI/UX e integrazione PDF: Claude (Anthropic)

Librerie: React, jsPDF

📬 Contatti
Per domande o proposte:
📧 [tua-email@example.com]
🐦 [@tuo_twitter] (opzionale)
