<script>
    import moment from "moment/min/moment-with-locales"
    import { link, push } from "svelte-spa-router";
    import fastapi from "../lib/api";
    import { is_login, prev_page, username } from "../lib/store";
    import Error from "../components/Error.svelte";

    export let params = {}
    const board_id = params.board_id
    let board = {comments:[], user:[]}
    let content = ""
    let error = {detail:[]}

    $prev_page = "/board-detail/" + board_id

    // 게시글 가져오기
    function get_board_detail() {
        let url = "/api/boards/" + board_id

        fastapi("get", url, {}, 
            (json) => {
                board = json
            }, 
        )
    }
    get_board_detail()

    // 게시글 삭제
    function delete_board() {
        if (confirm("삭제하시겠습니까?")) {
            let url = "/api/boards/" + board_id
    
            fastapi("delete", url, {}, 
                (json) => {
                    push("/board")
                }, 
                (json_error) => {
                    error = json_error
                }
            )
        }
    }

    // 댓글 등록
    function post_comment(event) {
        event.preventDefault()  // submit이 눌릴경우 form이 자동으로 전동되는 것을 방지하기 위함
        
        let url = "/api/comments"
        let params = {
            board_id: board_id,
            content: content,
        }
        fastapi("post", url, params, 
            (json) => {
                content = ""
                error = {detail:[]}
                get_board_detail()
            }, 
            (err_json) => {
                error = err_json
            }
        )
    }

    // 댓글 삭제
    function delete_comment(comment_id){
        if (confirm("댓글을 삭제하시겠습니까?")) {
            let url = "/api/comments/" + comment_id
    
            fastapi("delete", url, {}, 
                (json) => {
                    get_board_detail()
                },
                (json_error) => {
                    error = json_error
                }
            )
        }
    }

</script>

<div class="container my-3">
    <!-- 게시글 -->
    <h2 class="border-bottom py-2">{board.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text">{board.content}</div>
            <div class="d-flex justify-content-end">
                {#if board.modify_date}
                    <div class="badge bg-light text-dark p-2 text-start mx-3">
                        <div class="mb-2">modified at</div>
                        <div>{moment(board.modify_date).format("YYYY년 MM월 DD일 HH:mm")}</div>
                    </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{board.user ? board.user.username : ""}</div>
                    <div>{moment(board.create_date).format("YYYY년 MM월 DD일 HH:mm")}</div>
                </div>
            </div>
            <div class="my-3">
                <button class="btn btn-sm">
                    추천
                    <span class="badge rounded-pill bg-success">0</span>
                </button>
                    {#if board.user.username === $username}
                        <a use:link href="/board-modify/{board.id}" class="btn btn-sm btn-outline-secondary">수정</a>
                        <button class="btn btn-sm btn-outline-secondary" on:click={delete_board}>삭제</button>
                    {/if}
            </div>
        </div>
    </div>
    <button class="btn btn-primary" on:click={() => push("/board")}>목록으로</button>

    <!-- 댓글 -->
    <div class="border-bottom my-3 py-2 d-flex justify-content-between">
        <h5>{board.comments.length}개의 댓글이 있습니다.</h5>
    </div>    
    {#each board.comments as comment}
        <div class="card my-3">
            <div class="card-body">
                <div class="card-text">{comment.content}</div>
                <div class="d-flex justify-content-end">
                    {#if comment.modify_date}
                        <div class="badge bg-light text-dark p-2 text-start mx-2">
                            <div class="mb-2">modified at</div>
                            <div>{moment(comment.modify_date).format("YYYY년 MM월 DD일 HH:mm")}</div>
                        </div>
                    {/if}
                    <div class="badge bg-light text-dark p-2 text-start">
                        <div class="mb-2">{comment.user.username}</div>
                        <div>{moment(comment.create_date).format("YYYY년 MM월 DD일 HH:mm")}</div>
                    </div>
                </div>
                <div class="my-3">
                    <button class="btn btn-sm">
                        추천
                        <span class="badge rounded-pill bg-success">0</span>
                    </button>
                    {#if comment.user.username === $username}
                        <a use:link href="/comment-modify/{comment.id}" class="btn btn-sm btn-outline-secondary">수정</a>
                        <button class="btn btn-sm btn-outline-secondary" on:click={() => delete_comment(comment.id)}>삭제</button>
                    {/if}
                </div>
            </div>
        </div>
    {/each}

    <!-- 댓글 등록 -->
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content} class="form-control" disabled={$is_login ? "" : "disabled"} />
        </div>
        <input type="submit" value="댓글등록" class="btn btn-primary" on:click="{post_comment}" disabled={$is_login ? "" : "disabled"} />
    </form>
</div>