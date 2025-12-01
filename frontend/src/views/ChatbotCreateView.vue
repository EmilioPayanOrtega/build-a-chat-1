<template>
  <div class="min-h-screen bg-slate-50 p-6 animate-fade-in">
    <div class="max-w-7xl mx-auto space-y-6">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-800">Crear Nuevo Chatbot</h1>
          <p class="text-gray-500 mt-1">Define la estructura de conocimiento y la personalidad de tu asistente.</p>
        </div>
        <div class="flex gap-3">
          <button @click="$router.push('/dashboard')" class="px-4 py-2 rounded-xl text-gray-600 hover:bg-gray-100 font-medium transition-colors">
            Cancelar
          </button>
          <button @click="saveChatbot" :disabled="saving" class="px-6 py-2 rounded-xl bg-blue-600 text-white font-medium hover:bg-blue-700 transition-colors shadow-lg shadow-blue-200 disabled:opacity-70 disabled:cursor-not-allowed flex items-center gap-2">
            <span v-if="saving" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></span>
            {{ saving ? 'Guardando...' : 'Publicar Chatbot' }}
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column: Settings -->
        <div class="lg:col-span-1 space-y-6">
          <!-- Basic Info Card -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 space-y-4">
            <h2 class="text-lg font-bold text-gray-800 flex items-center gap-2">
              <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              Información Básica
            </h2>
            
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">Título del Chatbot</label>
              <input v-model="title" type="text" placeholder="Ej: Guía de Trámites 2024" class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all">
            </div>

            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">Descripción</label>
              <textarea 
                v-model="description" 
                rows="4"
                class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all resize-none"
                placeholder="Describe el propósito de este chatbot..."
              ></textarea>
            </div>

            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700">Visibilidad</label>
              <select v-model="visibility" class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all bg-white">
                <option value="public">Público (Visible para todos)</option>
                <option value="link_only">Solo con enlace</option>
                <option value="private">Privado (Solo yo)</option>
              </select>
            </div>
          </div>

          <!-- Tree Editor Input -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 space-y-4 flex flex-col h-[500px]">
            <div class="flex justify-between items-center">
              <h2 class="text-lg font-bold text-gray-800 flex items-center gap-2">
                <svg class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                Estructura del Árbol
              </h2>
              <span class="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded">Indentación: 2 espacios | Usa "|" para contenido</span>
            </div>
            <p class="text-xs text-gray-500">Escribe la jerarquía usando indentación. Cada línea es un nodo.</p>
            
            <textarea 
              v-model="treeInput" 
              class="flex-1 w-full p-4 rounded-xl border border-gray-200 font-mono text-sm focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all resize-none bg-slate-50 leading-relaxed"
              placeholder="Raíz del Tema | Descripción general del tema
  Capítulo 1 | Introducción al capítulo
    Sección 1.1 | Detalle específico
    Sección 1.2
  Capítulo 2"
              @input="updateTreePreview"
            ></textarea>
          </div>
        </div>

        <!-- Right Column: Preview -->
        <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col">
          <div class="p-4 border-b border-gray-100 bg-gray-50/50 flex justify-between items-center">
            <h2 class="font-bold text-gray-800">Vista Previa del Mapa</h2>
            <div class="flex gap-2">
              <button @click="() => fitView()" class="p-1.5 text-gray-500 hover:bg-white rounded-lg transition-colors" title="Centrar">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"></path></svg>
              </button>
            </div>
          </div>
          <div class="flex-1 bg-slate-50 relative min-h-[600px]">
             <VueFlow
              v-model="elements"
              :default-viewport="{ zoom: 1 }"
              :min-zoom="0.2"
              :max-zoom="4"
              fit-view-on-init
              class="h-full w-full"
            >
              <Background pattern-color="#e2e8f0" :gap="16" />
              <Controls />
              <MiniMap />
              
              <template #node-default="props">
                <div 
                  class="px-4 py-2 shadow-md rounded-md bg-white border-2 border-gray-200 min-w-[150px] text-center cursor-pointer transition-all duration-200 hover:shadow-lg"
                  :class="{ 'min-w-[300px] max-w-[500px]': props.data.expanded }"
                  @click="props.data.expanded = !props.data.expanded"
                >
                  <div class="font-bold text-sm text-gray-700">{{ props.data.label }}</div>
                  <div v-if="props.data.content" class="text-xs text-gray-500 mt-1">
                    <div :class="{ 'truncate max-w-[200px]': !props.data.expanded, 'whitespace-pre-wrap text-left': props.data.expanded }">
                      <template v-for="(segment, i) in parseContent(props.data.content)" :key="i">
                        <a 
                          v-if="segment.isLink" 
                          :href="segment.text" 
                          target="_blank" 
                          class="text-blue-600 hover:underline break-all"
                          @click.stop
                        >
                          {{ segment.text }}
                        </a>
                        <span v-else>{{ segment.text }}</span>
                      </template>
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { VueFlow, useVueFlow } from '@vue-flow/core';
import { Background } from '@vue-flow/background';
import { Controls } from '@vue-flow/controls';
import { MiniMap } from '@vue-flow/minimap';
import dagre from 'dagre';
import '@vue-flow/core/dist/style.css';
import '@vue-flow/controls/dist/style.css';
import '@vue-flow/minimap/dist/style.css';

const router = useRouter();
const { fitView } = useVueFlow();

// Form State
const title = ref('');
const description = ref('');
const visibility = ref('public');
const saving = ref(false);

// Tree State
const treeInput = ref('Raíz\n  Hijo 1\n    Nieto 1.1\n  Hijo 2');
const elements = ref<any[]>([]);

// Graph Layout Logic using Dagre
const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const nodeWidth = 172;
const nodeHeight = 36;

function getLayoutedElements(nodes: any[], edges: any[]) {
  dagreGraph.setGraph({ rankdir: 'TB' });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  return [
    ...nodes.map((node) => {
      const nodeWithPosition = dagreGraph.node(node.id);
      return {
        ...node,
        position: { x: nodeWithPosition.x - nodeWidth / 2, y: nodeWithPosition.y - nodeHeight / 2 },
      };
    }),
    ...edges,
  ];
}

// Parsing Logic
interface GraphNode {
  id: string;
  label: string;
  parentId: string | null;
}

function parseIndentedText(text: string): { nodes: any[], edges: any[] } {
  const lines = text.split('\n');
  const nodes: any[] = [];
  const edges: any[] = [];
  const stack: { level: number; id: string }[] = [];
  
  lines.forEach((line, index) => {
    // 1. Detect indentation (assuming 2 spaces per level)
    if (!line.trim()) return;
    
    // Count leading spaces
    const match = line.match(/^(\s*)/);
    const spaces = match ? match[1].length : 0;
    const level = Math.floor(spaces / 2);
    
    const id = `node-${index}`;
    const parts = line.trim().split('|');
    const label = parts[0].trim();
    const content = parts.slice(1).join('|').trim();
    
    // 2. Find parent
    // Pop stack until we find the direct parent (one level less)
    while (stack.length > 0 && stack[stack.length - 1].level >= level) {
      stack.pop();
    }
    
    const parentId = stack.length > 0 ? stack[stack.length - 1].id : null;
    
    nodes.push({
      id,
      label, // For internal logic
      type: 'default',
      data: { label, content, expanded: false }, // For Vue Flow
      position: { x: 0, y: 0 }, // Will be set by layout
      style: { 
        background: '#fff', 
        border: '1px solid #e2e8f0', 
        borderRadius: '8px', 
        padding: '8px 16px',
        width: 'auto',
        minWidth: '100px',
        textAlign: 'center',
        fontSize: '14px'
      }
    });

    if (parentId) {
      edges.push({
        id: `e-${parentId}-${id}`,
        source: parentId,
        target: id,
        type: 'smoothstep',
        animated: true,
        style: { stroke: '#94a3b8' }
      });
    }
    
    stack.push({ level, id });
  });

  return { nodes, edges };
}

function updateTreePreview() {
  const { nodes, edges } = parseIndentedText(treeInput.value);
  elements.value = getLayoutedElements(nodes, edges);
  setTimeout(() => fitView(), 50);
}

async function saveChatbot() {
  if (!title.value.trim()) {
    alert('Por favor ingresa un título');
    return;
  }
  
  saving.value = true;
  
  try {
    // Convert flat nodes to nested JSON for backend
    // Or send flat list if backend supports it. Design doc says "Frontend parses... into nested JSON".
    // Let's implement the nesting logic.
    
    const { nodes } = parseIndentedText(treeInput.value);
    
    // Helper to nest
    const nest = (items: any[], id = null, link = 'parentId'): any[] =>
      items
        .filter(item => item[link] === id)
        .map(item => ({ ...item, children: nest(items, item.id) }));
    
    // We need to reconstruct the parentId relationship from the parsing logic
    // The parseIndentedText function above didn't return parentId in the node object for the final array, 
    // but we can easily add it or re-parse.
    
    // Let's re-parse to get the structure with parentIds for saving
    const lines = treeInput.value.split('\n');
    const rawNodes: any[] = [];
    const stack: { level: number; id: string }[] = [];
    
    lines.forEach((line, index) => {
      if (!line.trim()) return;
      const match = line.match(/^(\s*)/);
      const spaces = match ? match[1].length : 0;
      const level = Math.floor(spaces / 2);
      const id = `node-${index}`;
      
      while (stack.length > 0 && stack[stack.length - 1].level >= level) stack.pop();
      const parentId = stack.length > 0 ? stack[stack.length - 1].id : null;
      
      const parts = line.trim().split('|');
      const label = parts[0].trim();
      const content = parts.slice(1).join('|').trim();
      
      
      rawNodes.push({ id, label, parentId, content });
      stack.push({ level, id });
    });
    
    // Convert to nested structure
    // The root nodes are those with parentId === null
    const buildTree = (parentId: string | null): any[] => {
      return rawNodes
        .filter(n => n.parentId === parentId)
        .map(n => ({
          label: n.label,
          content: n.content,
          children: buildTree(n.id)
        }));
    };
    
    const treeStructure = {
      label: 'Root', // Wrapper if needed, or just list of roots. 
      // Design doc example shows a single root object: { label: "Root", children: [...] }
      // But our input might have multiple top-level items.
      // Let's assume the first item is root or wrap them.
      // If multiple roots, we might need a virtual root.
      // For now, let's wrap in a virtual root if multiple, or just take the first one.
      // Actually, let's send the list of roots.
      // Design doc says: "Frontend parses... into a nested JSON structure".
      // Example: { "label": "Root", "children": [...] }
      
      // Let's assume the user input starts with a single root.
      // If not, we'll wrap it.
    };
    
    const roots = buildTree(null);
    let finalTree;
    if (roots.length === 1) {
      finalTree = roots[0];
    } else {
      finalTree = {
        label: title.value, // Use title as root label if multiple top-levels
        content: description.value,
        children: roots
      };
    }

    const payload = {
      title: title.value,
      description: description.value,
      visibility: visibility.value,
      tree_json: finalTree
    };

    const response = await fetch('/api/chatbots', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (data.success) {
      router.push('/dashboard');
    } else {
      alert('Error al guardar: ' + (data.error || 'Unknown error'));
    }
  } catch (e) {
    console.error(e);
    alert('Error de conexión');
  } finally {
    saving.value = false;
  }
}

onMounted(() => {
  updateTreePreview();
});

function parseContent(text: string) {
  if (!text) return [];
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  const parts = text.split(urlRegex);
  return parts.map(part => ({
    text: part,
    isLink: urlRegex.test(part)
  })).filter(part => part.text);
}
</script>

<style>
/* Vue Flow Customization */
.vue-flow__node-default {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  padding: 10px 20px;
  font-weight: 500;
  color: #1e293b;
  width: auto !important;
}
.vue-flow__edge-path {
  stroke: #94a3b8;
  stroke-width: 2;
}
</style>
