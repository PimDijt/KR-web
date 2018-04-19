C:/stardog-5.2.3/bin/stardog-admin db drop -n KRweb && ^
C:/stardog-5.2.3/bin/stardog-admin db create -o spatial.enabled=true reasoning.sameas=FULL -n KRweb outputTTL/*.ttl vocab.ttl
