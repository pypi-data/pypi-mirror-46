
Run This First…
===============

If you’re running this notebook in Jupyter, run this first in order to
have availability of the EParseCIS modules in the notebook.

.. code:: ipython3

    import os
    import sys
    nb_dir = os.path.split(os.getcwd())[0]
    if nb_dir not in sys.path:
        sys.path.append(nb_dir)

Using the EParseCIS Python Package
==================================

The EParseCIS Python package contains a number of modules that make it
easy to serialize EPCIS XML structures into EPCPyYes python classes for
use in any type of python application where having an EPCIS class loaded
into a usable python class that can be serialized to any structure using
Jinja2 templates or native python mechanisms would be of value.

There are Two Fundamental Parsers
---------------------------------

If you know you’ll be parsing EPCIS data that has implicit namespace
declarations for the main EPCIS namespace, use the ``EPCISParser`` as it
is a little bit faster. If you are dealing with EPCIS data that has
explicit namespace declarations for each element i.e.,
``<ns1:ObjectEvent>...</ns1:ObjectEvent>`` then use the
``eparsecis.eparsecis.FlexibleNSParser`` class. Examples below are
interchangeable between the two except for the namespaced XML example.

| Please Note: All examples below are in Python 3.5

Loading EPCIS Data From A String
--------------------------------

Before we can get into how to use the EParseCIS package and associated
modules, we’ll need to load some data into memory for use in our parsing
exercise. Here we’ll be loading it into memory using a string; however,
in the real world you may most likely be loading in from a file stream,
etc.

.. code:: ipython3

    import io
    from eparsecis import eparsecis
    
    test_data = io.BytesIO('''
    <epcis:EPCISDocument
        xmlns:epcis="urn:epcglobal:epcis:xsd:1"
        xmlns:cbvmd="urn:epcglobal:cbv:mda"
        schemaVersion="1.2" creationDate="2015-04-22T15:33:12.485128">
        <EPCISBody>
            <EventList>
                <ObjectEvent>
                    <eventTime>2015-04-22T15:34:31.500371+00:00</eventTime>
                    <recordTime>2015-04-22T15:34:31.500371+00:00</recordTime>
                    <eventTimeZoneOffset>+00:00</eventTimeZoneOffset>
                    <epcList>
                        <epc>urn:epc:id:sgtin:305555.0555555.1</epc>
                        <epc>urn:epc:id:sgtin:305555.0555555.2</epc>
                        <epc>urn:epc:id:sgtin:305555.0555555.3</epc>
                        <epc>urn:epc:id:sgtin:305555.0555555.4</epc>
                        <epc>urn:epc:id:sgtin:305555.0555555.5</epc>
                    </epcList>
                    <action>ADD</action>
                    <bizStep>urn:epcglobal:cbv:bizstep:commissioning</bizStep>
                    <disposition>urn:epcglobal:cbv:disp:encoded</disposition>
                    <readPoint>
                        <id>urn:epc:id:sgln:305555.123456.12</id>
                    </readPoint>
                    <bizLocation>
                        <id>urn:epc:id:sgln:305555.123456.0</id>
                    </bizLocation>
                    <extension>
                        <sourceList>
                            <source type="urn:epcglobal:cbv:sdt:possessing_party">
                                urn:epc:id:sgln:305555.123456.0
                            </source>
                            <source type="urn:epcglobal:cbv:sdt:location">
                                urn:epc:id:sgln:305555.123456.12
                            </source>
                        </sourceList>
                        <destinationList>
                            <destination
                                type="urn:epcglobal:cbv:sdt:owning_party">
                                urn:epc:id:sgln:309999.111111.0
                            </destination>
                            <destination
                                type="urn:epcglobal:cbv:sdt:location">
                                urn:epc:id:sgln:309999.111111.233
                            </destination>
                        </destinationList>
                        <ilmd>
                            <cbvmd:itemExpirationDate>2015-12-31
                            </cbvmd:itemExpirationDate>
                            <cbvmd:lotNumber>DL232</cbvmd:lotNumber>
                        </ilmd>
                    </extension>
                </ObjectEvent>
                <AggregationEvent>
                    <eventTime>2015-04-22T15:34:31.500371+00:00</eventTime>
                    <recordTime>2015-04-22T15:34:31.500371+00:00</recordTime>
                    <eventTimeZoneOffset>+00:00</eventTimeZoneOffset>
                    <parentID>urn:epc:id:sgtin:305555.3555555.1</parentID>
                    <childEPCs>
                        <epc>urn:epc:id:sgtin:305555.0555555.1</epc>
                        <epc>urn:epc:id:sgtin:305555.0555555.2</epc>
                        <epc>urn:epc:id:sgtin:305555.0555555.3</epc>
                        <epc>urn:epc:id:sgtin:305555.0555555.4</epc>
                        <epc>urn:epc:id:sgtin:305555.0555555.5</epc>
                    </childEPCs>
                    <action>ADD</action>
                    <bizStep>urn:epcglobal:cbv:bizstep:packing</bizStep>
                    <disposition>urn:epcglobal:cbv:disp:container_closed
                    </disposition>
                    <readPoint>
                        <id>urn:epc:id:sgln:305555.123456.12</id>
                    </readPoint>
                    <bizLocation>
                        <id>urn:epc:id:sgln:305555.123456.0</id>
                    </bizLocation>
                </AggregationEvent>
                <TransactionEvent>
                    <eventTime>2015-04-22T15:34:31.500371+00:00</eventTime>
                    <recordTime>2015-04-22T15:34:31.500371+00:00</recordTime>
                    <eventTimeZoneOffset>+00:00</eventTimeZoneOffset>
                    <parentID>urn:epc:id:sgtin:305555.3555555.1</parentID>
                    <action>ADD</action>
                    <bizStep>urn:epcglobal:cbv:bizstep:shipping</bizStep>
                    <disposition>urn:epcglobal:cbv:disp:in_transit</disposition>
                    <readPoint>
                        <id>urn:epc:id:sgln:305555.123456.12</id>
                    </readPoint>
                    <bizLocation>
                        <id>urn:epc:id:sgln:305555.123456.0</id>
                    </bizLocation>
                    <extension>
                        <quantityList>
                            <quantityElement>
                                <epcClass>urn:epc:idpat:sgtin:305555.0555555.*
                                </epcClass>
                                <quantity>5</quantity>
                            </quantityElement>
                            <quantityElement>
                                <epcClass>urn:epc:idpat:sgtin:305555.0555555.*
                                </epcClass>
                                <quantity>14.5</quantity>
                                <uom>LB</uom>
                            </quantityElement>
                        </quantityList>
                        <sourceList>
                            <source type="urn:epcglobal:cbv:sdt:possessing_party">
                                urn:epc:id:sgln:305555.123456.0
                            </source>
                            <source type="urn:epcglobal:cbv:sdt:location">
                                urn:epc:id:sgln:305555.123456.12
                            </source>
                        </sourceList>
                        <destinationList>
                            <destination
                                type="urn:epcglobal:cbv:sdt:owning_party">
                                urn:epc:id:sgln:309999.111111.0
                            </destination>
                            <destination
                                type="urn:epcglobal:cbv:sdt:location">
                                urn:epc:id:sgln:309999.111111.233
                            </destination>
                        </destinationList>
                    </extension>
                </TransactionEvent>
            </EventList>
        </EPCISBody>
    </epcis:EPCISDocument>
    '''.encode('utf-8'))
    
    #load the data into the parser
    parser = eparsecis.EPCISParser(test_data)
    parser.parse()

Parse a Document with Explicit Namespace Declarations
-----------------------------------------------------

The ``FlexibleNSParser`` class can handle XML documents that have
namespaces that have been explicitly defined. This parser is slightly
slower during very large document parsing but, overall, functions with
the same efficiency of the EPCISParser.

.. code:: ipython3

    import io
    from eparsecis import eparsecis
    
    test_data = io.BytesIO("""<ns1:EPCISDocument
            xmlns:ns1="urn:epcglobal:epcis:xsd:1"
            xmlns:cbvmd="urn:epcglobal:cbv:mda"
            xmlns:sbdh="http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader"
            schemaVersion="1.2" creationDate="2018-02-27T21:52:16.416129">
        <ns1:EPCISBody>
            <ns1:EventList>
                <ns1:ObjectEvent>
                    <ns1:eventTime>2018-01-22T22:51:49.294565+00:00</ns1:eventTime>
                    <ns1:recordTime>2018-01-22T22:51:49.294565+00:00</ns1:recordTime>
                    <ns1:eventTimeZoneOffset>+00:00</ns1:eventTimeZoneOffset>
                    <ns1:epcList>
                        <ns1:epc>urn:epc:id:sgtin:305555.3555555.1</ns1:epc>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.1</ns1:epc>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.2</ns1:epc>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.3</ns1:epc>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.4</ns1:epc>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.5</ns1:epc>
                    </ns1:epcList>
                    <ns1:action>ADD</ns1:action>
                    <ns1:bizStep>urn:epcglobal:cbv:bizstep:commissioning</ns1:bizStep>
                    <ns1:disposition>urn:epcglobal:cbv:disp:encoded</ns1:disposition>
                    <ns1:readPoint>
                        <ns1:id>urn:epc:id:sgln:305555.123456.12</ns1:id>
                    </ns1:readPoint>
                    <ns1:bizLocation>
                        <ns1:id>urn:epc:id:sgln:305555.123456.0</ns1:id>
                    </ns1:bizLocation>
                    <ns1:bizTransactionList>
                        <ns1:bizTransaction type="urn:epcglobal:cbv:btt:po">
                            urn:epc:id:gdti:0614141.06012.1234
                        </ns1:bizTransaction>
                    </ns1:bizTransactionList>
                    <ns1:extension>
                        <ns1:sourceList>
                            <ns1:source type="urn:epcglobal:cbv:sdt:possessing_party">
                                urn:epc:id:sgln:305555.123456.0
                            </ns1:source>
                            <ns1:source type="urn:epcglobal:cbv:sdt:location">
                                urn:epc:id:sgln:305555.123456.12
                            </ns1:source>
                        </ns1:sourceList>
                        <ns1:destinationList>
                            <ns1:destination
                                    type="urn:epcglobal:cbv:sdt:owning_party">
                                urn:epc:id:sgln:309999.111111.0
                            </ns1:destination>
                            <ns1:destination
                                    type="urn:epcglobal:cbv:sdt:location">
                                urn:epc:id:sgln:309999.111111.233
                            </ns1:destination>
                        </ns1:destinationList>x
                        <ns1:ilmd>
                            <cbvmd:itemExpirationDate>2015-12-31
                            </cbvmd:itemExpirationDate>
                            <cbvmd:lotNumber>DL232</cbvmd:lotNumber>
                        </ns1:ilmd>
                    </ns1:extension>
                </ns1:ObjectEvent>
                <ns1:AggregationEvent>
                    <ns1:eventTime>2018-01-22T22:51:50.294565+00:00</ns1:eventTime>
                    <ns1:recordTime>2018-01-22T22:51:50.294565+00:00</ns1:recordTime>
                    <ns1:eventTimeZoneOffset>+00:00</ns1:eventTimeZoneOffset>
                    <ns1:parentID>urn:epc:id:sgtin:305555.3555555.1</ns1:parentID>
                    <ns1:childEPCs>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.1</ns1:epc>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.2</ns1:epc>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.3</ns1:epc>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.4</ns1:epc>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.5</ns1:epc>
                    </ns1:childEPCs>
                    <ns1:action>ADD</ns1:action>
                    <ns1:bizStep>urn:epcglobal:cbv:bizstep:packing</ns1:bizStep>
                    <ns1:disposition>urn:epcglobal:cbv:disp:container_closed
                    </ns1:disposition>
                    <ns1:readPoint>
                        <ns1:id>urn:epc:id:sgln:305555.123456.12</ns1:id>
                    </ns1:readPoint>
                    <ns1:bizLocation>
                        <ns1:id>urn:epc:id:sgln:305555.123456.0</ns1:id>
                    </ns1:bizLocation>
                    <ns1:bizTransactionList>
                        <ns1:bizTransaction type="urn:epcglobal:cbv:btt:po">
                            urn:epc:id:gdti:0614141.06012.1234
                        </ns1:bizTransaction>
                    </ns1:bizTransactionList>
                    <ns1:extension>
                        <ns1:childQuantityList>
                            <ns1:quantityElement>
                                <ns1:epcClass>urn:epc:idpat:sgtin:305555.0555555.*
                                </ns1:epcClass>
                                <ns1:quantity>5</ns1:quantity>
                            </ns1:quantityElement>
                            <ns1:quantityElement>
                                <ns1:epcClass>urn:epc:idpat:sgtin:305555.0555555.*
                                </ns1:epcClass>
                                <ns1:quantity>14.5</ns1:quantity>
                                <ns1:uom>LB</ns1:uom>
                            </ns1:quantityElement>
                        </ns1:childQuantityList>
                        <ns1:sourceList>
                            <ns1:source type="urn:epcglobal:cbv:sdt:possessing_party">
                                urn:epc:id:sgln:305555.123456.0
                            </ns1:source>
                            <ns1:source type="urn:epcglobal:cbv:sdt:location">
                                urn:epc:id:sgln:305555.123456.12
                            </ns1:source>
                        </ns1:sourceList>
                        <ns1:destinationList>
                            <ns1:destination
                                    type="urn:epcglobal:cbv:sdt:owning_party">
                                urn:epc:id:sgln:309999.111111.0
                            </ns1:destination>
                            <ns1:destination
                                    type="urn:epcglobal:cbv:sdt:location">
                                urn:epc:id:sgln:309999.111111.233
                            </ns1:destination>
                        </ns1:destinationList>
                    </ns1:extension>
                </ns1:AggregationEvent>
                <ns1:TransactionEvent>
                    <ns1:eventTime>2018-01-22T22:51:52.294565+00:00</ns1:eventTime>
                    <ns1:recordTime>2018-01-22T22:51:52.294565+00:00</ns1:recordTime>
                    <ns1:eventTimeZoneOffset>+00:00</ns1:eventTimeZoneOffset>
                    <ns1:bizTransactionList>
                        <ns1:bizTransaction type="urn:epcglobal:cbv:btt:po">
                            urn:epc:id:gdti:0614141.06012.1234
                        </ns1:bizTransaction>
                    </ns1:bizTransactionList>
                    <ns1:parentID>urn:epc:id:sgtin:305555.3555555.1</ns1:parentID>
                    <ns1:epcList>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.1</ns1:epc>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.2</ns1:epc>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.3</ns1:epc>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.4</ns1:epc>
                        <ns1:epc>urn:epc:id:sgtin:305555.0555555.5</ns1:epc>
                    </ns1:epcList>
                    <ns1:action>ADD</ns1:action>
                    <ns1:bizStep>urn:epcglobal:cbv:bizstep:shipping</ns1:bizStep>
                    <ns1:disposition>urn:epcglobal:cbv:disp:in_transit</ns1:disposition>
                    <ns1:readPoint>
                        <ns1:id>urn:epc:id:sgln:305555.123456.12</ns1:id>
                    </ns1:readPoint>
                    <ns1:bizLocation>
                        <ns1:id>urn:epc:id:sgln:305555.123456.0</ns1:id>
                    </ns1:bizLocation>
                    <ns1:extension>
                        <ns1:quantityList>
                            <ns1:quantityElement>
                                <ns1:epcClass>urn:epc:idpat:sgtin:305555.0555555.*
                                </ns1:epcClass>
                                <ns1:quantity>5</ns1:quantity>
                            </ns1:quantityElement>
                            <ns1:quantityElement>
                                <ns1:epcClass>urn:epc:idpat:sgtin:305555.0555555.*
                                </ns1:epcClass>
                                <ns1:quantity>14.5</ns1:quantity>
                                <ns1:uom>LB</ns1:uom>
                            </ns1:quantityElement>
                        </ns1:quantityList>
                        <ns1:sourceList>
                            <ns1:source type="urn:epcglobal:cbv:sdt:possessing_party">
                                urn:epc:id:sgln:305555.123456.0
                            </ns1:source>
                            <ns1:source type="urn:epcglobal:cbv:sdt:location">
                                urn:epc:id:sgln:305555.123456.12
                            </ns1:source>
                        </ns1:sourceList>
                        <ns1:destinationList>
                            <ns1:destination
                                    type="urn:epcglobal:cbv:sdt:owning_party">
                                urn:epc:id:sgln:309999.111111.0
                            </ns1:destination>
                            <ns1:destination
                                    type="urn:epcglobal:cbv:sdt:location">
                                urn:epc:id:sgln:309999.111111.233
                            </ns1:destination>
                        </ns1:destinationList>
                    </ns1:extension>
                </ns1:TransactionEvent>
                <ns1:extension>
                    <ns1:TransformationEvent>
                        <ns1:eventTime>2018-01-31T18:50:20.847426+00:00</ns1:eventTime>
                        <ns1:recordTime>2018-01-31T18:50:20.847426+00:00</ns1:recordTime>
                        <ns1:eventTimeZoneOffset>+00:00</ns1:eventTimeZoneOffset>
                        <ns1:baseExtension>
                            <ns1:eventID>9db05f77-e007-41a2-a6d9-140254b7ce5a</ns1:eventID>
                            <ns1:errorDeclaration>
                                <ns1:declarationTime>2018-01-29T18:50:20.163126
                                </ns1:declarationTime>
                                <ns1:reason>
                                    urn:epcglobal:cbv:er:incorrect_data
                                </ns1:reason>
                                <ns1:correctiveEventIDs>
                                    <ns1:correctiveEventID>
                                        fd2c6646-e4f9-4ed8-a5e5-e98614d6ce84
                                    </ns1:correctiveEventID>
                                    <ns1:correctiveEventID>
                                        4b9932b7-45f7-4983-8b62-95c2784a2fc8
                                    </ns1:correctiveEventID>
                                </ns1:correctiveEventIDs>
                            </ns1:errorDeclaration>
                        </ns1:baseExtension>
                        <ns1:inputEPCList>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.1000</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.1001</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.1002</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.1003</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.1004</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.1005</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.1006</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.1007</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.1008</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.1009</ns1:epc>
                        </ns1:inputEPCList>
                        <ns1:inputQuantityList>
                            <ns1:quantityElement>
                                <ns1:epcClass>urn:epc:idpat:sgtin:305555.0555551.*
                                </ns1:epcClass>
                                <ns1:quantity>100</ns1:quantity>
                                <ns1:uom>EA</ns1:uom>
                            </ns1:quantityElement>
                            <ns1:quantityElement>
                                <ns1:epcClass>urn:epc:idpat:sgtin:305555.0555551.*
                                </ns1:epcClass>
                                <ns1:quantity>94.3</ns1:quantity>
                                <ns1:uom>LB</ns1:uom>
                            </ns1:quantityElement>
                        </ns1:inputQuantityList>
                        <ns1:outputEPCList>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.2000</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.2001</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.2002</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.2003</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.2004</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.2005</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.2006</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.2007</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.2008</ns1:epc>
                            <ns1:epc>urn:epc:id:sgtin:305555.1555555.2009</ns1:epc>
                        </ns1:outputEPCList>
                        <ns1:outputQuantityList>
                            <ns1:quantityElement>
                                <ns1:epcClass>urn:epc:idpat:sgtin:305555.0555551.*
                                </ns1:epcClass>
                                <ns1:quantity>10</ns1:quantity>
                                <ns1:uom>EA</ns1:uom>
                            </ns1:quantityElement>
                            <ns1:quantityElement>
                                <ns1:epcClass>urn:epc:idpat:sgtin:305555.0555551.*
                                </ns1:epcClass>
                                <ns1:quantity>94.3</ns1:quantity>
                                <ns1:uom>LB</ns1:uom>
                            </ns1:quantityElement>
                        </ns1:outputQuantityList>
                        <ns1:bizStep>urn:epcglobal:cbv:bizstep:repackaging</ns1:bizStep>
                        <ns1:disposition>urn:epcglobal:cbv:disp:returned</ns1:disposition>
                        <ns1:readPoint>
                            <ns1:id>urn:epc:id:sgln:305555.123456.12</ns1:id>
                        </ns1:readPoint>
                        <ns1:bizLocation>
                            <ns1:id>urn:epc:id:sgln:305555.123456.0</ns1:id>
                        </ns1:bizLocation>
                        <ns1:bizTransactionList>
                            <ns1:bizTransaction type="urn:epcglobal:cbv:btt:desadv">
                                urn:epcglobal:cbv:bt:0555555555555.DE45_111
                            </ns1:bizTransaction>
                            <ns1:bizTransaction type="urn:epcglobal:cbv:btt:bol">
                                urn:epcglobal:cbv:bt:0555555555555.00001
                            </ns1:bizTransaction>
                        </ns1:bizTransactionList>
                        <ns1:sourceList>
                            <ns1:source type="urn:epcglobal:cbv:sdt:possessing_party">
                                urn:epc:id:sgln:305555.123456.0
                            </ns1:source>
                            <ns1:source type="urn:epcglobal:cbv:sdt:location">
                                urn:epc:id:sgln:305555.123456.12
                            </ns1:source>
                        </ns1:sourceList>
                        <ns1:destinationList>
                            <ns1:destination
                                    type="urn:epcglobal:cbv:sdt:owning_party">
                                urn:epc:id:sgln:309999.111111.0
                            </ns1:destination>
                            <ns1:destination
                                    type="urn:epcglobal:cbv:sdt:location">
                                urn:epc:id:sgln:309999.111111.233
                            </ns1:destination>
                        </ns1:destinationList>
                        <ns1:ilmd>
                            <cbvmd:itemExpirationDate>2015-12-31
                            </cbvmd:itemExpirationDate>
                            <cbvmd:lotNumber>DL232</cbvmd:lotNumber>
                        </ns1:ilmd>
                    </ns1:TransformationEvent>
                </ns1:extension>
            </ns1:EventList>
        </ns1:EPCISBody>
    </ns1:EPCISDocument>
    """.encode('utf-8'))
    
    #load the data into the parser
    parser = eparsecis.FlexibleNSParser(test_data)
    parser.parse()

Loading EPCIS Data From a File
==============================

The following illustrates loading an EPCIS XML structure from a file.

.. code:: ipython3

    import os
    from eparsecis import eparsecis
    curpath = os.path.split(os.getcwd())[0]
    parser = eparsecis.FlexibleNSParser(
        os.path.join(curpath, './tests/data/epcis.xml'))
    parser.parse()

Overriding the Base EPCISParser Class
=====================================

The EParseCIS package provides, essentially, a single class instance
inside the ``eparsecis`` module that is desgined to be overridden in
order to be useful in any practical sense.

The following methods are provided for use by developers:

::

    * handle_object_event
    * handle_aggregation_event
    * handle_transaction_event
    * handle_transformation_event

Examples
--------

Below we can see the power of both EParseCIS and EPCPyYes combined. As
the EParseCIS parser encounters events within an EPCIS document, it
calls each of the helper functions and passes along an EPCPyYes class
for you to use within your application. Below you can see how one might
want to inspect or iterate through various attributes of an EPCIS event.
Obviously, you’ll need to have some background in both EPCIS and the
EPCPyYes python package; but, having said that, much of the hard work
has been done for you by these two packages. The ability to quickly
serialize EPCIS messages and events into python classes that can be
intuitively manipulated lets developers focus on building applications
rather than tinkering with the protocols involved.

.. code:: ipython3

    import os
    import logging
    from eparsecis import eparsecis
    
    class MyParser(eparsecis.FlexibleNSParser):
        def handle_object_event(self, epcis_event):
            # for example, access the epc list
            print("EPC List from the Object Event: %s\r\n" % 
                  epcis_event.epc_list)
    
        def handle_aggregation_event(self, epcis_event):
            # for example, inspect the biz_location
            print("Aggregation Event Biz Location: %s\r\n" % 
                  epcis_event.biz_location)
    
        def handle_transaction_event(self, epcis_event):
            # get the possessing party
            for source in epcis_event.source_list:
                if source.type == \
                "urn:epcglobal:cbv:sdt:possessing_party":
                    print("Transaction Event: Possessing Party: %s" 
                          % source.source)
            
    
    curpath = os.path.split(os.getcwd())[0]
    parser = MyParser(
        os.path.join(curpath, './tests/data/epcis.xml'))
    parser.parse()


.. parsed-literal::

    EPC List from the Object Event: ['urn:epc:id:sgtin:305555.0555555.1', 'urn:epc:id:sgtin:305555.0555555.2', 'urn:epc:id:sgtin:305555.0555555.3', 'urn:epc:id:sgtin:305555.0555555.4', 'urn:epc:id:sgtin:305555.0555555.5']
    
    Aggregation Event Biz Location: urn:epc:id:sgln:305555.123456.0
    
    Transaction Event: Possessing Party: urn:epc:id:sgln:305555.123456.0

