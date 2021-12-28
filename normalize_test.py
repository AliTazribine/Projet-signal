import Utils

signal = [454, 667, 78786, 877, 675]
normalized_sig=Utils.normalize(signal)
normalized = True
for i in normalized_sig:
    if(i>1 or i<-1):
        normalized = False
if(normalized):
    print("Le signal est bien normalisé")
else :
    print("il y'a une erreur")
