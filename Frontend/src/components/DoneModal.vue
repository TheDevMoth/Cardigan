<template>
    <div class="modal fade" id="doneModal" tabindex="-1" aria-labelledby="doneModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="doneModalLabel">Share Options</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body p-0">
                        <div class="list-group">
                            <button type="button" class="list-group-item list-group-item-action py-3" data-bs-target="#shareModal" data-bs-toggle="modal" @click="emit('shareCard')">
                                Share as Cardigan card (url)
                            </button>
                            <button type="button" class="list-group-item list-group-item-action py-3"
                                @click="emit('downloadImages')">
                                Download as Images
                            </button>
                            <button type="button" class="list-group-item list-group-item-action py-3" @click="emit('downloadPDF')">
                                Download as PDF
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="shareModal" data-bs-backdrop="static" aria-hidden="true" aria-labelledby="shareModalLabel" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="shareModalLabel">{{ resultsReceived ? "Here is the link to your card" : "Your card is being created" }}</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="emit('closeShareModal'); close();"></button>
                    </div>
                    <div class="modal-body">
                        <span v-if="resultsReceived">
                            {{ results }}
                        </span>
                        <div v-else>
                            This is supposed to be a loading bar...
                        </div>
                    </div>
                </div>
            </div>
        </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const resultsReceived = ref(false);
const results = ref("");
const emit = defineEmits<{
    shareCard: [],
    downloadImages: [],
    downloadPDF: [],
    closeShareModal: [],
}>();
defineExpose({
    updateResults
});

function updateResults(res: string) {
    results.value = res;
    resultsReceived.value = true;
}
function close(){
    resultsReceived.value = false;
    results.value = ""
}

</script>

<style scoped>
    
</style>