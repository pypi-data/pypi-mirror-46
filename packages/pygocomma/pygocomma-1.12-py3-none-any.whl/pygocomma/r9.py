'''
Created on 28 apr 2019

@author: Matteo
'''
import traceback
import struct
import asyncio
from base64 import b64decode, b64encode
import json
import time
from Crypto.Cipher import AES
import random, string
import binascii
from hashlib import md5
from . import _LOGGER
from .const import (CD_ADD_AND_CONTINUE_WAITING,CD_RETURN_IMMEDIATELY,CD_CONTINUE_WAITING,CD_ABORT_AND_RETRY)
from .asyncio_udp import open_local_endpoint

DEFAULT_PORT = 6668

class R9:
    STUDY_KEY_DICT = {
        "devId": '',
        "dps": {
            "1": "study_key",
            "10": 300,
            "7": '',
            #"8": keyorig
        },
        "t": 0,
        "uid": ''
    }
    STUDY_KEY_COMMAND = 7
    STUDY_KEY_RESP_1_COMMAND = 7
    STUDY_EXIT_COMMAND = 7
    STUDY_EXIT_RESP_COMMAND = 8
    STUDY_COMMAND = 7
    STUDY_RESP_COMMAND = 8
    STUDY_DICT = {
        "devId": '',
        "dps": {
            "1": "study",
            "10": 300
        },
        "t": 0,
        "uid": ''
    }
    
    STUDY_EXIT_DICT = {
        "devId": '',
        "dps": {
            "1": "study_exit",
            "10": 300
        },
        "t": 0,
        "uid": ''
    }
    
    ASK_LAST_DICT = {
        "devId": '',
        "gwId": ''
    }
    
    ASK_LAST_COMMAND = 0x0a
    ASK_LAST_RESP_COMMAND = 0x0a
    
    
    PING_COMMAND = 9
    PING_RESP_COMMAND = 9
    PING_DICT = {
    }
    
    PROTOCOL_VERSION_BYTES = b'3.1'
    
    LEARNED_COMMAND = 8
    
    crc32Table = [
      0x00000000, 0x77073096, 0xEE0E612C, 0x990951BA,
      0x076DC419, 0x706AF48F, 0xE963A535, 0x9E6495A3,
      0x0EDB8832, 0x79DCB8A4, 0xE0D5E91E, 0x97D2D988,
      0x09B64C2B, 0x7EB17CBD, 0xE7B82D07, 0x90BF1D91,
      0x1DB71064, 0x6AB020F2, 0xF3B97148, 0x84BE41DE,
      0x1ADAD47D, 0x6DDDE4EB, 0xF4D4B551, 0x83D385C7,
      0x136C9856, 0x646BA8C0, 0xFD62F97A, 0x8A65C9EC,
      0x14015C4F, 0x63066CD9, 0xFA0F3D63, 0x8D080DF5,
      0x3B6E20C8, 0x4C69105E, 0xD56041E4, 0xA2677172,
      0x3C03E4D1, 0x4B04D447, 0xD20D85FD, 0xA50AB56B,
      0x35B5A8FA, 0x42B2986C, 0xDBBBC9D6, 0xACBCF940,
      0x32D86CE3, 0x45DF5C75, 0xDCD60DCF, 0xABD13D59,
      0x26D930AC, 0x51DE003A, 0xC8D75180, 0xBFD06116,
      0x21B4F4B5, 0x56B3C423, 0xCFBA9599, 0xB8BDA50F,
      0x2802B89E, 0x5F058808, 0xC60CD9B2, 0xB10BE924,
      0x2F6F7C87, 0x58684C11, 0xC1611DAB, 0xB6662D3D,
      0x76DC4190, 0x01DB7106, 0x98D220BC, 0xEFD5102A,
      0x71B18589, 0x06B6B51F, 0x9FBFE4A5, 0xE8B8D433,
      0x7807C9A2, 0x0F00F934, 0x9609A88E, 0xE10E9818,
      0x7F6A0DBB, 0x086D3D2D, 0x91646C97, 0xE6635C01,
      0x6B6B51F4, 0x1C6C6162, 0x856530D8, 0xF262004E,
      0x6C0695ED, 0x1B01A57B, 0x8208F4C1, 0xF50FC457,
      0x65B0D9C6, 0x12B7E950, 0x8BBEB8EA, 0xFCB9887C,
      0x62DD1DDF, 0x15DA2D49, 0x8CD37CF3, 0xFBD44C65,
      0x4DB26158, 0x3AB551CE, 0xA3BC0074, 0xD4BB30E2,
      0x4ADFA541, 0x3DD895D7, 0xA4D1C46D, 0xD3D6F4FB,
      0x4369E96A, 0x346ED9FC, 0xAD678846, 0xDA60B8D0,
      0x44042D73, 0x33031DE5, 0xAA0A4C5F, 0xDD0D7CC9,
      0x5005713C, 0x270241AA, 0xBE0B1010, 0xC90C2086,
      0x5768B525, 0x206F85B3, 0xB966D409, 0xCE61E49F,
      0x5EDEF90E, 0x29D9C998, 0xB0D09822, 0xC7D7A8B4,
      0x59B33D17, 0x2EB40D81, 0xB7BD5C3B, 0xC0BA6CAD,
      0xEDB88320, 0x9ABFB3B6, 0x03B6E20C, 0x74B1D29A,
      0xEAD54739, 0x9DD277AF, 0x04DB2615, 0x73DC1683,
      0xE3630B12, 0x94643B84, 0x0D6D6A3E, 0x7A6A5AA8,
      0xE40ECF0B, 0x9309FF9D, 0x0A00AE27, 0x7D079EB1,
      0xF00F9344, 0x8708A3D2, 0x1E01F268, 0x6906C2FE,
      0xF762575D, 0x806567CB, 0x196C3671, 0x6E6B06E7,
      0xFED41B76, 0x89D32BE0, 0x10DA7A5A, 0x67DD4ACC,
      0xF9B9DF6F, 0x8EBEEFF9, 0x17B7BE43, 0x60B08ED5,
      0xD6D6A3E8, 0xA1D1937E, 0x38D8C2C4, 0x4FDFF252,
      0xD1BB67F1, 0xA6BC5767, 0x3FB506DD, 0x48B2364B,
      0xD80D2BDA, 0xAF0A1B4C, 0x36034AF6, 0x41047A60,
      0xDF60EFC3, 0xA867DF55, 0x316E8EEF, 0x4669BE79,
      0xCB61B38C, 0xBC66831A, 0x256FD2A0, 0x5268E236,
      0xCC0C7795, 0xBB0B4703, 0x220216B9, 0x5505262F,
      0xC5BA3BBE, 0xB2BD0B28, 0x2BB45A92, 0x5CB36A04,
      0xC2D7FFA7, 0xB5D0CF31, 0x2CD99E8B, 0x5BDEAE1D,
      0x9B64C2B0, 0xEC63F226, 0x756AA39C, 0x026D930A,
      0x9C0906A9, 0xEB0E363F, 0x72076785, 0x05005713,
      0x95BF4A82, 0xE2B87A14, 0x7BB12BAE, 0x0CB61B38,
      0x92D28E9B, 0xE5D5BE0D, 0x7CDCEFB7, 0x0BDBDF21,
      0x86D3D2D4, 0xF1D4E242, 0x68DDB3F8, 0x1FDA836E,
      0x81BE16CD, 0xF6B9265B, 0x6FB077E1, 0x18B74777,
      0x88085AE6, 0xFF0F6A70, 0x66063BCA, 0x11010B5C,
      0x8F659EFF, 0xF862AE69, 0x616BFFD3, 0x166CCF45,
      0xA00AE278, 0xD70DD2EE, 0x4E048354, 0x3903B3C2,
      0xA7672661, 0xD06016F7, 0x4969474D, 0x3E6E77DB,
      0xAED16A4A, 0xD9D65ADC, 0x40DF0B66, 0x37D83BF0,
      0xA9BCAE53, 0xDEBB9EC5, 0x47B2CF7F, 0x30B5FFE9,
      0xBDBDF21C, 0xCABAC28A, 0x53B39330, 0x24B4A3A6,
      0xBAD03605, 0xCDD70693, 0x54DE5729, 0x23D967BF,
      0xB3667A2E, 0xC4614AB8, 0x5D681B02, 0x2A6F2B94,
      0xB40BBE37, 0xC30C8EA1, 0x5A05DF1B, 0x2D02EF8D
    ]
    
    @staticmethod
    def crc32(cbytes):
        crc = 0xFFFFFFFF;
        for b in cbytes:
            crc = (crc >> 8) ^ R9.crc32Table[(crc ^ b) & 255]
        return crc ^ 0xFFFFFFFF;
    
    @staticmethod
    def _pad(s):
        padnum = 16 - len(s) % 16
        return s + padnum * chr(padnum)
    
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
    
    @staticmethod
    def check_discovery_packet(retdata,addr):
        lenorig = len(retdata)
        if lenorig<=12+8+8:
            _LOGGER.warning("CheckResp small len=%d",lenorig)
            return CD_CONTINUE_WAITING
        lenconf = struct.unpack('>I', retdata[12:16])[0]+8+8
        if lenconf!=lenorig:
            _LOGGER.warning("CheckResp len %d!=%d",lenorig,lenconf)
            return CD_CONTINUE_WAITING
        headerconf = struct.unpack('>I', retdata[0:4])[0]
        if headerconf!=0x000055AA:
            _LOGGER.warning("CheckResp header %d!=%d",0x000055AA,headerconf)
            return CD_CONTINUE_WAITING
        footerconf = struct.unpack('>I', retdata[-4:])[0]
        if footerconf!=0x0000AA55:
            _LOGGER.warning("CheckResp footer %d!=%d",0x0000AA55,headerconf)
            return CD_CONTINUE_WAITING
        crcconf =  struct.unpack('>I', retdata[-8:-4])[0]
        crcorig = R9.crc32(retdata[0:-8])        
        if crcconf!=crcorig:
            _LOGGER.warning("CheckResp crc %d!=%d",crcorig,crcconf)
            return CD_CONTINUE_WAITING
        statusconf = struct.unpack('>I', retdata[16:20])[0]
        if statusconf!=0:
            _LOGGER.warning("CheckResp status %d!=%d",0,statusconf)
            return CD_CONTINUE_WAITING
        payload = retdata[20:-8]
        try:
            jsonstr = payload.decode('utf-8')
        except BaseException as ex:
            _LOGGER.warning("CheckResp decode %s %s",ex,binascii.hexlify(payload))
            return CD_CONTINUE_WAITING
        except:
            _LOGGER.warning("CheckResp decode %s",binascii.hexlify(payload))
            return CD_CONTINUE_WAITING
        try:
            jsondec = json.loads(jsonstr)
        except BaseException as ex:
            _LOGGER.warning("CheckResp jsonp %s %s",ex,jsonstr)
            return CD_CONTINUE_WAITING
        except:
            _LOGGER.warning("CheckResp jsonp %s",jsonstr)
            return CD_CONTINUE_WAITING
        if "gwId" in jsondec:
            return CD_ADD_AND_CONTINUE_WAITING,jsondec
        else:
            return CD_CONTINUE_WAITING
        
    @staticmethod
    async def discovery(timeout,retry=3):
        """!
        Discovers Tuya devices listening to broadcast UDP messages sent to 6666 port
    
        @param timeout: [int] time to be waited for broadcast messages
        
        @param retry: [int] Number of retries to make if no device is found (Obtional)
        
        @return [dict] A dict whose keys are ip addresses of Tuya devices and values are R9 objects. Please note that th found R9 devices
        cannot be used before setting the correct encryption key (it is set to b'0123456789abcdef' by default)
          
        """
        out_data = None
        _local = None
        addr = ('255.255.255.255',6666)
        for _ in range(retry):
            try:
                _local = await open_local_endpoint(port=6666,allow_broadcast = True)
                if _local:
                    for _ in range(retry):
                        out_data = await _local.protocol(None,addr,R9.check_discovery_packet,timeout,1,True)
                        if out_data:
                            break
                    break
            except BaseException as ex:
                _LOGGER.error("Protocol[%s:%d] error: %s",*addr,str(ex))
            except:
                _LOGGER.error("Protocol[%s:%d] error %s",*addr,traceback.format_exc())
            finally:
                if _local:
                    try:
                        _local.abort()
                    except:
                        pass
                    finally:
                        _local = None
        if _local:
            try:
                _local.abort()
            except:
                pass
            finally:
                _local = None
        rv = dict()
        if out_data:
            for o in out_data:
                try:
                    it = o[0]
                    if it['ip'] not in rv:
                        obj = R9((it['ip'],DEFAULT_PORT) ,it['gwId'],b'0123456789abcdef')
                        rv[it['ip']] = obj
                        _LOGGER.info("Discovered %s",obj)
                except BaseException as ex:
                    _LOGGER.error("Error in discovery process %s", ex)
                except:
                    _LOGGER.error("Error in discovery process %s",traceback.format_exc())
        return rv
    
    def __init__(self,hp,idv,key,timeout = 5,force_reconnect_s = 20):
        """!
        Costructs R9 remote Object
    
        @param hp: [tuple] A tuple with host and port of the R9 remote
    
        @param idv: [string] id of the R9 object
        
        @param key: [string|bytes] key used to encrypt/decrypt messages from/to R9
        
        @param timeout: [int] timeout to be used in TCP communication (optional)
        
        @param force_reconnect_s: [int] seconds after which to force reconnection
          
        """
        self._hp = hp
        self._id = idv
        if isinstance(key, str):
            key = key.encode()
        self._key = key
        self._timeout = timeout
        self._cipher = AES.new(key, mode=AES.MODE_ECB)
        self._pktnum = 1
        self._uid = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        self._reader = None
        self._writer = None
        self._contime = 0
        self._force_reconnect_s = force_reconnect_s
    
    def __repr__(self):
        """!
        Gets string representation of this R9 object
        
        @return [string] string representation of this R9 object
          
        """
        return '(%s:%d) id=%s key=%s' %(*self._hp,self._id,self._key)
    
    async def destroy_connection(self):
        """!
        Destroys the connection with the R9 device    
        """
        try:
            if self._writer:
                self._writer.close()
                await self._writer.wait_closed()
        except:
            pass
        finally:
            self._writer = None
            self._reader = None
            self._pktnum = 1
    
    async def _init_connection(self):
        try:
            if self._force_reconnect_s>0 and time.time()-self._contime>self._force_reconnect_s:
                await self.destroy_connection()
            if not self._writer:
                _LOGGER.debug("Connecting to %s:%d (TCP)",*self._hp)
                self._reader,self._writer = await asyncio.open_connection(*self._hp)
                self._contime = time.time()
            return True
        except BaseException as ex:
            _LOGGER.error("Cannot estabilish connection %s: %s",ex,traceback.format_exc())
            await self.destroy_connection()
            return False
        except:
            _LOGGER.error("Cannot estabilish connection %s",traceback.format_exc())
            await self.destroy_connection()
            return False
    
    def _generic_check_resp(self,retdata,command,command_in_dict = None,status_ok = [0]):
        """!
        Checks payload of TCP packet got from R9 device. This includes Satus value check, CRC32 check, AES decryption (if needed), and MD5 check (if needed)
    
        @param retdata: [bytes] bytes of the TCP packet payload received prom R9 device
        
        @param command: [int] Command that is expected in the packet header
        
        @param command_in_dict: [string|NoneType] Command that is expected in the packet JSON dps["1"]. If NoneType, no JSON is expected in packet content. If equal to '', 
        no dps["1"] is expected in packet JSON
        
        @param status_ok: [list] Accepted status codes. Defaults to [0]
        
        @return [dict|boolean] On successful check if no JSON content is present, True is returned, Otherwise the parsed dict is returned.
        If check fails, False is returned
        """
        lenorig = len(retdata)
        if lenorig<12+8+8:
            _LOGGER.warning("CheckResp small len=%d",lenorig)
            return False
        lenconf = struct.unpack('>I', retdata[12:16])[0]+8+8
        if lenconf!=lenorig:
            _LOGGER.warning("CheckResp len %d!=%d",lenorig,lenconf)
            return False
        commandconf = struct.unpack('>I', retdata[8:12])[0]
        if commandconf!=command:
            _LOGGER.warning("CheckResp command[%d] %d!=%d",lenorig,command,commandconf)
            return False
        headerconf = struct.unpack('>I', retdata[0:4])[0]
        if headerconf!=0x000055AA:
            _LOGGER.warning("CheckResp header %d!=%d",0x000055AA,headerconf)
            return False
        footerconf = struct.unpack('>I', retdata[-4:])[0]
        if footerconf!=0x0000AA55:
            _LOGGER.warning("CheckResp footer %d!=%d",0x0000AA55,headerconf)
            return False
        crcconf =  struct.unpack('>I', retdata[-8:-4])[0]
        crcorig = R9.crc32(retdata[0:-8])        
        if crcconf!=crcorig:
            _LOGGER.warning("CheckResp crc %d!=%d",crcorig,crcconf)
            return False
        statusconf = struct.unpack('>I', retdata[16:20])[0]
        if statusconf not in status_ok:
            _LOGGER.warning("CheckResp status %d!=%d",status_ok,statusconf)
            return False
        if command_in_dict is None:
            return True
        if lenorig<=12+8+8+16+len(R9.PROTOCOL_VERSION_BYTES):
            _LOGGER.warning("CheckResp small2 len=%d",lenorig)
            return False
        protocolconf = retdata[20:23]
        if protocolconf!=R9.PROTOCOL_VERSION_BYTES:
            _LOGGER.warning("CheckResp prot %s!=%s",binascii.hexlify(R9.PROTOCOL_VERSION_BYTES),binascii.hexlify(protocolconf))
            return False
        b64payload = retdata[39:-8]
        hashconf = self._get_md5_hash(b64payload)
        hashorig = retdata[20:39]
        if hashconf!=hashorig:
            _LOGGER.warning("CheckResp md5 %s!=%s",binascii.hexlify(hashorig),binascii.hexlify(hashconf))
            return False
        try:
            cryptpayload = b64decode(b64payload)
        except BaseException as ex:
            _LOGGER.warning("CheckResp b64 %s %s",ex,binascii.hexlify(b64payload))
            return False
        except:
            _LOGGER.warning("CheckResp b64 %s",binascii.hexlify(b64payload))
            return False
        try:
            payload = self._cipher.decrypt(cryptpayload)
            payload = R9._unpad(payload)
        except BaseException as ex:
            _LOGGER.warning("CheckResp decry %s %s",ex,binascii.hexlify(cryptpayload))
            return False
        except:
            _LOGGER.warning("CheckResp decry %s",binascii.hexlify(cryptpayload))
            return False
        try:
            jsonstr = payload.decode('utf-8')
        except BaseException as ex:
            _LOGGER.warning("CheckResp decode %s %s",ex,binascii.hexlify(payload))
            return False
        except:
            _LOGGER.warning("CheckResp decode %s",binascii.hexlify(payload))
            return False
        try:
            jsondec = json.loads(jsonstr)
        except BaseException as ex:
            _LOGGER.warning("CheckResp jsonp %s %s",ex,jsonstr)
            return False
        except:
            _LOGGER.warning("CheckResp jsonp %s",jsonstr)
            return False
        if not len(command_in_dict):
            return jsondec
        if "dps" not in jsondec or "1" not in jsondec["dps"]:
            _LOGGER.warning("CheckResp struct %s",jsondec)
            return False
        if jsondec["dps"]["1"]!=command_in_dict:
            _LOGGER.warning("CheckResp command %s!=%s",command_in_dict,jsondec["dps"]["1"])
            return False
        return jsondec
    
    def _check_ping_resp(self,retdata):
        dictok = self._generic_check_resp(retdata,R9.PING_RESP_COMMAND)
        if dictok:
            return CD_RETURN_IMMEDIATELY,retdata
        else:
            return CD_CONTINUE_WAITING,None
        
    def _check_ask_last_resp(self,retdata):
        dictok = self._generic_check_resp(retdata,R9.ASK_LAST_RESP_COMMAND,status_ok=[0,1])
        if dictok:
            payload = retdata[20:-8]
            try:
                jsonstr = payload.decode('utf-8')
            except BaseException as ex:
                _LOGGER.warning("CheckResp decode %s %s",ex,binascii.hexlify(payload))
                return CD_CONTINUE_WAITING,None
            except:
                _LOGGER.warning("CheckResp decode %s",binascii.hexlify(payload))
                return CD_CONTINUE_WAITING,None
            if jsonstr.find("json obj")>=0:
                return CD_RETURN_IMMEDIATELY,{"devId":self._id}
            try:
                jsondec = json.loads(jsonstr)
            except BaseException as ex:
                _LOGGER.warning("CheckResp jsonp %s %s",ex,jsonstr)
                return CD_CONTINUE_WAITING,None
            except:
                _LOGGER.warning("CheckResp jsonp %s",jsonstr)
                return CD_CONTINUE_WAITING,None
            if ("devId" in jsondec and jsondec['devId']==self._id) or\
               ("gwId" in jsondec and jsondec['gwId']==self._id):
                return CD_RETURN_IMMEDIATELY,jsondec
        return CD_CONTINUE_WAITING,None
            
    async def ask_last(self,timeout = -1,retry = 2):
        """!
        Sends ping to R9 object to get last command. This command is sent not crypted
        
        @param timeout: [int] timeout to be used in TCP communication (optional). If not specified, the timeout specified when constructing the R9 object will be used
        
        @param retry: [int] Number of retries to make if no device is found (optional)
        
        @return [dict|NoneType] On successful send, the decoded confirmation dict obtained by R9 device is returned. Otherwise return value is None
          
        """
        pld = self._get_payload_bytes(R9.ASK_LAST_COMMAND,self._get_ask_last_bytes())
        return await self._tcp_protocol(pld, self._check_ask_last_resp, timeout, retry)
    async def ping(self,timeout = -1,retry = 2):
        """!
        Sends ping to R9 object to see if it is online
        
        @param timeout: [int] timeout to be used in TCP communication (optional). If not specified, the timeout specified when constructing the R9 object will be used
        
        @param retry: [int] Number of retries to make if no device is found (optional)
        
        @return [bytes|NoneType] On successful send, bytes got from R9 are returned; None otherwise.
          
        """
        pld = self._get_payload_bytes(R9.PING_COMMAND,{})
        return await self._tcp_protocol(pld, self._check_ping_resp, timeout, retry)
    
    def _check_study_resp(self,retdata):
        dictok = self._generic_check_resp(retdata,R9.STUDY_RESP_COMMAND,"study")
        if dictok:
            return CD_RETURN_IMMEDIATELY,dictok
        else:
            return CD_CONTINUE_WAITING,None
        
    def _check_study_key_resp(self,retdata):
        dictok = self._generic_check_resp(retdata,R9.STUDY_KEY_RESP_1_COMMAND)
        if dictok:
            return CD_RETURN_IMMEDIATELY,retdata
        else:
            return CD_CONTINUE_WAITING,None
        
    def _check_study_exit_resp(self,retdata):
        dictok = self._generic_check_resp(retdata,R9.STUDY_EXIT_RESP_COMMAND,"study_exit")
        if dictok:
            return CD_RETURN_IMMEDIATELY,dictok
        else:
            return CD_CONTINUE_WAITING,None
    
    async def emit_ir(self,keybytes,timeout = -1,retry=3):
        """!
        Sends ir to the R9 device
    
        @param keybytes: [bytes] key to be emitted by R9 device. The key should be a byte object that represents lirc/arduino format array of little-endian shorts.
        This is the same format obtained with the learning process
        
        @param timeout: [int] timeout to be used in TCP communication (optional). If not specified, the timeout specified when constructing the R9 object will be used
        
        @param retry: [int] Number of retries to make if no device is found (optional)
        
        @return [bytes|NoneType] On successful send, the array of bytes obtained by R9 device is returned. Otherwise return value is None
          
        """
        pld = self._get_payload_bytes(R9.STUDY_KEY_COMMAND,self._get_study_key_dict(keybytes))
        return await self._tcp_protocol(pld, self._check_study_key_resp, timeout,retry)
    
    async def enter_learning_mode(self,timeout = -1,retry=3):
        """!
        Puts R9 in learning mode
    
        @param timeout: [int] timeout to be used in TCP communication (optional). If not specified, the timeout specified when constructing the R9 object will be used
        
        @param retry: [int] Number of retries to make if no device is found (optional)
        
        @return [dict|NoneType] On successful send, the decoded confirmation dict obtained by R9 device is returned. Otherwise return value is None
          
        """
        pld = self._get_payload_bytes(R9.STUDY_COMMAND,self._get_study_dict())
        return await self._tcp_protocol(pld, self._check_study_resp, timeout, retry)
    
    async def exit_learning_mode(self,timeout = -1,retry=3):
        """!
        Exits R9 learning mode
    
        @param timeout: [int] timeout to be used in TCP communication (optional). If not specified, the timeout specified when constructing the R9 object will be used
        
        @param retry: [int] Number of retries to make if no device is found (optional)
        
        @return [dict|NoneType] On successful send, the decoded confirmation dict obtained by R9 device is returned. Otherwise return value is None
          
        """
        pld = self._get_payload_bytes(R9.STUDY_EXIT_COMMAND,self._get_study_exit_dict())
        return await self._tcp_protocol(pld, self._check_study_exit_resp, timeout,retry)
    
    def _check_learned_key(self,retdata):
        dictok = self._generic_check_resp(retdata,R9.LEARNED_COMMAND,"")
        if dictok:
            _LOGGER.debug("Learned dict %s",dictok)
            if "dps" not in dictok or "2" not in dictok["dps"]:
                _LOGGER.warning("CheckResp not2 %s",dictok)
                return CD_ABORT_AND_RETRY,None
            try:
                keydec = b64decode(dictok["dps"]["2"].encode())
            except BaseException as ex:
                _LOGGER.warning("CheckResp invalidkey %s %s",dictok,ex)
                return CD_ABORT_AND_RETRY,None
            except:
                _LOGGER.warning("CheckResp invalidkey %s",dictok)
                return CD_ABORT_AND_RETRY,None
            return CD_RETURN_IMMEDIATELY,keydec
        else:
            return CD_CONTINUE_WAITING,None
        
    async def get_learned_key(self,timeout=30):
        """!
        Puts R9 in learning mode
    
        @param timeout: [int] timeout to be used in TCP communication (optional). Default value is 30 seconds. If awaited, this method will block until a key is not received or
        timeout seconds have been passed
        
        @return [bytes|NoneType] On successful key reception, the byte object representing the learned key is returned. this can be used with emit_ir function for future key sending. It returns
        None on error or on timeout (no key was pressed/detected) 
        """
        return await self._tcp_protocol(None, self._check_learned_key, timeout,1)
        
    async def _tcp_protocol(self,data,check_data_fun,timeout = -1,retry=1):
        lstdata = []
        if timeout<0:
            timeout = self._timeout
        for _ in range(retry):
            try:
                passed = 0
                starttime = time.time()
                if await asyncio.wait_for(self._init_connection(),timeout):
                    if data:
                        self._writer.write(data)
                        await self._writer.drain()
                        self._contime = time.time()
                        self._pktnum+=1
                    while passed<timeout:
                        try:
                            rec_data = await asyncio.wait_for(self._reader.read(4096), timeout-passed)
                            #_LOGGER.info("Received[%s:%d][%d] %s",*self._hp,len(rec_data),binascii.hexlify(rec_data))
                            rv,rec_data = check_data_fun(rec_data) 
                            if rv==CD_RETURN_IMMEDIATELY:
                                return rec_data
                            elif rv==CD_ABORT_AND_RETRY:
                                break
                            elif rv==CD_ADD_AND_CONTINUE_WAITING:
                                lstdata.append(rec_data)
                        except asyncio.TimeoutError:
                            _LOGGER.warning("Protocol[%s:%d] timeout",*self._hp)
                            break
                        passed = time.time()-starttime
                    if lstdata:
                        return lstdata
                    elif not data:
                        break
            except asyncio.TimeoutError:
                _LOGGER.warning("Protocol[%s:%d] connecting timeout",*self._hp)
                await self.destroy_connection()
            except BaseException as ex:
                _LOGGER.warning("Protocol[%s:%d] error %s",*self._hp,ex)
                await self.destroy_connection()
            except:
                _LOGGER.warning("Protocol[%s:%d] error %s",*self._hp,traceback.format_exc())
                await self.destroy_connection()
        await self.destroy_connection()
        return None
    
    def _prepare_payload(self,dictjson):
        txtjs = json.dumps(dictjson)
        _LOGGER.debug("Send Schema (%d) %s",len(txtjs),txtjs)
        txtjs = R9._pad(txtjs).encode()
        crypted_text = self._cipher.encrypt(txtjs)
        _LOGGER.debug("Cipher (%d) %s",len(crypted_text),binascii.hexlify(crypted_text).decode('utf-8'))
        cifenc = b64encode(crypted_text)
        _LOGGER.debug("B64 cipher (%d) %s",len(cifenc),cifenc.decode('utf-8'))
        return cifenc
    
    def _generic_fill_dict(self,filld):
        filld["devId"] = self._id
        filld['t'] = int(time.time())
        filld['uid'] = self._uid
        return filld
    
    def _get_payload_bytes(self,command,filled_dict):
        if not filled_dict:
            pldall = bytes()
        elif isinstance(filled_dict, dict):
            pld = self._prepare_payload(filled_dict)
            md5bytes = self._get_md5_hash(pld)
            pldall = md5bytes+pld
        else:
            pldall = filled_dict
        ln = len(pldall)+16-8
        docrc = b'\x00\x00\x55\xAA'+struct.pack('>I',self._pktnum)+struct.pack('>I',command)+struct.pack('>I',ln)+pldall
        crcbytes = struct.pack('>I',R9.crc32(docrc))
        complete =  docrc+crcbytes+b'\x00\x00\xAA\x55'
        _LOGGER.debug("Comp packet (%d) %s",len(complete),binascii.hexlify(complete).decode('utf-8'))
        return complete
    
    def _get_study_key_dict(self,keybytes):
        R9.STUDY_KEY_DICT["dps"]["7"] = b64encode(keybytes).decode('utf8')
        return self._generic_fill_dict(R9.STUDY_KEY_DICT)
    
    def _get_study_dict(self):
        return self._generic_fill_dict(R9.STUDY_DICT)
    
    def _get_ask_last_bytes(self):
        R9.ASK_LAST_DICT["devId"] = self._id
        R9.ASK_LAST_DICT["gwId"] = self._id
        return json.dumps(R9.ASK_LAST_DICT).encode()
    
    def _get_study_exit_dict(self):
        return self._generic_fill_dict(R9.STUDY_EXIT_DICT)
    
    def _get_md5_hash(self,payload_bytes):
        preMd5String = b'data=' + payload_bytes + b'||lpv=' + R9.PROTOCOL_VERSION_BYTES + b'||' + self._key
        m = md5()
        m.update(preMd5String)
        #print(repr(m.digest()))
        hexdigest = m.hexdigest()
        s = hexdigest[8:][:16]
        _LOGGER.debug("Computed md5 %s",s)
        return R9.PROTOCOL_VERSION_BYTES+s.encode()
    
if __name__ == '__main__': # pragma: no cover
    import sys
    import logging
    async def testFake(n):
        for i in range(n):
            _LOGGER.debug("Counter is %d",i)
            await asyncio.sleep(1)
    async def ping_test(*args):
        a = R9((args[2],DEFAULT_PORT),args[3],args[4])
        rv = await a.ping()
        if rv:
            _LOGGER.info("Ping OK %s",binascii.hexlify(rv))
        else:
            _LOGGER.warning("Ping failed")
        await a.destroy_connection()
    async def ask_last_test(*args):
        a = R9((args[2],DEFAULT_PORT),args[3],args[4])
        rv = await a.ask_last()
        if rv:
            _LOGGER.info("Ask last OK %s",rv)
        else:
            _LOGGER.warning("Ask last failed")
        await a.destroy_connection()
    async def discovery_test(*args):
        rv = await R9.discovery(int(args[2]))
        if rv:
            _LOGGER.info("Discovery OK %s",rv)
        else:
            _LOGGER.warning("Discovery failed")
            
    async def emit_test(*args):
        import re
        mo = re.search('^[a-fA-F0-9]+$', args[5])
        if mo:
            payload = binascii.unhexlify(args[5])
        else:
            payload = b64decode(args[5])
        a = R9((args[2],DEFAULT_PORT),args[3],args[4])
        rv = await a.emit_ir(payload)
        if rv:
            _LOGGER.info("Emit OK %s",binascii.hexlify(rv).decode('utf-8'))
        else:
            _LOGGER.warning("Emit failed")
        await a.destroy_connection()
    async def learn_test(*args):
        a = R9((args[2],DEFAULT_PORT),args[3],args[4])
        rv = await a.enter_learning_mode()
        if rv:
            _LOGGER.info("Entered learning mode (%s): please press key",rv)
            rv = await a.get_learned_key()
            if rv:
                _LOGGER.info("Obtained %s",binascii.hexlify(rv).decode('utf-8'))
            else:
                _LOGGER.warning("No key pressed")
            rv = await a.exit_learning_mode()
            if rv:
                _LOGGER.info("Exit OK %s", rv)
            else:
                _LOGGER.warning("Exit failed")
        else:
            _LOGGER.warning("Enter learning failed")
        await a.destroy_connection()
    _LOGGER.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    _LOGGER.addHandler(handler)
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(testFake(150))
        if sys.argv[1]=="learn":
            loop.run_until_complete(learn_test(*sys.argv))
        elif sys.argv[1]=="discovery":
            loop.run_until_complete(discovery_test(*sys.argv))
        elif sys.argv[1]=="ping":
            loop.run_until_complete(ping_test(*sys.argv))
        elif sys.argv[1]=="asklast":
            loop.run_until_complete(ask_last_test(*sys.argv))
        elif sys.argv[1]=="pingst":
            for i in range(int(sys.argv[5])):
                loop.run_until_complete(ping_test(*sys.argv))
        else:
        #loop.run_until_complete(emit_test('00000000a801000000000000000098018e11951127029b0625029906270299062702380227023a0225023802270238022d023202270299062702990627029806270238022702380227023802270238022802370227023802270238022702980627023802240245021c02380227023802270238022702980627029c0623023802270298062702990627029b062502990627029906270220b7a1119d11270299062702990628029b06250238022702380227023802270238022702380227029906270299062702990627023802270238022a0234022702380227023802260238022702380226029a06260238022602380226023802260241021e02380227029b0624029906270238022702980627029b0625029906270299062702990629021db79f11a2112502990627029b0625029906270238022702380227023802270238022a02350227029906270299062702990628023702260238022702380227023802270238022702380226023b02240299062702380226023802270238022602380227023c0223029906270299062702380226029b062402990627029906270299062802980627020000'))
            loop.run_until_complete(emit_test(*sys.argv))
        #loop.run_until_complete(learn_test())
    except BaseException as ex:
        _LOGGER.error("Test error %s",str(ex))
        traceback.print_exc()
    except:
        _LOGGER.error("Test error")
        traceback.print_exc()
    finally:
        loop.close()
    