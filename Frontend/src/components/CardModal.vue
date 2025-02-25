<template>
    <div class="modal fade" ref="cardTypeModal" data-bs-backdrop="static" tabindex="-1"
        aria-labelledby="cardTypeModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="cardTypeModalLabel">Choose a Card Type</h5>
                </div>
                <div class="modal-body">
                    <div class="button-container">
                        <button class="btn type-button" @click="emit('cardSelected', CardType.Openable)" data-bs-dismiss="modal">
                            <div class="button-content">
                                <img src="/openable.png" alt="Openable card">
                                <span>Openable</span>
                            </div>
                        </button>
                        <button class="btn type-button" @click="emit('cardSelected', CardType.TwoSided)" data-bs-dismiss="modal">
                            <div class="button-content">
                                <img src="/doublesided.png" alt="Double-sided card">
                                <span>Front & Back</span>
                            </div>
                        </button>
                        <button class="btn type-button" @click="emit('cardSelected', CardType.OneSided)" data-bs-dismiss="modal">
                            <div class="button-content">
                                <img src="/onesided.png" alt="One-sided card">
                                <span>One-Sided</span>
                            </div>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Modal } from 'bootstrap';
import { onMounted, useTemplateRef } from 'vue';
import { CardType } from '@/scripts/Constants';

const modal = useTemplateRef("cardTypeModal");
var cardModal: Modal;
const emit = defineEmits<{
    cardSelected: [type: CardType]
}>();

onMounted(() => {
    cardModal = new Modal(modal.value!, {});
    cardModal.show();
});


</script>

<style scoped>
.button-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 16px;
}

.type-button {
    align-items: center;
    padding: 10px;
    border: none;
    background-color: white;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
    cursor: pointer;
    display: flex;
    justify-content: center;
    width: 100%;
}

.button-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}

.modal-body {
    background-color: #F5F3F4;
}

img {
    height: 120px;
    max-width: 100%;
}

span {
    font-size: 1rem;
}
</style>