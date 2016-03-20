#coding:utf-8
import nuke
from duplicateNode import duplicateNode

def separate(rotoNode):
    # ROTO节点拆分
    ckLayer = rotoNode['curves'].rootLayer
    dir(ckLayer)
    nums = len(ckLayer)
    rotos = []
    for i in range(nums):
        dup_node = duplicateNode(rotoNode)
        dup_ckLayer = dup_node['curves'].rootLayer
        shapei = dup_ckLayer[i]
        dup_ckLayer.removeAll()
        dup_ckLayer.append(shapei)
        rotos.append(dup_node)
    return rotos

def combine(rotoNodes):
    # ROTO节点合并
    comb_rotoNode = nuke.nodes.Roto()
    ckLayer = comb_rotoNode['curves'].rootLayer
    for node in rotoNodes:
        node_ckLayer = node['curves'].rootLayer
        [ckLayer.append(shape) for shape in node_ckLayer]
    return comb_rotoNode

