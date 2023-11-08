<script>
  import { push } from "svelte-spa-router";
    import Error from "../components/Error.svelte";
    import fastapi from "../lib/api";

    export let params = {}
    const comment_id = params.comment_id

    let error = {detail:[]}
    let board_id = 0
    let content = ""

    // 댓글 정보 가져오기
    fastapi("get", "/api/comment/detail/" + comment_id, {}, (json) => {
        board_id = json.board_id
        content = json.content
    }) 

    // 수정 요청 함수
    function update_comment(event) {
        event.preventDefault()

        let url = "/api/comment/update"
        let params = {
            id: comment_id,
            content: content
        }

        fastapi("put", url, params, 
            (json) => {
                if(confirm("수정하시겠습니까?")) {
                    push("/board-detail/" + board_id)
                }
            }, 
            (json_error) => {
                error = json_error
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">댓글 수정</h5>
    <Error error={error} />
    <form method="post">
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value="{content}"></textarea>
        </div>
        <button class="btn btn-primary" on:click="{update_comment}">수정하기</button>
        <button class="btn btn-danger" on:click={(event) => {
            event.preventDefault()
            if (confirm("수정을 취소하시겠습니까?")) {
                push("/board-detail/" + board_id)
            }
        }}>취소하기</button>
    </form>
</div>