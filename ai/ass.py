#coding:utf-8
'''
Created on 2015年11月13日 下午3:55:54

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: define ass object
'''

# import ai module
from arnold import ai_nodes, ai_render, ai_plugins, ai_msg, ai_dotass, ai_node_entry, ai_params, ai_universe
# ai_nodes module         #    主要是对节点的操作, 包括节点的创建与查询、 节点链接的创建、删除与查询、节点参数的set与get
# ai_render module        #    主要是begin 和 end
# ai_plugins module       #    加载插件
# ai_msg module           #    主要是显示日志等
# ai_dotass module        #    主要是对ass文件的读写
# ai_node_entry module    #    不太理解这个模块, 这里用这个模块查询了节点内包含的属性数量和序号
# ai_params module        #    主要是对节点参数的操作, 包括节点参数的类型和名称的查询等
# ai_universe module      #    主要是生成和销毁迭代器, 包括节点、aov等. 

# make funciton dic used for different types of parameters call differnet method
PARAMETER_FUNCTION_DIC = {
                          "BYTE": [ai_nodes.AiNodeSetByte, ai_nodes.AiNodeGetByte],
                          "INT": [ai_nodes.AiNodeSetInt, ai_nodes.AiNodeGetInt],
                          "UINT": [ai_nodes.AiNodeSetUInt, ai_nodes.AiNodeGetUInt],
                          "BOOL": [ai_nodes.AiNodeSetBool, ai_nodes.AiNodeGetBool],
                          "FLOAT": [ai_nodes.AiNodeSetFlt, ai_nodes.AiNodeGetFlt],
                          "RGB": [ai_nodes.AiNodeSetRGB, ai_nodes.AiNodeGetRGB],
                          "RGBA": [ai_nodes.AiNodeSetRGBA, ai_nodes.AiNodeGetRGBA],
                          "VEC": [ai_nodes.AiNodeSetVec, ai_nodes.AiNodeGetVec],
                          "POINT": [ai_nodes.AiNodeSetPnt, ai_nodes.AiNodeGetPnt],
                          "POINT2": [ai_nodes.AiNodeSetPnt2, ai_nodes.AiNodeGetPnt2],
                          "STRING": [ai_nodes.AiNodeSetStr, ai_nodes.AiNodeGetStr],
                          "PTR": [ai_nodes.AiNodeSetPtr, ai_nodes.AiNodeGetPtr],
                          "ARRAY": [ai_nodes.AiNodeSetArray, ai_nodes.AiNodeGetArray],
                          "pMTX": [ai_nodes.AiNodeSetMatrix, ai_nodes.AiNodeGetMatrix],
                          "ENUM": [ai_nodes.AiNodeSetStr, ai_nodes.AiNodeGetStr],
                          }

#===============================================================================
# ASSObject
#===============================================================================
class ASSObject(object):
    
    #===========================================================================
    # TianD_toolkit
    #===========================================================================
    def __init__(self, ass_path):
        super(ASSObject, self).__init__()
        self.__ass_path = ass_path
        self.load()
                    
    #===========================================================================
    # getPath
    #===========================================================================
    def getPath(self):
        '''
        return the ass file path
        '''
        return self.__ass_path
    
    #===========================================================================
    # consoleLog
    #===========================================================================
    def showConsoleLog(self):
        '''
        show log info in console
        '''
        ai_msg.AiMsgSetConsoleFlags(ai_msg.AI_LOG_ALL)
        
    #===========================================================================
    # loadPlugins
    #===========================================================================
    def loadPlugins(self, plugin_path = 'C:/solidangle/mtoadeploy/2014/shaders'):
        '''
        load third plugins for ai
        default load mtoa plugins
        '''
        ai_plugins.AiLoadPlugins(plugin_path)
        
    #===========================================================================
    # loadASS
    #===========================================================================
    def load(self):
        '''
        load ass file
        '''
        ai_render.AiBegin()
        
        self.loadPlugins()
        
        ai_dotass.AiASSLoad(self.__ass_path, ai_node_entry.AI_NODE_ALL)
        
    #===========================================================================
    # saveASS
    #===========================================================================
    def save(self):
        '''
        save changes
        '''
        ai_dotass.AiASSWrite(self.__ass_path, ai_node_entry.AI_NODE_ALL, False)
            
    #===========================================================================
    # closeASS
    #===========================================================================
    def close(self):
        '''
        close ass file
        '''
        ai_render.AiEnd()
    
    #===========================================================================
    # getNodeType
    #===========================================================================
    def draw(self, root = None):
        '''
        return a dict about the relationship between nodes
        '''
        tree = dict()
        return tree
            
    #===========================================================================
    # getASSParamType
    #===========================================================================
    def getParamType(self, node, parameter):
        '''
        get the parameter type of the node
        '''

        nentry = ai_nodes.AiNodeGetNodeEntry(node)
        
        count = ai_node_entry.AiNodeEntryGetNumParams(nentry)
        
        for i in range(count):
            
            pentry = ai_node_entry.AiNodeEntryGetParameter(nentry, i)
            pname = ai_params.AiParamGetName(pentry)
    
            if parameter == pname:
                ptypeIndex = ai_params.AiParamGetType(pentry)
                ptype = ai_params.AiParamGetTypeName(ptypeIndex)
                return ptype
    
    #===========================================================================
    # getASSParameter
    #===========================================================================
    def getValue(self, node, parameter):
        '''
        get the parameter value of the node
        '''
        # 获取节点属性值
        
        ptype = self.getParamType(node, parameter)
        # 获取属性连接节点
        link = ai_nodes.AiNodeGetLink(node, parameter)
        
        if link:
            value = link
        else :
            if PARAMETER_FUNCTION_DIC.has_key(ptype):
                try:
                    value = PARAMETER_FUNCTION_DIC[ptype][1](node, parameter)
                except Exception, e:
                    raise e, 'set {node}.{param}.value failure'.format(node = node, param = parameter)
        return value
    
    #===========================================================================
    # isLinked
    #===========================================================================
    def isLinked(self, node, parameter):
        '''
        whether the parameter of the node is linked
        '''
        
        ptype = self.getParamType(node, parameter)

        link = ai_nodes.AiNodeGetLink(node, parameter)
        if link:
            return True
        else :
            return False
    
    #===========================================================================
    # setASSParameter
    #===========================================================================
    def setValue(self, node, parameter, value):
        '''
        set the parameter value of the node
        '''
        
        ptype = self.getParamType(node, parameter)
        if PARAMETER_FUNCTION_DIC.has_key(ptype):
            try :
                value = PARAMETER_FUNCTION_DIC[ptype][0](node, parameter, value)
            except :
                return False
            return True
        else :
            return False
    
    #===========================================================================
    # getASSNode
    #===========================================================================
    def listNodes(self, nodeType = None, nameFilter = None, mask = ai_node_entry.AI_NODE_SHADER):
        '''
        List nodes in file
        '''
        # 获取.ass文件中的节点
        #
        # 参数ass_file: [string] ass文件路径
        # 参数nodeType: [string] 节点类型
        # 参数nameFilter: [list] 指定节点名称, 如果是None, 就是指定类型的所有节点; 如果是列表, 就匹配列表中的节点名称
        # 参数mask: [global variable] ai_node_entry内定义的节点类型的种类, 包括:
        #            AI_NODE_UNDEFINED =  0x0000  ## Undefined type
        #            AI_NODE_OPTIONS =    0x0001  ## Options node (following the "singleton" pattern, there is only one options node)
        #            AI_NODE_CAMERA =     0x0002  ## Camera nodes (\c persp_camera, \c fisheye_camera, etc)
        #            AI_NODE_LIGHT =      0x0004  ## Light source nodes (\c spot_light, etc)
        #            AI_NODE_SHAPE =      0x0008  ## Geometry nodes (\c sphere, \c polymesh, etc)
        #            AI_NODE_SHADER =     0x0010  ## Shader nodes (\c lambert, etc)
        #                maya的file节点、shadingEngine节点、shader节点都属于这个范围
        #            AI_NODE_OVERRIDE =   0x0020  ## EXPERIMENTAL: override nodes support "delayed parameter overrides" for \c procedural nodes
        #            AI_NODE_DRIVER =     0x0040  ## Output driver nodes (\c driver_tiff, etc)
        #            AI_NODE_FILTER =     0x0080  ## Pixel sample filter nodes (\c box_filter, etc
        #            AI_NODE_ALL =        0xFFFF  ## Bitmask including all node types, used by AiASSWrite()
        
        nodeLst = []
            
        iter = ai_universe.AiUniverseGetNodeIterator(mask)
        while not ai_universe.AiNodeIteratorFinished(iter):
            node = ai_universe.AiNodeIteratorGetNext(iter)
                                
            if ai_nodes.AiNodeIs(node, nodeType):
                if nameFilter:
                    name = node.AiNodeGetName(node)
                    if name in nameFilter:
                        nodeLst.append(node)
                    else :
                        continue
                else :
                    nodeLst.append(node)
                    
        ai_universe.AiNodeIteratorDestroy(iter)
    
        return nodeLst

if __name__ == '__main__':
    # 1.ass文件路径
    ass_file = "E:\\maya\\pSphere2.ass"
    # 2.实例化ASSObject
    assobj = ASSObject(ass_file)
    #assobj.showConsoleLog()
    # 3.获取指定类型的节点
    for n in assobj.listNodes("MayaFile"):
        # 4.获取属性
        value = assobj.getValue(n, "filename")
        print value
    # 4.关闭文件
    assobj.close()