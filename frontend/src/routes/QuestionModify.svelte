<script>
    import { push } from "svelte-spa-router";
    import fastapi from "../lib/api";
    import Error from "../components/Error.svelte";

    export let params = {}
    const question_id = params.question_id

    let error = {detail:[]}
    let subject = ""
    let content = ""
    
    // 수정할 질문 정보 가져오기
    fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
        subject = json.question.subject
        content = json.question.content
    })

    // 질문 수정 함수
    function update_question(event) {
        event.preventDefault()

        let url = "/api/question/update"
        let params = {
            id: question_id,
            subject: subject,
            content: content
        }

        fastapi("put", url, params, 
            (json) => {
                if(confirm("수정하시겠습니까?")) {
                    push("/detail/" + question_id)
                }
            },
            (json_error) => {
                error = json_error
            }
        )
    }

    // 취소하기
    function cancel(event) {
        event.preventDefault()
        if (confirm("수정을 취소하시겠습니까?")) {
            push("/detail/" + question_id)
        }
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">질문 수정</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" id="subject" bind:value={subject}>
        </div> 
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" id="content" rows="10" bind:value={content}></textarea>
        </div>
        <button class="btn btn-primary" on:click={update_question}>수정하기</button>
        <button class="btn btn-danger" on:click={cancel}>취소하기</button>
    </form>
</div>