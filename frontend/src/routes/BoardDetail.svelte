<script>
    import moment from "moment/min/moment-with-locales"
    import { link } from "svelte-spa-router";
    import fastapi from "../lib/api";

    export let params = {}
    let board_id = params.board_id
    let board = {comments:[]}

    // 게시글 가져오기
    function get_board_detail() {
        let url = "/api/board/detail/" + board_id

        fastapi("get", url, {}, 
            (json) => {
                board = json
                console.log(board.comments);
            }, 
        )
    }

    get_board_detail()

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
                    <a use:link href="/question-modify/" class="btn btn-sm btn-outline-secondary">수정</a>
                    <button class="btn btn-sm btn-outline-secondary" >삭제</button>
            </div>
        </div>
    </div>
    <button class="btn btn-primary">목록으로</button>

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
                    <a use:link href="/answer-modify/" class="btn btn-sm btn-outline-secondary">수정</a>
                    <button class="btn btn-sm btn-outline-secondary">삭제</button>
                </div>
            </div>
        </div>
    {/each}
</div>