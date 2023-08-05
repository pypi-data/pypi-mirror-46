# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2018

import streamsx.spl.op
import streamsx.spl.types
from streamsx.topology.schema import CommonSchema, StreamSchema
from streamsx.spl.types import rstring
import os
import getpass
import wget
from tempfile import gettempdir
import shutil
import tarfile


def _add_toolkit_dependency(topo):
    # IMPORTANT: Dependency of this python wrapper to a specific toolkit version
    # This is important when toolkit is not set with streamsx.spl.toolkit.add_toolkit (selecting toolkit from remote build service)
    streamsx.spl.toolkit.add_toolkit_dependency(topo, 'com.ibm.streamsx.eventstore', '[2.0.0,3.0.0)')

def _add_store_file(topology, path):
    filename = os.path.basename(path)
    topology.add_file_dependency(path, 'opt')
    return 'opt/'+filename


def _download_tk(url, name):
    targetdir=gettempdir() + '/' + name
    tmpfile = gettempdir() + '/' + name + '.tgz'
    if os.path.isdir(targetdir):
        shutil.rmtree(targetdir)
    if os.path.isfile(tmpfile):
        os.remove(tmpfile)
    wget.download(url, tmpfile)
    print (tmpfile + ": " + str(os.stat(tmpfile)))
    tar = tarfile.open(tmpfile, "r:gz")
    tar.extractall(path=targetdir)
    tar.close()
    toolkit_path = targetdir + '/' + name
    tkfile = toolkit_path + '/toolkit.xml'
    if os.path.isfile(tkfile):
        print (tkfile + ': ' + str(os.stat(tkfile)))
    return toolkit_path


def download_toolkit(url=None):
    """Downloads the event store toolkit from GitHub.

    Example for updating the Event Store toolkit::

        # download event store toolkit from GitHub
        eventstore_toolkit = es.update_toolkit(url=None)
        # add event store toolkit to topology
        streamsx.spl.toolkit.add_toolkit(topo, eventstore_toolkit)

   Returns:
        eventstore toolkit location
    """
    if url is None:
        url = 'https://github.com/IBMStreams/streamsx.eventstore/releases/download/v2.0.1-Enterprise-v2/streamsx.eventstore.toolkits-2.0.1-20190503-1449.tgz'
    eventstore_toolkit = _download_tk(url,'com.ibm.streamsx.eventstore')
    return eventstore_toolkit


def get_service_details(service_configuration):
    """Retrieve connection information for Event Store service in ICP4D.

    Example for retrieving Event Store service details::

        from icpd_core import icpd_util
        
        eventstore_cfg=icpd_util.get_service_instance_details(name='your-eventstore-instance')
        es_db, es_connection, es_user, es_password, es_truststore, es_truststore_password, es_keystore, es_keystore_password = get_service_details(eventstore_cfg)

   Returns:
        database_name, connection, user, password, truststore, truststore_password, keystore, keystore_password
    """

    es_db=input("Event Store database name (for example EVENTDB):")
    es_connection=input("Event Store connection (for example '<HOST1>:<JDBC_PORT>;<HOST1>:1101,<HOST2>:1101,<HOST3>:1101':")
    es_user=input("Event Store user:")
    es_password=getpass.getpass('Event Store password:')

    es_truststore=input("Event Store truststore file location (for example '/user-home/_global_/eventstore/db2eventstore-1234567890/clientkeystore':")
    es_truststore_password=getpass.getpass("Event Store truststore password:")
    # Change the lines below, if keystore and truststore is not in the same file
    es_keystore=es_truststore
    es_keystore_password=es_truststore_password

    return es_db, es_connection, es_user, es_password, es_truststore, es_truststore_password, es_keystore, es_keystore_password


def configure_connection(instance, name='eventstore', database=None, connection=None, user=None, password=None, keystore_password=None, truststore_password=None):
    """Configures IBM Streams for a connection to IBM Db2 Event Store database.

    Creates an application configuration object containing the required properties with connection information.

    Example for creating a configuration for a Streams instance with connection details::

        from streamsx.rest import Instance
        import streamsx.topology.context
        from icpd_core import icpd_util
        
        cfg=icpd_util.get_service_instance_details(name='your-streams-instance')
        cfg[streamsx.topology.context.ConfigParams.SSL_VERIFY] = False
        instance = Instance.of_service(cfg)
        app_cfg = configure_connection(instance, database='TESTDB', connection='HostIP:Port1;HostIP:Port2', user='db2-user', password='db2-password')


    Args:
        instance(streamsx.rest_primitives.Instance): IBM Streams instance object.
        name(str): Name of the application configuration
        database(str): The name of the database, as defined in IBM Db2 Event Store.
        connection(str): The set of IP addresses and port numbers needed to connect to IBM Db2 Event Store, format: <HostIP:Port from JDBC URL>;<SCALA connection URL>
        user(str): Name of the IBM Db2 Event Store User in order to connect.
        password(str): Password for the IBM Db2 Event Store User in order to connect.
        keystore_password(str): Password for key store file.
        truststore_password(str): Password for trust store file.

    Returns:
        Name of the application configuration.
    """

    # Prepare operator (toolkit) specific properties for application configuration
    description = 'Config for Db2 Event Store connection ' + name
    properties = {}
    if database is not None:
        properties['databaseName']=database
    if connection is not None:
        properties['connectionString']=connection
    if user is not None:
        properties['eventStoreUser']=user
    if password is not None:
        properties['eventStorePassword']=password
    if keystore_password is not None:
        properties['keyStorePassword']=keystore_password
    if truststore_password is not None:
        properties['trustStorePassword']=truststore_password
    
    # check if application configuration exists
    app_config = instance.get_application_configurations(name=name)
    if app_config:
        print ('update application configuration: '+name)
        app_config[0].update(properties)
    else:
        print ('create application configuration: '+name)
        instance.create_application_configuration(name, properties, description)
    return name


def insert(stream, table, schema_name=None, database=None, connection=None, user=None, password=None, config=None, batch_size=None, front_end_connection_flag=None, max_num_active_batches=None, partitioning_key=None, primary_key=None, truststore=None, truststore_password=None, keystore=None, keystore_password=None, plugin_name=None, schema=None, name=None):
    """Inserts tuple into a table using Db2 Event Store Scala API.

    Important: The tuple field types and positions in the IBM Streams schema must match the field names in your IBM Db2 Event Store table schema exactly.

    Creates the table if the table does not exist. Set the ``primary_key`` and ``partitioning_key`` in case the table needs to be created.

    Example of a Streams application inserting rows to a table in a Db2 Event Store database::

        # provide connection endpoint information in format <HostIP:Port from JDBC URL>;<SCALA connection URL>
        es_connection = 'HostIP:Port1;HostIP:Port2'
        # generate sample tuples with the schema of the target table
        s = topo.source([1,2,3,4,5,6,7,8,9])
        schema=StreamSchema('tuple<int32 id, rstring name>').as_tuple()
        s = s.map(lambda x : (x,'X'+str(x*2)), schema=schema)
        # insert tuple data into table as rows
        res = es.insert(s, connection=es_connection, database='TESTDB', table='SampleTable', schema_name='sample', primary_key='id', partitioning_key='id')

    Args:
        stream(Stream): Stream of tuples containing the fields to be inserted as a row. Supports ``streamsx.topology.schema.StreamSchema`` (schema for a structured stream) as input. The tuple attribute types and positions in the IBM Streams schema must match the field names in your IBM Db2 Event Store table schema exactly.
        table(str): The name of the table into which you want to insert rows.
        schema_name(str): The name of the table schema name of the table into which to insert data.
        database(str): The name of the database, as defined in IBM Db2 Event Store. Alternative this parameter can be set with function ``configure_connection()``.
        connection(str): The set of IP addresses and port numbers needed to connect to IBM Db2 Event Store. Alternative this parameter can be set with function ``configure_connection()``.
        user(str): Name of the IBM Db2 Event Store User in order to connect. Alternative this parameter can be set with function ``configure_connection()``.
        password(str): Password for the IBM Db2 Event Store User in order to connect. Alternative this parameter can be set with function ``configure_connection()``.
        config(str): The name of the application configuration. Value returned by the function ``configure_connection()``.
        batch_size(int): The number of rows that will be batched in the operator before the batch is inserted into IBM Db2 Event Store by using the batchInsertAsync method. If you do not specify this parameter, the batchSize defaults to the estimated number of rows that could fit into an 8K memory page.
        front_end_connection_flag(bool): Set to ``True`` to connect through a Secure Gateway (for Event Store Enterprise Edition version >= 1.1.2 and Developer Edition version > 1.1.4)
        max_num_active_batches(int): The number of batches that can be filled and inserted asynchronously. The default is 1.        
        partitioning_key(str): Partitioning key for the table. A string of attribute names separated by commas. The partitioning_key parameter is used only, if the table does not yet exist in the IBM Db2 Event Store database.
        primary_key(str): Primary key for the table.  A string of attribute names separated by commas. The order of the attribute names defines the order of entries in the primary key for the IBM Db2 Event Store table. The primary_key parameter is used only, if the table does not yet exist in the IBM Db2 Event Store database.
        truststore(str): Path to the trust store file for the SSL connection.
        truststore_password(str): Password for the trust store file given by the truststore parameter. Alternative this parameter can be set with function ``configure_connection()``.
        keystore(str): Path to the key store file for the SSL connection.
        keystore_password(str): Password for the key store file given by the keystore parameter. Alternative this parameter can be set with function ``configure_connection()``.
        plugin_name(str): The plug-in name for the SSL connection. The default value is IBMPrivateCloudAuth.      
        schema(StreamSchema): Schema for returned stream. Expects a Boolean attribute called "_Inserted_" in the output stream. This attribute is set to true if the data was successfully inserted and false if the insert failed. Input stream attributes are forwarded to the output stream if present in schema.            
        name(str): Sink name in the Streams context, defaults to a generated name.

    Returns:
        streamsx.topology.topology.Sink: Stream termination
        or
        Output Stream if ``schema`` parameter is specified. This output port is intended to output the information on whether a tuple was successful or not when it was inserted into the database.
    """

    if config is None and connection is None:
         raise ValueError("Either config parameter or connection must be set.")
    if config is None and database is None:
         raise ValueError("Either config parameter or database must be set.")

    # python wrapper eventstore toolkit dependency
    _add_toolkit_dependency(stream.topology)

    _op = _EventStoreSink(stream, schema, connectionString=connection, databaseName=database, tableName=table, schemaName=schema_name, partitioningKey=partitioning_key, primaryKey=primary_key, name=name)
    if front_end_connection_flag is not None:
        if front_end_connection_flag is True:
            _op.params['frontEndConnectionFlag'] = _op.expression('true')
    if batch_size is not None:
        _op.params['batchSize'] = streamsx.spl.types.int32(batch_size)
    if max_num_active_batches is not None:
        _op.params['maxNumActiveBatches'] = streamsx.spl.types.int32(max_num_active_batches)
          
    if keystore is not None:
        _op.params['keyStore'] = _add_store_file(stream.topology, keystore)
    if keystore_password is not None:
        _op.params['keyStorePassword'] = keystore_password
    if plugin_name is not None:
        _op.params['pluginFlag'] = _op.expression('true')
        _op.params['pluginName'] = plugin_name
    if truststore is not None:
        _op.params['trustStore'] = _add_store_file(stream.topology, truststore)
    if truststore_password is not None:
        _op.params['trustStorePassword'] = truststore_password

    if config is not None:
        _op.params['configObject'] = config
    else:
        if user is not None:
            _op.params['eventStoreUser'] = user
        if password is not None:
            _op.params['eventStorePassword'] = password

    if schema is not None:
        return _op.outputs[0]
    else:
        return streamsx.topology.topology.Sink(_op)


class _EventStoreSink(streamsx.spl.op.Invoke):
    def __init__(self, stream, schema, tableName, connectionString=None, databaseName=None, schemaName=None, batchSize=None, configObject=None, eventStorePassword=None, eventStoreUser=None, frontEndConnectionFlag=None, maxNumActiveBatches=None, nullMapString=None, partitioningKey=None, preserveOrder=None, primaryKey=None, keyStore=None, keyStorePassword=None, pluginFlag=None, pluginName=None, sslConnection=None, trustStore=None, trustStorePassword=None, vmArg=None, name=None):
        topology = stream.topology
        kind="com.ibm.streamsx.eventstore::EventStoreSink"
        inputs=stream
        schemas=schema
        params = dict()
        if vmArg is not None:
            params['vmArg'] = vmArg
        if connectionString is not None:
            params['connectionString'] = connectionString
        if databaseName is not None:
            params['databaseName'] = databaseName
        if tableName is not None:
            params['tableName'] = tableName
        if schemaName is not None:
            params['schemaName'] = schemaName
        if batchSize is not None:
            params['batchSize'] = batchSize
        if configObject is not None:
            params['configObject'] = configObject
        if eventStorePassword is not None:
            params['eventStorePassword'] = eventStorePassword
        if eventStoreUser is not None:
            params['eventStoreUser'] = eventStoreUser
        if frontEndConnectionFlag is not None:
            params['frontEndConnectionFlag'] = frontEndConnectionFlag
        if maxNumActiveBatches is not None:
            params['maxNumActiveBatches'] = maxNumActiveBatches
        if nullMapString is not None:
            params['nullMapString'] = nullMapString
        if partitioningKey is not None:
            params['partitioningKey'] = partitioningKey
        if preserveOrder is not None:
            params['preserveOrder'] = preserveOrder
        if primaryKey is not None:
            params['primaryKey'] = primaryKey
        if keyStore is not None:
            params['keyStore'] = keyStore
        if keyStorePassword is not None:
            params['keyStorePassword'] = keyStorePassword
        if pluginFlag is not None:
            params['pluginFlag'] = pluginFlag
        if pluginName is not None:
            params['pluginName'] = pluginName
        if sslConnection is not None:
            params['sslConnection'] = sslConnection
        if trustStore is not None:
            params['trustStore'] = trustStore
        if trustStorePassword is not None:
            params['trustStorePassword'] = trustStorePassword

        super(_EventStoreSink, self).__init__(topology,kind,inputs,schema,params,name)



