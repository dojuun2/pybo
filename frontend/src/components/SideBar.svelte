<script>
    import { link } from "svelte-spa-router";
    import { page, keyword, category, board_page, board_keyword } from "../lib/store"
</script>

<!-- 사이드바 -->
<div class="d-flex flex-column flex-shrink-0 p-3 bg-white my-3" style="width: 280px;">
    <ul class="nav nav-pills flex-column mb-auto">
        <li class="nav-item">
        <a use:link href="/" class="nav-link {$category === "home" && 'active'}" aria-current="page" on:click={() => {$category="home", $page = 0, $keyword = ""}}>
            <svg class="bi me-2" width="16" height="16"><use xlink:href="#home"></use></svg>
            질문과 답변
        </a>
        </li>
        <li>
        <a use:link href="/board" class="nav-link {$category === "board" && 'active'}" aria-current="page" on:click={() => {$category="board", $board_page = 0, $board_keyword = ""}} >
            <svg class="bi me-2" width="16" height="16"><use xlink:href="#speedometer2"></use></svg>
            자유게시판
        </a>
        </li>
    </ul>
</div>