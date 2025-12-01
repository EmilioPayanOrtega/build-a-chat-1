<template>
  <div class="h-full w-full">
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      :fit-view-on-init="true"
      class="bg-slate-50"
      :default-viewport="{ zoom: 1 }"
      :min-zoom="0.2"
      :max-zoom="4"
    >
      <Background pattern-color="#aaa" :gap="8" />
      <Controls />
      
      <template #node-default="props">
        <div 
          class="px-4 py-2 shadow-md rounded-md bg-white border-2 border-gray-200 min-w-[150px] text-center cursor-pointer transition-all duration-200 hover:shadow-lg"
          :class="{ 'min-w-[300px] max-w-[500px]': props.data.expanded }"
          @click="props.data.expanded = !props.data.expanded"
        >
          <div class="font-bold text-sm text-gray-700">{{ props.data.label }}</div>
          <div v-if="props.data.content" class="text-xs text-gray-500 mt-1">
            <div :class="{ 'truncate max-w-[200px]': !props.data.expanded, 'whitespace-pre-wrap text-left': props.data.expanded }">
              <a 
                v-if="props.data.content.startsWith('http')" 
                :href="props.data.content" 
                target="_blank" 
                class="text-blue-600 hover:underline"
                @click.stop
              >
                {{ props.data.content }}
              </a>
              <span v-else>{{ props.data.content }}</span>
            </div>
            <div v-if="!props.data.expanded" class="flex justify-center mt-1">
              <svg class="w-4 h-4 text-gray-400 animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            </div>
            <div v-else class="flex justify-center mt-2 pt-2 border-t border-gray-100">
              <svg class="w-4 h-4 text-gray-400 transform rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            </div>
          </div>
        </div>
      </template>
    </VueFlow>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { VueFlow, useVueFlow } from '@vue-flow/core';
import { Background } from '@vue-flow/background';
import { Controls } from '@vue-flow/controls';
import dagre from 'dagre';
import '@vue-flow/core/dist/style.css';
import '@vue-flow/controls/dist/style.css';

const props = defineProps<{
  data: any | null;
}>();

const nodes = ref<any[]>([]);
const edges = ref<any[]>([]);
const { fitView } = useVueFlow();

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const nodeWidth = 172;
const nodeHeight = 80;

const getLayoutedElements = (nodes: any[], edges: any[], direction = 'TB') => {
  dagreGraph.setGraph({ rankdir: direction });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  nodes.forEach((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    node.position = {
      x: nodeWithPosition.x - nodeWidth / 2,
      y: nodeWithPosition.y - nodeHeight / 2,
    };
  });

  return { nodes, edges };
};

const transformDataToFlow = (treeData: any) => {
  if (!treeData) return { nodes: [], edges: [] };

  const flowNodes: any[] = [];
  const flowEdges: any[] = [];

  const traverse = (node: any, parentId: string | null = null) => {
    const nodeId = node.id.toString();
    
    flowNodes.push({
      id: nodeId,
      type: 'default',
      data: { 
        label: node.label,
        content: node.content,
        expanded: false
      },
      position: { x: 0, y: 0 }, // Initial position, will be calculated by dagre
    });

    if (parentId) {
      flowEdges.push({
        id: `e${parentId}-${nodeId}`,
        source: parentId,
        target: nodeId,
        type: 'smoothstep',
        animated: true,
      });
    }

    if (node.children && node.children.length > 0) {
      node.children.forEach((child: any) => traverse(child, nodeId));
    }
  };

  traverse(treeData);

  return { nodes: flowNodes, edges: flowEdges };
};

const updateLayout = () => {
  if (!props.data) return;

  const { nodes: rawNodes, edges: rawEdges } = transformDataToFlow(props.data);
  const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
    rawNodes,
    rawEdges,
    'TB' // Top to Bottom
  );

  nodes.value = layoutedNodes;
  edges.value = layoutedEdges;
  
  // Fit view after a short delay to allow rendering
  setTimeout(() => {
    fitView();
  }, 50);
};

watch(() => props.data, () => {
  updateLayout();
}, { deep: true });

onMounted(() => {
  updateLayout();
});
</script>

<style>
/* Import default styles */
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/controls/dist/style.css';
</style>
