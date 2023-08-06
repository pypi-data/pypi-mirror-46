LHCb Software configuration Database 2
====================================
![](https://gitlab.cern.ch/lhcb-core/LbSoftConfDB2/badges/master/pipeline.svg)
![](https://gitlab.cern.ch/lhcb-core/LbSoftConfDB2/badges/master/coverage.svg)


Neo4j database used to store the dependencies of the LHCb software projects.

The project is composed of 2 packages:

* a client side package that contains all the clients. The clients connect to the server side application using XML RPC via HTTP requests. The communication is done for clients that only query the databse using non-authe requests, while the database modifications are done using SSO auth requests. 
* a server side package. It provides 2 XML RPC servers: one for non-auth requests and the other one for auth-requests. The SSO auth is managed by a revers Apache proxy. The data exchange with the Neo4j server is executed only the main component of the application.
![Service architecture](http://lbinstall.web.cern.ch/lbinstall/r1.png)

