# Posty na LinkedIn

Wrzuć post w dniu publikacji wpisu (cron publikuje o 6:10). Link w poście prowadzi do artykułu; obrazek podglądu wczyta się sam.

## 2026-09-16 · ClickFix i fałszywa CAPTCHA: jak działa atak i jak go usunąć ze strony

https://empirecorporation.eu/blog/clickfix-falszywa-captcha/

Fałszywa CAPTCHA nie łamie żadnych zabezpieczeń. Prosi, żebyś zrobił to sam.

Niedawno usuwaliśmy ClickFix ze strony klienta, więc zebrałem w jednym miejscu to, co warto wiedzieć:

- Kliknięcie „Nie jestem robotem” po cichu kopiuje polecenie do schowka, a strona każe nacisnąć Win+R, Ctrl+V i Enter.
- Nakładki siedzą głównie na przejętych stronach WordPress: w fałszywych wtyczkach, plikach motywu i bazie danych.
- Administrator często ich nie widzi, bo kod pomija zalogowanych użytkowników.
- Na końcu łańcucha są infostealery i trojany zdalnego dostępu. CERT Polska opisał firmę, w której jedno wklejone polecenie otworzyło drogę narzędziom poprzedzającym ransomware.
- ESET odnotował wzrost wykryć ClickFix o ponad 500% w pierwszej połowie 2025 r.

W artykule: jak sprawdzić i wyczyścić stronę oraz co zrobić po wklejeniu polecenia.

https://empirecorporation.eu/blog/clickfix-falszywa-captcha/

#cyberbezpieczeństwo #WordPress #ClickFix #malware

---

## 2026-09-16 · Czym jest MCP (Model Context Protocol)? Serwer MCP w praktyce

https://empirecorporation.eu/blog/czym-jest-mcp-model-context-protocol/

Jeśli podłączasz AI do systemów firmy, MCP (Model Context Protocol) przestał być opcją dla entuzjastów.

Co warto wiedzieć w 2026 roku:
- jeden serwer MCP dla CRM-a czy systemu zgłoszeń działa z Claude, ChatGPT, Copilotem i własnymi agentami,
- od grudnia 2025 protokół rozwija się w Agentic AI Foundation pod Linux Foundation, współtworzonej przez Anthropic, OpenAI i Block,
- specyfikacja z lipca 2026 uczyniła MCP bezstanowym, więc serwer skaluje się jak zwykła usługa HTTP,
- główne ryzyka to złośliwe serwery (tool poisoning) i zbyt szerokie uprawnienia,
- przy jednej aplikacji z trzema funkcjami MCP często nie jest potrzebny.

W artykule tłumaczę architekturę, pokazuję działający serwer w TypeScript i listę kontrolną bezpieczeństwa:
https://empirecorporation.eu/blog/czym-jest-mcp-model-context-protocol/

#MCP #AI #agenciAI #bezpieczeństwo #TypeScript

---

## 2026-09-16 · Czym jest RAG i jak podłączyć AI do dokumentów firmy

https://empirecorporation.eu/blog/czym-jest-rag/

Model AI nie zna Twoich procedur, umów ani dokumentacji. Kiedy o nie pytasz, zgaduje. RAG to sposób, żeby przestał.

Najważniejsze wnioski z wdrożeń RAG:
- jakość zależy głównie od wyszukiwania, a nie od wyboru modelu,
- samo wyszukiwanie wektorowe gubi numery umów i kody produktów, dlatego potrzebne jest wyszukiwanie hybrydowe,
- uprawnienia egzekwuje się przy wyszukiwaniu, a nie zdaniem w prompcie,
- skany PDF i tabele to najczęstsze źródło złych odpowiedzi,
- bez zestawu prawdziwych pytań testowych każda poprawka to strzał w ciemno.

Opisałem, jak działa RAG krok po kroku, porównanie z fine-tuningiem i realistyczny plan wdrożenia:
https://empirecorporation.eu/blog/czym-jest-rag/

#RAG #AI #LLM #bazaWiedzy #AIwFirmie

---

## 2026-09-19 · Jak wdrożyć AI w firmie krok po kroku

https://empirecorporation.eu/blog/jak-wdrozyc-ai-w-firmie/

Większość nieudanych wdrożeń AI, które widzę, zaczęła się od pytania „jakie narzędzie kupić”. To zła kolejność.

Co działa w praktyce:
- wybierz 2-3 powtarzalne procesy, w których da się zmierzyć czas i liczbę błędów,
- zanim ktokolwiek wklei dane do czatu, spisz, co wolno wprowadzać do jakich narzędzi,
- daj ludziom zatwierdzone narzędzie na planie biznesowym, bo zakaz kończy się prywatnymi kontami,
- zmierz stan wyjściowy przed pilotażem i ustal kryteria decyzji,
- pamiętaj o AI Act: obowiązek dbania o kompetencje pracowników nadal obowiązuje, choć po zmianach z 2026 roku jest łagodniejszy.

W artykule plan na 30, 60 i 90 dni, role w zespole i lista kosztów, które łatwo pominąć:
https://empirecorporation.eu/blog/jak-wdrozyc-ai-w-firmie/

#AI #wdrożenieAI #AIAct #transformacjacyfrowa #zarządzanie

---

## 2026-09-22 · Zainfekowana strona WordPress: objawy i co zrobić w pierwszej godzinie

https://empirecorporation.eu/blog/zainfekowany-wordpress-objawy/

Pierwsza reakcja na zainfekowany WordPress to zwykle kasowanie podejrzanych plików. To błąd, który utrudnia całą resztę.

Co robić w pierwszej godzinie po wykryciu włamania:

- Zapisz objawy i godzinę, zrób zrzuty ekranu.
- Zrób kopię plików i bazy w obecnym, zainfekowanym stanie. Bez niej nie ustalisz, jak przestępca wszedł.
- Odetnij ruch na poziomie serwera, żeby strona przestała szkodzić odwiedzającym.
- Zmień hasła do hostingu, SFTP, bazy i WordPressa, ale z czystego komputera.
- Pobierz logi serwera, zanim zostaną nadpisane.
- Jeśli wyciekły dane osobowe, pamiętaj o 72 godzinach na zgłoszenie do UODO.

Od czego zależy, czy potrzebny jest specjalista, i jakie objawy wskazują na infekcję, opisałem tutaj:

https://empirecorporation.eu/blog/zainfekowany-wordpress-objawy/

#WordPress #cyberbezpieczeństwo #reagowanienaincydenty

---

## 2026-09-25 · Agent AI do obsługi e-maili: jak to działa i jak wdrożyć

https://empirecorporation.eu/blog/agent-ai-skrzynka-email/

Agent AI do obsługi maili nie powinien sam wysyłać odpowiedzi klientom. Powinien za to zdjąć z zespołu sortowanie i przepisywanie danych.

Co działa w praktyce:
- klasyfikacja maili ze skrzynek współdzielonych: faktury, reklamacje, leady, zgłoszenia serwisowe,
- ekstrakcja danych do JSON-a z walidacją w kodzie, zanim cokolwiek trafi do ERP,
- szkice odpowiedzi z bazy wiedzy i CRM, zatwierdzane przez pracownika,
- minimalne uprawnienia: w Gmail API nawet zakres do szkiców pozwala wysyłać pocztę, więc blokadę trzeba zrobić samemu,
- ochrona przed prompt injection, bo każdego maila pisze ktoś z zewnątrz.

Cały przepływ krok po kroku, z przykładowym JSON-em i listą metryk: https://empirecorporation.eu/blog/agent-ai-skrzynka-email/

#AI #automatyzacja #AgenciAI #cyberbezpieczenstwo

---

## 2026-09-28 · Ile kosztuje aplikacja mobilna w 2026? Od czego zależy cena

https://empirecorporation.eu/blog/ile-kosztuje-aplikacja-mobilna-2026/

„Ile kosztuje aplikacja mobilna?” Uczciwa odpowiedź brzmi: tyle, ile godzin pracy wymaga zakres, pomnożone przez stawkę. Widełki bez zakresu niewiele mówią.

Co najmocniej zmienia budżet:
- jedna czy dwie platformy i wybór między natywną a cross-platform,
- backend i panel administracyjny, o których klienci często zapominają,
- płatności, tryb offline, funkcje w czasie rzeczywistym i integracje ze starymi systemami,
- koszty po premierze: Apple Developer Program to 99 USD rocznie, Google Play 25 USD jednorazowo, do tego prowizje, hosting i coroczne dostosowanie do wymagań sklepów (np. API 36 w Google Play od 31 sierpnia 2026 r.).

W artykule pokazuję przykładową wycenę krok po kroku (z wyraźnie założonymi liczbami) i tabelę: funkcja a wpływ na koszt.

https://empirecorporation.eu/blog/ile-kosztuje-aplikacja-mobilna-2026/

#aplikacjemobilne #MVP #iOS #Android

---

## 2026-10-01 · AI Act 2026: obowiązki firm po zmianach z Digital Omnibus

https://empirecorporation.eu/blog/ai-act-2026-obowiazki-firm/

Termin 2 sierpnia 2026 r. dla systemów AI wysokiego ryzyka już nie obowiązuje. Wiele firm wciąż planuje według starego harmonogramu.

Co zmieniło się w AI Act w 2026 roku:
- Digital Omnibus (rozporządzenie 2026/1744) przesunął obowiązki dla systemów z załącznika III na 2 grudnia 2027 r.,
- obowiązki przejrzystości dla chatbotów i deepfake’ów stosuje się od 2 sierpnia 2026 r.,
- obowiązek dotyczący kompetencji w zakresie AI złagodzono, ale nie usunięto,
- w Polsce powstaje organ nadzoru KRiBSI, a przepisy o kontrolach i karach stosuje się od 28 października 2026 r.,
- zakazane praktyki obowiązują od lutego 2025 r., a kary sięgają 7 procent światowego obrotu.

Harmonogram, role, kategorie ryzyka i checklista dla firm korzystających z AI:
https://empirecorporation.eu/blog/ai-act-2026-obowiazki-firm/

#AIAct #sztucznainteligencja #compliance #prawonowychtechnologii #AI

---

## 2026-10-04 · Automatyzacje AI w 2026: przykłady, które działają w firmach

https://empirecorporation.eu/blog/automatyzacje-ai-2026-przyklady/

Automatyzacja AI, która działa, rzadko wygląda jak autonomiczny agent z filmu. Zwykle to model, który czyta dokument, i człowiek, który klika „zatwierdź”.

Zebrałem 18 przykładów z podziałem na działy. Kilka wniosków:
- najszybciej zwracają się klasyfikacja zgłoszeń, notatki do CRM i szkice odpowiedzi,
- liczby w raportach mają pochodzić z zapytań do danych, model tylko je komentuje,
- faktury z KSeF to XML, więc tu wygrywa zwykły parser, a AI zostaje dla dokumentów spoza systemu,
- wstępna ocena CV to system wysokiego ryzyka według AI Act,
- n8n, Make, Zapier i Power Automate obsługują już agentów i MCP.

Przy każdym przykładzie: narzędzia, poziom nadzoru i realna trudność:
https://empirecorporation.eu/blog/automatyzacje-ai-2026-przyklady/

#automatyzacja #AI #n8n #agenciAI #AIwFirmie

---

## 2026-10-07 · Infostealer: jak działają Lumma, StealC i Vidar i co zrobić po infekcji

https://empirecorporation.eu/blog/lumma-stealer-infostealery/

Zmieniłeś hasło po infekcji infostealerem? To dopiero połowa roboty.

Infostealery takie jak Lumma, StealC i Vidar kradną nie tylko hasła, ale też ciasteczka sesyjne. A skradziona sesja to logowanie, które już przeszło MFA.

Co z tego wynika w praktyce:

- Hasła zmieniaj z czystego urządzenia, nigdy z zainfekowanego komputera.
- Zacznij od poczty e-mail, bo przez nią resetuje się resztę kont.
- Po każdej zmianie hasła wyloguj wszystkie sesje i sprawdź, czy nikt nie dodał własnej metody MFA.
- Nie zapominaj o kluczach API, tokenach GitHuba i danych do hostingu.
- Przejęcie infrastruktury Lumma w maju 2025 r. nie rozwiązało problemu: według Flashpoint w pierwszej połowie 2026 r. infostealery zebrały 1,7 mld danych logowania.

Pełna kolejność działań i sposoby wykrywania w firmie:

https://empirecorporation.eu/blog/lumma-stealer-infostealery/

#cyberbezpieczeństwo #infostealer #MFA #bezpieczeństwoIT

---

## 2026-10-10 · Chaos w IT firmy: jak go opanować, zanim coś się zepsuje

https://empirecorporation.eu/blog/chaos-w-it-jak-opanowac/

Hasła w arkuszu, domena na prywatnej karcie i jeden administrator, który wie wszystko. Tak zwykle wygląda chaos w IT firmy, zanim coś się zepsuje.

Plan na uporządkowanie nie wymaga wielkiego wdrożenia:
- spisz domeny, serwery, konta SaaS, umowy i to, kto ma do czego dostęp (faktury z 12 miesięcy pokażą zapomniane usługi),
- wdróż menedżer haseł, MFA na kontach administracyjnych i listę kroków przy odejściu pracownika lub dostawcy,
- sprawdź, czy kopię zapasową da się faktycznie odtworzyć,
- zamień wiedzę z głowy na runbooki i konfigurację opisaną kodem,
- wyznacz właściciela i comiesięczny przegląd.

Do tego NIS2: nowelizacja ustawy o KSC obowiązuje od 3 kwietnia 2026 r., a wnioski o wpis do wykazu trzeba złożyć do 3 października.

Cały plan z tabelą „co spisać w pierwszym tygodniu”: https://empirecorporation.eu/blog/chaos-w-it-jak-opanowac/

#IT #cyberbezpieczeństwo #NIS2 #zarządzanieIT

---

## 2026-10-13 · Automatyczne code review z AI: jak ustawić to w zespole

https://empirecorporation.eu/blog/automatyczne-code-review-ai/

AI w code review nie zastąpi seniora, ale może sprawić, że senior przestanie tracić czas na rzeczy, które maszyna wyłapie szybciej.

Co z naszego doświadczenia daje najwięcej:
- plik z zasadami review w repozytorium (AGENTS.md, CLAUDE.md, REVIEW.md albo copilot-instructions.md), zamiast promptu w głowie jednej osoby,
- jasna definicja błędu blokującego i limit drobnych uwag, bo inaczej zespół zacznie ignorować komentarze bota,
- wyłączenie z review wszystkiego, czego pilnuje linter i CI,
- merge zawsze zatwierdza człowiek; narzędzia takie jak Copilot czy Claude Code domyślnie nie liczą się do wymaganych zatwierdzeń,
- metryki: czas do pierwszej recenzji i błędy, które mimo review trafiły na produkcję.

Przykładowy workflow GitHub Actions i porównanie narzędzi: https://empirecorporation.eu/blog/automatyczne-code-review-ai/

#CodeReview #DevOps #AI #SoftwareEngineering

---

## 2026-10-16 · Publikacja aplikacji w Google Play w 2026: konto, weryfikacja i testy

https://empirecorporation.eu/blog/publikacja-aplikacji-google-play/

Aplikacja gotowa, a publikacja w Google Play stoi tygodniami. Zwykle nie przez kod, tylko przez formalności, o których nikt nie pomyślał wcześniej.

Na co zwrócić uwagę w 2026 r.:
- konto firmowe wymaga numeru D-U-N-S, a jego uzyskanie może potrwać do 30 dni,
- nowe konta osobiste muszą przed produkcją przeprowadzić test zamknięty: min. 12 testerów zapisanych nieprzerwanie przez 14 dni,
- od 31 sierpnia 2026 r. nowe aplikacje i aktualizacje muszą celować w API 36 (Android 16),
- Data safety i polityka prywatności są obowiązkowe nawet dla aplikacji, które nie zbierają danych,
- sprawdzenie aplikacji może potrwać do 7 dni, więc zaplanuj zapas przed premierą.

Pełny poradnik z checklistą przed kliknięciem „Opublikuj”: https://empirecorporation.eu/blog/publikacja-aplikacji-google-play/

#GooglePlay #Android #aplikacjemobilne #PlayConsole

---

## 2026-10-19 · Wdrożenie Wazuh w małej firmie: architektura, tuning i typowe błędy

https://empirecorporation.eu/blog/wazuh-wdrozenie-mala-firma/

Wazuh instaluje się jednym skryptem. Problemy zaczynają się tydzień później, gdy kanał z alertami ma kilka tysięcy wiadomości i nikt ich nie czyta.

Co sprawdza się przy wdrożeniu w małej firmie:
- instalacja all-in-one wystarczy do około 100 agentów (dokumentacja 4.14: 8 vCPU, 8 GiB RAM, 200 GB na 90 dni),
- klaster indexera od trzech węzłów, nigdy dwóch,
- hasło rejestracji agentów i przypięta wersja agenta,
- wyciszanie konkretnych źródeł regułą z poziomem 0 zamiast wyłączania całych reguł,
- dashboard i API tylko z sieci administracyjnej, alert na rozłączonego agenta.

Pełny poradnik z konfiguracją, integracją z Suricatą i listą typowych błędów:
https://empirecorporation.eu/blog/wazuh-wdrozenie-mala-firma/

#Wazuh #SIEM #cyberbezpieczeństwo #opensource #bezpieczeństwoIT

---

## 2026-10-22 · Zewnętrzny CTO (fractional CTO): kiedy się opłaca i czego oczekiwać

https://empirecorporation.eu/blog/zewnetrzny-cto-kiedy-sie-oplaca/

Zewnętrzny CTO nie jest tańszym programistą. To osoba, która po Twojej stronie stołu podejmuje decyzje technologiczne i pilnuje dostawców.

Kiedy fractional CTO ma sens:
- jesteś nietechnicznym założycielem i nie umiesz ocenić estymacji software house’u,
- produkt robi zewnętrzna firma, która sama ocenia jakość swojej pracy,
- szykujesz się do rozmów z inwestorem i due diligence,
- poprzedni projekt przekroczył budżet i trzeba zdecydować, co ratować.

Czego pilnować przy wyborze: konkretnego zakresu w umowie, jawnych zasad przy konflikcie interesów, dokumentowania decyzji i miar ustalonych na starcie (np. metryki DORA, koszty chmury, lista zamkniętych ryzyk).

Cały przewodnik z porównaniem etatowego CTO, fractional CTO i tech leada software house’u: https://empirecorporation.eu/blog/zewnetrzny-cto-kiedy-sie-oplaca/

#CTO #FractionalCTO #startup #softwarehouse

---

## 2026-10-25 · Specyfikacja projektu i user stories z AI: od notatek do backlogu

https://empirecorporation.eu/blog/specyfikacja-i-user-stories-z-ai/

Najlepsze, co AI robi przy specyfikacji projektu, to nie pisanie wymagań, tylko wskazywanie, czego jeszcze nie ustaliliście.

Jak to wygląda w praktyce:
- transkrypcja spotkania zamieniona w listę decyzji, wymagań i otwartych pytań, każda pozycja ze znacznikiem czasu,
- user stories z kryteriami akceptacji w Gherkin, także po polsku (Zakładając, Jeżeli, Wtedy),
- automatyczne wyłapywanie sprzeczności i brakujących wymagań niefunkcjonalnych,
- zadania w Jirze lub Linearze zakładane przez MCP jako szkice, nie od razu do sprintu,
- specyfikacja w repozytorium, zmieniana przez pull requesty.

Przykład: od fikcyjnej notatki ze spotkania do gotowej historii z kryteriami: https://empirecorporation.eu/blog/specyfikacja-i-user-stories-z-ai/

#ProductManagement #AI #Agile #UserStories

---

## 2026-10-28 · Strona oznaczona jako niebezpieczna w Google: jak usunąć ostrzeżenie

https://empirecorporation.eu/blog/ostrzezenie-google-strona-niebezpieczna/

Czerwony ekran „Niebezpieczna strona” w Chrome potrafi w jeden dzień wyzerować ruch z firmowej witryny.

Jak z tego wyjść:

- Przyczynę sprawdzisz w Search Console, w raporcie „Problemy dotyczące bezpieczeństwa”. Są tam typ problemu i przykładowe adresy URL.
- Najpierw wyczyść całą witrynę i usuń przyczynę włamania, dopiero potem kliknij „Poproś o sprawdzenie”.
- W prośbie opisz, co znalazłeś, co usunąłeś i jak załatałeś lukę.
- Według dokumentacji Google phishing jest weryfikowany zwykle w około dobę, malware w kilka dni, a spam po włamaniu nawet kilka tygodni.
- Nie wysyłaj prośby na zapas. Powtarzane odrzucenia mogą zablokować kolejne próby na 30 dni.

Pełna instrukcja krok po kroku:

https://empirecorporation.eu/blog/ostrzezenie-google-strona-niebezpieczna/

#SEO #cyberbezpieczeństwo #SearchConsole #WordPress

---

## 2026-10-31 · Aplikacja natywna czy cross-platform? React Native, Flutter, KMP

https://empirecorporation.eu/blog/natywna-czy-cross-platform/

Natywna czy cross-platform? W 2026 roku to już nie jest wybór między „szybko” a „dobrze”, tylko między różnymi kompromisami.

Kilka faktów, które warto znać przed decyzją:
- React Native od wersji 0.82 działa wyłącznie na nowej architekturze, a dokumentacja rekomenduje start z Expo,
- Flutter 3.44 przeszedł na Swift Package Manager na iOS, ale nowy wygląd iOS 26 (Liquid Glass) nie trafił do rdzenia biblioteki Cupertino,
- Kotlin Multiplatform jest oficjalnie wspierany przez Google, a Compose Multiplatform na iOS jest stabilny od maja 2025 r.,
- Bluetooth, AR i praca w tle nadal oznaczają sporo kodu natywnego, niezależnie od frameworka.

W artykule: tabela porównawcza i krótki przewodnik „wybierz X, jeśli…”.

https://empirecorporation.eu/blog/natywna-czy-cross-platform/

#ReactNative #Flutter #KotlinMultiplatform #iOS #Android

---

## 2026-11-03 · Prompt injection i bezpieczeństwo agentów AI: zagrożenia i obrona

https://empirecorporation.eu/blog/prompt-injection-bezpieczenstwo-agentow-ai/

Agent AI, który czyta firmową pocztę i może wysyłać e-maile, wykona polecenie z każdej wiadomości, jeśli ktoś sprytnie je tam ukryje.

To prompt injection, pierwsze ryzyko na liście OWASP Top 10 dla aplikacji LLM. Co warto wiedzieć:
- brytyjskie NCSC ostrzega, że tego problemu może nie dać się w pełni wyeliminować,
- najgroźniejsze jest połączenie: dostęp do prywatnych danych, niezaufane treści i możliwość komunikacji na zewnątrz,
- serwery MCP dokładają ryzyka: zatrute opisy narzędzi i zbyt szerokie uprawnienia,
- filtr w prompcie systemowym nie wystarczy, potrzebne są minimalne uprawnienia, zatwierdzanie akcji i allow-listy,
- agenta testuj tak jak aplikację: zestawem przypadków w CI i regularnym red teamingiem.

Pełny przewodnik z checklistą:
https://empirecorporation.eu/blog/prompt-injection-bezpieczenstwo-agentow-ai/

#AI #cyberbezpieczeństwo #LLM #MCP #OWASP

---

## 2026-11-06 · Automatyczne raporty z AI: agent, który co tydzień zrobi podsumowanie

https://empirecorporation.eu/blog/automatyczne-raporty-ai/

Automatyczny raport z AI ma jedną twardą zasadę: model językowy nie liczy żadnej liczby.

Jak to budujemy:
- harmonogram uruchamia pobranie danych z CRM, Jiry, GA4 czy Wazuha przez API,
- wszystkie wskaźniki i porównania liczy SQL lub kod,
- model pisze tylko komentarz i wskazuje anomalie, używając nazwanych miejsc na liczby, które kod potem wypełnia,
- raport ma sekcję o stanie danych: źródła, godzinę pobrania, braki,
- zanim trafi do zarządu, przegląda go właściciel danych.

Najczęstszy błąd, jaki widzimy: pusta odpowiedź API potraktowana jak zero i komentarz o dramatycznym spadku sprzedaży.

Przykładowa struktura raportu i lista pułapek: https://empirecorporation.eu/blog/automatyczne-raporty-ai/

#AI #Raportowanie #Automatyzacja #BusinessIntelligence

---

## 2026-11-09 · Fałszywa aktualizacja przeglądarki (SocGholish): jak działa i co robić

https://empirecorporation.eu/blog/socgholish-falszywa-aktualizacja-przegladarki/

Komunikat „Twoja przeglądarka jest nieaktualna” na stronie lokalnej firmy może być początkiem ataku ransomware.

Tak od lat działa SocGholish, znany też jako FakeUpdates:

- Przestępcy wstrzykują skrypt na legalne strony, najczęściej WordPress, często logując się skradzionym hasłem administratora.
- Przynęta pokazuje się tylko wybranym odwiedzającym, więc właściciel strony zwykle jej nie widzi.
- Pobrany plik to skrypt JavaScript, który zbiera informacje o komputerze i sieci firmowej.
- Red Canary odnotował w 2025 r. drugi etap ataku w mniej więcej co czwartym incydencie, m.in. trojany zdalnego dostępu i stealery.
- W czerwcu 2026 r. Operacja Endgame oczyściła 14 971 zainfekowanych stron.

W artykule: jak sprawdzić swoją stronę, jak ją wyczyścić i co zrobić, jeśli ktoś uruchomił plik.

https://empirecorporation.eu/blog/socgholish-falszywa-aktualizacja-przegladarki/

#cyberbezpieczeństwo #WordPress #SocGholish #ransomware

---

## 2026-11-12 · Jak ocenić ofertę software house’u i nie przepłacić

https://empirecorporation.eu/blog/jak-ocenic-oferte-software-house/

Najdroższa oferta software house’u to często ta najtańsza, która nie ma w wycenie testów, utrzymania i przeniesienia praw do kodu.

Na co patrzę, gdy klient prosi o drugą opinię:
- czy zakres ma założenia i wyłączenia, a wycena jest rozbita na moduły i role,
- czy są osobne pozycje na QA, środowisko testowe i wdrożenie,
- czy repozytorium, chmura i konta w sklepach będą na koncie klienta od pierwszego dnia,
- czy umowa przenosi autorskie prawa majątkowe na piśmie i wymienia pola eksploatacji,
- czy harmonogram uwzględnia discovery, testy i odbiory, czy tylko programowanie.

W artykule tabela do porównania trzech ofert i lista pytań do zadania przed podpisaniem umowy:
https://empirecorporation.eu/blog/jak-ocenic-oferte-software-house/

#softwarehouse #IT #zarządzanieprojektami #CTO #aplikacje

---

## 2026-11-15 · AI w wytwarzaniu oprogramowania: szybszy zespół bez utraty jakości

https://empirecorporation.eu/blog/sdlc-z-ai-szybszy-zespol/

Doświadczeni programiści w badaniu METR z 2025 roku pracowali z AI o 19% dłużej, a mimo to byli przekonani, że przyspieszyli o 20%.

To dobry powód, żeby wdrażać AI w zespole z metrykami, a nie na wyczucie. Co pokazują badania i praktyka:
- DORA 2025: więcej AI to wyższa przepustowość, ale też większa niestabilność wdrożeń,
- AI wzmacnia to, co już masz: małe zmiany, testy i przegląd kodu decydują o wyniku,
- kod od AI przechodzi te same skanery i review co kod pisany ręcznie,
- w każdej fazie SDLC człowiek zatwierdza zakres, merge i wdrożenie,
- efekt mierzysz metrykami DORA na tle danych sprzed pilotażu.

Przewodnik faza po fazie, z tabelą odpowiedzialności: https://empirecorporation.eu/blog/sdlc-z-ai-szybszy-zespol/

#SoftwareEngineering #DORA #AI #DevOps #EngineeringManagement

---

## 2026-11-18 · Strona przekierowuje na inną stronę? Japoński spam SEO i naprawa

https://empirecorporation.eu/blog/japonski-spam-seo-przekierowania/

Jeśli Twoja strona przekierowuje klientów na obcą domenę, a Ty tego nie widzisz, to nie przypadek. Tak działa cloaking w infekcjach typu japoński spam SEO.

Co sprawdzić:
- kod często uruchamia się tylko dla telefonów, wejść z Google albo Googlebota i pomija zalogowanych administratorów,
- kryje się w .htaccess, functions.php, mu-plugins i tabeli wp_options,
- atakujący potrafi dodać się jako właściciel w Search Console i podmienić mapę witryny,
- narzędzie Usunięcia ukrywa adresy tylko na około 6 miesięcy, trwałe usunięcie wymaga kodów 404 lub 410,
- bez usunięcia backdoora spam wraca.

Pełna procedura krok po kroku: https://empirecorporation.eu/blog/japonski-spam-seo-przekierowania/

#cyberbezpieczeństwo #WordPress #SEO #malware

---

## 2026-11-21 · Test penetracyjny strony, aplikacji i API: jak wygląda krok po kroku

https://empirecorporation.eu/blog/test-penetracyjny-jak-wyglada/

Skan podatności i test penetracyjny to dwie różne usługi, a w ofertach często są mylone.

Skaner znajdzie brakującą aktualizację. Nie znajdzie tego, że po zmianie numeru w adresie klient widzi cudze zamówienie. Co warto wiedzieć przed zleceniem testu:
- zakres i zasady spisz przed pierwszym żądaniem testera,
- grey box zwykle daje więcej konkretów w tym samym czasie niż black box,
- pytaj o metodykę: OWASP WSTG, MASTG dla mobile, API Security Top 10 dla API,
- raport bez dowodów, rekomendacji i retestu to tylko PDF,
- znowelizowana ustawa o KSC obowiązuje od 3 kwietnia 2026, a termin wniosku o wpis do wykazu mija 3 października.

Jak wygląda test krok po kroku: https://empirecorporation.eu/blog/test-penetracyjny-jak-wyglada/

#pentest #cyberbezpieczeństwo #OWASP #NIS2

---

## 2026-11-24 · Suricata IDS/IPS: poradnik wdrożenia, reguły i integracja z SIEM

https://empirecorporation.eu/blog/suricata-ids-ips-poradnik/

Suricata potrafi zablokować atak w locie. Potrafi też zablokować księgowość, jeśli włączysz tryb IPS pierwszego dnia.

Jak wdrażać Suricatę rozsądnie:
- start w trybie IDS na kopii ruchu z portu SPAN lub TAP,
- reguły ET Open przez suricata-update, aktualizowane codziennie z przeładowaniem bez restartu,
- logi EVE JSON prosto do Wazuh albo Elastic Agent, bez pisania parserów,
- regularna kontrola licznika capture.kernel_drops, bo zgubione pakiety to ślepe plamy,
- fałszywe alarmy wyciszane punktowo, a do IPS tylko reguły o wysokiej pewności.

Poradnik z minimalną konfiguracją dla Suricaty 8.0:
https://empirecorporation.eu/blog/suricata-ids-ips-poradnik/

#Suricata #IDS #cyberbezpieczeństwo #bezpieczeństwoSieci #opensource

---

## 2026-11-27 · Backdoor PHP i web shell: jak je znaleźć, zanim atakujący wróci

https://empirecorporation.eu/blog/backdoor-web-shell-php/

Typowy błąd przy czyszczeniu zhakowanej strony: usunięcie spamu i zostawienie backdoora.

Backdoor PHP to często kilka linijek, które pozwalają atakującemu wgrać ładunek od nowa. Na co zwrócić uwagę:
- porównuj pliki z czystymi wersjami (wp core verify-checksums), zamiast polegać tylko na grepie po eval,
- sprawdzaj mu-plugins, pliki PHP w uploads i .user.ini z auto_prepend_file,
- filtruj pliki po ctime, bo datę modyfikacji łatwo sfałszować,
- w logach szukaj żądań POST do plików, które nie powinny ich przyjmować,
- po usunięciu wymień wszystkie hasła, klucze i zamknij lukę.

Poradnik z bezpiecznymi poleceniami: https://empirecorporation.eu/blog/backdoor-web-shell-php/

#cyberbezpieczeństwo #PHP #WordPress #malware #incidentresponse

---

## 2026-11-30 · Monitoring logów: Elastic Stack, OpenSearch czy Grafana z Loki

https://empirecorporation.eu/blog/monitoring-logow-elk-grafana/

Dwuwęzłowy klaster Elasticsearch wygląda na bezpieczniejszy od jednego serwera. W praktyce nie przetrwa awarii żadnego z węzłów.

Kilka rzeczy, które warto wiedzieć przed wyborem systemu do monitoringu logów:
- Elastic i OpenSearch indeksują pełną treść logów, Loki tylko etykiety, co mocno zmienia koszty dysku,
- klaster wymaga większości głosów węzłów master, dlatego minimum to trzy (albo dwa plus węzeł rozstrzygający),
- od 2024 roku kod Elasticsearch jest dostępny także na AGPLv3, OpenSearch pozostaje na Apache 2.0,
- koszty rosną z wolumenem, replikami, retencją i kardynalnością etykiet,
- najważniejszy alert to często ten o braku logów z krytycznego źródła.

Porównanie z tabelą i przykładami konfiguracji:
https://empirecorporation.eu/blog/monitoring-logow-elk-grafana/

#observability #Elasticsearch #Grafana #OpenSearch #DevOps

---

## 2026-12-03 · Skimmer kart w sklepie internetowym: jak wykryć atak Magecart

https://empirecorporation.eu/blog/magecart-skimmer-kart-sklep/

Płatność przez przekierowanie do bramki nie chroni sklepu przed skimmerem kart.

Atak Magecart potrafi wyświetlić fałszywy formularz karty jeszcze na stronie sklepu, a dopiero potem przepuścić klienta do operatora. Co warto wiedzieć:
- skimmer często siedzi w bazie danych (wp_options, core_config_data, bloki CMS), więc podmiana plików go nie usuwa,
- aktywuje się zwykle tylko na stronie zamówienia,
- CSP pomaga, ale Sansec opisał skimmer ładowany przez Google Tag Manager z danymi w koncie Stripe,
- od 31 marca 2025 wymagania PCI DSS 6.4.3 i 11.6.1 są obowiązkowe,
- wyciek danych kart to sprawa dla UODO: 72 godziny od stwierdzenia naruszenia.

Jak wykryć i usunąć skimmer: https://empirecorporation.eu/blog/magecart-skimmer-kart-sklep/

#ecommerce #cyberbezpieczeństwo #PCIDSS #WooCommerce #Magento

---

## 2026-12-06 · Jak zabezpieczyć WordPress w 2026: checklista krok po kroku

https://empirecorporation.eu/blog/zabezpieczenie-wordpress-checklista/

Zabezpieczenie WordPressa to nie jedna wtyczka, tylko kilka nawyków, które sprawdzisz samodzielnie.

Najważniejsze punkty z naszej checklisty na 2026:
- PHP 8.1 i starsze nie dostają już poprawek, a 8.2 traci wsparcie 31 grudnia 2026,
- 2FA dla każdego administratora i jak najmniej kont z tą rolą,
- DISALLOW_FILE_EDIT w wp-config.php i blokada PHP w uploads,
- kopie według zasady 3-2-1 z regularnym testem odtwarzania,
- monitoring integralności plików i codzienna weryfikacja rdzenia przez WP-CLI.

Pełna lista z gotowymi poleceniami: https://empirecorporation.eu/blog/zabezpieczenie-wordpress-checklista/

#WordPress #cyberbezpieczeństwo #webdev #PHP

---
