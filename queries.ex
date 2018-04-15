SELECT DISTINCT ?namea ?nameb ?lona ?lonb ?lata ?latb WHERE {
  ?a ns2:latitude ?lata .
  ?a ns2:longitude ?lona .
  ?a rdfs:label ?namea .
  ?a g13vocab:providesSpecialCare g13vocab:night .
  ?b ns2:latitude ?latb .
  ?b ns2:longitude ?lonb .
  ?b rdfs:label ?nameb .
  ?b g13vocab:providesSpecialCare g13vocab:day .
  filter((?lata-?latb)*(?lata-?latb)+(?lona-?lonb)*(?lona-?lonb)>(100*100)) .
}
