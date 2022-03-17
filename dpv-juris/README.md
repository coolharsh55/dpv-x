# Jurisdictional Concept extension for DPV

See [juris.ttl](./juris.ttl) for the serialisation of concepts in Turtle. 

Contributors:
* Harshvardhan J. Pandit
* Julian Flake

## Concepts

1. Regions and Countries modelled as per ISO-3166
2. ISO-3166-2 and UN-M49 Country Codes
3. EU and EEA Memberships (e.g. EU27, EU28)
4. Data Protection Laws in EU (WIP): Currently models GDPR and German Federal Laws
5. Data Protection Authorities in EU

## Example

### Europe, EU, and EEA - Laws and DPAs

```
juris:Europe a dpv:Region ;
    dct:title "Europe"@en ;
    juris:un_m49 150 ;
    skos:narrowerTransitive juris:DE, ... juris:EasternEurope, ... .

juris:EU a dpv:SupraNationalUnion ;
    dct:title "European Union (EU)"@en ;
    skos:narrower juris:AT, ... .

juris:EU27 a dpv:SupraNationalUnion ;
    dct:temporal [ a time1:ProperInterval ;
            time1:hasBeginning [ time1:inXSDDate "2020-02-01"^^xsd:date ] ] ;
    dct:title "European Union (EU-27)" ;
    skos:broader juris:EU ;
    skos:narrower juris:AT ... .

juris:EU-GDPR a dpv:Law ;
    dct:temporal [ a time1:ProperInterval ;
            time1:hasBeginning [ time1:inXSDDate "2018-05-25"^^xsd:date ] ] ;
    dct:title "General Data Protection Regulation (GDPR)"@en ;
    dpv:hasAuthority juris:AT-DPA, ... ;
    dpv:hasJurisdiction juris:EEA, juris:AT, ... ;
    foaf1:homepage "http://data.europa.eu/eli/reg/2016/679/oj"^^xsd:anyURI .

juris:EU-EDPS a dpv:DataProtectionAuthority ;
    dct:title "European Data Protection Supervisor"@en ;
    dpv:hasJurisdiction juris:EU ;
    foaf1:homepage "https://edps.europa.eu/"^^xsd:anyURI .
```

### Country and Regional - Laws and DPAs

```
juris:DE a dpv:Country ;
    dct:title "Germany"@en ;
    dpv:hasApplicableLaw juris:DE-BDSG, juris:EU-GDPR ;
    dpv:hasAuthority juris:DE-DPA ;
    juris:iso_alpha2 "DE"^^xsd:string ;
    juris:iso_alpha3 "DEU"^^xsd:string ;
    juris:iso_numeric 276 ;
    juris:un_m49 276 ;
    skos:broaderTransitive juris:EEA, juris:EEA30, ... 
        juris:EU, juris:EU27, ... .

juris:DE-BDSG a dpv:Law ;
    dct:temporal [ a time1:ProperInterval ;
            time1:hasBeginning [ time1:inXSDDate "2019-11-20"^^xsd:date ] ] ;
    dct:title "Bundesdatenschutzgesetz (BDSG)"@de,
        "Federal Data Protection Act (BDSG)"@en ;
    dpv:hasAuthority juris:DE-BB-DPA, ... ;
    dpv:hasJurisdiction juris:DE ;
    foaf1:homepage "https://www.gesetze-im-internet.de/bdsg_2018/"^^xsd:anyURI .

juris:DE-DPA a dpv:DataProtectionAuthority ;
    dct:title "The Federal Commissioner for Data Protection and Freedom of Information "@en ;
    dpv:hasApplicableLaw juris:DE-BDSG, juris:EU-GDPR ;
    dpv:hasJurisdiction juris:DE ;
    foaf1:homepage "http://www.bfdi.bund.de/"^^xsd:anyURI .

juris:DE-BE a dpv:Region ;
    dct:title "Berlin"@de, "Berlin"@en ;
    dpv:hasApplicableLaw juris:DE-BDSG, juris:DE-BE-BlnDSG, juris:EU-GDPR ;
    dpv:hasAuthority juris:DE-BE-DPA ;
    skos:broaderTransitive juris:DE .

juris:DE-BE-BlnDSG a dpv:Law ;
    dct:title "Berliner Datenschutzgesetz (BlnDSG)" ;
    dpv:hasAuthority juris:DE-BE-DPA ;
    dpv:hasJurisdiction juris:DE-BE ;
    foaf1:homepage "https://www.datenschutz-berlin.de/fileadmin/user_upload/pdf/publikationen/informationsmaterialien/2018-BlnBDI_BlnDSG.pdf"^^xsd:anyURI .

juris:DE-BE-DPA a dpv:DataProtectionAuthority ;
    dct:title "Berliner Beauftragte für Datenschutz und Informationsfreiheit"@de ;
    dpv:hasApplicableLaw juris:DE-BDSG, juris:DE-BE-BlnDSG, juris:EU-GDPR ;
    dpv:hasJurisdiction juris:DE-BE ;
    foaf1:homepage "https://www.datenschutz-berlin.de/"^^xsd:anyURI .
```