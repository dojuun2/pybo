import { writable } from "svelte/store";

/**
 * 이름(key)과 초기값(initValue)를 입력받아 writable 스토어를 생성하여 리턴하는 함수
 * @param {*} key 이름
 * @param {*} initValue 초기값
 * @returns Writable 스토어 변수
 */
const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

export const page = persist_storage("page", 0)  // 질문과 답변 페이지 번호
export const keyword = persist_storage("keyword", "")
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_login = persist_storage("is_login", false)   // 로그인 여부를 체크할 변수
export const category = persist_storage("category", "home")  // 카테고리
export const board_page = persist_storage("board_page", 0)  // 자유게시판 페이지 번호
export const prev_page = persist_storage("prev_page", "/")   // 이전 페이지
export const board_keyword = persist_storage("board_keyword", "")   // 자유게시판 검색어