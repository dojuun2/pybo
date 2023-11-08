<script>
    import { link } from "svelte-spa-router";
    import fastapi from "../lib/api";
    import { board_page } from "../lib/store";

    let board_list = []
    let size = 10
    let total = 0
    $: total_page = Math.ceil(total / size)

    function get_board_list() {
        let url = "/api/board/list"
        let params = {
            page: $board_page,
            size: size,
        }
        
        fastapi("get", url, params, 
            (json) => {
                board_list = json.board_list
                total = json.total
            }
        )
    }

    $: $board_page, get_board_list()
</script>

<div class="container my-3">
  <h2 class="border-bottom py-2">자유게시판</h2>
  <div class="row my-3">
      <div class="col-6">
        <a use:link href="/question-create" class="btn btn-primary">게시글 작성하기</a>
      </div>
      <div class="col-6">
        <div class="input-group">
          <input type="text" class="form-control">
          <button class="btn btn-outline-secondary">
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
                    </td>
                    <td>{board.user.username}</td>
                    <td>{board.create_date}</td>
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