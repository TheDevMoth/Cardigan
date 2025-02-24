<template>
    <div class="container d-flex flex-column">
        <div class="search-container mb-3">
            <input 
                type="text" 
                v-model="searchQuery" 
                class="form-control" 
                placeholder="Search emojis..."
            />
            <div class="category-filters mt-2 d-flex flex-wrap">
                <button 
                    v-for="category in categories" 
                    :key="category"
                    @click="selectCategory(category)"
                    :class="{ active: selectedCategory === category }"
                    class="btn btn-sm me-2 mb-2"
                >
                    {{ formatCategoryName(category) }}
                </button>
            </div>
        </div>


        <div class="emoji-container">
            <div class="emoji-grid">
                <button
                    v-for="(emoji, index) in filteredEmojis"
                    :key="emoji.code + index"
                    @click="selectEmoji(emoji)"
                    class="emoji-button"
                >
                    <span class="emoji-char">{{ getEmojiChar(emoji.code) }}</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import Konva from 'konva';
import emojiData from '@/assets/emojis.json';

type Emoji = {
    name: string;
    code: string;
    category: string;
}

function formatCategoryName(category: string): string {
    return category === 'all' ? 'All' 
        : category.split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
};

// Convert unicode string to emoji character
function getEmojiChar(unicode: string): string {
    return unicode.split('-')
        .map(hex => String.fromCodePoint(parseInt(hex, 16)))
        .join('');
};

function selectCategory(category: string) {
    selectedCategory.value = category;
};

function selectEmoji(emoji:Emoji) {
    const emojiBox = new Konva.Text({
        text: getEmojiChar(emoji.code),
        fontSize: 50,
        fontFamily: 'Arial',
        name: "Emoji"
    });
    emojiBox.className = "Emoji";
    
    emit('emoji-selected', emojiBox);
};

const searchQuery = ref('');
const selectedCategory = ref('all');
const emojis = ref<Emoji[]>([]);
const categories = computed(() => ['all', ...Object.keys(emojiData)]);
const filteredEmojis = computed(() => {
    return emojis.value.filter(emoji => {
        const matchesSearch = emoji.name.toLowerCase().includes(searchQuery.value.toLowerCase());
        const matchesCategory = selectedCategory.value === 'all' || 
            emoji.category === selectedCategory.value;
        return matchesSearch && matchesCategory;
    });
});

const emit = defineEmits<{ "emoji-selected": [shape: Konva.Text] }>();
// Load and flatten emoji data
onMounted(() => {
    const flattenedEmojis: Emoji[] = [];
    Object.entries(emojiData).forEach(([category, categoryEmojis]) => { // for each category in the file
        const emojisWithCategory: Emoji[] = (categoryEmojis).map(emoji => ({
            name: emoji.n[0],
            code: emoji.u,
            category
        }));
        flattenedEmojis.push(...emojisWithCategory);
    }, []);    
    emojis.value = flattenedEmojis;
});

</script>

<style scoped>
.search-container {
    position: sticky;
    top: 0;
    background-color: white;
    z-index: 1;
    padding: 10px 0;
    width: 355px;
}

.category-filters .btn {
    border: 1px solid #F5F3F4;
}

.category-filters .btn.active {
    background-color: #E5383B;
    color: white;
}

.emoji-button {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    border: 1px solid #F5F3F4;
    border-radius: 8px;
    background-color: white;
    cursor: pointer;
    transition: all 0.2s ease;
}

.emoji-button:hover {
    background-color: #f8f9fa;
    transform: scale(1.1);
}

.emoji-char {
    font-size: 1.5rem;
}

.container {
    height: 100%;
    max-height: calc(100vh - 96px); 
}

@media (min-width: 996px) {
    .container {
        height: calc(100vh - 56px);
    }
}
.emoji-container {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
    scrollbar-width: thin;
    scrollbar-color: #E5383B #f0f0f0;
    width: 355px;
}

.emoji-container::-webkit-scrollbar {
    width: 8px;
}

.emoji-container::-webkit-scrollbar-track {
    background: #f0f0f0;
    border-radius: 4px;
}

.emoji-container::-webkit-scrollbar-thumb {
    background-color: #E5383B;
    border-radius: 4px;
}

.emoji-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
    gap: 8px;
}
</style>