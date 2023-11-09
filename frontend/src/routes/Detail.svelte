<script>
    import fastapi from "../lib/api";
    import Error from "../components/Error.svelte"
    import { link, push } from "svelte-spa-router";
    import moment from "moment/min/moment-with-locales"
    import { is_login, username } from "../lib/store";
    import { marked } from "marked"

    export let params = {}
    let question_id = params.question_id
    let question = {answers:[], voter:[], content: ""}
    let content = ""
    let error = {detail:[]}
    let page = 0    // 현재 페이지
    let size = 10   // 보여질 답변 건수
    let total = 0   // 전체 답변 건수
    let sort_order = "date"; // 답변 정렬에 쓰일 변수(기본값 "date")
    $: total_page = Math.ceil(total / size)   // 전체 페이지

    function get_question(_page) {
        let params = {
            size: size * (_page + 1),
            sort_order: sort_order,
        }

        fastapi("get", "/api/questions/" + question_id, params, (json) => {
            total = json.total
            page = _page
            question = json.question
        })
    }

    get_question(0)

    // 답변 등록
    function post_answer(event) {
        event.preventDefault()  // submit이 눌릴경우 form이 자동으로 전동되는 것을 방지하기 위함
        
        let url = "/api/answer/create/" + question_id
        let params = {
            content: content,
        }
        fastapi("post", url, params, 
            (json) => {
                content = ""
                error = {detail:[]}
                get_question(page)
            }, 
            (err_json) => {
                error = err_json
            }
        )
    }

    // 질문 삭제
    function delete_question(question_id) {
        if(confirm("정말 삭제하시겠습니까?")) {
            let url = "/api/question/delete/" + question_id
            
            fastapi("delete", url, {}, 
                (json) => {
                    push("/")
                }, 
                (json_error) => {
                    error = json_error
                }
            )
        }
    }

    // 답변 삭제
    function delete_answer(answer_id) {
        if(confirm("정말 삭제하시겠습니까?")) {
            let url = "/api/answer/delete/" + answer_id
            
            fastapi("delete", url, {}, 
                (json) => {
                    get_question(page)
                }, 
                (json_error) => {
                    error = json_error
                }
            )
        }
    }

    // 질문 추천
    function vote_question(question_id) {
        let url = "/api/question/vote/" + question_id
        fastapi("post", url, {}, 
            (json) => {
                get_question(page)
            },
            (json_error) => {
                error = json_error
            }
        )
    }

    // 질문 추천취소
    function unvote_question(question_id) {
        let url = "/api/question/unvote/" + question_id
        fastapi("delete", url, {}, 
            (json) => {
                get_question(page)
            },
            (json_error) => {
                error = json_error
            }
        )
    }

    // 답변 추천
    function vote_answer(answer_id) {
        let url = "/api/answer/vote/" + answer_id

        fastapi("post", url, {}, 
            (json) => {
                get_question(page)
            },
            (json_error) => {
                error = json_error
            }
        )
    }

    // 답변 추천취소
    function unvote_answer(answer_id) {
        let url = "/api/answer/unvote/" + answer_id

        fastapi("post", url, {}, 
            (json) => {
                get_question(page)
            },
            (json_error) => {
                error = json_error
            }
        )
    }

    // 질문, 답변 추천여부 판단 함수
    function check_voted(post) {
        // 추천을 한 게시물이면 true 반환
        if (post.voter.some(voter => voter.username === $username)) {
            return true
        } 

        // 그렇지 않은 경우엔 false 반환
        return false
    }


    // 선택한 정렬 옵션의 변경 이벤트를 처리하는 함수
    function handleSelectChange(event) {
        sort_order = event.target.value;
        get_question(page)
    }
</script>

<div class="container my-3">
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{question.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text">{@html marked.parse(question.content)}</div>
            <div class="d-flex justify-content-end">
                {#if question.modify_date}
                    <div class="badge bg-light text-dark p-2 text-start mx-3">
                        <div class="mb-2">modified at</div>
                        <div>{moment(question.modify_date).format("YYYY년 MM월 DD일 HH:mm")}</div>
                    </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{question.user ? question.user.username : ""}</div>
                    <div>{moment(question.create_date).format("YYYY년 MM월 DD일 HH:mm")}</div>
                </div>
            </div>
            <div class="my-3">
                <button 
                    class="btn btn-sm {check_voted(question) ? "btn-secondary" : "btn-outline-secondary"}" 
                    on:click={() => check_voted(question) 
                                                ? unvote_question(question.id) 
                                                : vote_question(question.id)}
                    >
                    추천
                    <span class="badge rounded-pill bg-success">{question.voter.length}</span>
                </button>
                {#if question.user && $username === question.user.username}
                    <a use:link href="/question-modify/{question.id}" class="btn btn-sm btn-outline-secondary">수정</a>
                    <button class="btn btn-sm btn-outline-secondary" on:click={() => delete_question(question.id)}>삭제</button>
                {/if}
            </div>
        </div>
    </div>

    <button class="btn btn-primary" on:click={() => {push("/")}}>목록으로</button>

    <!-- 답변 목록 -->
    <div class="border-bottom my-3 py-2 d-flex justify-content-between">
        <h5>{total}개의 답변이 있습니다.</h5>
        <!-- 답변 정렬 방법 -->
        <select name="answerSort" id="answerSort" on:change={handleSelectChange}>
            <option value="date">최신순</option>
            <option value="vote">추천순</option>
        </select>
    </div>    
    {#each question.answers as answer}
        <div class="card my-3">
            <div class="card-body">
                <div class="card-text">{@html marked.parse(answer.content)}</div>
                <div class="d-flex justify-content-end">
                    {#if answer.modify_date}
                        <div class="badge bg-light text-dark p-2 text-start mx-2">
                            <div class="mb-2">modified at</div>
                            <div>{moment(answer.modify_date).format("YYYY년 MM월 DD일 HH:mm")}</div>
                        </div>
                    {/if}
                    <div class="badge bg-light text-dark p-2 text-start">
                        <div class="mb-2">{answer.user ? answer.user.username : ""}</div>
                        <div>{moment(answer.create_date).format("YYYY년 MM월 DD일 HH:mm")}</div>
                    </div>
                </div>
                <div class="my-3">
                    <button class="btn btn-sm {check_voted(answer) ? "btn-secondary" : "btn-outline-secondary"}" 
                        on:click={() => check_voted(answer) ? unvote_answer(answer.id) : vote_answer(answer.id)}
                    >
                        추천
                        <span class="badge rounded-pill bg-success">{answer.voter.length}</span>
                    </button>
                    {#if answer.user && $username === answer.user.username}
                        <a use:link href="/answer-modify/{answer.id}" class="btn btn-sm btn-outline-secondary">수정</a>
                        <button class="btn btn-sm btn-outline-secondary" on:click={() => delete_answer(answer.id)}>삭제</button>
                    {/if}
                </div>
            </div>
        </div>
    {/each}

    <!-- 답변 페이징 처리 시작 -->
    <ul class="pagination justify-content-center">
        <li class="page-item {page + 1 >=  total_page && "disabled"}">
            <button on:click={() => {get_question(page + 1)}} class="page-link">더보기 ({page+1}/{total_page})</button>
        </li>
    </ul>
    <!-- 답변 페이징 처리 끝 -->
    
    <!-- 답변 등록 -->
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content} class="form-control" disabled={$is_login ? "" : "disabled"} />
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary" on:click="{post_answer}" disabled={$is_login ? "" : "disabled"} />
    </form>
</div>