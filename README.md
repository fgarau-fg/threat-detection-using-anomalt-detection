# threat-detection-using-anomalt-detection
Rilevamento di anomalie con Isolation Forest in Python utilizzando scikit-learn, applicato a dati di keylogger per identificare comportamenti sospetti.


link: [Sito](https://www.codemag.com/Article/2511031/Threat-Detection-Using-Anomaly-Detection)




Test dell algoritmo isolation forest su dati campione che simulano un log di un siem.
l'algoritmo si basa sulla struttura ad albero, che è a sua volta composta da nodi che contengono l info e i rami che stabiliscono i collegamenti.
questo algoritmo non è supervisionato.

generate-data.py crea:
- i dati normali, ossia relativamente bassi e vicini tra loro, che rappresentano l attivita normale del sistema osservato.
- i dati anomali, in questo caso 200 di default contro i 10000 dei normali. i valori qua sono molto più alti rispetto ai noramali, sono le anomalie che il sistema dovrà trovare. in una situazione con dati normali, queste anomalie sono esattamente uguali, ossia valori outlier su proprietà come login_attempts_per_min,files_accessed_per_min,cpu_usage_avg,network_out_mb,process_count
- un csv finale con i dati combinati. Mescola i dati normali e anomali per avvicinarsi di piu ad un dataset realistico. 


detect-anomalies.py

Per capire come funziona l'isolation tree, supponiamo di avere solamente questi dati: 
| cpu_usage_avg | network_out_mb |
| ------------- | -------------- |
| 10            | 1              |
| 12            | 2              |
| 11            | 1.5            |
| 90            | 50             |

ovviamente l ultima riga dimostra un outlier e lo si puo vedere anche ad occhio umano.
Cosa fa l'Isolation Forest.
prende casualmente una feature, per esempio cpu usage, e poi prende una soglia base, sulla quale poi baserà delle suddivisioni, in altre parole prende un numero a caso nel range che ci troviamo, per esempio 50.
da qua inizia a creare dei gruppi ed andare piu a fondo con le suddivisioni, ma in questo caso in realtà e molto semplice: 
quanti valori stanno sotto la soglia? 3: 10, 11, 12- 
quanti stanno sopra? 1: l'outlier, l'anomalia, già isolata. 

quindi in generale il criterio è questo, se per isolare un valore ci vogliono molte suddivisioni, allora è normalità, se no è un outlier 

questo processo viene fatto su tantissimi sottoinsiemi (alberi) in un dataset e tutti casuali, prendendo in considerazione e in riferimento valori, soglie e feature diverse. 

Albero 1: primo split su cpu_usage_avg, soglia = 50 → [90] isolato subito

Albero 2: primo split su network_out_mb, soglia = 2 → [90] isolato subito

Albero 3: primo split su cpu_usage_avg, soglia = 30 → [90] isolato subito

Per ogni albero:

Si sceglie una feature casuale (es. cpu_usage_avg o network_out_mb)

Si sceglie una soglia casuale per dividere i dati

Ogni punto ha una profondità diversa in ogni albero (quanti split ci vogliono per isolarlo),la profondità media su tutti gli alberi diventa il punteggio reale
