<template>
<div class="modal fade" id="audioModal" ref="audioModal" data-bs-backdrop="static" tabindex="-1" aria-labelledby="audioModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="audioModalLabel">Upload an audio clip</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <p>
                    This audio clip will play when the card is opened.
                    File size is limited to 2 MB.
                </p>
                <input type="file" ref="audioInput" @change="handleAudioUpload" accept="audio/*" />
                <button v-if="audioUploaded" type="button" class="btn-close" id="remove-file" @click="removeFile"></button>
            </div>
        </div>
    </div>
</div>
</template>

<script setup lang="ts">
import { ref, useTemplateRef } from 'vue';

const audioUploaded = ref(false);
const audioInput = useTemplateRef("audioInput");

const emit = defineEmits<{
    fileUploaded: [file: File],
    fileRemoved: []
}>();

function removeFile() {
    audioUploaded.value = false;
    audioInput.value!.value = '';
    emit("fileRemoved");
}
function handleAudioUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files || !input.files[0]) return;

    const file = input.files[0];
    const maxSize = 2 * 1024 * 1024; // 2MB in bytes

    // Check file size
    if (file.size > maxSize) {
        alert('Audio file must be less than 2MB');
        input.value = '';
        return;
    } else if (file.type !== 'audio/mpeg' && file.type !== 'audio/wav' && file.type !== 'audio/mp3') {
        alert('Invalid audio format. Please upload an mp3, wav, or mpeg file.');
        input.value = '';
        return;
    }

    // Store the file for later upload
    audioUploaded.value = true;
    emit('fileUploaded', file);
}

</script>