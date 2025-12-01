<template>
  <div class="border border-gray-200 rounded-xl overflow-hidden bg-white focus-within:ring-2 focus-within:ring-blue-500/20 transition-all duration-300">
    <!-- Toolbar -->
    <div v-if="editor" class="flex flex-wrap gap-1 p-2 border-b border-gray-100 bg-gray-50/50">
      <button 
        @click="editor.chain().focus().toggleBold().run()" 
        :class="{ 'bg-blue-100 text-blue-600': editor.isActive('bold'), 'text-gray-600 hover:bg-gray-200': !editor.isActive('bold') }"
        class="p-1.5 rounded-lg transition-colors"
        title="Bold"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 12h8a4 4 0 100-8H6v8zm0 0h8a4 4 0 110 8H6v-8z"></path></svg>
      </button>
      <button 
        @click="editor.chain().focus().toggleItalic().run()" 
        :class="{ 'bg-blue-100 text-blue-600': editor.isActive('italic'), 'text-gray-600 hover:bg-gray-200': !editor.isActive('italic') }"
        class="p-1.5 rounded-lg transition-colors"
        title="Italic"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>
      </button>
      <button 
        @click="editor.chain().focus().toggleStrike().run()" 
        :class="{ 'bg-blue-100 text-blue-600': editor.isActive('strike'), 'text-gray-600 hover:bg-gray-200': !editor.isActive('strike') }"
        class="p-1.5 rounded-lg transition-colors"
        title="Strike"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 15L3 9m0 0l6-6M9 9h10.5a2.5 2.5 0 010 5H9z"></path></svg>
      </button>
      <div class="w-px h-6 bg-gray-200 mx-1 self-center"></div>
      <button 
        @click="editor.chain().focus().setParagraph().run()" 
        :class="{ 'bg-blue-100 text-blue-600': editor.isActive('paragraph'), 'text-gray-600 hover:bg-gray-200': !editor.isActive('paragraph') }"
        class="p-1.5 rounded-lg transition-colors"
        title="Paragraph"
      >
        <span class="text-xs font-bold">P</span>
      </button>
      <button 
        @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" 
        :class="{ 'bg-blue-100 text-blue-600': editor.isActive('heading', { level: 1 }), 'text-gray-600 hover:bg-gray-200': !editor.isActive('heading', { level: 1 }) }"
        class="p-1.5 rounded-lg transition-colors"
        title="H1"
      >
        <span class="text-xs font-bold">H1</span>
      </button>
      <button 
        @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" 
        :class="{ 'bg-blue-100 text-blue-600': editor.isActive('heading', { level: 2 }), 'text-gray-600 hover:bg-gray-200': !editor.isActive('heading', { level: 2 }) }"
        class="p-1.5 rounded-lg transition-colors"
        title="H2"
      >
        <span class="text-xs font-bold">H2</span>
      </button>
      <div class="w-px h-6 bg-gray-200 mx-1 self-center"></div>
      <button 
        @click="editor.chain().focus().toggleBulletList().run()" 
        :class="{ 'bg-blue-100 text-blue-600': editor.isActive('bulletList'), 'text-gray-600 hover:bg-gray-200': !editor.isActive('bulletList') }"
        class="p-1.5 rounded-lg transition-colors"
        title="Bullet List"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
      </button>
      <button 
        @click="editor.chain().focus().toggleOrderedList().run()" 
        :class="{ 'bg-blue-100 text-blue-600': editor.isActive('orderedList'), 'text-gray-600 hover:bg-gray-200': !editor.isActive('orderedList') }"
        class="p-1.5 rounded-lg transition-colors"
        title="Ordered List"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14"></path></svg>
      </button>
    </div>

    <!-- Editor Content -->
    <editor-content :editor="editor" class="p-4 min-h-[150px] prose prose-sm max-w-none focus:outline-none" />
  </div>
</template>

<script setup lang="ts">
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import { watch, onBeforeUnmount } from 'vue'

const props = defineProps<{
  modelValue: string
  placeholder?: string
}>()

const emit = defineEmits(['update:modelValue'])

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit,
    Placeholder.configure({
      placeholder: props.placeholder || 'Write something...',
    }),
  ],
  editorProps: {
    attributes: {
      class: 'focus:outline-none min-h-[150px]',
    },
  },
  onUpdate: ({ editor }) => {
    emit('update:modelValue', editor.getHTML())
  },
})

watch(() => props.modelValue, (newValue) => {
  // Only update if the content is different to avoid cursor jumping
  const isSame = editor.value?.getHTML() === newValue
  if (!isSame && editor.value) {
    editor.value.commands.setContent(newValue, { emitUpdate: false })
  }
})

onBeforeUnmount(() => {
  editor.value?.destroy()
})
</script>

<style>
.ProseMirror p.is-editor-empty:first-child::before {
  color: #adb5bd;
  content: attr(data-placeholder);
  float: left;
  height: 0;
  pointer-events: none;
}
</style>
