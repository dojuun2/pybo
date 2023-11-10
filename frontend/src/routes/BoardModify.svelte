<script>
  import { push } from "svelte-spa-router";
    import Error from "../components/Error.svelte";
  import fastapi from "../lib/api";

    export let params = {}
    const board_id = params.board_id

    let error = {detail:[]}
    let subject = ""
    let content = ""

    // 수정할 게시글 가져오기
    function get_board_detail() {
        let url = "/api/boards/" + board_id
        
        fastapi("get", url, {}, (json) => {
            subject = json.subject
            content = json.content
        })
    }

    get_board_detail()

    // 수정 요청
    function update_board(event) {
        event.preventDefault()

        let url = "/api/boards"
        let params = {
            id: board_id,
            subject: subject,
            content: content,
        }

        fastapi("put", url, params, 
            (json) => {
                if (confirm("수정하시겠습니까?")) {
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
    <h5 class="my-3 border-bottom pb-2">게시글 수정</h5>
    <Error error = {error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" id="subject" bind:value={subject}>
        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea type="text" class="form-control" id="content" rows="10" bind:value={content} />
        </div>
        <button class="btn btn-primary" on:click={update_board}>수정하기</button>
        <button class="btn btn-danger">취소하기</button>
    </form>
</div>