HTML Clones 

HTML Clones este o problema de clustering. O idee initiala de rezolvare a constat in observatia ca similaritatea a 2 pagini <==> cu similaritatea celor 2 arbori asociati celor 2 pagini.
Ideea initiala(care nu a fost implementata) ar fi fost sa parsez fisierele in arbori(similar cu solutia in fapt folosita) si apoi sa construiesc o functie de comparatie a  2 arborii.
Functia respectiva ar returna o valoare intre 0 si 1. 
Algoritmul respectiv ar fi comparat arborii 2 cate 2, si in momentul in care o comparatie ar fi trecut peste un threshold atunci aveam un cluster nou.
Problema cu aceasta abordare consta in faptul ca, functia de comparatie e greu de gasit in practica(ce presupune aceasta ?). Comparatie dupa structura ierarhica/styling etc.. ? Comparatia dupa structura ierarhica este destul de realizat,
folosind un algoritm de parcurgere precum BFS, dar verifica styling-ului impiedica tragerea unor concluzii relevante. De asemenea faptul ca 2 arborii au o structura ierarhica similara nu inseamna intodeauna ca vom avea aceleasi 2 pagini din punct de vedere vizual.
Se poate emula aceeasi parte vizuala cu elemente diferite sau mai putine.

O doua abordare ar fi, pentru functia de comparatie, in loc sa comparam cei 2 arbori, sa comparam matricea de pixeli a celor 2 pagini(sa fie facute screenshot-uri). Aceasta abordare desi pe langa faptul ca ar fi destul de ineficienta
, dar usor de implementat, culorile ar impiedica o comparatie obiectiva corecta. Daca o pagina identica ar avea dark mode, faptul ca pixeli sunt flipped, ar rezulta o similaritate 0, desi pagina e identica.





