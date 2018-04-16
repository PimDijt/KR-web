~/stardog-5.2.2/bin/stardog-admin db drop -n KRweb
~/stardog-5.2.2/bin/stardog-admin db create  -o reasoning.sameas=FULL -n KRweb outputTTL/*.trig
