ROUTER_PROMPT = """
**INSTRUKCIJE:**
Tvoj zadatak je da na osnovu datog pitanja korisnika odlucis koji zakon ili zakoni su potrebni da bi se odgovorilo na korisnikovo pitanje.
Ponudjeni zakoni i njihova objasnjenja su sledeci:

    - zakon_o_digitalnoj_imovini
    Zakon o digitalnoj imovini Republike Srbije reguliše pravni okvir za digitalnu imovinu, uključujući virtuelne valute i digitalne tokene. Zakon definiše uslove pod kojima se digitalna imovina može izdavati, trgovati i koristiti, kao i nadležnosti organa koji prate ove aktivnosti. Takođe, zakon obuhvata pravila o zaštiti prava korisnika, sprečavanju pranja novca i finansiranju terorizma u vezi sa digitalnom imovinom.

    - zakon_o_doprinosima_za_obavezno_socijalno_osiguranje
    Zakon o doprinosima za obavezno socijalno osiguranje uređuje obaveze zaposlenih i poslodavaca u pogledu plaćanja doprinosa za socijalno osiguranje, koje uključuje penzijsko i invalidsko osiguranje, zdravstveno osiguranje, kao i osiguranje za slučaj nezaposlenosti. Zakon precizira osnovicu, stope i način uplate doprinosa, kao i kaznene mere za neplaćanje ili nepravovremenu uplatu.

    - zakon_o_fiskalizaciji_republike_srbije
    Zakon o fiskalizaciji propisuje obaveznu fiskalizaciju svih transakcija koje se odnose na promet dobara i usluga u Srbiji. Zakon definiše obavezu uvođenja i korišćenja fiskalnih kasa i elektronskih uređaja za registrovanje prometa, kao i obaveze obveznika fiskalizacije u pogledu evidentiranja i prijavljivanja prometa Poreskoj upravi. Takođe, zakon predviđa sankcije za kršenje obaveza vezanih za fiskalizaciju.

    - zakon_o_deviznom_poslovanju
    Zakon o deviznom poslovanju uređuje poslovanje sa inostranstvom i promet deviza u Republici Srbiji. Zakon propisuje uslove za kupovinu, prodaju, prijenos i upotrebu deviza, kao i vođenje računa u inostranstvu. Takođe reguliše poslovanje sa stranim investicijama, izvoz i uvoz kapitala, te mehanizme kontrole deviznog tržišta od strane Narodne banke Srbije.

    - zakon_o_poreskom_postupku_i_poreskoj_administraciji
    Zakon o poreskom postupku i poreskoj administraciji definiše postupak utvrđivanja, naplate i kontrole poreza u Republici Srbiji. Zakon obuhvata pravila o pravima i obavezama poreskih obveznika, rokovima za podnošenje poreskih prijava, kao i nadležnosti Poreske uprave. Takođe, zakon predviđa kazne za neplaćanje poreza, kao i postupke prinudne naplate i žalbe.

    - zakon_o_porezima_na_imovinu
    Zakon o porezima na imovinu uređuje način oporezivanja nepokretne i pokretne imovine u Srbiji. Zakon definiše osnovicu i stope poreza na različite vrste imovine, uključujući nekretnine, motorna vozila i brodove. Takođe obuhvata olakšice i oslobođenja za određene kategorije imovine i poreskih obveznika, kao i postupke utvrđivanja i plaćanja poreza.

    - zakon_o_porezu_na_dobit_pravnih_lica
    Zakon o porezu na dobit pravnih lica propisuje način oporezivanja dobiti koju ostvaruju pravna lica u Republici Srbiji. Zakon definiše osnovicu poreza na dobit, stope poreza, kao i olakšice i oslobođenja koja mogu da se primene. Takođe obuhvata pravila o prijavi i plaćanju poreza, kao i kaznene mere za neplaćanje ili nepravovremeno plaćanje.

    - zakon_o_porezu_na_dodatu_vrednost
    Zakon o porezu na dodatu vrednost (PDV) reguliše sistem PDV-a u Republici Srbiji. Zakon definiše šta se smatra oporezivim prometom, ko su obveznici PDV-a, kao i stope PDV-a. Takođe obuhvata pravila o odbitku prethodnog poreza, prijavljivanju i plaćanju PDV-a, kao i olakšice i oslobođenja za određene vrste prometa i subjekte.

    - zakon_o_porezu_na_dohodak_gradjana
    Zakon o porezu na dohodak građana reguliše način oporezivanja prihoda fizičkih lica u Republici Srbiji. Zakon obuhvata oporezivanje zarada, prihoda od samostalnih delatnosti, kapitala, nepokretnosti i drugih prihoda. Takođe, zakon propisuje poreske stope, osnovice, olakšice i oslobođenja za određene kategorije građana, kao i postupak prijave i plaćanja poreza.

    - zakon_o_radu
    Zakon o radu Republike Srbije uređuje radne odnose između zaposlenih i poslodavaca. Zakon definiše prava i obaveze obe strane, uključujući radno vreme, odmore, odsustva, uslove za otkaz ugovora o radu, kao i pravila za ugovore o radu, minimalnu zaradu i zaštitu na radu. Takođe, zakon predviđa mehanizme za rešavanje radnih sporova i uređuje kolektivne ugovore i sindikalna prava.
- nema_zakona
 - Korisnikovo pitanje ne odgovara ni jednom zakonu.

**FORMAT ODGOVORA:**
- Odgovor vratiti u JSON formatu koji moze da se učita sa json.loads().
- Imena zakona mogu biti samo sledeca: 
    - zakon-o-digitalnoj-imovini
    - zakon-o-doprinosima-za-obavezno-socijalno-osiguranje
    - zakon-o-fiskalizaciji-republike-srbije
    - zakon_o_deviznom_poslovanju
    - zakon_o_poreskom_postupku_i_poreskoj_administraciji
    - zakon_o_porezima_na_imovinu
    - zakon_o_porezu_na_dobit_pravnih_lica
    - zakon_o_porezu_na_dodatu_vrednost
    - zakon_o_porezu_na_dohodak_gradjana
    - zakon_o_radu
    - nema_zakona
    
- Jedno pitanje korisnika moze da se odnosi na vise zakona.
- Vrati zakone koji mogu da pomognu prilikom generisanja odgovora.
- Ukoliko korisnikovo pitanje ne odgovara ni jednom zakonu vrati listu sa generickim stringom: ["nema_zakona"].

**PRIMER ODGOVORA:**
{{
    response: ["ime_zakona"]
}}
"""

USER_QUERY = """
**PITANJE KORISINKA:**
{query}
"""

ROUTER_PROMPT_ENG = """
**INSTRUCTIONS:**
Your task is to determine which law or laws are needed to answer the user's question based on the given query.
The offered laws and their descriptions are as follows:

    - zakon_o_digitalnoj_imovini
    The Law on Digital Assets of the Republic of Serbia regulates the legal framework for digital assets, including virtual currencies and digital tokens. The law defines the conditions under which digital assets can be issued, traded, and used, as well as the competencies of authorities monitoring these activities. It also encompasses rules on user rights protection, prevention of money laundering, and terrorism financing related to digital assets.

    - zakon_o_doprinosima_za_obavezno_socijalno_osiguranje
    The Law on Contributions for Mandatory Social Insurance regulates the obligations of employees and employers regarding the payment of contributions for social insurance, which includes pension and disability insurance, health insurance, and unemployment insurance. The law specifies the base, rates, and method of contribution payment, as well as punitive measures for non-payment or late payment.

    - zakon_o_fiskalizaciji_republike_srbije
    The Law on Fiscalization mandates the fiscalization of all transactions related to the sale of goods and services in Serbia. The law defines the obligation to introduce and use fiscal cash registers and electronic devices for recording turnover, as well as the duties of fiscalization subjects regarding the recording and reporting of turnover to the Tax Administration. It also prescribes sanctions for violations related to fiscalization.

    - zakon_o_deviznom_poslovanju
    The Law on Foreign Exchange Operations regulates business with foreign entities and foreign currency transactions in the Republic of Serbia. The law prescribes conditions for the purchase, sale, transfer, and use of foreign currency, as well as maintaining accounts abroad. It also regulates operations with foreign investments, export and import of capital, and mechanisms for controlling the foreign exchange market by the National Bank of Serbia.

    - zakon_o_poreskom_postupku_i_poreskoj_administraciji
    The Law on Tax Procedure and Tax Administration defines the procedure for determining, collecting, and controlling taxes in the Republic of Serbia. The law encompasses rules on the rights and obligations of taxpayers, deadlines for submitting tax returns, and the competencies of the Tax Administration. It also prescribes penalties for non-payment of taxes, as well as procedures for enforced collection and appeals.

    - zakon_o_porezima_na_imovinu
    The Law on Property Taxes regulates the taxation method of movable and immovable property in Serbia. The law defines the tax base and rates for different types of property, including real estate, motor vehicles, and ships. It also includes reliefs and exemptions for certain categories of property and taxpayers, as well as procedures for determining and paying taxes.

    - zakon_o_porezu_na_dobit_pravnih_lica
    The Law on Corporate Profit Tax prescribes the method of taxing profits earned by legal entities in the Republic of Serbia. The law defines the tax base for profit tax, tax rates, and reliefs and exemptions that can be applied. It also encompasses rules on tax reporting and payment, as well as punitive measures for non-payment or late payment.

    - zakon_o_porezu_na_dodatu_vrednost
    The Law on Value Added Tax (VAT) regulates the VAT system in the Republic of Serbia. The law defines what is considered taxable turnover, who are VAT payers, and the VAT rates. It also includes rules on input tax deduction, VAT reporting and payment, and reliefs and exemptions for certain types of turnover and subjects.

    - zakon_o_porezu_na_dohodak_gradjana
    The Law on Personal Income Tax regulates the taxation method of individual incomes in the Republic of Serbia. The law encompasses the taxation of salaries, income from self-employment, capital, real estate, and other incomes. It also prescribes tax rates, bases, reliefs, and exemptions for certain categories of citizens, as well as the procedure for tax reporting and payment.

    - zakon_o_radu
    The Labor Law of the Republic of Serbia regulates labor relations between employees and employers. The law defines the rights and obligations of both parties, including working hours, vacations, leaves, conditions for terminating employment contracts, as well as rules for employment contracts, minimum wage, and occupational safety. It also provides mechanisms for resolving labor disputes and regulates collective agreements and union rights.
- nema_zakona
 - The user's question does not correspond to any law.

**RESPONSE FORMAT:**
- Return the answer in JSON format that can be loaded with json.loads().
- The names of the laws can only be the following: zakon-o-digitalnoj-imovini, zakon-o-doprinosima-za-obavezno-socijalno-osiguranje, zakon-o-fiskalizaciji-republike-srbije, zakon_o_deviznom_poslovanju, zakon_o_poreskom_postupku_i_poreskoj_administraciji, zakon_o_porezima_na_imovinu, zakon_o_porezu_na_dobit_pravnih_lica, zakon_o_porezu_na_dodatu_vrednost, zakon_o_porezu_na_dohodak_gradjana, zakon_o_radu, nema_zakona.
- A single user question may relate to multiple laws.
- Return the laws that can assist in generating the answer.
- If the user's question does not correspond to any law, return a list with the generic string: ["nema_zakona"].

**SAMPLE ANSWER:**
{{
    response: ["law_name"]
}}

"""


DEFAULT_ROUTER_RESPONSE = "nema_zakona"
