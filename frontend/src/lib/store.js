import { writable } from "svelte/store";

/**
 * 이름(key)과 초기값(initValue)를 입력받아 writable 스토어를 생성하여 리턴하는 함수
 * @param {*} key 이름
 * @param {*} initValue 초기값
 * @returns Writable 스토어 변수
 */
const persis_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

export const page = persis_storage("page", 0)