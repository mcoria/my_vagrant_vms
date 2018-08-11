DOMAIN      = 'edg_domain'
DOMAIN_PATH = '/u01/oracle/config/domains/edg_domain'
APP_PATH    = '/u01/oracle/config/applications/edg_domain'

ADMINHOST_ADDRESS	   =  'adminvh'
SOAHOST1_ADDRESS       =  'soavh01'
SOAHOST2_ADDRESS       =  'soavh02'

JSSE_ENABLED     = true
DEVELOPMENT_MODE = false
WEBTIER_ENABLED  = false

ADMIN_USER     = 'weblogic'
ADMIN_PASSWORD = 'Welcome1'

JAVA_HOME      = '/opt/jdk1.8.0_152'

ADM_JAVA_ARGUMENTS = '-XX:PermSize=512m -XX:MaxPermSize=1024m -Xms1024m -Xmx2048m '
WSM_JAVA_ARGUMENTS = '-XX:PermSize=128m -XX:MaxPermSize=512m  -Xms512m  -Xmx1024m '
OSB_JAVA_ARGUMENTS = '-XX:PermSize=512m -XX:MaxPermSize=1024m -Xms1024m -Xmx2048m '
SOA_JAVA_ARGUMENTS = '-XX:PermSize=512m -XX:MaxPermSize=1024m -Xms1024m -Xmx2048m '
BAM_JAVA_ARGUMENTS = '-XX:PermSize=512m -XX:MaxPermSize=1024m -Xms1024m -Xmx2048m '


SOA_REPOS_DBURL          = 'jdbc:oracle:thin:@services:1521/ORCLPDB1.localdomain'
SOA_REPOS_DBUSER_PREFIX  = 'EDG'
SOA_REPOS_DBPASSWORD     = 'Welcome1'

BPM_ENABLED=false
BAM_ENABLED=false
B2B_ENABLED=false
ESS_ENABLED=false

# ----------------------------------------------------
def createBootPropertiesFile(directoryPath,fileName,username,password):
  serverDir = File(directoryPath)
  bool = serverDir.mkdirs()
  fileNew=open(directoryPath + '/'+fileName, 'w')
  fileNew.write('username=%s\n' % username)
  fileNew.write('password=%s\n' % password)
  fileNew.flush()
  fileNew.close()

def createAdminStartupPropertiesFile(directoryPath, args):
  adminserverDir = File(directoryPath)
  bool = adminserverDir.mkdirs()
  fileNew=open(directoryPath + '/startup.properties', 'w')
  args=args.replace(':','\\:')
  args=args.replace('=','\\=')
  fileNew.write('Arguments=%s\n' % args)
  fileNew.flush()
  fileNew.close()

def changeDatasourceToXA(datasource):
  print 'Change datasource '+datasource
  cd('/')
  cd('/JDBCSystemResource/'+datasource+'/JdbcResource/'+datasource+'/JDBCDriverParams/NO_NAME_0')
  set('DriverName','oracle.jdbc.xa.client.OracleXADataSource')
  set('UseXADataSourceInterface','True') 
  cd('/JDBCSystemResource/'+datasource+'/JdbcResource/'+datasource+'/JDBCDataSourceParams/NO_NAME_0')
  set('GlobalTransactionsProtocol','TwoPhaseCommit')

def createManagedServer(server_name, server_group):
  cd('/')
  create(server_name, 'Server')
  setServerGroups(server_name, server_group)

def changeServer(server_name, server_host, server_port, java_arguments):
  cd('/Servers/'+server_name)
  set('ListenAddress',server_host)
  set('ListenPort'   ,server_port)
  
  create(server_name,'ServerStart')
  cd('ServerStart/'+server_name)
  set('Arguments' , java_arguments)
  set('JavaVendor','Sun')
  set('JavaHome'  , JAVA_HOME)  

def createMachine(machine_name, nodemanager_address):
  cd('/')
  create(machine_name,'UnixMachine')
  cd('UnixMachine/'+machine_name)
  create(machine_name,'NodeManager')
  cd('NodeManager/'+machine_name)
  set('ListenAddress',nodemanager_address)
  set('NMType','Plain')

def assignServerToMachine(server_name, machine_name):  
  cd('/Servers/'+server_name)
  set('Machine',machine_name)

# ----------------------------------------------------
# Set domain Options
print('Start...wls domain with template Basic WebLogic Server Domain')
selectTemplate('Basic WebLogic Server Domain','12.2.1.3.0')
selectTemplate('Oracle Enterprise Manager','12.2.1.3.0')
selectTemplate('Oracle WSM Policy Manager','12.2.1.3.0')
loadTemplates()

cd('/')
setOption('DomainName', DOMAIN)
setOption('AppDir', APP_PATH)

if DEVELOPMENT_MODE == true:
  setOption('ServerStartMode', 'dev')
else:
  setOption('ServerStartMode', 'prod')

setOption('JavaHome', JAVA_HOME)
setOption('OverwriteDomain', 'true')
setOption('NodeManagerType', 'ManualNodeManagerSetup')

print('Set weblogic password...')
cd('/Security/base_domain/User/weblogic')
set('Name',ADMIN_USER)
cmo.setPassword(ADMIN_PASSWORD)

print 'AdminServer configuration'
changeServer('AdminServer', ADMINHOST_ADDRESS, 7001, ADM_JAVA_ARGUMENTS)

print 'Creating WLS_WSM1'
createManagedServer('WLS_WSM1', ["WSM-CACHE-SVR" , "WSMPM-MAN-SVR" , "JRF-MAN-SVR"])
changeServer('WLS_WSM1',SOAHOST1_ADDRESS,8001,WSM_JAVA_ARGUMENTS)

print 'Creating WLS_WSM2'
createManagedServer('WLS_WSM2', ["WSM-CACHE-SVR" , "WSMPM-MAN-SVR" , "JRF-MAN-SVR"])
changeServer('WLS_WSM2',SOAHOST2_ADDRESS,8001,WSM_JAVA_ARGUMENTS)

print 'Creating wsm_cluster and assign managed servers'
cd('/')
create('wsm_cluser', 'Cluster')
assign('Server','WLS_WSM1','Cluster','wsm_cluser')
assign('Server','WLS_WSM2','Cluster','wsm_cluser')

print 'Configure datasources start'
cd('/JDBCSystemResource/LocalSvcTblDataSource/JdbcResource/LocalSvcTblDataSource/JDBCDriverParams/NO_NAME_0')
set('URL',SOA_REPOS_DBURL)
set('PasswordEncrypted',SOA_REPOS_DBPASSWORD)
cd('Properties/NO_NAME_0/Property/user')
set('Value',SOA_REPOS_DBUSER_PREFIX+'_STB')
print 'Executing getDatabaseDefaults().....'
getDatabaseDefaults() 
print 'Configure datasources end'

print 'Create Machines'
createMachine('ADMINHOST', ADMINHOST_ADDRESS)
createMachine('SOAHOST1', SOAHOST1_ADDRESS)
createMachine('SOAHOST2', SOAHOST2_ADDRESS)

print 'Assign Servers to Machines'
assignServerToMachine('AdminServer', 'ADMINHOST')
assignServerToMachine('WLS_WSM1', 'SOAHOST1')
assignServerToMachine('WLS_WSM2', 'SOAHOST2')

print('Write domain...')
writeDomain(DOMAIN_PATH)
closeTemplate()

# ----------------------------------------------------
#createAdminStartupPropertiesFile(DOMAIN_PATH+'/servers/AdminServer/data/nodemanager',ADM_JAVA_ARGUMENTS)
createBootPropertiesFile(DOMAIN_PATH+'/servers/AdminServer/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
#createBootPropertiesFile(DOMAIN_PATH+'/servers/WLS_WSM1/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
#createBootPropertiesFile(DOMAIN_PATH+'/config/nodemanager','nm_password.properties',ADMIN_USER,ADMIN_PASSWORD)

#es = encrypt(ADMIN_PASSWORD,DOMAIN_PATH)

#readDomain(DOMAIN_PATH)

#print('Set domain password...') 
#cd('/SecurityConfiguration/'+DOMAIN)
#set('CredentialEncrypted',es)

#print('Set nodemanager password')
#set('NodeManagerUsername'         ,ADMIN_USER )
#set('NodeManagerPasswordEncrypted',es )
   

#changeDatasourceToXA('EDNDataSource')
#changeDatasourceToXA('wlsbjmsrpDataSource')
#changeDatasourceToXA('OraSDPMDataSource')
#changeDatasourceToXA('SOADataSource')


#updateDomain()
#closeDomain()


#print('Exiting...')
exit()

#NEXT STETP: 
#	NodeManager
#	Comparar con el dominio generado por GUI

