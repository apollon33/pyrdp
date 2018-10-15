from rdpy.enum.rdp import RDPConnectionDataType, ServerCertificateType, NegotiationProtocols
from rdpy.protocol.rdp.x224 import NegociationType


class RDPClientDataPDU:
    def __init__(self, coreData, securityData, networkData, clusterData):
        """
        :type coreData: ClientCoreData
        :type securityData: ClientSecurityData
        :type networkData: ClientNetworkData
        :type clusterData: ClientClusterData
        """
        self.coreData = coreData
        self.securityData = securityData
        self.networkData = networkData
        self.clusterData = clusterData

class ClientCoreData:
    def __init__(self, version, desktopWidth, desktopHeight, colorDepth, sasSequence, keyboardLayout, clientBuild, clientName, keyboardType, keyboardSubType, keyboardFunctionKey, imeFileName):
        self.header = RDPConnectionDataType.CLIENT_CORE
        self.version = version
        self.desktopWidth = desktopWidth
        self.desktopHeight = desktopHeight
        self.colorDepth = colorDepth
        self.sasSequence = sasSequence
        self.keyboardLayout = keyboardLayout
        self.clientBuild = clientBuild
        self.clientName = clientName
        self.keyboardType = keyboardType
        self.keyboardSubType = keyboardSubType
        self.keyboardFunctionKey = keyboardFunctionKey
        self.imeFileName = imeFileName
        self.postBeta2ColorDepth = None
        self.clientProductId = None
        self.serialNumber = None
        self.highColorDepth = None
        self.supportedColorDepths = None
        self.earlyCapabilityFlags = None
        self.clientDigProductId = None
        self.connectionType = None
        self.pad1octet = None
        self.serverSelectedProtocol = None
        self.desktopPhysicalWidth = None
        self.desktopPhysicalHeight = None
        self.desktopOrientation = None
        self.desktopScaleFactor = None
        self.deviceScaleFactor = None   

class ClientSecurityData:
    def __init__(self, encryptionMethods, extEncryptionMethods):
        self.header = RDPConnectionDataType.CLIENT_SECURITY
        self.encryptionMethods = encryptionMethods
        # extEncryptionMethods is used only for the French locale (https://msdn.microsoft.com/en-us/library/cc240511.aspx)
        self.extEncryptionMethods = extEncryptionMethods

class ClientChannelDefinition:
    def __init__(self, name, options):
        self.name = name
        self.options = options
    
    def __repr__(self):
        return "%s (0x%lx)" % (self.name, self.options)

class ClientNetworkData:
    def __init__(self, channelDefinitions):
        self.header = RDPConnectionDataType.CLIENT_NETWORK
        self.channelDefinitions = channelDefinitions

class ClientClusterData:
    def __init__(self, flags, redirectedSessionID):
        self.header = RDPConnectionDataType.CLIENT_CLUSTER
        self.flags = flags
        self.redirectedSessionID = redirectedSessionID



class RDPServerDataPDU:
    def __init__(self, core, security, network):
        self.core = core
        self.security = security
        self.network = network

class ServerCoreData:
    def __init__(self, version, clientRequestedProtocols, earlyCapabilityFlags):
        self.header = RDPConnectionDataType.SERVER_CORE
        self.version = version
        self.clientRequestedProtocols = clientRequestedProtocols
        self.earlyCapabilityFlags = earlyCapabilityFlags

class ServerNetworkData:
    def __init__(self, mcsChannelID, channels):
        self.header = RDPConnectionDataType.SERVER_NETWORK
        self.mcsChannelID = mcsChannelID
        self.channels = channels
    
class ServerSecurityData:
    def __init__(self, encryptionMethod, encryptionLevel, serverRandom, serverCertificate):
        self.header = RDPConnectionDataType.SERVER_SECURITY
        self.encryptionMethod = encryptionMethod
        self.encryptionLevel = encryptionLevel
        self.serverRandom = serverRandom
        self.serverCertificate = serverCertificate

class ServerCertificate:
    def __init__(self, type, publicKey, signature):
        self.type = type
        self.publicKey = publicKey
        self.signature = signature

class ProprietaryCertificate(ServerCertificate):
    def __init__(self, signatureAlgorithmID, keyAlgorithmID, publicKeyType, publicKey, signatureType, signature, padding):
        ServerCertificate.__init__(self, ServerCertificateType.PROPRIETARY, publicKey, signature)
        self.signatureAlgorithmID = signatureAlgorithmID
        self.keyAlgorithmID = keyAlgorithmID
        self.publicKeyType = publicKeyType
        self.signatureType = signatureType
        self.padding = padding


class RDPNegotiationResponsePDU:
    """
    Second PDU of the RDP connection sequence. Sent by the server.
    Important information is the chosen encryption method.
    """

    def __init__(self, flags, selected_protocol):
        self.packetType = NegociationType.TYPE_RDP_NEG_RSP
        self.length = 8
        self.flags = flags
        self.selected_protocol = selected_protocol


class RDPNegotiationRequestPDU:
    """
    First PDU of the RDP connection sequence. Sent by the client.
    """

    def __init__(self, cookie, flags, requested_protocols):
        self.cookie = cookie
        self.flags = flags
        self.packetType = NegociationType.TYPE_RDP_NEG_REQ
        self.requestedProtocols = requested_protocols
        self.tlsSupported = self.requestedProtocols & NegotiationProtocols.SSL != 0
        self.credSspSupported = self.requestedProtocols & NegotiationProtocols.CRED_SSP != 0
        self.earlyUserAuthSupported = self.requestedProtocols & NegotiationProtocols.EARLY_USER_AUTHORIZATION_RESULT != 0