STARDOG_JAVA_ARGS="-Xmx15g -Xms15g"
STARDOG_SERVER_JAVA_ARGS="-Xmx15g -Xms15g"
#export $STARDOG_JAVA_ARGS

~/stardog-5.2.3/bin/stardog-admin server stop
~/stardog-5.2.3/bin/stardog-admin server start --disable-security
~/stardog-5.2.3/bin/stardog-admin db drop -n KRweb
~/stardog-5.2.3/bin/stardog-admin db create -o spatial.enabled=true reasoning.sameas=FULL -n KRweb outputTTL/*.trig
#~/stardog-5.2.3/bin/stardog-admin server stop
#~/stardog-5.2.3/bin/stardog-admin server start --disable-security

#select ?name where {
#  ?loc rdfs:label ?name .
#  ?loc geo:hasGeometry ?feature .
#  ?hq geo:hasGeometry ?hqGeo .
#  ?feature geof:nearby (?hqGeo 2 <http://qudt.org/vocab/unit#Kilometer>).
#}