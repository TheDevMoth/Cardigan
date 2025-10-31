import { expect, test, describe, beforeEach, afterEach, vi } from "vitest";
import { mount } from "@vue/test-utils";
import AudioModal from "@/components/AudioModal.vue";

describe("AudioModal.vue", () => {
    let wrapper: ReturnType<typeof mount>;
    let alertSpy: ReturnType<typeof vi.spyOn>;

    function uploadFile(File: File) {
        const input = wrapper.find('input[type="file"]');
        const changeEvent = new Event("change");
        Object.defineProperty(changeEvent, "target", {
            writable: false,
            value: { files: [File] },
        });
        input.element.dispatchEvent(changeEvent);
    }

    beforeEach(() => {
        wrapper = mount(AudioModal);
        alertSpy = vi.spyOn(window, "alert").mockImplementation(() => {});
    });

    afterEach(() => {
        wrapper.unmount();
        alertSpy.mockRestore();
    });

    test("should emit fileUploaded when a valid file is uploaded", async () => {
        const file = new File(["audio content"], "test.mp3", {
            type: "audio/mp3",
        });
        uploadFile(file);
        await wrapper.vm.$nextTick();

        console.log("Emitted events:", wrapper.emitted());

        expect(wrapper.emitted().fileUploaded).toBeTruthy();
        expect(wrapper.emitted().fileUploaded[0]![0]).toBe(file);
    });

    test("should not emit fileUploaded when file size exceeds 2MB", async () => {
        const largeFile = new File(
            ["a".repeat(2 * 1024 * 1024 + 1)],
            "large.mp3",
            { type: "audio/mp3" }
        );
        uploadFile(largeFile);
        await wrapper.vm.$nextTick();

        expect(wrapper.emitted().fileUploaded).toBeFalsy();
        expect(alertSpy).toHaveBeenCalled();
    });

    test("should emit fileRemoved when removeFile is called", async () => {
        const file = new File(["audio content"], "test.mp3", {
            type: "audio/mp3",
        });
        uploadFile(file);
        await wrapper.vm.$nextTick();

        const removeButton = wrapper.find("#remove-file");
        await removeButton.trigger("click");

        expect(wrapper.emitted().fileRemoved).toBeTruthy();
    });

    test("should display the remove button when a file is uploaded", async () => {
        const file = new File(["audio content"], "test.mp3", {
            type: "audio/mp3",
        });
        uploadFile(file);
        await wrapper.vm.$nextTick();

        expect(wrapper.find("#remove-file").exists()).toBe(true);
    });

    test("should hide the remove button when no file is uploaded", async () => {
        expect(wrapper.find("#remove-file").exists()).toBe(false);
    });

    test("should not emit fileUploaded when an invalid file type is uploaded", async () => {
        const file = new File(["text content"], "test.txt", {
            type: "text/plain",
        });
        uploadFile(file);
        await wrapper.vm.$nextTick();

        expect(wrapper.emitted().fileUploaded).toBeFalsy();
        expect(alertSpy).toHaveBeenCalled();
    });
});
