<script>
    import { link } from "svelte-spa-router";
    import fastapi from "../lib/api";
    import moment from "moment/min/moment-with-locales"
    import { board_keyword, board_page, category, is_login, prev_page } from "../lib/store";

    $category = "board"
    $prev_page = "/board"

    let board_list = []
    let size = 10
    let total = 0
    let board_kw = ""
    $: total_page = Math.ceil(total / size)


    // 게시글 목록 가져오기
    function get_board_list() {
        let url = "/api/boards"
        let params = {
            page: $board_page,
            size: size,
            keyword: $board_keyword,
        }
        
        fastapi("get", url, params, 
            (json) => {
                board_list = json.board_list
                total = json.total
                board_kw = $board_keyword
            }
        )
    }
    
    $: $board_page, $board_keyword, get_board_list()
</script>

<div class="container my-3">
  <h2 class="border-bottom py-2">자유게시판</h2>
  <div class="row my-3">
      <div class="col-6">
        <a use:link href="/board-create" class="btn btn-primary {$is_login ? '' : 'disabled'}">게시글 작성하기</a>
      </div>
      <div class="col-6">
        <div class="input-group">
          <input type="text" class="form-control" bind:value="{board_kw}">
          <button class="btn btn-outline-secondary" on:click={() => {$board_keyword = board_kw, $board_page = 0}}>
            검색하기
          </button>
        </div>
      </div>
    </div>
    <!-- 글 목록 -->
    <table class="table text-center">
        <thead>
            <tr class="table-dark">
                <th>번호</th>
                <th style="width: 50%;">제목</th>
                <th>작성자</th>
                <th>작성일시</th>
                <th>조회수</th>
            </tr>
        </thead>
        <tbody>
            {#each board_list as board}
                <tr class="text-center">
                    <td>{board.id}</td>
                    <td class="text-start">
                        <a use:link href="/board-detail/{board.id}">{board.subject}</a>
                        {#if board.comments.length > 0}
                            <span class="text-danger small mx-2">{board.comments.length}</span>
                        {/if}
                    </td>
                    <td>{board.user.username}</td>
                    <td>{moment(board.create_date).format("YYYY년 MM월 DD일 HH:mm")}</td>
                    <td>{board.hits}</td>
                </tr>
            {/each}
        </tbody>
    </table>

    <!-- 페이징 처리 -->
    <ul class="pagination justify-content-center">
        <!-- 이전 -->
        <li class="page-item {$board_page <= 0 && 'disabled'}">
            <button class="page-link" on:click={() => $board_page--}>이전</button>
        </li>
        <!-- 페이지 번호 -->
        {#each Array(total_page) as _, loop_page}
            {#if loop_page >= $board_page - 5 && loop_page <= $board_page + 5}
                <li class="page-item {loop_page === $board_page && 'active'}">
                    <button class="page-link" on:click={() => $board_page = loop_page}>
                        {loop_page + 1}
                    </button>
                </li>
            {/if}
        {/each}
        <!-- 다음 -->
        <li class="page-item {$board_page >= total_page - 1 && 'disabled'}">
            <button class="page-link" on:click={() => $board_page++}>다음</button>
        </li>
    </ul>
</div>